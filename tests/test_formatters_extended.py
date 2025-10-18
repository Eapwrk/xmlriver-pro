"""
Расширенные тесты для форматтеров
"""

import pytest
from xmlriver_pro.utils.formatters import (
    format_search_result,
    format_search_response,
    format_news_result,
    format_image_result,
    format_map_result,
    format_ads_result,
    format_ads_response,
    format_onebox_document,
    format_searchster_result,
    format_related_search,
    format_search_stats,
    format_ads_stats,
    format_results_summary,
    format_ads_summary,
    format_error_message,
    format_api_response,
)
from xmlriver_pro.core.types import (
    SearchResult,
    SearchResponse,
    NewsResult,
    ImageResult,
    MapResult,
    AdResult,
    AdsResponse,
    OneBoxDocument,
    SearchsterResult,
    RelatedSearch,
)


class TestFormatSearchResultExtended:
    """Расширенные тесты для format_search_result"""

    def test_format_search_result_minimal_data(self):
        """Тест с минимальными данными"""
        result = SearchResult(
            rank=1,
            url="https://example.com",
            title="Test Title",
            snippet="Test snippet",
        )

        formatted = format_search_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://example.com"
        assert formatted["title"] == "Test Title"
        assert formatted["snippet"] == "Test snippet"
        assert formatted["breadcrumbs"] is None
        assert formatted["content_type"] == "organic"  # Значение по умолчанию
        assert formatted["pub_date"] is None
        assert formatted["extended_passage"] is None
        assert formatted["stars"] is None
        assert formatted["sitelinks"] is None
        assert formatted["turbo_link"] is None

    def test_format_search_result_with_nulls(self):
        """Тест с None значениями"""
        result = SearchResult(
            rank=None,
            url="https://example.com",
            title="Test Title",
            snippet=None,
        )

        formatted = format_search_result(result)

        assert formatted["rank"] is None
        assert formatted["url"] == "https://example.com"
        assert formatted["title"] == "Test Title"
        assert formatted["snippet"] is None  # None остается None, не преобразуется в ""
        assert formatted["breadcrumbs"] is None
        assert formatted["content_type"] == "organic"  # Значение по умолчанию

    def test_format_search_result_full_data(self):
        """Тест с полными данными"""
        result = SearchResult(
            rank=1,
            url="https://example.com",
            title="Test Title",
            snippet="Test snippet",
            breadcrumbs="Example > Test",
            content_type="organic",
            pub_date="2023-01-01",
            extended_passage="Extended passage text",
            stars=4.5,
            sitelinks=["link1", "link2"],
            turbo_link="https://turbo.example.com",
        )

        formatted = format_search_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://example.com"
        assert formatted["title"] == "Test Title"
        assert formatted["snippet"] == "Test snippet"
        assert formatted["breadcrumbs"] == "Example > Test"
        assert formatted["content_type"] == "organic"
        assert formatted["pub_date"] == "2023-01-01"
        assert formatted["extended_passage"] == "Extended passage text"
        assert formatted["stars"] == 4.5
        assert formatted["sitelinks"] == ["link1", "link2"]
        assert formatted["turbo_link"] == "https://turbo.example.com"


class TestFormatNewsResult:
    """Тесты для format_news_result"""

    def test_format_news_result_no_media(self):
        """Тест без медиа"""
        result = NewsResult(
            rank=1,
            url="https://news.example.com",
            title="News Title",
            snippet="News snippet",
            media=None,
            pub_date="2023-01-01",
        )

        formatted = format_news_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://news.example.com"
        assert formatted["title"] == "News Title"
        assert formatted["snippet"] == "News snippet"
        assert formatted["media"] is None
        assert formatted["pub_date"] == "2023-01-01"

    def test_format_news_result_no_date(self):
        """Тест без даты"""
        result = NewsResult(
            rank=1,
            url="https://news.example.com",
            title="News Title",
            snippet="News snippet",
            media="image.jpg",
            pub_date=None,
        )

        formatted = format_news_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://news.example.com"
        assert formatted["title"] == "News Title"
        assert formatted["snippet"] == "News snippet"
        assert formatted["media"] == "image.jpg"
        assert formatted["pub_date"] is None

    def test_format_news_result_full_data(self):
        """Тест с полными данными"""
        result = NewsResult(
            rank=1,
            url="https://news.example.com",
            title="News Title",
            snippet="News snippet",
            media="image.jpg",
            pub_date="2023-01-01",
        )

        formatted = format_news_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://news.example.com"
        assert formatted["title"] == "News Title"
        assert formatted["snippet"] == "News snippet"
        assert formatted["media"] == "image.jpg"
        assert formatted["pub_date"] == "2023-01-01"


