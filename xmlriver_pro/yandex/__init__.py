"""
Yandex API модуль для XMLRiver Pro
"""

from .client import YandexClient
from .search import YandexSearch
from .news import YandexNews
from .ads import YandexAds
from .special_blocks import YandexSpecialBlocks

__all__ = [
    "YandexClient",
    "YandexSearch",
    "YandexNews",
    "YandexAds",
    "YandexSpecialBlocks",
]
