"""
XMLRiver Pro - Professional Python client for XMLRiver API

Полнофункциональная Python библиотека для работы с API xmlriver.com
с поддержкой всех типов поиска Google и Yandex.

Version: 1.2.5
"""

# Импорт основных клиентов
from .google import (
    GoogleClient,
    GoogleSearch,
    GoogleNews,
    GoogleImages,
    GoogleMaps,
    GoogleAds,
    GoogleSpecialBlocks,
)
from .yandex import (
    YandexClient,
    YandexSearch,
    YandexNews,
    YandexAds,
    YandexSpecialBlocks,
)

# Импорт асинхронных клиентов
from .google.async_client import AsyncGoogleClient
from .yandex.async_client import AsyncYandexClient

# Импорт типов и исключений
from .core import (
    # Типы
    SearchType,
    TimeFilter,
    DeviceType,
    OSType,
    SearchResult,
    SearchResponse,
    NewsResult,
    ImageResult,
    MapResult,
    AdResult,
    AdsResponse,
    OneBoxDocument,
    KnowledgeGraph,
    RelatedSearch,
    SearchsterResult,
    Coords,
    SearchParams,
    # Исключения
    XMLRiverError,
    AuthenticationError,
    RateLimitError,
    NoResultsError,
    NetworkError,
    ValidationError,
    APIError,
)

# Импорт утилит
from .utils import (
    validate_coords,
    validate_zoom,
    validate_url,
    validate_query,
    validate_device,
    validate_os,
    format_search_result,
    format_ads_result,
    format_news_result,
    format_image_result,
    format_map_result,
)

# Версия и метаданные
__version__ = "1.2.5"
__author__ = "XMLRiver Pro Team"
__email__ = "support@xmlriver.com"

"""
Основные возможности:
- Органический поиск Google и Yandex
- Поиск по новостям, изображениям, картам
- Рекламные блоки
- Специальные блоки (OneBox, колдунщики)
- Полная типизация
- Современная архитектура
- Comprehensive тесты

Пример использования:
    from xmlriver_pro import GoogleClient, YandexClient

    # Google поиск
    google = GoogleClient(user_id=123, api_key="your_key")
    results = google.search("python programming")

    # Yandex поиск
    yandex = YandexClient(user_id=123, api_key="your_key")
    results = yandex.search("программирование на python")
"""

__all__ = [
    # Версия
    "__version__",
    "__author__",
    "__email__",
    # Google клиенты
    "GoogleClient",
    "GoogleSearch",
    "GoogleNews",
    "GoogleImages",
    "GoogleMaps",
    "GoogleAds",
    "GoogleSpecialBlocks",
    # Yandex клиенты
    "YandexClient",
    "YandexSearch",
    "YandexNews",
    "YandexAds",
    "YandexSpecialBlocks",
    # Асинхронные клиенты
    "AsyncGoogleClient",
    "AsyncYandexClient",
    # Типы
    "SearchType",
    "TimeFilter",
    "DeviceType",
    "OSType",
    "SearchResult",
    "SearchResponse",
    "NewsResult",
    "ImageResult",
    "MapResult",
    "AdResult",
    "AdsResponse",
    "OneBoxDocument",
    "KnowledgeGraph",
    "RelatedSearch",
    "SearchsterResult",
    "Coords",
    "SearchParams",
    # Исключения
    "XMLRiverError",
    "AuthenticationError",
    "RateLimitError",
    "NoResultsError",
    "NetworkError",
    "ValidationError",
    "APIError",
    # Утилиты
    "validate_coords",
    "validate_zoom",
    "validate_url",
    "validate_query",
    "validate_device",
    "validate_os",
    "format_search_result",
    "format_ads_result",
    "format_news_result",
    "format_image_result",
    "format_map_result",
]
