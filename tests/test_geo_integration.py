"""
Интеграционные тесты для географических данных
Подробное тестирование функционала с реальными запросами к API
"""

import os
import time
import pytest
from xmlriver_pro import YandexClient, GoogleClient
from xmlriver_pro.utils.geo_data_builtin import (
    get_geo_stats,
    get_yandex_region,
    find_yandex_regions,
    get_yandex_regions_by_parent,
    get_yandex_region_hierarchy,
    get_google_language,
    find_google_languages,
    get_google_domain,
    find_google_domains,
    get_city,
    find_cities,
    get_cities_by_country,
    search_place,
    get_region_for_yandex_search,
    get_country_code_for_google_search,
    YandexRegion,
    GoogleLanguage,
    GoogleDomain,
    City,
)


class TestGeoDataLoading:
    """Тесты загрузки и доступа к географическим данным"""

    def test_geo_stats_complete(self):
        """Проверка полной загрузки всех типов данных"""
        stats = get_geo_stats()

        # Проверяем что все категории присутствуют
        assert "yandex_regions" in stats
        assert "google_languages" in stats
        assert "google_domains" in stats
        assert "cities" in stats

        # Проверяем что данные загружены
        assert stats["yandex_regions"] > 0
        assert stats["google_languages"] > 0
        assert stats["google_domains"] > 0
        assert stats["cities"] > 0

        # Проверяем точные количества
        assert (
            stats["yandex_regions"] == 869
        ), f"Expected 869 Yandex regions, got {stats['yandex_regions']}"
        assert (
            stats["google_languages"] == 87
        ), f"Expected 87 Google languages, got {stats['google_languages']}"
        assert (
            stats["google_domains"] == 71
        ), f"Expected 71 Google domains, got {stats['google_domains']}"
        assert stats["cities"] == 869, f"Expected 869 cities, got {stats['cities']}"

    def test_yandex_regions_loading(self):
        """Проверка загрузки регионов Yandex"""
        # Проверяем ключевые регионы
        moscow = get_yandex_region(213)
        assert moscow is not None
        assert moscow.name == "Москва"
        assert moscow.id == 213

        spb = get_yandex_region(2)
        assert spb is not None
        assert spb.name == "Санкт-Петербург"
        assert spb.id == 2

        # Проверяем что все регионы загружены
        all_regions = find_yandex_regions("")  # Пустой поиск должен вернуть все
        assert len(all_regions) == 869

    def test_google_languages_loading(self):
        """Проверка загрузки языков Google"""
        # Проверяем ключевые языки
        russian = get_google_language("ru")
        assert russian is not None
        assert russian.code == "ru"
        assert "Russian" in russian.name

        english = get_google_language("en")
        assert english is not None
        assert english.code == "en"
        assert "English" in english.name

        # Проверяем что все языки загружены
        all_languages = find_google_languages("")  # Пустой поиск
        assert len(all_languages) == 87

    def test_google_domains_loading(self):
        """Проверка загрузки доменов Google"""
        # Проверяем ключевые домены
        russia = get_google_domain("ru")
        assert russia is not None
        assert russia.code == "ru"
        assert "Russia" in russia.name

        global_domain = get_google_domain("com")
        assert global_domain is not None
        assert global_domain.code == "com"
        assert "Global" in global_domain.name

        # Проверяем что все домены загружены
        all_domains = find_google_domains("")  # Пустой поиск
        assert len(all_domains) == 71

    def test_cities_loading(self):
        """Проверка загрузки городов"""
        # Проверяем ключевые города
        moscow_cities = find_cities("Москва", exact=True)
        assert len(moscow_cities) >= 1
        assert any(c.name == "Москва" for c in moscow_cities)

        # Проверяем что все города загружены
        all_cities = find_cities("")  # Пустой поиск
        assert len(all_cities) == 869


