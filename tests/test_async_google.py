"""
Тесты для AsyncGoogleClient
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core.types import (
    SearchType,
    DeviceType,
    OSType,
    SearchResponse,
    SearchResult,
)
from xmlriver_pro.core.exceptions import (
    ValidationError,
    RateLimitError,
    NetworkError,
)


class TestAsyncGoogleClient:
    """Тесты для AsyncGoogleClient"""

    @pytest.fixture
    def client(self):
        """Фикстура для создания клиента"""
        return AsyncGoogleClient(user_id=123, api_key="test_key")

    @pytest.fixture
    def mock_session(self):
        """Фикстура для мокирования aiohttp сессии"""
        session = AsyncMock()
        response = AsyncMock()
        response.status = 200
        response.text = AsyncMock(
            return_value="""
        <response>
            <total>100</total>
            <query>test query</query>
            <search_time>0.5</search_time>
            <results>
                <result>
                    <title>Test Result</title>
                    <url>https://example.com</url>
                    <snippet>Test snippet</snippet>
                    <position>1</position>
                </result>
            </results>
        </response>
        """
        )

        # Создаем контекстный менеджер для get()
        context_manager = AsyncMock()
        context_manager.__aenter__ = AsyncMock(return_value=response)
        context_manager.__aexit__ = AsyncMock(return_value=None)

        # Мокируем get() как корутину, которая возвращает контекстный менеджер
        session.get = AsyncMock(return_value=context_manager)

        return session

    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """Тест инициализации клиента"""
        assert client.user_id == 123
        assert client.api_key == "test_key"
        assert client.system == "google"
        assert client.timeout == 60

    @pytest.mark.asyncio
    async def test_context_manager(self, client, mock_session):
        """Тест работы с контекстным менеджером"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client as c:
                assert c._session is not None
                assert c._own_session is True

    @pytest.mark.asyncio
    async def test_search_basic(self, client, mock_session):
        """Тест базового поиска"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.search("test query")
                assert result.total_results == 100
                assert result.query == "test query"
                assert len(result.results) == 1

    @pytest.mark.asyncio
    async def test_search_with_parameters(self, client, mock_session):
        """Тест поиска с параметрами"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.search(
                    query="test query",
                    search_type=SearchType.ORGANIC,
                    num_results=20,
                    start=10,
                    device=DeviceType.MOBILE,
                    os=OSType.ANDROID,
                )
                assert result.total_results == 100

    @pytest.mark.asyncio
    async def test_search_news(self, client, mock_session):
        """Тест поиска новостей"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.search_news("test news")
                assert result.total_results == 100

    @pytest.mark.asyncio
    async def test_search_images(self, client, mock_session):
        """Тест поиска изображений"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.search_images(
                    "test images",
                    size="large",
                    color="color",
                    image_type="photo",
                )
                assert result.total_results == 100

    @pytest.mark.asyncio
    async def test_search_maps(self, client, mock_session):
        """Тест поиска по картам"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.search_maps(
                    "test maps", coords=(55.7558, 37.6176), zoom=10
                )
                assert result.total_results == 100

    @pytest.mark.asyncio
    async def test_get_ads(self, client, mock_session):
        """Тест получения рекламных блоков"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.get_ads("test ads")
                assert result.total_results == 100

    @pytest.mark.asyncio
    async def test_get_special_blocks(self, client, mock_session):
        """Тест получения специальных блоков"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.get_special_blocks("test special")
                assert result.total_results == 100

    @pytest.mark.asyncio
    async def test_validation_errors(self, client):
        """Тест ошибок валидации"""
        with pytest.raises(ValidationError):
            await client.search("", num_results=0)  # Пустой запрос

        with pytest.raises(ValidationError):
            await client.search("test", num_results=101)  # Слишком много результатов

        with pytest.raises(ValidationError):
            await client.search("test", start=-1)  # Отрицательный start

    @pytest.mark.asyncio
    async def test_rate_limit_error(self, client):
        """Тест ошибки превышения лимитов"""
        mock_session = AsyncMock()
        response = AsyncMock()
        response.status = 429
        response.text = AsyncMock(return_value="Rate limit exceeded")

        # Создаем контекстный менеджер для get()
        context_manager = AsyncMock()
        context_manager.__aenter__ = AsyncMock(return_value=response)
        context_manager.__aexit__ = AsyncMock(return_value=None)

        # Мокируем get() как корутину, которая возвращает контекстный менеджер
        mock_session.get = AsyncMock(return_value=context_manager)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                with pytest.raises(RateLimitError):
                    await client.search("test query")

    @pytest.mark.asyncio
    async def test_get_api_limits(self, client):
        """Тест получения лимитов API"""
        limits = client.get_api_limits()
        assert "max_concurrent_streams" in limits
        assert "daily_limits" in limits
        assert "recommendations" in limits
        assert limits["max_concurrent_streams"] == 10

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client, mock_session):
        """Тест параллельных запросов"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                # Создаем несколько задач
                tasks = [
                    client.search("query 1"),
                    client.search("query 2"),
                    client.search("query 3"),
                ]

                # Выполняем параллельно
                results = await asyncio.gather(*tasks)

                assert len(results) == 3
                for result in results:
                    assert result.total_results == 100

    @pytest.mark.asyncio
    async def test_session_management(self, client):
        """Тест управления сессией"""
        # Тест без контекстного менеджера
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value = mock_session

            # Создаем клиента с собственной сессией
            client_with_session = AsyncGoogleClient(
                user_id=123, api_key="test_key", session=mock_session
            )

            async with client_with_session:
                assert client_with_session._session == mock_session
                assert client_with_session._own_session is False


