# Примеры использования XMLRiver Pro

## Содержание

1. [Базовое использование](#базовое-использование)
2. [Google API](#google-api)
3. [Yandex API](#yandex-api)
4. [Обработка ошибок](#обработка-ошибок)
5. [Валидация и форматирование](#валидация-и-форматирование)
6. [Продвинутые сценарии](#продвинутые-сценарии)

## Базовое использование

### Инициализация клиентов

```python
from xmlriver_pro import GoogleClient, YandexClient

# Google клиент
google = GoogleClient(
    user_id=123,
    api_key="your_google_api_key"
)

# Yandex клиент
yandex = YandexClient(
    user_id=123,
    api_key="your_yandex_api_key"
)
```

### Простой поиск

```python
# Google поиск
google_results = google.search("python programming")
print(f"Найдено результатов: {google_results.total_results}")

for result in google_results.results:
    print(f"{result.rank}. {result.title}")
    print(f"   URL: {result.url}")
    print(f"   Snippet: {result.snippet}")
    print()

# Yandex поиск
yandex_results = yandex.search("программирование на python")
print(f"Найдено результатов: {yandex_results.total_results}")
```

## Google API

### Органический поиск

```python
from xmlriver_pro import GoogleSearch
from xmlriver_pro.core.types import DeviceType, TimeFilter

search = GoogleSearch(user_id=123, api_key="your_key")

# Базовый поиск
results = search.search("python programming")

# Поиск с параметрами
results = search.search(
    query="python programming",
    groupby=10,
    page=1,
    country=10,  # США
    device=DeviceType.DESKTOP
)

# Поиск с фильтром времени
results = search.search_with_time_filter(
    query="python news",
    time_filter=TimeFilter.LAST_WEEK
)

# Поиск без исправления запроса
results = search.search_without_correction("pythn programmng")

# Поиск с подсветкой ключевых слов
results = search.search_with_highlights("python programming")

# Поиск по сайту
results = search.search_site("python.org", "tutorial")

# Поиск точной фразы
results = search.search_exact_phrase("python programming language")

# Поиск с исключением слов
results = search.search_exclude_words(
    "python programming",
    ["java", "c++", "javascript"]
)

# Поиск по типу файла
results = search.search_file_type("python tutorial", "pdf")

# Поиск в заголовках
results = search.search_in_title("python")

# Поиск в URL
results = search.search_in_url("python.org")

# Поиск похожих сайтов
results = search.search_related("https://python.org")

# Поиск кэшированной версии
results = search.search_cache("https://python.org")

# Поиск определения
results = search.search_define("python programming")

# Получение информации о сайте
results = search.search_info("https://python.org")
```

### Поиск по новостям

```python
from xmlriver_pro import GoogleNews
from xmlriver_pro.core.types import TimeFilter

news = GoogleNews(user_id=123, api_key="your_key")

# Базовый поиск новостей
results = news.search_news("python programming")

# Поиск с фильтром времени
results = news.search_news(
    query="python programming",
    time_filter=TimeFilter.LAST_DAY
)

# Поиск за последний час
results = news.search_news_last_hour("python news")

# Поиск за последний день
results = news.search_news_last_day("python news")

# Поиск за последнюю неделю
results = news.search_news_last_week("python news")

# Поиск за последний месяц
results = news.search_news_last_month("python news")

# Поиск за последний год
results = news.search_news_last_year("python news")

# Поиск за пользовательский период
results = news.search_news_custom_period(
    query="python news",
    start_date="01/01/2023",
    end_date="12/31/2023"
)

# Обработка результатов новостей
for result in results.results:
    print(f"Заголовок: {result.title}")
    print(f"URL: {result.url}")
    print(f"Дата публикации: {result.pub_date}")
    print(f"Источник: {result.media}")
    print(f"Описание: {result.snippet}")
    print()
```

### Поиск по изображениям

```python
from xmlriver_pro import GoogleImages

images = GoogleImages(user_id=123, api_key="your_key")

# Базовый поиск изображений
results = images.search_images("python logo", count=20)

# Поиск по размеру
large_images = images.search_images_by_size("python logo", "large")
small_images = images.search_images_by_size("python logo", "small")

# Поиск по цвету
blue_images = images.search_images_by_color("python logo", "blue")
color_images = images.search_images_by_color("python logo", "color")
grayscale_images = images.search_images_by_color("python logo", "grayscale")

# Поиск по типу
photo_images = images.search_images_by_type("python logo", "photo")
clipart_images = images.search_images_by_type("python logo", "clipart")
animated_images = images.search_images_by_type("python logo", "animated")

# Поиск по правам использования
free_images = images.search_images_by_usage_rights("python logo", "cc_publicdomain")
attribution_images = images.search_images_by_usage_rights("python logo", "cc_attribute")

# Обработка результатов изображений
for result in results.results:
    print(f"Заголовок: {result.title}")
    print(f"URL: {result.url}")
    print(f"Изображение: {result.img_url}")
    print(f"Сайт: {result.display_link}")
    print(f"Размер: {result.original_width}x{result.original_height}")
    print()

# Получение предложенных запросов
suggestions = images.get_suggested_searches("python logo")
print("Предложенные запросы:", suggestions)
```

### Поиск по картам

```python
from xmlriver_pro import GoogleMaps

maps = GoogleMaps(user_id=123, api_key="your_key")

# Базовый поиск по картам
results = maps.search_maps(
    query="кафе Москва",
    zoom=12,
    coords=(55.7558, 37.6176),  # Координаты Москвы
    count=20
)

# Поиск поблизости
nearby_results = maps.search_nearby(
    query="кафе",
    coords=(55.7558, 37.6176),
    radius=1000  # 1 км
)

# Специализированные поиски
restaurants = maps.search_restaurants((55.7558, 37.6176))
hotels = maps.search_hotels((55.7558, 37.6176))
gas_stations = maps.search_gas_stations((55.7558, 37.6176))
pharmacies = maps.search_pharmacies((55.7558, 37.6176))

# Обработка результатов карт
for result in results.results:
    print(f"Название: {result.title}")
    print(f"Рейтинг: {result.stars} звезд")
    print(f"Тип: {result.type}")
    print(f"Адрес: {result.address}")
    print(f"Телефон: {result.phone}")
    print(f"Координаты: {result.latitude}, {result.longitude}")
    print(f"Количество отзывов: {result.count_reviews}")
    print()
```

### Рекламные блоки

```python
from xmlriver_pro import GoogleAds

ads = GoogleAds(user_id=123, api_key="your_key")

# Получение всех рекламных блоков
ads_response = ads.get_ads("python programming")

# Получение только верхних рекламных блоков
top_ads = ads.get_top_ads("python programming")

# Получение только нижних рекламных блоков
bottom_ads = ads.get_bottom_ads("python programming")

# Получение всех рекламных блоков
all_ads = ads.get_all_ads("python programming")

# Подсчет рекламных блоков
ads_count = ads.count_ads("python programming")
print(f"Количество рекламных блоков: {ads_count}")

# Проверка наличия рекламы
has_ads = ads.has_ads("python programming")
print(f"Есть реклама: {has_ads}")

# Фильтрация по домену
domain_ads = ads.get_ads_by_domain("python programming", "python.org")

# Статистика рекламы
stats = ads.get_ads_stats("python programming")
print(f"Верхние: {stats['top_ads_count']}")
print(f"Нижние: {stats['bottom_ads_count']}")
print(f"Всего: {stats['total_ads_count']}")

# Обработка рекламных блоков
for ad in ads_response.top_ads:
    print(f"Заголовок: {ad.title}")
    print(f"URL: {ad.url}")
    print(f"Рекламный URL: {ad.ads_url}")
    print(f"Описание: {ad.snippet}")
    print()
```

### Специальные блоки

```python
from xmlriver_pro import GoogleSpecialBlocks

special = GoogleSpecialBlocks(user_id=123, api_key="your_key")

# OneBox документы
onebox_docs = special.get_onebox_documents(
    query="python programming",
    types=["organic", "video", "images", "news"]
)

# Knowledge Graph
kg = special.get_knowledge_graph("Python programming language")
if kg:
    print(f"Сущность: {kg.entity_name}")
    print(f"Описание: {kg.description}")
    print(f"Изображение: {kg.image_url}")

# Связанные поиски
related_searches = special.get_related_searches("python programming")
for search in related_searches:
    print(f"Запрос: {search.query}")
    print(f"URL: {search.url}")

# Блок ответов
answer_box = special.get_answer_box("What is Python?")
if answer_box:
    print(f"Ответ: {answer_box['answer']}")
    print(f"Источник: {answer_box['source']}")

# Калькулятор
calc_result = special.get_calculator("2 + 2 * 3")
if calc_result:
    print(f"Выражение: {calc_result['expression']}")
    print(f"Результат: {calc_result['result']}")

# Переводчик
translation = special.get_translator("Hello world")
if translation:
    print(f"Оригинал: {translation['original_text']}")
    print(f"Перевод: {translation['translation']}")

# Погода
weather = special.get_weather("погода Москва")
if weather:
    print(f"Местоположение: {weather['location']}")
    print(f"Погода: {weather['weather_info']}")

# Конвертер валют
currency = special.get_currency_converter("100 USD to RUB")
if currency:
    print(f"Запрос: {currency['conversion_query']}")
    print(f"Результат: {currency['result']}")

# Время
time_info = special.get_time("время в Лондоне")
if time_info:
    print(f"Местоположение: {time_info['location_query']}")
    print(f"Время: {time_info['time_info']}")
```

## Yandex API

### Органический поиск

```python
from xmlriver_pro import YandexSearch
from xmlriver_pro.core.types import DeviceType

search = YandexSearch(user_id=123, api_key="your_key")

# Базовый поиск
results = search.search("программирование на python")

# Поиск с параметрами
results = search.search(
    query="программирование на python",
    groupby=10,
    page=0,  # Yandex использует 0-based пагинацию
    lr=213,  # Москва
    lang="ru",
    domain="ru",
    device=DeviceType.DESKTOP
)

# Поиск с фильтром времени
results = search.search_with_time_filter(
    query="python новости",
    within=77  # За сутки
)

# Поиск с подсветкой
results = search.search_with_highlights("python programming")

# Поиск с фильтрацией
results = search.search_with_filter("python programming")

# Поиск по сайту
results = search.search_site("python.org", "tutorial")

# Поиск точной фразы
results = search.search_exact_phrase("программирование на python")

# Поиск с исключением слов
results = search.search_exclude_words(
    "python programming",
    ["java", "c++", "javascript"]
)

# Поиск в заголовках
results = search.search_in_title("python")

# Поиск в URL
results = search.search_in_url("python.org")

# Поиск по региону
results = search.search_by_region("python", 213)  # Москва

# Поиск по языку
results = search.search_by_language("python", "ru")

# Поиск по домену
results = search.search_by_domain("python", "ru")

# Поиск по типу файла
results = search.search_file_type("python tutorial", "pdf")

# Поиск определения
results = search.search_define("python programming")

# Поиск похожих сайтов
results = search.search_related("https://python.org")
```

### Поиск по новостям

```python
from xmlriver_pro import YandexNews

news = YandexNews(user_id=123, api_key="your_key")

# Базовый поиск новостей
results = news.search_news("python новости")

# Поиск с фильтром времени
results = news.search_news(
    query="python новости",
    within=77  # За сутки
)

# Специализированные поиски
last_day = news.search_news_last_day("python новости")
last_2_weeks = news.search_news_last_2_weeks("python новости")
last_month = news.search_news_last_month("python новости")
all_time = news.search_news_all_time("python новости")

# Поиск по региону
moscow_news = news.search_news_by_region("python новости", 213)

# Поиск по языку
russian_news = news.search_news_by_language("python новости", "ru")

# Поиск по домену
ru_news = news.search_news_by_domain("python новости", "ru")

# Получение трендов
trends = news.get_news_trends("python")
print("Трендовые темы:", trends)
```

### Рекламные блоки

```python
from xmlriver_pro import YandexAds

ads = YandexAds(user_id=123, api_key="your_key")

# Получение рекламных блоков
ads_response = ads.get_ads("программирование python")

# Поиск по региону
moscow_ads = ads.get_ads_by_region("python", 213)

# Поиск по языку
russian_ads = ads.get_ads_by_language("python", "ru")

# Поиск по домену
ru_ads = ads.get_ads_by_domain("python", "ru")

# Статистика
stats = ads.get_ads_stats("python")
print(f"Верхние: {stats['top_ads_count']}")
print(f"Нижние: {stats['bottom_ads_count']}")
print(f"Всего: {stats['total_ads_count']}")
```

### Колдунщики (специальные блоки)

```python
from xmlriver_pro import YandexSpecialBlocks

special = YandexSpecialBlocks(user_id=123, api_key="your_key")

# Получение колдунщиков
searchsters = special.get_searchsters(
    query="python programming",
    types=["organic", "calculator", "weather", "translate"]
)

# Погода
weather = special.get_weather("погода Москва")
if weather:
    print(f"Местоположение: {weather['location']}")
    print(f"Погода: {weather['weather_info']}")

# Калькулятор
calc_result = special.get_calculator("2 + 2 * 3")
if calc_result:
    print(f"Выражение: {calc_result['expression']}")
    print(f"Результат: {calc_result['result']}")

# Переводчик
translation = special.get_translator("Hello world")
if translation:
    print(f"Оригинал: {translation['original_text']}")
    print(f"Перевод: {translation['translation']}")

# Конвертер валют
currency = special.get_currency_converter("100 USD to RUB")
if currency:
    print(f"Запрос: {currency['conversion_query']}")
    print(f"Результат: {currency['result']}")

# Время
time_info = special.get_time("время в Лондоне")
if time_info:
    print(f"Местоположение: {time_info['location_query']}")
    print(f"Время: {time_info['time_info']}")

# IP адрес
ip_info = special.get_ip_address()
if ip_info:
    print(f"IP адрес: {ip_info['ip_info']}")

# Карты
maps_info = special.get_maps("кафе Москва")
if maps_info:
    print(f"Местоположение: {maps_info['location_query']}")
    print(f"Информация: {maps_info['maps_info']}")

# Музыка
music_info = special.get_music("python programming music")
if music_info:
    print(f"Запрос: {music_info['music_query']}")
    print(f"Информация: {music_info['music_info']}")

# Текст песни
lyrics = special.get_lyrics("python song lyrics")
if lyrics:
    print(f"Песня: {lyrics['song_query']}")
    print(f"Текст: {lyrics['lyrics']}")

# Цитаты
quotes = special.get_quotes("python programming quotes")
if quotes:
    print(f"Запрос: {quotes['quotes_query']}")
    print(f"Цитаты: {quotes['quotes']}")

# Факты
facts = special.get_facts("python programming facts")
if facts:
    print(f"Запрос: {facts['fact_query']}")
    print(f"Факты: {facts['facts']}")

# Связанные поиски
related_searches = special.get_related_searches("python programming")
for search in related_searches:
    print(f"Запрос: {search.query}")
    print(f"URL: {search.url}")
```

## Обработка ошибок

```python
from xmlriver_pro.core import (
    XMLRiverError, AuthenticationError, RateLimitError,
    NoResultsError, NetworkError, ValidationError, APIError
)

try:
    results = google.search("python programming")
except AuthenticationError as e:
    print(f"Ошибка аутентификации: {e}")
    print(f"Код ошибки: {e.code}")
    print(f"Сообщение: {e.message}")
except RateLimitError as e:
    print(f"Превышен лимит запросов: {e}")
    print("Попробуйте позже")
except NoResultsError as e:
    print(f"Нет результатов для запроса: {e}")
except NetworkError as e:
    print(f"Ошибка сети: {e}")
    print("Проверьте подключение к интернету")
except ValidationError as e:
    print(f"Ошибка валидации параметров: {e}")
    print("Проверьте правильность параметров")
except APIError as e:
    print(f"Ошибка API: {e}")
    print(f"Код ошибки: {e.code}")
except XMLRiverError as e:
    print(f"Общая ошибка XMLRiver: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
```

## Валидация и форматирование

### Валидация параметров

```python
from xmlriver_pro.utils import (
    validate_coords, validate_zoom, validate_url, validate_query,
    validate_device, validate_os, validate_country, validate_region,
    validate_language, validate_domain, validate_groupby, validate_page,
    validate_time_filter, validate_within, validate_file_type,
    validate_image_size, validate_image_color, validate_image_type,
    validate_usage_rights
)

# Валидация координат
coords = (55.7558, 37.6176)
if validate_coords(coords):
    print("Координаты валидны")
else:
    print("Неверные координаты")

# Валидация zoom
if validate_zoom(12):
    print("Zoom валиден")
else:
    print("Неверный zoom (должен быть от 1 до 15)")

# Валидация URL
if validate_url("https://python.org"):
    print("URL валиден")
else:
    print("Неверный URL")

# Валидация запроса
if validate_query("python programming"):
    print("Запрос валиден")
else:
    print("Запрос содержит недопустимые символы")

# Валидация устройства
if validate_device("desktop"):
    print("Тип устройства валиден")
else:
    print("Неверный тип устройства")

# Валидация ОС
if validate_os("ios"):
    print("ОС валидна")
else:
    print("Неверная ОС")

# Валидация страны
if validate_country(10):
    print("ID страны валиден")
else:
    print("Неверный ID страны")

# Валидация региона
if validate_region(213):
    print("ID региона валиден")
else:
    print("Неверный ID региона")

# Валидация языка
if validate_language("ru"):
    print("Код языка валиден")
else:
    print("Неверный код языка")

# Валидация домена
if validate_domain("ru"):
    print("Домен валиден")
else:
    print("Неверный домен")

# Валидация groupby
if validate_groupby(10):
    print("Groupby валиден")
else:
    print("Неверный groupby (должен быть от 1 до 10)")

# Валидация страницы
if validate_page(1, "google"):
    print("Номер страницы валиден для Google")
else:
    print("Неверный номер страницы для Google")

if validate_page(0, "yandex"):
    print("Номер страницы валиден для Yandex")
else:
    print("Неверный номер страницы для Yandex")

# Валидация фильтра времени
if validate_time_filter("qdr:d"):
    print("Фильтр времени валиден")
else:
    print("Неверный фильтр времени")

# Валидация within
if validate_within(77):
    print("Within валиден")
else:
    print("Неверный within")

# Валидация типа файла
if validate_file_type("pdf"):
    print("Тип файла валиден")
else:
    print("Неверный тип файла")

# Валидация размера изображения
if validate_image_size("large"):
    print("Размер изображения валиден")
else:
    print("Неверный размер изображения")

# Валидация цвета изображения
if validate_image_color("blue"):
    print("Цвет изображения валиден")
else:
    print("Неверный цвет изображения")

# Валидация типа изображения
if validate_image_type("photo"):
    print("Тип изображения валиден")
else:
    print("Неверный тип изображения")

# Валидация прав использования
if validate_usage_rights("cc_publicdomain"):
    print("Права использования валидны")
else:
    print("Неверные права использования")
```

### Форматирование результатов

```python
from xmlriver_pro.utils import (
    format_search_result, format_search_response, format_news_result,
    format_image_result, format_map_result, format_ads_result,
    format_ads_response, format_onebox_document, format_searchster_result,
    format_related_search, format_search_stats, format_ads_stats,
    format_results_summary, format_ads_summary, format_error_message,
    format_api_response
)

# Форматирование результата поиска
result = search_results.results[0]
formatted_result = format_search_result(result)
print("Отформатированный результат:")
print(formatted_result)

# Форматирование ответа поиска
formatted_response = format_search_response(search_results)
print("Отформатированный ответ:")
print(formatted_response)

# Форматирование результата новостей
news_result = news_results.results[0]
formatted_news = format_news_result(news_result)
print("Отформатированная новость:")
print(formatted_news)

# Форматирование результата изображения
image_result = image_results.results[0]
formatted_image = format_image_result(image_result)
print("Отформатированное изображение:")
print(formatted_image)

# Форматирование результата карт
map_result = map_results.results[0]
formatted_map = format_map_result(map_result)
print("Отформатированная карта:")
print(formatted_map)

# Форматирование рекламного блока
ad_result = ads_response.top_ads[0]
formatted_ad = format_ads_result(ad_result)
print("Отформатированная реклама:")
print(formatted_ad)

# Форматирование ответа рекламы
formatted_ads = format_ads_response(ads_response)
print("Отформатированная реклама:")
print(formatted_ads)

# Форматирование OneBox документа
onebox_doc = onebox_docs[0]
formatted_onebox = format_onebox_document(onebox_doc)
print("Отформатированный OneBox:")
print(formatted_onebox)

# Форматирование колдунщика
searchster = searchsters[0]
formatted_searchster = format_searchster_result(searchster)
print("Отформатированный колдунщик:")
print(formatted_searchster)

# Форматирование связанного поиска
related_search = related_searches[0]
formatted_related = format_related_search(related_search)
print("Отформатированный связанный поиск:")
print(formatted_related)

# Статистика поиска
search_stats = format_search_stats(search_results)
print("Статистика поиска:")
print(search_stats)

# Статистика рекламы
ads_stats = format_ads_stats(ads_response)
print("Статистика рекламы:")
print(ads_stats)

# Краткое описание результатов
summary = format_results_summary(search_results)
print("Краткое описание:")
print(summary)

# Краткое описание рекламы
ads_summary = format_ads_summary(ads_response)
print("Краткое описание рекламы:")
print(ads_summary)

# Форматирование ошибки
try:
    results = google.search("")
except Exception as e:
    error_message = format_error_message(e)
    print("Ошибка:")
    print(error_message)

# Форматирование ответа API
api_response = {"found": {"#text": "1000000"}}
formatted_api = format_api_response(api_response)
print("Ответ API:")
print(formatted_api)
```

## Продвинутые сценарии

### Массовый поиск

```python
import time
from xmlriver_pro import GoogleClient, YandexClient

def mass_search(queries, search_engines=["google", "yandex"]):
    """Массовый поиск по списку запросов"""
    results = {}
    
    if "google" in search_engines:
        google = GoogleClient(user_id=123, api_key="your_google_key")
        results["google"] = {}
        
        for query in queries:
            try:
                search_results = google.search(query)
                results["google"][query] = {
                    "total": search_results.total_results,
                    "returned": len(search_results.results),
                    "results": search_results.results
                }
                time.sleep(1)  # Задержка между запросами
            except Exception as e:
                results["google"][query] = {"error": str(e)}
    
    if "yandex" in search_engines:
        yandex = YandexClient(user_id=123, api_key="your_yandex_key")
        results["yandex"] = {}
        
        for query in queries:
            try:
                search_results = yandex.search(query)
                results["yandex"][query] = {
                    "total": search_results.total_results,
                    "returned": len(search_results.results),
                    "results": search_results.results
                }
                time.sleep(1)  # Задержка между запросами
            except Exception as e:
                results["yandex"][query] = {"error": str(e)}
    
    return results

# Использование
queries = ["python programming", "machine learning", "data science"]
results = mass_search(queries)

for engine, engine_results in results.items():
    print(f"\n{engine.upper()}:")
    for query, query_results in engine_results.items():
        if "error" in query_results:
            print(f"  {query}: Ошибка - {query_results['error']}")
        else:
            print(f"  {query}: {query_results['total']} результатов")
```

### Мониторинг позиций

```python
def monitor_positions(url, keywords, search_engines=["google", "yandex"]):
    """Мониторинг позиций URL по ключевым словам"""
    positions = {}
    
    if "google" in search_engines:
        google = GoogleClient(user_id=123, api_key="your_google_key")
        positions["google"] = {}
        
        for keyword in keywords:
            try:
                results = google.search(keyword)
                position = None
                for i, result in enumerate(results.results, 1):
                    if url in result.url:
                        position = i
                        break
                positions["google"][keyword] = position
            except Exception as e:
                positions["google"][keyword] = f"Ошибка: {e}"
    
    if "yandex" in search_engines:
        yandex = YandexClient(user_id=123, api_key="your_yandex_key")
        positions["yandex"] = {}
        
        for keyword in keywords:
            try:
                results = yandex.search(keyword)
                position = None
                for i, result in enumerate(results.results, 1):
                    if url in result.url:
                        position = i
                        break
                positions["yandex"][keyword] = position
            except Exception as e:
                positions["yandex"][keyword] = f"Ошибка: {e}"
    
    return positions

# Использование
url = "https://python.org"
keywords = ["python programming", "python tutorial", "python documentation"]
positions = monitor_positions(url, keywords)

for engine, engine_positions in positions.items():
    print(f"\n{engine.upper()}:")
    for keyword, position in engine_positions.items():
        if isinstance(position, int):
            print(f"  {keyword}: позиция {position}")
        else:
            print(f"  {keyword}: {position}")
```

### Анализ конкурентов

```python
def analyze_competitors(domain, keywords, search_engines=["google", "yandex"]):
    """Анализ конкурентов по ключевым словам"""
    analysis = {}
    
    if "google" in search_engines:
        google = GoogleClient(user_id=123, api_key="your_google_key")
        analysis["google"] = {}
        
        for keyword in keywords:
            try:
                results = google.search(keyword)
                competitors = []
                for result in results.results:
                    if domain not in result.url:
                        competitors.append({
                            "url": result.url,
                            "title": result.title,
                            "rank": result.rank
                        })
                analysis["google"][keyword] = competitors
            except Exception as e:
                analysis["google"][keyword] = f"Ошибка: {e}"
    
    if "yandex" in search_engines:
        yandex = YandexClient(user_id=123, api_key="your_yandex_key")
        analysis["yandex"] = {}
        
        for keyword in keywords:
            try:
                results = yandex.search(keyword)
                competitors = []
                for result in results.results:
                    if domain not in result.url:
                        competitors.append({
                            "url": result.url,
                            "title": result.title,
                            "rank": result.rank
                        })
                analysis["yandex"][keyword] = competitors
            except Exception as e:
                analysis["yandex"][keyword] = f"Ошибка: {e}"
    
    return analysis

# Использование
domain = "python.org"
keywords = ["python programming", "python tutorial", "python documentation"]
competitors = analyze_competitors(domain, keywords)

for engine, engine_competitors in competitors.items():
    print(f"\n{engine.upper()}:")
    for keyword, keyword_competitors in engine_competitors.items():
        if isinstance(keyword_competitors, list):
            print(f"  {keyword}:")
            for competitor in keyword_competitors[:5]:  # Топ-5
                print(f"    {competitor['rank']}. {competitor['title']}")
                print(f"       {competitor['url']}")
        else:
            print(f"  {keyword}: {keyword_competitors}")
```

### Экспорт результатов

```python
import json
import csv
from datetime import datetime

def export_results(results, format="json", filename=None):
    """Экспорт результатов в различные форматы"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_results_{timestamp}"
    
    if format == "json":
        filename += ".json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    elif format == "csv":
        filename += ".csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Engine', 'Query', 'Rank', 'Title', 'URL', 'Snippet'])
            
            for engine, engine_results in results.items():
                for query, query_results in engine_results.items():
                    if "error" not in query_results:
                        for result in query_results["results"]:
                            writer.writerow([
                                engine,
                                query,
                                result.rank,
                                result.title,
                                result.url,
                                result.snippet
                            ])
    
    print(f"Результаты экспортированы в {filename}")

# Использование
results = mass_search(["python programming", "machine learning"])
export_results(results, "json")
export_results(results, "csv")
```

### Кэширование результатов

```python
import pickle
import os
from datetime import datetime, timedelta

class SearchCache:
    """Кэш для результатов поиска"""
    
    def __init__(self, cache_dir="cache", ttl_hours=24):
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
    
    def clear(self):
        """Очистить кэш"""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.pkl'):
                os.remove(os.path.join(self.cache_dir, filename))

# Использование с кэшем
cache = SearchCache()

def cached_search(engine, query, **kwargs):
    """Поиск с кэшированием"""
    cache_key = f"{engine}_{query}_{hash(str(kwargs))}"
    
    # Проверяем кэш
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        print(f"Результат из кэша: {query}")
        return cached_result
    
    # Выполняем поиск
    if engine == "google":
        client = GoogleClient(user_id=123, api_key="your_google_key")
    elif engine == "yandex":
        client = YandexClient(user_id=123, api_key="your_yandex_key")
    else:
        raise ValueError(f"Неизвестная поисковая система: {engine}")
    
    result = client.search(query, **kwargs)
    
    # Сохраняем в кэш
    cache.set(cache_key, result)
    print(f"Результат сохранен в кэш: {query}")
    
    return result

# Использование
result1 = cached_search("google", "python programming")
result2 = cached_search("google", "python programming")  # Из кэша
result3 = cached_search("yandex", "программирование python")
```

Эти примеры демонстрируют широкие возможности XMLRiver Pro для работы с поисковыми системами Google и Yandex. Библиотека предоставляет полный контроль над всеми аспектами поиска и позволяет создавать сложные системы мониторинга и анализа.
