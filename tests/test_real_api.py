import os
import pytest
from dotenv import load_dotenv
from xmlriver_pro.google import GoogleClient
from xmlriver_pro.yandex import YandexClient

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем учетные данные из переменных окружения
USER_ID = os.getenv("XMLRIVER_USER_ID")
API_KEY = os.getenv("XMLRIVER_API_KEY")

# Пропускаем все тесты в этом файле, если учетные данные не установлены
pytestmark = pytest.mark.skipif(
    not USER_ID or not API_KEY,
    reason="XMLRIVER_USER_ID and XMLRIVER_API_KEY are not set in the environment",
)


@pytest.fixture(scope="module")
def google_client():
    """Фикстура для создания клиента Google."""
    return GoogleClient(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def yandex_client():
    """Фикстура для создания клиента Yandex."""
    return YandexClient(user_id=int(USER_ID), api_key=API_KEY)


def test_get_balance(google_client):
    """Тест для проверки получения баланса."""
    balance = google_client.get_balance()
    assert isinstance(balance, float)
    assert balance >= 0


def test_google_search_by_city(google_client):
    """Тест для поиска в Google по городу (Москва)."""
    # ID России для Google - 2643
    response = google_client.search("погода в москве", country=2643)
    assert response is not None
    assert len(response.results) > 0


def test_yandex_search_by_city(yandex_client):
    """Тест для поиска в Яндексе по городу (Санкт-Петербург)."""
    # ID Санкт-Петербурга для Яндекса - 2
    response = yandex_client.search("достопримечательности", lr=2)
    assert response is not None
    assert len(response.results) > 0


def test_commercial_query_google(google_client):
    """Тест для коммерческого запроса в Google."""
    response = google_client.search("купить ноутбук")
    assert response is not None
    assert len(response.results) > 0
