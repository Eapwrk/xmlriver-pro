"""
Форматтеры для XMLRiver Pro API
"""

from typing import Dict, Any, Union
from ..core.types import (
    SearchResult,
    SearchResponse,
    NewsResult,
    ImageResult,
    MapResult,
    AdResult,
    AdsResponse,
    OneBoxDocument,
    SearchsterResult,
    RelatedSearch,
)


def format_search_result(
    result: Union[SearchResult, NewsResult, ImageResult, MapResult, AdResult],
) -> Dict[str, Any]:
    """
    Форматирование результата поиска

    Args:
        result: Результат поиска

    Returns:
        Отформатированный словарь
    """
    return {
        "rank": result.rank if hasattr(result, "rank") else None,
        "url": result.url,
        "title": result.title,
        "snippet": result.snippet if hasattr(result, "snippet") else "",
        "breadcrumbs": (result.breadcrumbs if hasattr(result, "breadcrumbs") else None),
        "content_type": (
            result.content_type if hasattr(result, "content_type") else None
        ),
        "pub_date": result.pub_date if hasattr(result, "pub_date") else None,
        "extended_passage": (
            result.extended_passage if hasattr(result, "extended_passage") else None
        ),
        "stars": result.stars if hasattr(result, "stars") else None,
        "sitelinks": (result.sitelinks if hasattr(result, "sitelinks") else None),
        "turbo_link": (result.turbo_link if hasattr(result, "turbo_link") else None),
    }


def format_search_response(response: SearchResponse) -> Dict[str, Any]:
    """
    Форматирование ответа поиска

    Args:
        response: Ответ поиска

    Returns:
        Отформатированный словарь
    """
    return {
        "query": response.query,
        "total_results": response.total_results,
        "results": [format_search_result(result) for result in response.results],
        "showing_results_for": response.showing_results_for,
        "correct": response.correct,
        "fixtype": response.fixtype,
    }


def format_news_result(result: NewsResult) -> Dict[str, Any]:
    """
    Форматирование результата новостей

    Args:
        result: Результат новостей

    Returns:
        Отформатированный словарь
    """
    return {
        "rank": result.rank,
        "url": result.url,
        "title": result.title,
        "snippet": result.snippet,
        "media": result.media,
        "pub_date": result.pub_date,
    }


def format_image_result(result: ImageResult) -> Dict[str, Any]:
    """
    Форматирование результата изображения

    Args:
        result: Результат изображения

    Returns:
        Отформатированный словарь
    """
    return {
        "rank": result.rank,
        "url": result.url,
        "img_url": result.img_url,
        "title": result.title,
        "display_link": result.display_link,
        "original_width": result.original_width,
        "original_height": result.original_height,
    }


def format_map_result(result: MapResult) -> Dict[str, Any]:
    """
    Форматирование результата карт

    Args:
        result: Результат карт

    Returns:
        Отформатированный словарь
    """
    return {
        "title": result.title,
        "stars": result.stars,
        "type": result.type,
        "address": result.address,
        "url": result.url,
        "phone": result.phone,
        "review": result.review,
        "possibility": result.possibility,
        "latitude": result.latitude,
        "longitude": result.longitude,
        "place_id": result.place_id,
        "count_reviews": result.count_reviews,
        "accessibility": result.accessibility,
        "price": result.price,
        "gas_price": result.gas_price,
    }


def format_ads_result(result: AdResult) -> Dict[str, Any]:
    """
    Форматирование результата рекламы

    Args:
        result: Результат рекламы

    Returns:
        Отформатированный словарь
    """
    return {
        "url": result.url,
        "ads_url": result.ads_url,
        "title": result.title,
        "snippet": result.snippet,
    }


def format_ads_response(response: AdsResponse) -> Dict[str, Any]:
    """
    Форматирование ответа рекламы

    Args:
        response: Ответ рекламы

    Returns:
        Отформатированный словарь
    """
    return {
        "top_ads": [format_ads_result(ad) for ad in response.top_ads],
        "bottom_ads": [format_ads_result(ad) for ad in response.bottom_ads],
        "total_ads_count": len(response.top_ads) + len(response.bottom_ads),
    }


