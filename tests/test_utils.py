"""
Тесты для утилит
"""

import pytest
from xmlriver_pro.utils.validators import validate_coords, validate_zoom
from xmlriver_pro.utils.formatters import (
    format_search_result,
    format_search_response,
)


class TestValidators:
    """Тесты для валидаторов"""

    def test_validate_coords_valid(self):
        """Тест валидации валидных координат"""
        assert validate_coords((55.7558, 37.6176)) is True
        assert validate_coords((0.0, 0.0)) is True
        assert validate_coords((90.0, 180.0)) is True
        assert validate_coords((-90.0, -180.0)) is True

    def test_validate_coords_invalid(self):
        """Тест валидации невалидных координат"""
        assert validate_coords((91.0, 0.0)) is False
        assert validate_coords((-91.0, 0.0)) is False
        assert validate_coords((0.0, 181.0)) is False
        assert validate_coords((0.0, -181.0)) is False
        assert validate_coords((0.0,)) is False
        assert validate_coords(None) is False

    def test_validate_zoom_valid(self):
        """Тест валидации валидного уровня зума"""
        assert validate_zoom(1) is True
        assert validate_zoom(10) is True
        assert validate_zoom(15) is True

    def test_validate_zoom_invalid(self):
        """Тест валидации невалидного уровня зума"""
        assert validate_zoom(0) is False
        assert validate_zoom(16) is False
        assert validate_zoom(-1) is False
        assert validate_zoom("invalid") is False
        assert validate_zoom(None) is False


class TestFormatters:
    """Тесты для форматтеров"""

    def test_format_search_result(self):
        """Тест форматирования результата поиска"""
        from xmlriver_pro.core.types import SearchResult

        result = SearchResult(
            rank=1,
            url="https://example.com",
            title="Test Title",
            snippet="Test snippet",
            breadcrumbs="Example > Test",
            content_type="organic",
        )

        formatted = format_search_result(result)

        assert formatted["rank"] == 1
        assert formatted["url"] == "https://example.com"
        assert formatted["title"] == "Test Title"
        assert formatted["snippet"] == "Test snippet"
        assert formatted["breadcrumbs"] == "Example > Test"
        assert formatted["content_type"] == "organic"

    def test_format_search_response(self):
        """Тест форматирования ответа поиска"""
        from xmlriver_pro.core.types import SearchResponse, SearchResult

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
        ]

        response = SearchResponse(
            query="test query",
            total_results=100,
            results=results,
            showing_results_for="test",
        )

        formatted = format_search_response(response)

        assert formatted["query"] == "test query"
        assert formatted["total_results"] == 100
        assert formatted["showing_results_for"] == "test"
        assert len(formatted["results"]) == 2
        assert formatted["results"][0]["title"] == "Title 1"
        assert formatted["results"][1]["title"] == "Title 2"
