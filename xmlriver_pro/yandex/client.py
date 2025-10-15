"""
Yandex клиент для работы с XMLRiver API
"""

from typing import Optional, Any
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, DeviceType, OSType
from ..core.exceptions import NoResultsError


class YandexClient(BaseClient):
    """Клиент для работы с Яндекс через XMLRiver"""

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
        **kwargs: Any,
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
        self, query: str, within: int, **kwargs: Any
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

    def search_with_highlights(self, query: str, **kwargs: Any) -> SearchResponse:
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

    def search_with_filter(self, query: str, **kwargs: Any) -> SearchResponse:
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
        return self.search(query, **kwargs)

    def search_site(self, site: str, query: str, **kwargs: Any) -> SearchResponse:
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

    def search_exact_phrase(self, phrase: str, **kwargs: Any) -> SearchResponse:
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
        self, query: str, exclude_words: list, **kwargs: Any
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

    def search_in_title(self, query: str, **kwargs: Any) -> SearchResponse:
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

    def search_in_url(self, query: str, **kwargs: Any) -> SearchResponse:
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

    def check_indexing(self, url: str, strict: bool = False, **kwargs: Any) -> bool:
        """
        Проверка индексации URL в Яндексе

        Args:
            url: URL для проверки
            strict: Строгое соответствие регистра
            **kwargs: Дополнительные параметры

        Returns:
            True если URL проиндексирован
        """
        params = {"inindex": 1, "strict": int(strict)}
        params.update(kwargs)

        try:
            response = self.search(url, **params)
            return any(result.url == url for result in response.results)
        except NoResultsError:
            return False

    def is_trust_domain(self, domain: str, **kwargs: Any) -> bool:
        """
        Проверка доверия к домену

        Args:
            domain: Домен для проверки
            **kwargs: Дополнительные параметры

        Returns:
            True если домен доверенный
        """
        # Убираем www. если есть
        clean_domain = domain.replace("www.", "")
        query = clean_domain.replace(".", " ")

        try:
            response = self.search(query, **kwargs)
            for result in response.results:
                if clean_domain in result.url:
                    return True
            return False
        except NoResultsError:
            return False

    def is_url_pessimized(self, url: str, **kwargs: Any) -> bool:
        """
        Проверка URL на наличие фильтров

        Args:
            url: URL для проверки
            **kwargs: Дополнительные параметры

        Returns:
            True если URL под фильтром
        """
        query = f"url:{url}"

        try:
            response = self.search(query, **kwargs)
            return not any(result.url == url for result in response.results)
        except NoResultsError:
            return True

    def get_cost(self, system: str = "yandex") -> float:
        """
        Получить стоимость за 1000 запросов Яндекс

        Returns:
            Стоимость в рублях
        """
        return super().get_cost("yandex")
