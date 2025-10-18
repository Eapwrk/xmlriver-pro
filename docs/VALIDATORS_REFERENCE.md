# Справочник валидаторов

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md)

Полный справочник всех валидаторов XMLRiver Pro с примерами использования.

## Содержание

- [Основные валидаторы](#основные-валидаторы)
- [Валидаторы поиска](#валидаторы-поиска)
- [Валидаторы устройств](#валидаторы-устройств)
- [Валидаторы локализации](#валидаторы-локализации)
- [Валидаторы пагинации](#валидаторы-пагинации)
- [Валидаторы времени](#валидаторы-времени)
- [Валидаторы файлов](#валидаторы-файлов)
- [Валидаторы изображений](#валидаторы-изображений)
- [Примеры использования](#примеры-использования)

## Основные валидаторы

### validate_coords(coords: Coords) -> bool

Валидация координат (широта и долгота).

```python
from xmlriver_pro.utils import validate_coords
from xmlriver_pro.core.types import Coords

# Валидные координаты
coords1 = (55.7558, 37.6176)  # Москва
coords2 = Coords(latitude=55.7558, longitude=37.6176)

print(validate_coords(coords1))  # True
print(validate_coords(coords2))  # True

# Невалидные координаты
coords3 = (91.0, 37.6176)  # Широта > 90
coords4 = (55.7558, 181.0)  # Долгота > 180
coords5 = (-91.0, 37.6176)  # Широта < -90
coords6 = (55.7558, -181.0)  # Долгота < -180

print(validate_coords(coords3))  # False
print(validate_coords(coords4))  # False
print(validate_coords(coords5))  # False
print(validate_coords(coords6))  # False
```

### validate_zoom(zoom: int) -> bool

Валидация уровня масштабирования карты (1-15).

```python
from xmlriver_pro.utils import validate_zoom

# Валидные значения
print(validate_zoom(1))   # True
print(validate_zoom(8))   # True
print(validate_zoom(15))  # True

# Невалидные значения
print(validate_zoom(0))   # False
print(validate_zoom(16))  # False
print(validate_zoom(-1))  # False
```

### validate_url(url: str) -> bool

Валидация URL.

```python
from xmlriver_pro.utils import validate_url

# Валидные URL
print(validate_url("https://python.org"))           # True
print(validate_url("http://example.com"))           # True
print(validate_url("https://subdomain.example.com/path?param=value"))  # True

# Невалидные URL
print(validate_url("not-a-url"))                    # False
print(validate_url(""))                             # False
print(validate_url("ftp://example.com"))            # True (ftp валиден)
```

## Валидаторы поиска

### validate_query(query: str) -> bool

Валидация поискового запроса.

```python
from xmlriver_pro.utils import validate_query

# Валидные запросы
print(validate_query("python programming"))         # True
print(validate_query("машинное обучение"))          # True
print(validate_query("data science 2024"))          # True

# Невалидные запросы
print(validate_query(""))                           # False
print(validate_query("   "))                        # False
print(validate_query(None))                         # False
```

## Валидаторы устройств

### validate_device(device: Union[str, DeviceType]) -> bool

Валидация типа устройства.

```python
from xmlriver_pro.utils import validate_device
from xmlriver_pro.core.types import DeviceType

# Валидные типы устройств
print(validate_device("desktop"))                   # True
print(validate_device("mobile"))                    # True
print(validate_device("tablet"))                    # True
print(validate_device(DeviceType.DESKTOP))          # True
print(validate_device(DeviceType.MOBILE))           # True
print(validate_device(DeviceType.TABLET))           # True

# Невалидные типы устройств
print(validate_device("laptop"))                    # False
print(validate_device("phone"))                     # False
print(validate_device(""))                          # False
print(validate_device(None))                        # False
```

### validate_os(os: Union[str, OSType]) -> bool

Валидация операционной системы.

```python
from xmlriver_pro.utils import validate_os
from xmlriver_pro.core.types import OSType

# Валидные ОС
print(validate_os("windows"))                       # True
print(validate_os("macos"))                         # True
print(validate_os("linux"))                         # True
print(validate_os("android"))                       # True
print(validate_os("ios"))                           # True
print(validate_os(OSType.WINDOWS))                  # True
print(validate_os(OSType.MACOS))                    # True
print(validate_os(OSType.LINUX))                    # True
print(validate_os(OSType.ANDROID))                  # True
print(validate_os(OSType.IOS))                      # True

# Невалидные ОС
print(validate_os("ubuntu"))                        # False
print(validate_os("centos"))                        # False
print(validate_os(""))                              # False
print(validate_os(None))                            # False
```

## Валидаторы локализации

### validate_country(country: int) -> bool

Валидация ID страны.

```python
from xmlriver_pro.utils import validate_country

# Валидные ID стран
print(validate_country(2840))  # США
print(validate_country(225))   # Россия
print(validate_country(826))   # Великобритания
print(validate_country(276))   # Германия
print(validate_country(250))   # Франция

# Невалидные ID стран
print(validate_country(0))     # False
print(validate_country(-1))    # False
print(validate_country(9999))  # False
```

### validate_region(region: int) -> bool

Валидация ID региона.

```python
from xmlriver_pro.utils import validate_region

# Валидные ID регионов
print(validate_region(213))    # Москва
print(validate_region(2))      # Санкт-Петербург
print(validate_region(1))      # Республика Адыгея
print(validate_region(3))      # Республика Башкортостан

# Невалидные ID регионов
print(validate_region(0))      # False
print(validate_region(-1))     # False
print(validate_region(9999))   # False
```

### validate_language(language: str) -> bool

Валидация кода языка.

```python
from xmlriver_pro.utils import validate_language

# Валидные коды языков
print(validate_language("ru"))     # True
print(validate_language("en"))     # True
print(validate_language("de"))     # True
print(validate_language("fr"))     # True
print(validate_language("es"))     # True
print(validate_language("zh"))     # True
print(validate_language("ja"))     # True

# Невалидные коды языков
print(validate_language(""))       # False
print(validate_language("rus"))    # False
print(validate_language("eng"))    # False
print(validate_language("123"))    # False
print(validate_language(None))     # False
```

### validate_domain(domain: str) -> bool

Валидация домена.

```python
from xmlriver_pro.utils import validate_domain

# Валидные домены
print(validate_domain("ru"))       # True
print(validate_domain("com"))      # True
print(validate_domain("org"))      # True
print(validate_domain("net"))      # True
print(validate_domain("edu"))      # True
print(validate_domain("gov"))      # True

# Невалидные домены
print(validate_domain(""))         # False
print(validate_domain("invalid"))  # False
print(validate_domain("123"))      # False
print(validate_domain(None))       # False
```

## Валидаторы пагинации

### validate_groupby(groupby: int) -> bool

Валидация количества результатов на странице (1-10).

```python
from xmlriver_pro.utils import validate_groupby

# Валидные значения
print(validate_groupby(1))     # True
print(validate_groupby(5))     # True
print(validate_groupby(10))    # True

# Невалидные значения
print(validate_groupby(0))     # False
print(validate_groupby(11))    # False
print(validate_groupby(-1))    # False
```

### validate_page(page: int, search_engine: str = "google") -> bool

Валидация номера страницы с учетом поисковой системы.

```python
from xmlriver_pro.utils import validate_page

# Google (1-based)
print(validate_page(1, "google"))      # True
print(validate_page(10, "google"))     # True
print(validate_page(0, "google"))      # False

# Yandex (0-based)
print(validate_page(0, "yandex"))      # True
print(validate_page(9, "yandex"))      # True
print(validate_page(1, "yandex"))      # False

# Невалидные значения
print(validate_page(-1, "google"))     # False
print(validate_page(-1, "yandex"))     # False
print(validate_page(11, "google"))     # False
print(validate_page(10, "yandex"))     # False
```

## Валидаторы времени

### validate_time_filter(time_filter: str) -> bool

Валидация фильтра времени для Google.

```python
from xmlriver_pro.utils import validate_time_filter

# Валидные фильтры времени
print(validate_time_filter("qdr:d"))   # За день
print(validate_time_filter("qdr:w"))   # За неделю
print(validate_time_filter("qdr:m"))   # За месяц
print(validate_time_filter("qdr:y"))   # За год

# Невалидные фильтры времени
print(validate_time_filter(""))        # False
print(validate_time_filter("qdr:h"))   # False
print(validate_time_filter("invalid")) # False
print(validate_time_filter(None))      # False
```

### validate_within(within: int) -> bool

Валидация параметра within для Yandex (в днях).

```python
from xmlriver_pro.utils import validate_within

# Валидные значения
print(validate_within(1))      # За день
print(validate_within(7))      # За неделю
print(validate_within(30))     # За месяц
print(validate_within(77))     # За все время

# Невалидные значения
print(validate_within(0))      # False
print(validate_within(-1))     # False
print(validate_within(100))    # False
```

## Валидаторы файлов

### validate_file_type(file_type: str) -> bool

Валидация типа файла для поиска.

```python
from xmlriver_pro.utils import validate_file_type

# Валидные типы файлов
print(validate_file_type("pdf"))       # True
print(validate_file_type("doc"))       # True
print(validate_file_type("docx"))      # True
print(validate_file_type("xls"))       # True
print(validate_file_type("xlsx"))      # True
print(validate_file_type("ppt"))       # True
print(validate_file_type("pptx"))      # True
print(validate_file_type("txt"))       # True
print(validate_file_type("rtf"))       # True

# Невалидные типы файлов
print(validate_file_type(""))          # False
print(validate_file_type("image"))     # False
print(validate_file_type("video"))     # False
print(validate_file_type("123"))       # False
print(validate_file_type(None))        # False
```

## Валидаторы изображений

### validate_image_size(size: str) -> bool

Валидация размера изображения.

```python
from xmlriver_pro.utils import validate_image_size

# Валидные размеры
print(validate_image_size("small"))    # True
print(validate_image_size("medium"))   # True
print(validate_image_size("large"))    # True
print(validate_image_size("xlarge"))   # True

# Невалидные размеры
print(validate_image_size(""))         # False
print(validate_image_size("tiny"))     # False
print(validate_image_size("huge"))     # False
print(validate_image_size("123"))      # False
print(validate_image_size(None))       # False
```

### validate_image_color(color: str) -> bool

Валидация цвета изображения.

```python
from xmlriver_pro.utils import validate_image_color

# Валидные цвета
print(validate_image_color("black"))       # True
print(validate_image_color("white"))       # True
print(validate_image_color("red"))         # True
print(validate_image_color("green"))       # True
print(validate_image_color("blue"))        # True
print(validate_image_color("yellow"))      # True
print(validate_image_color("pink"))        # True
print(validate_image_color("purple"))      # True
print(validate_image_color("brown"))       # True
print(validate_image_color("gray"))        # True
print(validate_image_color("teal"))        # True

# Невалидные цвета
print(validate_image_color(""))            # False
print(validate_image_color("orange"))      # False
print(validate_image_color("violet"))      # False
print(validate_image_color("123"))         # False
print(validate_image_color(None))          # False
```

### validate_image_type(image_type: str) -> bool

Валидация типа изображения.

```python
from xmlriver_pro.utils import validate_image_type

# Валидные типы изображений
print(validate_image_type("photo"))        # True
print(validate_image_type("clipart"))      # True
print(validate_image_type("lineart"))      # True
print(validate_image_type("gif"))          # True
print(validate_image_type("transparent"))  # True

# Невалидные типы изображений
print(validate_image_type(""))             # False
print(validate_image_type("image"))        # False
print(validate_image_type("picture"))      # False
print(validate_image_type("123"))          # False
print(validate_image_type(None))           # False
```

### validate_usage_rights(usage_rights: str) -> bool

Валидация прав использования изображения.

```python
from xmlriver_pro.utils import validate_usage_rights

# Валидные права использования
print(validate_usage_rights("cc_publicdomain"))        # True
print(validate_usage_rights("cc_attribute"))           # True
print(validate_usage_rights("cc_sharealike"))          # True
print(validate_usage_rights("cc_noncommercial"))       # True
print(validate_usage_rights("cc_nonderived"))          # True
print(validate_usage_rights("cc_publicdomain"))        # True

# Невалидные права использования
print(validate_usage_rights(""))                       # False
print(validate_usage_rights("copyright"))              # False
print(validate_usage_rights("free"))                   # False
print(validate_usage_rights("123"))                    # False
print(validate_usage_rights(None))                     # False
```

## Примеры использования

### Комплексная валидация параметров поиска

```python
from xmlriver_pro.utils import (
    validate_query, validate_device, validate_os, validate_country,
    validate_region, validate_language, validate_domain, validate_groupby,
    validate_page, validate_time_filter, validate_within
)

def validate_search_params(params, search_engine="google"):
    """Комплексная валидация параметров поиска"""
    errors = []
    
    # Обязательные параметры
    if not validate_query(params.get("query")):
        errors.append("Невалидный поисковый запрос")
    
    # Опциональные параметры
    if "device" in params and not validate_device(params["device"]):
        errors.append("Невалидный тип устройства")
    
    if "os" in params and not validate_os(params["os"]):
        errors.append("Невалидная операционная система")
    
    if "country" in params and not validate_country(params["country"]):
        errors.append("Невалидный ID страны")
    
    if "region" in params and not validate_region(params["region"]):
        errors.append("Невалидный ID региона")
    
    if "language" in params and not validate_language(params["language"]):
        errors.append("Невалидный код языка")
    
    if "domain" in params and not validate_domain(params["domain"]):
        errors.append("Невалидный домен")
    
    if "groupby" in params and not validate_groupby(params["groupby"]):
        errors.append("Невалидное количество результатов")
    
    if "page" in params and not validate_page(params["page"], search_engine):
        errors.append("Невалидный номер страницы")
    
    if "time_filter" in params and not validate_time_filter(params["time_filter"]):
        errors.append("Невалидный фильтр времени")
    
    if "within" in params and not validate_within(params["within"]):
        errors.append("Невалидный параметр within")
    
    return len(errors) == 0, errors

# Использование
params = {
    "query": "python programming",
    "device": "desktop",
    "os": "windows",
    "country": 2840,
    "region": 213,
    "language": "en",
    "domain": "com",
    "groupby": 10,
    "page": 1,
    "time_filter": "qdr:w"
}

is_valid, errors = validate_search_params(params, "google")

if is_valid:
    print("Все параметры валидны")
else:
    print("Ошибки валидации:")
    for error in errors:
        print(f"  - {error}")
```

### Валидация параметров изображений

```python
from xmlriver_pro.utils import (
    validate_image_size, validate_image_color, validate_image_type, validate_usage_rights
)

def validate_image_params(params):
    """Валидация параметров поиска изображений"""
    errors = []
    
    if "size" in params and not validate_image_size(params["size"]):
        errors.append("Невалидный размер изображения")
    
    if "color" in params and not validate_image_color(params["color"]):
        errors.append("Невалидный цвет изображения")
    
    if "image_type" in params and not validate_image_type(params["image_type"]):
        errors.append("Невалидный тип изображения")
    
    if "usage_rights" in params and not validate_usage_rights(params["usage_rights"]):
        errors.append("Невалидные права использования")
    
    return len(errors) == 0, errors

# Использование
image_params = {
    "size": "large",
    "color": "blue",
    "image_type": "photo",
    "usage_rights": "cc_publicdomain"
}

is_valid, errors = validate_image_params(image_params)

if is_valid:
    print("Все параметры изображений валидны")
else:
    print("Ошибки валидации:")
    for error in errors:
        print(f"  - {error}")
```

### Валидация координат для карт

```python
from xmlriver_pro.utils import validate_coords, validate_zoom

def validate_map_params(params):
    """Валидация параметров поиска по картам"""
    errors = []
    
    if "coords" in params and not validate_coords(params["coords"]):
        errors.append("Невалидные координаты")
    
    if "zoom" in params and not validate_zoom(params["zoom"]):
        errors.append("Невалидный уровень масштабирования")
    
    return len(errors) == 0, errors

# Использование
map_params = {
    "coords": (55.7558, 37.6176),  # Москва
    "zoom": 12
}

is_valid, errors = validate_map_params(map_params)

if is_valid:
    print("Все параметры карт валидны")
else:
    print("Ошибки валидации:")
    for error in errors:
        print(f"  - {error}")
```

### Универсальная валидация

```python
def universal_validate(param_name, param_value, search_engine="google"):
    """Универсальная валидация параметра"""
    validators = {
        "query": validate_query,
        "device": validate_device,
        "os": validate_os,
        "country": validate_country,
        "region": validate_region,
        "language": validate_language,
        "domain": validate_domain,
        "groupby": validate_groupby,
        "page": lambda x: validate_page(x, search_engine),
        "time_filter": validate_time_filter,
        "within": validate_within,
        "file_type": validate_file_type,
        "image_size": validate_image_size,
        "image_color": validate_image_color,
        "image_type": validate_image_type,
        "usage_rights": validate_usage_rights,
        "coords": validate_coords,
        "zoom": validate_zoom,
        "url": validate_url
    }
    
    if param_name not in validators:
        return False, f"Неизвестный параметр: {param_name}"
    
    validator = validators[param_name]
    
    try:
        is_valid = validator(param_value)
        if is_valid:
            return True, "Параметр валиден"
        else:
            return False, f"Невалидное значение для {param_name}: {param_value}"
    except Exception as e:
        return False, f"Ошибка валидации {param_name}: {e}"

# Использование
test_params = [
    ("query", "python programming"),
    ("device", "desktop"),
    ("country", 2840),
    ("page", 1),
    ("coords", (55.7558, 37.6176)),
    ("image_size", "large"),
    ("invalid_param", "value")
]

for param_name, param_value in test_params:
    is_valid, message = universal_validate(param_name, param_value)
    status = "✅" if is_valid else "❌"
    print(f"{status} {param_name}: {message}")
```

---

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md) • [Справочник форматтеров](FORMATTERS_REFERENCE.md)
