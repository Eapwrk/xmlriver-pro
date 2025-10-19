# Руководство по работе с географическими данными

Модуль `geo_data` предоставляет полный набор функций для работы с географическими данными в XMLRiver Pro.

## 📋 Содержание

- [Yandex регионы](#yandex-регионы)
- [Google страны](#google-страны)
- [Google языки](#google-языки)
- [Google домены](#google-домены)
- [Города](#города)
- [Универсальные функции](#универсальные-функции)
- [Примеры использования](#примеры-использования)

## 🗺️ Yandex регионы

### Получение региона по ID
```python
from xmlriver_pro.utils import get_yandex_region

# Получить регион по ID
region = get_yandex_region(213)  # Москва
print(f"Регион: {region.name}, ID: {region.id}")
```

### Поиск регионов по названию
```python
from xmlriver_pro.utils import find_yandex_regions

# Точный поиск
moscow_regions = find_yandex_regions("Москва", exact=True)

# Частичный поиск
moscow_like = find_yandex_regions("Москва", exact=False)
```

### Получение дочерних регионов
```python
from xmlriver_pro.utils import get_yandex_regions_by_parent

# Получить все регионы с родительским ID 1 (Москва и область)
child_regions = get_yandex_regions_by_parent(1)
```

### Иерархия региона
```python
from xmlriver_pro.utils import get_yandex_region_hierarchy

# Получить полную иерархию от корня до указанного региона
hierarchy = get_yandex_region_hierarchy(213)
for region in hierarchy:
    print(f"  {region.name} (ID: {region.id})")
```

## 🌍 Google страны

### Получение страны по коду
```python
from xmlriver_pro.utils import get_google_country

# Получить страну по коду
country = get_google_country("RU")  # Россия
print(f"Страна: {country.name}, Код: {country.code}")
```

### Поиск стран по названию
```python
from xmlriver_pro.utils import find_google_countries

# Поиск стран
russia_countries = find_google_countries("Russia", exact=True)
```

## 🗣️ Google языки

### Получение языка по коду
```python
from xmlriver_pro.utils import get_google_language

# Получить язык по коду
language = get_google_language("ru")  # Русский
print(f"Язык: {language.name}, Код: {language.code}")
```

### Поиск языков по названию
```python
from xmlriver_pro.utils import find_google_languages

# Поиск языков
russian_languages = find_google_languages("Russian", exact=True)
```

### Получение всех языков
```python
from xmlriver_pro.utils import get_all_google_languages

# Получить все доступные языки
all_languages = get_all_google_languages()
for lang in all_languages[:10]:  # Первые 10
    print(f"{lang.code}: {lang.name}")
```

## 🌐 Google домены

### Получение домена по коду
```python
from xmlriver_pro.utils import get_google_domain

# Получить домен по коду
domain = get_google_domain("ru")  # Россия
print(f"Домен: {domain.name}, Код: {domain.code}")
```

### Поиск доменов по названию
```python
from xmlriver_pro.utils import find_google_domains

# Поиск доменов
russia_domains = find_google_domains("Russia", exact=True)
```

### Получение всех доменов
```python
from xmlriver_pro.utils import get_all_google_domains

# Получить все доступные домены
all_domains = get_all_google_domains()
for domain in all_domains:
    print(f"{domain.code}: {domain.name}")
```

## 🏙️ Города

### Получение города по ID
```python
from xmlriver_pro.utils import get_city

# Получить город по ID
city = get_city(1000002)  # Кабул
print(f"Город: {city.name}, Страна: {city.country_code}")
```

### Поиск городов по названию
```python
from xmlriver_pro.utils import find_cities

# Поиск городов
moscow_cities = find_cities("Moscow", exact=True)

# Поиск с фильтром по стране
russia_cities = find_cities("Moscow", country_code="RU", exact=True)
```

### Получение городов по стране
```python
from xmlriver_pro.utils import get_cities_by_country

# Получить все города России
russia_cities = get_cities_by_country("RU")
print(f"Найдено городов в России: {len(russia_cities)}")
```

## 🔍 Универсальные функции

### Универсальный поиск места
```python
from xmlriver_pro.utils import search_place

# Поиск во всех источниках
results = search_place("Moscow")

print("Yandex регионы:")
for region in results["yandex_regions"]:
    print(f"  {region.name} (ID: {region.id})")

print("Google страны:")
for country in results["google_countries"]:
    print(f"  {country.name} ({country.code})")

print("Города:")
for city in results["cities"]:
    print(f"  {city.name} ({city.country_code})")
```

### Получение региона для Yandex поиска
```python
from xmlriver_pro.utils import get_region_for_yandex_search

# Получить ID региона для поиска
region_id = get_region_for_yandex_search("Москва")
if region_id:
    print(f"ID региона для поиска: {region_id}")
```

### Получение кода страны для Google поиска
```python
from xmlriver_pro.utils import get_country_code_for_google_search

# Получить код страны для поиска
country_code = get_country_code_for_google_search("Moscow")
if country_code:
    print(f"Код страны для поиска: {country_code}")
```

### Статистика данных
```python
from xmlriver_pro.utils import get_geo_stats

# Получить статистику загруженных данных
stats = get_geo_stats()
print("Статистика географических данных:")
for key, value in stats.items():
    print(f"  {key}: {value}")
```

## 📚 Примеры использования

### Пример 1: Поиск с региональными настройками
```python
from xmlriver_pro import AsyncYandexClient, AsyncGoogleClient
from xmlriver_pro.utils import get_region_for_yandex_search, get_country_code_for_google_search

# Настройка клиентов
async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex, \
         AsyncGoogleClient(user_id=123, api_key="your_key") as google:
    # Ваш код здесь

# Поиск по региону
place = "Москва"
yandex_region_id = get_region_for_yandex_search(place)
google_country_code = get_country_code_for_google_search(place)

# Поиск в Yandex
if yandex_region_id:
    yandex_results = yandex.search("python программирование", lr=yandex_region_id)

# Поиск в Google
if google_country_code:
    google_results = google.search("python programming", gl=google_country_code)
```

### Пример 2: Массовый поиск по регионам
```python
from xmlriver_pro.utils import get_yandex_regions_by_parent, get_all_google_domains
from xmlriver_pro import AsyncYandexClient, AsyncGoogleClient
import asyncio

async def mass_regional_search():
    async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex, \
             AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        # Ваш код здесь
    
    # Получить все регионы России (ID = 225)
    russia_regions = get_yandex_regions_by_parent(225)
    
    # Получить все домены Google
    google_domains = get_all_google_domains()
    
    # Поиск по регионам
    for region in russia_regions[:5]:  # Первые 5 регионов
        try:
            results = yandex.search("python", lr=region.id)
            print(f"Регион {region.name}: {len(results.results)} результатов")
        except Exception as e:
            print(f"Ошибка в регионе {region.name}: {e}")
    
    # Поиск по доменам Google
    for domain in google_domains[:5]:  # Первые 5 доменов
        try:
            results = google.search("python", gl=domain.code)
            print(f"Домен {domain.name}: {len(results.results)} результатов")
        except Exception as e:
            print(f"Ошибка в домене {domain.name}: {e}")

# Запуск
asyncio.run(mass_regional_search())
```

### Пример 3: Анализ географических данных
```python
from xmlriver_pro.utils import get_geo_stats, get_all_google_languages, get_all_google_domains

# Анализ доступных данных
stats = get_geo_stats()
print("Доступные данные:")
for key, value in stats.items():
    print(f"  {key}: {value:,}")

# Анализ языков
languages = get_all_google_languages()
print(f"\nДоступно языков: {len(languages)}")
print("Популярные языки:")
popular_langs = ["en", "ru", "es", "fr", "de", "zh", "ja", "ko"]
for lang_code in popular_langs:
    lang = next((l for l in languages if l.code == lang_code), None)
    if lang:
        print(f"  {lang.code}: {lang.name}")

# Анализ доменов
domains = get_all_google_domains()
print(f"\nДоступно доменов: {len(domains)}")
print("Основные домены:")
for domain in domains:
    print(f"  {domain.code}: {domain.name}")
```

## 🚀 Интеграция с XMLRiver Pro

### Использование в поисковых запросах
```python
from xmlriver_pro import AsyncYandexClient, AsyncGoogleClient
from xmlriver_pro.utils import (
    get_region_for_yandex_search,
    get_country_code_for_google_search,
    get_google_language,
    get_google_domain
)

def smart_search(query: str, place: str, language: str = "ru"):
    """Умный поиск с автоматическим определением параметров"""
    
    # Определение параметров для Yandex
    yandex_region_id = get_region_for_yandex_search(place)
    
    # Определение параметров для Google
    google_country_code = get_country_code_for_google_search(place)
    google_language = get_google_language(language)
    google_domain = get_google_domain("ru")  # По умолчанию .ru
    
    # Настройка клиентов
    async with AsyncYandexClient(user_id=123, api_key="your_key") as yandex, \
             AsyncGoogleClient(user_id=123, api_key="your_key") as google:
        # Ваш код здесь
    
    results = {}
    
    # Поиск в Yandex
    if yandex_region_id:
        try:
            yandex_results = yandex.search(query, lr=yandex_region_id)
            results["yandex"] = yandex_results
        except Exception as e:
            results["yandex_error"] = str(e)
    
    # Поиск в Google
    if google_country_code and google_language:
        try:
            google_results = google.search(
                query, 
                gl=google_country_code,
                hl=google_language.code
            )
            results["google"] = google_results
        except Exception as e:
            results["google_error"] = str(e)
    
    return results

# Использование
results = smart_search("python программирование", "Москва", "ru")
```

## 📊 Производительность

### Ленивая загрузка
Данные загружаются только при первом обращении к функциям:

```python
# Данные не загружены
from xmlriver_pro.utils import get_geo_stats

# Данные загружаются автоматически при первом вызове
stats = get_geo_stats()  # Загрузка происходит здесь
```

### Кэширование
Загруженные данные кэшируются в памяти для быстрого доступа:

```python
# Первый вызов - загрузка из файлов
regions1 = find_yandex_regions("Москва")

# Второй вызов - данные из кэша
regions2 = find_yandex_regions("Москва")  # Быстро!
```

## 🔧 Настройка

### Пути к файлам данных
По умолчанию модуль ищет файлы в корневой директории проекта:
- `yandex_geo.csv` - регионы Yandex
- `countries.xlsx` - страны Google  
- `langs.xlsx` - языки Google
- `geo.csv` - города

### Обработка ошибок
Модуль gracefully обрабатывает отсутствующие файлы:

```python
# Если файл не найден, выводится предупреждение
# Warning: yandex_geo.csv not found
```

## 📈 Расширение функциональности

### Добавление новых доменов
```python
# В geo_data.py можно добавить новые домены в _load_google_domains()
domains = {
    # ... существующие домены
    "new_domain": GoogleDomain("new_domain", "New Country", "New Country"),
}
```

### Добавление новых языков
Новые языки автоматически загружаются из `langs.xlsx` при обновлении файла.

## 🎯 Лучшие практики

1. **Используйте точный поиск** для критически важных операций
2. **Кэшируйте результаты** для часто используемых запросов
3. **Обрабатывайте ошибки** при работе с внешними API
4. **Проверяйте наличие данных** перед использованием
5. **Используйте универсальные функции** для сложных сценариев

## 🔗 Связанные модули

- [API Reference](API_REFERENCE.md) - полный справочник API
- [Validators Reference](VALIDATORS_REFERENCE.md) - валидация данных
- [Examples](examples.md) - примеры использования
