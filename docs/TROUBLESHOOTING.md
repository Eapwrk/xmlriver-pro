# Решение проблем

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md)

Руководство по решению типичных проблем при использовании XMLRiver Pro.

## Содержание

- [Ошибки аутентификации](#ошибки-аутентификации)
- [Превышение лимитов](#превышение-лимитов)
- [Проблемы с потоками](#проблемы-с-потоками)
- [Таймауты](#таймауты)
- [Проблемы с парсингом](#проблемы-с-парсингом)
- [Валидация параметров](#валидация-параметров)
- [Проблемы с асинхронностью](#проблемы-с-асинхронностью)
- [Проблемы с установкой](#проблемы-с-установкой)
- [Отладка](#отладка)

## Ошибки аутентификации

### AuthenticationError: Invalid API key

**Проблема:** Ошибка аутентификации с кодом 31, 42 или 45.

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core.exceptions import AuthenticationError

async def main():
    try:
        async with AsyncGoogleClient(user_id=123, api_key="invalid_key") as client:
            results = await client.search("python")
    except AuthenticationError as e:
        print(f"Ошибка аутентификации: {e}")

asyncio.run(main())
```

**Решение:**

1. **Проверьте API ключ:**
   ```python
   # Убедитесь, что ключ правильный
   api_key = "your_correct_api_key"  # Без пробелов, лишних символов
   ```

2. **Проверьте user_id:**
   ```python
   # Убедитесь, что user_id правильный
   user_id = 123  # Число, не строка
   ```

3. **Используйте переменные окружения:**
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()

   user_id = int(os.getenv("XMLRIVER_USER_ID"))
   api_key = os.getenv("XMLRIVER_API_KEY")

   async with AsyncGoogleClient(user_id=user_id, api_key=api_key) as client:
       results = await client.search("test")
   ```

4. **Проверьте баланс:**
   ```python
   try:
       balance = await client.get_balance()
       print(f"Баланс: {balance}")
   except AuthenticationError:
       print("Проблема с аутентификацией")
   ```

### AuthenticationError: Insufficient funds

**Проблема:** Недостаточно средств на балансе (код 200).

```python
from xmlriver_pro.core.exceptions import InsufficientFundsError

try:
    results = client.search("python")
except InsufficientFundsError as e:
    print(f"Недостаточно средств: {e}")
```

**Решение:**

1. **Проверьте баланс:**
   ```python
   balance = await client.get_balance()
   print(f"Текущий баланс: {balance}")

   if balance <= 0:
       print("Пополните баланс на xmlriver.com")
   ```

2. **Проверьте стоимость запросов:**
   ```python
   google_cost = await client.get_cost()
   print(f"Стоимость Google запроса: {google_cost}")
   ```

## Превышение лимитов

### RateLimitError: Rate limit exceeded

**Проблема:** Превышен лимит запросов (коды 110, 111, 115).

```python
from xmlriver_pro.core.exceptions import RateLimitError
import time

try:
    results = client.search("python")
except RateLimitError as e:
    print(f"Превышен лимит: {e}")
```

**Решение:**

1. **Добавьте задержки между запросами:**
   ```python
   import time

   queries = ["python", "javascript", "java"]

   for query in queries:
       try:
           results = client.search(query)
           print(f"Найдено {results.total_results} результатов для '{query}'")
       except RateLimitError:
           print("Превышен лимит, ждем 5 секунд...")
           time.sleep(5)
           # Повторяем запрос
           results = client.search(query)
   ```

2. **Используйте адаптивные задержки:**
   ```python
   def adaptive_search(client, queries, initial_delay=1.0):
       delay = initial_delay

       for query in queries:
           try:
               results = client.search(query)
               print(f"Успех: {query}")
               delay = max(0.1, delay * 0.9)  # Уменьшаем задержку
           except RateLimitError:
               print(f"Rate limit, увеличиваем задержку до {delay:.1f} сек")
               delay = min(10.0, delay * 1.5)  # Увеличиваем задержку
               time.sleep(delay)
               results = client.search(query)

           time.sleep(delay)
   ```

3. **Проверьте лимиты API:**
   ```python
   limits = client.get_api_limits()
   print(f"Максимум потоков: {limits['max_concurrent_streams']}")
   print(f"Дневной лимит Google: {limits['daily_limits']['google']:,}")
   print(f"Дневной лимит Yandex: {limits['daily_limits']['yandex']:,}")
   ```

## Проблемы с потоками

### Слишком много одновременных запросов

**Проблема:** Ошибки при использовании асинхронных клиентов.

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

async def too_many_requests():
    async with AsyncGoogleClient(user_id=123, api_key="key") as client:
        # Слишком много одновременных запросов
        tasks = [client.search(f"query_{i}") for i in range(100)]
        results = await asyncio.gather(*tasks)  # Может вызвать ошибки
```

**Решение:**

1. **Используйте ограничение потоков:**
   ```python
   async def controlled_requests():
       async with AsyncGoogleClient(
           user_id=123,
           api_key="key",
           max_concurrent=5  # Ограничиваем до 5 потоков
       ) as client:
           tasks = [client.search(f"query_{i}") for i in range(20)]
           results = await asyncio.gather(*tasks)
   ```

2. **Мониторинг потоков:**
   ```python
   async def monitor_requests():
       async with AsyncGoogleClient(user_id=123, api_key="key") as client:
           # Проверяем статус потоков
           status = client.get_concurrent_status()
           print(f"Активных запросов: {status['active_requests']}")
           print(f"Доступных слотов: {status['available_slots']}")

           # Выполняем запросы
           results = await client.search("python")
   ```

3. **Используйте семафор для дополнительного контроля:**
   ```python
   async def semaphore_controlled():
       semaphore = asyncio.Semaphore(3)  # Максимум 3 одновременных запроса

       async with AsyncGoogleClient(user_id=123, api_key="key") as client:
           async def controlled_search(query):
               async with semaphore:
                   return await client.search(query)

           tasks = [controlled_search(f"query_{i}") for i in range(10)]
           results = await asyncio.gather(*tasks)
   ```

## Таймауты

### TimeoutError: Request timeout

**Проблема:** Запросы превышают установленный таймаут.

```python
import asyncio
import aiohttp
from xmlriver_pro import AsyncGoogleClient

async def main():
    try:
        async with AsyncGoogleClient(user_id=123, api_key="key", timeout=5) as client:
            results = await client.search("python")
    except asyncio.TimeoutError:
        print("Превышен таймаут запроса")

asyncio.run(main())
```

**Решение:**

1. **Увеличьте таймаут:**
   ```python
   # Рекомендуемый таймаут 60 секунд
   async with AsyncGoogleClient(user_id=123, api_key="key", timeout=60) as client:
       results = await client.search("python")
   ```

2. **Используйте retry механизм:**
   ```python
   async with AsyncGoogleClient(
       user_id=123,
       api_key="key",
       timeout=60,
       max_retries=3,  # 3 попытки
       retry_delay=1.0  # 1 секунда между попытками
   ) as client:
       results = await client.search("python")
   ```

3. **Обработка таймаутов:**
   ```python
   import time
   from requests.exceptions import Timeout

   def search_with_retry(client, query, max_retries=3):
       for attempt in range(max_retries):
           try:
               return client.search(query)
           except Timeout:
               if attempt < max_retries - 1:
                   print(f"Таймаут, попытка {attempt + 2}/{max_retries}")
                   time.sleep(2 ** attempt)  # Экспоненциальная задержка
               else:
                   raise
   ```

## Проблемы с парсингом

### Ошибки парсинга XML

**Проблема:** Ошибки при парсинге ответов API.

```python
import xmltodict
from xml.parsers.expat import ExpatError

try:
    # Внутренний парсинг XML
    results = client.search("python")
except ExpatError as e:
    print(f"Ошибка парсинга XML: {e}")
```

**Решение:**

1. **Проверьте формат ответа:**
   ```python
   # Включите отладку для просмотра сырого ответа
   import logging
   logging.basicConfig(level=logging.DEBUG)

   results = client.search("python")
   ```

2. **Обработка некорректных ответов:**
   ```python
   try:
       results = await client.search("python")
   except Exception as e:
       print(f"Ошибка: {e}")
       # Проверьте баланс и лимиты
       balance = await client.get_balance()
       print(f"Баланс: {balance}")
   ```

3. **Валидация ответа:**
   ```python
   def safe_search(client, query):
       try:
           results = client.search(query)

           # Проверяем структуру ответа
           if not hasattr(results, 'total_results'):
               print("Некорректная структура ответа")
               return None

           if results.total_results == 0:
               print("Нет результатов")
               return results

           return results

       except Exception as e:
           print(f"Ошибка поиска: {e}")
           return None
   ```

## Валидация параметров

### ValidationError: Invalid parameters

**Проблема:** Ошибки валидации параметров (коды 2, 102-108, 120, 121).

```python
from xmlriver_pro.core.exceptions import ValidationError

try:
    results = client.search("")  # Пустой запрос
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
```

**Решение:**

1. **Используйте валидаторы:**
   ```python
   from xmlriver_pro.utils import validate_query, validate_device, validate_country

   def safe_search(client, query, device="desktop", country=2840):
       # Валидируем параметры перед запросом
       if not validate_query(query):
           raise ValueError("Невалидный поисковый запрос")

       if not validate_device(device):
           raise ValueError("Невалидный тип устройства")

       if not validate_country(country):
           raise ValueError("Невалидный ID страны")

       return client.search(query, device=device, country=country)
   ```

2. **Комплексная валидация:**
   ```python
   from xmlriver_pro.utils import (
       validate_query, validate_device, validate_os, validate_country,
       validate_region, validate_language, validate_domain, validate_groupby,
       validate_page, validate_time_filter, validate_within
   )

   def validate_all_params(params, search_engine="google"):
       errors = []

       if not validate_query(params.get("query")):
           errors.append("Невалидный поисковый запрос")

       if "device" in params and not validate_device(params["device"]):
           errors.append("Невалидный тип устройства")

       if "country" in params and not validate_country(params["country"]):
           errors.append("Невалидный ID страны")

       if "page" in params and not validate_page(params["page"], search_engine):
           errors.append("Невалидный номер страницы")

       if errors:
           raise ValidationError(f"Ошибки валидации: {', '.join(errors)}")

       return True
   ```

## Проблемы с асинхронностью

### RuntimeError: Event loop is closed

**Проблема:** Ошибки при работе с асинхронными клиентами.

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient

# Неправильное использование
async def wrong_usage():
    client = AsyncGoogleClient(user_id=123, api_key="key")
    results = await client.search("python")
    # Забыли закрыть клиент
```

**Решение:**

1. **Используйте контекстный менеджер:**
   ```python
   async def correct_usage():
       async with AsyncGoogleClient(user_id=123, api_key="key") as client:
           results = await client.search("python")
           return results
   ```

2. **Правильное закрытие клиента:**
   ```python
   async def manual_close():
       client = AsyncGoogleClient(user_id=123, api_key="key")
       try:
           results = await client.search("python")
           return results
       finally:
           await client.close()
   ```

3. **Обработка ошибок асинхронности:**
   ```python
   async def safe_async_search():
       try:
           async with AsyncGoogleClient(user_id=123, api_key="key") as client:
               results = await client.search("python")
               return results
       except Exception as e:
           print(f"Ошибка асинхронного поиска: {e}")
           return None
   ```

## Проблемы с установкой

### ImportError: No module named 'xmlriver_pro'

**Проблема:** Модуль не найден при импорте.

```python
from xmlriver_pro import AsyncGoogleClient  # Правильный импорт
```

**Решение:**

1. **Установите пакет:**
   ```bash
   pip install xmlriver-pro
   ```

2. **Проверьте версию Python:**
   ```bash
   python --version  # Должно быть 3.10+
   ```

3. **Установите в виртуальном окружении:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # или
   .venv\Scripts\activate     # Windows
   pip install xmlriver-pro
   ```

4. **Проверьте установку:**
   ```python
   import xmlriver_pro
   print(xmlriver_pro.__version__)
   ```

### ModuleNotFoundError: No module named 'aiohttp'

**Проблема:** Отсутствуют зависимости для асинхронных клиентов.

**Решение:**

1. **Установите зависимости:**
   ```bash
   pip install aiohttp xmltodict python-dotenv
   ```

2. **Или установите с зависимостями:**
   ```bash
   pip install xmlriver-pro[async]
   ```

## Отладка

### Включение отладки

```python
import logging

# Включите отладку
logging.basicConfig(level=logging.DEBUG)

# Теперь вы увидите детальную информацию о запросах
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    results = await client.search("python")
```

### Проверка статуса клиента

```python
async def debug_client_status(client):
    """Отладочная информация о клиенте"""
    try:
        balance = await client.get_balance()
        cost = await client.get_cost()
        limits = client.get_api_limits()

        print("=== Статус клиента ===")
        print(f"Баланс: {balance}")
        print(f"Стоимость запроса: {cost}")
        print(f"Лимиты: {limits}")

    except Exception as e:
        print(f"Ошибка получения статуса: {e}")

# Использование
debug_client_status(client)
```

### Тестирование подключения

```python
def test_connection(client):
    """Тест подключения к API"""
    try:
        # Простой запрос для проверки
        results = client.search("test")
        print("✅ Подключение работает")
        print(f"Найдено результатов: {results.total_results}")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

# Использование
if test_connection(client):
    print("API доступен")
else:
    print("Проблемы с API")
```

### Логирование запросов

```python
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('xmlriver.log'),
        logging.StreamHandler()
    ]
)

def logged_search(client, query):
    """Поиск с логированием"""
    start_time = datetime.now()

    try:
        results = client.search(query)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logging.info(f"Поиск '{query}': {results.total_results} результатов за {duration:.2f} сек")
        return results

    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logging.error(f"Ошибка поиска '{query}' за {duration:.2f} сек: {e}")
        raise

# Использование
results = logged_search(client, "python programming")
```

---

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md) • [Продвинутое использование](ADVANCED_USAGE.md)
