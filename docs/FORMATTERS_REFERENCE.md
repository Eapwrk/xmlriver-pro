# Справочник форматтеров

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md)

Полный справочник всех форматтеров XMLRiver Pro с примерами использования.

## Содержание

- [Основные форматтеры](#основные-форматтеры)
- [Форматтеры результатов](#форматтеры-результатов)
- [Форматтеры специальных блоков](#форматтеры-специальных-блоков)
- [Форматтеры статистики](#форматтеры-статистики)
- [Форматтеры ошибок](#форматтеры-ошибок)
- [Примеры использования](#примеры-использования)

## Основные форматтеры

### format_search_response(response: SearchResponse) -> Dict[str, Any]

Форматирование ответа поиска в удобный для использования формат.

```python
from xmlriver_pro.utils import format_search_response
from xmlriver_pro.core.types import SearchResponse, SearchResult

# Создаем тестовый ответ
response = SearchResponse(
    query="python programming",
    total_results=1000000,
    results=[
        SearchResult(
            rank=1,
            url="https://python.org",
            title="Python Programming Language",
            snippet="Python is a programming language...",
            content_type="organic"
        ),
        SearchResult(
            rank=2,
            url="https://docs.python.org",
            title="Python Documentation",
            snippet="Official Python documentation...",
            content_type="organic"
        )
    ],
    search_time=0.5
)

# Форматируем ответ
formatted = format_search_response(response)

print(formatted)
# {
#     'query': 'python programming',
#     'total_results': 1000000,
#     'results_count': 2,
#     'search_time': 0.5,
#     'results': [
#         {
#             'rank': 1,
#             'url': 'https://python.org',
#             'title': 'Python Programming Language',
#             'snippet': 'Python is a programming language...',
#             'content_type': 'organic'
#         },
#         ...
#     ],
#     'showing_results_for': None,
#     'correct': None,
#     'fixtype': None
# }
```

### format_ads_response(response: AdsResponse) -> Dict[str, Any]

Форматирование ответа с рекламными блоками.

```python
from xmlriver_pro.utils import format_ads_response
from xmlriver_pro.core.types import AdsResponse, AdResult

# Создаем тестовый ответ с рекламой
response = AdsResponse(
    results=[
        AdResult(
            rank=1,
            url="https://ad.example.com",
            title="Python Course",
            snippet="Learn Python programming",
            ad_type="top"
        ),
        AdResult(
            rank=2,
            url="https://ad2.example.com",
            title="Python Tutorial",
            snippet="Free Python tutorial",
            ad_type="bottom"
        )
    ]
)

# Форматируем ответ
formatted = format_ads_response(response)

print(formatted)
# {
#     'results_count': 2,
#     'results': [
#         {
#             'rank': 1,
#             'url': 'https://ad.example.com',
#             'title': 'Python Course',
#             'snippet': 'Learn Python programming',
#             'ad_type': 'top'
#         },
#         ...
#     ]
# }
```

## Форматтеры результатов

### format_search_result(result: SearchResult) -> Dict[str, Any]

Форматирование отдельного результата поиска.

```python
from xmlriver_pro.utils import format_search_result
from xmlriver_pro.core.types import SearchResult

# Создаем тестовый результат
result = SearchResult(
    rank=1,
    url="https://python.org",
    title="Python Programming Language",
    snippet="Python is a programming language...",
    breadcrumbs="Home > Programming > Python",
    content_type="organic",
    pub_date="2024-01-15",
    extended_passage="Extended description...",
    stars=4.8,
    sitelinks=[
        {"title": "Download", "url": "https://python.org/downloads/"},
        {"title": "Documentation", "url": "https://docs.python.org/"}
    ],
    turbo_link="https://turbo.python.org"
)

# Форматируем результат
formatted = format_search_result(result)

print(formatted)
# {
#     'rank': 1,
#     'url': 'https://python.org',
#     'title': 'Python Programming Language',
#     'snippet': 'Python is a programming language...',
#     'breadcrumbs': 'Home > Programming > Python',
#     'content_type': 'organic',
#     'pub_date': '2024-01-15',
#     'extended_passage': 'Extended description...',
#     'stars': 4.8,
#     'sitelinks': [
#         {'title': 'Download', 'url': 'https://python.org/downloads/'},
#         {'title': 'Documentation', 'url': 'https://docs.python.org/'}
#     ],
#     'turbo_link': 'https://turbo.python.org'
# }
```

### format_news_result(result: NewsResult) -> Dict[str, Any]

Форматирование результата поиска новостей.

```python
from xmlriver_pro.utils import format_news_result
from xmlriver_pro.core.types import NewsResult

# Создаем тестовый результат новостей
result = NewsResult(
    rank=1,
    url="https://news.example.com/python-update",
    title="Python 3.12 Released",
    snippet="New features in Python 3.12...",
    pub_date="2024-01-15",
    media="Python Software Foundation",
    breadcrumbs="News > Technology > Programming"
)

# Форматируем результат
formatted = format_news_result(result)

print(formatted)
# {
#     'rank': 1,
#     'url': 'https://news.example.com/python-update',
#     'title': 'Python 3.12 Released',
#     'snippet': 'New features in Python 3.12...',
#     'pub_date': '2024-01-15',
#     'media': 'Python Software Foundation',
#     'breadcrumbs': 'News > Technology > Programming'
# }
```

### format_image_result(result: ImageResult) -> Dict[str, Any]

Форматирование результата поиска изображений.

```python
from xmlriver_pro.utils import format_image_result
from xmlriver_pro.core.types import ImageResult

# Создаем тестовый результат изображения
result = ImageResult(
    rank=1,
    url="https://example.com/python-logo",
    title="Python Logo",
    snippet="Official Python programming language logo",
    img_url="https://example.com/logo.png",
    display_link="python.org",
    original_width=200,
    original_height=200,
    image_size="medium"
)

# Форматируем результат
formatted = format_image_result(result)

print(formatted)
# {
#     'rank': 1,
#     'url': 'https://example.com/python-logo',
#     'title': 'Python Logo',
#     'snippet': 'Official Python programming language logo',
#     'img_url': 'https://example.com/logo.png',
#     'display_link': 'python.org',
#     'original_width': 200,
#     'original_height': 200,
#     'image_size': 'medium'
# }
```

### format_map_result(result: MapResult) -> Dict[str, Any]

Форматирование результата поиска по картам.

```python
from xmlriver_pro.utils import format_map_result
from xmlriver_pro.core.types import MapResult, Coords

# Создаем тестовый результат карты
result = MapResult(
    rank=1,
    url="https://maps.google.com/...",
    title="Python Software Foundation",
    snippet="Python Software Foundation office",
    coords=Coords(latitude=37.7749, longitude=-122.4194),
    address="9450 SW Gemini Dr, Beaverton, OR 97008, USA",
    phone="+1-503-517-1139",
    stars=4.5,
    type="Organization",
    count_reviews=150
)

# Форматируем результат
formatted = format_map_result(result)

print(formatted)
# {
#     'rank': 1,
#     'url': 'https://maps.google.com/...',
#     'title': 'Python Software Foundation',
#     'snippet': 'Python Software Foundation office',
#     'coords': {'latitude': 37.7749, 'longitude': -122.4194},
#     'address': '9450 SW Gemini Dr, Beaverton, OR 97008, USA',
#     'phone': '+1-503-517-1139',
#     'stars': 4.5,
#     'type': 'Organization',
#     'count_reviews': 150
# }
```

### format_ads_result(result: AdResult) -> Dict[str, Any]

Форматирование рекламного результата.

```python
from xmlriver_pro.utils import format_ads_result
from xmlriver_pro.core.types import AdResult

# Создаем тестовый рекламный результат
result = AdResult(
    rank=1,
    url="https://ad.example.com/python-course",
    title="Learn Python Programming",
    snippet="Complete Python course for beginners",
    ads_url="https://ads.example.com/click",
    ad_type="top"
)

# Форматируем результат
formatted = format_ads_result(result)

print(formatted)
# {
#     'rank': 1,
#     'url': 'https://ad.example.com/python-course',
#     'title': 'Learn Python Programming',
#     'snippet': 'Complete Python course for beginners',
#     'ads_url': 'https://ads.example.com/click',
#     'ad_type': 'top'
# }
```

## Форматтеры специальных блоков

### format_onebox_document(doc: OneBoxDocument) -> Dict[str, Any]

Форматирование OneBox документа.

```python
from xmlriver_pro.utils import format_onebox_document
from xmlriver_pro.core.types import OneBoxDocument

# Создаем тестовый OneBox документ
doc = OneBoxDocument(
    title="Python Programming Language",
    url="https://python.org",
    snippet="Python is a high-level programming language...",
    doc_type="organic"
)

# Форматируем документ
formatted = format_onebox_document(doc)

print(formatted)
# {
#     'title': 'Python Programming Language',
#     'url': 'https://python.org',
#     'snippet': 'Python is a high-level programming language...',
#     'doc_type': 'organic'
# }
```

### format_searchster_result(result: SearchsterResult) -> Dict[str, Any]

Форматирование результата колдунщика Yandex.

```python
from xmlriver_pro.utils import format_searchster_result
from xmlriver_pro.core.types import SearchsterResult

# Создаем тестовый результат колдунщика
result = SearchsterResult(
    title="Python Programming",
    url="https://yandex.ru/search/?text=python",
    snippet="Python programming language information",
    searchster_type="calculator"
)

# Форматируем результат
formatted = format_searchster_result(result)

print(formatted)
# {
#     'title': 'Python Programming',
#     'url': 'https://yandex.ru/search/?text=python',
#     'snippet': 'Python programming language information',
#     'searchster_type': 'calculator'
# }
```

### format_related_search(search: RelatedSearch) -> Dict[str, Any]

Форматирование связанного поиска.

```python
from xmlriver_pro.utils import format_related_search
from xmlriver_pro.core.types import RelatedSearch

# Создаем тестовый связанный поиск
search = RelatedSearch(
    query="python tutorial",
    url="https://google.com/search?q=python+tutorial"
)

# Форматируем поиск
formatted = format_related_search(search)

print(formatted)
# {
#     'query': 'python tutorial',
#     'url': 'https://google.com/search?q=python+tutorial'
# }
```

## Форматтеры статистики

### format_search_stats(response: SearchResponse) -> Dict[str, Any]

Форматирование статистики поиска.

```python
from xmlriver_pro.utils import format_search_stats
from xmlriver_pro.core.types import SearchResponse, SearchResult

# Создаем тестовый ответ с разными типами контента
response = SearchResponse(
    query="python programming",
    total_results=1000000,
    results=[
        SearchResult(rank=1, url="https://python.org", title="Python", snippet="...", content_type="organic"),
        SearchResult(rank=2, url="https://docs.python.org", title="Docs", snippet="...", content_type="organic"),
        SearchResult(rank=3, url="https://youtube.com/python", title="Video", snippet="...", content_type="video"),
        SearchResult(rank=4, url="https://images.python.org", title="Image", snippet="...", content_type="image")
    ],
    search_time=0.5
)

# Форматируем статистику
formatted = format_search_stats(response)

print(formatted)
# {
#     'total_results': 1000000,
#     'returned_results': 4,
#     'search_time': 0.5,
#     'content_types': {
#         'organic': 2,
#         'video': 1,
#         'image': 1
#     },
#     'avg_rank': 2.5,
#     'domains': {
#         'python.org': 1,
#         'docs.python.org': 1,
#         'youtube.com': 1,
#         'images.python.org': 1
#     }
# }
```

### format_ads_stats(response: AdsResponse) -> Dict[str, Any]

Форматирование статистики рекламы.

```python
from xmlriver_pro.utils import format_ads_stats
from xmlriver_pro.core.types import AdsResponse, AdResult

# Создаем тестовый ответ с рекламой
response = AdsResponse(
    results=[
        AdResult(rank=1, url="https://ad1.com", title="Ad 1", snippet="...", ad_type="top"),
        AdResult(rank=2, url="https://ad2.com", title="Ad 2", snippet="...", ad_type="top"),
        AdResult(rank=3, url="https://ad3.com", title="Ad 3", snippet="...", ad_type="bottom")
    ]
)

# Форматируем статистику
formatted = format_ads_stats(response)

print(formatted)
# {
#     'total_ads': 3,
#     'top_ads': 2,
#     'bottom_ads': 1,
#     'ad_types': {
#         'top': 2,
#         'bottom': 1
#     },
#     'domains': {
#         'ad1.com': 1,
#         'ad2.com': 1,
#         'ad3.com': 1
#     }
# }
```

### format_results_summary(response: SearchResponse) -> str

Форматирование краткого описания результатов поиска.

```python
from xmlriver_pro.utils import format_results_summary
from xmlriver_pro.core.types import SearchResponse, SearchResult

# Создаем тестовый ответ
response = SearchResponse(
    query="python programming",
    total_results=1000000,
    results=[
        SearchResult(rank=1, url="https://python.org", title="Python", snippet="...", content_type="organic"),
        SearchResult(rank=2, url="https://docs.python.org", title="Docs", snippet="...", content_type="organic")
    ],
    search_time=0.5
)

# Форматируем краткое описание
summary = format_results_summary(response)

print(summary)
# "Найдено 1,000,000 результатов по запросу 'python programming'. Показано 2 результата за 0.5 сек."
```

### format_ads_summary(response: AdsResponse) -> str

Форматирование краткого описания рекламы.

```python
from xmlriver_pro.utils import format_ads_summary
from xmlriver_pro.core.types import AdsResponse, AdResult

# Создаем тестовый ответ с рекламой
response = AdsResponse(
    results=[
        AdResult(rank=1, url="https://ad1.com", title="Ad 1", snippet="...", ad_type="top"),
        AdResult(rank=2, url="https://ad2.com", title="Ad 2", snippet="...", ad_type="bottom")
    ]
)

# Форматируем краткое описание
summary = format_ads_summary(response)

print(summary)
# "Найдено 2 рекламных блока: 1 верхний, 1 нижний"
```

## Форматтеры ошибок

### format_error_message(error: Exception) -> str

Форматирование сообщения об ошибке.

```python
from xmlriver_pro.utils import format_error_message
from xmlriver_pro.core.exceptions import AuthenticationError, RateLimitError

# Тестируем разные типы ошибок
auth_error = AuthenticationError(31, "Invalid API key")
rate_error = RateLimitError(110, "Rate limit exceeded")
generic_error = Exception("Something went wrong")

print(format_error_message(auth_error))
# "[31] Invalid API key"

print(format_error_message(rate_error))
# "[110] Rate limit exceeded"

print(format_error_message(generic_error))
# "Something went wrong"
```

### format_api_response(response_data: Dict[str, Any]) -> str

Форматирование ответа API в читаемый вид.

```python
from xmlriver_pro.utils import format_api_response

# Тестовые данные ответа API
response_data = {
    "response": {
        "found": {"#text": "1000000"},
        "results": {
            "grouping": {
                "group": [
                    {
                        "doc": {
                            "url": "https://python.org",
                            "title": "Python Programming Language",
                            "snippet": "Python is a programming language..."
                        }
                    }
                ]
            }
        }
    }
}

# Форматируем ответ
formatted = format_api_response(response_data)

print(formatted)
# "API Response: 1000000 results found"
```

## Примеры использования

### Комплексное форматирование результатов

```python
from xmlriver_pro.utils import (
    format_search_response, format_search_result, format_search_stats,
    format_results_summary
)
from xmlriver_pro.core.types import SearchResponse, SearchResult

def comprehensive_formatting(response):
    """Комплексное форматирование результатов поиска"""
    
    # Основное форматирование
    formatted_response = format_search_response(response)
    
    # Статистика
    stats = format_search_stats(response)
    
    # Краткое описание
    summary = format_results_summary(response)
    
    # Форматирование каждого результата
    formatted_results = []
    for result in response.results:
        formatted_result = format_search_result(result)
        formatted_results.append(formatted_result)
    
    return {
        "formatted_response": formatted_response,
        "stats": stats,
        "summary": summary,
        "formatted_results": formatted_results
    }

# Использование
response = SearchResponse(
    query="python programming",
    total_results=1000000,
    results=[
        SearchResult(
            rank=1,
            url="https://python.org",
            title="Python Programming Language",
            snippet="Python is a programming language...",
            content_type="organic"
        )
    ],
    search_time=0.5
)

formatted = comprehensive_formatting(response)

print("=== Форматированный ответ ===")
print(formatted["formatted_response"])

print("\n=== Статистика ===")
print(formatted["stats"])

print("\n=== Краткое описание ===")
print(formatted["summary"])

print("\n=== Форматированные результаты ===")
for result in formatted["formatted_results"]:
    print(f"Ранг {result['rank']}: {result['title']}")
```

### Форматирование для экспорта

```python
import json
import csv
from xmlriver_pro.utils import format_search_response, format_ads_response

def export_formatted_results(search_response, ads_response=None, format="json"):
    """Экспорт отформатированных результатов"""
    
    # Форматируем результаты поиска
    formatted_search = format_search_response(search_response)
    
    # Форматируем рекламу (если есть)
    formatted_ads = None
    if ads_response:
        formatted_ads = format_ads_response(ads_response)
    
    if format == "json":
        export_data = {
            "search_results": formatted_search,
            "ads_results": formatted_ads
        }
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    elif format == "csv":
        # Создаем CSV данные
        csv_data = []
        
        # Добавляем результаты поиска
        for result in formatted_search["results"]:
            csv_data.append({
                "type": "search",
                "rank": result["rank"],
                "title": result["title"],
                "url": result["url"],
                "snippet": result["snippet"]
            })
        
        # Добавляем рекламу (если есть)
        if formatted_ads:
            for result in formatted_ads["results"]:
                csv_data.append({
                    "type": "ad",
                    "rank": result["rank"],
                    "title": result["title"],
                    "url": result["url"],
                    "snippet": result["snippet"]
                })
        
        return csv_data

# Использование
search_response = SearchResponse(
    query="python programming",
    total_results=1000000,
    results=[
        SearchResult(
            rank=1,
            url="https://python.org",
            title="Python Programming Language",
            snippet="Python is a programming language...",
            content_type="organic"
        )
    ],
    search_time=0.5
)

# Экспорт в JSON
json_export = export_formatted_results(search_response, format="json")
print("JSON Export:")
print(json_export)

# Экспорт в CSV
csv_export = export_formatted_results(search_response, format="csv")
print("\nCSV Export:")
for row in csv_export:
    print(f"{row['type']}, {row['rank']}, {row['title']}")
```

### Универсальное форматирование

```python
def universal_format(data, data_type="search_response"):
    """Универсальное форматирование данных"""
    
    formatters = {
        "search_response": format_search_response,
        "ads_response": format_ads_response,
        "search_result": format_search_result,
        "news_result": format_news_result,
        "image_result": format_image_result,
        "map_result": format_map_result,
        "ads_result": format_ads_result,
        "onebox_document": format_onebox_document,
        "searchster_result": format_searchster_result,
        "related_search": format_related_search,
        "search_stats": format_search_stats,
        "ads_stats": format_ads_stats,
        "results_summary": format_results_summary,
        "ads_summary": format_ads_summary,
        "error_message": format_error_message,
        "api_response": format_api_response
    }
    
    if data_type not in formatters:
        return {"error": f"Неизвестный тип данных: {data_type}"}
    
    try:
        formatter = formatters[data_type]
        return formatter(data)
    except Exception as e:
        return {"error": f"Ошибка форматирования: {e}"}

# Использование
test_data = SearchResponse(
    query="test",
    total_results=100,
    results=[],
    search_time=0.1
)

formatted = universal_format(test_data, "search_response")
print("Универсальное форматирование:")
print(formatted)
```

---

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md) • [Справочник валидаторов](VALIDATORS_REFERENCE.md)
