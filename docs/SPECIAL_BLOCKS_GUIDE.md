# Руководство по специальным блокам

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md)

Подробное руководство по использованию специальных блоков Google и Yandex.

## Содержание

- [Google Special Blocks](#google-special-blocks)
- [Yandex Special Blocks](#yandex-special-blocks)
- [Сравнение блоков](#сравнение-блоков)
- [Примеры использования](#примеры-использования)

## Google Special Blocks

### Инициализация

```python
from xmlriver_pro import GoogleSpecialBlocks

special = GoogleSpecialBlocks(user_id=123, api_key="your_key")
```

### OneBox документы

OneBox - это специальные блоки Google, которые отображают структурированную информацию.

```python
# Получение OneBox документов
onebox_docs = special.get_onebox_documents(
    query="python programming",
    types=["organic", "video", "images", "news"]
)

for doc in onebox_docs:
    print(f"Тип: {doc.doc_type}")
    print(f"Заголовок: {doc.title}")
    print(f"URL: {doc.url}")
    print(f"Описание: {doc.snippet}")
    print("---")
```

### Knowledge Graph

Граф знаний Google предоставляет структурированную информацию о сущностях.

```python
# Получение информации из графа знаний
kg = special.get_knowledge_graph("Python programming language")

if kg:
    print(f"Сущность: {kg.entity_name}")
    print(f"Описание: {kg.description}")
    if kg.image_url:
        print(f"Изображение: {kg.image_url}")
else:
    print("Информация не найдена")
```

### Связанные поиски

Получение связанных поисковых запросов.

```python
# Получение связанных поисков
related_searches = special.get_related_searches("python programming")

for search in related_searches:
    print(f"Запрос: {search.query}")
    print(f"URL: {search.url}")
    print("---")
```

### Блок ответов

Блок с прямым ответом на вопрос.

```python
# Получение блока ответов
answer_box = special.get_answer_box("What is Python?")

if answer_box:
    print(f"Ответ: {answer_box['answer']}")
    print(f"Источник: {answer_box['source']}")
else:
    print("Прямой ответ не найден")
```

### Калькулятор

Выполнение математических вычислений.

```python
# Использование калькулятора
calc_result = special.get_calculator("2 + 2 * 3")

if calc_result:
    print(f"Выражение: {calc_result['expression']}")
    print(f"Результат: {calc_result['result']}")
else:
    print("Вычисление не выполнено")
```

### Переводчик

Перевод текста.

```python
# Использование переводчика
translation = special.get_translator("Hello world")

if translation:
    print(f"Оригинал: {translation['original_text']}")
    print(f"Перевод: {translation['translation']}")
else:
    print("Перевод не выполнен")
```

### Погода

Получение информации о погоде.

```python
# Получение информации о погоде
weather = special.get_weather("weather Moscow")

if weather:
    print(f"Местоположение: {weather['location']}")
    print(f"Погода: {weather['weather_info']}")
else:
    print("Информация о погоде не найдена")
```

### Конвертер валют

Конвертация валют.

```python
# Конвертация валют
currency = special.get_currency_converter("100 USD to EUR")

if currency:
    print(f"Запрос: {currency['conversion_query']}")
    print(f"Результат: {currency['result']}")
else:
    print("Конвертация не выполнена")
```

### Время

Получение информации о времени в разных часовых поясах.

```python
# Получение информации о времени
time_info = special.get_time("time in Moscow")

if time_info:
    print(f"Местоположение: {time_info['location_query']}")
    print(f"Время: {time_info['time_info']}")
else:
    print("Информация о времени не найдена")
```

## Yandex Special Blocks

### Инициализация

```python
from xmlriver_pro import YandexSpecialBlocks

special = YandexSpecialBlocks(user_id=123, api_key="your_key")
```

### Колдунщики поиска

Колдунщики - это специальные блоки Yandex с различными функциями.

```python
# Получение колдунщиков
searchsters = special.get_searchsters(
    query="python programming",
    types=["organic", "calculator", "weather", "translate"]
)

for searchster in searchsters:
    print(f"Тип: {searchster.searchster_type}")
    print(f"Заголовок: {searchster.title}")
    print(f"URL: {searchster.url}")
    print(f"Описание: {searchster.snippet}")
    print("---")
```

### Погода

Получение информации о погоде.

```python
# Получение информации о погоде
weather = special.get_weather("погода Москва")

if weather:
    print(f"Местоположение: {weather['location']}")
    print(f"Погода: {weather['weather_info']}")
else:
    print("Информация о погоде не найдена")
```

### Калькулятор

Выполнение математических вычислений.

```python
# Использование калькулятора
calc_result = special.get_calculator("2 + 2 * 3")

if calc_result:
    print(f"Выражение: {calc_result['expression']}")
    print(f"Результат: {calc_result['result']}")
else:
    print("Вычисление не выполнено")
```

### Переводчик

Перевод текста.

```python
# Использование переводчика
translation = special.get_translator("Hello world")

if translation:
    print(f"Оригинал: {translation['original_text']}")
    print(f"Перевод: {translation['translation']}")
else:
    print("Перевод не выполнен")
```

### Конвертер валют

Конвертация валют.

```python
# Конвертация валют
currency = special.get_currency_converter("100 долларов в рубли")

if currency:
    print(f"Запрос: {currency['conversion_query']}")
    print(f"Результат: {currency['result']}")
else:
    print("Конвертация не выполнена")
```

### Время

Получение информации о времени в разных часовых поясах.

```python
# Получение информации о времени
time_info = special.get_time("время в Москве")

if time_info:
    print(f"Местоположение: {time_info['location_query']}")
    print(f"Время: {time_info['time_info']}")
else:
    print("Информация о времени не найдена")
```

### IP адрес

Получение информации о IP адресе.

```python
# Получение информации об IP адресе
ip_info = special.get_ip_address()

if ip_info:
    print(f"IP адрес: {ip_info['ip_info']}")
else:
    print("Информация об IP адресе не найдена")
```

### Карты

Получение информации о картах и местоположениях.

```python
# Получение информации о картах
maps_info = special.get_maps("кафе Москва")

if maps_info:
    print(f"Местоположение: {maps_info['location_query']}")
    print(f"Информация: {maps_info['maps_info']}")
else:
    print("Информация о картах не найдена")
```

### Музыка

Получение информации о музыке.

```python
# Получение информации о музыке
music_info = special.get_music("python programming music")

if music_info:
    print(f"Запрос: {music_info['music_query']}")
    print(f"Информация: {music_info['music_info']}")
else:
    print("Информация о музыке не найдена")
```

### Текст песни

Получение текста песни.

```python
# Получение текста песни
lyrics = special.get_lyrics("python song lyrics")

if lyrics:
    print(f"Песня: {lyrics['song_query']}")
    print(f"Текст: {lyrics['lyrics']}")
else:
    print("Текст песни не найден")
```

### Цитаты

Получение цитат по теме.

```python
# Получение цитат
quotes = special.get_quotes("python programming quotes")

if quotes:
    print(f"Запрос: {quotes['quotes_query']}")
    print(f"Цитаты: {quotes['quotes']}")
else:
    print("Цитаты не найдены")
```

### Факты

Получение интересных фактов по теме.

```python
# Получение фактов
facts = special.get_facts("python programming facts")

if facts:
    print(f"Запрос: {facts['fact_query']}")
    print(f"Факты: {facts['facts']}")
else:
    print("Факты не найдены")
```

### Связанные поиски

Получение связанных поисковых запросов.

```python
# Получение связанных поисков
related_searches = special.get_related_searches("python programming")

for search in related_searches:
    print(f"Запрос: {search.query}")
    print(f"URL: {search.url}")
    print("---")
```

## Сравнение блоков

### Доступность функций

| Функция | Google | Yandex |
|---------|--------|--------|
| OneBox документы | ✅ | ❌ |
| Knowledge Graph | ✅ | ❌ |
| Калькулятор | ✅ | ✅ |
| Переводчик | ✅ | ✅ |
| Погода | ✅ | ✅ |
| Конвертер валют | ✅ | ✅ |
| Время | ✅ | ✅ |
| Блок ответов | ✅ | ❌ |
| IP адрес | ❌ | ✅ |
| Карты | ❌ | ✅ |
| Музыка | ❌ | ✅ |
| Текст песни | ❌ | ✅ |
| Цитаты | ❌ | ✅ |
| Факты | ❌ | ✅ |
| Колдунщики | ❌ | ✅ |

### Особенности использования

#### Google Special Blocks
- **OneBox документы**: Структурированная информация в различных форматах
- **Knowledge Graph**: Авторитетная информация о сущностях
- **Блок ответов**: Прямые ответы на вопросы
- **Универсальность**: Подходит для широкого круга запросов

#### Yandex Special Blocks
- **Колдунщики**: Специализированные блоки для конкретных задач
- **Локализация**: Оптимизированы для русскоязычных запросов
- **Разнообразие**: Больше типов специальных блоков
- **Специализация**: Каждый блок решает конкретную задачу

## Примеры использования

### Комплексный анализ запроса

```python
def analyze_query_comprehensive(query):
    """Комплексный анализ запроса с использованием всех блоков"""
    results = {}
    
    # Google анализ
    google_special = GoogleSpecialBlocks(user_id=123, api_key="your_google_key")
    
    # OneBox документы
    onebox_docs = google_special.get_onebox_documents(query, ["organic", "video", "images"])
    results["google_onebox"] = onebox_docs
    
    # Knowledge Graph
    kg = google_special.get_knowledge_graph(query)
    results["google_kg"] = kg
    
    # Блок ответов
    answer_box = google_special.get_answer_box(query)
    results["google_answer"] = answer_box
    
    # Yandex анализ
    yandex_special = YandexSpecialBlocks(user_id=123, api_key="your_yandex_key")
    
    # Колдунщики
    searchsters = yandex_special.get_searchsters(query, ["organic", "calculator", "weather"])
    results["yandex_searchsters"] = searchsters
    
    # Специальные блоки
    weather = yandex_special.get_weather(f"погода {query}")
    results["yandex_weather"] = weather
    
    return results

# Использование
query = "python programming"
analysis = analyze_query_comprehensive(query)

print("=== Анализ запроса ===")
print(f"Запрос: {query}")
print()

if analysis["google_onebox"]:
    print(f"Google OneBox: {len(analysis['google_onebox'])} документов")
    
if analysis["google_kg"]:
    print(f"Google Knowledge Graph: {analysis['google_kg'].entity_name}")
    
if analysis["google_answer"]:
    print(f"Google Answer Box: {analysis['google_answer']['answer'][:100]}...")
    
if analysis["yandex_searchsters"]:
    print(f"Yandex Колдунщики: {len(analysis['yandex_searchsters'])} блоков")
    
if analysis["yandex_weather"]:
    print(f"Yandex Погода: {analysis['yandex_weather']['weather_info']}")
```

### Асинхронный анализ

```python
async def async_analyze_query(query):
    """Асинхронный анализ запроса"""
    results = {}
    
    async with GoogleSpecialBlocks(user_id=123, api_key="your_google_key") as google_special, \
             YandexSpecialBlocks(user_id=123, api_key="your_yandex_key") as yandex_special:
        
        # Создаем задачи для параллельного выполнения
        tasks = [
            google_special.get_onebox_documents(query, ["organic", "video"]),
            google_special.get_knowledge_graph(query),
            google_special.get_answer_box(query),
            yandex_special.get_searchsters(query, ["organic", "calculator"]),
            yandex_special.get_weather(f"погода {query}")
        ]
        
        # Выполняем все задачи параллельно
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        results["onebox"] = results_list[0] if not isinstance(results_list[0], Exception) else None
        results["kg"] = results_list[1] if not isinstance(results_list[1], Exception) else None
        results["answer"] = results_list[2] if not isinstance(results_list[2], Exception) else None
        results["searchsters"] = results_list[3] if not isinstance(results_list[3], Exception) else None
        results["weather"] = results_list[4] if not isinstance(results_list[4], Exception) else None
    
    return results

# Использование
async def main():
    query = "python programming"
    analysis = await async_analyze_query(query)
    
    print("=== Асинхронный анализ ===")
    for key, value in analysis.items():
        if value:
            print(f"{key}: найдено")
        else:
            print(f"{key}: не найдено")

asyncio.run(main())
```

### Обработка ошибок

```python
def safe_special_block_call(special_client, method_name, *args, **kwargs):
    """Безопасный вызов метода специального блока"""
    try:
        method = getattr(special_client, method_name)
        result = method(*args, **kwargs)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Использование
google_special = GoogleSpecialBlocks(user_id=123, api_key="your_google_key")

# Безопасный вызов
result = safe_special_block_call(google_special, "get_calculator", "2 + 2")

if result["success"]:
    print(f"Результат: {result['result']}")
else:
    print(f"Ошибка: {result['error']}")
```

### Кэширование результатов

```python
import pickle
import os
from datetime import datetime, timedelta

class SpecialBlocksCache:
    """Кэш для результатов специальных блоков"""
    
    def __init__(self, cache_dir="special_cache", ttl_hours=6):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.pkl")
    
    def _is_expired(self, cache_path):
        if not os.path.exists(cache_path):
            return True
        
        mtime = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - mtime > self.ttl
    
    def get(self, key):
        """Получить результат из кэша"""
        cache_path = self._get_cache_path(key)
        
        if self._is_expired(cache_path):
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None
    
    def set(self, key, value):
        """Сохранить результат в кэш"""
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            print(f"Ошибка сохранения в кэш: {e}")

# Использование с кэшем
cache = SpecialBlocksCache()

def cached_special_block(special_client, method_name, query, *args, **kwargs):
    """Специальный блок с кэшированием"""
    cache_key = f"{method_name}_{query}_{hash(str(args) + str(kwargs))}"
    
    # Проверяем кэш
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        print(f"Результат из кэша: {method_name}({query})")
        return cached_result
    
    # Выполняем запрос
    method = getattr(special_client, method_name)
    result = method(query, *args, **kwargs)
    
    # Сохраняем в кэш
    cache.set(cache_key, result)
    print(f"Результат сохранен в кэш: {method_name}({query})")
    
    return result

# Использование
google_special = GoogleSpecialBlocks(user_id=123, api_key="your_google_key")

# Первый вызов - из API
result1 = cached_special_block(google_special, "get_calculator", "2 + 2")

# Второй вызов - из кэша
result2 = cached_special_block(google_special, "get_calculator", "2 + 2")
```

---

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md) • [Продвинутое использование](ADVANCED_USAGE.md)
