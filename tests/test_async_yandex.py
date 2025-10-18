"""
Тесты для AsyncYandexClient
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from xmlriver_pro import AsyncYandexClient
from xmlriver_pro.core.types import SearchType, DeviceType, OSType
from xmlriver_pro.core.exceptions import ValidationError, RateLimitError


class TestAsyncYandexClient:
    """Тесты для AsyncYandexClient"""

    @pytest.fixture
    def client(self):
        """Фикстура для создания клиента"""
        return AsyncYandexClient(user_id=123, api_key="test_key")

    @pytest.fixture
    def mock_session(self):
        """Фикстура для мокирования aiohttp сессии"""
        session = AsyncMock()
        response = AsyncMock()
        response.status = 200
        response.text = AsyncMock(
            return_value="""
        <response>
            <total>50</total>
            <query>test query</query>
            <search_time>0.3</search_time>
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
        assert client.system == "yandex"
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
                assert result.total_results == 50
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
                assert result.total_results == 50

    @pytest.mark.asyncio
    async def test_search_news(self, client, mock_session):
        """Тест поиска новостей"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.search_news("test news")
                assert result.total_results == 50

    @pytest.mark.asyncio
    async def test_get_ads(self, client, mock_session):
        """Тест получения рекламных блоков"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.get_ads("test ads")
                assert result.total_results == 50

    @pytest.mark.asyncio
    async def test_get_special_blocks(self, client, mock_session):
        """Тест получения специальных блоков"""
        with patch("aiohttp.ClientSession", return_value=mock_session):
            async with client:
                result = await client.get_special_blocks("test special")
                assert result.total_results == 50

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
        assert limits["daily_limits"]["yandex"] == 150000

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
                    assert result.total_results == 50

    @pytest.mark.asyncio
    async def test_session_management(self, client):
        """Тест управления сессией"""
        # Тест без контекстного менеджера
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value = mock_session

            # Создаем клиента с собственной сессией
            client_with_session = AsyncYandexClient(
                user_id=123, api_key="test_key", session=mock_session
            )

            async with client_with_session:
                assert client_with_session._session == mock_session
                assert client_with_session._own_session is False
