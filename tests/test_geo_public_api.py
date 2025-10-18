"""
Тесты для проверки экспорта geo_data функций в публичный API.

Критически важно: все geo_data функции должны быть доступны через:
from xmlriver_pro.utils import <function_name>
"""

import pytest


class TestGeoDataPublicAPI:
    """Проверка экспорта всех geo_data функций в публичный API."""

    def test_yandex_regions_exported(self):
        """Проверка экспорта функций для работы с Yandex регионами."""
        from xmlriver_pro.utils import (
            get_yandex_region,
            find_yandex_regions,
            get_yandex_regions_by_parent,
            get_yandex_region_hierarchy,
        )

        # Проверяем что функции работают
        region = get_yandex_region(213)
        assert region is not None
        assert region.name == "Москва"

        regions = find_yandex_regions("Санкт")
        assert len(regions) > 0

    def test_google_languages_exported(self):
        """Проверка экспорта функций для работы с Google языками."""
        from xmlriver_pro.utils import (
            get_google_language,
            find_google_languages,
            get_all_google_languages,
        )

        # Проверяем что функции работают
        lang = get_google_language("ru")
        assert lang is not None
        assert lang.name == "Russian"

        langs = find_google_languages("Russian")
        assert len(langs) > 0

        all_langs = get_all_google_languages()
        assert len(all_langs) > 0

    def test_google_domains_exported(self):
        """Проверка экспорта функций для работы с Google доменами."""
        from xmlriver_pro.utils import (
            get_google_domain,
            find_google_domains,
            get_all_google_domains,
        )

        # Проверяем что функции работают
        domain = get_google_domain("com")
        assert domain is not None

        domains = find_google_domains("Russia")
        assert len(domains) > 0

        all_domains = get_all_google_domains()
        assert len(all_domains) > 0

    def test_cities_exported(self):
        """Проверка экспорта функций для работы с городами."""
        from xmlriver_pro.utils import (
            get_city,
            find_cities,
            get_cities_by_country,
        )

        # Проверяем что функции работают
        cities = find_cities("Москва")
        assert len(cities) > 0

        ru_cities = get_cities_by_country("RU")
        assert len(ru_cities) > 0

    def test_universal_functions_exported(self):
        """Проверка экспорта универсальных функций."""
        from xmlriver_pro.utils import (
            search_place,
            get_region_for_yandex_search,
            get_country_code_for_google_search,
        )

        # Проверяем что функции работают
        places = search_place("Москва")
        assert len(places) > 0

        region_id = get_region_for_yandex_search("Москва")
        assert region_id == 213

        # get_country_code_for_google_search возвращает ID региона
        region = get_country_code_for_google_search("Москва")
        assert region is not None
        assert isinstance(region, int)

    def test_stats_function_exported(self):
        """Проверка экспорта функции статистики."""
        from xmlriver_pro.utils import get_geo_stats

        # Проверяем что функция работает
        stats = get_geo_stats()
        assert "yandex_regions" in stats
        assert "google_languages" in stats
        assert "google_domains" in stats
        assert "cities" in stats

    def test_all_functions_in_all_list(self):
        """Проверка что все geo_data функции в __all__."""
        from xmlriver_pro import utils

        expected_functions = [
            # Yandex регионы
            "get_yandex_region",
            "find_yandex_regions",
            "get_yandex_regions_by_parent",
            "get_yandex_region_hierarchy",
            # Google языки
            "get_google_language",
            "find_google_languages",
            "get_all_google_languages",
            # Google домены
            "get_google_domain",
            "find_google_domains",
            "get_all_google_domains",
            # Города
            "get_city",
            "find_cities",
            "get_cities_by_country",
            # Универсальные
            "search_place",
            "get_region_for_yandex_search",
            "get_country_code_for_google_search",
            # Статистика
            "get_geo_stats",
        ]

        for func_name in expected_functions:
            assert func_name in utils.__all__, f"Функция {func_name} не в __all__"
            assert hasattr(utils, func_name), f"Функция {func_name} не экспортирована"

    def test_import_all_functions_at_once(self):
        """Проверка импорта всех функций одним импортом."""
        from xmlriver_pro.utils import (
            # Yandex регионы
            get_yandex_region,
            find_yandex_regions,
            get_yandex_regions_by_parent,
            get_yandex_region_hierarchy,
            # Google языки
            get_google_language,
            find_google_languages,
            get_all_google_languages,
            # Google домены
            get_google_domain,
            find_google_domains,
            get_all_google_domains,
            # Города
            get_city,
            find_cities,
            get_cities_by_country,
            # Универсальные
            search_place,
            get_region_for_yandex_search,
            get_country_code_for_google_search,
            # Статистика
            get_geo_stats,
        )

        # Проверяем что все функции callable
        all_functions = [
            get_yandex_region,
            find_yandex_regions,
            get_yandex_regions_by_parent,
            get_yandex_region_hierarchy,
            get_google_language,
            find_google_languages,
            get_all_google_languages,
            get_google_domain,
            find_google_domains,
            get_all_google_domains,
            get_city,
            find_cities,
            get_cities_by_country,
            search_place,
            get_region_for_yandex_search,
            get_country_code_for_google_search,
            get_geo_stats,
        ]

        for func in all_functions:
            assert callable(func), f"Функция {func.__name__} не callable"

