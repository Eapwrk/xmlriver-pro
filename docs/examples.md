# Примеры использования XMLRiver Pro

[← Назад к README](../README.md) • [Документация](README.md)

## Содержание

1. [Базовое использование](#базовое-использование)
2. [Google API](#google-api)
3. [Yandex API](#yandex-api)
4. [Обработка ошибок](#обработка-ошибок)
5. [Продвинутые сценарии](#продвинутые-сценарии)

## Базовое использование

### Инициализация клиентов

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def main():
    # Google клиент
    async with AsyncGoogleClient(
        user_id=123,
        api_key="your_google_api_key"
    ) as google:
        results = await google.search("python programming")
        print(f"Найдено результатов: {results.total_results}")
    
    # Yandex клиент
    async with AsyncYandexClient(
        user_id=123,
        api_key="your_yandex_api_key"
    ) as yandex:
        results = await yandex.search("программирование на python")
        print(f"Найдено результатов: {results.total_results}")

asyncio.run(main())
```

### Простой поиск

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        # Google поиск
        results = await google.search("python programming")
        print(f"Найдено результатов: {results.total_results}")
        
        for result in results.results:
            print(f"{result.rank}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Snippet: {result.snippet}")
            print()

asyncio.run(main())
```

## Google API

### Органический поиск

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core.types import DeviceType, SearchType, TimeFilter

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
        # Базовый поиск
        results = await client.search("python programming")
        
        # Поиск с параметрами
        results = await client.search(
            query="python programming",
            num_results=10,
            start=0,
            country=10,  # США
            device=DeviceType.DESKTOP
        )

asyncio.run(main())
```

### Поиск новостей

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core.types import TimeFilter

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
        # Базовый поиск новостей
        results = await client.search_news("python")
        
        # Поиск новостей с фильтром времени
        results = await client.search_news(
            "python news",
            time_filter=TimeFilter.LAST_WEEK
        )
        
        for news in results.results:
            print(f"{news.title}")
            print(f"Дата: {news.pub_date}")
            print(f"URL: {news.url}")
            print()

asyncio.run(main())
```

### Поиск изображений

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
        # Базовый поиск изображений
        results = await client.search_images("python logo", num_results=20)
        
        # Поиск с параметрами
        results = await client.search_images(
            query="python programming",
            num_results=50,
            size="large",
            color="color",
            image_type="photo"
        )
        
        for image in results.results:
            print(f"{image.title}")
            print(f"URL изображения: {image.img_url}")
            print(f"Размер: {image.original_width}x{image.original_height}")
            print()

asyncio.run(main())
```

### Поиск по картам

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
        # Поиск с координатами
        results = await client.search_maps(
            query="python office",
            coords=(37.7749, -122.4194),  # Сан-Франциско
            zoom=12
        )
        
        for place in results.results:
            print(f"{place.title}")
            print(f"Адрес: {place.address}")
            print(f"Координаты: {place.latitude}, {place.longitude}")
            print(f"Рейтинг: {place.stars}")
            print()

asyncio.run(main())
```

### Рекламные блоки

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
        # Получение рекламных блоков
        results = await client.get_ads("python programming")
        
        for ad in results.results:
            print(f"{ad.title}")
            print(f"URL: {ad.url}")
            print(f"Рекламный URL: {ad.ads_url}")
            print()

asyncio.run(main())
```

### Специальные блоки

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="your_key") as client:
        # Получение специальных блоков (OneBox, Knowledge Graph)
        results = await client.get_special_blocks("python programming")
        
        for block in results.results:
            if hasattr(block, 'entity_name'):  # Knowledge Graph
                print(f"Knowledge Graph: {block.entity_name}")
                print(f"Описание: {block.description}")
            elif hasattr(block, 'content_type'):  # OneBox
                print(f"OneBox: {block.title}")
                print(f"Контент: {block.snippet}")
            print()

asyncio.run(main())
```

## Yandex API

### Органический поиск

```python
import asyncio
from xmlriver_pro import AsyncYandexClient
from xmlriver_pro.core.types import DeviceType, OSType

async def main():
    async with AsyncYandexClient(user_id=123, api_key="your_key") as client:
        # Базовый поиск
        results = await client.search("программирование python")
        
        # Поиск с параметрами
        results = await client.search(
            query="python программирование",
            num_results=10,
            start=0,
            lr=213,  # Москва
            lang="ru",
            domain="ru",
            device=DeviceType.DESKTOP
        )

asyncio.run(main())
```

### Поиск новостей

```python
import asyncio
from xmlriver_pro import AsyncYandexClient

async def main():
    async with AsyncYandexClient(user_id=123, api_key="your_key") as client:
        # Базовый поиск новостей
        results = await client.search_news("python")
        
        for news in results.results:
            print(f"{news.title}")
            print(f"Дата: {news.pub_date}")
            print(f"URL: {news.url}")
            print()

asyncio.run(main())
```

### Рекламные блоки

```python
import asyncio
from xmlriver_pro import AsyncYandexClient

async def main():
    async with AsyncYandexClient(user_id=123, api_key="your_key") as client:
        # Получение рекламных блоков
        results = await client.get_ads("программирование python")
        
        for ad in results.results:
            print(f"{ad.title}")
            print(f"URL: {ad.url}")
            print()

asyncio.run(main())
```

### Специальные блоки (Колдунщики)

```python
import asyncio
from xmlriver_pro import AsyncYandexClient

async def main():
    async with AsyncYandexClient(user_id=123, api_key="your_key") as client:
        # Получение специальных блоков (колдунщиков)
        results = await client.get_special_blocks("погода москва")
        
        for block in results.results:
            print(f"{block.title}: {block.snippet}")
            print()

asyncio.run(main())
```

## Обработка ошибок

### Базовая обработка ошибок

```python
import asyncio
import logging
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core import (
    XMLRiverError, AuthenticationError, RateLimitError,
    NoResultsError, NetworkError, ValidationError
)

logger = logging.getLogger(__name__)

async def main():
    async with AsyncGoogleClient(user_id=123, api_key="key") as client:
        try:
            results = await client.search("python")
        except AuthenticationError as e:
            logger.error(f"Ошибка аутентификации: {e}")
        except RateLimitError as e:
            logger.warning(f"Превышен лимит запросов: {e}")
            await asyncio.sleep(5)  # Подождать перед повтором
        except NoResultsError as e:
            logger.info(f"Результаты не найдены: {e}")
        except NetworkError as e:
            logger.error(f"Ошибка сети: {e}")
        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except XMLRiverError as e:
            logger.error(f"Общая ошибка XMLRiver: {e}")

asyncio.run(main())
```

## Продвинутые сценарии

### Параллельные запросы

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def main():
    # Создаём клиенты
    async with AsyncGoogleClient(user_id=123, api_key="key1") as google, \
               AsyncYandexClient(user_id=123, api_key="key2") as yandex:
        
        # Параллельные запросы
        google_results, yandex_results = await asyncio.gather(
            google.search("python programming"),
            yandex.search("программирование python")
        )
        
        print(f"Google: {google_results.total_results} результатов")
        print(f"Yandex: {yandex_results.total_results} результатов")

asyncio.run(main())
```

### Множественные запросы с семафором

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def search_query(client, query, semaphore):
    async with semaphore:
        results = await client.search(query)
        return query, results.total_results

async def main():
    queries = ["python", "java", "javascript", "c++", "ruby"]
    semaphore = asyncio.Semaphore(3)  # Максимум 3 одновременных запроса
    
    async with AsyncGoogleClient(user_id=123, api_key="key") as client:
        tasks = [search_query(client, q, semaphore) for q in queries]
        results = await asyncio.gather(*tasks)
        
        for query, count in results:
            print(f"{query}: {count:,} результатов")

asyncio.run(main())
```

### Использование с переменными окружения

```python
import os
import asyncio
from dotenv import load_dotenv
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

load_dotenv()

async def main():
    user_id = int(os.getenv("XMLRIVER_USER_ID"))
    api_key = os.getenv("XMLRIVER_API_KEY")
    
    async with AsyncGoogleClient(user_id=user_id, api_key=api_key) as google:
        results = await google.search("python")
        print(f"Найдено: {results.total_results}")

asyncio.run(main())
```

---

**Подробнее:**
- [API Reference](API_REFERENCE.md) - полный справочник API
- [Advanced Usage](ADVANCED_USAGE.md) - продвинутые техники
- [Troubleshooting](TROUBLESHOOTING.md) - решение проблем
