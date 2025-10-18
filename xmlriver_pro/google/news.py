"""
Google News API для XMLRiver Pro
"""

from typing import Optional
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, NewsResult, TimeFilter


class GoogleNews(BaseClient):
    """Клиент для работы с Google News через XMLRiver"""

    BASE_URL = "http://xmlriver.com/search/xml"

    def search_news(
        self,
        query: str,
        time_filter: Optional[TimeFilter] = None,
        *,
        groupby: int = 10,
        page: int = 1,
        country: Optional[int] = None,
        device: str = "desktop",
        **kwargs,
    ) -> SearchResponse:
        """
        Поиск по новостям Google

        Args:
            query: Поисковый запрос
            time_filter: Фильтр по времени
            groupby: Количество результатов
            page: Номер страницы
            country: ID страны
            device: Тип устройства
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска новостей
        """
        params = {
            **self.base_params,
            "query": query,
            "setab": "news",
            "groupby": groupby,
            "page": page,
            "device": device,
        }

        if time_filter:
            params["tbs"] = time_filter.value
        if country:
            params["country"] = country

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_news_results(response, query)

    def _parse_news_results(self, response: dict, query: str = "") -> SearchResponse:
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
            query=response.get("query", query),
            total_results=total,
            results=results,
            showing_results_for=response.get("showing_results_for"),
        )

    def search_news_last_hour(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последний час"""
        return self.search_news(query, TimeFilter.LAST_HOUR, **kwargs)

    def search_news_last_day(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последний день"""
        return self.search_news(query, TimeFilter.LAST_DAY, **kwargs)

    def search_news_last_week(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последнюю неделю"""
        return self.search_news(query, TimeFilter.LAST_WEEK, **kwargs)

    def search_news_last_month(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последний месяц"""
        return self.search_news(query, TimeFilter.LAST_MONTH, **kwargs)

    def search_news_last_year(self, query: str, **kwargs) -> SearchResponse:
        """Поиск новостей за последний год"""
        return self.search_news(query, TimeFilter.LAST_YEAR, **kwargs)

    def search_news_custom_period(
        self, query: str, start_date: str, end_date: str, **kwargs
    ) -> SearchResponse:
        """
        Поиск новостей за пользовательский период

        Args:
            query: Поисковый запрос
            start_date: Начальная дата в формате MM/DD/YYYY
            end_date: Конечная дата в формате MM/DD/YYYY
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска новостей
        """
        kwargs["tbs"] = f"cdr:1,cd_min:{start_date},cd_max:{end_date}"
        return self.search_news(query, **kwargs)
