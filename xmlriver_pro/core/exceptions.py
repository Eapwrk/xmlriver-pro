"""
Исключения для XMLRiver Pro API
"""

from typing import Optional


class XMLRiverError(Exception):
    """Базовое исключение для XMLRiver"""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class AuthenticationError(XMLRiverError):
    """Ошибка аутентификации"""


class RateLimitError(XMLRiverError):
    """Превышен лимит запросов"""


class NoResultsError(XMLRiverError):
    """Нет результатов поиска"""


class NetworkError(XMLRiverError):
    """Ошибка сети"""


class ValidationError(XMLRiverError):
    """Ошибка валидации параметров"""


class APIError(XMLRiverError):
    """Ошибка API"""


# Коды ошибок XMLRiver API
ERROR_CODES = {
    2: "Задан пустой поисковый запрос",
    15: "Для заданного поискового запроса отсутствуют результаты поиска",
    20: "Внутренняя ошибка. Обратитесь в службу поддержки",
    21: "Внутренняя ошибка. Обратитесь в службу поддержки",
    22: "Внутренняя ошибка. Обратитесь в службу поддержки",
    23: "Внутренняя ошибка. Обратитесь в службу поддержки",
    24: "Внутренняя ошибка. Обратитесь в службу поддержки",
    31: "Пользователь не зарегистрирован на сервисе",
    42: "Ключ, выданный при регистрации, содержит ошибку",
    45: "С вашего IP сбор запрещён",
    101: "Сервис сбора данных на обновлении. Попробуйте чуть позже",
    102: "Неверный параметр groupby",
    103: "Неверный параметр lr",
    104: "Неверный параметр loc",
    105: "Неверный параметр country",
    106: "Неверный параметр domain",
    107: "По Яндексу возможное значение ТОПа: 10",
    110: "Заняты все доступные вам каналы для сбора данных",
    111: "Нет свободных каналов для сбора данных",
    115: "Ваше ПО слишком часто отправляет большее количество параллельных запросов",
    120: "Недопустимые символы или операторы в запросе",
    200: "На вашем счету закончились деньги",
    201: "Ваше ПО не забирает ответы по запросам",
    500: "Ошибка сети. Повторите попытку",
    999: "Неизвестная ошибка",
}


def get_error_message(code: int) -> str:
    """Получить сообщение об ошибке по коду"""
    return ERROR_CODES.get(code, ERROR_CODES[999])


def raise_xmlriver_error(code: int, message: Optional[str] = None) -> None:
    """Вызвать соответствующее исключение по коду ошибки"""
    if message is None:
        message = get_error_message(code)

    if code == 15:  # Нет результатов
        raise NoResultsError(code, message)
    if code in [31, 42, 45]:  # Ошибки аутентификации
        raise AuthenticationError(code, message)
    if code in [110, 111, 115]:  # Лимиты
        raise RateLimitError(code, message)
    if code == 500:  # Ошибки сети
        raise NetworkError(code, message)
    if code in [102, 103, 104, 105, 106, 107, 120]:  # Ошибки валидации
        raise ValidationError(code, message)
    raise APIError(code, message)
