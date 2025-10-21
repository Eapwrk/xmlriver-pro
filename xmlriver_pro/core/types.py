"""
Типы данных для XMLRiver Pro API
"""

from typing import Optional, List, Dict, Any, Union, Sequence
from dataclasses import dataclass
from enum import Enum


class SearchType(str, Enum):
    """Типы поиска"""

    ORGANIC = "organic"
    NEWS = "news"
    IMAGES = "images"
    MAPS = "maps"
    ADS = "ads"


class TimeFilter(str, Enum):
    """Фильтры по времени для Google"""

    LAST_HOUR = "qdr:h"
    LAST_DAY = "qdr:d"
    LAST_WEEK = "qdr:w"
    LAST_MONTH = "qdr:m"
    LAST_YEAR = "qdr:y"


class DeviceType(str, Enum):
    """Типы устройств"""

    DESKTOP = "desktop"
    TABLET = "tablet"
    MOBILE = "mobile"


class OSType(str, Enum):
    """Типы операционных систем для мобильных устройств"""

    IOS = "ios"
    ANDROID = "android"


@dataclass
class SearchResult:
    """Результат поиска"""

    rank: int
    url: str
    title: str
    snippet: str
    breadcrumbs: Optional[str] = None
    content_type: str = "organic"
    pub_date: Optional[str] = None
    extended_passage: Optional[str] = None
    stars: Optional[float] = None
    sitelinks: Optional[List[Dict[str, str]]] = None
    turbo_link: Optional[str] = None


@dataclass
class NewsResult:
    """Результат поиска новостей"""

    rank: int
    url: str
    title: str
    snippet: str
    media: Optional[str] = None
    pub_date: Optional[str] = None


@dataclass
class ImageResult:
    """Результат поиска изображений"""

    rank: int
    url: str
    img_url: str
    title: str
    display_link: str
    original_width: Optional[int] = None
    original_height: Optional[int] = None


@dataclass
class MapResult:
    """Результат поиска по картам"""

    title: str
    stars: Optional[float] = None
    type: Optional[str] = None
    address: Optional[str] = None
    url: Optional[str] = None
    phone: Optional[str] = None
    review: Optional[str] = None
    possibility: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_id: Optional[str] = None
    count_reviews: Optional[int] = None
    accessibility: Optional[bool] = None
    price: Optional[str] = None
    gas_price: Optional[str] = None


@dataclass
class AdResult:
    """Результат рекламного блока"""

    url: str
    ads_url: str
    title: str
    snippet: str


@dataclass
class AdsResponse:
    """Ответ с рекламными блоками"""

    top_ads: List[AdResult]
    bottom_ads: List[AdResult]


@dataclass
class OneBoxDocument:
    """OneBox документ"""

    content_type: str
    title: str
    url: str
    snippet: str
    additional_data: Optional[Dict[str, Any]] = None


@dataclass
class KnowledgeGraph:
    """Knowledge Graph данные"""

    entity_name: str
    description: str
    image_url: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None


@dataclass
class RelatedSearch:
    """Связанный поисковый запрос"""

    query: str
    url: Optional[str] = None


@dataclass
class SearchsterResult:
    """Результат колдунщика Яндекса"""

    content_type: str
    title: str
    url: str
    snippet: str
    additional_data: Optional[Dict[str, Any]] = None


# Типы для валидации
Coords = tuple[float, float]
SearchParams = Dict[str, Any]


@dataclass
class SearchResponse:
    """Ответ на поисковый запрос"""

    query: str
    total_results: int
    results: Sequence[Union[SearchResult, NewsResult, ImageResult, MapResult, AdResult]]
    showing_results_for: Optional[str] = None
    correct: Optional[str] = None
    fixtype: Optional[str] = None


@dataclass
class WordstatKeyword:
    """Ключевое слово из Wordstat"""

    text: str
    value: int
    is_association: bool = True


@dataclass
class WordstatResponse:
    """Ответ Wordstat API с топами запросов"""

    query: str
    associations: List[WordstatKeyword]
    popular: List[WordstatKeyword]


@dataclass
class WordstatHistoryPoint:
    """Точка в динамике Wordstat"""

    date: str
    absolute_value: int
    relative_value: Optional[float] = None


@dataclass
class WordstatHistoryResponse:
    """Ответ Wordstat API с динамикой запроса"""

    query: str
    total_value: int
    history: List[WordstatHistoryPoint]
    associations: List[WordstatKeyword]
    popular: List[WordstatKeyword]
