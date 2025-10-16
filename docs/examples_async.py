#!/usr/bin/env python3
"""
Примеры асинхронного использования XMLRiver Pro API

[← Назад к README](../README.md) • [Документация](README.md)
"""

import asyncio
import time
from typing import List, Dict, Any

from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient
from xmlriver_pro.core import RateLimitError, NetworkError


async def basic_async_search_example():
    """Базовый пример асинхронного поиска"""
    
    print("🚀 Базовый асинхронный поиск")
    print("=" * 40)
    
    # Используем async context manager с настройками по умолчанию
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        try:
            # Простой поиск
            results = await google.search("python programming")
            print(f"✅ Google: {results.total_results} результатов")
            print(f"   Время поиска: {results.search_time:.2f} сек")
            
            # Поиск новостей
            news = await google.search_news("artificial intelligence")
            print(f"✅ Новости: {news.total_results} результатов")
            
            # Поиск изображений
            images = await google.search_images("machine learning", num_results=5)
            print(f"✅ Изображения: {images.total_results} результатов")
            
        except RateLimitError as e:
            print(f"⚠️ Rate limit: {e}")
        except NetworkError as e:
            print(f"❌ Network error: {e}")


async def concurrent_async_search_example():
    """Пример параллельного асинхронного поиска"""
    
    print("\n🔄 Параллельный асинхронный поиск")
    print("=" * 40)
    
    queries = [
        "python programming",
        "machine learning",
        "data science",
        "web development",
        "artificial intelligence"
    ]
    
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        # Создаем задачи для параллельного выполнения
        tasks = [google.search(query) for query in queries]
        
        try:
            # Выполняем все задачи параллельно
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"❌ Запрос {i+1} ({queries[i]}): {result}")
                else:
                    print(f"✅ Запрос {i+1} ({queries[i]}): {result.total_results} результатов")
                    
        except Exception as e:
            print(f"❌ Общая ошибка: {e}")


async def mixed_google_yandex_example():
    """Пример одновременного поиска в Google и Yandex"""
    
    print("\n🌐 Смешанный поиск Google + Yandex")
    print("=" * 40)
    
    query = "программирование на python"
    
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google, \
             AsyncYandexClient(user_id=123, api_key="your_yandex_key") as yandex:
        
        # Создаем задачи для обеих систем
        google_task = google.search(query)
        yandex_task = yandex.search(query)
        
        try:
            # Выполняем поиск в обеих системах параллельно
            google_results, yandex_results = await asyncio.gather(
                google_task, yandex_task, return_exceptions=True
            )
            
            if isinstance(google_results, Exception):
                print(f"❌ Google: {google_results}")
            else:
                print(f"✅ Google: {google_results.total_results} результатов")
            
            if isinstance(yandex_results, Exception):
                print(f"❌ Yandex: {yandex_results}")
            else:
                print(f"✅ Yandex: {yandex_results.total_results} результатов")
                
        except Exception as e:
            print(f"❌ Общая ошибка: {e}")


async def adaptive_rate_limiting_async_example():
    """Пример адаптивного управления скоростью с асинхронностью"""
    
    print("\n⚡ Адаптивное управление скоростью (async)")
    print("=" * 40)
    
    queries = ["python", "javascript", "java", "c++", "go", "rust"]
    delay = 1.0  # Начальная задержка
    max_delay = 10.0
    min_delay = 0.1
    
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for i, query in enumerate(queries):
            try:
                print(f"Запрос {i+1}/{len(queries)}: {query}")
                results = await google.search(query)
                print(f"  ✅ Успех: {results.total_results} результатов")
                
                # Уменьшаем задержку при успехе
                delay = max(min_delay, delay * 0.9)
                
            except RateLimitError as e:
                print(f"  ⚠️ Rate limit: {e}")
                
                # Увеличиваем задержку при ошибке лимита
                delay = min(max_delay, delay * 1.5)
                print(f"  ⏱️ Увеличиваем задержку до {delay:.1f} сек")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
            
            # Задержка между запросами
            if i < len(queries) - 1:
                await asyncio.sleep(delay)
        
        print(f"Финальная задержка: {delay:.1f} секунд")


