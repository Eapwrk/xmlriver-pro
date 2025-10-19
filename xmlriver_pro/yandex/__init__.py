"""
Yandex API модуль для XMLRiver Pro

Только асинхронный клиент.
"""

from .async_client import AsyncYandexClient

__all__ = [
    "AsyncYandexClient",
]
