# XMLRiver Pro

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/Eapwrk/xmlriver-pro?style=social)](https://github.com/Eapwrk/xmlriver-pro)
[![Star this repo](https://img.shields.io/badge/⭐-Star%20this%20repo-yellow?style=social)](https://github.com/Eapwrk/xmlriver-pro)
[![Fork this repo](https://img.shields.io/badge/🍴-Fork%20this%20repo-blue?style=social)](https://github.com/Eapwrk/xmlriver-pro/fork)
[![Watch this repo](https://img.shields.io/badge/👁-Watch%20this%20repo-green?style=social)](https://github.com/Eapwrk/xmlriver-pro/subscription)
[![Sponsor this repo](https://img.shields.io/badge/💖-Sponsor%20this%20repo-pink?style=social)](https://github.com/sponsors/Eapwrk)
[![Report Issues](https://img.shields.io/badge/🐛-Report%20Issues-red?style=social)](https://github.com/Eapwrk/xmlriver-pro/issues)
[![Join Discussions](https://img.shields.io/badge/💬-Join%20Discussions-purple?style=social)](https://github.com/Eapwrk/xmlriver-pro/discussions)
[![Pull Requests](https://img.shields.io/badge/🔀-Pull%20Requests-orange?style=social)](https://github.com/Eapwrk/xmlriver-pro/pulls)
[![Wiki](https://img.shields.io/badge/📚-Wiki-teal?style=social)](https://github.com/Eapwrk/xmlriver-pro/wiki)
[![Actions](https://img.shields.io/badge/⚙️-Actions-gray?style=social)](https://github.com/Eapwrk/xmlriver-pro/actions)
[![Releases](https://img.shields.io/badge/🚀-Releases-cyan?style=social)](https://github.com/Eapwrk/xmlriver-pro/releases)
[![Security](https://img.shields.io/badge/🔒-Security-indigo?style=social)](https://github.com/Eapwrk/xmlriver-pro/security)
[![Insights](https://img.shields.io/badge/📊-Insights-lime?style=social)](https://github.com/Eapwrk/xmlriver-pro/pulse)
[![Settings](https://img.shields.io/badge/⚙️-Settings-slate?style=social)](https://github.com/Eapwrk/xmlriver-pro/settings)
[![Code](https://img.shields.io/badge/💻-Code-emerald?style=social)](https://github.com/Eapwrk/xmlriver-pro)
[![Issues](https://img.shields.io/badge/🐛-Issues-red?style=social)](https://github.com/Eapwrk/xmlriver-pro/issues)
[![Pull Requests](https://img.shields.io/badge/🔀-Pull%20Requests-orange?style=social)](https://github.com/Eapwrk/xmlriver-pro/pulls)
[![Discussions](https://img.shields.io/badge/💬-Discussions-purple?style=social)](https://github.com/Eapwrk/xmlriver-pro/discussions)
[![Wiki](https://img.shields.io/badge/📚-Wiki-teal?style=social)](https://github.com/Eapwrk/xmlriver-pro/wiki)
[![Actions](https://img.shields.io/badge/⚙️-Actions-gray?style=social)](https://github.com/Eapwrk/xmlriver-pro/actions)
[![PyPI version](https://img.shields.io/pypi/v/xmlriver-pro?color=blue)](https://pypi.org/project/xmlriver-pro/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/xmlriver-pro?color=orange)](https://pypi.org/project/xmlriver-pro/)
[![Coverage](https://img.shields.io/badge/coverage-57%25-brightgreen.svg)](https://github.com/Eapwrk/xmlriver-pro)
[![GitHub last commit](https://img.shields.io/github/last-commit/Eapwrk/xmlriver-pro?color=blue)](https://github.com/Eapwrk/xmlriver-pro)
[![GitHub issues](https://img.shields.io/github/issues/Eapwrk/xmlriver-pro?color=red)](https://github.com/Eapwrk/xmlriver-pro/issues)

```
__  ____  __ _     ____  _                  ____            
\ \/ /  \/  | |   |  _ \(_)_   _____ _ __  |  _ \ _ __ ___  
 \  /| |\/| | |   | |_) | \ \ / / _ \ '__| | |_) | '__/ _ \ 
 /  \| |  | | |___|  _ <| |\ V /  __/ |    |  __/| | | (_) |
/_/\_\_|  |_|_____|_| \_\_| \_/ \___|_|    |_|   |_|  \___/ 
```

**Professional Python client for XMLRiver API with full coverage**

*Fork of [KursHub-ru/xmlriver](https://github.com/KursHub-ru/xmlriver)*

[🚀 Quick Start](#-быстрый-старт) • [📚 Documentation](#-документация) • [🔧 Configuration](#-конфигурация) • [💡 Examples](#-примеры-использования)

</div>

---

## 🎯 О проекте

XMLRiver Pro — это **профессиональная** Python библиотека для работы с API xmlriver.com. Расширенная версия с поддержкой **всех типов поиска** в Google и Yandex.

### 📊 Сравнение с оригинальной библиотекой

| Функция | Оригинал | **XMLRiver Pro** |
|---------|----------|------------------|
| 🔍 Органический поиск | ✅ | ✅ **Улучшенный** |
| 📰 Новости | ✅ | ✅ **С фильтрами времени** |
| 🖼️ Изображения | ✅ | ✅ **Расширенные параметры** |
| 🗺️ Карты | ✅ | ✅ **С координатами** |
| 📢 Реклама | ✅ | ✅ **Верхние и нижние блоки** |
| 🧩 Специальные блоки | ❌ | ✅ **OneBox, Knowledge Graph** |
| ⚡ Асинхронность | ❌ | ✅ **Полная поддержка** |
| 🔄 Retry механизм | ❌ | ✅ **Экспоненциальный backoff** |
| 🛡️ Ограничение потоков | ❌ | ✅ **Максимум 10 одновременных** |
| 📊 Типизация | ❌ | ✅ **100% типизирован** |
| 🧪 Тесты | ❌ | ✅ **66 тестов, 57% покрытие** |

**Поддерживает все типы поиска:**
- 🔍 Органический поиск
- 📰 Новости с фильтрами времени  
- 🖼️ Изображения (размер, цвет, тип)
- 🗺️ Карты с координатами
- 📢 Рекламные блоки
- 🧩 Специальные блоки (OneBox, Knowledge Graph)
- ⚡ **Асинхронная поддержка** с ограничением потоков

## ✨ Ключевые особенности

- ⚡ **Асинхронная поддержка** с ограничением потоков (максимум 10)
- 🔄 **Retry механизм** с экспоненциальным backoff
- 🛡️ **Валидация параметров** и обработка ошибок
- 📊 **Форматирование результатов** поиска
- 🎯 **100% покрытие API** - все методы XMLRiver
- 🚀 **Высокая производительность** - оптимизированные запросы
- ✅ **Полная типизация** для Python 3.10+
- 🏛️ **Модульная архитектура** с четким разделением
- 🧪 **66 тестов** с покрытием 57%

## 📦 Установка

### 📦 **Из PyPI (рекомендуется):**
```bash
# Установка последней версии
pip install xmlriver-pro

# Установка конкретной версии
pip install xmlriver-pro==1.1.1

# Обновление до последней версии
pip install --upgrade xmlriver-pro
```

### 🚀 **Из GitHub:**
```bash
# Установка последней версии
pip install git+https://github.com/Eapwrk/xmlriver-pro.git

# Установка конкретной версии
pip install git+https://github.com/Eapwrk/xmlriver-pro.git@v1.1.1

# Обновление до последней версии
pip install --upgrade git+https://github.com/Eapwrk/xmlriver-pro.git
```

### 🔍 **Проверка версии:**
```bash
python -c "import xmlriver_pro; print(xmlriver_pro.__version__)"
```

## 🔄 Обновления

### 📋 **Как узнать об обновлениях:**
- ⭐ **Watch репозиторий** на GitHub для уведомлений
- 📧 **Email:** seo@controlseo.ru
- 🐛 **Issues:** [GitHub Issues](https://github.com/Eapwrk/xmlriver-pro/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/Eapwrk/xmlriver-pro/discussions)

### 📚 **История изменений:**
- 📄 **CHANGELOG.md** - полная история изменений
- 🏷️ **GitHub Releases** - релизы с описанием
- 🔄 **Semantic Versioning** - мажорные.минорные.патч версии

### 🚀 **Как обновляться:**
```bash
# Проверить текущую версию
pip show xmlriver-pro

# Обновить до последней версии
pip install --upgrade xmlriver-pro

# Обновить до конкретной версии
pip install xmlriver-pro==1.1.0
```

Для разработки:
```bash
git clone https://github.com/Eapwrk/xmlriver-pro.git
cd xmlriver-pro
pip install -e .
```

## 🔧 Зависимости

### Основные:
- **requests** - HTTP запросы к API
- **xmltodict** - парсинг XML ответов
- **aiohttp** - асинхронные HTTP запросы

### Для разработки:
- **pytest** - тестирование
- **black** - форматирование кода
- **pylint** - анализ кода
- **mypy** - проверка типов

## ⚙️ Конфигурация

### Переменные окружения

Для удобства тестирования и разработки можно использовать переменные окружения:

```bash
# Создайте файл .env в корне проекта
XMLRIVER_USER_ID=6881
XMLRIVER_API_KEY=your_api_key_here
```

```python
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Используем в коде
user_id = int(os.getenv("XMLRIVER_USER_ID", "0"))
api_key = os.getenv("XMLRIVER_API_KEY", "")

client = GoogleClient(user_id, api_key)
```

Все клиенты поддерживают настройку retry механизма и таймаутов:

### Параметры конфигурации:

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `timeout` | `int` | `60` | Таймаут запроса в секундах (максимум 60) |
| `max_retries` | `int` | `3` | Максимальное количество попыток повтора |
| `retry_delay` | `float` | `1.0` | Базовая задержка между попытками в секундах |
| `enable_retry` | `bool` | `True` | Включить автоматические повторы |
| `max_concurrent` | `int` | `10` | Максимум одновременных запросов (жесткое ограничение) |

### Экспоненциальный backoff:

При включенном retry используется экспоненциальная задержка:
- 1-я попытка: `retry_delay * 1` = 1.0 сек
- 2-я попытка: `retry_delay * 2` = 2.0 сек  
- 3-я попытка: `retry_delay * 4` = 4.0 сек
- 4-я попытка: `retry_delay * 8` = 8.0 сек

### Примеры конфигурации:

```python
# Стандартная конфигурация (рекомендуется)
client = GoogleClient(user_id=123, api_key="key")

# Кастомные настройки retry
client = GoogleClient(
    user_id=123, 
    api_key="key",
    timeout=120,        # 2 минуты
    max_retries=5,      # 5 попыток
    retry_delay=2.0,    # базовая задержка 2 сек
    max_concurrent=5    # максимум 5 одновременных запросов
)

# Отключить retry для продвинутых пользователей
client = GoogleClient(
    user_id=123, 
    api_key="key",
    enable_retry=False  # без повторов
)

# Асинхронный клиент с настройками
async with AsyncGoogleClient(
    user_id=123,
    api_key="key", 
    max_retries=3,
    retry_delay=1.5,
    max_concurrent=8
) as client:
    result = await client.search("python")
    
    # Проверка состояния семафора
    status = client.get_concurrent_status()
    print(f"Active requests: {status['active_requests']}/{status['max_concurrent']}")
```

## 🚀 Быстрый старт

```python
from xmlriver_pro import GoogleClient, YandexClient

# Инициализация клиентов
google = GoogleClient(user_id=123, api_key="your_google_key")
yandex = YandexClient(user_id=123, api_key="your_yandex_key")

# Органический поиск
google_results = google.search("python programming")
yandex_results = yandex.search("программирование на python")

# Результаты поиска
google_count = google_results.total_results
yandex_count = yandex_results.total_results
```

## ⚡ Асинхронное использование

### Базовый асинхронный поиск

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def main():
    # Google поиск
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        results = await google.search("python programming")
        print(f"Google: {results.total_results} результатов")
    
    # Yandex поиск
    async with AsyncYandexClient(user_id=123, api_key="your_yandex_key") as yandex:
        results = await yandex.search("программирование на python")
        print(f"Yandex: {results.total_results} результатов")

# Запуск
asyncio.run(main())
```

### Параллельные запросы

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def parallel_search():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        # Создаем задачи для параллельного выполнения
        tasks = [
            google.search("python programming"),
            google.search("machine learning"),
            google.search("data science")
        ]
        
        # Выполняем все задачи параллельно
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results):
            print(f"Запрос {i+1}: {result.total_results} результатов")

asyncio.run(parallel_search())
```

### Смешанный поиск Google + Yandex

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def mixed_search():
    query = "программирование на python"
    
    async with AsyncGoogleClient(user_id=123, api_key="google_key") as google, \
             AsyncYandexClient(user_id=123, api_key="yandex_key") as yandex:
        
        # Поиск в обеих системах параллельно
        google_task = google.search(query)
        yandex_task = yandex.search(query)
        
        google_results, yandex_results = await asyncio.gather(
            google_task, yandex_task
        )
        
        print(f"Google: {google_results.total_results} результатов")
        print(f"Yandex: {yandex_results.total_results} результатов")

asyncio.run(mixed_search())
```

### 📰 Поиск по новостям

```python
from xmlriver_pro import GoogleNews, YandexNews
from xmlriver_pro.core.types import TimeFilter

google_news = GoogleNews(user_id=123, api_key="your_key")
news_results = google_news.search_news("python", time_filter=TimeFilter.LAST_WEEK)

yandex_news = YandexNews(user_id=123, api_key="your_key")
yandex_news_results = yandex_news.search_news_last_day("python новости")
```

### 🖼️ Поиск по изображениям

```python
from xmlriver_pro import GoogleImages

images = GoogleImages(user_id=123, api_key="your_key")

image_results = images.search_images("python logo", count=20)
large_images = images.search_images_by_size("python logo", "large")
color_images = images.search_images_by_color("python logo", "blue")
```

### 🗺️ Поиск по картам

```python
from xmlriver_pro import GoogleMaps

maps = GoogleMaps(user_id=123, api_key="your_key")

map_results = maps.search_maps(
    query="кафе Москва",
    zoom=12,
    coords=(55.7558, 37.6176)
)

nearby_cafes = maps.search_nearby("кафе", coords=(55.7558, 37.6176), radius=1000)
```

### 📢 Рекламные блоки

```python
from xmlriver_pro import GoogleAds, YandexAds

google_ads = GoogleAds(user_id=123, api_key="your_key")
ads_response = google_ads.get_ads("python programming")

yandex_ads = YandexAds(user_id=123, api_key="your_key")
yandex_ads_response = yandex_ads.get_ads("программирование python")
```

### 🧩 Специальные блоки

```python
from xmlriver_pro import GoogleSpecialBlocks, YandexSpecialBlocks

# Google специальные блоки
google_special = GoogleSpecialBlocks(user_id=123, api_key="your_key")

# OneBox документы
onebox_docs = google_special.get_onebox_documents("python", ["organic", "video"])

# Knowledge Graph
kg = google_special.get_knowledge_graph("Python programming language")

# Калькулятор
calc_result = google_special.get_calculator("2 + 2")

# Переводчик
translation = google_special.get_translator("hello world")

# Погода
weather = google_special.get_weather("weather Moscow")

# Конвертер валют
currency = google_special.get_currency_converter("100 USD to EUR")

# Время
time_info = google_special.get_time("time in Moscow")

# Блок ответов
answer_box = google_special.get_answer_box("what is python")

# Yandex колдунщики
yandex_special = YandexSpecialBlocks(user_id=123, api_key="your_key")

# Колдунщики поиска
searchsters = yandex_special.get_searchsters("python", ["organic", "video"])

# Погода
weather = yandex_special.get_weather("погода Москва")

# Переводчик
translation = yandex_special.get_translator("hello world")

# Конвертер валют
currency = yandex_special.get_currency_converter("100 долларов в рубли")

# Время
time_info = yandex_special.get_time("время в Москве")

# IP адрес
ip_info = yandex_special.get_ip_address()

# Карты
maps_info = yandex_special.get_maps("кафе Москва")

# Музыка
music_info = yandex_special.get_music("python programming")

# Цитаты
quotes = yandex_special.get_quotes("python programming")

# Факты
facts = yandex_special.get_facts("python programming")
```

## 📊 Типы данных

### Основные типы результатов

```python
from xmlriver_pro.core.types import (
    SearchResult, NewsResult, ImageResult, MapResult, 
    AdResult, AdsResponse, SearchResponse
)

# SearchResult - результат органического поиска
result = SearchResult(
    rank=1,
    url="https://python.org",
    title="Python Programming Language",
    snippet="Python is a programming language...",
    content_type="organic",
    stars=4.8
)

# NewsResult - результат поиска новостей
news = NewsResult(
    rank=1,
    url="https://news.example.com",
    title="Python News",
    snippet="Latest Python updates...",
    pub_date="2024-01-15"
)

# ImageResult - результат поиска изображений
image = ImageResult(
    rank=1,
    url="https://example.com/image.jpg",
    title="Python Logo",
    snippet="Official Python logo",
    image_url="https://example.com/logo.png",
    image_size="large"
)

# MapResult - результат поиска по картам
map_result = MapResult(
    rank=1,
    url="https://maps.google.com/...",
    title="Python Office",
    snippet="Python Software Foundation office",
    coords=(37.7749, -122.4194),
    address="San Francisco, CA"
)

# AdResult - рекламный результат
ad = AdResult(
    rank=1,
    url="https://ad.example.com",
    title="Python Course",
    snippet="Learn Python programming",
    ad_type="top"
)
```

### Перечисления (Enums)

```python
from xmlriver_pro.core.types import (
    SearchType, TimeFilter, DeviceType, OSType
)

# Типы поиска
search_type = SearchType.ORGANIC  # ORGANIC, NEWS, IMAGES, MAPS, ADS

# Фильтры времени для новостей
time_filter = TimeFilter.LAST_WEEK  # LAST_DAY, LAST_WEEK, LAST_MONTH, LAST_YEAR

# Типы устройств
device = DeviceType.DESKTOP  # DESKTOP, MOBILE, TABLET

# Операционные системы
os_type = OSType.WINDOWS  # WINDOWS, MACOS, LINUX, ANDROID, IOS
```

## 🔧 Расширенные возможности

### ✔️ Валидация параметров

```python
from xmlriver_pro.utils import validate_coords, validate_zoom, validate_url

# Валидация координат
coords = (55.7558, 37.6176)
if validate_coords(coords):
    # Координаты валидны

# Валидация zoom
if validate_zoom(12):
    # Zoom валиден

# Валидация URL
if validate_url("https://python.org"):
    # URL валиден
```

### 🔍 Расширенные методы поиска

```python
# Google расширенные методы
google = GoogleClient(user_id=123, api_key="your_key")

# Поиск с фильтром времени
results = google.search_with_time_filter("python", TimeFilter.LAST_WEEK)

# Поиск без автокоррекции
results = google.search_without_correction("pythn programming")

# Поиск с подсветкой
results = google.search_with_highlights("python programming")

# Поиск без фильтров
results = google.search_without_filter("python programming")

# Yandex расширенные методы
yandex = YandexClient(user_id=123, api_key="your_key")

# Поиск с фильтром времени (в днях)
results = yandex.search_with_time_filter("python", within=7)

# Поиск с подсветкой
results = yandex.search_with_highlights("python programming")

# Поиск с фильтрами
results = yandex.search_with_filter("python programming")

# Поиск по сайту
results = yandex.search_site("python.org", "programming")

# Поиск точной фразы
results = yandex.search_exact_phrase("python programming language")

# Поиск с исключением слов
results = yandex.search_exclude_words("python programming", ["tutorial", "course"])

# Поиск в заголовке
results = yandex.search_in_title("python programming")

# Поиск в URL
results = yandex.search_in_url("python.org")
```

### 🗺️ Специальные методы карт

```python
from xmlriver_pro import GoogleMaps

maps = GoogleMaps(user_id=123, api_key="your_key")

# Поиск ресторанов рядом
restaurants = maps.search_restaurants(
    coords=(55.7558, 37.6176), 
    query="ресторан"
)

# Поиск отелей
hotels = maps.search_hotels(
    coords=(55.7558, 37.6176)
)

# Поиск заправок
gas_stations = maps.search_gas_stations(
    coords=(55.7558, 37.6176)
)

# Поиск аптек
pharmacies = maps.search_pharmacies(
    coords=(55.7558, 37.6176)
)
```

### 🖼️ Специальные методы изображений

```python
from xmlriver_pro import GoogleImages

images = GoogleImages(user_id=123, api_key="your_key")

# Получение предложенных поисков
suggestions = images.get_suggested_searches("python logo")
```

### 📰 Специальные методы новостей

```python
from xmlriver_pro import YandexNews

news = YandexNews(user_id=123, api_key="your_key")

# Поиск новостей по региону
results = news.search_news_by_region("python", region_id=213)

# Поиск новостей по языку
results = news.search_news_by_language("python", language="en")

# Поиск новостей по домену
results = news.search_news_by_domain("python", domain="python.org")

# Получение трендов
trends = news.get_news_trends("python programming")
```

### 📝 Форматирование результатов

```python
from xmlriver_pro.utils import format_search_response, format_ads_response

# Форматирование результатов поиска
formatted_results = format_search_response(search_results)

# Форматирование рекламных блоков
formatted_ads = format_ads_response(ads_response)
```

### ⚠️ Обработка ошибок

```python
from xmlriver_pro.core import (
    XMLRiverError, AuthenticationError, RateLimitError, 
    NoResultsError, NetworkError, ValidationError,
    InsufficientFundsError, ServiceUnavailableError
)

try:
    results = google.search("python")
except AuthenticationError as e:
    # Ошибка аутентификации (коды 31, 42, 45)
    logger.error(f"Authentication failed: {e}")
except RateLimitError as e:
    # Превышен лимит запросов (коды 110, 111, 115)
    logger.warning(f"Rate limit exceeded: {e}")
except NoResultsError as e:
    # Нет результатов поиска (код 15)
    logger.info(f"No results found: {e}")
except InsufficientFundsError as e:
    # Недостаточно средств (код 200)
    logger.error(f"Insufficient funds: {e}")
except ServiceUnavailableError as e:
    # Сервис недоступен (коды 101, 201)
    logger.warning(f"Service unavailable: {e}")
except NetworkError as e:
    # Ошибка сети (коды 500, 202) - требует повтора
    logger.error(f"Network error: {e}")
except ValidationError as e:
    # Ошибка валидации параметров (коды 2, 102-108, 120, 121)
    logger.error(f"Validation error: {e}")
```

## 📊 Статистика и мониторинг

```python
# Получение баланса (один на весь аккаунт)
balance = google.get_balance()  # или yandex.get_balance() - результат одинаковый

# Получение стоимости (разная для каждой системы)
google_cost = google.get_cost()  # Стоимость Google запросов
yandex_cost = yandex.get_cost()  # Стоимость Yandex запросов

# Получение информации об ограничениях API
limits = google.get_api_limits()
print(f"Максимум потоков: {limits['max_concurrent_streams']}")
print(f"Дневной лимит Google: {limits['daily_limits']['google']:,} запросов")
print(f"Дневной лимит Yandex: {limits['daily_limits']['yandex']:,} запросов")

# Проверка индексации
is_indexed = google.check_indexing("https://python.org")

# Проверка доверия к домену
is_trusted = google.is_trust_domain("python.org")
```

## ⚡ Ограничения API

### 🔢 **Потоки и производительность:**
- **Максимум потоков:** 10 для каждой системы (Google, Yandex, Wordstat)
- **Дневные лимиты:**
  - Google: ~200,000 запросов/сутки
  - Yandex: ~150,000 запросов/сутки
- **Скорость ответа:** 3-6 секунд (обычно), максимум 60 секунд

### ⏱️ **Рекомендации по таймаутам:**
```python
# Используйте таймаут 60 секунд для надежности
google = GoogleClient(user_id=123, api_key="key", timeout=60)

# При низком таймауте есть риск потерять ответы
# Деньги за запрос снимаются, но результат может не прийти
```

### 🚨 **Обработка ошибок потоков:**
```python
try:
    results = google.search("python")
except RateLimitError as e:
    if e.code in [110, 111, 115]:
        # Временные ошибки потоков - повторите запрос
        time.sleep(5)  # Подождите 5 секунд
        results = google.search("python")  # Повторите
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=xmlriver_pro

# Запуск конкретных тестов
pytest tests/test_google.py
pytest tests/test_yandex.py

# Запуск с детальным выводом
pytest -v
```

## 📚 Документация

- [README.md](README.md) - основная документация
- [docs/examples.md](docs/examples.md) - примеры использования
- [Исходный код](https://github.com/Eapwrk/xmlriver-pro) - полный код с комментариями

## 🤝 Вклад в проект

Issues и Pull Requests приветствуются на [GitHub](https://github.com/Eapwrk/xmlriver-pro).

### Установка для разработки

```bash
git clone https://github.com/Eapwrk/xmlriver-pro.git
cd xmlriver-pro
pip install -e ".[dev]"
pre-commit install
```

### Запуск тестов

```bash
pytest
black xmlriver_pro tests
pylint xmlriver_pro
mypy xmlriver_pro
```

## 📄 Лицензия

MIT License. Подробности в [LICENSE](LICENSE).

## 🙏 Благодарности

- [xmlriver.com](https://xmlriver.com) за предоставление API
- Python сообществу за экосистему
- Контрибьюторам проекта

## 📞 Поддержка

- 📧 Email: seo@controlseo.ru
- 🐛 Issues: [GitHub Issues](https://github.com/Eapwrk/xmlriver-pro/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Eapwrk/xmlriver-pro/discussions)

---

## 📈 Статистика проекта

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/Eapwrk/xmlriver-pro?style=social&label=Stars)
![GitHub forks](https://img.shields.io/github/forks/Eapwrk/xmlriver-pro?style=social&label=Forks)
![GitHub watchers](https://img.shields.io/github/watchers/Eapwrk/xmlriver-pro?style=social&label=Watchers)

**XMLRiver Pro** - Professional Python client for XMLRiver API

</div>
