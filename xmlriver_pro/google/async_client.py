"""
Асинхронный клиент для Google Search API через XMLRiver
"""

from typing import Dict, Any, Optional, List

from ..core.async_base_client import AsyncBaseClient
from ..core.types import (
    SearchResponse,
    SearchResult,
    NewsResult,
    ImageResult,
    MapResult,
    AdResult,
    OneBoxDocument,
    KnowledgeGraph,
    SearchType,
    TimeFilter,
    DeviceType,
    OSType,
)
from ..core.exceptions import ValidationError
from ..utils.validators import (
    validate_coords,
    validate_zoom,
    validate_query,
    validate_device,
    validate_os,
)


class AsyncGoogleClient(AsyncBaseClient):
    """
    Асинхронный клиент для Google Search API

    Поддерживает все типы поиска Google через XMLRiver API:
    - Органический поиск
    - Поиск новостей
    - Поиск изображений
    - Поиск по картам
    - Рекламные блоки
    - Специальные блоки
    """

    BASE_URL = "http://xmlriver.com/search/xml"

    def __init__(
        self,
        user_id: int,
        api_key: str,
        timeout: int = 60,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        enable_retry: bool = True,
        max_concurrent: int = 10,
        session: Optional[Any] = None,
    ):
        """
        Инициализация асинхронного Google клиента

        Args:
            user_id: ID пользователя XMLRiver
            api_key: API ключ
            timeout: Таймаут запроса в секундах
            max_retries: Максимальное количество попыток повтора
            retry_delay: Базовая задержка между попытками в секундах
            enable_retry: Включить автоматические повторы
            max_concurrent: Максимум одновременных запросов (по умолчанию 10)
            session: Существующая aiohttp сессия
        """
        super().__init__(
            user_id=user_id,
            api_key=api_key,
            system="google",
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            enable_retry=enable_retry,
            max_concurrent=max_concurrent,
            session=session,
        )

    async def search(
        self,
        query: str,
        search_type: SearchType = SearchType.ORGANIC,
        num_results: int = 10,
        start: int = 0,
        device: DeviceType = DeviceType.DESKTOP,
        os: Optional[OSType] = None,
        lr: Optional[int] = None,
        lang: Optional[str] = None,
        domain: Optional[str] = None,
        country: Optional[int] = None,
        **kwargs,
    ) -> SearchResponse:
        """
        Асинхронный поиск в Google

        Args:
            query: Поисковый запрос
            search_type: Тип поиска (web, news, images, maps)
            num_results: Количество результатов
            start: Начальная позиция
            device: Тип устройства
            os: Операционная система
            **kwargs: Дополнительные параметры

        Returns:
            SearchResponse: Результаты поиска
        """
        # Валидация параметров
        validate_query(query)
        validate_device(device)
        validate_os(os)

        if not 1 <= num_results <= 100:
            raise ValidationError(400, "num_results must be between 1 and 100")
        if start < 0:
            raise ValidationError(400, "start must be non-negative")

        # Параметры запроса
        params = {
            "query": query,
            "type": search_type.value,
            "num": num_results,
            "start": start,
            "device": device.value,
            **kwargs,
        }
        if os:
            params["os"] = os.value

        return await self._make_request(self.BASE_URL, params, search_type.value)

    async def search_news(
        self,
        query: str,
        num_results: int = 10,
        start: int = 0,
        time_filter: Optional[TimeFilter] = None,
        **kwargs,
    ) -> SearchResponse:
        """
        Асинхронный поиск новостей в Google

        Args:
            query: Поисковый запрос
            num_results: Количество результатов
            start: Начальная позиция
            time_filter: Фильтр по времени
            **kwargs: Дополнительные параметры

        Returns:
            SearchResponse: Результаты поиска новостей
        """
        params = {
            "query": query,
            "type": "news",
            "num": num_results,
            "start": start,
            **kwargs,
        }

        if time_filter:
            params["time"] = time_filter.value

        return await self._make_request(self.BASE_URL, params, "news")

    async def search_images(
        self,
        query: str,
        num_results: int = 10,
        start: int = 0,
        size: Optional[str] = None,
        color: Optional[str] = None,
        image_type: Optional[str] = None,
        **kwargs,
    ) -> SearchResponse:
        """
        Асинхронный поиск изображений в Google

        Args:
            query: Поисковый запрос
            num_results: Количество результатов
            start: Начальная позиция
            size: Размер изображений (large, medium, small)
            color: Цвет изображений (color, grayscale, transparent)
            image_type: Тип изображений (photo, clipart, lineart)
            **kwargs: Дополнительные параметры

        Returns:
            SearchResponse: Результаты поиска изображений
        """
        params = {
            "query": query,
            "type": "images",
            "num": num_results,
            "start": start,
            **kwargs,
        }

        if size:
            params["imgsz"] = size
        if color:
            params["imgc"] = color
        if image_type:
            params["imgtype"] = image_type

        return await self._make_request(self.BASE_URL, params, "images")

    async def search_maps(
        self,
        query: str,
        coords: Optional[tuple] = None,
        zoom: Optional[int] = None,
        num_results: int = 10,
        **kwargs,
    ) -> SearchResponse:
        """
        Асинхронный поиск по картам Google

        Args:
            query: Поисковый запрос
            coords: Координаты (широта, долгота)
            zoom: Уровень масштабирования
            num_results: Количество результатов
            **kwargs: Дополнительные параметры

        Returns:
            SearchResponse: Результаты поиска по картам
        """
        params = {"query": query, "type": "maps", "num": num_results, **kwargs}

        if coords:
            validate_coords(coords)
            params["coords"] = f"{coords[0]},{coords[1]}"

        if zoom:
            validate_zoom(zoom)
            params["zoom"] = zoom

        return await self._make_request(self.BASE_URL, params, "maps")

    async def get_ads(
        self, query: str, num_results: int = 10, **kwargs
    ) -> SearchResponse:
        """
        Асинхронное получение рекламных блоков Google

        Args:
            query: Поисковый запрос
            num_results: Количество результатов
            **kwargs: Дополнительные параметры

        Returns:
            SearchResponse: Рекламные блоки
        """
        params = {"query": query, "type": "ads", "num": num_results, **kwargs}

        return await self._make_request(self.BASE_URL, params, "ads")

    async def get_special_blocks(self, query: str, **kwargs) -> SearchResponse:
        """
        Асинхронное получение специальных блоков Google

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            SearchResponse: Специальные блоки (OneBox, Knowledge Graph)
        """
        params = {"query": query, "type": "special", **kwargs}

        return await self._make_request(self.BASE_URL, params, "special")

    def _extract_results(
        self, data: Dict[str, Any], search_type: str
    ) -> List[SearchResult]:
        """Извлечение результатов из ответа Google API"""
        results = []

        # Извлекаем основные результаты из Google API структуры (как в Yandex)
        if "response" in data and "results" in data["response"]:
            response_data = data["response"]
            if (
                "grouping" in response_data["results"]
                and "group" in response_data["results"]["grouping"]
            ):
                groups = response_data["results"]["grouping"]["group"]
                if not isinstance(groups, list):
                    groups = [groups]

                for group in groups:
                    if "doc" in group:
                        doc = group["doc"]
                        result = self._create_search_result(doc, search_type)
                        if result:
                            results.append(result)
        elif "results" in data and "result" in data["results"]:
            # Fallback для старого формата
            results_data = data["results"]["result"]
            if not isinstance(results_data, list):
                results_data = [results_data]

            for item in results_data:
                result = self._create_search_result(item, search_type)
                if result:
                    results.append(result)

        # Извлекаем специальные блоки Google
        if "special_blocks" in data:
            special_blocks = data["special_blocks"]
            if isinstance(special_blocks, dict):
                for block_type, block_data in special_blocks.items():
                    if block_type == "onebox" and isinstance(block_data, dict):
                        onebox = OneBoxDocument(
                            content_type="onebox",
                            title=block_data.get("title", ""),
                            url=block_data.get("url", ""),
                            snippet=block_data.get("snippet", ""),
                        )
                        results.append(onebox)

                    elif block_type == "knowledge_graph" and isinstance(
                        block_data, dict
                    ):
                        kg = KnowledgeGraph(
                            entity_name=block_data.get("title", ""),
                            description=block_data.get("description", ""),
                            image_url=block_data.get("image_url", ""),
                            additional_info=block_data.get("attributes", {}),
                        )
                        results.append(kg)

        return results

    async def get_balance(self) -> float:
        """
        Получение текущего баланса счета XMLRiver

        Баланс единый для всего аккаунта (Google, Yandex, Wordstat).

        Returns:
            float: Баланс в рублях

        Example:
            >>> async with AsyncGoogleClient(user_id=123, api_key="key") as client:
            ...     balance = await client.get_balance()
            ...     print(f"Баланс: {balance} руб.")
        """
        if not self._session:
            raise RuntimeError(
                "Session не инициализирована. "
                "Используйте async with AsyncGoogleClient(...) as client:"
            )

        params = {"user": self.user_id, "key": self.api_key}
        url = "http://xmlriver.com/api/get_balance/"

        try:
            async with self._session.get(url, params=params) as response:
                text = await response.text()
                return float(text.strip())
        except (ValueError, Exception):
            return 0.0

    async def get_cost(self) -> float:
        """
        Получение стоимости запросов для Google

        Стоимость зависит от системы поиска (Google/Yandex имеют разные цены).

        Returns:
            float: Стоимость за 1000 запросов в рублях

        Example:
            >>> async with AsyncGoogleClient(user_id=123, api_key="key") as client:
            ...     cost = await client.get_cost()
            ...     print(f"Стоимость Google: {cost} руб/1000 запросов")
        """
        if not self._session:
            raise RuntimeError(
                "Session не инициализирована. "
                "Используйте async with AsyncGoogleClient(...) as client:"
            )

        params = {"user": self.user_id, "key": self.api_key}
        url = "http://xmlriver.com/api/get_cost/google/"

        try:
            async with self._session.get(url, params=params) as response:
                text = await response.text()
                return float(text.strip())
        except (ValueError, Exception):
            return 0.0

    def _create_search_result(
        self, item: Dict[str, Any], search_type: str
    ) -> Optional[SearchResult]:
        """Создание объекта результата поиска"""
        try:
            # Извлекаем snippet из passages для Google API (как в Yandex)
            snippet = ""
            if "passages" in item and "passage" in item["passages"]:
                passages = item["passages"]["passage"]
                if isinstance(passages, list):
                    snippet = " ".join(passages)
                else:
                    snippet = str(passages)

            if search_type == "news":
                return NewsResult(
                    rank=int(item.get("position", 0)),
                    url=item.get("url", ""),
                    title=item.get("title", ""),
                    snippet=snippet or item.get("snippet", ""),
                    media=item.get("media"),
                    pub_date=item.get("pub_date"),
                )
            if search_type == "images":
                return ImageResult(
                    rank=int(item.get("position", 0)),
                    url=item.get("url", ""),
                    img_url=item.get("img_url", ""),
                    title=item.get("title", ""),
                    display_link=item.get("display_link", ""),
                    original_width=(
                        int(item.get("original_width"))
                        if item.get("original_width")
                        else None
                    ),
                    original_height=(
                        int(item.get("original_height"))
                        if item.get("original_height")
                        else None
                    ),
                )
            if search_type == "maps":
                return MapResult(
                    title=item.get("title", ""),
                    stars=(float(item.get("stars")) if item.get("stars") else None),
                    type=item.get("type"),
                    address=item.get("address"),
                    url=item.get("url"),
                    phone=item.get("phone"),
                    review=item.get("review"),
                    possibility=item.get("possibility"),
                    latitude=(
                        float(item.get("latitude")) if item.get("latitude") else None
                    ),
                    longitude=(
                        float(item.get("longitude")) if item.get("longitude") else None
                    ),
                    place_id=item.get("place_id"),
                    count_reviews=(
                        int(item.get("count_reviews"))
                        if item.get("count_reviews")
                        else None
                    ),
                    accessibility=(
                        bool(item.get("accessibility"))
                        if item.get("accessibility") is not None
                        else None
                    ),
                )
            if search_type == "ads":
                return AdResult(
                    url=item.get("url", ""),
                    ads_url=item.get("ads_url", ""),
                    title=item.get("title", ""),
                    snippet=snippet or item.get("snippet", ""),
                )
            # web
            return SearchResult(
                rank=int(item.get("position", 0)),
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=snippet or item.get("snippet", ""),
            )
        except (ValueError, KeyError) as _:
            # Логируем ошибку и возвращаем None
            return None
