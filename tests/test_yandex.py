"""
Тесты для Yandex API
"""

import pytest
from unittest.mock import Mock, patch
from xmlriver_pro.yandex import (
    YandexClient,
    YandexSearch,
    YandexNews,
    YandexAds,
)
from xmlriver_pro.core.types import SearchResponse, SearchResult, DeviceType


class TestYandexClient:
    """Тесты для YandexClient"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.client = YandexClient(user_id=123, api_key="test_key")

    def test_init(self):
        """Тест инициализации клиента"""
        assert self.client.user_id == 123
        assert self.client.api_key == "test_key"
        assert self.client.BASE_URL == "https://xmlriver.com/search_yandex/xml"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search(self, mock_request):
        """Тест базового поиска"""
        # Мокаем ответ API
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {
                "grouping": {
                    "group": [
                        {
                            "doc": {
                                "url": "https://python.org",
                                "title": "Python",
                                "passages": {"passage": "Python programming language"},
                            }
                        }
                    ]
                }
            },
        }
        mock_request.return_value = mock_response

        result = self.client.search("python")

        assert isinstance(result, SearchResponse)
        assert result.query == "python"
        assert result.total_results == 1000000
        assert len(result.results) == 1
        assert result.results[0].url == "https://python.org"
        assert result.results[0].title == "Python"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_with_lr(self, mock_request):
        """Тест поиска с указанием региона"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        self.client.search("python", lr=213)  # Москва

        # Проверяем, что параметр lr был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["lr"] == 213

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_with_lang(self, mock_request):
        """Тест поиска с указанием языка"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        self.client.search("python", lang="ru")

        # Проверяем, что параметр lang был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["lang"] == "ru"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_with_domain(self, mock_request):
        """Тест поиска с указанием домена"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        self.client.search("python", domain="ru")

        # Проверяем, что параметр domain был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["domain"] == "ru"

    def test_get_cost(self):
        """Тест получения стоимости"""
        with patch.object(self.client.session, "get") as mock_get:
            mock_response = Mock()
            mock_response.text = "0.3"
            mock_get.return_value = mock_response

            cost = self.client.get_cost()
            assert cost == 0.3


class TestYandexSearch:
    """Тесты для YandexSearch"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.search = YandexSearch(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_exact_phrase(self, mock_request):
        """Тест поиска точной фразы"""
        mock_response = {
            "query": '"программирование на python"',
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.search.search_exact_phrase("программирование на python")

        # Проверяем, что запрос был обернут в кавычки
        call_args = mock_request.call_args
        assert call_args[0][1]["query"] == '"программирование на python"'

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_site(self, mock_request):
        """Тест поиска по сайту"""
        mock_response = {
            "query": "site:python.org python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.search.search_site("python.org", "python")

        # Проверяем, что запрос содержит site:
        call_args = mock_request.call_args
        assert call_args[0][1]["query"] == "site:python.org python"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_exclude_words(self, mock_request):
        """Тест поиска с исключением слов"""
        mock_response = {
            "query": "python -java -c++",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.search.search_exclude_words("python", ["java", "c++"])

        # Проверяем, что слова были исключены
        call_args = mock_request.call_args
        assert call_args[0][1]["query"] == "python -java -c++"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_by_region(self, mock_request):
        """Тест поиска по региону"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.search.search_by_region("python", 213)  # Москва

        # Проверяем, что параметр lr был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["lr"] == 213

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_by_language(self, mock_request):
        """Тест поиска по языку"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.search.search_by_language("python", "ru")

        # Проверяем, что параметр lang был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["lang"] == "ru"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_by_domain(self, mock_request):
        """Тест поиска по домену"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.search.search_by_domain("python", "ru")

        # Проверяем, что параметр domain был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["domain"] == "ru"


