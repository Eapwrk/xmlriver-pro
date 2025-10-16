# Продвинутое использование

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md)

Продвинутые сценарии использования XMLRiver Pro для сложных задач.

## Содержание

- [Массовый поиск](#массовый-поиск)
- [Мониторинг позиций](#мониторинг-позиций)
- [Анализ конкурентов](#анализ-конкурентов)
- [Экспорт результатов](#экспорт-результатов)
- [Кэширование результатов](#кэширование-результатов)
- [Пакетная обработка](#пакетная-обработка)
- [Адаптивное управление скоростью](#адаптивное-управление-скоростью)
- [Мониторинг потоков](#мониторинг-потоков)

## Массовый поиск

### Синхронный массовый поиск

```python
import time
from xmlriver_pro import GoogleClient, YandexClient

def mass_search(queries, search_engines=["google", "yandex"]):
    """Массовый поиск по списку запросов"""
    results = {}
    
    if "google" in search_engines:
        google = GoogleClient(user_id=123, api_key="your_google_key")
        results["google"] = {}
        
        for query in queries:
            try:
                search_results = google.search(query)
                results["google"][query] = {
                    "total": search_results.total_results,
                    "returned": len(search_results.results),
                    "results": search_results.results
                }
                time.sleep(1)  # Задержка между запросами
            except Exception as e:
                results["google"][query] = {"error": str(e)}
    
    if "yandex" in search_engines:
        yandex = YandexClient(user_id=123, api_key="your_yandex_key")
        results["yandex"] = {}
        
        for query in queries:
            try:
                search_results = yandex.search(query)
                results["yandex"][query] = {
                    "total": search_results.total_results,
                    "returned": len(search_results.results),
                    "results": search_results.results
                }
                time.sleep(1)  # Задержка между запросами
            except Exception as e:
                results["yandex"][query] = {"error": str(e)}
    
    return results

# Использование
queries = ["python programming", "machine learning", "data science"]
results = mass_search(queries)

for engine, engine_results in results.items():
    print(f"\n{engine.upper()}:")
    for query, query_results in engine_results.items():
        if "error" in query_results:
            print(f"  {query}: Ошибка - {query_results['error']}")
        else:
            print(f"  {query}: {query_results['total']} результатов")
```

### Асинхронный массовый поиск

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def async_mass_search(queries, search_engines=["google", "yandex"]):
    """Асинхронный массовый поиск"""
    results = {}
    
    if "google" in search_engines:
        async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
            results["google"] = {}
            
            # Создаем задачи для параллельного выполнения
            tasks = [google.search(query) for query in queries]
            search_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for query, result in zip(queries, search_results):
                if isinstance(result, Exception):
                    results["google"][query] = {"error": str(result)}
                else:
                    results["google"][query] = {
                        "total": result.total_results,
                        "returned": len(result.results),
                        "results": result.results
                    }
    
    if "yandex" in search_engines:
        async with AsyncYandexClient(user_id=123, api_key="your_yandex_key") as yandex:
            results["yandex"] = {}
            
            # Создаем задачи для параллельного выполнения
            tasks = [yandex.search(query) for query in queries]
            search_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for query, result in zip(queries, search_results):
                if isinstance(result, Exception):
                    results["yandex"][query] = {"error": str(result)}
                else:
                    results["yandex"][query] = {
                        "total": result.total_results,
                        "returned": len(result.results),
                        "results": result.results
                    }
    
    return results

# Использование
async def main():
    queries = ["python programming", "machine learning", "data science"]
    results = await async_mass_search(queries)
    
    for engine, engine_results in results.items():
        print(f"\n{engine.upper()}:")
        for query, query_results in engine_results.items():
            if "error" in query_results:
                print(f"  {query}: Ошибка - {query_results['error']}")
            else:
                print(f"  {query}: {query_results['total']} результатов")

asyncio.run(main())
```

## Мониторинг позиций

### Отслеживание позиций URL по ключевым словам

```python
def monitor_positions(url, keywords, search_engines=["google", "yandex"]):
    """Мониторинг позиций URL по ключевым словам"""
    positions = {}
    
    if "google" in search_engines:
        google = GoogleClient(user_id=123, api_key="your_google_key")
        positions["google"] = {}
        
        for keyword in keywords:
            try:
                results = google.search(keyword)
                position = None
                for i, result in enumerate(results.results, 1):
                    if url in result.url:
                        position = i
                        break
                positions["google"][keyword] = position
            except Exception as e:
                positions["google"][keyword] = f"Ошибка: {e}"
    
    if "yandex" in search_engines:
        yandex = YandexClient(user_id=123, api_key="your_yandex_key")
        positions["yandex"] = {}
        
        for keyword in keywords:
            try:
                results = yandex.search(keyword)
                position = None
                for i, result in enumerate(results.results, 1):
                    if url in result.url:
                        position = i
                        break
                positions["yandex"][keyword] = position
            except Exception as e:
                positions["yandex"][keyword] = f"Ошибка: {e}"
    
    return positions

# Использование
url = "https://python.org"
keywords = ["python programming", "python tutorial", "python documentation"]
positions = monitor_positions(url, keywords)

for engine, engine_positions in positions.items():
    print(f"\n{engine.upper()}:")
    for keyword, position in engine_positions.items():
        if isinstance(position, int):
            print(f"  {keyword}: позиция {position}")
        else:
            print(f"  {keyword}: {position}")
```

### Асинхронный мониторинг позиций

```python
async def async_monitor_positions(url, keywords, search_engines=["google", "yandex"]):
    """Асинхронный мониторинг позиций"""
    positions = {}
    
    if "google" in search_engines:
        async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
            positions["google"] = {}
            
            # Создаем задачи для параллельного поиска
            tasks = [google.search(keyword) for keyword in keywords]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for keyword, result in zip(keywords, results):
                if isinstance(result, Exception):
                    positions["google"][keyword] = f"Ошибка: {result}"
                else:
                    position = None
                    for i, search_result in enumerate(result.results, 1):
                        if url in search_result.url:
                            position = i
                            break
                    positions["google"][keyword] = position
    
    if "yandex" in search_engines:
        async with AsyncYandexClient(user_id=123, api_key="your_yandex_key") as yandex:
            positions["yandex"] = {}
            
            # Создаем задачи для параллельного поиска
            tasks = [yandex.search(keyword) for keyword in keywords]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for keyword, result in zip(keywords, results):
                if isinstance(result, Exception):
                    positions["yandex"][keyword] = f"Ошибка: {result}"
                else:
                    position = None
                    for i, search_result in enumerate(result.results, 1):
                        if url in search_result.url:
                            position = i
                            break
                    positions["yandex"][keyword] = position
    
    return positions
```

## Анализ конкурентов

### Анализ конкурентов по ключевым словам

```python
def analyze_competitors(domain, keywords, search_engines=["google", "yandex"]):
    """Анализ конкурентов по ключевым словам"""
    analysis = {}
    
    if "google" in search_engines:
        google = GoogleClient(user_id=123, api_key="your_google_key")
        analysis["google"] = {}
        
        for keyword in keywords:
            try:
                results = google.search(keyword)
                competitors = []
                for result in results.results:
                    if domain not in result.url:
                        competitors.append({
                            "url": result.url,
                            "title": result.title,
                            "rank": result.rank
                        })
                analysis["google"][keyword] = competitors
            except Exception as e:
                analysis["google"][keyword] = f"Ошибка: {e}"
    
    if "yandex" in search_engines:
        yandex = YandexClient(user_id=123, api_key="your_yandex_key")
        analysis["yandex"] = {}
        
        for keyword in keywords:
            try:
                results = yandex.search(keyword)
                competitors = []
                for result in results.results:
                    if domain not in result.url:
                        competitors.append({
                            "url": result.url,
                            "title": result.title,
                            "rank": result.rank
                        })
                analysis["yandex"][keyword] = competitors
            except Exception as e:
                analysis["yandex"][keyword] = f"Ошибка: {e}"
    
    return analysis

# Использование
domain = "python.org"
keywords = ["python programming", "python tutorial", "python documentation"]
competitors = analyze_competitors(domain, keywords)

for engine, engine_competitors in competitors.items():
    print(f"\n{engine.upper()}:")
    for keyword, keyword_competitors in engine_competitors.items():
        if isinstance(keyword_competitors, list):
            print(f"  {keyword}:")
            for competitor in keyword_competitors[:5]:  # Топ-5
                print(f"    {competitor['rank']}. {competitor['title']}")
                print(f"       {competitor['url']}")
        else:
            print(f"  {keyword}: {keyword_competitors}")
```

## Экспорт результатов

### Экспорт в JSON

```python
import json
from datetime import datetime

def export_to_json(results, filename=None):
    """Экспорт результатов в JSON"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Результаты экспортированы в {filename}")

# Использование
results = mass_search(["python programming", "machine learning"])
export_to_json(results)
```

### Экспорт в CSV

```python
import csv
from datetime import datetime

def export_to_csv(results, filename=None):
    """Экспорт результатов в CSV"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_results_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Engine', 'Query', 'Rank', 'Title', 'URL', 'Snippet'])
        
        for engine, engine_results in results.items():
            for query, query_results in engine_results.items():
                if "error" not in query_results:
                    for result in query_results["results"]:
                        writer.writerow([
                            engine,
                            query,
                            result.rank,
                            result.title,
                            result.url,
                            result.snippet
                        ])
    
    print(f"Результаты экспортированы в {filename}")

# Использование
results = mass_search(["python programming", "machine learning"])
export_to_csv(results)
```

### Универсальный экспорт

```python
def export_results(results, format="json", filename=None):
    """Универсальный экспорт результатов"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_results_{timestamp}"
    
    if format == "json":
        filename += ".json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    elif format == "csv":
        filename += ".csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Engine', 'Query', 'Rank', 'Title', 'URL', 'Snippet'])
            
            for engine, engine_results in results.items():
                for query, query_results in engine_results.items():
                    if "error" not in query_results:
                        for result in query_results["results"]:
                            writer.writerow([
                                engine,
                                query,
                                result.rank,
                                result.title,
                                result.url,
                                result.snippet
                            ])
    
    print(f"Результаты экспортированы в {filename}")

# Использование
results = mass_search(["python programming", "machine learning"])
export_results(results, "json")
export_results(results, "csv")
```

## Кэширование результатов

### Простое кэширование

```python
import pickle
import os
from datetime import datetime, timedelta

class SearchCache:
    """Кэш для результатов поиска"""
    
    def __init__(self, cache_dir="cache", ttl_hours=24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.pkl")
    
    def _is_expired(self, cache_path):
        if not os.path.exists(cache_path):
            return True
        
        mtime = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - mtime > self.ttl
    
    def get(self, key):
        """Получить результат из кэша"""
        cache_path = self._get_cache_path(key)
        
        if self._is_expired(cache_path):
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None
    
    def set(self, key, value):
        """Сохранить результат в кэш"""
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            print(f"Ошибка сохранения в кэш: {e}")
    
    def clear(self):
        """Очистить кэш"""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.pkl'):
                os.remove(os.path.join(self.cache_dir, filename))

# Использование с кэшем
cache = SearchCache()

def cached_search(engine, query, **kwargs):
    """Поиск с кэшированием"""
    cache_key = f"{engine}_{query}_{hash(str(kwargs))}"
    
    # Проверяем кэш
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        print(f"Результат из кэша: {query}")
        return cached_result
    
    # Выполняем поиск
    if engine == "google":
        client = GoogleClient(user_id=123, api_key="your_google_key")
    elif engine == "yandex":
        client = YandexClient(user_id=123, api_key="your_yandex_key")
    else:
        raise ValueError(f"Неизвестная поисковая система: {engine}")
    
    result = client.search(query, **kwargs)
    
    # Сохраняем в кэш
    cache.set(cache_key, result)
    print(f"Результат сохранен в кэш: {query}")
    
    return result

# Использование
result1 = cached_search("google", "python programming")
result2 = cached_search("google", "python programming")  # Из кэша
result3 = cached_search("yandex", "программирование python")
```

## Пакетная обработка

### Синхронная пакетная обработка

```python
def batch_processing(queries, batch_size=10, delay_between_batches=5):
    """Пакетная обработка запросов"""
    results = []
    
    # Разбиваем на батчи
    batches = [queries[i:i + batch_size] for i in range(0, len(queries), batch_size)]
    
    google = GoogleClient(user_id=123, api_key="your_google_key")
    
    for batch_num, batch in enumerate(batches):
        print(f"Обработка батча {batch_num + 1}/{len(batches)}")
        
        batch_results = []
        for query in batch:
            try:
                result = google.search(query)
                batch_results.append({
                    "query": query,
                    "success": True,
                    "total_results": result.total_results,
                    "results": result.results
                })
            except Exception as e:
                batch_results.append({
                    "query": query,
                    "success": False,
                    "error": str(e)
                })
        
        results.extend(batch_results)
        
        # Пауза между батчами
        if batch_num < len(batches) - 1:
            print(f"Пауза {delay_between_batches} секунд...")
            time.sleep(delay_between_batches)
    
    return results

# Использование
queries = [f"query_{i}" for i in range(50)]  # 50 запросов
results = batch_processing(queries, batch_size=10, delay_between_batches=5)

successful = [r for r in results if r['success']]
failed = [r for r in results if not r['success']]

print(f"Успешных: {len(successful)}")
print(f"Неудачных: {len(failed)}")
```

### Асинхронная пакетная обработка

```python
async def async_batch_processing(queries, batch_size=10, delay_between_batches=5):
    """Асинхронная пакетная обработка"""
    results = []
    
    # Разбиваем на батчи
    batches = [queries[i:i + batch_size] for i in range(0, len(queries), batch_size)]
    
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for batch_num, batch in enumerate(batches):
            print(f"Обработка батча {batch_num + 1}/{len(batches)}")
            
            # Создаем задачи для батча
            tasks = [google.search(query) for query in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for query, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    results.append({
                        "query": query,
                        "success": False,
                        "error": str(result)
                    })
                else:
                    results.append({
                        "query": query,
                        "success": True,
                        "total_results": result.total_results,
                        "results": result.results
                    })
            
            # Пауза между батчами
            if batch_num < len(batches) - 1:
                print(f"Пауза {delay_between_batches} секунд...")
                await asyncio.sleep(delay_between_batches)
    
    return results

# Использование
async def main():
    queries = [f"query_{i}" for i in range(50)]  # 50 запросов
    results = await async_batch_processing(queries, batch_size=10, delay_between_batches=5)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"Успешных: {len(successful)}")
    print(f"Неудачных: {len(failed)}")

asyncio.run(main())
```

## Адаптивное управление скоростью

### Адаптивная задержка

```python
def adaptive_rate_limiting(queries, initial_delay=1.0, max_delay=10.0, min_delay=0.1):
    """Адаптивное управление скоростью запросов"""
    delay = initial_delay
    results = []
    
    google = GoogleClient(user_id=123, api_key="your_google_key")
    
    for i, query in enumerate(queries):
        try:
            print(f"Запрос {i+1}/{len(queries)}: {query}")
            result = google.search(query)
            results.append({
                "query": query,
                "success": True,
                "total_results": result.total_results
            })
            
            # Уменьшаем задержку при успехе
            delay = max(min_delay, delay * 0.9)
            
        except RateLimitError as e:
            print(f"Rate limit: {e}")
            
            # Увеличиваем задержку при ошибке лимита
            delay = min(max_delay, delay * 1.5)
            print(f"Увеличиваем задержку до {delay:.1f} сек")
            
            results.append({
                "query": query,
                "success": False,
                "error": str(e)
            })
            
        except Exception as e:
            print(f"Ошибка: {e}")
            results.append({
                "query": query,
                "success": False,
                "error": str(e)
            })
        
        # Задержка между запросами
        if i < len(queries) - 1:
            time.sleep(delay)
    
    print(f"Финальная задержка: {delay:.1f} секунд")
    return results

# Использование
queries = ["python", "javascript", "java", "c++", "go", "rust"]
results = adaptive_rate_limiting(queries)
```

### Асинхронное адаптивное управление

```python
async def async_adaptive_rate_limiting(queries, initial_delay=1.0, max_delay=10.0, min_delay=0.1):
    """Асинхронное адаптивное управление скоростью"""
    delay = initial_delay
    results = []
    
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for i, query in enumerate(queries):
            try:
                print(f"Запрос {i+1}/{len(queries)}: {query}")
                result = await google.search(query)
                results.append({
                    "query": query,
                    "success": True,
                    "total_results": result.total_results
                })
                
                # Уменьшаем задержку при успехе
                delay = max(min_delay, delay * 0.9)
                
            except RateLimitError as e:
                print(f"Rate limit: {e}")
                
                # Увеличиваем задержку при ошибке лимита
                delay = min(max_delay, delay * 1.5)
                print(f"Увеличиваем задержку до {delay:.1f} сек")
                
                results.append({
                    "query": query,
                    "success": False,
                    "error": str(e)
                })
                
            except Exception as e:
                print(f"Ошибка: {e}")
                results.append({
                    "query": query,
                    "success": False,
                    "error": str(e)
                })
            
            # Задержка между запросами
            if i < len(queries) - 1:
                await asyncio.sleep(delay)
    
    print(f"Финальная задержка: {delay:.1f} секунд")
    return results
```

## Мониторинг потоков

### Мониторинг асинхронных потоков

```python
async def monitor_concurrent_requests():
    """Мониторинг асинхронных потоков"""
    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        # Получаем начальный статус
        status = google.get_concurrent_status()
        print(f"Начальный статус: {status}")
        
        # Создаем много задач для тестирования
        queries = [f"query_{i}" for i in range(20)]
        tasks = [google.search(query) for query in queries]
        
        # Запускаем задачи
        print("Запускаем задачи...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Проверяем финальный статус
        final_status = google.get_concurrent_status()
        print(f"Финальный статус: {final_status}")
        
        # Анализируем результаты
        successful = [r for r in results if not isinstance(r, Exception)]
        failed = [r for r in results if isinstance(r, Exception)]
        
        print(f"Успешных: {len(successful)}")
        print(f"Неудачных: {len(failed)}")

# Использование
asyncio.run(monitor_concurrent_requests())
```

### Контроль лимитов потоков

```python
async def controlled_concurrent_requests(max_concurrent=5):
    """Контролируемые одновременные запросы"""
    async with AsyncGoogleClient(
        user_id=123, 
        api_key="your_google_key",
        max_concurrent=max_concurrent
    ) as google:
        
        queries = [f"query_{i}" for i in range(20)]
        
        # Создаем семафор для дополнительного контроля
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def controlled_search(query):
            async with semaphore:
                try:
                    result = await google.search(query)
                    return {"query": query, "success": True, "result": result}
                except Exception as e:
                    return {"query": query, "success": False, "error": str(e)}
        
        # Запускаем контролируемые задачи
        tasks = [controlled_search(query) for query in queries]
        results = await asyncio.gather(*tasks)
        
        # Анализируем результаты
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"Успешных: {len(successful)}")
        print(f"Неудачных: {len(failed)}")
        
        # Проверяем статус семафора
        status = google.get_concurrent_status()
        print(f"Статус семафора: {status}")

# Использование
asyncio.run(controlled_concurrent_requests(max_concurrent=3))
```

---

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md) • [Специальные блоки](SPECIAL_BLOCKS_GUIDE.md)
