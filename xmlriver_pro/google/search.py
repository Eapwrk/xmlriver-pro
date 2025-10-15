"""
Google Search API для XMLRiver Pro
"""

from typing import Optional, List
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, TimeFilter, DeviceType, OSType


class GoogleSearch(BaseClient):
    """Клиент для работы с Google Search через XMLRiver"""

    BASE_URL = "http://xmlriver.com/search/xml"

    def search(
        self,
        query: str,
        groupby: int = 10,
        page: int = 1,
        country: Optional[int] = None,
        device: DeviceType = DeviceType.DESKTOP,
        os: Optional[OSType] = None,
        **kwargs,
    ) -> SearchResponse:
        """
        Органический поиск Google

        Args:
            query: Поисковый запрос
            groupby: Количество результатов (максимум 10)
            page: Номер страницы (начинается с 1)
            country: ID страны из файла countries.xlsx
            device: Тип устройства
            os: Операционная система для мобильных устройств
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        params = {
            **self.base_params,
            "query": query,
            "groupby": groupby,
            "page": page,
            "device": device.value,
        }

        if country:
            params["country"] = country
        if os and device == DeviceType.MOBILE:
            params["os"] = os.value

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_results(response)

    def search_with_time_filter(
        self, query: str, time_filter: TimeFilter, **kwargs
    ) -> SearchResponse:
        """
        Поиск с фильтром по времени

        Args:
            query: Поисковый запрос
            time_filter: Фильтр по времени
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        params = {"tbs": time_filter.value}
        params.update(kwargs)
        return self.search(query, **params)

    def search_without_correction(self, query: str, **kwargs) -> SearchResponse:
        """
        Поиск без исправления запроса

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        params = {"nfpr": 1}
        params.update(kwargs)
        return self.search(query, **params)

    def search_with_highlights(self, query: str, **kwargs) -> SearchResponse:
        """
        Поиск с подсветкой ключевых слов

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска с подсветкой
        """
        params = {"highlights": 1}
        params.update(kwargs)
        return self.search(query, **params)

    def search_without_filter(self, query: str, **kwargs) -> SearchResponse:
        """
        Поиск без фильтрации похожих результатов

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        params = {"filter": 0}
        params.update(kwargs)
        return self.search(query, **params)

    def search_site(self, site: str, query: str, **kwargs) -> SearchResponse:
        """
        Поиск по конкретному сайту

        Args:
            site: Домен сайта
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"site:{site} {query}"
        return self.search(search_query, **kwargs)

    def search_exact_phrase(self, phrase: str, **kwargs) -> SearchResponse:
        """
        Поиск точной фразы

        Args:
            phrase: Точная фраза в кавычках
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f'"{phrase}"'
        return self.search(search_query, **kwargs)

    def search_exclude_words(
        self, query: str, exclude_words: List[str], **kwargs
    ) -> SearchResponse:
        """
        Поиск с исключением слов

        Args:
            query: Поисковый запрос
            exclude_words: Слова для исключения
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        exclude_query = " ".join([f"-{word}" for word in exclude_words])
        search_query = f"{query} {exclude_query}"
        return self.search(search_query, **kwargs)

    def search_file_type(self, query: str, file_type: str, **kwargs) -> SearchResponse:
        """
        Поиск по типу файла

        Args:
            query: Поисковый запрос
            file_type: Тип файла (pdf, doc, xls, ppt, etc.)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"{query} filetype:{file_type}"
        return self.search(search_query, **kwargs)

    def search_in_title(self, query: str, **kwargs) -> SearchResponse:
        """
        Поиск в заголовках

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"intitle:{query}"
        return self.search(search_query, **kwargs)

    def search_in_url(self, query: str, **kwargs) -> SearchResponse:
        """
        Поиск в URL

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"inurl:{query}"
        return self.search(search_query, **kwargs)

    def search_related(self, url: str, **kwargs) -> SearchResponse:
        """
        Поиск похожих сайтов

        Args:
            url: URL для поиска похожих
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"related:{url}"
        return self.search(search_query, **kwargs)

    def search_cache(self, url: str, **kwargs) -> SearchResponse:
        """
        Поиск кэшированной версии страницы

        Args:
            url: URL для поиска в кэше
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"cache:{url}"
        return self.search(search_query, **kwargs)

    def search_define(self, term: str, **kwargs) -> SearchResponse:
        """
        Поиск определения термина

        Args:
            term: Термин для определения
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"define:{term}"
        return self.search(search_query, **kwargs)

    def search_info(self, url: str, **kwargs) -> SearchResponse:
        """
        Получить информацию о сайте

        Args:
            url: URL сайта
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"info:{url}"
        return self.search(search_query, **kwargs)
