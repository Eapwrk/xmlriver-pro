"""
Yandex Search API для XMLRiver Pro
"""

from typing import Optional, List
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, DeviceType, OSType


class YandexSearch(BaseClient):
    """Клиент для работы с Яндекс Search через XMLRiver"""

    BASE_URL = "https://xmlriver.com/search_yandex/xml"

    def search(
        self,
        query: str,
        groupby: int = 10,
        page: int = 0,
        lr: Optional[int] = None,
        lang: Optional[str] = None,
        domain: Optional[str] = None,
        device: DeviceType = DeviceType.DESKTOP,
        os: Optional[OSType] = None,
        **kwargs,
    ) -> SearchResponse:
        """
        Органический поиск Яндекс

        Args:
            query: Поисковый запрос
            groupby: Количество результатов (максимум 10)
            page: Номер страницы (начинается с 0)
            lr: ID региона Яндекса
            lang: Код языка (ru, uk, etc.)
            domain: Домен Яндекса (ru, com, ua, etc.)
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

        if lr:
            params["lr"] = lr
        if lang:
            params["lang"] = lang
        if domain:
            params["domain"] = domain
        if os and device == DeviceType.MOBILE:
            params["os"] = os.value

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_results(response)

    def search_with_time_filter(
        self, query: str, within: int, **kwargs
    ) -> SearchResponse:
        """
        Поиск с фильтром по времени

        Args:
            query: Поисковый запрос
            within: Фильтр по периоду (77 - сутки, 1 - 2 недели,
                   2 - месяц, 0 - весь период)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        params = {"within": within}
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

    def search_with_filter(self, query: str, **kwargs) -> SearchResponse:
        """
        Поиск с фильтрацией похожих результатов

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        params = {"filter": 1}
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

    def search_in_title(self, query: str, **kwargs) -> SearchResponse:
        """
        Поиск в заголовках

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        search_query = f"title:{query}"
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
        search_query = f"url:{query}"
        return self.search(search_query, **kwargs)

    def search_by_region(self, query: str, region_id: int, **kwargs) -> SearchResponse:
        """
        Поиск по региону

        Args:
            query: Поисковый запрос
            region_id: ID региона Яндекса
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        return self.search(query, lr=region_id, **kwargs)

    def search_by_language(self, query: str, language: str, **kwargs) -> SearchResponse:
        """
        Поиск по языку

        Args:
            query: Поисковый запрос
            language: Код языка
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        return self.search(query, lang=language, **kwargs)

    def search_by_domain(
        self, query: str, yandex_domain: str, **kwargs
    ) -> SearchResponse:
        """
        Поиск по домену Яндекса

        Args:
            query: Поисковый запрос
            yandex_domain: Домен Яндекса (ru, com, ua, etc.)
            **kwargs: Дополнительные параметры

        Returns:
            Результаты поиска
        """
        return self.search(query, domain=yandex_domain, **kwargs)

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
