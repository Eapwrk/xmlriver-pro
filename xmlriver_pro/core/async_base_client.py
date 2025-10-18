"""
Асинхронный базовый клиент для XMLRiver API
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import aiohttp
import xmltodict

from .types import DeviceType, OSType, SearchType

from .exceptions import (
    XMLRiverError,
    AuthenticationError,
    RateLimitError,
    NetworkError,
    APIError,
)
from .types import SearchResponse

logger = logging.getLogger(__name__)

# Константы для API
DEFAULT_TIMEOUT = 60
MAX_TIMEOUT = 60
TYPICAL_RESPONSE_TIME = 3.0
DAILY_LIMITS = {"google": 200_000, "yandex": 150_000}
MAX_CONCURRENT_STREAMS = 10


class AsyncBaseClient:  # pylint: disable=too-many-instance-attributes
    """
    Асинхронный базовый клиент для работы с XMLRiver API

    Предоставляет общую функциональность для всех типов поиска
    с поддержкой асинхронных HTTP запросов через aiohttp.
    """

    BASE_URL: Optional[str] = None

    def __init__(
        self,
        user_id: int,
        api_key: str,
        system: str,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        enable_retry: bool = True,
        max_concurrent: int = MAX_CONCURRENT_STREAMS,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """
        Инициализация асинхронного клиента

        Args:
            user_id: ID пользователя XMLRiver
            api_key: API ключ
            system: Система поиска (google/yandex)
            timeout: Таймаут запроса в секундах
            max_retries: Максимальное количество попыток повтора (по умолчанию 3)
            retry_delay: Базовая задержка между попытками в секундах (по умолчанию 1.0)
            enable_retry: Включить автоматические повторы (по умолчанию True)
            max_concurrent: Максимум одновременных запросов (по умолчанию 10)
            session: Существующая aiohttp сессия (опционально)
        """
        self.user_id = user_id
        self.api_key = api_key
        self.system = system
        self.timeout = min(timeout, 60)  # Максимум 60 секунд как в BaseClient
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.enable_retry = enable_retry
        self.max_concurrent = max_concurrent
        self._session = session
        self._own_session = session is None
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._active_requests = 0
        self.base_params = {"user": self.user_id, "key": self.api_key}

    async def __aenter__(self) -> "AsyncBaseClient":
        """Async context manager entry"""
        if self._own_session:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit"""
        if self._own_session and self._session:
            await self._session.close()

    async def _make_request(
        self, url: str, params: Dict[str, Any], search_type: str = "web"
    ) -> SearchResponse:
        """
        Выполнение асинхронного HTTP запроса к API с retry механизмом и
        ограничением потоков

        Args:
            url: Полный URL для запроса
            params: Параметры запроса
            search_type: Тип поиска

        Returns:
            SearchResponse: Результат поиска

        Raises:
            XMLRiverError: Общая ошибка API
            AuthenticationError: Ошибка аутентификации
            RateLimitError: Превышение лимитов
            NetworkError: Сетевая ошибка
        """
        # Ограничиваем количество активных запросов на уровне клиента
        async with self._semaphore:
            self._active_requests += 1
            try:
                if not self.enable_retry:
                    return await self._make_single_request(url, params, search_type)

                attempt = 0
                while attempt < self.max_retries:
                    try:
                        return await self._make_single_request(url, params, search_type)
                    except (RateLimitError, NetworkError) as e:
                        attempt += 1
                        if attempt < self.max_retries:
                            delay = self.retry_delay * (2 ** (attempt - 1))
                            logger.warning(
                                "Request failed: %s. Retrying in %.1f seconds... "
                                "(attempt %s/%s)",
                                e,
                                delay,
                                attempt,
                                self.max_retries,
                            )
                            await asyncio.sleep(delay)
                        else:
                            logger.error("Max retries (%s) exceeded", self.max_retries)
                            raise

                raise NetworkError(999, "Max retries exceeded")
            finally:
                self._active_requests -= 1

    async def _make_single_request(
        self, url: str, params: Dict[str, Any], search_type: str = "web"
    ) -> SearchResponse:
        """
        Выполнение одиночного асинхронного HTTP запроса к API без повторов

        Args:
            url: Полный URL для запроса
            params: Параметры запроса
            search_type: Тип поиска

        Returns:
            SearchResponse: Результат поиска

        Raises:
            XMLRiverError: Общая ошибка API
            AuthenticationError: Ошибка аутентификации
            RateLimitError: Превышение лимитов
            NetworkError: Сетевая ошибка
        """
        if not self._session:
            raise XMLRiverError(999, "Client session not initialized")

        # Добавляем обязательные параметры
        params.update(
            {
                "user": self.user_id,
                "key": self.api_key,
                "system": self.system,
                "query": params.get("query", ""),
            }
        )

        # URL уже полный, используем как есть

        try:
            response = await self._session.get(url, params=params)
            async with response as resp:
                # Проверяем статус ответа
                if resp.status == 401:
                    raise AuthenticationError(401, "Invalid API key or user ID")
                if resp.status == 429:
                    raise RateLimitError(429, "Rate limit exceeded")
                if resp.status != 200:
                    raise NetworkError(resp.status, f"HTTP {resp.status}")

                # Читаем и парсим ответ
                text = await resp.text()
                return await self._parse_response(
                    text, search_type, params.get("query", "")
                )

        except aiohttp.ClientError as e:
            raise NetworkError(999, f"Network error: {e}") from e
        except asyncio.TimeoutError:
            raise NetworkError(999, f"Request timeout after {self.timeout}s") from None

    async def _parse_response(
        self, xml_text: str, search_type: str, query: str = ""
    ) -> SearchResponse:
        """
        Парсинг XML ответа от API

        Args:
            xml_text: XML текст ответа
            search_type: Тип поиска

        Returns:
            SearchResponse: Структурированный ответ

        Raises:
            XMLRiverError: Ошибка парсинга
        """
        try:
            # Парсим XML в словарь
            data = xmltodict.parse(xml_text)

            # Извлекаем корневой элемент
            root_key = list(data.keys())[0]
            response_data = data[root_key]

            # Проверяем наличие ошибок в response
            if "response" in response_data and "error" in response_data["response"]:
                error_data = response_data["response"]["error"]
                error_code = int(error_data.get("@code", 999))
                error_message = error_data.get("#text", "Unknown error")
                raise APIError(error_code, error_message)
            if "error" in response_data:
                error_code = int(response_data["error"].get("@code", 999))
                error_message = response_data["error"].get("#text", "Unknown error")
                raise APIError(error_code, error_message)

            # Создаем SearchResponse
            # Извлекаем total из response.found для Google/Yandex API
            total_results = 0
            if "response" in response_data and "found" in response_data["response"]:
                found_data = response_data["response"]["found"]
                if isinstance(found_data, dict) and "#text" in found_data:
                    total_results = int(found_data["#text"])
                else:
                    total_results = int(found_data)
            elif "total" in response_data:
                total_results = int(response_data["total"])

            # Извлекаем дополнительные поля для исправлений и подсказок
            response_obj = response_data.get("response", {})
            showing_results_for = response_obj.get("showing_results_for")
            correct = response_obj.get("correct")
            fixtype = response_obj.get("fixtype")

            return SearchResponse(
                query=response_data.get("query", query),
                total_results=total_results,
                results=self._extract_results(response_data, search_type),
                showing_results_for=showing_results_for,
                correct=correct,
                fixtype=fixtype,
            )

        except Exception as e:
            if isinstance(e, (APIError, XMLRiverError)):
                raise
            raise XMLRiverError(999, f"Failed to parse response: {e}") from e

    def _extract_results(self, data: Dict[str, Any], search_type: str) -> list:
        """Извлечение результатов из ответа API"""
        # Базовая реализация - переопределяется в дочерних классах
        return []

    def get_api_limits(self) -> Dict[str, Any]:
        """
        Получить информацию об ограничениях API

        Returns:
            Словарь с ограничениями API
        """
        return {
            "max_concurrent_streams": MAX_CONCURRENT_STREAMS,
            "default_timeout": DEFAULT_TIMEOUT,
            "max_timeout": MAX_TIMEOUT,
            "typical_response_time": TYPICAL_RESPONSE_TIME,
            "daily_limits": DAILY_LIMITS,
            "recommendations": {
                "timeout": "Используйте таймаут 60 секунд для надежности",
                "concurrent_requests": (
                    f"Максимум {MAX_CONCURRENT_STREAMS} одновременных запросов"
                ),
                "daily_limits": (
                    f"Google: {DAILY_LIMITS['google']:,}, "
                    f"Yandex: {DAILY_LIMITS['yandex']:,} запросов в день"
                ),
            },
        }

    def get_concurrent_status(self) -> Dict[str, Any]:
        """
        Получение информации о текущем состоянии семафора

        Returns:
            Словарь с информацией о семафоре
        """
        return {
            "max_concurrent": self.max_concurrent,
            "active_requests": self._active_requests,
            "available_slots": self.max_concurrent - self._active_requests,
            "semaphore_value": self._semaphore._value,  # pylint: disable=protected-access
        }

    async def search(
        self,
        query: str,
        *,
        groupby: int = 10,
        page: int = 1,
        device: DeviceType = DeviceType.DESKTOP,
        search_type: SearchType = SearchType.ORGANIC,
        num_results: int = 10,
        start: int = 0,
        os: Optional[OSType] = None,
        lr: Optional[int] = None,
        lang: Optional[str] = None,
        domain: Optional[str] = None,
        country: Optional[int] = None,
        **kwargs: Any,
    ) -> SearchResponse:
        """
        Базовый асинхронный метод поиска

        Args:
            query: Поисковый запрос
            groupby: Количество результатов
            page: Номер страницы
            device: Тип устройства
            search_type: Тип поиска
            num_results: Количество результатов
            start: Начальная позиция
            os: Операционная система
            lr: ID региона (Yandex)
            lang: Язык (Yandex)
            domain: Домен (Yandex)
            country: ID страны (Google)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        if not self.BASE_URL:
            raise NotImplementedError("BASE_URL must be defined in a subclass")

        params = {
            **self.base_params,
            "query": query,
            "groupby": kwargs.get("groupby", 10),
            "page": kwargs.get("page", 1),
            "device": device.value,
            "type": search_type.value,
            "num": num_results,
            "start": start,
        }
        if os:
            params["os"] = os.value
        if lr:
            params["lr"] = lr
        if lang:
            params["lang"] = lang
        if domain:
            params["domain"] = domain
        if country:
            params["country"] = country

        params.update(kwargs)

        return await self._make_request(self.BASE_URL, params, search_type.value)

    async def close(self) -> None:
        """Закрытие клиента и освобождение ресурсов"""
        if self._session and self._own_session:
            await self._session.close()
            self._session = None
