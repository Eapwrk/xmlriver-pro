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
]
