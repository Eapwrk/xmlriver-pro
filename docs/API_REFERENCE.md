# API Reference - XMLRiver Pro

[← Назад к README](../README.md) • [Документация](README.md)

## Содержание

1. [Асинхронные клиенты](#асинхронные-клиенты)
   - [AsyncGoogleClient](#asyncgoogleclient)
   - [AsyncYandexClient](#asyncyandexclient)
   - [AsyncWordstatClient](#asyncwordstatclient)
2. [Типы данных](#типы-данных)
3. [Исключения](#исключения)
4. [Утилиты](#утилиты)

## Асинхронные клиенты

### AsyncGoogleClient

Асинхронный клиент для работы с Google Search API через XMLRiver.

#### Инициализация

```python
from xmlriver_pro import AsyncGoogleClient

async with AsyncGoogleClient(
    user_id=123,
    api_key="your_key",
    timeout=60,
    max_retries=3,
    retry_delay=1.0,
    max_concurrent=10
) as client:
    # Ваш код
    pass
```

**Параметры:**
- `user_id` (int): ID пользователя XMLRiver
- `api_key` (str): API ключ
- `timeout` (int, optional): Таймаут в секундах (по умолчанию: 60)
- `max_retries` (int, optional): Максимум попыток (по умолчанию: 3)
- `retry_delay` (float, optional): Задержка между попытками (по умолчанию: 1.0)
- `max_concurrent` (int, optional): Максимум одновременных запросов (по умолчанию: 10)

#### Методы

##### `search(query, **kwargs)`

Асинхронный органический поиск в Google.

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    results = await client.search(
        query="python programming",
        num_results=10,
        start=0,
        device=DeviceType.DESKTOP,
        country=225  # Россия
    )
```

**Параметры:**
- `query` (str): Поисковый запрос
- `num_results` (int, optional): Количество результатов (по умолчанию: 10)
- `start` (int, optional): Начальная позиция (по умолчанию: 0)
- `device` (DeviceType, optional): Тип устройства
- `os` (OSType, optional): Операционная система
- `country` (int, optional): ID страны

**Возвращает:** `SearchResponse`

##### `search_news(query, **kwargs)`

Асинхронный поиск новостей в Google.

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    results = await client.search_news(
        query="python news",
        num_results=10,
        time_filter=TimeFilter.LAST_WEEK
    )
```

**Параметры:**
- `query` (str): Поисковый запрос
- `num_results` (int, optional): Количество результатов
- `time_filter` (TimeFilter, optional): Фильтр по времени

**Возвращает:** `SearchResponse`

##### `search_images(query, **kwargs)`

Асинхронный поиск изображений в Google.

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    results = await client.search_images(
        query="python logo",
        num_results=20,
        size="large",
        color="color"
    )
```

**Параметры:**
- `query` (str): Поисковый запрос
- `num_results` (int, optional): Количество результатов
- `size` (str, optional): Размер изображений (large, medium, small)
- `color` (str, optional): Цвет (color, grayscale, transparent)
- `image_type` (str, optional): Тип (photo, clipart, lineart)

**Возвращает:** `SearchResponse`

##### `search_maps(query, **kwargs)`

Асинхронный поиск по картам Google.

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    results = await client.search_maps(
        query="python office",
        coords=(37.7749, -122.4194),
        zoom=12
    )
```

**Параметры:**
- `query` (str): Поисковый запрос
- `coords` (tuple, optional): Координаты (широта, долгота)
- `zoom` (int, optional): Уровень масштабирования

**Возвращает:** `SearchResponse`

##### `get_ads(query, **kwargs)`

Асинхронное получение рекламных блоков Google.

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    results = await client.get_ads("python programming", num_results=10)
```

**Параметры:**
- `query` (str): Поисковый запрос
- `num_results` (int, optional): Количество результатов

**Возвращает:** `SearchResponse`

##### `get_special_blocks(query, **kwargs)`

Асинхронное получение специальных блоков Google (OneBox, Knowledge Graph).

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    results = await client.get_special_blocks("python programming")
```

**Параметры:**
- `query` (str): Поисковый запрос

**Возвращает:** `SearchResponse`

##### `get_balance()`

Асинхронное получение текущего баланса счета XMLRiver.

Баланс единый для всего аккаунта (Google, Yandex, Wordstat).

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    balance = await client.get_balance()
    print(f"Баланс: {balance:.2f} руб.")
```

**Возвращает:** `float` - баланс в рублях

##### `get_cost()`

Асинхронное получение стоимости запросов для Google.

Стоимость зависит от системы поиска (Google/Yandex/Wordstat).

```python
async with AsyncGoogleClient(user_id=123, api_key="key") as client:
    cost = await client.get_cost()
    print(f"Стоимость: {cost:.2f} руб/1000 запросов")
```

**Возвращает:** `float` - стоимость за 1000 запросов в рублях

---

### AsyncYandexClient

Асинхронный клиент для работы с Yandex Search API через XMLRiver.

#### Инициализация

```python
from xmlriver_pro import AsyncYandexClient

async with AsyncYandexClient(
    user_id=123,
    api_key="your_key",
    timeout=60,
    max_retries=3,
    retry_delay=1.0,
    max_concurrent=10
) as client:
    # Ваш код
    pass
```

**Параметры:** аналогичны AsyncGoogleClient

#### Методы

##### `search(query, **kwargs)`

Асинхронный органический поиск в Yandex.

```python
async with AsyncYandexClient(user_id=123, api_key="key") as client:
    results = await client.search(
        query="программирование python",
        num_results=10,
        lr=213,  # Москва
        lang="ru",
        domain="ru"
    )
```

**Параметры:**
- `query` (str): Поисковый запрос
- `num_results` (int, optional): Количество результатов
- `lr` (int, optional): ID региона Яндекса
- `lang` (str, optional): Код языка (ru, uk, etc.)
- `domain` (str, optional): Домен Яндекса (ru, com, ua, etc.)

**Возвращает:** `SearchResponse`

##### `search_news(query, **kwargs)`

Асинхронный поиск новостей в Yandex.

```python
async with AsyncYandexClient(user_id=123, api_key="key") as client:
    results = await client.search_news("python новости")
```

**Возвращает:** `SearchResponse`

##### `get_ads(query, **kwargs)`

Асинхронное получение рекламных блоков Yandex.

```python
async with AsyncYandexClient(user_id=123, api_key="key") as client:
    results = await client.get_ads("программирование python")
```

**Возвращает:** `SearchResponse`

##### `get_special_blocks(query, **kwargs)`

Асинхронное получение специальных блоков Yandex (колдунщики).

```python
async with AsyncYandexClient(user_id=123, api_key="key") as client:
    results = await client.get_special_blocks("погода москва")
```

**Возвращает:** `SearchResponse`

##### `get_balance()`

Асинхронное получение текущего баланса счета XMLRiver.

Баланс единый для всего аккаунта (Google, Yandex, Wordstat).

```python
async with AsyncYandexClient(user_id=123, api_key="key") as client:
    balance = await client.get_balance()
    print(f"Баланс: {balance:.2f} руб.")
```

**Возвращает:** `float` - баланс в рублях

##### `get_cost()`

Асинхронное получение стоимости запросов для Yandex.

Стоимость зависит от системы поиска (Google/Yandex/Wordstat).

```python
async with AsyncYandexClient(user_id=123, api_key="key") as client:
    cost = await client.get_cost()
    print(f"Стоимость: {cost:.2f} руб/1000 запросов")
```

**Возвращает:** `float` - стоимость за 1000 запросов в рублях

---

### AsyncWordstatClient

Асинхронный клиент для работы с Yandex Wordstat API через XMLRiver.

#### Инициализация

```python
from xmlriver_pro import AsyncWordstatClient

async with AsyncWordstatClient(
    user_id=123,
    api_key="your_key",
    timeout=60,
    max_retries=3,
    retry_delay=1.0
) as client:
    # Ваш код
    pass
```

**Параметры:** аналогичны AsyncGoogleClient

#### Методы

##### `get_words(query, **kwargs)`

Асинхронное получение топов запросов (associations и popular).

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    result = await client.get_words(
        query="купить телефон",
        regions=213,  # Москва
        device="desktop",
        limit=100
    )
    
    print(f"Associations: {len(result.associations)}")
    print(f"Popular: {len(result.popular)}")
    
    for kw in result.associations[:5]:
        print(f"{kw.text}: {kw.value}")
```

**Параметры:**
- `query` (str): Поисковый запрос
- `regions` (int | list, optional): ID региона/регионов Яндекса
- `device` (str, optional): Тип устройства ("desktop", "phone", "tablet")
- `limit` (int, optional): Количество результатов

**Возвращает:** `WordstatResponse`

##### `get_history(query, **kwargs)`

Асинхронное получение динамики частотности запроса.

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    history = await client.get_history(
        query="купить телефон",
        regions=213,
        device="desktop",
        period="month",
        start="01.01.2024",
        end="31.03.2024"
    )
    
    print(f"Total frequency: {history.total_value}")
    for point in history.history:
        print(f"{point.date}: {point.absolute_value}")
```

**Параметры:**
- `query` (str): Поисковый запрос
- `regions` (int | list, optional): ID региона/регионов Яндекса
- `device` (str, optional): Тип устройства
- `period` (str, optional): Период группировки ("month", "week", "day")
- `start` (str, optional): Дата начала (dd.mm.yyyy)
- `end` (str, optional): Дата окончания (dd.mm.yyyy)

**Возвращает:** `WordstatHistoryResponse`

##### `get_frequency(query, **kwargs)`

Асинхронное получение общей частотности запроса (быстрый метод).

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    frequency = await client.get_frequency(
        query="купить телефон",
        regions=213,
        device="desktop"
    )
    print(f"Frequency: {frequency}")
```

**Параметры:**
- `query` (str): Поисковый запрос
- `regions` (int | list, optional): ID региона/регионов Яндекса
- `device` (str, optional): Тип устройства

**Возвращает:** `int` - частотность запроса

##### `get_balance()`

Асинхронное получение текущего баланса счета XMLRiver.

Баланс единый для всего аккаунта (Google, Yandex, Wordstat).

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    balance = await client.get_balance()
    print(f"Баланс: {balance:.2f} руб.")
```

**Возвращает:** `float` - баланс в рублях

##### `get_cost()`

Асинхронное получение стоимости запросов для Wordstat.

Стоимость зависит от системы поиска (Google/Yandex/Wordstat).

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    cost = await client.get_cost()
    print(f"Стоимость: {cost:.2f} руб/1000 запросов")
```

**Возвращает:** `float` - стоимость за 1000 запросов в рублях

#### Операторы Wordstat

AsyncWordstatClient поддерживает все операторы Yandex Wordstat:

```python
async with AsyncWordstatClient(user_id=123, api_key="key") as client:
    # Точная форма слова
    freq = await client.get_frequency('"купить телефон"')
    
    # Исключение слова
    freq = await client.get_frequency('купить телефон -айфон')
    
    # ИЛИ
    freq = await client.get_frequency('купить (телефон | смартфон)')
```

**Поддерживаемые операторы:**
- `"слово"` - точная форма слова
- `[слово]` - фиксация порядка слов
- `!слово` - точное вхождение
- `-слово` - исключение слова
- `слово1 | слово2` - ИЛИ
- `+слово` - обязательное слово

**См. также:** [WORDSTAT_GUIDE.md](WORDSTAT_GUIDE.md) - полное руководство по Wordstat API

---

## Типы данных

### SearchResponse

Результат поискового запроса.

**Атрибуты:**
- `query` (str): Исходный запрос
- `total_results` (int): Общее количество результатов
- `results` (List[SearchResult]): Список результатов
- `found` (int, optional): Количество найденных результатов

### SearchResult

Результат органического поиска.

**Атрибуты:**
- `rank` (int): Позиция в результатах
- `url` (str): URL страницы
- `title` (str): Заголовок
- `snippet` (str): Описание

### NewsResult

Результат поиска новостей.

**Атрибуты:**
- `rank` (int): Позиция
- `url` (str): URL новости
- `title` (str): Заголовок
- `snippet` (str): Описание
- `media` (str, optional): Источник новости
- `pub_date` (str, optional): Дата публикации

### ImageResult

Результат поиска изображений.

**Атрибуты:**
- `rank` (int): Позиция
- `url` (str): URL страницы
- `img_url` (str): URL изображения
- `title` (str): Заголовок
- `display_link` (str, optional): Отображаемая ссылка
- `original_width` (int, optional): Ширина
- `original_height` (int, optional): Высота

### MapResult

Результат поиска по картам.

**Атрибуты:**
- `title` (str): Название места
- `stars` (float, optional): Рейтинг
- `type` (str, optional): Тип места
- `address` (str, optional): Адрес
- `url` (str, optional): URL на карте
- `latitude` (float, optional): Широта
- `longitude` (float, optional): Долгота

### AdResult

Рекламный результат.

**Атрибуты:**
- `url` (str): URL рекламодателя
- `ads_url` (str): Рекламный URL
- `title` (str): Заголовок
- `snippet` (str): Описание

### WordstatResponse

Ответ Wordstat API с топами запросов.

**Атрибуты:**
- `query` (str): Исходный запрос
- `associations` (List[WordstatKeyword]): Список похожих запросов
- `popular` (List[WordstatKeyword]): Список популярных запросов

### WordstatHistoryResponse

Ответ Wordstat API с динамикой запроса.

**Атрибуты:**
- `query` (str): Исходный запрос
- `total_value` (int): Общая частотность
- `history` (List[WordstatHistoryPoint]): История по периодам
- `associations` (List[WordstatKeyword]): Список похожих запросов
- `popular` (List[WordstatKeyword]): Список популярных запросов

### WordstatKeyword

Ключевое слово из Wordstat.

**Атрибуты:**
- `text` (str): Текст запроса
- `value` (int): Частотность запроса
- `is_association` (bool): Является ли похожим запросом (True) или популярным (False)

### WordstatHistoryPoint

Точка в динамике Wordstat.

**Атрибуты:**
- `date` (str): Дата в формате "dd.mm.yyyy"
- `absolute_value` (int): Абсолютное значение частотности
- `relative_value` (float, optional): Относительное значение частотности

### Перечисления (Enums)

#### SearchType
- `ORGANIC` - органический поиск
- `NEWS` - новости
- `IMAGES` - изображения
- `MAPS` - карты
- `ADS` - реклама

#### TimeFilter
- `LAST_HOUR` - последний час
- `LAST_DAY` - последний день
- `LAST_WEEK` - последняя неделя
- `LAST_MONTH` - последний месяц
- `LAST_YEAR` - последний год

#### DeviceType
- `DESKTOP` - десктоп
- `MOBILE` - мобильное устройство
- `TABLET` - планшет

#### OSType
- `WINDOWS` - Windows
- `MACOS` - macOS
- `LINUX` - Linux
- `ANDROID` - Android
- `IOS` - iOS

---

## Исключения

### XMLRiverError
Базовое исключение для всех ошибок XMLRiver.

### AuthenticationError
Ошибка аутентификации (коды 31, 42, 45).

### RateLimitError
Превышен лимит запросов (коды 110, 111, 115).

### NoResultsError
Результаты не найдены (код 15).

### NetworkError
Ошибка сети (коды 500, 202).

### ValidationError
Ошибка валидации параметров (коды 2, 102-108, 120, 121).

### InsufficientFundsError
Недостаточно средств на балансе (код 200).

### ServiceUnavailableError
Сервис недоступен (коды 101, 201).

---

## Утилиты

### Валидаторы

```python
from xmlriver_pro.utils import (
    validate_coords,
    validate_zoom,
    validate_url,
    validate_query,
    validate_device,
    validate_os
)

# Валидация координат
validate_coords((55.7558, 37.6176))  # True

# Валидация zoom
validate_zoom(12)  # True

# Валидация URL
validate_url("https://python.org")  # True

# Валидация запроса
validate_query("python programming")  # True

# Валидация устройства
validate_device(DeviceType.DESKTOP)  # True

# Валидация ОС
validate_os(OSType.ANDROID)  # True
```

### Форматтеры

```python
from xmlriver_pro.utils import (
    format_search_result,
    format_ads_result,
    format_news_result,
    format_image_result,
    format_map_result
)

# Форматирование результата поиска
formatted = format_search_result(result)

# Форматирование рекламного результата
formatted = format_ads_result(ad_result)

# Форматирование новостного результата
formatted = format_news_result(news_result)

# Форматирование изображения
formatted = format_image_result(image_result)

# Форматирование места на карте
formatted = format_map_result(map_result)
```

---

**Подробнее:**
- [Examples](examples.md) - примеры использования
- [Advanced Usage](ADVANCED_USAGE.md) - продвинутые техники
- [Troubleshooting](TROUBLESHOOTING.md) - решение проблем