class TestFormatImageResult:
    """Тесты для format_image_result"""

    def test_format_image_result_no_dimensions(self):
        """Тест без размеров"""
        result = ImageResult(
            rank=1,
            url="https://image.example.com",
            img_url="https://img.example.com/image.jpg",
            title="Image Title",
            display_link="example.com",
            original_width=None,
            original_height=None,
        )

        formatted = format_image_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://image.example.com"
        assert formatted["img_url"] == "https://img.example.com/image.jpg"
        assert formatted["title"] == "Image Title"
        assert formatted["display_link"] == "example.com"
        assert formatted["original_width"] is None
        assert formatted["original_height"] is None

    def test_format_image_result_no_thumbnail(self):
        """Тест без миниатюры"""
        result = ImageResult(
            rank=1,
            url="https://image.example.com",
            img_url=None,
            title="Image Title",
            display_link="example.com",
            original_width=800,
            original_height=600,
        )

        formatted = format_image_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://image.example.com"
        assert formatted["img_url"] is None
        assert formatted["title"] == "Image Title"
        assert formatted["display_link"] == "example.com"
        assert formatted["original_width"] == 800
        assert formatted["original_height"] == 600

    def test_format_image_result_full_data(self):
        """Тест с полными данными"""
        result = ImageResult(
            rank=1,
            url="https://image.example.com",
            img_url="https://img.example.com/image.jpg",
            title="Image Title",
            display_link="example.com",
            original_width=800,
            original_height=600,
        )

        formatted = format_image_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://image.example.com"
        assert formatted["img_url"] == "https://img.example.com/image.jpg"
        assert formatted["title"] == "Image Title"
        assert formatted["display_link"] == "example.com"
        assert formatted["original_width"] == 800
        assert formatted["original_height"] == 600


class TestFormatMapResult:
    """Тесты для format_map_result"""

    def test_format_map_result_no_coords(self):
        """Тест без координат"""
        result = MapResult(
            title="Map Title",
            stars=4.5,
            type="restaurant",
            address="123 Main St",
            url="https://map.example.com",
            phone="+1234567890",
            review="Great place",
            possibility="delivery",
            latitude=None,
            longitude=None,
            place_id="place123",
            count_reviews=100,
            accessibility="wheelchair_accessible",
            price="$$",
            gas_price="3.50",
        )

        formatted = format_map_result(result)

        assert formatted["title"] == "Map Title"
        assert formatted["stars"] == 4.5
        assert formatted["type"] == "restaurant"
        assert formatted["address"] == "123 Main St"
        assert formatted["url"] == "https://map.example.com"
        assert formatted["phone"] == "+1234567890"
        assert formatted["review"] == "Great place"
        assert formatted["possibility"] == "delivery"
        assert formatted["latitude"] is None
        assert formatted["longitude"] is None
        assert formatted["place_id"] == "place123"
        assert formatted["count_reviews"] == 100
        assert formatted["accessibility"] == "wheelchair_accessible"
        assert formatted["price"] == "$$"
        assert formatted["gas_price"] == "3.50"

    def test_format_map_result_minimal_info(self):
        """Тест с минимальной информацией"""
        result = MapResult(
            title="Map Title",
            stars=None,
            type=None,
            address=None,
            url="https://map.example.com",
            phone=None,
            review=None,
            possibility=None,
            latitude=55.7558,
            longitude=37.6176,
            place_id=None,
            count_reviews=None,
            accessibility=None,
            price=None,
            gas_price=None,
        )

        formatted = format_map_result(result)

        assert formatted["title"] == "Map Title"
        assert formatted["stars"] is None
        assert formatted["type"] is None
        assert formatted["address"] is None
        assert formatted["url"] == "https://map.example.com"
        assert formatted["phone"] is None
        assert formatted["review"] is None
        assert formatted["possibility"] is None
        assert formatted["latitude"] == 55.7558
        assert formatted["longitude"] == 37.6176
        assert formatted["place_id"] is None
        assert formatted["count_reviews"] is None
        assert formatted["accessibility"] is None
        assert formatted["price"] is None
        assert formatted["gas_price"] is None


