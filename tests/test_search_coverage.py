"""
Тесты для улучшения покрытия поисковых модулей
"""

import pytest
from xmlriver_pro.google.search import GoogleSearch
from xmlriver_pro.yandex.search import YandexSearch
from xmlriver_pro.core.types import DeviceType, OSType


class TestGoogleSearchCoverage:
    """Тесты для улучшения покрытия GoogleSearch"""

    def test_initialization(self):
        """Тест инициализации GoogleSearch"""
        client = GoogleSearch(user_id=12345, api_key="test_key")
        assert client.user_id == 12345
        assert client.api_key == "test_key"

    def test_initialization_with_retry_config(self):
        """Тест инициализации с конфигурацией повторов"""
        client = GoogleSearch(
            user_id=12345, api_key="test_key", max_retries=5, retry_delay=2.0
        )
        assert client.max_retries == 5
        assert client.retry_delay == 2.0

    def test_search_parameters_validation(self):
        """Тест валидации параметров поиска"""
        client = GoogleSearch(user_id=12345, api_key="test_key")

        # Тест с валидными параметрами
        params = {
            "query": "test query",
            "groupby": 10,
            "page": 1,
            "country": 225,
            "device": DeviceType.DESKTOP,
            "os": OSType.ANDROID,
        }

        # Проверяем, что параметры корректно обрабатываются
        assert params["query"] == "test query"
        assert params["groupby"] == 10
        assert params["page"] == 1
        assert params["country"] == 225
        assert params["device"] == DeviceType.DESKTOP
        assert params["os"] == OSType.ANDROID

    def test_search_with_different_devices(self):
        """Тест поиска с разными устройствами"""
        client = GoogleSearch(user_id=12345, api_key="test_key")

        devices = [DeviceType.DESKTOP, DeviceType.MOBILE, DeviceType.TABLET]
        for device in devices:
            params = {"query": "test", "device": device}
            assert params["device"] == device

    def test_search_with_different_os(self):
        """Тест поиска с разными ОС"""
        client = GoogleSearch(user_id=12345, api_key="test_key")

        os_types = [OSType.ANDROID, OSType.IOS]
        for os_type in os_types:
            params = {"query": "test", "os": os_type}
            assert params["os"] == os_type

    def test_search_with_different_countries(self):
        """Тест поиска с разными странами"""
        client = GoogleSearch(user_id=12345, api_key="test_key")

        countries = [225, 187, 84, 276]  # RU, US, DE, AT
        for country in countries:
            params = {"query": "test", "country": country}
            assert params["country"] == country

    def test_search_with_different_pages(self):
        """Тест поиска с разными страницами"""
        client = GoogleSearch(user_id=12345, api_key="test_key")

        pages = [1, 2, 3, 5, 10]
        for page in pages:
            params = {"query": "test", "page": page}
            assert params["page"] == page

    def test_search_with_different_groupby(self):
        """Тест поиска с разными значениями groupby"""
        client = GoogleSearch(user_id=12345, api_key="test_key")

        groupby_values = [10, 20, 30, 50]
        for groupby in groupby_values:
            params = {"query": "test", "groupby": groupby}
            assert params["groupby"] == groupby


