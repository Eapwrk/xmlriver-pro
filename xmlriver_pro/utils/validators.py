"""
Валидаторы для XMLRiver Pro API
"""

from typing import Union
from urllib.parse import urlparse
from ..core.types import DeviceType, OSType, Coords


def validate_coords(coords: Coords) -> bool:
    """
    Валидация координат

    Args:
        coords: Координаты (широта, долгота)

    Returns:
        True если координаты валидны
    """
    if not isinstance(coords, (list, tuple)) or len(coords) != 2:
        return False
    lat, lon = coords
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False
    return -90 <= lat <= 90 and -180 <= lon <= 180


def validate_zoom(zoom: int) -> bool:
    """
    Валидация zoom уровня

    Args:
        zoom: Уровень приближения

    Returns:
        True если zoom валиден
    """
    return isinstance(zoom, int) and (1 <= zoom <= 15)


def validate_url(url: str) -> bool:
    """
    Валидация URL

    Args:
        url: URL для проверки

    Returns:
        True если URL валиден
    """
    if not isinstance(url, str):
        return False
    if not url or not url.strip():
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:  # pylint: disable=broad-exception-caught
        return False


def validate_query(query: str) -> bool:
    """
    Валидация поискового запроса

    Args:
        query: Поисковый запрос

    Returns:
        True если запрос валиден
    """
    if not isinstance(query, str) or not query.strip():
        return False

    # Проверяем на недопустимые символы
    invalid_chars = ["&", "<", ">", '"', "'"]
    return not any(char in query for char in invalid_chars)


def validate_device(device: Union[str, DeviceType]) -> bool:
    """
    Валидация типа устройства

    Args:
        device: Тип устройства

    Returns:
        True если тип устройства валиден
    """
    if device is None:
        return False
    if isinstance(device, DeviceType):
        return True

    if not isinstance(device, str):
        return False

    # mypy assumes str otherwise
    return device.lower() in ["desktop", "tablet", "mobile"]


def validate_os(os: Union[str, OSType]) -> bool:
    """
    Валидация операционной системы

    Args:
        os: Операционная система

    Returns:
        True если ОС валидна
    """
    if os is None:
        return False

    if isinstance(os, OSType):
        return True

    if not isinstance(os, str):
        return False

    # mypy assumes str otherwise
    return os.lower() in ["ios", "android"]


def validate_country(country: int) -> bool:
    """
    Валидация ID страны

    Args:
        country: ID страны

    Returns:
        True если ID страны валиден
    """
    return isinstance(country, int) and country > 0


def validate_region(region: int) -> bool:
    """
    Валидация ID региона

    Args:
        region: ID региона

    Returns:
        True если ID региона валиден
    """
    return isinstance(region, int) and region > 0


def validate_language(language: str) -> bool:
    """
    Валидация кода языка

    Args:
        language: Код языка

    Returns:
        True если код языка валиден
    """
    # Простая проверка на 2-символьный код
    if not isinstance(language, str):
        return False
    return len(language) == 2 and language.isalpha()


def validate_domain(domain: str) -> bool:
    """
    Валидация домена

    Args:
        domain: Домен

    Returns:
        True если домен валиден
    """
    if not isinstance(domain, str):
        return False
    valid_domains = ["ru", "com", "ua", "com.tr", "by", "kz"]
    return domain.lower() in valid_domains


def validate_groupby(groupby: int) -> bool:
    """
    Валидация параметра groupby

    Args:
        groupby: Количество результатов

    Returns:
        True если groupby валиден
    """
    return isinstance(groupby, int) and (1 <= groupby <= 10)


def validate_page(page: int, search_engine: str = "google") -> bool:
    """
    Валидация номера страницы

    Args:
        page: Номер страницы
        search_engine: Поисковая система

    Returns:
        True если номер страницы валиден
    """
    if not isinstance(page, int):
        return False
    if search_engine.lower() == "google":
        return page >= 1
    if search_engine.lower() == "yandex":
        return page >= 0

    return False


def validate_time_filter(time_filter: str) -> bool:
    """
    Валидация фильтра времени

    Args:
        time_filter: Фильтр времени

    Returns:
        True если фильтр валиден
    """
    valid_filters = ["qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"]
    return time_filter in valid_filters


def validate_within(within: int) -> bool:
    """
    Валидация параметра within для Яндекса

    Args:
        within: Период поиска

    Returns:
        True если within валиден
    """
    valid_values = [0, 1, 2, 77]
    return within in valid_values


def validate_file_type(file_type: str) -> bool:
    """
    Валидация типа файла

    Args:
        file_type: Тип файла

    Returns:
        True если тип файла валиден
    """
    valid_types = [
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "txt",
        "rtf",
        "odt",
        "ods",
        "odp",
        "csv",
        "xml",
        "html",
        "htm",
        "php",
        "asp",
        "jsp",
        "js",
        "css",
    ]

    if not isinstance(file_type, str):
        return False
    return file_type.lower() in valid_types


def validate_image_size(size: str) -> bool:
    """
    Валидация размера изображения

    Args:
        size: Размер изображения

    Returns:
        True если размер валиден
    """
    valid_sizes = ["small", "medium", "large", "xlarge"]
    if not isinstance(size, str):
        return False
    return size.lower() in valid_sizes


def validate_image_color(color: str) -> bool:
    """
    Валидация цвета изображения

    Args:
        color: Цвет изображения

    Returns:
        True если цвет валиден
    """
    valid_colors = [
        "any",
        "color",
        "grayscale",
        "transparent",
        "red",
        "orange",
        "yellow",
        "green",
        "teal",
        "blue",
        "purple",
        "pink",
        "white",
        "gray",
        "black",
        "brown",
    ]
    if not isinstance(color, str):
        return False
    return color.lower() in valid_colors


def validate_image_type(image_type: str) -> bool:
    """
    Валидация типа изображения

    Args:
        image_type: Тип изображения

    Returns:
        True если тип валиден
    """
    valid_types = ["any", "face", "photo", "clipart", "lineart", "animated"]
    if not isinstance(image_type, str):
        return False
    return image_type.lower() in valid_types


def validate_usage_rights(usage_rights: str) -> bool:
    """
    Валидация прав использования изображения

    Args:
        usage_rights: Права использования

    Returns:
        True если права валидны
    """
    valid_rights = [
        "any",
        "cc_publicdomain",
        "cc_attribute",
        "cc_sharealike",
        "cc_noncommercial",
        "cc_nonderived",
    ]
    if not isinstance(usage_rights, str):
        return False
    return usage_rights.lower() in valid_rights
