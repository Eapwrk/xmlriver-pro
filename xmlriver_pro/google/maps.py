"""
Google Maps API для XMLRiver Pro
"""

from typing import Optional
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, MapResult, Coords
from ..core.exceptions import ValidationError


class GoogleMaps(BaseClient):
    """Клиент для работы с Google Maps через XMLRiver"""

    BASE_URL = "http://xmlriver.com/search/xml"

    def search_maps(
        self,
        query: str,
        zoom: int,
        coords: Coords,
        count: int = 20,
        lr: Optional[str] = None,
        **kwargs,
    ) -> SearchResponse:
        """
        Поиск по Google Maps

        Args:
            query: Поисковый запрос
            zoom: Уровень приближения (1-15)
            coords: Координаты центра карты (широта, долгота)
            count: Количество результатов (5-50)
            lr: Код языка
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска по картам

        Raises:
            ValidationError: При неверных параметрах
        """
        # Валидация параметров
        if not 1 <= zoom <= 15:
            raise ValidationError(102, "Zoom level must be between 1 and 15")

        if not 5 <= count <= 50:
            raise ValidationError(102, "Count must be between 5 and 50")

        lat, lon = coords
        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise ValidationError(102, "Invalid coordinates")

        params = {
            **self.base_params,
            "query": query,
            "setab": "maps",
            "zoom": zoom,
            "coords": f"{lat},{lon}",
            "count": count,
        }

        if lr:
            params["lr"] = lr

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_maps_results(response, query)

    def _parse_maps_results(self, response: dict, query: str = "") -> SearchResponse:
        """Парсинг результатов поиска по картам"""
        found = response.get("found", {})
        total = int(found.get("#text", 0)) if isinstance(found, dict) else 0

        maps_data = response.get("maps", {})
        items = maps_data.get("item", []) if isinstance(maps_data, dict) else []

        if not isinstance(items, list):
            items = [items] if items else []

        results = []
        for item in items:
            result = MapResult(
                title=item.get("title", ""),
                stars=self._extract_stars(item.get("stars")),
                type=item.get("type"),
                address=item.get("address"),
                url=item.get("url"),
                phone=item.get("phone"),
                review=item.get("review"),
                possibility=item.get("possibility"),
                latitude=self._extract_coordinate(item.get("latitude")),
                longitude=self._extract_coordinate(item.get("longitude")),
                place_id=item.get("placeid"),
                count_reviews=self._extract_count(item.get("countreviews")),
                accessibility=self._extract_bool(item.get("accessibility")),
                price=item.get("price"),
                gas_price=item.get("gasprice"),
            )
            results.append(result)

        return SearchResponse(
            query=response.get("query", query),
            total_results=total,
            results=results,
            showing_results_for=response.get("showing_results_for"),
        )

    def _extract_stars(self, doc) -> Optional[float]:
        """Извлечение рейтинга"""
        if doc:
            try:
                return float(str(doc).replace(",", "."))
            except (ValueError, TypeError):
                pass
        return None

    def _extract_coordinate(self, value) -> Optional[float]:
        """Извлечение координаты"""
        if value:
            try:
                return float(str(value).replace(",", "."))
            except (ValueError, TypeError):
                pass
        return None

    def _extract_count(self, value) -> Optional[int]:
        """Извлечение количества"""
        if value:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        return None

    def _extract_bool(self, value) -> Optional[bool]:
        """Извлечение булевого значения"""
        if value is not None:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ("true", "1", "yes")
        return None

    def search_nearby(
        self, query: str, coords: Coords, radius: int = 1000, **kwargs
    ) -> SearchResponse:
        """
        Поиск объектов поблизости

        Args:
            query: Поисковый запрос
            coords: Координаты центра
            radius: Радиус поиска в метрах
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        # Определяем zoom на основе радиуса
        if radius <= 500:
            zoom = 15
        elif radius <= 1000:
            zoom = 14
        elif radius <= 2000:
            zoom = 13
        elif radius <= 5000:
            zoom = 12
        else:
            zoom = 11

        return self.search_maps(query, zoom, coords, **kwargs)

    def search_restaurants(
        self, coords: Coords, query: str = "ресторан", **kwargs
    ) -> SearchResponse:
        """Поиск ресторанов поблизости"""
        return self.search_nearby(query, coords, **kwargs)

    def search_hotels(
        self, coords: Coords, query: str = "отель", **kwargs
    ) -> SearchResponse:
        """Поиск отелей поблизости"""
        return self.search_nearby(query, coords, **kwargs)

    def search_gas_stations(
        self, coords: Coords, query: str = "заправка", **kwargs
    ) -> SearchResponse:
        """Поиск заправок поблизости"""
        return self.search_nearby(query, coords, **kwargs)

    def search_pharmacies(
        self, coords: Coords, query: str = "аптека", **kwargs
    ) -> SearchResponse:
        """Поиск аптек поблизости"""
        return self.search_nearby(query, coords, **kwargs)
