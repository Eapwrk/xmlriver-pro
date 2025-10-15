# XMLRiver Pro

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-57%25-brightgreen.svg)](https://github.com/Eapwrk/xmlriver-pro)

> Fork of [KursHub-ru/xmlriver](https://github.com/KursHub-ru/xmlriver) - переписанная версия с полным покрытием API

Python библиотека для работы с API xmlriver.com. Оригинальная библиотека покрывала только ~5% возможностей API, поэтому я переписал её с нуля.

Поддерживает все типы поиска в Google и Yandex: органический поиск, новости, изображения, карты, реклама и специальные блоки.

## 🔄 Отличия от оригинала

| Характеристика | Оригинал | XMLRiver Pro |
|---|---|---|
| **Покрытие API** | ~5% | **100%** |
| **Архитектура** | Монолитная | **Модульная** |
| **Типизация** | Отсутствует | **Полная типизация** |
| **Тесты** | Отсутствуют | **66 тестов, 57% покрытие** |
| **Документация** | Минимальная | **Профессиональная** |
| **Качество кода** | Базовое | **Pylint 9.38/10** |
| **Обработка ошибок** | Простая | **Специализированные исключения** |
| **Логирование** | print() | **Профессиональное** |

## Что умеет

- Органический поиск в Google и Yandex
- Поиск по новостям с фильтрами времени
- Поиск по изображениям (размер, цвет, тип)
- Поиск по картам с координатами
- Рекламные блоки (верхние и нижние)
- Специальные блоки (OneBox, Knowledge Graph)

## Особенности

- Полная типизация для Python 3.10+
- Модульная архитектура
- 66 тестов с покрытием 57%
- Логирование вместо print()
- Специализированные исключения
- Валидация параметров

## Установка

```bash
pip install xmlriver-pro
```

Для разработки:
```bash
git clone https://github.com/Eapwrk/xmlriver-pro.git
cd xmlriver-pro
pip install -e .
```

## Быстрый старт

```python
from xmlriver_pro import GoogleClient, YandexClient

# Инициализация клиентов
google = GoogleClient(user_id=123, api_key="your_google_key")
yandex = YandexClient(user_id=123, api_key="your_yandex_key")

# Органический поиск
google_results = google.search("python programming")
yandex_results = yandex.search("программирование на python")

print(f"Google: {google_results.total_results} результатов")
print(f"Yandex: {yandex_results.total_results} результатов")
```

### Поиск по новостям

```python
from xmlriver_pro import GoogleNews, YandexNews
from xmlriver_pro.core.types import TimeFilter

# Google новости
google_news = GoogleNews(user_id=123, api_key="your_key")
news_results = google_news.search_news("python", time_filter=TimeFilter.LAST_WEEK)

# Yandex новости
yandex_news = YandexNews(user_id=123, api_key="your_key")
yandex_news_results = yandex_news.search_news_last_day("python новости")
```

### Поиск по изображениям

```python
from xmlriver_pro import GoogleImages

images = GoogleImages(user_id=123, api_key="your_key")

# Поиск изображений
image_results = images.search_images("python logo", count=20)

# Поиск с фильтрами
large_images = images.search_images_by_size("python logo", "large")
color_images = images.search_images_by_color("python logo", "blue")
```

### Поиск по картам

```python
from xmlriver_pro import GoogleMaps

maps = GoogleMaps(user_id=123, api_key="your_key")

# Поиск по картам
map_results = maps.search_maps(
    query="кафе Москва",
    zoom=12,
    coords=(55.7558, 37.6176)
)

# Поиск поблизости
nearby_cafes = maps.search_nearby("кафе", coords=(55.7558, 37.6176), radius=1000)
```

### Рекламные блоки

```python
from xmlriver_pro import GoogleAds, YandexAds

# Google реклама
google_ads = GoogleAds(user_id=123, api_key="your_key")
ads_response = google_ads.get_ads("python programming")

print(f"Верхние рекламные блоки: {len(ads_response.top_ads)}")
print(f"Нижние рекламные блоки: {len(ads_response.bottom_ads)}")

# Yandex реклама
yandex_ads = YandexAds(user_id=123, api_key="your_key")
yandex_ads_response = yandex_ads.get_ads("программирование python")
```

### Специальные блоки

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

### Валидация параметров

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

### Форматирование результатов

```python
from xmlriver_pro.utils import format_search_response, format_ads_response

# Форматирование результатов поиска
formatted_results = format_search_response(search_results)

# Форматирование рекламных блоков
formatted_ads = format_ads_response(ads_response)
```

### Обработка ошибок

```python
from xmlriver_pro.core import (
    XMLRiverError, AuthenticationError, RateLimitError, 
    NoResultsError, NetworkError, ValidationError
)

try:
    results = google.search("python")
except AuthenticationError as e:
    print(f"Ошибка аутентификации: {e}")
except RateLimitError as e:
    print(f"Превышен лимит запросов: {e}")
except NoResultsError as e:
    print(f"Нет результатов: {e}")
except NetworkError as e:
    print(f"Ошибка сети: {e}")
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
```

## 📊 Статистика и мониторинг

```python
# Получение баланса
balance = google.get_balance()
print(f"Баланс: {balance} руб.")

# Получение стоимости
google_cost = google.get_cost()
yandex_cost = yandex.get_cost()
print(f"Google: {google_cost} руб./1000 запросов")
print(f"Yandex: {yandex_cost} руб./1000 запросов")

# Проверка индексации
is_indexed = google.check_indexing("https://python.org")
print(f"URL проиндексирован: {is_indexed}")

# Проверка доверия к домену
is_trusted = google.is_trust_domain("python.org")
print(f"Домен доверенный: {is_trusted}")
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

- [Полная документация](https://xmlriver-pro.readthedocs.io/)
- [API Reference](https://xmlriver-pro.readthedocs.io/api/)
- [Примеры использования](https://xmlriver-pro.readthedocs.io/examples/)
- [Руководство по миграции](https://xmlriver-pro.readthedocs.io/migration/)

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста, ознакомьтесь с [руководством по вкладу](CONTRIBUTING.md).

### Установка для разработки

```bash
git clone https://github.com/xmlriver-pro/xmlriver-pro.git
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

Этот проект распространяется под лицензией MIT. См. [LICENSE](LICENSE) для получения дополнительной информации.

## 🙏 Благодарности

- [xmlriver.com](https://xmlriver.com) за предоставление API
- Сообществу Python за отличные инструменты
- Всем контрибьюторам проекта

## 📞 Поддержка

- 📧 Email: seo@controlseo.ru
- 🐛 Issues: [GitHub Issues](https://github.com/Eapwrk/xmlriver-pro/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Eapwrk/xmlriver-pro/discussions)

---

**XMLRiver Pro** - профессиональное решение для работы с поисковыми системами через API xmlriver.com
