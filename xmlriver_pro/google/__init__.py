"""
Google API модуль для XMLRiver Pro
"""

from .client import GoogleClient
from .search import GoogleSearch
from .news import GoogleNews
from .images import GoogleImages
from .maps import GoogleMaps
from .ads import GoogleAds
from .special_blocks import GoogleSpecialBlocks

__all__ = [
    "GoogleClient",
    "GoogleSearch",
    "GoogleNews",
    "GoogleImages",
    "GoogleMaps",
    "GoogleAds",
    "GoogleSpecialBlocks",
]
