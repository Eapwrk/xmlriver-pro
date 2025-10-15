"""
Асинхронный базовый клиент для XMLRiver API
"""

import asyncio
import logging
from typing import Dict, Any, Optional

import aiohttp
import xmltodict

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


class AsyncBaseClient:
    """
    Асинхронный базовый клиент для работы с XMLRiver API

    Предоставляет общую функциональность для всех типов поиска
    с поддержкой асинхронных HTTP запросов через aiohttp.
    """

    def __init__(
        self,
        user_id: int,
        api_key: str,
        system: str,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        enable_retry: bool = True,
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
            session: Существующая aiohttp сессия (опционально)
        """
        self.user_id = user_id
        self.api_key = api_key
        self.system = system
        self.timeout = min(timeout, 60)  # Максимум 60 секунд как в BaseClient
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.enable_retry = enable_retry
        self._session = session
        self._own_session = session is None

    async def __aenter__(self):
        """Async context manager entry"""
        if self._own_session:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._own_session and self._session:
            await self._session.close()

    async def _make_request(
        self, url: str, params: Dict[str, Any], search_type: str = "web"
    ) -> SearchResponse:
        """
        Выполнение асинхронного HTTP запроса к API с retry механизмом

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
            elif "error" in response_data:
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
            showing_results_for = None
            correct = None
            fixtype = None

            if "response" in response_data:
                response_obj = response_data["response"]
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

    async def get_api_limits(self) -> Dict[str, Any]:
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

    async def close(self):
        """Закрытие клиента и освобождение ресурсов"""
        if self._session and self._own_session:
            await self._session.close()
            self._session = None
