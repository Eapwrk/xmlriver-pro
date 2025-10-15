"""
Тесты для Google API
"""

import pytest
from unittest.mock import Mock, patch
from xmlriver_pro.google import (
    GoogleClient,
    GoogleSearch,
    GoogleNews,
    GoogleImages,
    GoogleMaps,
    GoogleAds,
)
from xmlriver_pro.core.types import SearchResponse, SearchResult, TimeFilter, DeviceType


class TestGoogleClient:
    """Тесты для GoogleClient"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.client = GoogleClient(user_id=123, api_key="test_key")

    def test_init(self):
        """Тест инициализации клиента"""
        assert self.client.user_id == 123
        assert self.client.api_key == "test_key"
        assert self.client.BASE_URL == "http://xmlriver.com/search/xml"

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
    def test_search_with_country(self, mock_request):
        """Тест поиска с указанием страны"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        self.client.search("python", country=10)

        # Проверяем, что параметр country был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["country"] == 10  # params - второй позиционный аргумент

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_with_device(self, mock_request):
        """Тест поиска с указанием устройства"""
        mock_response = {
            "query": "python",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        self.client.search("python", device=DeviceType.MOBILE)

        # Проверяем, что параметр device был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["device"] == "mobile"

    def test_get_cost(self):
        """Тест получения стоимости"""
        with patch.object(self.client.session, "get") as mock_get:
            mock_response = Mock()
            mock_response.text = "0.5"
            mock_get.return_value = mock_response

            cost = self.client.get_cost()
            assert cost == 0.5


class TestGoogleSearch:
    """Тесты для GoogleSearch"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.search = GoogleSearch(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_exact_phrase(self, mock_request):
        """Тест поиска точной фразы"""
        mock_response = {
            "query": '"python programming"',
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.search.search_exact_phrase("python programming")

        # Проверяем, что запрос был обернут в кавычки
        call_args = mock_request.call_args
        assert call_args[0][1]["query"] == '"python programming"'

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


class TestGoogleNews:
    """Тесты для GoogleNews"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.news = GoogleNews(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_news(self, mock_request):
        """Тест поиска новостей"""
        mock_response = {
            "query": "python news",
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

        result = self.news.search_news("python news")

        assert isinstance(result, SearchResponse)
        assert result.query == "python news"
        assert len(result.results) == 1
        assert result.results[0].url == "https://news.python.org"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_news_with_time_filter(self, mock_request):
        """Тест поиска новостей с фильтром времени"""
        mock_response = {
            "query": "python news",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.news.search_news("python news", time_filter=TimeFilter.LAST_WEEK)

        # Проверяем, что параметр tbs был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["tbs"] == "qdr:w"
        assert call_args[0][1]["setab"] == "news"


class TestGoogleImages:
    """Тесты для GoogleImages"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.images = GoogleImages(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_images(self, mock_request):
        """Тест поиска изображений"""
        mock_response = {
            "query": "python logo",
            "found": {"#text": "1000000"},
            "results": {
                "grouping": {
                    "group": [
                        {
                            "doc": {
                                "url": "https://python.org/logo.png",
                                "imgurl": "https://python.org/logo.png",
                                "title": "Python Logo",
                                "displaylink": "python.org",
                                "originalwidth": "500",
                                "originalheight": "500",
                            }
                        }
                    ]
                }
            },
        }
        mock_request.return_value = mock_response

        result = self.images.search_images("python logo")

        assert isinstance(result, SearchResponse)
        assert result.query == "python logo"
        assert len(result.results) == 1
        assert result.results[0].url == "https://python.org/logo.png"

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_images_by_size(self, mock_request):
        """Тест поиска изображений по размеру"""
        mock_response = {
            "query": "python logo",
            "found": {"#text": "1000000"},
            "results": {"grouping": {"group": []}},
        }
        mock_request.return_value = mock_response

        result = self.images.search_images_by_size("python logo", "large")

        # Проверяем, что параметр tbs был передан
        call_args = mock_request.call_args
        assert call_args[0][1]["tbs"] == "isz:large"
        assert call_args[0][1]["setab"] == "images"


class TestGoogleMaps:
    """Тесты для GoogleMaps"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.maps = GoogleMaps(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_search_maps(self, mock_request):
        """Тест поиска по картам"""
        mock_response = {
            "query": "cafe moscow",
            "found": {"#text": "10"},
            "maps": {
                "item": [
                    {
                        "title": "Cafe Moscow",
                        "stars": "4.5",
                        "type": "Кафе",
                        "address": "ул. Тверская, 1",
                        "latitude": "55.7558",
                        "longitude": "37.6176",
                    }
                ]
            },
        }
        mock_request.return_value = mock_response

        result = self.maps.search_maps(
            "cafe moscow", zoom=12, coords=(55.7558, 37.6176)
        )

        assert isinstance(result, SearchResponse)
        assert result.query == "cafe moscow"
        assert len(result.results) == 1
        assert result.results[0].title == "Cafe Moscow"

    def test_validate_coords(self):
        """Тест валидации координат"""
        # Валидные координаты
        assert self.maps._extract_coordinate("55.7558") == 55.7558
        assert self.maps._extract_coordinate("37.6176") == 37.6176

        # Невалидные координаты
        assert self.maps._extract_coordinate("invalid") is None
        assert self.maps._extract_coordinate(None) is None


class TestGoogleAds:
    """Тесты для GoogleAds"""

    def setup_method(self):
        """Настройка для каждого теста"""
        self.ads = GoogleAds(user_id=123, api_key="test_key")

    @patch("xmlriver_pro.core.base_client.BaseClient._make_request")
    def test_get_ads(self, mock_request):
        """Тест получения рекламных блоков"""
        mock_response = {
            "topads": {
                "query": [
                    {
                        "url": "https://advertiser.com",
                        "adsurl": "https://googleadservices.com/ad",
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
        assert result.top_ads[0].url == "https://advertiser.com"
        assert result.top_ads[0].title == "Ad Title"

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
