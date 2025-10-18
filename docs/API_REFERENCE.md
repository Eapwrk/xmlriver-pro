# API Reference

[← Назад к README](../README.md) • [Документация](README.md)

Полный справочник всех публичных методов, типов данных и исключений XMLRiver Pro.

## Содержание

- [Основные клиенты](#основные-клиенты)
- [Специализированные клиенты](#специализированные-клиенты)
- [Асинхронные клиенты](#асинхронные-клиенты)
- [Типы данных](#типы-данных)
- [Исключения](#исключения)
- [Утилиты](#утилиты)

## Основные клиенты

### GoogleClient

Базовый клиент для работы с Google API.

```python
from xmlriver_pro import GoogleClient

client = GoogleClient(user_id=123, api_key="your_key")
```

#### Методы

- `search(query: str, groupby: int = 10, page: int = 1, device: str = "desktop", **kwargs) -> SearchResponse`
- `get_balance() -> float` - получение баланса аккаунта
- `get_cost() -> float` - получение стоимости Google запросов
- `get_api_limits() -> Dict[str, Any]` - получение лимитов API
- `check_indexing(url: str) -> bool` - проверка индексации URL
- `is_trust_domain(domain: str) -> bool` - проверка доверия к домену

### YandexClient

Базовый клиент для работы с Yandex API.

```python
from xmlriver_pro import YandexClient

client = YandexClient(user_id=123, api_key="your_key")
```

#### Методы

- `search(query: str, groupby: int = 10, page: int = 0, lr: int = None, lang: str = "ru", domain: str = "ru", device: str = "desktop", **kwargs) -> SearchResponse`
- `get_balance() -> float` - получение баланса аккаунта
- `get_cost() -> float` - получение стоимости Yandex запросов
- `get_api_limits() -> Dict[str, Any]` - получение лимитов API
- `check_indexing(url: str) -> bool` - проверка индексации URL
- `is_trust_domain(domain: str) -> bool` - проверка доверия к домену

## Специализированные клиенты

### GoogleSearch

Расширенный поиск Google с дополнительными методами.

```python
from xmlriver_pro import GoogleSearch

search = GoogleSearch(user_id=123, api_key="your_key")
```

#### Методы

- `search_with_time_filter(query: str, time_filter: TimeFilter) -> SearchResponse`
- `search_without_correction(query: str) -> SearchResponse`
- `search_with_highlights(query: str) -> SearchResponse`
- `search_without_filter(query: str) -> SearchResponse`
- `search_site(site: str, query: str) -> SearchResponse`
- `search_exact_phrase(query: str) -> SearchResponse`
- `search_exclude_words(query: str, exclude_words: List[str]) -> SearchResponse`
- `search_file_type(query: str, file_type: str) -> SearchResponse`
- `search_in_title(query: str) -> SearchResponse`
- `search_in_url(query: str) -> SearchResponse`
- `search_related(url: str) -> SearchResponse`
- `search_cache(url: str) -> SearchResponse`
- `search_define(query: str) -> SearchResponse`
- `search_info(url: str) -> SearchResponse`

### YandexSearch

Расширенный поиск Yandex с дополнительными методами.

```python
from xmlriver_pro import YandexSearch

search = YandexSearch(user_id=123, api_key="your_key")
```

#### Методы

- `search_with_time_filter(query: str, within: int) -> SearchResponse`
- `search_with_highlights(query: str) -> SearchResponse`
- `search_with_filter(query: str) -> SearchResponse`
- `search_site(site: str, query: str) -> SearchResponse`
- `search_exact_phrase(query: str) -> SearchResponse`
- `search_exclude_words(query: str, exclude_words: List[str]) -> SearchResponse`
- `search_in_title(query: str) -> SearchResponse`
- `search_in_url(query: str) -> SearchResponse`
- `search_by_region(query: str, region_id: int) -> SearchResponse`
- `search_by_language(query: str, language: str) -> SearchResponse`
- `search_by_domain(query: str, domain: str) -> SearchResponse`
- `search_file_type(query: str, file_type: str) -> SearchResponse`
- `search_define(query: str) -> SearchResponse`
- `search_related(url: str) -> SearchResponse`

### GoogleNews

Поиск новостей Google.

```python
from xmlriver_pro import GoogleNews

news = GoogleNews(user_id=123, api_key="your_key")
```

#### Методы

- `search_news(query: str, time_filter: TimeFilter = None, **kwargs) -> SearchResponse`
- `search_news_last_hour(query: str) -> SearchResponse`
- `search_news_last_day(query: str) -> SearchResponse`
- `search_news_last_week(query: str) -> SearchResponse`
- `search_news_last_month(query: str) -> SearchResponse`
- `search_news_last_year(query: str) -> SearchResponse`
- `search_news_custom_period(query: str, start_date: str, end_date: str) -> SearchResponse`

### YandexNews

Поиск новостей Yandex.

```python
from xmlriver_pro import YandexNews

news = YandexNews(user_id=123, api_key="your_key")
```

#### Методы

- `search_news(query: str, within: int = None, **kwargs) -> SearchResponse`
- `search_news_last_day(query: str) -> SearchResponse`
- `search_news_last_2_weeks(query: str) -> SearchResponse`
- `search_news_last_month(query: str) -> SearchResponse`
- `search_news_all_time(query: str) -> SearchResponse`
- `search_news_by_region(query: str, region_id: int) -> SearchResponse`
- `search_news_by_language(query: str, language: str) -> SearchResponse`
- `search_news_by_domain(query: str, domain: str) -> SearchResponse`
- `get_news_trends(query: str) -> List[str]`

### GoogleImages

Поиск изображений Google.

```python
from xmlriver_pro import GoogleImages

images = GoogleImages(user_id=123, api_key="your_key")
```

#### Методы

- `search_images(query: str, count: int = 20, **kwargs) -> SearchResponse`
- `search_images_by_size(query: str, size: str) -> SearchResponse`
- `search_images_by_color(query: str, color: str) -> SearchResponse`
- `search_images_by_type(query: str, image_type: str) -> SearchResponse`
- `search_images_by_usage_rights(query: str, usage_rights: str) -> SearchResponse`
- `get_suggested_searches(query: str) -> List[str]`

### GoogleMaps

Поиск по картам Google.

```python
from xmlriver_pro import GoogleMaps

maps = GoogleMaps(user_id=123, api_key="your_key")
```

#### Методы

- `search_maps(query: str, zoom: int = 12, coords: Coords = None, count: int = 20, **kwargs) -> SearchResponse`
- `search_nearby(query: str, coords: Coords, radius: int = 1000) -> SearchResponse`
- `search_restaurants(coords: Coords, query: str = "ресторан") -> SearchResponse`
- `search_hotels(coords: Coords) -> SearchResponse`
- `search_gas_stations(coords: Coords) -> SearchResponse`
- `search_pharmacies(coords: Coords) -> SearchResponse`

### GoogleAds

Рекламные блоки Google.

```python
from xmlriver_pro import GoogleAds

ads = GoogleAds(user_id=123, api_key="your_key")
```

#### Методы

- `get_ads(query: str, **kwargs) -> AdsResponse`
- `get_top_ads(query: str, **kwargs) -> List[AdResult]`
- `get_bottom_ads(query: str, **kwargs) -> List[AdResult]`
- `get_all_ads(query: str, **kwargs) -> List[AdResult]`
- `count_ads(query: str, **kwargs) -> int`
- `has_ads(query: str, **kwargs) -> bool`
- `get_ads_by_domain(query: str, domain: str, **kwargs) -> AdsResponse`
- `get_ads_stats(query: str, **kwargs) -> Dict[str, int]`

### YandexAds

Рекламные блоки Yandex.

```python
from xmlriver_pro import YandexAds

ads = YandexAds(user_id=123, api_key="your_key")
```

#### Методы

- `get_ads(query: str, **kwargs) -> AdsResponse`
- `get_ads_by_region(query: str, region_id: int, **kwargs) -> AdsResponse`
- `get_ads_by_language(query: str, language: str, **kwargs) -> AdsResponse`
- `get_ads_by_domain(query: str, domain: str, **kwargs) -> AdsResponse`
- `get_ads_stats(query: str, **kwargs) -> Dict[str, int]`

## Асинхронные клиенты

### AsyncGoogleClient

Асинхронный клиент для работы с Google API.

```python
from xmlriver_pro import AsyncGoogleClient

async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
    results = await client.search("python")
```

#### Методы

- `search(query: str, groupby: int = 10, page: int = 1, device: str = "desktop", **kwargs) -> SearchResponse`
- `search_news(query: str, **kwargs) -> SearchResponse`
- `search_images(query: str, **kwargs) -> SearchResponse`
- `search_maps(query: str, **kwargs) -> SearchResponse`
- `get_ads(query: str, **kwargs) -> AdsResponse`
- `get_balance() -> float`
- `get_cost() -> float`
- `get_api_limits() -> Dict[str, Any]`
- `get_concurrent_status() -> Dict[str, int]` - статус семафора потоков

### AsyncYandexClient

Асинхронный клиент для работы с Yandex API.

```python
from xmlriver_pro import AsyncYandexClient

async with AsyncYandexClient(user_id=123, api_key="your_key") as client:
    results = await client.search("python")
```

#### Методы

- `search(query: str, groupby: int = 10, page: int = 0, lr: int = None, lang: str = "ru", domain: str = "ru", device: str = "desktop", **kwargs) -> SearchResponse`
- `search_news(query: str, **kwargs) -> SearchResponse`
- `get_ads(query: str, **kwargs) -> AdsResponse`
- `get_balance() -> float`
- `get_cost() -> float`
- `get_api_limits() -> Dict[str, Any]`
- `get_concurrent_status() -> Dict[str, int]` - статус семафора потоков

## Типы данных

### Основные типы результатов

#### SearchResult

```python
@dataclass
class SearchResult:
    rank: int
    url: str
    title: str
    snippet: str = ""
    breadcrumbs: Optional[str] = None
    content_type: str = "organic"
    pub_date: Optional[str] = None
    extended_passage: Optional[str] = None
    stars: Optional[float] = None
    sitelinks: Optional[List[Dict[str, str]]] = None
    turbo_link: Optional[str] = None
```

#### NewsResult

```python
@dataclass
class NewsResult:
    rank: int
    url: str
    title: str
    snippet: str
    pub_date: Optional[str] = None
    media: Optional[str] = None
    breadcrumbs: Optional[str] = None
```

#### ImageResult

```python
@dataclass
class ImageResult:
    rank: int
    url: str
    title: str
    snippet: str
    img_url: str
    display_link: str
    original_width: Optional[int] = None
    original_height: Optional[int] = None
    image_size: Optional[str] = None
```

#### MapResult

```python
@dataclass
class MapResult:
    rank: int
    url: str
    title: str
    snippet: str
    coords: Optional[Coords] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    stars: Optional[float] = None
    type: Optional[str] = None
    count_reviews: Optional[int] = None
```

#### AdResult

```python
@dataclass
class AdResult:
    rank: int
    url: str
    title: str
    snippet: str
    ads_url: Optional[str] = None
    ad_type: str = "top"
```

#### SearchResponse

```python
@dataclass
class SearchResponse:
    query: str
    total_results: int
    results: List[SearchResult]
    search_time: float
    showing_results_for: Optional[str] = None
    correct: Optional[str] = None
    fixtype: Optional[str] = None
```

#### AdsResponse

```python
@dataclass
class AdsResponse:
    results: List[AdResult]
```

### Перечисления

#### SearchType

```python
class SearchType(str, Enum):
    ORGANIC = "organic"
    NEWS = "news"
    IMAGES = "images"
    MAPS = "maps"
    ADS = "ads"
```

#### TimeFilter

```python
class TimeFilter(str, Enum):
    LAST_DAY = "qdr:d"
    LAST_WEEK = "qdr:w"
    LAST_MONTH = "qdr:m"
    LAST_YEAR = "qdr:y"
```

#### DeviceType

```python
class DeviceType(str, Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
```

#### OSType

```python
class OSType(str, Enum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    ANDROID = "android"
    IOS = "ios"
```

### Специальные типы

#### OneBoxDocument

```python
@dataclass
class OneBoxDocument:
    title: str
    url: str
    snippet: str
    doc_type: str
```

#### KnowledgeGraph

```python
@dataclass
class KnowledgeGraph:
    entity_name: str
    description: str
    image_url: Optional[str] = None
```

#### RelatedSearch

```python
@dataclass
class RelatedSearch:
    query: str
    url: str
```

#### SearchsterResult

```python
@dataclass
class SearchsterResult:
    title: str
    url: str
    snippet: str
    searchster_type: str
```

#### Coords

```python
@dataclass
class Coords:
    latitude: float
    longitude: float
```

#### SearchParams

```python
@dataclass
class SearchParams:
    query: str
    groupby: int = 10
    page: int = 1
    device: str = "desktop"
```

## Исключения

### XMLRiverError

Базовый класс для всех исключений XMLRiver Pro.

```python
class XMLRiverError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")
```

### AuthenticationError

Ошибка аутентификации (коды: 31, 42, 45).

```python
class AuthenticationError(XMLRiverError):
    """Ошибка аутентификации"""
```

### RateLimitError

Превышен лимит запросов (коды: 110, 111, 115).

```python
class RateLimitError(XMLRiverError):
    """Превышен лимит запросов"""
```

### NoResultsError

Нет результатов поиска (код: 15).

```python
class NoResultsError(XMLRiverError):
    """Нет результатов поиска"""
```

### NetworkError

Ошибка сети (коды: 500, 202).

```python
class NetworkError(XMLRiverError):
    """Ошибка сети"""
```

### ValidationError

Ошибка валидации параметров (коды: 2, 102-108, 120, 121).

```python
class ValidationError(XMLRiverError):
    """Ошибка валидации параметров"""
```

### InsufficientFundsError

Недостаточно средств (код: 200).

```python
class InsufficientFundsError(XMLRiverError):
    """Недостаточно средств"""
```

### ServiceUnavailableError

Сервис недоступен (коды: 101, 201).

```python
class ServiceUnavailableError(XMLRiverError):
    """Сервис недоступен"""
```

### APIError

Общая ошибка API.

```python
class APIError(XMLRiverError):
    """Общая ошибка API"""
```

## Утилиты

### Валидаторы

#### validate_coords(coords: Coords) -> bool

Валидация координат.

```python
from xmlriver_pro.utils import validate_coords

coords = (55.7558, 37.6176)
if validate_coords(coords):
    print("Координаты валидны")
```

#### validate_zoom(zoom: int) -> bool

Валидация zoom (1-15).

```python
from xmlriver_pro.utils import validate_zoom

if validate_zoom(12):
    print("Zoom валиден")
```

#### validate_url(url: str) -> bool

Валидация URL.

```python
from xmlriver_pro.utils import validate_url

if validate_url("https://python.org"):
    print("URL валиден")
```

#### validate_query(query: str) -> bool

Валидация поискового запроса.

```python
from xmlriver_pro.utils import validate_query

if validate_query("python programming"):
    print("Запрос валиден")
```

#### validate_device(device: Union[str, DeviceType]) -> bool

Валидация типа устройства.

```python
from xmlriver_pro.utils import validate_device

if validate_device("desktop"):
    print("Тип устройства валиден")
```

#### validate_os(os: Union[str, OSType]) -> bool

Валидация операционной системы.

```python
from xmlriver_pro.utils import validate_os

if validate_os("windows"):
    print("ОС валидна")
```

#### validate_country(country: int) -> bool

Валидация ID страны.

```python
from xmlriver_pro.utils import validate_country

if validate_country(2840):  # США
    print("ID страны валиден")
```

#### validate_region(region: int) -> bool

Валидация ID региона.

```python
from xmlriver_pro.utils import validate_region

if validate_region(213):  # Москва
    print("ID региона валиден")
```

#### validate_language(language: str) -> bool

Валидация кода языка.

```python
from xmlriver_pro.utils import validate_language

if validate_language("ru"):
    print("Код языка валиден")
```

#### validate_domain(domain: str) -> bool

Валидация домена.

```python
from xmlriver_pro.utils import validate_domain

if validate_domain("ru"):
    print("Домен валиден")
```

#### validate_groupby(groupby: int) -> bool

Валидация groupby (1-10).

```python
from xmlriver_pro.utils import validate_groupby

if validate_groupby(10):
    print("Groupby валиден")
```

#### validate_page(page: int, search_engine: str = "google") -> bool

Валидация номера страницы.

```python
from xmlriver_pro.utils import validate_page

if validate_page(1, "google"):  # Google: 1-based
    print("Номер страницы валиден для Google")

if validate_page(0, "yandex"):  # Yandex: 0-based
    print("Номер страницы валиден для Yandex")
```

#### validate_time_filter(time_filter: str) -> bool

Валидация фильтра времени.

```python
from xmlriver_pro.utils import validate_time_filter

if validate_time_filter("qdr:d"):
    print("Фильтр времени валиден")
```

#### validate_within(within: int) -> bool

Валидация within для Yandex.

```python
from xmlriver_pro.utils import validate_within

if validate_within(77):  # За сутки
    print("Within валиден")
```

#### validate_file_type(file_type: str) -> bool

Валидация типа файла.

```python
from xmlriver_pro.utils import validate_file_type

if validate_file_type("pdf"):
    print("Тип файла валиден")
```

#### validate_image_size(size: str) -> bool

Валидация размера изображения.

```python
from xmlriver_pro.utils import validate_image_size

if validate_image_size("large"):
    print("Размер изображения валиден")
```

#### validate_image_color(color: str) -> bool

Валидация цвета изображения.

```python
from xmlriver_pro.utils import validate_image_color

if validate_image_color("blue"):
    print("Цвет изображения валиден")
```

#### validate_image_type(image_type: str) -> bool

Валидация типа изображения.

```python
from xmlriver_pro.utils import validate_image_type

if validate_image_type("photo"):
    print("Тип изображения валиден")
```

#### validate_usage_rights(usage_rights: str) -> bool

Валидация прав использования изображения.

```python
from xmlriver_pro.utils import validate_usage_rights

if validate_usage_rights("cc_publicdomain"):
    print("Права использования валидны")
```

### Форматтеры

#### format_search_response(response: SearchResponse) -> Dict[str, Any]

Форматирование ответа поиска.

```python
from xmlriver_pro.utils import format_search_response

formatted = format_search_response(search_results)
```

#### format_ads_response(response: AdsResponse) -> Dict[str, Any]

Форматирование ответа рекламы.

```python
from xmlriver_pro.utils import format_ads_response

formatted = format_ads_response(ads_response)
```

#### format_search_result(result: SearchResult) -> Dict[str, Any]

Форматирование результата поиска.

```python
from xmlriver_pro.utils import format_search_result

formatted = format_search_result(result)
```

#### format_news_result(result: NewsResult) -> Dict[str, Any]

Форматирование результата новостей.

```python
from xmlriver_pro.utils import format_news_result

formatted = format_news_result(news_result)
```

#### format_image_result(result: ImageResult) -> Dict[str, Any]

Форматирование результата изображения.

```python
from xmlriver_pro.utils import format_image_result

formatted = format_image_result(image_result)
```

#### format_map_result(result: MapResult) -> Dict[str, Any]

Форматирование результата карты.

```python
from xmlriver_pro.utils import format_map_result

formatted = format_map_result(map_result)
```

#### format_ads_result(result: AdResult) -> Dict[str, Any]

Форматирование рекламного результата.

```python
from xmlriver_pro.utils import format_ads_result

formatted = format_ads_result(ad_result)
```

#### format_onebox_document(doc: OneBoxDocument) -> Dict[str, Any]

Форматирование OneBox документа.

```python
from xmlriver_pro.utils import format_onebox_document

formatted = format_onebox_document(onebox_doc)
```

#### format_searchster_result(result: SearchsterResult) -> Dict[str, Any]

Форматирование колдунщика.

```python
from xmlriver_pro.utils import format_searchster_result

formatted = format_searchster_result(searchster)
```

#### format_related_search(search: RelatedSearch) -> Dict[str, Any]

Форматирование связанного поиска.

```python
from xmlriver_pro.utils import format_related_search

formatted = format_related_search(related_search)
```

#### format_search_stats(response: SearchResponse) -> Dict[str, Any]

Статистика поиска.

```python
from xmlriver_pro.utils import format_search_stats

stats = format_search_stats(search_results)
```

#### format_ads_stats(response: AdsResponse) -> Dict[str, Any]

Статистика рекламы.

```python
from xmlriver_pro.utils import format_ads_stats

stats = format_ads_stats(ads_response)
```

#### format_results_summary(response: SearchResponse) -> str

Краткое описание результатов.

```python
from xmlriver_pro.utils import format_results_summary

summary = format_results_summary(search_results)
```

#### format_ads_summary(response: AdsResponse) -> str

Краткое описание рекламы.

```python
from xmlriver_pro.utils import format_ads_summary

summary = format_ads_summary(ads_response)
```

#### format_error_message(error: Exception) -> str

Форматирование ошибки.

```python
from xmlriver_pro.utils import format_error_message

try:
    results = client.search("")
except Exception as e:
    error_message = format_error_message(e)
    print(error_message)
```

#### format_api_response(response_data: Dict[str, Any]) -> str

Форматирование ответа API.

```python
from xmlriver_pro.utils import format_api_response

formatted = format_api_response(api_response)
```

---

[← Назад к README](../README.md) • [Документация](README.md) • [Продвинутое использование](ADVANCED_USAGE.md)