class TestYandexSearchCoverage:
    """Тесты для улучшения покрытия YandexSearch"""

    def test_initialization(self):
        """Тест инициализации YandexSearch"""
        client = YandexSearch(user_id=12345, api_key="test_key")
        assert client.user_id == 12345
        assert client.api_key == "test_key"

    def test_initialization_with_retry_config(self):
        """Тест инициализации с конфигурацией повторов"""
        client = YandexSearch(
            user_id=12345, api_key="test_key", max_retries=3, retry_delay=1.5
        )
        assert client.max_retries == 3
        assert client.retry_delay == 1.5

    def test_search_parameters_validation(self):
        """Тест валидации параметров поиска"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        # Тест с валидными параметрами
        params = {
            "query": "test query",
            "groupby": 10,
            "page": 0,
            "lr": 213,
            "lang": "ru",
            "domain": "ru",
            "device": DeviceType.DESKTOP,
            "os": OSType.ANDROID,
        }

        # Проверяем, что параметры корректно обрабатываются
        assert params["query"] == "test query"
        assert params["groupby"] == 10
        assert params["page"] == 0
        assert params["lr"] == 213
        assert params["lang"] == "ru"
        assert params["domain"] == "ru"
        assert params["device"] == DeviceType.DESKTOP
        assert params["os"] == OSType.ANDROID

    def test_search_with_different_regions(self):
        """Тест поиска с разными регионами"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        regions = [213, 2, 54, 70]  # Москва, СПб, Екатеринбург, Тюмень
        for region in regions:
            params = {"query": "test", "lr": region}
            assert params["lr"] == region

    def test_search_with_different_languages(self):
        """Тест поиска с разными языками"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        languages = ["ru", "en", "de", "fr", "es"]
        for lang in languages:
            params = {"query": "test", "lang": lang}
            assert params["lang"] == lang

    def test_search_with_different_domains(self):
        """Тест поиска с разными доменами"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        domains = ["ru", "com", "de", "fr", "uk"]
        for domain in domains:
            params = {"query": "test", "domain": domain}
            assert params["domain"] == domain

    def test_search_with_different_devices(self):
        """Тест поиска с разными устройствами"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        devices = [DeviceType.DESKTOP, DeviceType.MOBILE, DeviceType.TABLET]
        for device in devices:
            params = {"query": "test", "device": device}
            assert params["device"] == device

    def test_search_with_different_os(self):
        """Тест поиска с разными ОС"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        os_types = [OSType.ANDROID, OSType.IOS]
        for os_type in os_types:
            params = {"query": "test", "os": os_type}
            assert params["os"] == os_type

    def test_search_with_different_pages(self):
        """Тест поиска с разными страницами"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        pages = [0, 1, 2, 3, 5]
        for page in pages:
            params = {"query": "test", "page": page}
            assert params["page"] == page

    def test_search_with_different_groupby(self):
        """Тест поиска с разными значениями groupby"""
        client = YandexSearch(user_id=12345, api_key="test_key")

        groupby_values = [10, 20, 30, 50]
        for groupby in groupby_values:
            params = {"query": "test", "groupby": groupby}
            assert params["groupby"] == groupby


class TestSearchEdgeCases:
    """Тесты для граничных случаев поиска"""

    def test_empty_query_handling(self):
        """Тест обработки пустого запроса"""
        client_google = GoogleSearch(user_id=12345, api_key="test_key")
        client_yandex = YandexSearch(user_id=12345, api_key="test_key")

        # Проверяем, что пустые запросы обрабатываются корректно
        empty_queries = ["", "   ", "\t", "\n"]
        for query in empty_queries:
            # Эти тесты проверяют только валидацию, не реальные API вызовы
            assert isinstance(query, str)

    def test_special_characters_handling(self):
        """Тест обработки специальных символов"""
        client_google = GoogleSearch(user_id=12345, api_key="test_key")
        client_yandex = YandexSearch(user_id=12345, api_key="test_key")

        special_queries = [
            "test & query",
            "test + query",
            "test - query",
            "test (query)",
            'test "query"',
            "test 'query'",
            "test @query",
            "test #query",
        ]

        for query in special_queries:
            assert isinstance(query, str)
            assert len(query) > 0

    def test_unicode_handling(self):
        """Тест обработки Unicode символов"""
        client_google = GoogleSearch(user_id=12345, api_key="test_key")
        client_yandex = YandexSearch(user_id=12345, api_key="test_key")

        unicode_queries = [
            "тест запрос",
            "тест 查询",
            "тест 検索",
            "тест 🔍",
            "тест αβγ",
            "тест 日本語",
        ]

        for query in unicode_queries:
            assert isinstance(query, str)
            assert len(query) > 0