class TestYandexNews:
    """Тесты для YandexNews"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.news = YandexNews(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_news(self, mock_request):
        """Тест поиска новостей"""
        mock_response = {
            "query": "python новости",
            "found": {"#text": "1000000"},
            "results": {
                "grouping": {
                    "group": [
                        {
                            "doc": {
                                "url": "https://news.python.org",
                                "title": "Python News",
                                "passages": {"passage": "Latest Python news"},
                                "media": "Python.org",
                                "pubDate": "2023-01-01",
                            }
                        }
                    ]
                }
            },
        }
        mock_request.return_value = mock_response

        result = self.news.search_news("python новости")

        assert isinstance(result, SearchResponse)
        assert result.query == "python новости"
        assert len(result.results) == 1
        assert result.results[0].url == "https://news.python.org"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_news_with_within(self, mock_request):
        """Тест поиска новостей с фильтром времени"""
        mock_response = {
            "query": "python новости",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.news.search_news("python новости", within=77)  # За сутки

        # Проверяем, что параметр within был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["within"] == 77

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_news_last_day(self, mock_request):
        """Тест поиска новостей за последний день"""
        mock_response = {
            "query": "python новости",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.news.search_news_last_day("python новости")

        # Проверяем, что параметр within был установлен в 77
        call_args = mock_request.call_args
        assert call_args[0][1]["within"] == 77

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_news_by_region(self, mock_request):
        """Тест поиска новостей по региону"""
        mock_response = {
            "query": "python новости",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.news.search_news_by_region("python новости", 213)  # Москва

        # Проверяем, что параметр lr был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["lr"] == 213


class TestYandexAds:
    """Тесты для YandexAds"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.ads = YandexAds(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_get_ads(self, mock_request):
        """Тест получения рекламных блоков"""
        mock_response = {
            "topads": {
                "query": [
                    {
                        "url": "https://advertiser.ru",
                        "adsurl": "https://yandex.ru/ads",
                        "title": "Ad Title",
                        "snippet": "Ad description",
                    }
                ]
            },
            "bottomads": {"query": []},
        }
        mock_request.return_value = mock_response

        result = self.ads.get_ads("python")

        assert len(result.top_ads) == 1
        assert len(result.bottom_ads) == 0
        assert result.top_ads[0].url == "https://advertiser.ru"
        assert result.top_ads[0].title == "Ad Title"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_get_ads_by_region(self, mock_request):
        """Тест получения рекламы по региону"""
        mock_response = {"topads": {"query": []}, "bottomads": {"query": []}}
        mock_request.return_value = mock_response

        result = self.ads.get_ads_by_region("python", 213)  # Москва

        # Проверяем, что параметр lr был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["lr"] == 213

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_get_ads_by_language(self, mock_request):
        """Тест получения рекламы по языку"""
        mock_response = {"topads": {"query": []}, "bottomads": {"query": []}}
        mock_request.return_value = mock_response

        result = self.ads.get_ads_by_language("python", "ru")

        # Проверяем, что параметр lang был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["lang"] == "ru"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_get_ads_by_domain(self, mock_request):
        """Тест получения рекламы по домену"""
        mock_response = {
            "topads": {"query": [{"url": "https://example.ru/page", "title": "Test"}]},
            "bottomads": {"query": []},
        }
        mock_request.return_value = mock_response

        result = self.ads.get_ads_by_domain("python", "ru")

        # Проверяем, что метод был вызван
        assert mock_request.called
        # Проверяем, что результат содержит только рекламы с доменом "ru"
        assert len(result) == 1
        assert "ru" in result[0].url

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_count_ads(self, mock_request):
        """Тест подсчета рекламных блоков"""
        mock_response = {
            "topads": {
                "query": [
                    {
                        "url": "ad1",
                        "adsurl": "url1",
                        "title": "Ad 1",
                        "snippet": "Desc 1",
                    }
                ]
            },
            "bottomads": {
                "query": [
                    {
                        "url": "ad2",
                        "adsurl": "url2",
                        "title": "Ad 2",
                        "snippet": "Desc 2",
                    }
                ]
            },
        }
        mock_request.return_value = mock_response

        count = self.ads.count_ads("python")
        assert count == 2

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_has_ads(self, mock_request):
        """Тест проверки наличия рекламы"""
        mock_response = {"topads": {"query": []}, "bottomads": {"query": []}}
        mock_request.return_value = mock_response

        has_ads = self.ads.has_ads("python")
        assert has_ads is False
