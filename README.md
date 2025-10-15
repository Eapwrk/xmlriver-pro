# XMLRiver Pro

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-57%25-brightgreen.svg)](https://github.com/Eapwrk/xmlriver-pro)

> Fork of [KursHub-ru/xmlriver](https://github.com/KursHub-ru/xmlriver)

Python библиотека для работы с API xmlriver.com. Расширенная версия с поддержкой всех типов поиска.

Поддерживает все типы поиска в Google и Yandex: органический поиск, новости, изображения, карты, реклама и специальные блоки.

## ✨ Что умеет

- 🔍 Органический поиск в Google и Yandex
- 📰 Поиск по новостям с фильтрами времени
- 🖼️ Поиск по изображениям (размер, цвет, тип)
- 🗺️ Поиск по картам с координатами
- 📢 Рекламные блоки (верхние и нижние)
- 🧩 Специальные блоки (OneBox, Knowledge Graph)
- ⚡ **Асинхронная поддержка** с aiohttp
- 🔄 **Параллельные запросы** с asyncio

## 🏗️ Особенности

- ✅ Полная типизация для Python 3.10+
- 🏛️ Модульная архитектура
- 🧪 66 тестов с покрытием 57%
- ⚠️ Специализированные исключения
- ✔️ Валидация параметров
- ⚡ **Синхронные и асинхронные клиенты**
- 🔄 **Поддержка многопоточности и параллелизма**

## 📦 Установка

### 🚀 **Из GitHub (рекомендуется):**
```bash
# Установка последней версии
pip install git+https://github.com/Eapwrk/xmlriver-pro.git

# Установка конкретной версии
pip install git+https://github.com/Eapwrk/xmlriver-pro.git@v1.0.1

# Обновление до последней версии
pip install --upgrade git+https://github.com/Eapwrk/xmlriver-pro.git
```

### 📦 **Из PyPI (если доступно):**
```bash
# Установка последней версии
pip install xmlriver-pro

# Установка конкретной версии
pip install xmlriver-pro==1.0.1

# Обновление до последней версии
pip install --upgrade xmlriver-pro
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

### Для разработки:
- **pytest** - тестирование
- **black** - форматирование кода
- **pylint** - анализ кода
- **mypy** - проверка типов

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

# Yandex колдунщики
yandex_special = YandexSpecialBlocks(user_id=123, api_key="your_key")

# Погода
weather = yandex_special.get_weather("погода Москва")

# Переводчик
translation = yandex_special.get_translator("hello world")
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

**XMLRiver Pro** - Python клиент для API xmlriver.com
