"""
Тесты для модуля geo_data (встроенные данные)
"""

import pytest
from xmlriver_pro.utils.geo_data_builtin import (
    YandexRegion,
    GoogleLanguage,
    GoogleDomain,
    City,
    get_yandex_region,
    find_yandex_regions,
    get_google_language,
    find_google_languages,
    get_google_domain,
    find_google_domains,
    get_city,
    find_cities,
    search_place,
    get_region_for_yandex_search,
    get_country_code_for_google_search,
    get_geo_stats,
)


class TestYandexRegions:
    """Тесты для работы с регионами Yandex"""

    def test_get_yandex_region_moscow(self):
        """Тест получения региона Москва"""
        region = get_yandex_region(213)  # Москва
        assert region is not None
        assert region.name == "Москва"
        assert region.id == 213

    def test_get_yandex_region_not_found(self):
        """Тест получения несуществующего региона"""
        region = get_yandex_region(999999)
        assert region is None

    def test_find_yandex_regions_moscow(self):
        """Тест поиска регионов Москва"""
        regions = find_yandex_regions("Москва", exact=True)
        assert len(regions) >= 1
        assert any(r.name == "Москва" for r in regions)

    def test_find_yandex_regions_partial(self):
        """Тест частичного поиска регионов"""
        regions = find_yandex_regions("Моск")
        assert len(regions) >= 1
        assert any("Моск" in r.name for r in regions)

    def test_find_yandex_regions_empty(self):
        """Тест поиска несуществующих регионов"""
        regions = find_yandex_regions("NonExistentRegion")
        assert len(regions) == 0


class TestGoogleLanguages:
    """Тесты для работы с языками Google"""

    def test_get_google_language_russian(self):
        """Тест получения русского языка"""
        language = get_google_language("ru")
        assert language is not None
        assert language.code == "ru"
        assert "Russian" in language.name

    def test_get_google_language_not_found(self):
        """Тест получения несуществующего языка"""
        language = get_google_language("xx")
        assert language is None

    def test_find_google_languages_russian(self):
        """Тест поиска русского языка"""
        languages = find_google_languages("Russian", exact=True)
        assert len(languages) >= 1
        assert any(l.name == "Russian" for l in languages)

    def test_find_google_languages_partial(self):
        """Тест частичного поиска языков"""
        languages = find_google_languages("Russ")
        assert len(languages) >= 1
        assert any("Russ" in l.name for l in languages)


class TestGoogleDomains:
    """Тесты для работы с доменами Google"""

    def test_get_google_domain_russia(self):
        """Тест получения российского домена"""
        domain = get_google_domain("ru")
        assert domain is not None
        assert domain.code == "ru"
        assert "Russia" in domain.name

    def test_get_google_domain_not_found(self):
        """Тест получения несуществующего домена"""
        domain = get_google_domain("xx")
        assert domain is None

    def test_find_google_domains_russia(self):
        """Тест поиска российского домена"""
        domains = find_google_domains("Russia", exact=True)
        assert len(domains) >= 1
        assert any(d.name == "Russia" for d in domains)


class TestCities:
    """Тесты для работы с городами"""

    def test_find_cities_moscow(self):
        """Тест поиска города Москва"""
        cities = find_cities("Москва", exact=True)
        assert len(cities) >= 1
        assert any(c.name == "Москва" for c in cities)

    def test_find_cities_partial(self):
        """Тест частичного поиска городов"""
        cities = find_cities("Моск")
        assert len(cities) >= 1
        assert any("Моск" in c.name for c in cities)

    def test_find_cities_empty(self):
        """Тест поиска несуществующих городов"""
        cities = find_cities("NonExistentCity")
        assert len(cities) == 0

    def test_get_city_by_id(self):
        """Тест получения города по ID"""
        # Найдем любой город
        cities = find_cities("Москва", exact=True)
        if cities:
            city_id = cities[0].id
            city = get_city(city_id)
            assert city is not None
            assert city.id == city_id


class TestSearchFunctions:
    """Тесты для функций поиска"""

    def test_search_place_moscow(self):
        """Тест универсального поиска Москвы"""
        results = search_place("Москва")
        assert "yandex_regions" in results
        assert "cities" in results
        assert len(results["yandex_regions"]) >= 1
        assert len(results["cities"]) >= 1

    def test_get_region_for_yandex_search_moscow(self):
        """Тест получения ID региона для поиска Москвы"""
        region_id = get_region_for_yandex_search("Москва")
        assert region_id is not None
        assert region_id == 213  # ID Москвы

    def test_get_region_for_yandex_search_not_found(self):
        """Тест получения ID региона для несуществующего места"""
        region_id = get_region_for_yandex_search("NonExistentPlace")
        assert region_id is None

    def test_get_country_code_for_google_search_moscow(self):
        """Тест получения кода страны для поиска Москвы"""
        country_code = get_country_code_for_google_search("Москва")
        assert country_code is not None
        assert country_code == 2643  # Россия (Google API код)

    def test_get_country_code_for_google_search_not_found(self):
        """Тест получения кода страны для несуществующего места"""
        country_code = get_country_code_for_google_search("NonExistentPlace")
        assert country_code is None


class TestStats:
    """Тесты для статистики"""

    def test_get_geo_stats(self):
        """Тест получения статистики"""
        stats = get_geo_stats()
        assert "yandex_regions" in stats
        assert "google_languages" in stats
        assert "google_domains" in stats
        assert "cities" in stats

        # Проверяем, что данные загружены
        assert stats["yandex_regions"] > 0
        assert stats["google_languages"] > 0
        assert stats["google_domains"] > 0
        assert stats["cities"] > 0


class TestDataClasses:
    """Тесты для классов данных"""

    def test_yandex_region_creation(self):
        """Тест создания региона Yandex"""
        region = YandexRegion(213, "Москва", 1, "RU")
        assert region.id == 213
        assert region.name == "Москва"
        assert region.parent_id == 1
        assert region.country_code == "RU"

    def test_google_language_creation(self):
        """Тест создания языка Google"""
        language = GoogleLanguage("ru", "Russian")
        assert language.code == "ru"
        assert language.name == "Russian"

    def test_google_domain_creation(self):
        """Тест создания домена Google"""
        domain = GoogleDomain("ru", "Russia", "Russia")
        assert domain.code == "ru"
        assert domain.name == "Russia"
        assert domain.country == "Russia"

    def test_city_creation(self):
        """Тест создания города"""
        city = City(2000001, "Москва", "Москва,RU", 1, "RU", "City", "Active")
        assert city.id == 2000001
        assert city.name == "Москва"
        assert city.canonical_name == "Москва,RU"
        assert city.parent_id == 1
        assert city.country_code == "RU"
        assert city.target_type == "City"
        assert city.status == "Active"