def format_onebox_document(doc: OneBoxDocument) -> Dict[str, Any]:
    """
    Форматирование OneBox документа

    Args:
        doc: OneBox документ

    Returns:
        Отформатированный словарь
    """
    return {
        "content_type": doc.content_type,
        "title": doc.title,
        "url": doc.url,
        "snippet": doc.snippet,
        "additional_data": doc.additional_data,
    }


def format_searchster_result(result: SearchsterResult) -> Dict[str, Any]:
    """
    Форматирование результата колдунщика

    Args:
        result: Результат колдунщика

    Returns:
        Отформатированный словарь
    """
    return {
        "content_type": result.content_type,
        "title": result.title,
        "url": result.url,
        "snippet": result.snippet,
        "additional_data": result.additional_data,
    }


def format_related_search(search: RelatedSearch) -> Dict[str, Any]:
    """
    Форматирование связанного поиска

    Args:
        search: Связанный поиск

    Returns:
        Отформатированный словарь
    """
    return {"query": search.query, "url": search.url}


def format_search_stats(response: SearchResponse) -> Dict[str, Any]:
    """
    Форматирование статистики поиска

    Args:
        response: Ответ поиска

    Returns:
        Статистика поиска
    """
    content_types: Dict[str, int] = {}
    for result in response.results:
        if hasattr(result, "content_type"):
            content_type = result.content_type
            content_types[content_type] = content_types.get(content_type, 0) + 1

    return {
        "total_results": response.total_results,
        "returned_results": len(response.results),
        "content_types": content_types,
        "has_corrections": response.correct is not None,
        "has_fixtype": response.fixtype is not None,
    }


def format_ads_stats(response: AdsResponse) -> Dict[str, Any]:
    """
    Форматирование статистики рекламы

    Args:
        response: Ответ рекламы

    Returns:
        Статистика рекламы
    """
    return {
        "top_ads_count": len(response.top_ads),
        "bottom_ads_count": len(response.bottom_ads),
        "total_ads_count": len(response.top_ads) + len(response.bottom_ads),
        "has_ads": (len(response.top_ads) + len(response.bottom_ads)) > 0,
    }


def format_results_summary(response: SearchResponse) -> str:
    """
    Форматирование краткого описания результатов

    Args:
        response: Ответ поиска

    Returns:
        Краткое описание
    """
    total = response.total_results
    returned = len(response.results)

    summary = f"Найдено {total:,} результатов, показано {returned}"

    if response.correct:
        summary += f" (исправлено с '{response.correct}')"

    if response.fixtype:
        summary += f" (тип исправления: {response.fixtype})"

    return summary


def format_ads_summary(response: AdsResponse) -> str:
    """
    Форматирование краткого описания рекламы

    Args:
        response: Ответ рекламы

    Returns:
        Краткое описание
    """
    top_count = len(response.top_ads)
    bottom_count = len(response.bottom_ads)
    total = top_count + bottom_count

    if total == 0:
        return "Реклама не найдена"

    summary = f"Найдено {total} рекламных блоков"
    if top_count > 0:
        summary += f" (верхние: {top_count})"
    if bottom_count > 0:
        summary += f" (нижние: {bottom_count})"

    return summary


def format_error_message(error: Exception) -> str:
    """
    Форматирование сообщения об ошибке

    Args:
        error: Исключение

    Returns:
        Отформатированное сообщение
    """
    if hasattr(error, "code") and hasattr(error, "message"):
        return f"[{error.code}] {error.message}"

    return str(error)


def format_api_response(response_data: Dict[str, Any]) -> str:
    """
    Форматирование ответа API для отображения

    Args:
        response_data: Данные ответа

    Returns:
        Отформатированная строка
    """
    if "error" in response_data:
        error = response_data["error"]
        code = error.get("@code", "unknown")
        message = error.get("#text", "Unknown error")
        return f"Ошибка API [{code}]: {message}"

    if "found" in response_data:
        found = response_data["found"]
        total = found.get("#text", 0) if isinstance(found, dict) else 0
        return f"Успешно получено {total} результатов"

    return "Ответ получен успешно"
