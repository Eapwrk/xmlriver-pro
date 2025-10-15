"""
Асинхронный базовый клиент для XMLRiver API
"""

import asyncio
import aiohttp
import xmltodict
from typing import Dict, Any, Optional

from .exceptions import (
    XMLRiverError,
    AuthenticationError,
    RateLimitError,
    NetworkError,
    APIError,
)
from .types import SearchResponse

# Константы для API
BASE_URL = "https://xmlriver.com/api"
DEFAULT_TIMEOUT = 60
MAX_TIMEOUT = 300
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
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """
        Инициализация асинхронного клиента

        Args:
            user_id: ID пользователя XMLRiver
            api_key: API ключ
            system: Система поиска (google/yandex)
            timeout: Таймаут запроса в секундах
            session: Существующая aiohttp сессия (опционально)
        """
        self.user_id = user_id
        self.api_key = api_key
        self.system = system
        self.timeout = min(timeout, MAX_TIMEOUT)
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
        self, endpoint: str, params: Dict[str, Any], search_type: str = "web"
    ) -> SearchResponse:
        """
        Выполнение асинхронного HTTP запроса к API

        Args:
            endpoint: Конечная точка API
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

        # Формируем URL
        url = f"{BASE_URL}/{endpoint}"

        try:
            response = await self._session.get(url, params=params)
            async with response as resp:
                # Проверяем статус ответа
                if resp.status == 401:
                    raise AuthenticationError(401, "Invalid API key or user ID")
                elif resp.status == 429:
                    raise RateLimitError(429, "Rate limit exceeded")
                elif resp.status != 200:
                    raise NetworkError(resp.status, f"HTTP {resp.status}")

                # Читаем и парсим ответ
                text = await resp.text()
                return await self._parse_response(text, search_type)

        except aiohttp.ClientError as e:
            raise NetworkError(999, f"Network error: {e}") from e
        except asyncio.TimeoutError:
            raise NetworkError(999, f"Request timeout after {self.timeout}s") from None

    async def _parse_response(self, xml_text: str, search_type: str) -> SearchResponse:
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

            # Проверяем наличие ошибок
            if "error" in response_data:
                error_code = int(response_data["error"].get("@code", 999))
                error_message = response_data["error"].get("#text", "Unknown error")
                raise APIError(error_code, error_message)

            # Создаем SearchResponse
            return SearchResponse(
                query=response_data.get("query", ""),
                total_results=int(response_data.get("total", 0)),
                results=self._extract_results(response_data, search_type),
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
