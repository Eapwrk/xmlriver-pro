"""
Yandex Special Blocks API для XMLRiver Pro
"""

from typing import List, Optional, Dict, Any
from ..core.base_client import BaseClient
from ..core.types import SearchsterResult, RelatedSearch


class YandexSpecialBlocks(BaseClient):
    """Клиент для работы со специальными блоками Яндекс (колдунщики)"""

    BASE_URL = "https://xmlriver.com/search_yandex/xml"

    def get_searchsters(
        self, query: str, types: List[str], **kwargs
    ) -> List[SearchsterResult]:
        """
        Получить колдунщики Яндекса

        Args:
            query: Поисковый запрос
            types: Список типов колдунщиков (organic, address, afisha, avia,
                businessChatCenter, calculator, colors, converter, convertercurrency,
                fact, formula, images, index, ipaddress, lyrics, maps, market,
                misspell, music, news, quotes, shedule, sportscore, time, translate,
                uslugi, video, weather)
            **kwargs: Дополнительные параметры

        Returns:
            Список колдунщиков
        """
        response = self.search(query, **kwargs)

        searchsters = []
        for result in response.results:
            if result.content_type in types:
                searchster = SearchsterResult(
                    content_type=result.content_type,
                    title=result.title,
                    url=result.url,
                    snippet=result.snippet,
                    additional_data={
                        "breadcrumbs": result.breadcrumbs,
                        "pub_date": result.pub_date,
                        "extended_passage": result.extended_passage,
                        "stars": result.stars,
                        "sitelinks": result.sitelinks,
                        "turbo_link": result.turbo_link,
                    },
                )
                searchsters.append(searchster)

        return searchsters

    def get_weather(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить информацию о погоде

        Args:
            query: Запрос о погоде (например, "погода Москва")
            **kwargs: Дополнительные параметры

        Returns:
            Информация о погоде или None
        """
        searchsters = self.get_searchsters(query, ["weather"], **kwargs)

        if searchsters:
            return {
                "location": query,
                "weather_info": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_calculator(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить результат калькулятора

        Args:
            query: Математическое выражение
            **kwargs: Дополнительные параметры

        Returns:
            Результат калькулятора или None
        """
        searchsters = self.get_searchsters(query, ["calculator"], **kwargs)

        if searchsters:
            return {
                "expression": query,
                "result": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_translator(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить результат переводчика

        Args:
            query: Текст для перевода
            **kwargs: Дополнительные параметры

        Returns:
            Результат перевода или None
        """
        searchsters = self.get_searchsters(query, ["translate"], **kwargs)

        if searchsters:
            return {
                "original_text": query,
                "translation": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_currency_converter(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить результат конвертера валют

        Args:
            query: Запрос конвертации (например, "100 USD to RUB")
            **kwargs: Дополнительные параметры

        Returns:
            Результат конвертации или None
        """
        searchsters = self.get_searchsters(
            query, ["converter", "convertercurrency"], **kwargs
        )

        if searchsters:
            return {
                "conversion_query": query,
                "result": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_time(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить информацию о времени

        Args:
            query: Запрос о времени (например, "время в Лондоне")
            **kwargs: Дополнительные параметры

        Returns:
            Информация о времени или None
        """
        searchsters = self.get_searchsters(query, ["time"], **kwargs)

        if searchsters:
            return {
                "location_query": query,
                "time_info": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_ip_address(
        self, query: str = "мой ip", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Получить IP адрес

        Args:
            query: Запрос об IP адресе
            **kwargs: Дополнительные параметры

        Returns:
            Информация об IP адресе или None
        """
        searchsters = self.get_searchsters(query, ["ipaddress"], **kwargs)

        if searchsters:
            return {
                "ip_query": query,
                "ip_info": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_maps(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить информацию с карт

        Args:
            query: Запрос о местоположении
            **kwargs: Дополнительные параметры

        Returns:
            Информация с карт или None
        """
        searchsters = self.get_searchsters(query, ["maps"], **kwargs)

        if searchsters:
            return {
                "location_query": query,
                "maps_info": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_music(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить информацию о музыке

        Args:
            query: Запрос о музыке
            **kwargs: Дополнительные параметры

        Returns:
            Информация о музыке или None
        """
        searchsters = self.get_searchsters(query, ["music"], **kwargs)

        if searchsters:
            return {
                "music_query": query,
                "music_info": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_lyrics(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить текст песни

        Args:
            query: Запрос о тексте песни
            **kwargs: Дополнительные параметры

        Returns:
            Текст песни или None
        """
        searchsters = self.get_searchsters(query, ["lyrics"], **kwargs)

        if searchsters:
            return {
                "song_query": query,
                "lyrics": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_quotes(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить цитаты

        Args:
            query: Запрос о цитатах
            **kwargs: Дополнительные параметры

        Returns:
            Цитаты или None
        """
        searchsters = self.get_searchsters(query, ["quotes"], **kwargs)

        if searchsters:
            return {
                "quotes_query": query,
                "quotes": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_facts(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить факты

        Args:
            query: Запрос о фактах
            **kwargs: Дополнительные параметры

        Returns:
            Факты или None
        """
        searchsters = self.get_searchsters(query, ["fact"], **kwargs)

        if searchsters:
            return {
                "fact_query": query,
                "facts": searchsters[0].snippet,
                "additional_data": searchsters[0].additional_data,
            }

        return None

    def get_related_searches(self, query: str, **kwargs) -> List[RelatedSearch]:
        """
        Получить связанные поисковые запросы

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Список связанных запросов
        """
        response = self._make_request(
            self.BASE_URL, {**self.base_params, "query": query, **kwargs}
        )

        related_searches = []
        rs_data = response.get("related_searches", {})
        if rs_data:
            items = rs_data.get("item", [])
            if not isinstance(items, list):
                items = [items] if items else []

            for item in items:
                related_search = RelatedSearch(
                    query=item.get("query", ""), url=item.get("url")
                )
                related_searches.append(related_search)

        return related_searches
