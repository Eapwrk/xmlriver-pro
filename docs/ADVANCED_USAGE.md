# Продвинутое использование

[← Назад к README](../README.md) • [Документация](README.md) • [API Reference](API_REFERENCE.md)

Продвинутые сценарии использования XMLRiver Pro для сложных задач.

## Содержание

- [Массовый поиск](#массовый-поиск)
- [Мониторинг позиций](#мониторинг-позиций)
- [Анализ конкурентов](#анализ-конкурентов)
- [Анализ семантического ядра с Wordstat](#анализ-семантического-ядра-с-wordstat)
- [Экспорт результатов](#экспорт-результатов)
- [Кэширование результатов](#кэширование-результатов)
- [Пакетная обработка](#пакетная-обработка)
- [Адаптивное управление скоростью](#адаптивное-управление-скоростью)
- [Мониторинг потоков](#мониторинг-потоков)

## Массовый поиск

### Асинхронный массовый поиск

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def mass_search(queries, search_engines=["google", "yandex"]):
    """Асинхронный массовый поиск по списку запросов"""
    results = {}

    if "google" in search_engines:
        async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
            results["google"] = {}

            for query in queries:
                try:
                    search_results = await google.search(query)
                    results["google"][query] = {
                        "total": search_results.total_results,
                        "returned": len(search_results.results),
                        "results": search_results.results
                    }
                    await asyncio.sleep(1)  # Задержка между запросами
                except Exception as e:
                    results["google"][query] = {"error": str(e)}

    if "yandex" in search_engines:
        async with AsyncYandexClient(user_id=123, api_key="your_yandex_key") as yandex:
            results["yandex"] = {}

            for query in queries:
                try:
                    search_results = await yandex.search(query)
                    results["yandex"][query] = {
                        "total": search_results.total_results,
                        "returned": len(search_results.results),
                        "results": search_results.results
                    }
                    await asyncio.sleep(1)  # Задержка между запросами
                except Exception as e:
                    results["yandex"][query] = {"error": str(e)}

    return results

# Использование
async def main():
    queries = ["python programming", "machine learning", "data science"]
    results = await mass_search(queries)
    print(f"Обработано {len(queries)} запросов")

asyncio.run(main())
```

### Параллельный массовый поиск

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

async def parallel_mass_search(queries, search_engines=["google", "yandex"]):
    """Параллельный массовый поиск с семафором"""
    results = {}
    semaphore = asyncio.Semaphore(5)  # Максимум 5 одновременных запросов

    async def search_query(client, query, engine):
        async with semaphore:
            try:
                search_results = await client.search(query)
                return {
                    "engine": engine,
                    "query": query,
                    "total": search_results.total_results,
                    "returned": len(search_results.results),
                    "results": search_results.results
                }
            except Exception as e:
                return {
                    "engine": engine,
                    "query": query,
                    "error": str(e)
                }

    tasks = []

    if "google" in search_engines:
        async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
            for query in queries:
                task = search_query(google, query, "google")
                tasks.append(task)

    if "yandex" in search_engines:
        async with AsyncYandexClient(user_id=123, api_key="your_yandex_key") as yandex:
            for query in queries:
                task = search_query(yandex, query, "yandex")
                tasks.append(task)

    # Выполняем все задачи параллельно
    results = await asyncio.gather(*tasks)
    return results

# Использование
async def main():
    queries = ["python", "javascript", "java", "c++", "go"]
    results = await parallel_mass_search(queries)

    for result in results:
        if "error" in result:
            print(f"Ошибка {result['engine']} для '{result['query']}': {result['error']}")
        else:
            print(f"{result['engine']} - '{result['query']}': {result['total']} результатов")

asyncio.run(main())
```

## Мониторинг позиций

### Отслеживание позиций сайта

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient
from datetime import datetime

async def monitor_positions(domain, keywords, days=30):
    """Мониторинг позиций сайта по ключевым словам"""
    positions = {}

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for keyword in keywords:
            try:
                results = await google.search(keyword, num_results=100)

                # Ищем домен в результатах
                position = None
                for i, result in enumerate(results.results, 1):
                    if domain in result.url:
                        position = i
                        break

                positions[keyword] = {
                    "position": position,
                    "total_results": results.total_results,
                    "date": datetime.now().isoformat(),
                    "url": result.url if position else None
                }

                await asyncio.sleep(2)  # Задержка между запросами

            except Exception as e:
                positions[keyword] = {"error": str(e)}

    return positions

# Использование
async def main():
    domain = "python.org"
    keywords = ["python programming", "python tutorial", "python documentation"]

    positions = await monitor_positions(domain, keywords)

    for keyword, data in positions.items():
        if "error" in data:
            print(f"Ошибка для '{keyword}': {data['error']}")
        else:
            pos = data["position"]
            if pos:
                print(f"'{keyword}': позиция {pos} из {data['total_results']}")
            else:
                print(f"'{keyword}': не найдено в топ-100")

asyncio.run(main())
```

## Анализ конкурентов

### Сравнение с конкурентами

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient
from collections import defaultdict

async def analyze_competitors(keywords, competitors):
    """Анализ позиций конкурентов по ключевым словам"""
    analysis = {}

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for keyword in keywords:
            try:
                results = await google.search(keyword, num_results=50)

                competitor_positions = {}
                for competitor in competitors:
                    positions = []
                    for i, result in enumerate(results.results, 1):
                        if competitor in result.url:
                            positions.append(i)

                    competitor_positions[competitor] = positions

                analysis[keyword] = {
                    "total_results": results.total_results,
                    "competitor_positions": competitor_positions,
                    "top_10_domains": [result.url for result in results.results[:10]]
                }

                await asyncio.sleep(2)

            except Exception as e:
                analysis[keyword] = {"error": str(e)}

    return analysis

# Использование
async def main():
    keywords = ["python web framework", "python api", "python testing"]
    competitors = ["django.com", "flask.palletsprojects.com", "fastapi.tiangolo.com"]

    analysis = await analyze_competitors(keywords, competitors)

    for keyword, data in analysis.items():
        if "error" in data:
            print(f"Ошибка для '{keyword}': {data['error']}")
        else:
            print(f"\n'{keyword}':")
            for competitor, positions in data["competitor_positions"].items():
                if positions:
                    print(f"  {competitor}: позиции {positions}")
                else:
                    print(f"  {competitor}: не найдено в топ-50")

asyncio.run(main())
```

## Анализ семантического ядра с Wordstat

### Сбор семантического ядра

```python
import asyncio
from xmlriver_pro import AsyncWordstatClient
from typing import Set, List
import json

async def collect_semantic_core(
    seed_keywords: List[str],
    region: int = 213,  # Москва
    device: str = "desktop",
    min_frequency: int = 100,
    depth: int = 2
) -> dict:
    """
    Сбор семантического ядра на основе seed keywords
    
    Args:
        seed_keywords: Начальные ключевые слова
        region: ID региона Яндекса
        device: Тип устройства
        min_frequency: Минимальная частотность запроса
        depth: Глубина расширения (сколько уровней ассоциаций)
    """
    all_keywords = {}
    processed = set()
    to_process = set(seed_keywords)
    
    async with AsyncWordstatClient(user_id=123, api_key="key") as client:
        for level in range(depth):
            print(f"\n📊 Уровень {level + 1}/{depth}")
            print(f"Обработка {len(to_process)} запросов...")
            
            next_level = set()
            
            for keyword in to_process:
                if keyword in processed:
                    continue
                    
                try:
                    # Получаем частотность
                    frequency = await client.get_frequency(
                        keyword,
                        regions=region,
                        device=device
                    )
                    
                    # Фильтруем по минимальной частотности
                    if frequency < min_frequency:
                        processed.add(keyword)
                        continue
                    
                    # Получаем ассоциации
                    result = await client.get_words(
                        keyword,
                        regions=region,
                        device=device
                    )
                    
                    # Сохраняем результаты
                    all_keywords[keyword] = {
                        "frequency": frequency,
                        "level": level + 1,
                        "associations": [
                            {
                                "text": kw.text,
                                "value": kw.value
                            }
                            for kw in result.associations
                            if kw.value >= min_frequency
                        ][:10]  # Топ-10
                    }
                    
                    # Добавляем ассоциации для следующего уровня
                    for kw in result.associations[:5]:  # Топ-5 для расширения
                        if kw.value >= min_frequency and kw.text not in processed:
                            next_level.add(kw.text)
                    
                    processed.add(keyword)
                    print(f"✅ {keyword}: {frequency:,} запросов")
                    
                    await asyncio.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    print(f"❌ {keyword}: {e}")
                    processed.add(keyword)
            
            to_process = next_level
            
            if not to_process:
                print("Больше нет запросов для расширения")
                break
    
    return all_keywords

# Использование
async def main():
    seed_keywords = ["купить телефон", "смартфон"]
    
    semantic_core = await collect_semantic_core(
        seed_keywords=seed_keywords,
        region=213,  # Москва
        min_frequency=1000,
        depth=2
    )
    
    # Сохраняем результаты
    with open("semantic_core.json", "w", encoding="utf-8") as f:
        json.dump(semantic_core, f, ensure_ascii=False, indent=2)
    
    print(f"\n📈 Собрано {len(semantic_core)} запросов")
    
    # Статистика по уровням
    by_level = {}
    total_freq = 0
    for kw, data in semantic_core.items():
        level = data["level"]
        by_level[level] = by_level.get(level, 0) + 1
        total_freq += data["frequency"]
    
    print("\n📊 Статистика:")
    for level, count in sorted(by_level.items()):
        print(f"  Уровень {level}: {count} запросов")
    print(f"  Суммарная частотность: {total_freq:,}")

asyncio.run(main())
```

### Кластеризация запросов

```python
import asyncio
from xmlriver_pro import AsyncWordstatClient
from typing import List, Dict
import json

async def cluster_keywords(keywords: List[str], region: int = 213) -> Dict:
    """
    Кластеризация запросов на основе пересечения ассоциаций
    """
    keyword_data = {}
    
    async with AsyncWordstatClient(user_id=123, api_key="key") as client:
        print("📊 Сбор данных по запросам...")
        
        for keyword in keywords:
            try:
                result = await client.get_words(keyword, regions=region)
                frequency = await client.get_frequency(keyword, regions=region)
                
                keyword_data[keyword] = {
                    "frequency": frequency,
                    "associations": set(kw.text for kw in result.associations[:20])
                }
                
                print(f"✅ {keyword}: {frequency:,} запросов")
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ {keyword}: {e}")
    
    # Кластеризация
    clusters = []
    processed = set()
    
    for kw1 in keywords:
        if kw1 in processed or kw1 not in keyword_data:
            continue
        
        cluster = {
            "core_keyword": kw1,
            "frequency": keyword_data[kw1]["frequency"],
            "related": []
        }
        
        # Ищем похожие запросы
        for kw2 in keywords:
            if kw2 == kw1 or kw2 in processed or kw2 not in keyword_data:
                continue
            
            # Вычисляем пересечение ассоциаций
            intersection = keyword_data[kw1]["associations"] & keyword_data[kw2]["associations"]
            similarity = len(intersection) / min(
                len(keyword_data[kw1]["associations"]),
                len(keyword_data[kw2]["associations"])
            ) if keyword_data[kw1]["associations"] and keyword_data[kw2]["associations"] else 0
            
            # Если сходство > 30%, добавляем в кластер
            if similarity > 0.3:
                cluster["related"].append({
                    "keyword": kw2,
                    "frequency": keyword_data[kw2]["frequency"],
                    "similarity": round(similarity * 100, 1)
                })
                processed.add(kw2)
        
        clusters.append(cluster)
        processed.add(kw1)
    
    return {
        "clusters": sorted(clusters, key=lambda x: x["frequency"], reverse=True),
        "total_keywords": len(keywords),
        "clusters_count": len(clusters)
    }

# Использование
async def main():
    keywords = [
        "купить телефон",
        "смартфон цена",
        "телефон недорого",
        "мобильный телефон",
        "купить смартфон",
        "айфон цена",
        "samsung телефон",
    ]
    
    result = await cluster_keywords(keywords, region=213)
    
    # Сохраняем результаты
    with open("keyword_clusters.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 Кластеризация завершена:")
    print(f"  Всего запросов: {result['total_keywords']}")
    print(f"  Создано кластеров: {result['clusters_count']}")
    
    print("\n🔍 Топ-3 кластера:")
    for i, cluster in enumerate(result["clusters"][:3], 1):
        print(f"\n{i}. {cluster['core_keyword']} ({cluster['frequency']:,} запросов)")
        for rel in cluster["related"][:3]:
            print(f"   └─ {rel['keyword']} ({rel['similarity']}% схожесть)")

asyncio.run(main())
```

### Анализ сезонности

```python
import asyncio
from xmlriver_pro import AsyncWordstatClient
from datetime import datetime, timedelta
import json

async def analyze_seasonality(
    keywords: List[str],
    region: int = 213,
    months: int = 12
) -> Dict:
    """
    Анализ сезонности запросов за последние N месяцев
    """
    # Вычисляем диапазон дат
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)
    
    results = {}
    
    async with AsyncWordstatClient(user_id=123, api_key="key") as client:
        print(f"📊 Анализ сезонности за {months} месяцев")
        print(f"Период: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}\n")
        
        for keyword in keywords:
            try:
                # Получаем динамику по месяцам
                history = await client.get_history(
                    keyword,
                    regions=region,
                    period="month",
                    start=start_date.strftime("%d.%m.%Y"),
                    end=end_date.strftime("%d.%m.%Y")
                )
                
                # Анализируем данные
                values = [point.absolute_value for point in history.history]
                avg_value = sum(values) / len(values) if values else 0
                max_value = max(values) if values else 0
                min_value = min(values) if values else 0
                
                # Определяем пиковый месяц
                peak_month = max(history.history, key=lambda x: x.absolute_value) if history.history else None
                
                results[keyword] = {
                    "total_frequency": history.total_value,
                    "average_monthly": int(avg_value),
                    "max_monthly": max_value,
                    "min_monthly": min_value,
                    "peak_month": peak_month.date if peak_month else None,
                    "volatility": round((max_value - min_value) / avg_value * 100, 1) if avg_value else 0,
                    "history": [
                        {"date": point.date, "value": point.absolute_value}
                        for point in history.history
                    ]
                }
                
                print(f"✅ {keyword}:")
                print(f"   Средняя частотность: {int(avg_value):,}/мес")
                print(f"   Волатильность: {results[keyword]['volatility']}%")
                if peak_month:
                    print(f"   Пик: {peak_month.date} ({peak_month.absolute_value:,})")
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ {keyword}: {e}")
                results[keyword] = {"error": str(e)}
    
    return results

# Использование
async def main():
    keywords = ["купить елку", "кондиционер", "зимняя резина"]
    
    seasonality = await analyze_seasonality(keywords, months=12)
    
    # Сохраняем результаты
    with open("seasonality_analysis.json", "w", encoding="utf-8") as f:
        json.dump(seasonality, f, ensure_ascii=False, indent=2)
    
    print("\n📈 Анализ завершен!")
    print("\n🔥 Самые волатильные запросы:")
    volatile = sorted(
        [(k, v["volatility"]) for k, v in seasonality.items() if "volatility" in v],
        key=lambda x: x[1],
        reverse=True
    )
    for keyword, vol in volatile[:5]:
        print(f"  {keyword}: {vol}%")

asyncio.run(main())
```

**См. также:** [WORDSTAT_GUIDE.md](WORDSTAT_GUIDE.md) - полное руководство по Wordstat API

## Экспорт результатов

### Экспорт в CSV

```python
import asyncio
import csv
from xmlriver_pro import AsyncGoogleClient

async def export_to_csv(queries, filename="search_results.csv"):
    """Экспорт результатов поиска в CSV"""
    results = []

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for query in queries:
            try:
                search_results = await google.search(query, num_results=10)

                for result in search_results.results:
                    results.append({
                        "query": query,
                        "position": result.rank,
                        "title": result.title,
                        "url": result.url,
                        "snippet": result.snippet,
                        "total_results": search_results.total_results
                    })

                await asyncio.sleep(1)

            except Exception as e:
                print(f"Ошибка для запроса '{query}': {e}")

    # Записываем в CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['query', 'position', 'title', 'url', 'snippet', 'total_results']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print(f"Экспортировано {len(results)} результатов в {filename}")

# Использование
async def main():
    queries = ["python programming", "machine learning", "data science"]
    await export_to_csv(queries)

asyncio.run(main())
```

### Экспорт в JSON

```python
import asyncio
import json
from xmlriver_pro import AsyncGoogleClient

async def export_to_json(queries, filename="search_results.json"):
    """Экспорт результатов поиска в JSON"""
    results = []

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for query in queries:
            try:
                search_results = await google.search(query, num_results=10)

                query_results = {
                    "query": query,
                    "total_results": search_results.total_results,
                    "results": [
                        {
                            "position": result.rank,
                            "title": result.title,
                            "url": result.url,
                            "snippet": result.snippet
                        }
                        for result in search_results.results
                    ]
                }
                results.append(query_results)

                await asyncio.sleep(1)

            except Exception as e:
                print(f"Ошибка для запроса '{query}': {e}")

    # Записываем в JSON
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, ensure_ascii=False, indent=2)

    print(f"Экспортировано {len(results)} запросов в {filename}")

# Использование
async def main():
    queries = ["python programming", "machine learning", "data science"]
    await export_to_json(queries)

asyncio.run(main())
```

## Кэширование результатов

### Простое кэширование

```python
import asyncio
import json
import hashlib
from pathlib import Path
from xmlriver_pro import AsyncGoogleClient

class SearchCache:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, query, **kwargs):
        """Генерируем ключ кэша на основе запроса и параметров"""
        cache_data = {"query": query, **kwargs}
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()

    def get(self, query, **kwargs):
        """Получаем результат из кэша"""
        cache_key = self._get_cache_key(query, **kwargs)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def set(self, query, result, **kwargs):
        """Сохраняем результат в кэш"""
        cache_key = self._get_cache_key(query, **kwargs)
        cache_file = self.cache_dir / f"{cache_key}.json"

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

async def cached_search(queries, cache_ttl_hours=24):
    """Поиск с кэшированием результатов"""
    cache = SearchCache()
    results = []

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        for query in queries:
            # Проверяем кэш
            cached_result = cache.get(query)
            if cached_result:
                print(f"Результат для '{query}' взят из кэша")
                results.append(cached_result)
                continue

            # Выполняем поиск
            try:
                search_results = await google.search(query, num_results=10)

                result = {
                    "query": query,
                    "total_results": search_results.total_results,
                    "results": [
                        {
                            "position": result.rank,
                            "title": result.title,
                            "url": result.url,
                            "snippet": result.snippet
                        }
                        for result in search_results.results
                    ]
                }

                # Сохраняем в кэш
                cache.set(query, result)
                results.append(result)

                await asyncio.sleep(1)

            except Exception as e:
                print(f"Ошибка для запроса '{query}': {e}")

    return results

# Использование
async def main():
    queries = ["python programming", "machine learning", "data science"]
    results = await cached_search(queries)
    print(f"Обработано {len(results)} запросов")

asyncio.run(main())
```

## Пакетная обработка

### Обработка больших объемов данных

```python
import asyncio
from xmlriver_pro import AsyncGoogleClient
from typing import List, Dict, Any

async def batch_process(queries: List[str], batch_size: int = 10):
    """Пакетная обработка запросов"""
    results = []

    # Разбиваем запросы на батчи
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        print(f"Обрабатываем батч {i//batch_size + 1}: {len(batch)} запросов")

        batch_results = await process_batch(batch)
        results.extend(batch_results)

        # Пауза между батчами
        if i + batch_size < len(queries):
            await asyncio.sleep(5)

    return results

async def process_batch(queries: List[str]) -> List[Dict[str, Any]]:
    """Обработка одного батча запросов"""
    batch_results = []

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        # Создаем задачи для параллельной обработки
        tasks = []
        for query in queries:
            task = process_single_query(google, query)
            tasks.append(task)

        # Выполняем все задачи параллельно
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Обрабатываем результаты
        processed_results = []
        for i, result in enumerate(batch_results):
            if isinstance(result, Exception):
                processed_results.append({
                    "query": queries[i],
                    "error": str(result)
                })
            else:
                processed_results.append(result)

    return processed_results

async def process_single_query(google, query: str) -> Dict[str, Any]:
    """Обработка одного запроса"""
    try:
        search_results = await google.search(query, num_results=10)

        return {
            "query": query,
            "total_results": search_results.total_results,
            "results": [
                {
                    "position": result.rank,
                    "title": result.title,
                    "url": result.url,
                    "snippet": result.snippet
                }
                for result in search_results.results
            ]
        }
    except Exception as e:
        return {
            "query": query,
            "error": str(e)
        }

# Использование
async def main():
    # Большой список запросов
    queries = [f"python topic {i}" for i in range(100)]

    results = await batch_process(queries, batch_size=20)

    successful = len([r for r in results if "error" not in r])
    failed = len([r for r in results if "error" in r])

    print(f"Обработано: {successful} успешно, {failed} с ошибками")

asyncio.run(main())
```

## Адаптивное управление скоростью

### Динамическая регулировка скорости

```python
import asyncio
import time
from xmlriver_pro import AsyncGoogleClient
from xmlriver_pro.core import RateLimitError

class AdaptiveRateLimiter:
    def __init__(self, initial_delay=1.0, max_delay=60.0, backoff_factor=2.0):
        self.delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.last_request_time = 0

    async def wait_if_needed(self):
        """Ожидание если нужно соблюдать rate limit"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.delay:
            await asyncio.sleep(self.delay - time_since_last)

        self.last_request_time = time.time()

    def increase_delay(self):
        """Увеличиваем задержку при ошибках rate limit"""
        self.delay = min(self.delay * self.backoff_factor, self.max_delay)
        print(f"Увеличена задержка до {self.delay:.2f} секунд")

    def decrease_delay(self):
        """Уменьшаем задержку при успешных запросах"""
        self.delay = max(self.delay / self.backoff_factor, 0.1)
        print(f"Уменьшена задержка до {self.delay:.2f} секунд")

async def adaptive_search(queries, max_concurrent=5):
    """Адаптивный поиск с динамической регулировкой скорости"""
    rate_limiter = AdaptiveRateLimiter()
    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def search_with_retry(google, query):
        async with semaphore:
            for attempt in range(3):  # Максимум 3 попытки
                try:
                    await rate_limiter.wait_if_needed()
                    search_results = await google.search(query)

                    # Уменьшаем задержку при успехе
                    rate_limiter.decrease_delay()

                    return {
                        "query": query,
                        "total_results": search_results.total_results,
                        "results": search_results.results
                    }

                except RateLimitError as e:
                    print(f"Rate limit для '{query}': {e}")
                    rate_limiter.increase_delay()

                    if attempt < 2:  # Не последняя попытка
                        await asyncio.sleep(rate_limiter.delay)
                        continue
                    else:
                        return {"query": query, "error": str(e)}

                except Exception as e:
                    return {"query": query, "error": str(e)}

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key") as google:
        tasks = [search_with_retry(google, query) for query in queries]
        results = await asyncio.gather(*tasks)

    return results

# Использование
async def main():
    queries = ["python programming", "machine learning", "data science", "web development"]
    results = await adaptive_search(queries)

    for result in results:
        if "error" in result:
            print(f"Ошибка для '{result['query']}': {result['error']}")
        else:
            print(f"'{result['query']}': {result['total_results']} результатов")

asyncio.run(main())
```

## Мониторинг потоков

### Отслеживание использования потоков

```python
import asyncio
import time
from xmlriver_pro import AsyncGoogleClient

async def monitor_concurrent_usage(queries):
    """Мониторинг использования потоков"""
    start_time = time.time()
    active_requests = 0
    max_concurrent = 0

    async def search_with_monitoring(google, query, request_id):
        nonlocal active_requests, max_concurrent

        active_requests += 1
        max_concurrent = max(max_concurrent, active_requests)

        print(f"Запрос {request_id}: '{query}' (активных: {active_requests})")

        try:
            result = await google.search(query)
            return {"request_id": request_id, "query": query, "result": result}
        except Exception as e:
            return {"request_id": request_id, "query": query, "error": str(e)}
        finally:
            active_requests -= 1
            print(f"Запрос {request_id} завершен (активных: {active_requests})")

    async with AsyncGoogleClient(user_id=123, api_key="your_google_key", max_concurrent=5) as google:
        tasks = []
        for i, query in enumerate(queries):
            task = search_with_monitoring(google, query, i + 1)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

    end_time = time.time()
    duration = end_time - start_time

    print(f"\nСтатистика:")
    print(f"Всего запросов: {len(queries)}")
    print(f"Максимум одновременных: {max_concurrent}")
    print(f"Время выполнения: {duration:.2f} секунд")
    print(f"Средняя скорость: {len(queries)/duration:.2f} запросов/сек")

    return results

# Использование
async def main():
    queries = [f"python topic {i}" for i in range(20)]
    results = await monitor_concurrent_usage(queries)

    successful = len([r for r in results if "error" not in r])
    print(f"Успешно обработано: {successful}/{len(queries)}")

asyncio.run(main())
```

---

**Подробнее:**
- [Examples](examples.md) - базовые примеры использования
- [API Reference](API_REFERENCE.md) - полный справочник API
- [Troubleshooting](TROUBLESHOOTING.md) - решение проблем
