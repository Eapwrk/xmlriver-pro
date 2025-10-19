"""
Google API модуль для XMLRiver Pro

Только асинхронный клиент.
"""

from .async_client import AsyncGoogleClient

__all__ = [
    "AsyncGoogleClient",
]
