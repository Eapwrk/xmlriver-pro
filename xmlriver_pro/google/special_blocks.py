"""
Google Special Blocks API для XMLRiver Pro
"""

from typing import List, Optional, Dict, Any
from ..core.base_client import BaseClient
from ..core.types import OneBoxDocument, KnowledgeGraph, RelatedSearch


class GoogleSpecialBlocks(BaseClient):
    """Клиент для работы со специальными блоками Google"""

    BASE_URL = "http://xmlriver.com/search/xml"

    def get_onebox_documents(
        self, query: str, types: List[str], **kwargs
    ) -> List[OneBoxDocument]:
        """
        Получить OneBox документы

        Args:
            query: Поисковый запрос
            types: Список типов OneBox (organic, video, images, news,
                   calculator, recipes, translator, related_queries)
            **kwargs: Дополнительные параметры

        Returns:
            Список OneBox документов
        """
        response = self.search(query, **kwargs)  # pylint: disable=no-member

        onebox_docs = []
        for result in response.results:
            if result.content_type in types:
                doc = OneBoxDocument(
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
                    },
                )
                onebox_docs.append(doc)

        return onebox_docs

    def get_knowledge_graph(self, query: str, **kwargs) -> Optional[KnowledgeGraph]:
        """
        Получить Knowledge Graph данные

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Knowledge Graph данные или None
        """
        # Для Knowledge Graph нужен специальный параметр ai=1
        params = {"ai": 1}
        params.update(kwargs)

        response = self._make_request(
            self.BASE_URL, {**self.base_params, "query": query, **params}
        )

        # Парсинг Knowledge Graph из ответа
        # Это упрощенная реализация, в реальности нужен более сложный парсинг
        knowledge_graph = response.get("knowledge_graph")
        if knowledge_graph:
            return KnowledgeGraph(
                entity_name=knowledge_graph.get("entity_name", ""),
                description=knowledge_graph.get("description", ""),
                image_url=knowledge_graph.get("image_url"),
                additional_info=knowledge_graph,
            )

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

    def get_answer_box(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить блок ответов

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры

        Returns:
            Данные блока ответов или None
        """
        response = self._make_request(
            self.BASE_URL, {**self.base_params, "query": query, **kwargs}
        )

        answer_box = response.get("answer_box")
        if answer_box:
            return {
                "answer": answer_box.get("answer", ""),
                "source": answer_box.get("source", ""),
                "url": answer_box.get("url", ""),
                "additional_info": answer_box,
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
        onebox_docs = self.get_onebox_documents(query, ["calculator"], **kwargs)

        if onebox_docs:
            return {
                "expression": query,
                "result": onebox_docs[0].snippet,
                "additional_data": onebox_docs[0].additional_data,
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
        onebox_docs = self.get_onebox_documents(query, ["translator"], **kwargs)

        if onebox_docs:
            return {
                "original_text": query,
                "translation": onebox_docs[0].snippet,
                "additional_data": onebox_docs[0].additional_data,
            }

        return None

    def get_weather(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Получить информацию о погоде

        Args:
            query: Запрос о погоде (например, "погода Москва")
            **kwargs: Дополнительные параметры

        Returns:
            Информация о погоде или None
        """
        onebox_docs = self.get_onebox_documents(query, ["weather"], **kwargs)

        if onebox_docs:
            return {
                "location": query,
                "weather_info": onebox_docs[0].snippet,
                "additional_data": onebox_docs[0].additional_data,
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
        onebox_docs = self.get_onebox_documents(query, ["converter"], **kwargs)

        if onebox_docs:
            return {
                "conversion_query": query,
                "result": onebox_docs[0].snippet,
                "additional_data": onebox_docs[0].additional_data,
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
        onebox_docs = self.get_onebox_documents(query, ["time"], **kwargs)

        if onebox_docs:
            return {
                "location_query": query,
                "time_info": onebox_docs[0].snippet,
                "additional_data": onebox_docs[0].additional_data,
            }

        return None
