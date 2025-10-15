"""
Google Ads API для XMLRiver Pro
"""

from typing import Optional, List, Dict
from ..core.base_client import BaseClient
from ..core.types import AdsResponse, AdResult


class GoogleAds(BaseClient):
    """Клиент для работы с Google Ads через XMLRiver"""

    BASE_URL = "http://xmlriver.com/search/xml"

    def get_ads(
        self,
        query: str,
        country: Optional[int] = None,
        device: str = "desktop",
        **kwargs,
    ) -> AdsResponse:
        """
        Получить рекламные блоки Google

        Args:
            query: Поисковый запрос
            country: ID страны
            device: Тип устройства
            **kwargs: Дополнительные параметры

        Returns:
            Рекламные блоки
        """
        params = {
            **self.base_params,
            "query": query,
            "ads": 1,
            "device": device,
        }

        if country:
            params["country"] = country

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_ads_response(response)

    def _parse_ads_response(self, response: dict) -> AdsResponse:
        """Парсинг ответа с рекламными блоками"""
        top_ads = self._parse_ads_block(response.get("topads", {}))
        bottom_ads = self._parse_ads_block(response.get("bottomads", {}))

        return AdsResponse(top_ads=top_ads, bottom_ads=bottom_ads)

    def _parse_ads_block(self, ads_data: dict) -> List[AdResult]:
        """Парсинг блока рекламы"""
        if not ads_data:
            return []

        queries = ads_data.get("query", [])
        if not isinstance(queries, list):
            queries = [queries] if queries else []

        ads = []
        for ad_data in queries:
            ad = AdResult(
                url=ad_data.get("url", ""),
                ads_url=ad_data.get("adsurl", ""),
                title=ad_data.get("title", ""),
                snippet=ad_data.get("snippet", ""),
            )
            ads.append(ad)

        return ads

    def get_top_ads(self, query: str, **kwargs) -> List[AdResult]:
        """
        Получить только верхние рекламные блоки

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Список верхних рекламных блоков
        """
        ads_response = self.get_ads(query, **kwargs)
        return ads_response.top_ads

    def get_bottom_ads(self, query: str, **kwargs) -> List[AdResult]:
        """
        Получить только нижние рекламные блоки

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Список нижних рекламных блоков
        """
        ads_response = self.get_ads(query, **kwargs)
        return ads_response.bottom_ads

    def get_all_ads(self, query: str, **kwargs) -> List[AdResult]:
        """
        Получить все рекламные блоки

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Список всех рекламных блоков
        """
        ads_response = self.get_ads(query, **kwargs)
        return ads_response.top_ads + ads_response.bottom_ads

    def count_ads(self, query: str, **kwargs) -> int:
        """
        Подсчитать количество рекламных блоков

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Общее количество рекламных блоков
        """
        ads_response = self.get_ads(query, **kwargs)
        return len(ads_response.top_ads) + len(ads_response.bottom_ads)

    def has_ads(self, query: str, **kwargs) -> bool:
        """
        Проверить наличие рекламных блоков

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            True если есть реклама
        """
        return self.count_ads(query, **kwargs) > 0

    def get_ads_by_domain(self, query: str, domain: str, **kwargs) -> List[AdResult]:
        """
        Получить рекламные блоки определенного домена

        Args:
            query: Поисковый запрос
            domain: Домен для фильтрации
            **kwargs: Дополнительные параметры

        Returns:
            Рекламные блоки домена
        """
        all_ads = self.get_all_ads(query, **kwargs)
        return [ad for ad in all_ads if domain in ad.url]

    def get_ads_stats(self, query: str, **kwargs) -> Dict[str, int]:
        """
        Получить статистику рекламных блоков

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Словарь со статистикой
        """
        ads_response = self.get_ads(query, **kwargs)

        return {
            "top_ads_count": len(ads_response.top_ads),
            "bottom_ads_count": len(ads_response.bottom_ads),
            "total_ads_count": len(ads_response.top_ads) + len(ads_response.bottom_ads),
            "has_ads": (len(ads_response.top_ads) + len(ads_response.bottom_ads)) > 0,
        }