class TestGeoDataSearch:
    """Тесты поиска географических данных"""

    def test_yandex_regions_search_exact(self):
        """Тест точного поиска регионов Yandex"""
        # Точный поиск Москвы
        moscow_regions = find_yandex_regions("Москва", exact=True)
        assert len(moscow_regions) >= 1
        assert any(r.name == "Москва" for r in moscow_regions)

        # Точный поиск Санкт-Петербурга
        spb_regions = find_yandex_regions("Санкт-Петербург", exact=True)
        assert len(spb_regions) >= 1
        assert any(r.name == "Санкт-Петербург" for r in spb_regions)

    def test_yandex_regions_search_partial(self):
        """Тест частичного поиска регионов Yandex"""
        # Частичный поиск
        moscow_like = find_yandex_regions("Моск")
        assert len(moscow_like) >= 1
        assert any("Моск" in r.name for r in moscow_like)

        # Поиск по части названия
        regions_with_sk = find_yandex_regions("ск")
        assert len(regions_with_sk) > 0

    def test_yandex_regions_hierarchy(self):
        """Тест иерархии регионов"""
        # Получаем иерархию Москвы
        moscow_hierarchy = get_yandex_region_hierarchy(213)
        assert len(moscow_hierarchy) > 0
        assert moscow_hierarchy[-1].name == "Москва"  # Последний элемент - Москва

        # Получаем дочерние регионы для России
        russia_children = get_yandex_regions_by_parent(225)  # Россия
        assert len(russia_children) > 0

    def test_google_languages_search(self):
        """Тест поиска языков Google"""
        # Точный поиск русского
        russian_langs = find_google_languages("Russian", exact=True)
        assert len(russian_langs) >= 1
        assert any(l.name == "Russian" for l in russian_langs)

        # Частичный поиск
        english_langs = find_google_languages("Eng")
        assert len(english_langs) >= 1
        assert any("Eng" in l.name for l in english_langs)

    def test_google_domains_search(self):
        """Тест поиска доменов Google"""
        # Точный поиск российского домена
        russia_domains = find_google_domains("Russia", exact=True)
        assert len(russia_domains) >= 1
        assert any(d.name == "Russia" for d in russia_domains)

        # Частичный поиск
        global_domains = find_google_domains("Global")
        assert len(global_domains) >= 1
        assert any("Global" in d.name for d in global_domains)

    def test_cities_search(self):
        """Тест поиска городов"""
        # Точный поиск Москвы
        moscow_cities = find_cities("Москва", exact=True)
        assert len(moscow_cities) >= 1
        assert any(c.name == "Москва" for c in moscow_cities)

        # Поиск по стране
        russian_cities = get_cities_by_country("RU")
        assert len(russian_cities) > 0
        assert all(c.country_code == "RU" for c in russian_cities)

        # Частичный поиск
        moscow_like_cities = find_cities("Моск")
        assert len(moscow_like_cities) >= 1
        assert any("Моск" in c.name for c in moscow_like_cities)


class TestUniversalFunctions:
    """Тесты универсальных функций"""

    def test_search_place_moscow(self):
        """Тест универсального поиска Москвы"""
        results = search_place("Москва")

        assert "yandex_regions" in results
        assert "cities" in results

        # Проверяем что найдены регионы Yandex
        assert len(results["yandex_regions"]) >= 1
        assert any(r.name == "Москва" for r in results["yandex_regions"])

        # Проверяем что найдены города
        assert len(results["cities"]) >= 1
        assert any(c.name == "Москва" for c in results["cities"])

    def test_search_place_london(self):
        """Тест универсального поиска Лондона"""
        results = search_place("London")

        assert "yandex_regions" in results
        assert "cities" in results

        # Лондон может быть найден в городах
        if results["cities"]:
            assert any("London" in c.name for c in results["cities"])

    def test_get_region_for_yandex_search(self):
        """Тест получения ID региона для Yandex поиска"""
        # Тест с существующими городами
        moscow_id = get_region_for_yandex_search("Москва")
        assert moscow_id is not None
        assert moscow_id == 213

        spb_id = get_region_for_yandex_search("Санкт-Петербург")
        assert spb_id is not None
        assert spb_id == 2

        # Тест с несуществующим местом
        non_existent_id = get_region_for_yandex_search("NonExistentPlace")
        assert non_existent_id is None

    def test_get_country_code_for_google_search(self):
        """Тест получения кода страны для Google поиска"""
        # Тест с существующими городами
        moscow_code = get_country_code_for_google_search("Москва")
        assert moscow_code is not None
        assert moscow_code == 2643  # Россия (Google API код)

        # Тест с несуществующим местом
        non_existent_code = get_country_code_for_google_search("NonExistentPlace")
        assert non_existent_code is None


