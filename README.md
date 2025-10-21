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
[![GitHub issues](https://img.shields.io/badge/github-issues-red?style=social)](https://github.com/Eapwrk/xmlriver-pro/issues)

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
- 📊 **Yandex Wordstat** - частотность и динамика запросов
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
pip install xmlriver-pro==1.2.7
```

### 🔧 **Из исходного кода:**
```bash
git clone https://github.com/Eapwrk/xmlriver-pro.git
cd xmlriver-pro
pip install -e .
```

### 📋 **Зависимости:**
- Python 3.10+
- requests
- aiohttp (для асинхронных клиентов)
- xmltodict
- python-dotenv

## 🚀 Быстрый старт

### 🔑 Получение API ключей

1. Зарегистрируйтесь на [xmlriver.com](https://xmlriver.com)
2. Получите `user_id` и `api_key` в личном кабинете
3. Пополните баланс для использования API

### 🔧 Переменные окружения

Создайте файл `.env`:
```bash
XMLRIVER_USER_ID=your_user_id_here
XMLRIVER_API_KEY=your_api_key_here
```

### 📝 Базовые примеры

#### Асинхронный поиск
```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def main():
    # Google асинхронный поиск
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        results = await google.search("python programming")
        print(f"Найдено: {results.total_results} результатов")

    # Yandex асинхронный поиск
    async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex:
        results = await yandex.search("программирование python")
        print(f"Найдено: {results.total_results} результатов")

asyncio.run(main())
```

#### Поиск новостей
```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient
from xmlriver_pro.core.types import TimeFilter

async def main():
    # Google новости
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        results = await google.search_news("python", time_filter=TimeFilter.LAST_WEEK)
        for news in results.results:
            print(f"{news.title}: {news.url}")

    # Yandex новости
    async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex:
        results = await yandex.search_news("python")
        for news in results.results:
            print(f"{news.title}: {news.url}")

asyncio.run(main())
```

#### Поиск изображений
```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        results = await google.search_images("python logo", num_results=20)
        for image in results.results:
            print(f"{image.title}: {image.img_url}")

asyncio.run(main())
```

#### Поиск по картам
```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        results = await google.search_maps(
            "python office",
            coords=(37.7749, -122.4194),
            zoom=12
        )
        for place in results.results:
            print(f"{place.title}: {place.address}")

asyncio.run(main())
```

#### Рекламные блоки
```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def main():
    # Google реклама
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        results = await google.get_ads("python programming")
        for ad in results.results:
            print(f"{ad.title}: {ad.url}")

    # Yandex реклама
    async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex:
        results = await yandex.get_ads("программирование python")
        for ad in results.results:
            print(f"{ad.title}: {ad.url}")

asyncio.run(main())
```

#### Yandex Wordstat

```python
import asyncio
from xmlriver_pro import AsyncWordstatClient

async def main():
    async with AsyncWordstatClient(user_id=123, api_key="your_key") as client:
        # Получение топов запросов
        result = await client.get_words("python")
        print(f"Associations: {len(result.associations)}")
        print(f"Popular: {len(result.popular)}")

        # Получение динамики
        history = await client.get_history("python", period="month")
        print(f"Total frequency: {history.total_value}")

        # Получение частотности
        frequency = await client.get_frequency("python")
        print(f"Frequency: {frequency}")

asyncio.run(main())
```

## 🔧 Конфигурация

### Основные параметры

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `user_id` | ID пользователя XMLRiver | Обязательный |
| `api_key` | API ключ XMLRiver | Обязательный |
| `timeout` | Таймаут запроса (сек) | 60 |
| `retry_count` | Количество повторов | 3 |
| `retry_delay` | Задержка между повторами (сек) | 1.0 |
| `max_concurrent` | Максимум одновременных запросов | 10 |

### Пример конфигурации
```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(
        user_id=123,
        api_key="your_key",
        timeout=60,           # 60 секунд таймаут
        max_retries=3,        # 3 попытки
        retry_delay=1.0,      # 1 секунда между попытками
        max_concurrent=5      # 5 одновременных запросов
    ) as client:
        results = await client.search("python")
        print(f"Найдено: {results.total_results}")

asyncio.run(main())
```

### Переменные окружения
```python
import os
import asyncio
from dotenv import load_dotenv
from xmlriver_pro import AsyncGoogleClient

load_dotenv()

async def main():
    async with AsyncGoogleClient(
        user_id=int(os.getenv("XMLRIVER_USER_ID")),
        api_key=os.getenv("XMLRIVER_API_KEY")
    ) as client:
        results = await client.search("python")
        print(f"Найдено: {results.total_results}")

asyncio.run(main())
```

## 💡 Примеры использования

### Мониторинг потоков (асинхронные клиенты)
```python
async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
    # Проверяем статус потоков
    status = client.get_concurrent_status()
    print(f"Активных запросов: {status['active_requests']}")
    print(f"Доступных слотов: {status['available_slots']}")
```

### Основные валидаторы
```python
from xmlriver_pro.utils import validate_coords, validate_zoom, validate_url

# Валидация координат
coords = (55.7558, 37.6176)
if validate_coords(coords):
    print("Координаты валидны")

# Валидация zoom
if validate_zoom(12):
    print("Zoom валиден")

# Валидация URL
if validate_url("https://python.org"):
    print("URL валиден")
```

### Основные форматтеры
```python
from xmlriver_pro.utils import format_search_response, format_ads_response

# Форматирование результатов поиска
formatted_results = format_search_response(search_results)

# Форматирование рекламных блоков
formatted_ads = format_ads_response(ads_response)
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

## ⚠️ Обработка ошибок

```python
import asyncio
import logging
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core import (
    XMLRiverError, AuthenticationError, RateLimitError,
    NoResultsError, NetworkError, ValidationError,
    InsufficientFundsError, ServiceUnavailableError
)

logger = logging.getLogger(__name__)

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="key") as google:
        try:
            results = await google.search("python")
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

asyncio.run(main())
```

## 📊 Статистика и мониторинг

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        # Получение баланса (один на весь аккаунт)
        balance = await google.get_balance()
        print(f"Баланс: {balance} руб.")

        # Получение стоимости Google запросов
        google_cost = await google.get_cost()
        print(f"Стоимость Google: {google_cost} руб/1000 запросов")

    async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex:
        # Получение стоимости Yandex запросов (разная для каждой системы)
        yandex_cost = await yandex.get_cost()
        print(f"Стоимость Yandex: {yandex_cost} руб/1000 запросов")

asyncio.run(main())
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
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    # Используйте таймаут 60 секунд для надежности
    async with AsyncGoogleClient(user_id=123, api_key="key", timeout=60) as google:
        results = await google.search("python")
        # При низком таймауте есть риск потерять ответы
        # Деньги за запрос снимаются, но результат может не прийти

asyncio.run(main())
```

### 🚨 **Обработка ошибок потоков:**
```python
import asyncio
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core import RateLimitError

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="key") as google:
        try:
            results = await google.search("python")
        except RateLimitError as e:
            if e.code in [110, 111, 115]:
                # Временные ошибки потоков - повторите запрос
                await asyncio.sleep(5)  # Подождите 5 секунд
                results = await google.search("python")  # Повторите

asyncio.run(main())
```

## 🧪 Тестирование

### ✅ Безопасное тестирование (БЕЗ реальных API запросов)

```bash
# Запуск всех тестов (БЕЗ real_api, по умолчанию)
pytest

# Запуск с покрытием
pytest --cov=xmlriver_pro

# Запуск конкретных тестов
pytest tests/test_google.py
pytest tests/test_yandex.py

# Запуск с детальным выводом
pytest -v
```

**✅ Эти команды БЕЗОПАСНЫ и НЕ требуют API ключей**

### ⚠️ Real API тесты (требуют ключи и СТОЯТ ДЕНЕГ!)

```bash
# ⚠️ ВНИМАНИЕ: следующие команды делают реальные API запросы и ТРАТЯТ ДЕНЬГИ!
pytest -m real_api -v  # Запуск ТОЛЬКО real_api тестов (~$5-10)
```

📖 **Полная документация по тестированию:** [TESTING.md](TESTING.md)
- Подробное описание всех типов тестов
- Инструкции по настройке Real API тестов
- Защитные механизмы и best practices

## 📚 Документация

- **[README.md](README.md)** - основная документация (этот файл)
- **[docs/README.md](docs/README.md)** - обзор всей документации
- **[docs/examples.md](docs/examples.md)** - детальные примеры всех методов
- **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - полный справочник API
- **[docs/ADVANCED_USAGE.md](docs/ADVANCED_USAGE.md)** - продвинутые сценарии
- **[docs/SPECIAL_BLOCKS_GUIDE.md](docs/SPECIAL_BLOCKS_GUIDE.md)** - специальные блоки
- **[docs/WORDSTAT_GUIDE.md](docs/WORDSTAT_GUIDE.md)** - руководство по Wordstat API
- **[docs/VALIDATORS_REFERENCE.md](docs/VALIDATORS_REFERENCE.md)** - все валидаторы
- **[docs/FORMATTERS_REFERENCE.md](docs/FORMATTERS_REFERENCE.md)** - все форматтеры
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - решение проблем
- **[Исходный код](https://github.com/Eapwrk/xmlriver-pro)** - полный код с комментариями

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
