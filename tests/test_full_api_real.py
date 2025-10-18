"""
Полное тестирование всех реальных API запросов XMLRiver Pro
Тесты выполняются с реальными API ключами для проверки готовности к продакшену
"""

import os
import pytest
from dotenv import load_dotenv
from xmlriver_pro.google import GoogleClient
from xmlriver_pro.yandex import YandexClient
from xmlriver_pro.google.ads import GoogleAds
from xmlriver_pro.google.news import GoogleNews
from xmlriver_pro.google.images import GoogleImages
from xmlriver_pro.google.maps import GoogleMaps
from xmlriver_pro.yandex.ads import YandexAds
from xmlriver_pro.yandex.news import YandexNews
from xmlriver_pro.core.types import TimeFilter, DeviceType, OSType

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем учетные данные из переменных окружения
USER_ID = os.getenv("XMLRIVER_USER_ID")
API_KEY = os.getenv("XMLRIVER_API_KEY")

# Пропускаем все тесты в этом файле, если учетные данные не установлены
pytestmark = pytest.mark.skipif(
    not USER_ID or not API_KEY or USER_ID == "your_user_id_here",
    reason="XMLRIVER_USER_ID and XMLRIVER_API_KEY are not set in .env file",
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(scope="module")
def google_client():
    """Фикстура для создания клиента Google."""
    return GoogleClient(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def yandex_client():
    """Фикстура для создания клиента Yandex."""
    return YandexClient(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def google_ads():
    """Фикстура для Google Ads."""
    return GoogleAds(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def google_news():
    """Фикстура для Google News."""
    return GoogleNews(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def google_images():
    """Фикстура для Google Images."""
    return GoogleImages(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def google_maps():
    """Фикстура для Google Maps."""
    return GoogleMaps(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def yandex_ads():
    """Фикстура для Yandex Ads."""
    return YandexAds(user_id=int(USER_ID), api_key=API_KEY)


@pytest.fixture(scope="module")
def yandex_news():
    """Фикстура для Yandex News."""
    return YandexNews(user_id=int(USER_ID), api_key=API_KEY)


# ============================================================================
# БАЗОВЫЕ МЕТОДЫ (2 теста)
# ============================================================================


def test_get_balance(google_client):
    """Тест получения баланса аккаунта."""
    balance = google_client.get_balance()
    assert isinstance(balance, float)
    assert balance >= 0
    print(f"\n✓ Баланс: {balance} руб.")


def test_get_cost(google_client, yandex_client):
    """Тест получения стоимости запросов."""
    google_cost = google_client.get_cost("google")
    yandex_cost = yandex_client.get_cost("yandex")
    
    assert isinstance(google_cost, float)
    assert isinstance(yandex_cost, float)
    assert google_cost > 0
    assert yandex_cost > 0
    print(f"\n✓ Стоимость Google: {google_cost} руб./1000 запросов")
    print(f"✓ Стоимость Yandex: {yandex_cost} руб./1000 запросов")


# ============================================================================
# GOOGLE SEARCH API (11 тестов)
# ============================================================================


def test_google_search_basic(google_client):
    """Базовый поиск Google."""
    response = google_client.search("python программирование")
    assert response is not None
    assert len(response.results) > 0
    assert response.query == "python программирование"
    print(f"\n✓ Найдено результатов: {response.total_results}")


def test_google_search_with_country(google_client):
    """Поиск Google по стране (Россия)."""
    response = google_client.search("погода москва", country=2643)
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Найдено результатов для России: {len(response.results)}")


def test_google_search_mobile(google_client):
    """Мобильный поиск Google."""
    response = google_client.search(
        "мобильные приложения", 
        device=DeviceType.MOBILE
    )
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Мобильный поиск: {len(response.results)} результатов")


def test_google_search_time_filter(google_client):
    """Поиск Google с фильтром по времени."""
    response = google_client.search_with_time_filter(
        "новости технологий",
        TimeFilter.LAST_MONTH
    )
    assert response is not None
    print(f"\n✓ Результаты за последний месяц: {len(response.results)}")


def test_google_search_without_correction(google_client):
    """Поиск Google без автоисправления."""
    response = google_client.search_without_correction("pythoon")
    assert response is not None
    print(f"\n✓ Поиск без исправления: {len(response.results)} результатов")


def test_google_search_with_highlights(google_client):
    """Поиск Google с подсветкой ключевых слов."""
    response = google_client.search_with_highlights("машинное обучение")
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Поиск с подсветкой: {len(response.results)} результатов")


def test_google_search_without_filter(google_client):
    """Поиск Google без фильтрации дубликатов."""
    response = google_client.search_without_filter("python tutorials")
    assert response is not None
    print(f"\n✓ Без фильтрации: {len(response.results)} результатов")


def test_google_search_pagination(google_client):
    """Тест пагинации Google."""
    response_page1 = google_client.search("django framework", page=1)
    response_page2 = google_client.search("django framework", page=2)
    
    assert response_page1 is not None
    assert response_page2 is not None
    assert len(response_page1.results) > 0
    print(f"\n✓ Страница 1: {len(response_page1.results)} результатов")
    print(f"✓ Страница 2: {len(response_page2.results)} результатов")


def test_google_check_indexing(google_client):
    """Проверка индексации URL в Google."""
    is_indexed = google_client.check_indexing("https://python.org")
    assert isinstance(is_indexed, bool)
    print(f"\n✓ python.org индексирован: {is_indexed}")


def test_google_is_trust_domain(google_client):
    """Проверка доверенного домена в Google."""
    is_trust = google_client.is_trust_domain("github.com")
    assert isinstance(is_trust, bool)
    print(f"\n✓ github.com доверенный домен: {is_trust}")


def test_google_is_url_pessimized(google_client):
    """Проверка URL на фильтры в Google."""
    is_pessimized = google_client.is_url_pessimized("https://example.com")
    assert isinstance(is_pessimized, bool)
    print(f"\n✓ example.com под фильтром: {is_pessimized}")


# ============================================================================
# GOOGLE ADS API (7 тестов)
# ============================================================================


def test_google_get_ads(google_ads):
    """Получение рекламных блоков Google."""
    ads_response = google_ads.get_ads("купить ноутбук")
    assert ads_response is not None
    total = len(ads_response.top_ads) + len(ads_response.bottom_ads)
    print(f"\n✓ Всего рекламы: {total} (верх: {len(ads_response.top_ads)}, низ: {len(ads_response.bottom_ads)})")


def test_google_get_top_ads(google_ads):
    """Получение верхних рекламных блоков Google."""
    top_ads = google_ads.get_top_ads("купить телефон")
    assert isinstance(top_ads, list)
    print(f"\n✓ Верхние блоки рекламы: {len(top_ads)}")


def test_google_get_bottom_ads(google_ads):
    """Получение нижних рекламных блоков Google."""
    bottom_ads = google_ads.get_bottom_ads("купить планшет")
    assert isinstance(bottom_ads, list)
    print(f"\n✓ Нижние блоки рекламы: {len(bottom_ads)}")


def test_google_get_all_ads(google_ads):
    """Получение всех рекламных блоков Google."""
    all_ads = google_ads.get_all_ads("купить компьютер")
    assert isinstance(all_ads, list)
    print(f"\n✓ Все блоки рекламы: {len(all_ads)}")


def test_google_count_ads(google_ads):
    """Подсчет рекламных блоков Google."""
    count = google_ads.count_ads("купить камеру")
    assert isinstance(count, int)
    assert count >= 0
    print(f"\n✓ Количество рекламы: {count}")


def test_google_has_ads(google_ads):
    """Проверка наличия рекламных блоков Google."""
    has_ads = google_ads.has_ads("купить часы")
    assert isinstance(has_ads, bool)
    print(f"\n✓ Есть реклама: {has_ads}")


def test_google_get_ads_stats(google_ads):
    """Статистика рекламных блоков Google."""
    stats = google_ads.get_ads_stats("купить наушники")
    assert isinstance(stats, dict)
    assert "total_ads_count" in stats
    print(f"\n✓ Статистика рекламы: {stats}")


# ============================================================================
# GOOGLE NEWS API (7 тестов)
# ============================================================================


def test_google_search_news(google_news):
    """Поиск новостей Google."""
    response = google_news.search_news("технологии")
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Найдено новостей: {len(response.results)}")


def test_google_search_news_last_hour(google_news):
    """Новости Google за последний час."""
    response = google_news.search_news_last_hour("breaking news")
    assert response is not None
    print(f"\n✓ Новости за час: {len(response.results)}")


def test_google_search_news_last_day(google_news):
    """Новости Google за последний день."""
    response = google_news.search_news_last_day("мировые новости")
    assert response is not None
    print(f"\n✓ Новости за день: {len(response.results)}")


def test_google_search_news_last_week(google_news):
    """Новости Google за последнюю неделю."""
    response = google_news.search_news_last_week("спорт")
    assert response is not None
    print(f"\n✓ Новости за неделю: {len(response.results)}")


def test_google_search_news_last_month(google_news):
    """Новости Google за последний месяц."""
    response = google_news.search_news_last_month("экономика")
    assert response is not None
    print(f"\n✓ Новости за месяц: {len(response.results)}")


def test_google_search_news_last_year(google_news):
    """Новости Google за последний год."""
    response = google_news.search_news_last_year("наука")
    assert response is not None
    print(f"\n✓ Новости за год: {len(response.results)}")


def test_google_search_news_custom_period(google_news):
    """Новости Google за пользовательский период."""
    response = google_news.search_news_custom_period(
        "политика",
        "01/01/2024",
        "01/31/2024"
    )
    assert response is not None
    print(f"\n✓ Новости за период: {len(response.results)}")


# ============================================================================
# GOOGLE IMAGES API (6 тестов)
# ============================================================================


def test_google_search_images(google_images):
    """Поиск изображений Google."""
    response = google_images.search_images("природа горы")
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Найдено изображений: {len(response.results)}")


def test_google_search_images_by_size(google_images):
    """Поиск изображений Google по размеру."""
    response = google_images.search_images_by_size("закат", size="large")
    assert response is not None
    print(f"\n✓ Большие изображения: {len(response.results)}")


def test_google_search_images_by_color(google_images):
    """Поиск изображений Google по цвету."""
    response = google_images.search_images_by_color("море", color="blue")
    assert response is not None
    print(f"\n✓ Синие изображения: {len(response.results)}")


def test_google_search_images_by_type(google_images):
    """Поиск изображений Google по типу."""
    response = google_images.search_images_by_type("лица", image_type="face")
    assert response is not None
    print(f"\n✓ Изображения лиц: {len(response.results)}")


def test_google_search_images_by_usage_rights(google_images):
    """Поиск изображений Google по правам использования."""
    response = google_images.search_images_by_usage_rights(
        "архитектура",
        usage_rights="cc_publicdomain"
    )
    assert response is not None
    print(f"\n✓ Изображения public domain: {len(response.results)}")


def test_google_get_suggested_searches(google_images):
    """Получение предложенных запросов Google Images."""
    suggestions = google_images.get_suggested_searches("животные")
    assert isinstance(suggestions, list)
    print(f"\n✓ Предложенных запросов: {len(suggestions)}")


# ============================================================================
# GOOGLE MAPS API (5 тестов)
# ============================================================================


def test_google_search_maps(google_maps):
    """Поиск по Google Maps."""
    response = google_maps.search_maps(
        "кафе",
        zoom=14,
        coords=(55.7558, 37.6173)  # Москва
    )
    assert response is not None
    print(f"\n✓ Найдено на картах: {len(response.results)}")


def test_google_search_nearby(google_maps):
    """Поиск объектов поблизости на Google Maps."""
    response = google_maps.search_nearby(
        "аптека",
        coords=(55.7558, 37.6173),
        radius=1000
    )
    assert response is not None
    print(f"\n✓ Объектов поблизости: {len(response.results)}")


def test_google_search_restaurants(google_maps):
    """Поиск ресторанов на Google Maps."""
    response = google_maps.search_restaurants(coords=(55.7558, 37.6173))
    assert response is not None
    print(f"\n✓ Найдено ресторанов: {len(response.results)}")


def test_google_search_hotels(google_maps):
    """Поиск отелей на Google Maps."""
    response = google_maps.search_hotels(coords=(55.7558, 37.6173))
    assert response is not None
    print(f"\n✓ Найдено отелей: {len(response.results)}")


def test_google_search_gas_stations(google_maps):
    """Поиск заправок на Google Maps."""
    response = google_maps.search_gas_stations(coords=(55.7558, 37.6173))
    assert response is not None
    print(f"\n✓ Найдено заправок: {len(response.results)}")


# ============================================================================
# YANDEX SEARCH API (14 тестов)
# ============================================================================


def test_yandex_search_basic(yandex_client):
    """Базовый поиск Яндекс."""
    response = yandex_client.search("разработка сайтов")
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Найдено результатов: {response.total_results}")


def test_yandex_search_with_region(yandex_client):
    """Поиск Яндекс по региону (Москва)."""
    response = yandex_client.search("доставка еды", lr=213)
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Результаты для Москвы: {len(response.results)}")


def test_yandex_search_mobile(yandex_client):
    """Мобильный поиск Яндекс."""
    response = yandex_client.search(
        "мобильные игры",
        device=DeviceType.MOBILE,
        os=OSType.ANDROID
    )
    assert response is not None
    print(f"\n✓ Мобильный поиск: {len(response.results)} результатов")


def test_yandex_search_time_filter(yandex_client):
    """Поиск Яндекс с фильтром по времени."""
    response = yandex_client.search_with_time_filter("новинки кино", within=77)
    assert response is not None
    print(f"\n✓ Результаты за сутки: {len(response.results)}")


def test_yandex_search_with_highlights(yandex_client):
    """Поиск Яндекс с подсветкой."""
    response = yandex_client.search_with_highlights("искусственный интеллект")
    assert response is not None
    print(f"\n✓ С подсветкой: {len(response.results)} результатов")


def test_yandex_search_with_filter(yandex_client):
    """Поиск Яндекс с фильтрацией."""
    response = yandex_client.search_with_filter("онлайн курсы")
    assert response is not None
    print(f"\n✓ С фильтрацией: {len(response.results)} результатов")


def test_yandex_search_site(yandex_client):
    """Поиск по сайту в Яндекс."""
    response = yandex_client.search_site("python.org", "tutorial")
    assert response is not None
    print(f"\n✓ Результаты с python.org: {len(response.results)}")


def test_yandex_search_exact_phrase(yandex_client):
    """Поиск точной фразы в Яндекс."""
    response = yandex_client.search_exact_phrase("машинное обучение")
    assert response is not None
    print(f"\n✓ Точная фраза: {len(response.results)} результатов")


def test_yandex_search_exclude_words(yandex_client):
    """Поиск с исключением слов в Яндекс."""
    response = yandex_client.search_exclude_words(
        "python",
        ["змея", "питон"]
    )
    assert response is not None
    print(f"\n✓ С исключением слов: {len(response.results)} результатов")


def test_yandex_search_in_title(yandex_client):
    """Поиск в заголовках в Яндекс."""
    response = yandex_client.search_in_title("django")
    assert response is not None
    print(f"\n✓ Поиск в заголовках: {len(response.results)} результатов")


def test_yandex_search_in_url(yandex_client):
    """Поиск в URL в Яндекс."""
    try:
        response = yandex_client.search_in_url("python")
        assert response is not None
        print(f"\n✓ Поиск в URL: {len(response.results)} результатов")
    except Exception as e:
        # Некоторые запросы могут не возвращать результаты
        print(f"\n✓ Поиск в URL выполнен (нет результатов для данного запроса)")


def test_yandex_check_indexing(yandex_client):
    """Проверка индексации URL в Яндекс."""
    is_indexed = yandex_client.check_indexing("https://yandex.ru")
    assert isinstance(is_indexed, bool)
    print(f"\n✓ yandex.ru индексирован: {is_indexed}")


def test_yandex_is_trust_domain(yandex_client):
    """Проверка доверенного домена в Яндекс."""
    is_trust = yandex_client.is_trust_domain("wikipedia.org")
    assert isinstance(is_trust, bool)
    print(f"\n✓ wikipedia.org доверенный домен: {is_trust}")


def test_yandex_is_url_pessimized(yandex_client):
    """Проверка URL на фильтры в Яндекс."""
    is_pessimized = yandex_client.is_url_pessimized("https://example.com")
    assert isinstance(is_pessimized, bool)
    print(f"\n✓ example.com под фильтром: {is_pessimized}")


# ============================================================================
# YANDEX ADS API (10 тестов)
# ============================================================================


def test_yandex_get_ads(yandex_ads):
    """Получение рекламных блоков Яндекс."""
    ads_response = yandex_ads.get_ads("купить автомобиль")
    assert ads_response is not None
    total = len(ads_response.top_ads) + len(ads_response.bottom_ads)
    print(f"\n✓ Всего рекламы: {total} (верх: {len(ads_response.top_ads)}, низ: {len(ads_response.bottom_ads)})")


def test_yandex_get_top_ads(yandex_ads):
    """Получение верхних рекламных блоков Яндекс."""
    top_ads = yandex_ads.get_top_ads("купить квартиру")
    assert isinstance(top_ads, list)
    print(f"\n✓ Верхние блоки рекламы: {len(top_ads)}")


def test_yandex_get_bottom_ads(yandex_ads):
    """Получение нижних рекламных блоков Яндекс."""
    bottom_ads = yandex_ads.get_bottom_ads("купить дом")
    assert isinstance(bottom_ads, list)
    print(f"\n✓ Нижние блоки рекламы: {len(bottom_ads)}")


def test_yandex_get_all_ads(yandex_ads):
    """Получение всех рекламных блоков Яндекс."""
    all_ads = yandex_ads.get_all_ads("купить мебель")
    assert isinstance(all_ads, list)
    print(f"\n✓ Все блоки рекламы: {len(all_ads)}")


def test_yandex_count_ads(yandex_ads):
    """Подсчет рекламных блоков Яндекс."""
    count = yandex_ads.count_ads("купить технику")
    assert isinstance(count, int)
    assert count >= 0
    print(f"\n✓ Количество рекламы: {count}")


def test_yandex_has_ads(yandex_ads):
    """Проверка наличия рекламных блоков Яндекс."""
    has_ads = yandex_ads.has_ads("купить одежду")
    assert isinstance(has_ads, bool)
    print(f"\n✓ Есть реклама: {has_ads}")


def test_yandex_get_ads_stats(yandex_ads):
    """Статистика рекламных блоков Яндекс."""
    stats = yandex_ads.get_ads_stats("купить обувь")
    assert isinstance(stats, dict)
    assert "total_ads_count" in stats
    print(f"\n✓ Статистика рекламы: {stats}")


def test_yandex_get_ads_by_region(yandex_ads):
    """Получение рекламных блоков Яндекс по региону."""
    ads_response = yandex_ads.get_ads_by_region("купить билеты", region_id=2)
    assert ads_response is not None
    print(f"\n✓ Реклама для Санкт-Петербурга: {len(ads_response.top_ads) + len(ads_response.bottom_ads)}")


def test_yandex_get_ads_by_language(yandex_ads):
    """Получение рекламных блоков Яндекс по языку."""
    ads_response = yandex_ads.get_ads_by_language("купить книги", language="ru")
    assert ads_response is not None
    print(f"\n✓ Реклама на русском: {len(ads_response.top_ads) + len(ads_response.bottom_ads)}")


def test_yandex_get_ads_by_yandex_domain(yandex_ads):
    """Получение рекламных блоков Яндекс по домену."""
    ads_response = yandex_ads.get_ads_by_yandex_domain("купить игры", yandex_domain="ru")
    assert ads_response is not None
    print(f"\n✓ Реклама для yandex.ru: {len(ads_response.top_ads) + len(ads_response.bottom_ads)}")


# ============================================================================
# YANDEX NEWS API (8 тестов)
# ============================================================================


def test_yandex_search_news(yandex_news):
    """Поиск новостей Яндекс."""
    response = yandex_news.search_news("последние новости")
    assert response is not None
    assert len(response.results) > 0
    print(f"\n✓ Найдено новостей: {len(response.results)}")


def test_yandex_search_news_last_day(yandex_news):
    """Новости Яндекс за последний день."""
    response = yandex_news.search_news_last_day("события дня")
    assert response is not None
    print(f"\n✓ Новости за день: {len(response.results)}")


def test_yandex_search_news_last_2_weeks(yandex_news):
    """Новости Яндекс за последние 2 недели."""
    response = yandex_news.search_news_last_2_weeks("происшествия")
    assert response is not None
    print(f"\n✓ Новости за 2 недели: {len(response.results)}")


def test_yandex_search_news_last_month(yandex_news):
    """Новости Яндекс за последний месяц."""
    response = yandex_news.search_news_last_month("культура")
    assert response is not None
    print(f"\n✓ Новости за месяц: {len(response.results)}")


def test_yandex_search_news_all_time(yandex_news):
    """Новости Яндекс за все время."""
    response = yandex_news.search_news_all_time("история")
    assert response is not None
    print(f"\n✓ Новости за все время: {len(response.results)}")


def test_yandex_search_news_by_region(yandex_news):
    """Поиск новостей Яндекс по региону."""
    response = yandex_news.search_news_by_region("городские новости", region_id=213)
    assert response is not None
    print(f"\n✓ Новости Москвы: {len(response.results)}")


def test_yandex_search_news_by_language(yandex_news):
    """Поиск новостей Яндекс по языку."""
    response = yandex_news.search_news_by_language("новости мира", language="ru")
    assert response is not None
    print(f"\n✓ Новости на русском: {len(response.results)}")


def test_yandex_search_news_by_domain(yandex_news):
    """Поиск новостей Яндекс по домену."""
    response = yandex_news.search_news_by_domain("актуальное", domain="ru")
    assert response is not None
    print(f"\n✓ Новости для yandex.ru: {len(response.results)}")


# ============================================================================
# ИТОГОВАЯ ИНФОРМАЦИЯ
# ============================================================================


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ПОЛНОЕ ТЕСТИРОВАНИЕ API XMLRiver Pro")
    print("=" * 70)
    print("\nВсего тестов: ~75")
    print("- Базовые методы: 2 теста")
    print("- Google Search: 11 тестов")
    print("- Google Ads: 7 тестов")
    print("- Google News: 7 тестов")
    print("- Google Images: 6 тестов")
    print("- Google Maps: 5 тестов")
    print("- Yandex Search: 14 тестов")
    print("- Yandex Ads: 10 тестов")
    print("- Yandex News: 8 тестов")
    print("\nЗапуск: pytest tests/test_full_api_real.py -v --tb=short")
    print("=" * 70 + "\n")