class TestAsyncGoogleClientRetry:
    """Тесты retry механизма для AsyncGoogleClient"""

    def test_retry_configuration_defaults(self):
        """Тест конфигурации retry по умолчанию"""
        client = AsyncGoogleClient(user_id=123, api_key="test_key")

        assert client.timeout == 60
        assert client.max_retries == 3
        assert client.retry_delay == 1.0
        assert client.enable_retry is True

    def test_retry_configuration_custom(self):
        """Тест кастомной конфигурации retry"""
        client = AsyncGoogleClient(
            user_id=123,
            api_key="test_key",
            timeout=120,
            max_retries=5,
            retry_delay=2.0,
            enable_retry=False,
        )

        assert (
            client.timeout == 60
        )  # Максимум 60, но передали 120 - должно быть ограничено
        assert client.max_retries == 5
        assert client.retry_delay == 2.0
        assert client.enable_retry is False

    @pytest.mark.asyncio
    async def test_retry_disabled(self):
        """Тест отключенного retry"""
        client = AsyncGoogleClient(user_id=123, api_key="test_key", enable_retry=False)

        with patch(
            "xmlriver_pro.core.async_base_client.AsyncBaseClient._make_single_request"
        ) as mock_single_request:
            # Мокаем успешный ответ
            mock_response = SearchResponse(
                query="test",
                total_results=10,
                results=[
                    SearchResult(
                        rank=1,
                        title="Test",
                        url="http://test.com",
                        snippet="Test snippet",
                    )
                ],
            )
            mock_single_request.return_value = mock_response

            async with client:
                result = await client.search("test")

            # Должен быть только один вызов без повторов
            mock_single_request.assert_called_once()
            assert result is not None

    @pytest.mark.asyncio
    async def test_retry_with_exponential_backoff(self):
        """Тест retry с экспоненциальным backoff"""
        client = AsyncGoogleClient(
            user_id=123,
            api_key="test_key",
            max_retries=3,
            retry_delay=0.1,  # Быстрый тест
        )

        with patch(
            "xmlriver_pro.core.async_base_client.AsyncBaseClient._make_single_request"
        ) as mock_single_request:
            with patch("asyncio.sleep") as mock_sleep:
                # Первые два вызова падают, третий успешен
                mock_response = SearchResponse(
                    query="test",
                    total_results=10,
                    results=[
                        SearchResult(
                            rank=1,
                            title="Test",
                            url="http://test.com",
                            snippet="Test snippet",
                        )
                    ],
                )
                mock_single_request.side_effect = [
                    NetworkError(999, "Network error"),
                    NetworkError(999, "Network error"),
                    mock_response,
                ]

                async with client:
                    result = await client.search("test")

                # Проверяем количество вызовов
                assert mock_single_request.call_count == 3

                # Проверяем задержки: 0.1, 0.2 секунды
                expected_delays = [0.1, 0.2]
                actual_delays = [call[0][0] for call in mock_sleep.call_args_list]
                assert actual_delays == expected_delays

                assert result is not None

    @pytest.mark.asyncio
    async def test_retry_max_attempts_exceeded(self):
        """Тест превышения максимального количества попыток"""
        client = AsyncGoogleClient(
            user_id=123,
            api_key="test_key",
            max_retries=2,
            retry_delay=0.01,  # Быстрый тест
        )

        with patch(
            "xmlriver_pro.core.async_base_client.AsyncBaseClient._make_single_request"
        ) as mock_single_request:
            with patch("asyncio.sleep") as mock_sleep:
                # Все попытки падают
                mock_single_request.side_effect = NetworkError(999, "Persistent error")

                async with client:
                    with pytest.raises(NetworkError, match="Persistent error"):
                        await client.search("test")

                # Проверяем количество попыток
                assert mock_single_request.call_count == 2
