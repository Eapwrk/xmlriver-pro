# Руководство по работе с Yandex Wordstat API

[← Назад к README](../README.md) • [Документация](README.md)

## Содержание

1. [Введение](#введение)
2. [Быстрый старт](#быстрый-старт)
3. [Получение топов запросов](#получение-топов-запросов)
4. [Получение динамики](#получение-динамики)
5. [Получение частотности](#получение-частотности)
6. [Фильтры и параметры](#фильтры-и-параметры)
7. [Обработка ошибок](#обработка-ошибок)
8. [Примеры использования](#примеры-использования)

## Введение

**AsyncWordstatClient** предоставляет асинхронный доступ к Yandex Wordstat API через XMLRiver. Позволяет получать:

- **Топы запросов** - похожие и популярные запросы
- **Динамику частотности** - изменение частотности во времени
- **Общую частотность** - количество запросов за период

## Быстрый старт

### Инициализация клиента

```python
import asyncio
from xmlriver_pro import AsyncWordstatClient

async def main():
    async with AsyncWordstatClient(
        user_id=123,
        api_key="your_api_key"
    ) as client:
        # Получение топов запросов
        result = await client.get_words("python")
        print(f"Associations: {len(result.associations)}")
        print(f"Popular: {len(result.popular)}")

asyncio.run(main())
```

### Параметры инициализации

```python
AsyncWordstatClient(
    user_id=123,               # ID пользователя XMLRiver
    api_key="your_key",        # API ключ
    timeout=60,                # Таймаут запроса (по умолчанию 60 сек)
    max_retries=3,             # Максимум попыток повтора (по умолчанию 3)
    retry_delay=1.0,           # Задержка между попытками (по умолчанию 1.0 сек)
    enable_retry=True,         # Включить автоматические повторы (по умолчанию True)
    max_concurrent=10,         # Максимум одновременных запросов (по умолчанию 10)
)
```

## Получение топов запросов

Метод `get_words()` возвращает похожие (associations) и популярные (popular) запросы.

### Базовый пример

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    result = await client.get_words("купить телефон")
    
    # Похожие запросы (associations)
    print("Похожие запросы:")
    for keyword in result.associations[:10]:
        print(f"  {keyword.text}: {keyword.value}")
    
    # Популярные запросы (popular)
    print("\nПопулярные запросы:")
    for keyword in result.popular:
        print(f"  {keyword.text}: {keyword.value}")
```

### С фильтрами

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # Фильтр по региону (213 = Москва)
    result = await client.get_words(
        "купить телефон",
        regions=213
    )
    
    # Фильтр по устройству
    result = await client.get_words(
        "купить телефон",
        device="desktop"  # или "phone", "tablet"
    )
    
    # Несколько устройств
    result = await client.get_words(
        "купить телефон",
        device="desktop,phone"
    )
```

## Получение динамики

Метод `get_history()` возвращает изменение частотности запроса во времени.

### Базовый пример

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    result = await client.get_history("купить телефон")
    
    print(f"Общая частотность: {result.total_value}")
    print("\nДинамика:")
    for point in result.history:
        print(f"  {point.date}: {point.absolute_value}")
```

### С периодами

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # По месяцам (минимум 3 месяца)
    result = await client.get_history(
        "купить телефон",
        period="month",
        start="01.01.2024",
        end="31.03.2024"
    )
    
    # По неделям (минимум 3 недели)
    result = await client.get_history(
        "купить телефон",
        period="week",
        start="01.01.2024",  # Понедельник
        end="21.01.2024"     # Воскресенье
    )
    
    # По дням (минимум 3 дня, end не может быть текущим днём!)
    result = await client.get_history(
        "купить телефон",
        period="day",
        start="01.01.2024",
        end="05.01.2024"
    )
```

### Анализ динамики

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    result = await client.get_history(
        "купить телефон",
        period="month",
        start="01.01.2024",
        end="31.12.2024"
    )
    
    # График динамики
    import matplotlib.pyplot as plt
    
    dates = [point.date for point in result.history]
    values = [point.absolute_value for point in result.history]
    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o')
    plt.title(f'Динамика запроса "{result.query}"')
    plt.xlabel('Период')
    plt.ylabel('Частотность')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

## Получение частотности

Метод `get_frequency()` - упрощённый способ получить общую частотность запроса.

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # Общая частотность
    frequency = await client.get_frequency("купить телефон")
    print(f"Частотность: {frequency}")
    
    # С фильтрами
    frequency = await client.get_frequency(
        "купить телефон",
        regions=213,
        device="desktop"
    )
    print(f"Частотность в Москве на desktop: {frequency}")
```

## Фильтры и параметры

### Регионы

Используйте ID региона Яндекса:

```python
# Популярные регионы
REGIONS = {
    "Россия": 225,
    "Москва": 213,
    "Санкт-Петербург": 2,
    "Киев": 143,
    "Минск": 157,
}

async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    result = await client.get_words("купить телефон", regions=REGIONS["Москва"])
```

Полный список регионов: [Яндекс.Регионы](https://tech.yandex.ru/xml/doc/dg/reference/regions-docpage/)

### Устройства

Поддерживаемые устройства:

- `"desktop"` - десктопы
- `"phone"` - телефоны
- `"tablet"` - планшеты
- `"desktop,phone"` - несколько устройств через запятую

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # Только desktop
    result = await client.get_words("купить телефон", device="desktop")
    
    # Desktop и phone
    result = await client.get_words("купить телефон", device="desktop,phone")
    
    # Все устройства (по умолчанию)
    result = await client.get_words("купить телефон")
```

### Периоды для динамики

| Период | Минимум | Требования к датам |
|--------|---------|-------------------|
| `month` | 3 месяца | start - первое число месяца, end - последнее число месяца |
| `week` | 3 недели | start - понедельник, end - воскресенье |
| `day` | 3 дня | end не может быть текущим днём |

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # Правильно
    result = await client.get_history(
        "купить телефон",
        period="month",
        start="01.01.2024",  # Первое число
        end="31.03.2024"     # Последнее число, минимум 3 месяца
    )
    
    # Неправильно - ошибка 400
    result = await client.get_history(
        "купить телефон",
        period="month",
        start="05.01.2024",  # НЕ первое число!
        end="05.02.2024"     # Меньше 3 месяцев
    )
```

## Обработка ошибок

```python
from xmlriver_pro import AsyncWordstatClient
from xmlriver_pro.core import (
    ValidationError,
    AuthenticationError,
    RateLimitError,
    InsufficientFundsError,
    ServiceUnavailableError,
    NetworkError,
)

async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    try:
        result = await client.get_words("купить телефон")
    
    except ValidationError as e:
        # Код 2: пустой запрос
        # Код 400: неверный период или другие параметры
        print(f"Ошибка валидации: {e}")
    
    except AuthenticationError as e:
        # Код 31: пользователь не зарегистрирован
        # Код 42: неверный ключ
        # Код 45: доступ запрещён с вашего IP
        print(f"Ошибка аутентификации: {e}")
    
    except RateLimitError as e:
        # Код 110: нет свободных каналов
        # Код 115: слишком частые запросы
        print(f"Превышен лимит запросов: {e}")
        await asyncio.sleep(10)  # Подождите перед повтором
    
    except InsufficientFundsError as e:
        # Код 200: закончились деньги
        print(f"Недостаточно средств: {e}")
    
    except ServiceUnavailableError as e:
        # Код 101: сервис на обслуживании
        # Код 121: неверный request id
        print(f"Сервис недоступен: {e}")
    
    except NetworkError as e:
        # Код 500: сетевая ошибка
        print(f"Сетевая ошибка: {e}")
```

## Примеры использования

### Анализ конкурентов

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    query = "купить айфон"
    result = await client.get_words(query)
    
    print(f"Анализ запроса: {query}")
    print(f"Похожих запросов: {len(result.associations)}")
    
    # Топ-10 самых популярных похожих запросов
    sorted_associations = sorted(
        result.associations,
        key=lambda x: x.value,
        reverse=True
    )
    
    print("\nТоп-10 похожих запросов:")
    for i, keyword in enumerate(sorted_associations[:10], 1):
        print(f"{i}. {keyword.text}: {keyword.value}")
```

### Сезонность запросов

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # Получаем данные за год
    result = await client.get_history(
        "купить кондиционер",
        period="month",
        start="01.01.2024",
        end="31.12.2024"
    )
    
    # Анализируем сезонность
    max_value = max(point.absolute_value for point in result.history)
    min_value = min(point.absolute_value for point in result.history)
    
    print(f"Сезонность запроса '{result.query}':")
    print(f"Максимум: {max_value}")
    print(f"Минимум: {min_value}")
    print(f"Разница: {max_value - min_value} ({(max_value/min_value - 1)*100:.1f}%)")
```

### Сбор семантического ядра

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    base_queries = ["купить телефон", "смартфон", "мобильный телефон"]
    all_keywords = set()
    
    for query in base_queries:
        result = await client.get_words(query)
        
        for keyword in result.associations:
            if keyword.value >= 100:  # Минимальная частотность
                all_keywords.add(keyword.text)
    
    print(f"Собрано уникальных запросов: {len(all_keywords)}")
    print("\nПримеры:")
    for keyword in list(all_keywords)[:20]:
        print(f"  - {keyword}")
```

### Параллельная обработка запросов

```python
async with AsyncWordstatClient(user_id=123, api_key="key", max_concurrent=5) as client:
    queries = [
        "купить телефон",
        "купить ноутбук",
        "купить планшет",
        "купить наушники",
        "купить зарядку",
    ]
    
    # Создаём задачи
    tasks = [client.get_frequency(query) for query in queries]
    
    # Выполняем параллельно (максимум 5 одновременно)
    results = await asyncio.gather(*tasks)
    
    # Выводим результаты
    for query, frequency in zip(queries, results):
        print(f"{query}: {frequency}")
```

### Мониторинг запросов

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # Проверяем статус семафора
    status = client.get_concurrent_status()
    print(f"Активных запросов: {status['active_requests']}")
    print(f"Максимум запросов: {status['max_concurrent']}")
    print(f"Доступных слотов: {status['available_slots']}")
    
    # Проверяем баланс
    balance = await client.get_balance()
    print(f"Баланс: {balance} руб.")
```

## Полезные советы

### 1. Оптимизация запросов

```python
# Плохо - много запросов
for query in queries:
    result = await client.get_words(query)
    process(result)

# Хорошо - параллельная обработка
tasks = [client.get_words(query) for query in queries]
results = await asyncio.gather(*tasks)
for result in results:
    process(result)
```

### 2. Кэширование результатов

```python
import json
from pathlib import Path

cache_dir = Path("cache")
cache_dir.mkdir(exist_ok=True)

async def get_words_cached(client, query):
    cache_file = cache_dir / f"{query}.json"
    
    if cache_file.exists():
        # Загружаем из кэша
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return WordstatResponse(**data)
    
    # Запрашиваем у API
    result = await client.get_words(query)
    
    # Сохраняем в кэш
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({
            "query": result.query,
            "associations": [{"text": k.text, "value": k.value, "is_association": k.is_association}
                           for k in result.associations],
            "popular": [{"text": k.text, "value": k.value, "is_association": k.is_association}
                       for k in result.popular],
        }, f, ensure_ascii=False, indent=2)
    
    return result
```

### 3. Обработка амперсандов

```python
# Библиотека автоматически заменяет & на %26
query = "black & white"
result = await client.get_words(query)  # Отправляется как "black %26 white"
```

---

**Подробнее:**
- [API Reference](API_REFERENCE.md)
- [Examples](examples.md)
- [Troubleshooting](TROUBLESHOOTING.md)

