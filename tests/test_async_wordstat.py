"""
Тесты для AsyncWordstatClient
"""

import pytest
from xmlriver_pro import AsyncWordstatClient
from xmlriver_pro.core import (
    WordstatKeyword,
    WordstatResponse,
    WordstatHistoryPoint,
    WordstatHistoryResponse,
    ValidationError,
)


@pytest.mark.asyncio
async def test_wordstat_client_init():
    """Тест инициализации Wordstat клиента"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key") as client:
        assert client.user_id == 123
        assert client.api_key == "test_key"
        assert client.system == "wordstat"
        assert client.timeout == 60
        assert client.max_concurrent == 10


@pytest.mark.asyncio
async def test_wordstat_build_params():
    """Тест формирования параметров запроса"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key") as client:
        params = client._build_params(
            query="python programming",
            pagetype="words",
            regions=213,
            device="desktop",
        )

        assert params["query"] == "python programming"
        assert params["pagetype"] == "words"
        assert params["regions"] == 213
        assert params["device"] == "desktop"
        assert params["user"] == 123
        assert params["key"] == "test_key"


@pytest.mark.asyncio
async def test_wordstat_ampersand_replacement():
    """Тест замены амперсанда в запросе"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key") as client:
        params = client._build_params(
            query="black & white", pagetype="words"
        )
        assert params["query"] == "black %26 white"


@pytest.mark.asyncio
async def test_wordstat_parse_words_response():
    """Тест парсинга ответа с топами запросов"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key") as client:
        mock_data = {
            "associations": [
                {"text": "python programming", "value": "1000", "isAssociations": True},
                {"text": "python tutorial", "value": "500", "isAssociations": True},
            ],
            "popular": [
                {"text": "python", "value": "10000", "isAssociations": False},
            ],
        }

        response = client._parse_words_response("python", mock_data)

        assert isinstance(response, WordstatResponse)
        assert response.query == "python"
        assert len(response.associations) == 2
        assert len(response.popular) == 1

        assert response.associations[0].text == "python programming"
        assert response.associations[0].value == 1000
        assert response.associations[0].is_association is True

        assert response.popular[0].text == "python"
        assert response.popular[0].value == 10000
        assert response.popular[0].is_association is False


@pytest.mark.asyncio
async def test_wordstat_parse_history_response():
    """Тест парсинга ответа с динамикой"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key") as client:
        mock_data = {
            "totalValue": 5000,
            "graph": {
                "tableData": [
                    {
                        "text": "01.01.2024 - 31.01.2024",
                        "absoluteValue": "1000",
                        "value": "0,20",
                    },
                    {
                        "text": "01.02.2024 - 29.02.2024",
                        "absoluteValue": "1500",
                        "value": "0,30",
                    },
                ]
            },
            "table": {
                "tableData": {
                    "associations": [
                        {"text": "python programming", "value": "1000", "isAssociations": True},
                    ],
                    "popular": [
                        {"text": "python", "value": "10000", "isAssociations": False},
                    ],
                }
            },
        }

        response = client._parse_history_response("python", mock_data)

        assert isinstance(response, WordstatHistoryResponse)
        assert response.query == "python"
        assert response.total_value == 5000
        assert len(response.history) == 2
        assert len(response.associations) == 1
        assert len(response.popular) == 1

        assert response.history[0].date == "01.01.2024 - 31.01.2024"
        assert response.history[0].absolute_value == 1000
        assert response.history[0].relative_value == 0.20


@pytest.mark.asyncio
async def test_wordstat_empty_query_validation():
    """Тест валидации пустого запроса"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key") as client:
        with pytest.raises(ValidationError) as exc_info:
            await client.get_words("")

        assert exc_info.value.code == 2
        assert "пустой поисковый запрос" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_wordstat_invalid_period_validation():
    """Тест валидации неверного периода"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key") as client:
        with pytest.raises(ValidationError) as exc_info:
            await client.get_history("python", period="invalid")

        assert exc_info.value.code == 400
        assert "неверный период" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_wordstat_concurrent_status():
    """Тест получения статуса семафора"""
    async with AsyncWordstatClient(user_id=123, api_key="test_key", max_concurrent=5) as client:
        status = client.get_concurrent_status()

        assert status["active_requests"] == 0
        assert status["max_concurrent"] == 5
        assert status["available_slots"] == 5


# Тесты для типов данных


def test_wordstat_keyword_creation():
    """Тест создания WordstatKeyword"""
    keyword = WordstatKeyword(
        text="python programming",
        value=1000,
        is_association=True,
    )

    assert keyword.text == "python programming"
    assert keyword.value == 1000
    assert keyword.is_association is True


def test_wordstat_response_creation():
    """Тест создания WordstatResponse"""
    associations = [
        WordstatKeyword(text="python tutorial", value=500, is_association=True),
    ]
    popular = [
        WordstatKeyword(text="python", value=10000, is_association=False),
    ]

    response = WordstatResponse(
        query="python",
        associations=associations,
        popular=popular,
    )

    assert response.query == "python"
    assert len(response.associations) == 1
    assert len(response.popular) == 1


def test_wordstat_history_point_creation():
    """Тест создания WordstatHistoryPoint"""
    point = WordstatHistoryPoint(
        date="01.01.2024 - 31.01.2024",
        absolute_value=1000,
        relative_value=0.20,
    )

    assert point.date == "01.01.2024 - 31.01.2024"
    assert point.absolute_value == 1000
    assert point.relative_value == 0.20


def test_wordstat_history_response_creation():
    """Тест создания WordstatHistoryResponse"""
    history = [
        WordstatHistoryPoint(
            date="01.01.2024 - 31.01.2024",
            absolute_value=1000,
            relative_value=0.20,
        ),
    ]
    associations = [
        WordstatKeyword(text="python tutorial", value=500, is_association=True),
    ]
    popular = [
        WordstatKeyword(text="python", value=10000, is_association=False),
    ]

    response = WordstatHistoryResponse(
        query="python",
        total_value=5000,
        history=history,
        associations=associations,
        popular=popular,
    )

    assert response.query == "python"
    assert response.total_value == 5000
    assert len(response.history) == 1
    assert len(response.associations) == 1
    assert len(response.popular) == 1

