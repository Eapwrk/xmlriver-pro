"""
Google Images API для XMLRiver Pro
"""

from typing import Optional, List
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, ImageResult


class GoogleImages(BaseClient):
    """Клиент для работы с Google Images через XMLRiver"""

    BASE_URL = "http://xmlriver.com/search/xml"

    def search_images(
        self,
        query: str,
        count: int = 50,
        page: int = 1,
        country: Optional[int] = None,
        device: str = "desktop",
        **kwargs,
    ) -> SearchResponse:
        """
        Поиск по изображениям Google

        Args:
            query: Поисковый запрос
            count: Количество изображений (максимум 50)
            page: Номер страницы
            country: ID страны
            device: Тип устройства
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска изображений
        """
        # Для изображений groupby всегда = 50
        params = {
            **self.base_params,
            "query": query,
            "setab": "images",
            "groupby": 50,  # Фиксированное значение для изображений
            "page": page,
            "device": device,
        }

        if country:
            params["country"] = country

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_image_results(response)

    def _parse_image_results(self, response: dict) -> SearchResponse:
        """Парсинг результатов поиска изображений"""
        found = response.get("found", {})
        total = int(found.get("#text", 0)) if isinstance(found, dict) else 0

        groups = response.get("results", {}).get("grouping", {}).get("group", [])
        if not isinstance(groups, list):
            groups = [groups] if groups else []

        results = []
        for rank, group in enumerate(groups, 1):
            doc = group.get("doc", {})
            result = ImageResult(
                rank=rank,
                url=doc.get("url", ""),
                img_url=doc.get("imgurl", ""),
                title=doc.get("title", ""),
                display_link=doc.get("displaylink", ""),
                original_width=self._extract_dimension(doc.get("originalwidth")),
                original_height=self._extract_dimension(doc.get("originalheight")),
            )
            results.append(result)

        return SearchResponse(
            query=response.get("query", ""),
            total_results=total,
            results=results,
            showing_results_for=response.get("showing_results_for"),
        )

    def _extract_dimension(self, value) -> Optional[int]:
        """Извлечение размеров изображения"""
        if value:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        return None

    def search_images_by_size(
        self, query: str, size: str = "large", **kwargs
    ) -> SearchResponse:
        """
        Поиск изображений по размеру

        Args:
            query: Поисковый запрос
            size: Размер изображений (small, medium, large, xlarge)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска изображений
        """
        params = {"tbs": f"isz:{size}"}
        params.update(kwargs)
        return self.search_images(query, **params)

    def search_images_by_color(
        self, query: str, color: str = "any", **kwargs
    ) -> SearchResponse:
        """
        Поиск изображений по цвету

        Args:
            query: Поисковый запрос
            color: Цвет (any, color, grayscale, transparent, red, orange, yellow,
                         green, teal, blue, purple, pink, white, gray, black, brown)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска изображений
        """
        params = {"tbs": f"ic:{color}"}
        params.update(kwargs)
        return self.search_images(query, **params)

    def search_images_by_type(
        self, query: str, image_type: str = "any", **kwargs
    ) -> SearchResponse:
        """
        Поиск изображений по типу

        Args:
            query: Поисковый запрос
            image_type: Тип изображения (any, face, photo, clipart, lineart, animated)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска изображений
        """
        params = {"tbs": f"itp:{image_type}"}
        params.update(kwargs)
        return self.search_images(query, **params)

    def search_images_by_usage_rights(
        self, query: str, usage_rights: str = "any", **kwargs
    ) -> SearchResponse:
        """
        Поиск изображений по правам использования

        Args:
            query: Поисковый запрос
            usage_rights: Права использования (any, cc_publicdomain,
                         cc_attribute, cc_sharealike, cc_noncommercial,
                         cc_nonderived)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска изображений
        """
        params = {"tbs": f"sur:{usage_rights}"}
        params.update(kwargs)
        return self.search_images(query, **params)

    def get_suggested_searches(self, query: str, **kwargs) -> List[str]:
        """
        Получить предложенные поисковые запросы для изображений

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Список предложенных запросов
        """
        response = self.search_images(query, **kwargs)

        # Извлекаем suggestedsearches из ответа
        suggested_searches = response.get("suggestedsearches", {}).get("item", [])
        if isinstance(suggested_searches, list):
            return [
                item.get("name", "") for item in suggested_searches if item.get("name")
            ]
        if isinstance(suggested_searches, dict) and suggested_searches.get("name"):
            return [suggested_searches.get("name", "")]

        return []
