"""
Утилиты для XMLRiver Pro API
"""

from .validators import (
    validate_coords,
    validate_zoom,
    validate_url,
    validate_query,
    validate_device,
    validate_os,
)
from .formatters import (
    format_search_result,
    format_ads_result,
    format_news_result,
    format_image_result,
    format_map_result,
)
from .geo_data_builtin import (
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

__all__ = [
    # Validators
    "validate_coords",
    "validate_zoom",
    "validate_url",
    "validate_query",
    "validate_device",
    "validate_os",
    # Formatters
    "format_search_result",
    "format_ads_result",
    "format_news_result",
    "format_image_result",
    "format_map_result",
    # Geo Data - Yandex регионы
    "get_yandex_region",
    "find_yandex_regions",
    "get_yandex_regions_by_parent",
    "get_yandex_region_hierarchy",
    # Geo Data - Google языки
    "get_google_language",
    "find_google_languages",
    "get_all_google_languages",
    # Geo Data - Google домены
    "get_google_domain",
    "find_google_domains",
    "get_all_google_domains",
    # Geo Data - Города
    "get_city",
    "find_cities",
    "get_cities_by_country",
    # Geo Data - Универсальные
    "search_place",
    "get_region_for_yandex_search",
    "get_country_code_for_google_search",
    # Geo Data - Статистика
    "get_geo_stats",
]