class TestFormatAdsResult:
    """Тесты для format_ads_result"""

    def test_format_ads_result_full_data(self):
        """Тест с полными данными"""
        result = AdResult(
            url="https://ad.example.com",
            ads_url="https://ads.example.com",
            title="Ad Title",
            snippet="Ad snippet",
        )

        formatted = format_ads_result(result)

        assert formatted["url"] == "https://ad.example.com"
        assert formatted["ads_url"] == "https://ads.example.com"
        assert formatted["title"] == "Ad Title"
        assert formatted["snippet"] == "Ad snippet"

    def test_format_ads_result_minimal_data(self):
        """Тест с минимальными данными"""
        result = AdResult(
            url="https://ad.example.com",
            ads_url=None,
            title="Ad Title",
            snippet=None,
        )

        formatted = format_ads_result(result)

        assert formatted["url"] == "https://ad.example.com"
        assert formatted["ads_url"] is None
        assert formatted["title"] == "Ad Title"
        assert formatted["snippet"] is None


class TestFormatAdsResponse:
    """Тесты для format_ads_response"""

    def test_format_ads_response_empty_ads(self):
        """Тест с пустыми рекламными блоками"""
        response = AdsResponse(top_ads=[], bottom_ads=[])

        formatted = format_ads_response(response)

        assert formatted["top_ads"] == []
        assert formatted["bottom_ads"] == []
        assert formatted["total_ads_count"] == 0

    def test_format_ads_response_top_only(self):
        """Тест только с верхними рекламными блоками"""
        top_ad = AdResult(
            url="https://top.example.com",
            ads_url="https://ads.example.com",
            title="Top Ad",
            snippet="Top ad snippet",
        )

        response = AdsResponse(top_ads=[top_ad], bottom_ads=[])

        formatted = format_ads_response(response)

        assert len(formatted["top_ads"]) == 1
        assert formatted["bottom_ads"] == []
        assert formatted["total_ads_count"] == 1
        assert formatted["top_ads"][0]["title"] == "Top Ad"

    def test_format_ads_response_bottom_only(self):
        """Тест только с нижними рекламными блоками"""
        bottom_ad = AdResult(
            url="https://bottom.example.com",
            ads_url="https://ads.example.com",
            title="Bottom Ad",
            snippet="Bottom ad snippet",
        )

        response = AdsResponse(top_ads=[], bottom_ads=[bottom_ad])

        formatted = format_ads_response(response)

        assert formatted["top_ads"] == []
        assert len(formatted["bottom_ads"]) == 1
        assert formatted["total_ads_count"] == 1
        assert formatted["bottom_ads"][0]["title"] == "Bottom Ad"

    def test_format_ads_response_full_data(self):
        """Тест с полными данными"""
        top_ad = AdResult(
            url="https://top.example.com",
            ads_url="https://ads.example.com",
            title="Top Ad",
            snippet="Top ad snippet",
        )

        bottom_ad = AdResult(
            url="https://bottom.example.com",
            ads_url="https://ads.example.com",
            title="Bottom Ad",
            snippet="Bottom ad snippet",
        )

        response = AdsResponse(top_ads=[top_ad], bottom_ads=[bottom_ad])

        formatted = format_ads_response(response)

        assert len(formatted["top_ads"]) == 1
        assert len(formatted["bottom_ads"]) == 1
        assert formatted["total_ads_count"] == 2
        assert formatted["top_ads"][0]["title"] == "Top Ad"
        assert formatted["bottom_ads"][0]["title"] == "Bottom Ad"


