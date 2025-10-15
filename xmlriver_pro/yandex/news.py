"""
Yandex News API для XMLRiver Pro
"""

from typing import Optional, List
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, NewsResult


class YandexNews(BaseClient):
    """Клиент для работы с Яндекс Новости через XMLRiver"""

    BASE_URL = "https://xmlriver.com/search_yandex/xml"

    def search_news(
        self,
        query: str,
        within: Optional[int] = None,
        groupby: int = 10,
        page: int = 0,
        lr: Optional[int] = None,
        lang: Optional[str] = None,
        domain: Optional[str] = None,
        device: str = "desktop",
        **kwargs,
    ) -> SearchResponse:
        """
        Поиск по новостям Яндекс

        Args:
            query: Поисковый запрос
            within: Фильтр по периоду (77 - сутки, 1 - 2 недели,
                   2 - месяц, 0 - весь период)
            groupby: Количество результатов
            page: Номер страницы
            lr: ID региона
            lang: Код языка
            domain: Домен Яндекса
            device: Тип устройства
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска новостей
        """
        params = {
            **self.base_params,
            "query": query,
            "groupby": groupby,
            "page": page,
            "device": device,
        }

        if within is not None:
            params["within"] = within
        if lr:
            params["lr"] = lr
        if lang:
            params["lang"] = lang
        if domain:
            params["domain"] = domain

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_news_results(response)

    def _parse_news_results(self, response: dict) -> SearchResponse:
        """Парсинг результатов поиска новостей"""
        found = response.get("found", {})
        total = int(found.get("#text", 0)) if isinstance(found, dict) else 0

        groups = response.get("results", {}).get("grouping", {}).get("group", [])
        if not isinstance(groups, list):
            groups = [groups] if groups else []

        results = []
        for rank, group in enumerate(groups, 1):
            doc = group.get("doc", {})
            result = NewsResult(
                rank=rank,
                url=doc.get("url", ""),
                title=doc.get("title", ""),
                snippet=self._extract_snippet(doc),
                media=doc.get("media"),
                pub_date=doc.get("pubDate"),
            )
            results.append(result)

        return SearchResponse(
            query=response.get("query", ""),
            total_results=total,
            results=results,
            showing_results_for=response.get("showing_results_for"),
        )

    def search_news_last_day(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последний день"""
        return self.search_news(query, within=77, **kwargs)

    def search_news_last_2_weeks(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последние 2 недели"""
        return self.search_news(query, within=1, **kwargs)

    def search_news_last_month(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последний месяц"""
        return self.search_news(query, within=2, **kwargs)

    def search_news_all_time(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за весь период"""
        return self.search_news(query, within=0, **kwargs)

    def search_news_by_region(
        self, query: str, region_id: int, **kwargs
    ) -> SearchResponse:
        """
        Поиск новостей по региону

        Args:
            query: Поисковый запрос
            region_id: ID региона Яндекса
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска новостей
        """
        return self.search_news(query, lr=region_id, **kwargs)

    def search_news_by_language(
        self, query: str, language: str, **kwargs
    ) -> SearchResponse:
        """
        Поиск новостей по языку

        Args:
            query: Поисковый запрос
            language: Код языка (ru, uk, etc.)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска новостей
        """
        return self.search_news(query, lang=language, **kwargs)

    def search_news_by_domain(
        self, query: str, domain: str, **kwargs
    ) -> SearchResponse:
        """
        Поиск новостей по домену Яндекса

        Args:
            query: Поисковый запрос
            domain: Домен Яндекса (ru, com, ua, etc.)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска новостей
        """
        return self.search_news(query, domain=domain, **kwargs)

    def get_news_trends(self, query: str, **kwargs) -> List[str]:
        """
        Получить тренды новостей

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Список трендовых тем
        """
        response = self.search_news(query, **kwargs)

        # Извлекаем тренды из результатов
        trends = []
        for result in response.results:
            if result.title and len(result.title) > 10:
                trends.append(result.title)

        return trends[:10]  # Возвращаем топ-10 трендов
