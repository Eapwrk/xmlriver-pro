"""
Базовый клиент для работы с XMLRiver API
"""

import time
import logging
from typing import Optional, Dict, Any, List

import requests
import xmltodict
from .exceptions import (
    XMLRiverError,
    NoResultsError,
    NetworkError,
    raise_xmlriver_error,
)
from .types import SearchResponse, SearchResult

logger = logging.getLogger(__name__)


class BaseClient:
    """Базовый клиент для работы с XMLRiver API"""

    def __init__(self, user_id: int, api_key: str, **kwargs: Any) -> None:
        """
        Инициализация клиента

        Args:
            user_id: ID пользователя XMLRiver
            api_key: API ключ
            **kwargs: Дополнительные параметры
        """
        self.user_id = user_id
        self.api_key = api_key
        self.base_params = {
            "user": self.user_id,
            "key": self.api_key,
        }
        self.base_params.update(kwargs)
        self.session = requests.Session()

        # Настройка логирования
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

    def _make_request(
        self, url: str, params: Dict[str, Any], max_retries: int = 3, timeout: int = 120
    ) -> Dict[str, Any]:
        """
        Выполнить запрос к API с обработкой ошибок

        Args:
            url: URL для запроса
            params: Параметры запроса
            max_retries: Максимальное количество попыток
            timeout: Таймаут запроса в секундах

        Returns:
            Словарь с ответом API

        Raises:
            XMLRiverError: При ошибках API
            NetworkError: При сетевых ошибках
        """
        attempt = 0

        while attempt < max_retries:
            try:
                logger.debug("Making request to %s with params: %s", url, params)
                response = self.session.get(url, params=params, timeout=timeout)

                if response.status_code == 200:
                    parsed = xmltodict.parse(response.text)
                    api_response = parsed["yandexsearch"]["response"]

                    if "error" in api_response:
                        error_code = int(api_response["error"]["@code"])
                        error_text = api_response["error"].get("#text", "")
                        logger.error("API error %s: %s", error_code, error_text)
                        raise_xmlriver_error(error_code, error_text)

                    logger.debug("Request successful")
                    return api_response

                logger.warning(
                    "HTTP %s, retry %s/%s",
                    response.status_code,
                    attempt + 1,
                    max_retries,
                )

            except requests.RequestException as e:
                logger.error("Request failed: %s", e)

            attempt += 1
            if attempt < max_retries:
                logger.info(
                    "Retrying in 10 seconds... (attempt %s/%s)",
                    attempt + 1,
                    max_retries,
                )
                time.sleep(10)

        raise NetworkError(999, "Max retries exceeded")

    def _parse_results(self, response: Dict[str, Any]) -> SearchResponse:
        """
        Парсинг результатов поиска

        Args:
            response: Ответ от API

        Returns:
            Объект SearchResponse с результатами
        """
        found = response.get("found", {})
        total = int(found.get("#text", 0)) if isinstance(found, dict) else 0

        groups = response.get("results", {}).get("grouping", {}).get("group", [])
        if not isinstance(groups, list):
            groups = [groups] if groups else []

        results = []
        for rank, group in enumerate(groups, 1):
            doc = group.get("doc", {})
            result = SearchResult(
                rank=rank,
                url=doc.get("url", ""),
                title=doc.get("title", ""),
                snippet=self._extract_snippet(doc),
                breadcrumbs=doc.get("breadcrumbs"),
                content_type=doc.get("contenttype", "organic"),
                pub_date=doc.get("pubDate"),
                extended_passage=doc.get("extendedpassage"),
                stars=self._extract_stars(doc),
                sitelinks=self._extract_sitelinks(doc),
                turbo_link=self._extract_turbo_link(doc),
            )
            results.append(result)

        return SearchResponse(
            query=response.get("query", ""),
            total_results=total,
            results=results,
            showing_results_for=response.get("showing_results_for"),
            correct=response.get("correct"),
            fixtype=response.get("fixtype"),
        )

    def _extract_snippet(self, doc: Dict[str, Any]) -> str:
        """Извлечение сниппета из документа"""
        passages = doc.get("passages", {})
        if isinstance(passages, dict):
            passage = passages.get("passage", [])
            if isinstance(passage, list) and passage:
                return passage[0]
            if isinstance(passage, str):
                return passage
        return ""

    def _extract_stars(self, doc: Dict[str, Any]) -> Optional[float]:
        """Извлечение рейтинга из документа"""
        stars = doc.get("stars")
        if stars:
            try:
                return float(stars.replace(",", "."))
            except (ValueError, AttributeError):
                pass
        return None

    def _extract_sitelinks(self, doc: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
        """Извлечение быстрых ссылок из документа"""
        sitelinks = doc.get("sitelinks", {}).get("sitelink", [])
        if isinstance(sitelinks, list):
            return [
                {
                    "url": link.get("url", ""),
                    "title": link.get("title", ""),
                    "snippet": link.get("snippet", ""),
                }
                for link in sitelinks
            ]
        return None

    def _extract_turbo_link(self, doc: Dict[str, Any]) -> Optional[str]:
        """Извлечение турбо-ссылки из документа"""
        properties = doc.get("properties", {})
        if isinstance(properties, dict):
            return properties.get("TurboLink")
        return None

    def get_balance(self) -> float:
        """
        Получить баланс аккаунта

        Returns:
            Баланс в рублях

        Raises:
            XMLRiverError: При ошибках API
        """
        url = "https://xmlriver.com/api/get_balance/"
        params = {"user": self.user_id, "key": self.api_key}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return float(response.text.strip())
        except requests.RequestException as e:
            logger.error("Failed to get balance: %s", e)
            raise NetworkError(999, f"Failed to get balance: {e}") from e
        except ValueError as e:
            logger.error("Invalid balance response: %s", e)
            raise XMLRiverError(999, "Invalid balance response") from e

    def get_cost(self, system: str = "google") -> float:
        """
        Получить стоимость за 1000 запросов

        Args:
            system: Система поиска ('google' или 'yandex')

        Returns:
            Стоимость в рублях за 1000 запросов

        Raises:
            XMLRiverError: При ошибках API
        """
        url = f"https://xmlriver.com/api/get_cost/{system}/"
        params = {"user": self.user_id, "key": self.api_key}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return float(response.text.strip())
        except requests.RequestException as e:
            logger.error("Failed to get cost: %s", e)
            raise NetworkError(999, f"Failed to get cost: {e}") from e
        except ValueError as e:
            logger.error("Invalid cost response: %s", e)
            raise XMLRiverError(999, "Invalid cost response") from e

    def check_indexing(self, url: str, strict: bool = False, **kwargs: Any) -> bool:
        """
        Проверить индексацию URL

        Args:
            url: URL для проверки
            strict: Строгое соответствие регистра
            **kwargs: Дополнительные параметры

        Returns:
            True если URL проиндексирован, False иначе
        """
        params = {"inindex": 1, "strict": int(strict)}
        params.update(kwargs)

        try:
            response = self.search(url, **params)
            return any(result.url == url for result in response.results)
        except NoResultsError:
            return False
