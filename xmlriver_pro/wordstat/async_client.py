"""
Асинхронный клиент для работы с Yandex Wordstat API через XMLRiver
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import aiohttp

from ..core.async_base_client import AsyncBaseClient
from ..core.types import (
    WordstatKeyword,
    WordstatResponse,
    WordstatHistoryPoint,
    WordstatHistoryResponse,
)
from ..core.exceptions import (
    XMLRiverError,
    ValidationError,
    AuthenticationError,
    InsufficientFundsError,
    ServiceUnavailableError,
    RateLimitError,
    NetworkError,
)

logger = logging.getLogger(__name__)


class AsyncWordstatClient(AsyncBaseClient):
    """
    Асинхронный клиент для работы с Yandex Wordstat API через XMLRiver

    Поддерживает:
    - Получение топов запросов (associations и popular)
    - Получение динамики частотности запроса
    - Фильтрацию по регионам
    - Фильтрацию по устройствам
    - Группировку по периодам (месяц, неделя, день)
    """

    BASE_URL = "http://xmlriver.com/wordstat/new/json"

    def __init__(
        self,
        user_id: int,
        api_key: str,
        *,
        timeout: int = 60,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        enable_retry: bool = True,
        max_concurrent: int = 10,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """
        Инициализация асинхронного Wordstat клиента

        Args:
            user_id: ID пользователя XMLRiver
            api_key: API ключ
            timeout: Таймаут запроса в секундах (по умолчанию 60)
            max_retries: Максимум попыток повтора (по умолчанию 3)
            retry_delay: Базовая задержка между попытками в секундах (по умолчанию 1.0)
            enable_retry: Включить автоматические повторы (по умолчанию True)
            max_concurrent: Максимум одновременных запросов (по умолчанию 10)
            session: Существующая aiohttp сессия (опционально)
        """
        super().__init__(
            user_id=user_id,
            api_key=api_key,
            system="wordstat",
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            enable_retry=enable_retry,
            max_concurrent=max_concurrent,
            session=session,
        )

    async def get_words(
        self,
        query: str,
        *,
        regions: Optional[int] = None,
        device: Optional[str] = None,
    ) -> WordstatResponse:
        """
        Получение топов запросов (associations и popular)

        Args:
            query: Поисковый запрос
            regions: ID региона Яндекса (опционально)
            device: Устройства: desktop, phone, tablet или через запятую (опционально)

        Returns:
            WordstatResponse: Топы запросов

        Example:
            >>> async with AsyncWordstatClient(user_id=123, api_key="key") as client:
            ...     result = await client.get_words("python")
            ...     print(f"Associations: {len(result.associations)}")
            ...     print(f"Popular: {len(result.popular)}")
        """
        if not query or not query.strip():
            raise ValidationError(2, "Задан пустой поисковый запрос")

        params = self._build_params(
            query=query, pagetype="words", regions=regions, device=device
        )

        response = await self._make_wordstat_request(params)
        return self._parse_words_response(query, response)

    async def get_history(
        self,
        query: str,
        *,
        regions: Optional[int] = None,
        device: Optional[str] = None,
        period: str = "month",
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> WordstatHistoryResponse:
        """
        Получение динамики частотности запроса

        Args:
            query: Поисковый запрос
            regions: ID региона Яндекса (опционально)
            device: Устройства: desktop, phone, tablet или через запятую (опционально)
            period: Группировка по: month, week, day (по умолчанию month)
            start: Дата начала в формате dd.mm.yyyy (опционально)
            end: Дата окончания в формате dd.mm.yyyy (опционально)

        Returns:
            WordstatHistoryResponse: Динамика частотности

        Example:
            >>> async with AsyncWordstatClient(user_id=123, api_key="key") as client:
            ...     result = await client.get_history(
            ...         "python",
            ...         period="month",
            ...         start="01.01.2024",
            ...         end="31.03.2024"
            ...     )
            ...     print(f"Total value: {result.total_value}")
            ...     print(f"History points: {len(result.history)}")
        """
        if not query or not query.strip():
            raise ValidationError(2, "Задан пустой поисковый запрос")

        if period not in ["month", "week", "day"]:
            raise ValidationError(
                400, "Неверный период. Допустимые значения: month, week, day"
            )

        params = self._build_params(
            query=query,
            pagetype="history",
            regions=regions,
            device=device,
            period=period,
            start=start,
            end=end,
        )

        response = await self._make_wordstat_request(params)
        return self._parse_history_response(query, response)

    async def get_frequency(
        self,
        query: str,
        *,
        regions: Optional[int] = None,
        device: Optional[str] = None,
    ) -> int:
        """
        Получение общей частотности запроса за предыдущий месяц

        Метод использует вкладку "Динамика" и берет значение из поля totalValue.

        Args:
            query: Поисковый запрос
            regions: ID региона Яндекса (опционально)
            device: Устройства: desktop, phone, tablet или через запятую (опционально)

        Returns:
            int: Частотность запроса

        Example:
            >>> async with AsyncWordstatClient(user_id=123, api_key="key") as client:
            ...     frequency = await client.get_frequency("python")
            ...     print(f"Frequency: {frequency}")
        """
        history = await self.get_history(query, regions=regions, device=device)
        return history.total_value

    def _build_params(
        self,
        query: str,
        pagetype: str,
        regions: Optional[int] = None,
        device: Optional[str] = None,
        period: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Формирование параметров запроса"""
        # Заменяем амперсанд на код %26
        query = query.replace("&", "%26")

        params = {
            **self.base_params,
            "query": query,
            "pagetype": pagetype,
        }

        if regions is not None:
            params["regions"] = regions

        if device is not None:
            params["device"] = device

        if period is not None:
            params["period"] = period

        if start is not None:
            params["start"] = start

        if end is not None:
            params["end"] = end

        return params

    async def _make_wordstat_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполнение запроса к Wordstat API

        Args:
            params: Параметры запроса

        Returns:
            Dict[str, Any]: JSON ответ

        Raises:
            XMLRiverError: Ошибки API
        """
        if not self._session:
            raise RuntimeError(
                "Session не инициализирована. "
                "Используйте async with AsyncWordstatClient(...) as client:"
            )

        attempt = 0
        while attempt < self.max_retries:
            try:
                async with self._session.get(
                    self.BASE_URL, params=params
                ) as response:
                    text = await response.text()
                    data = await response.json()

                    # Проверяем наличие ошибки в ответе
                    if "code" in data and "error" in data:
                        self._handle_error(data["code"], data["error"])

                    return data

            except (aiohttp.ClientError, aiohttp.ServerTimeoutError) as e:
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
                    raise NetworkError(500, f"Сетевая ошибка: {e}") from e

        raise NetworkError(500, "Превышено максимальное количество попыток")

    def _handle_error(self, code: int, error: str) -> None:
        """Обработка ошибок Wordstat API"""
        if code == 2:
            raise ValidationError(code, error)
        if code in [31, 42, 45]:
            raise AuthenticationError(code, error)
        if code in [110, 115]:
            raise RateLimitError(code, error)
        if code == 200:
            raise InsufficientFundsError(code, error)
        if code in [101, 121]:
            raise ServiceUnavailableError(code, error)
        if code == 400:
            raise ValidationError(code, error)
        if code == 500:
            raise NetworkError(code, error)

        raise XMLRiverError(code, error)

    def _parse_words_response(
        self, query: str, data: Dict[str, Any]
    ) -> WordstatResponse:
        """Парсинг ответа с топами запросов"""
        associations: List[WordstatKeyword] = []
        popular: List[WordstatKeyword] = []

        # Парсим associations
        if "associations" in data and data["associations"]:
            for item in data["associations"]:
                # Убираем пробелы из числа (формат "38 721" -> "38721")
                value_str = str(item.get("value", "0")).replace(" ", "")
                associations.append(
                    WordstatKeyword(
                        text=item.get("text", ""),
                        value=int(value_str),
                        is_association=item.get("isAssociations", True),
                    )
                )

        # Парсим popular
        if "popular" in data and data["popular"]:
            for item in data["popular"]:
                # Убираем пробелы из числа
                value_str = str(item.get("value", "0")).replace(" ", "")
                popular.append(
                    WordstatKeyword(
                        text=item.get("text", ""),
                        value=int(value_str),
                        is_association=item.get("isAssociations", False),
                    )
                )

        return WordstatResponse(
            query=query, associations=associations, popular=popular
        )

    def _parse_history_response(
        self, query: str, data: Dict[str, Any]
    ) -> WordstatHistoryResponse:
        """Парсинг ответа с динамикой"""
        history: List[WordstatHistoryPoint] = []
        associations: List[WordstatKeyword] = []
        popular: List[WordstatKeyword] = []

        # Парсим totalValue (убираем пробелы)
        total_value_str = str(data.get("totalValue", "0")).replace(" ", "")
        total_value = int(total_value_str)

        # Парсим динамику из graph.tableData
        if "graph" in data and "tableData" in data["graph"]:
            for item in data["graph"]["tableData"]:
                # Убираем пробелы из absoluteValue
                abs_value_str = str(item.get("absoluteValue", "0")).replace(" ", "")
                history.append(
                    WordstatHistoryPoint(
                        date=item.get("text", ""),
                        absolute_value=int(abs_value_str),
                        relative_value=float(item.get("value", "0").replace(",", ".")),
                    )
                )

        # Парсим associations из table.tableData
        if (
            "table" in data
            and "tableData" in data["table"]
            and "associations" in data["table"]["tableData"]
        ):
            for item in data["table"]["tableData"]["associations"]:
                # Убираем пробелы из value
                value_str = str(item.get("value", "0")).replace(" ", "")
                associations.append(
                    WordstatKeyword(
                        text=item.get("text", ""),
                        value=int(value_str),
                        is_association=item.get("isAssociations", True),
                    )
                )

        # Парсим popular из table.tableData
        if (
            "table" in data
            and "tableData" in data["table"]
            and "popular" in data["table"]["tableData"]
        ):
            for item in data["table"]["tableData"]["popular"]:
                # Убираем пробелы из value
                value_str = str(item.get("value", "0")).replace(" ", "")
                popular.append(
                    WordstatKeyword(
                        text=item.get("text", ""),
                        value=int(value_str),
                        is_association=item.get("isAssociations", False),
                    )
                )

        return WordstatHistoryResponse(
            query=query,
            total_value=total_value,
            history=history,
            associations=associations,
            popular=popular,
        )

    async def get_balance(self) -> float:
        """
        Получение текущего баланса счета

        Returns:
            float: Баланс в рублях

        Example:
            >>> async with AsyncWordstatClient(user_id=123, api_key="key") as client:
            ...     balance = await client.get_balance()
            ...     print(f"Balance: {balance} руб.")
        """
        # Wordstat использует тот же endpoint, что и Google/Yandex для баланса
        params = {**self.base_params, "action": "get_balance"}

        if not self._session:
            raise RuntimeError(
                "Session не инициализирована. "
                "Используйте async with AsyncWordstatClient(...) as client:"
            )

        try:
            async with self._session.get(
                "http://xmlriver.com/search/xml", params=params
            ) as response:
                text = await response.text()
                # Парсим XML ответ
                import xmltodict

                data = xmltodict.parse(text)
                if "yandexsearch" in data and "response" in data["yandexsearch"]:
                    balance_str = data["yandexsearch"]["response"].get("balance", "0")
                    return float(balance_str)
                return 0.0
        except Exception:
            # Если не удалось получить баланс, возвращаем 0
            return 0.0

    def get_concurrent_status(self) -> Dict[str, int]:
        """
        Получение статуса семафора (количество активных запросов)

        Returns:
            Dict[str, int]: Статус с ключами 'active_requests', 'max_concurrent',
                'available_slots'
        """
        return {
            "active_requests": self._active_requests,
            "max_concurrent": self.max_concurrent,
            "available_slots": self.max_concurrent - self._active_requests,
        }