class TestFormatOneBoxDocument:
    """Тесты для format_onebox_document"""

    def test_format_onebox_document_full_data(self):
        """Тест с полными данными"""
        doc = OneBoxDocument(
            content_type="weather",
            title="Weather in Moscow",
            url="https://weather.example.com",
            snippet="Temperature: 20°C",
            additional_data={"temperature": "20", "humidity": "60%"},
        )

        formatted = format_onebox_document(doc)

        assert formatted["content_type"] == "weather"
        assert formatted["title"] == "Weather in Moscow"
        assert formatted["url"] == "https://weather.example.com"
        assert formatted["snippet"] == "Temperature: 20°C"
        assert formatted["additional_data"] == {
            "temperature": "20",
            "humidity": "60%",
        }

    def test_format_onebox_document_minimal_data(self):
        """Тест с минимальными данными"""
        doc = OneBoxDocument(
            content_type="calculator",
            title="Calculator",
            url="https://calc.example.com",
            snippet="2 + 2 = 4",
            additional_data=None,
        )

        formatted = format_onebox_document(doc)

        assert formatted["content_type"] == "calculator"
        assert formatted["title"] == "Calculator"
        assert formatted["url"] == "https://calc.example.com"
        assert formatted["snippet"] == "2 + 2 = 4"
        assert formatted["additional_data"] is None


class TestFormatSearchsterResult:
    """Тесты для format_searchster_result"""

    def test_format_searchster_result_full_data(self):
        """Тест с полными данными"""
        result = SearchsterResult(
            content_type="weather",
            title="Weather in Moscow",
            url="https://weather.example.com",
            snippet="Temperature: 20°C",
            additional_data={"temperature": "20", "humidity": "60%"},
        )

        formatted = format_searchster_result(result)

        assert formatted["content_type"] == "weather"
        assert formatted["title"] == "Weather in Moscow"
        assert formatted["url"] == "https://weather.example.com"
        assert formatted["snippet"] == "Temperature: 20°C"
        assert formatted["additional_data"] == {
            "temperature": "20",
            "humidity": "60%",
        }

    def test_format_searchster_result_minimal_data(self):
        """Тест с минимальными данными"""
        result = SearchsterResult(
            content_type="calculator",
            title="Calculator",
            url="https://calc.example.com",
            snippet="2 + 2 = 4",
            additional_data=None,
        )

        formatted = format_searchster_result(result)

        assert formatted["content_type"] == "calculator"
        assert formatted["title"] == "Calculator"
        assert formatted["url"] == "https://calc.example.com"
        assert formatted["snippet"] == "2 + 2 = 4"
        assert formatted["additional_data"] is None


class TestFormatRelatedSearch:
    """Тесты для format_related_search"""

    def test_format_related_search_full_data(self):
        """Тест с полными данными"""
        search = RelatedSearch(
            query="python programming",
            url="https://search.example.com?q=python+programming",
        )

        formatted = format_related_search(search)

        assert formatted["query"] == "python programming"
        assert formatted["url"] == "https://search.example.com?q=python+programming"

    def test_format_related_search_minimal_data(self):
        """Тест с минимальными данными"""
        search = RelatedSearch(query="test query", url=None)

        formatted = format_related_search(search)

        assert formatted["query"] == "test query"
        assert formatted["url"] is None