class TestPerformance:
    """Тесты производительности"""

    def test_search_performance(self):
        """Тест производительности поиска"""
        start_time = time.time()

        # Выполняем множественные поиски
        for _ in range(10):
            find_yandex_regions("Москва")
            find_google_languages("Russian")
            find_cities("Москва")

        end_time = time.time()
        elapsed = end_time - start_time

        # Проверяем что поиск выполняется быстро
        assert elapsed < 1.0, f"Search took too long: {elapsed:.3f}s"

    def test_large_dataset_search(self):
        """Тест поиска в большом наборе данных"""
        start_time = time.time()

        # Поиск во всех типах данных
        all_regions = find_yandex_regions("")
        all_languages = find_google_languages("")
        all_domains = find_google_domains("")
        all_cities = find_cities("")

        end_time = time.time()
        elapsed = end_time - start_time

        # Проверяем что загрузка выполняется быстро
        assert elapsed < 0.5, f"Large dataset search took too long: {elapsed:.3f}s"

        # Проверяем что все данные загружены
        assert len(all_regions) == 869
        assert len(all_languages) == 87
        assert len(all_domains) == 71
        assert len(all_cities) == 869


class TestAPIIntegration:
    """Тесты интеграции с реальными API"""

    @pytest.fixture(scope="class")
    def yandex_credentials(self):
        """Получение credentials для Yandex API"""
        user_id = os.getenv("XMLRIVER_USER_ID")
        api_key = os.getenv("XMLRIVER_API_KEY")

        if not user_id or not api_key:
            pytest.skip("Yandex API credentials not found in environment variables")

        return int(user_id), api_key

    @pytest.fixture(scope="class")
    def google_credentials(self):
        """Получение credentials для Google API"""
        user_id = os.getenv("XMLRIVER_USER_ID")
        api_key = os.getenv("XMLRIVER_API_KEY")

        if not user_id or not api_key:
            pytest.skip("Google API credentials not found in environment variables")

        return int(user_id), api_key

    def test_yandex_search_with_geo_data(self, yandex_credentials):
        """Тест Yandex поиска с использованием географических данных"""
        user_id, api_key = yandex_credentials

        # Получаем ID региона для Москвы
        moscow_region_id = get_region_for_yandex_search("Москва")
        assert moscow_region_id is not None

        # Создаем клиент и выполняем поиск
        client = YandexClient(user_id=user_id, api_key=api_key)

        try:
            # Поиск с региональными параметрами
            results = client.search("python", lr=moscow_region_id)

            # Проверяем что запрос выполнился успешно
            assert results is not None
            assert hasattr(results, "results")

            print(
                f"SUCCESS: Yandex поиск с регионом Москва (lr={moscow_region_id}) выполнен успешно"
            )

        except Exception as e:
            pytest.fail(f"Yandex search failed: {e}")

    def test_yandex_news_with_geo_data(self, yandex_credentials):
        """Тест Yandex новостей с региональными параметрами"""
        user_id, api_key = yandex_credentials

        # Получаем ID региона для Санкт-Петербурга
        spb_region_id = get_region_for_yandex_search("Санкт-Петербург")
        assert spb_region_id is not None

        client = YandexClient(user_id=user_id, api_key=api_key)

        try:
            # Используем правильный класс для новостей
            from xmlriver_pro.yandex.news import YandexNews

            news_client = YandexNews(user_id=user_id, api_key=api_key)
            results = news_client.search_news("новости", lr=spb_region_id)

            # Проверяем что запрос выполнился успешно
            assert results is not None
            assert hasattr(results, "results")

            print(
                f"SUCCESS: Yandex новости с регионом СПб (lr={spb_region_id}) выполнены успешно"
            )

        except Exception as e:
            pytest.fail(f"Yandex news search failed: {e}")

    def test_google_search_with_geo_data(self, google_credentials):
        """Тест Google поиска с использованием географических данных"""
        user_id, api_key = google_credentials

        # Получаем параметры для Google
        russian_lang = get_google_language("ru")
        russian_domain = get_google_domain("ru")

        assert russian_lang is not None
        assert russian_domain is not None

        client = GoogleClient(user_id=user_id, api_key=api_key)

        try:
            # Поиск с региональными параметрами
            results = client.search("python", country=2643)  # Россия (Google API код)

            # Проверяем что запрос выполнился успешно
            assert results is not None
            assert hasattr(results, "results")

            print(
                f"SUCCESS: Google поиск с языком {russian_lang.name} выполнен успешно"
            )

        except Exception as e:
            pytest.fail(f"Google search failed: {e}")

    def test_google_news_with_geo_data(self, google_credentials):
        """Тест Google новостей с географическими параметрами"""
        user_id, api_key = google_credentials

        # Получаем параметры
        english_lang = get_google_language("en")
        assert english_lang is not None

        client = GoogleClient(user_id=user_id, api_key=api_key)

        try:
            # Используем правильный класс для новостей Google
            from xmlriver_pro.google.news import GoogleNews

            news_client = GoogleNews(user_id=user_id, api_key=api_key)
            results = news_client.search_news(
                "news", country=2840
            )  # США (Google API код)

            # Проверяем что запрос выполнился успешно
            assert results is not None
            assert hasattr(results, "results")

            print(
                f"SUCCESS: Google новости с языком {english_lang.name} выполнены успешно"
            )

        except Exception as e:
            pytest.fail(f"Google news search failed: {e}")

    def test_combined_geo_parameters(self, yandex_credentials, google_credentials):
        """Тест комбинированного использования географических параметров"""
        yandex_user_id, yandex_api_key = yandex_credentials
        google_user_id, google_api_key = google_credentials

        # Yandex с регионом
        yandex_client = YandexClient(user_id=yandex_user_id, api_key=yandex_api_key)
        moscow_region_id = get_region_for_yandex_search("Москва")

        # Google с языком и доменом
        google_client = GoogleClient(user_id=google_user_id, api_key=google_api_key)
        russian_lang = get_google_language("ru")

        try:
            # Параллельные запросы с разными географическими параметрами
            yandex_results = yandex_client.search("python", lr=moscow_region_id)
            google_results = google_client.search(
                "python", country=2643
            )  # Россия (Google API код)

            # Проверяем что оба запроса выполнились успешно
            assert yandex_results is not None
            assert google_results is not None

            print(
                "SUCCESS: Комбинированные географические параметры работают корректно"
            )

        except Exception as e:
            pytest.fail(f"Combined geo parameters test failed: {e}")