async def batch_processing_async_example():
    """Пример пакетной обработки с асинхронностью"""
    
    print("\n📦 Пакетная обработка (async)")
    print("=" * 40)
    
    # Получаем лимиты
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        limits = await google.get_api_limits()
        daily_limit = limits['daily_limits']['google']
        max_concurrent = limits['max_concurrent_streams']
        
        print(f"Дневной лимит Google: {daily_limit:,} запросов")
        print(f"Максимум потоков: {max_concurrent}")
        
        # Создаем список запросов
        queries = [f"query_{i}" for i in range(20)]  # 20 запросов для примера
        
        # Разбиваем на батчи
        batch_size = 5  # Маленькие батчи для примера
        batches = [queries[i:i + batch_size] for i in range(0, len(queries), batch_size)]
        
        print(f"Создано батчей: {len(batches)}")
        print(f"Размер батча: {batch_size} запросов")
        
        total_processed = 0
        
        for batch_num, batch in enumerate(batches):
            print(f"\n🔄 Обработка батча {batch_num + 1}/{len(batches)}")
            
            # Создаем семафор для ограничения одновременных запросов
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def process_query_with_semaphore(query):
                async with semaphore:
                    try:
                        result = await google.search(query)
                        return {"query": query, "success": True, "results": result.total_results}
                    except Exception as e:
                        return {"query": query, "success": False, "error": str(e)}
            
            # Обрабатываем батч параллельно
            tasks = [process_query_with_semaphore(query) for query in batch]
            batch_results = await asyncio.gather(*tasks)
            
            successful = [r for r in batch_results if r['success']]
            failed = [r for r in batch_results if not r['success']]
            
            print(f"  ✅ Успешных: {len(successful)}")
            print(f"  ❌ Неудачных: {len(failed)}")
            
            total_processed += len(successful)
            
            # Пауза между батчами
            if batch_num < len(batches) - 1:
                print("  ⏸️ Пауза между батчами...")
                await asyncio.sleep(1)
        
        print(f"\n📊 Всего обработано: {total_processed} запросов")


async def advanced_async_example():
    """Продвинутый пример с различными типами поиска"""
    
    print("\n🎯 Продвинутый асинхронный поиск")
    print("=" * 40)
    
    query = "artificial intelligence"
    
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        try:
            # Создаем задачи для разных типов поиска
            tasks = {
                "web": google.search(query, num_results=5),
                "news": google.search_news(query, num_results=5),
                "images": google.search_images(query, num_results=5),
                "maps": google.search_maps(query, num_results=5),
                "ads": google.get_ads(query, num_results=5),
                "special": google.get_special_blocks(query)
            }
            
            # Выполняем все типы поиска параллельно
            results = await asyncio.gather(*tasks.values(), return_exceptions=True)
            
            for task_name, result in zip(tasks.keys(), results):
                if isinstance(result, Exception):
                    print(f"❌ {task_name}: {result}")
                else:
                    print(f"✅ {task_name}: {result.total_results} результатов")
                    
        except Exception as e:
            print(f"❌ Общая ошибка: {e}")


async def retry_configuration_example():
    """Пример настройки retry механизма"""
    
    print("⚙️ Настройка retry механизма")
    print("=" * 40)
    
    # Кастомные настройки retry
    async with AsyncGoogleClient(
        user_id=123, 
        api_key="your_google_key",
        timeout=120,        # 2 минуты таймаут
        max_retries=5,      # 5 попыток
        retry_delay=2.0,    # базовая задержка 2 сек
        enable_retry=True   # включить retry
    ) as google:
        try:
            results = await google.search("machine learning")
            print(f"✅ Поиск с кастомными настройками: {results.total_results} результатов")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    # Отключение retry для продвинутых пользователей
    async with AsyncGoogleClient(
        user_id=123, 
        api_key="your_google_key",
        enable_retry=False  # без повторов
    ) as google:
        try:
            results = await google.search("deep learning")
            print(f"✅ Поиск без retry: {results.total_results} результатов")
        except Exception as e:
            print(f"❌ Ошибка (ожидаемо без retry): {e}")


async def main():
    """Главная функция с примерами"""
    
    print("🚀 Примеры асинхронного использования XMLRiver Pro")
    print("=" * 60)
    
    start_time = time.time()
    
    # Запускаем все примеры
    await basic_async_search_example()
    await concurrent_async_search_example()
    await mixed_google_yandex_example()
    await adaptive_rate_limiting_async_example()
    await batch_processing_async_example()
    await retry_configuration_example()
    await advanced_async_example()
    
    print(f"\n✅ Все примеры завершены за {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    # Запускаем асинхронную главную функцию
    asyncio.run(main())