class TestFormatSearchStats:
    """Тесты для format_search_stats"""

    def test_format_search_stats_with_content_types(self):
        """Тест со статистикой типов контента"""
        results = [
            SearchResult(
                rank=1,
                url="https://example1.com",
                title="Title 1",
                snippet="Snippet 1",
                content_type="organic",
            ),
            SearchResult(
                rank=2,
                url="https://example2.com",
                title="Title 2",
                snippet="Snippet 2",
                content_type="organic",
            ),
            SearchResult(
                rank=3,
                url="https://example3.com",
                title="Title 3",
                snippet="Snippet 3",
                content_type="video",
            ),
        ]

        response = SearchResponse(
            query="test query",
            total_results=100,
            results=results,
            showing_results_for="test",
            correct="corrected query",
            fixtype="spelling",
        )

        formatted = format_search_stats(response)

        assert formatted["total_results"] == 100
        assert formatted["returned_results"] == 3
        assert formatted["content_types"]["organic"] == 2
        assert formatted["content_types"]["video"] == 1
        assert formatted["has_corrections"] is True
        assert formatted["has_fixtype"] is True

    def test_format_search_stats_no_content_types(self):
        """Тест без типов контента"""
        results = [
            SearchResult(
                rank=1,
                url="https://example1.com",
                title="Title 1",
                snippet="Snippet 1",
            )
        ]

        response = SearchResponse(
            query="test query",
            total_results=50,
            results=results,
            showing_results_for="test",
        )

        formatted = format_search_stats(response)

        assert formatted["total_results"] == 50
        assert formatted["returned_results"] == 1
        assert formatted["content_types"] == {
            "organic": 1
        }  # content_type по умолчанию "organic"
        assert formatted["has_corrections"] is False
        assert formatted["has_fixtype"] is False


class TestFormatAdsStats:
    """Тесты для format_ads_stats"""

    def test_format_ads_stats_with_ads(self):
        """Тест со статистикой рекламы"""
        top_ad = AdResult(
            url="https://top.example.com",
            ads_url="https://ads.example.com",
            title="Top Ad",
            snippet="Top ad snippet",
        )

        bottom_ad = AdResult(
            url="https://bottom.example.com",
            ads_url="https://ads.example.com",
            title="Bottom Ad",
            snippet="Bottom ad snippet",
        )

        response = AdsResponse(top_ads=[top_ad], bottom_ads=[bottom_ad])

        formatted = format_ads_stats(response)

        assert formatted["top_ads_count"] == 1
        assert formatted["bottom_ads_count"] == 1
        assert formatted["total_ads_count"] == 2
        assert formatted["has_ads"] is True

    def test_format_ads_stats_no_ads(self):
        """Тест без рекламы"""
        response = AdsResponse(top_ads=[], bottom_ads=[])

        formatted = format_ads_stats(response)

        assert formatted["top_ads_count"] == 0
        assert formatted["bottom_ads_count"] == 0
        assert formatted["total_ads_count"] == 0
        assert formatted["has_ads"] is False


class TestFormatResultsSummary:
    """Тесты для format_results_summary"""

    def test_format_results_summary_basic(self):
        """Тест базового форматирования"""
        response = SearchResponse(
            query="test query",
            total_results=1000,
            results=[],
            showing_results_for="test",
        )

        summary = format_results_summary(response)

        assert "Найдено 1,000 результатов, показано 0" in summary

    def test_format_results_summary_with_correction(self):
        """Тест с исправлением"""
        response = SearchResponse(
            query="test query",
            total_results=500,
            results=[],
            showing_results_for="test",
            correct="original query",
        )

        summary = format_results_summary(response)

        assert "Найдено 500 результатов, показано 0" in summary
        assert "исправлено с 'original query'" in summary

    def test_format_results_summary_with_fixtype(self):
        """Тест с типом исправления"""
        response = SearchResponse(
            query="test query",
            total_results=300,
            results=[],
            showing_results_for="test",
            fixtype="spelling",
        )

        summary = format_results_summary(response)

        assert "Найдено 300 результатов, показано 0" in summary
        assert "тип исправления: spelling" in summary

    def test_format_results_summary_full(self):
        """Тест с полными данными"""
        response = SearchResponse(
            query="test query",
            total_results=200,
            results=[],
            showing_results_for="test",
            correct="original query",
            fixtype="spelling",
        )

        summary = format_results_summary(response)

        assert "Найдено 200 результатов, показано 0" in summary
        assert "исправлено с 'original query'" in summary
        assert "тип исправления: spelling" in summary