class TestDataIntegrity:
    """Тесты целостности данных"""

    def test_data_consistency(self):
        """Тест согласованности данных"""
        # Проверяем что все регионы имеют корректные parent_id
        all_regions = find_yandex_regions("")
        for region in all_regions:
            assert isinstance(region.id, int)
            assert isinstance(region.parent_id, int)
            assert isinstance(region.name, str)
            assert len(region.name) > 0

        # Проверяем что все языки имеют корректные коды
        all_languages = find_google_languages("")
        for language in all_languages:
            assert isinstance(language.code, str)
            assert len(language.code) > 0
            assert isinstance(language.name, str)
            assert len(language.name) > 0

        # Проверяем что все домены имеют корректные коды
        all_domains = find_google_domains("")
        for domain in all_domains:
            assert isinstance(domain.code, str)
            assert len(domain.code) > 0
            assert isinstance(domain.name, str)
            assert len(domain.name) > 0

    def test_no_duplicate_ids(self):
        """Тест отсутствия дублирующихся ID"""
        # Проверяем регионы Yandex
        all_regions = find_yandex_regions("")
        region_ids = [r.id for r in all_regions]
        assert len(region_ids) == len(
            set(region_ids)
        ), "Duplicate Yandex region IDs found"

        # Проверяем языки Google
        all_languages = find_google_languages("")
        language_codes = [l.code for l in all_languages]
        assert len(language_codes) == len(
            set(language_codes)
        ), "Duplicate Google language codes found"

        # Проверяем домены Google
        all_domains = find_google_domains("")
        domain_codes = [d.code for d in all_domains]
        assert len(domain_codes) == len(
            set(domain_codes)
        ), "Duplicate Google domain codes found"

    def test_critical_regions_present(self):
        """Тест наличия критически важных регионов"""
        critical_regions = [
            (213, "Москва"),
            (2, "Санкт-Петербург"),
            (225, "Россия"),
        ]

        for region_id, expected_name in critical_regions:
            region = get_yandex_region(region_id)
            assert region is not None, f"Critical region {region_id} not found"
            assert (
                region.name == expected_name
            ), f"Region {region_id} has wrong name: {region.name}"

    def test_critical_languages_present(self):
        """Тест наличия критически важных языков"""
        critical_languages = [
            ("ru", "Russian"),
            ("en", "English"),
        ]

        for lang_code, expected_name in critical_languages:
            language = get_google_language(lang_code)
            assert language is not None, f"Critical language {lang_code} not found"
            assert (
                expected_name in language.name
            ), f"Language {lang_code} has wrong name: {language.name}"

    def test_critical_domains_present(self):
        """Тест наличия критически важных доменов"""
        critical_domains = [
            ("ru", "Russia"),
            ("com", "Global"),
        ]

        for domain_code, expected_name in critical_domains:
            domain = get_google_domain(domain_code)
            assert domain is not None, f"Critical domain {domain_code} not found"
            assert (
                expected_name in domain.name
            ), f"Domain {domain_code} has wrong name: {domain.name}"
