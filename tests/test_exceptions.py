"""
Тесты для системы исключений
"""

import pytest
from xmlriver_pro.core.exceptions import (
    XMLRiverError,
    APIError,
    NetworkError,
    AuthenticationError,
    RateLimitError,
    NoResultsError,
    ValidationError,
    get_error_message,
    raise_xmlriver_error,
)


class TestXMLRiverError:
    """Тесты для базового исключения XMLRiverError"""

    def test_init_with_code_and_message(self):
        """Тест инициализации с кодом и сообщением"""
        error = XMLRiverError(123, "Test error")
        assert error.message == "Test error"
        assert error.code == 123
        assert str(error) == "[123] Test error"

    def test_init_with_message_only(self):
        """Тест инициализации только с сообщением"""
        error = XMLRiverError(123, "Test error")
        assert error.message == "Test error"
        assert error.code == 123
        assert str(error) == "[123] Test error"

    def test_inheritance(self):
        """Тест наследования от Exception"""
        error = XMLRiverError(123, "Test error")
        assert isinstance(error, Exception)


class TestAPIError:
    """Тесты для APIError"""

    def test_inheritance(self):
        """Тест наследования от XMLRiverError"""
        error = APIError(500, "API error")
        assert isinstance(error, XMLRiverError)
        assert error.message == "API error"
        assert error.code == 500


class TestNetworkError:
    """Тесты для NetworkError"""

    def test_inheritance(self):
        """Тест наследования от XMLRiverError"""
        error = NetworkError(999, "Network error")
        assert isinstance(error, XMLRiverError)
        assert error.message == "Network error"
        assert error.code == 999


class TestValidationError:
    """Тесты для ValidationError"""

    def test_inheritance(self):
        """Тест наследования от XMLRiverError"""
        error = ValidationError(422, "Validation error")
        assert isinstance(error, XMLRiverError)
        assert error.message == "Validation error"
        assert error.code == 422


class TestAuthenticationError:
    """Тесты для AuthenticationError"""

    def test_inheritance(self):
        """Тест наследования от XMLRiverError"""
        error = AuthenticationError(401, "Auth failed")
        assert isinstance(error, XMLRiverError)
        assert error.message == "Auth failed"
        assert error.code == 401


class TestRateLimitError:
    """Тесты для RateLimitError"""

    def test_inheritance(self):
        """Тест наследования от XMLRiverError"""
        error = RateLimitError(429, "Rate limit exceeded")
        assert isinstance(error, XMLRiverError)
        assert error.message == "Rate limit exceeded"
        assert error.code == 429


class TestNoResultsError:
    """Тесты для NoResultsError"""

    def test_inheritance(self):
        """Тест наследования от XMLRiverError"""
        error = NoResultsError(404, "No results found")
        assert isinstance(error, XMLRiverError)
        assert error.message == "No results found"
        assert error.code == 404


class TestGetErrorMessage:
    """Тесты для get_error_message"""

    def test_get_known_error_message(self):
        """Тест получения известного сообщения об ошибке"""
        message = get_error_message(15)
        assert (
            message == "Для заданного поискового запроса отсутствуют результаты поиска"
        )

    def test_get_unknown_error_message(self):
        """Тест получения неизвестного сообщения об ошибке"""
        message = get_error_message(999)
        assert message == "Неизвестная ошибка"

    def test_get_authentication_error_message(self):
        """Тест получения сообщения об ошибке аутентификации"""
        message = get_error_message(31)
        assert message == "Пользователь не зарегистрирован на сервисе"


class TestRaiseXmlRiverError:
    """Тесты для raise_xmlriver_error"""

    def test_raise_no_results_error(self):
        """Тест вызова NoResultsError"""
        with pytest.raises(NoResultsError):
            raise_xmlriver_error(15)

    def test_raise_authentication_error(self):
        """Тест вызова AuthenticationError"""
        with pytest.raises(AuthenticationError):
            raise_xmlriver_error(31)

    def test_raise_rate_limit_error(self):
        """Тест вызова RateLimitError"""
        with pytest.raises(RateLimitError):
            raise_xmlriver_error(110)

    def test_raise_network_error(self):
        """Тест вызова NetworkError"""
        with pytest.raises(NetworkError):
            raise_xmlriver_error(500)

    def test_raise_validation_error(self):
        """Тест вызова ValidationError"""
        with pytest.raises(ValidationError):
            raise_xmlriver_error(102)

    def test_raise_api_error(self):
        """Тест вызова APIError для неизвестной ошибки"""
        with pytest.raises(APIError):
            raise_xmlriver_error(999)


class TestExceptionChaining:
    """Тесты для цепочки исключений"""

    def test_exception_chaining(self):
        """Тест цепочки исключений"""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise APIError(500, "API error") from e
        except APIError as api_error:
            assert api_error.__cause__ is not None
            assert isinstance(api_error.__cause__, ValueError)
            assert str(api_error.__cause__) == "Original error"


class TestExceptionEquality:
    """Тесты для сравнения исключений"""

    def test_exception_equality(self):
        """Тест равенства исключений"""
        error1 = APIError(500, "Test error")
        error2 = APIError(500, "Test error")
        error3 = APIError(500, "Different error")
        error4 = APIError(400, "Test error")

        # Исключения не равны по умолчанию (разные объекты)
        assert error1 != error2
        assert error1 != error3
        assert error1 != error4

    def test_exception_attributes(self):
        """Тест атрибутов исключений"""
        error = APIError(500, "Test error")
        assert hasattr(error, "message")
        assert hasattr(error, "code")
        assert error.message == "Test error"
        assert error.code == 500
