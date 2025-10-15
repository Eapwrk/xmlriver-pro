"""
Google клиент для работы с XMLRiver API
"""

from typing import Optional, Any
from ..core.base_client import BaseClient
from ..core.types import SearchResponse, TimeFilter, DeviceType
from ..core.exceptions import NoResultsError


class GoogleClient(BaseClient):
    """Клиент для работы с Google через XMLRiver"""

    BASE_URL = "http://xmlriver.com/search/xml"

    def __init__(
        self,
        user_id: int,
        api_key: str,
        timeout: int = 60,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        enable_retry: bool = True,
        **kwargs: Any,
    ):
        """
        Инициализация Google клиента

        Args:
            user_id: ID пользователя XMLRiver
            api_key: API ключ
            timeout: Таймаут запроса в секундах
            max_retries: Максимальное количество попыток повтора
            retry_delay: Базовая задержка между попытками в секундах
            enable_retry: Включить автоматические повторы
            **kwargs: Дополнительные параметры
        """
        super().__init__(
            user_id=user_id,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            enable_retry=enable_retry,
            **kwargs,
        )

    def search(
        self,
        query: str,
        groupby: int = 10,
        page: int = 1,
        country: Optional[int] = None,
        device: DeviceType = DeviceType.DESKTOP,
        **kwargs: Any,
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
        if kwargs.get("os") and device == DeviceType.MOBILE:
            params["os"] = kwargs["os"].value

        params.update(kwargs)

        response = self._make_request(self.BASE_URL, params)
        return self._parse_results(response, query)

    def search_with_time_filter(
        self, query: str, time_filter: TimeFilter, **kwargs: Any
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

    def search_without_correction(self, query: str, **kwargs: Any) -> SearchResponse:
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

    def search_without_filter(self, query: str, **kwargs: Any) -> SearchResponse:
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

    def check_indexing(self, url: str, strict: bool = False, **kwargs: Any) -> bool:
        """
        Проверка индексации URL в Google

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
        query = f"inurl:{url}"

        try:
            response = self.search(query, **kwargs)
            return not any(result.url == url for result in response.results)
        except NoResultsError:
            return True

    def get_cost(self, system: str = "google") -> float:
        """
        Получить стоимость за 1000 запросов Google

        Returns:
            Стоимость в рублях
        """
        return super().get_cost("google")