class TestFormatAdsSummary:
    """Тесты для format_ads_summary"""

    def test_format_ads_summary_no_ads(self):
        """Тест без рекламы"""
        response = AdsResponse(top_ads=[], bottom_ads=[])

        summary = format_ads_summary(response)

        assert summary == "Реклама не найдена"

    def test_format_ads_summary_top_only(self):
        """Тест только с верхними рекламными блоками"""
        top_ad = AdResult(
            url="https://top.example.com",
            ads_url="https://ads.example.com",
            title="Top Ad",
            snippet="Top ad snippet",
        )

        response = AdsResponse(top_ads=[top_ad], bottom_ads=[])

        summary = format_ads_summary(response)

        assert "Найдено 1 рекламных блоков" in summary
        assert "верхние: 1" in summary

    def test_format_ads_summary_bottom_only(self):
        """Тест только с нижними рекламными блоками"""
        bottom_ad = AdResult(
            url="https://bottom.example.com",
            ads_url="https://ads.example.com",
            title="Bottom Ad",
            snippet="Bottom ad snippet",
        )

        response = AdsResponse(top_ads=[], bottom_ads=[bottom_ad])

        summary = format_ads_summary(response)

        assert "Найдено 1 рекламных блоков" in summary
        assert "нижние: 1" in summary

    def test_format_ads_summary_both(self):
        """Тест с обоими типами рекламных блоков"""
        top_ad = AdResult(
            url="https://top.example.com",
            ads_url="https://ads.example.com",
            title="Top Ad",
            snippet="Top ad snippet",
        )

        bottom_ad = AdResult(
            url="https://bottom.example.com",
            ads_url="https://ads.example.com",
            title="Bottom Ad",
            snippet="Bottom ad snippet",
        )

        response = AdsResponse(top_ads=[top_ad], bottom_ads=[bottom_ad])

        summary = format_ads_summary(response)

        assert "Найдено 2 рекламных блоков" in summary
        assert "верхние: 1" in summary
        assert "нижние: 1" in summary


class TestFormatErrorMessage:
    """Тесты для format_error_message"""

    def test_format_error_message_with_code_and_message(self):
        """Тест с кодом и сообщением"""

        class CustomError(Exception):
            def __init__(self, code, message):
                self.code = code
                self.message = message

        error = CustomError("404", "Not found")

        formatted = format_error_message(error)

        assert formatted == "[404] Not found"

    def test_format_error_message_without_code_and_message(self):
        """Тест без кода и сообщения"""
        error = ValueError("Simple error message")

        formatted = format_error_message(error)

        assert formatted == "Simple error message"

    def test_format_error_message_with_code_only(self):
        """Тест только с кодом"""

        class CustomError(Exception):
            def __init__(self, code):
                self.code = code

        error = CustomError("500")

        formatted = format_error_message(error)

        assert formatted == "500"


class TestFormatApiResponse:
    """Тесты для format_api_response"""

    def test_format_api_response_with_error(self):
        """Тест с ошибкой API"""
        response_data = {"error": {"@code": "404", "#text": "Not found"}}

        formatted = format_api_response(response_data)

        assert formatted == "Ошибка API [404]: Not found"

    def test_format_api_response_with_found(self):
        """Тест с найденными результатами"""
        response_data = {"found": {"#text": "1000"}}

        formatted = format_api_response(response_data)

        assert formatted == "Успешно получено 1000 результатов"

    def test_format_api_response_with_found_string(self):
        """Тест с найденными результатами как строка"""
        response_data = {"found": "500"}

        formatted = format_api_response(response_data)

        assert formatted == "Успешно получено 0 результатов"

    def test_format_api_response_success(self):
        """Тест успешного ответа"""
        response_data = {"success": True, "data": "some data"}

        formatted = format_api_response(response_data)

        assert formatted == "Ответ получен успешно"
