#!/usr/bin/env python3
"""
Примеры многопоточного использования XMLRiver Pro API
"""

import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from xmlriver_pro import GoogleClient, YandexClient
from xmlriver_pro.core import RateLimitError, NetworkError


def concurrent_search_example():
    """Пример многопоточного поиска с соблюдением лимитов"""
    
    # Инициализация клиентов
    google = GoogleClient(user_id=123, api_key="your_google_key")
    yandex = YandexClient(user_id=123, api_key="your_yandex_key")
    
    # Получаем информацию об ограничениях
    limits = google.get_api_limits()
    max_streams = limits['max_concurrent_streams']
    print(f"Максимум потоков: {max_streams}")
    
    # Список запросов для поиска
    queries = [
        "python programming",
        "machine learning",
        "data science",
        "web development",
        "artificial intelligence",
        "blockchain technology",
        "cloud computing",
        "mobile development",
        "cybersecurity",
        "devops"
    ]
    
    def search_google(query: str) -> Dict[str, Any]:
        """Поиск в Google с обработкой ошибок"""
        try:
            results = google.search(query)
            return {
                "query": query,
                "system": "google",
                "total_results": results.total_results,
                "returned": len(results.results),
                "success": True
            }
        except RateLimitError as e:
            print(f"Rate limit error for '{query}': {e}")
            return {"query": query, "system": "google", "error": str(e), "success": False}
        except Exception as e:
            print(f"Error searching '{query}': {e}")
            return {"query": query, "system": "google", "error": str(e), "success": False}
    
    def search_yandex(query: str) -> Dict[str, Any]:
        """Поиск в Yandex с обработкой ошибок"""
        try:
            results = yandex.search(query)
            return {
                "query": query,
                "system": "yandex", 
                "total_results": results.total_results,
                "returned": len(results.results),
                "success": True
            }
        except RateLimitError as e:
            print(f"Rate limit error for '{query}': {e}")
            return {"query": query, "system": "yandex", "error": str(e), "success": False}
        except Exception as e:
            print(f"Error searching '{query}': {e}")
            return {"query": query, "system": "yandex", "error": str(e), "success": False}
    
    # Многопоточный поиск с ограничением потоков
    results = []
    
    with ThreadPoolExecutor(max_workers=max_streams) as executor:
        # Запускаем поиск в Google
        google_futures = {
            executor.submit(search_google, query): query 
            for query in queries
        }
        
        # Запускаем поиск в Yandex
        yandex_futures = {
            executor.submit(search_yandex, query): query 
            for query in queries
        }
        
        # Собираем результаты Google
        for future in as_completed(google_futures):
            result = future.result()
            results.append(result)
            print(f"Google: {result['query']} - {result.get('total_results', 'error')} результатов")
        
        # Собираем результаты Yandex
        for future in as_completed(yandex_futures):
            result = future.result()
            results.append(result)
            print(f"Yandex: {result['query']} - {result.get('total_results', 'error')} результатов")
    
    # Статистика
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print(f"\n📊 Статистика:")
    print(f"Успешных запросов: {len(successful)}")
    print(f"Неудачных запросов: {len(failed)}")
    print(f"Общее время: {time.time() - start_time:.2f} секунд")
    
    return results


def adaptive_rate_limiting_example():
    """Пример адаптивного управления скоростью запросов"""
    
    google = GoogleClient(user_id=123, api_key="your_google_key")
    
    # Начальные настройки
    delay_between_requests = 1.0  # секунды
    max_delay = 10.0  # максимальная задержка
    min_delay = 0.1   # минимальная задержка
    
    queries = ["python", "javascript", "java", "c++", "go", "rust"]
    
    for i, query in enumerate(queries):
        try:
            print(f"Запрос {i+1}/{len(queries)}: {query}")
            results = google.search(query)
            print(f"  ✅ Успех: {results.total_results} результатов")
            
            # Уменьшаем задержку при успехе
            delay_between_requests = max(min_delay, delay_between_requests * 0.9)
            
        except RateLimitError as e:
            print(f"  ⚠️ Rate limit: {e}")
            
            # Увеличиваем задержку при ошибке лимита
            delay_between_requests = min(max_delay, delay_between_requests * 1.5)
            print(f"  ⏱️ Увеличиваем задержку до {delay_between_requests:.1f} сек")
            
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            
        # Задержка между запросами
        if i < len(queries) - 1:  # Не ждем после последнего запроса
            time.sleep(delay_between_requests)
    
    print(f"Финальная задержка: {delay_between_requests:.1f} секунд")


def batch_processing_example():
    """Пример пакетной обработки с контролем дневных лимитов"""
    
    google = GoogleClient(user_id=123, api_key="your_google_key")
    limits = google.get_api_limits()
    
    # Получаем дневные лимиты
    daily_limit = limits['daily_limits']['google']
    print(f"Дневной лимит Google: {daily_limit:,} запросов")
    
    # Большой список запросов (больше дневного лимита)
    all_queries = [f"query_{i}" for i in range(300_000)]  # 300k запросов
    
    # Разбиваем на батчи по дневному лимиту
    batch_size = daily_limit // 2  # Используем половину лимита для безопасности
    batches = [all_queries[i:i + batch_size] for i in range(0, len(all_queries), batch_size)]
    
    print(f"Создано батчей: {len(batches)}")
    print(f"Размер батча: {batch_size:,} запросов")
    
    total_processed = 0
    
    for batch_num, batch in enumerate(batches[:3]):  # Обрабатываем только первые 3 батча
        print(f"\n🔄 Обработка батча {batch_num + 1}/{len(batches)}")
        
        batch_results = []
        with ThreadPoolExecutor(max_workers=limits['max_concurrent_streams']) as executor:
            futures = {
                executor.submit(google.search, query): query 
                for query in batch[:10]  # Обрабатываем только первые 10 запросов для примера
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    batch_results.append(result)
                    total_processed += 1
                except Exception as e:
                    print(f"Ошибка в батче: {e}")
        
        print(f"Обработано запросов в батче: {len(batch_results)}")
        print(f"Всего обработано: {total_processed}")
        
        # Пауза между батчами (например, 1 час)
        if batch_num < len(batches) - 1:
            print("⏸️ Пауза между батчами...")
            time.sleep(1)  # В реальности здесь была бы пауза в час


if __name__ == "__main__":
    print("🚀 Примеры многопоточного использования XMLRiver Pro")
    print("=" * 60)
    
    start_time = time.time()
    
    print("\n1️⃣ Базовый многопоточный поиск:")
    concurrent_search_example()
    
    print("\n2️⃣ Адаптивное управление скоростью:")
    adaptive_rate_limiting_example()
    
    print("\n3️⃣ Пакетная обработка с контролем лимитов:")
    batch_processing_example()
    
    print(f"\n✅ Все примеры завершены за {time.time() - start_time:.2f} секунд")
