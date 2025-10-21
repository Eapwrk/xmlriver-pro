"""
XMLRiver Pro - Professional Python client for XMLRiver API

Полнофункциональная асинхронная Python библиотека для работы с API xmlriver.com
с поддержкой всех типов поиска Google, Yandex и Wordstat.

Version: 2.1.0
"""

# Импорт асинхронных клиентов
from .google.async_client import AsyncGoogleClient
from .yandex.async_client import AsyncYandexClient
from .wordstat.async_client import AsyncWordstatClient

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
    WordstatKeyword,
    WordstatResponse,
    WordstatHistoryPoint,
    WordstatHistoryResponse,
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
__version__ = "2.1.0"
__author__ = "XMLRiver Pro Team"
__email__ = "support@xmlriver.com"

"""
Основные возможности:
- Асинхронный API для максимальной производительности
- Органический поиск Google и Yandex
- Поиск по новостям, изображениям, картам
- Рекламные блоки
- Специальные блоки (OneBox, колдунщики)
- Yandex Wordstat - частотность и динамика запросов
- Полная типизация
- Современная архитектура
- Comprehensive тесты

Пример использования:
    import asyncio
    from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient, AsyncWordstatClient

    async def main():
        # Google поиск
        async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
            results = await google.search("python programming")
            for result in results.results:
                print(f"{result.title}: {result.url}")

        # Yandex поиск
        async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex:
            results = await yandex.search("программирование на python")
            for result in results.results:
                print(f"{result.title}: {result.url}")
        
        # Wordstat
        async with AsyncWordstatClient(user_id=123, api_key="your_key") as wordstat:
            result = await wordstat.get_words("python")
            print(f"Associations: {len(result.associations)}")
            frequency = await wordstat.get_frequency("python")
            print(f"Frequency: {frequency}")

    asyncio.run(main())
"""

__all__ = [
    # Версия
    "__version__",
    "__author__",
    "__email__",
    # Асинхронные клиенты
    "AsyncGoogleClient",
    "AsyncYandexClient",
    "AsyncWordstatClient",
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
    "WordstatKeyword",
    "WordstatResponse",
    "WordstatHistoryPoint",
    "WordstatHistoryResponse",
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
