"""
Пример использования методов get_balance() и get_cost()

Демонстрация:
- get_balance() - единый баланс для всего аккаунта XMLRiver
- get_cost() - стоимость запросов для каждой системы (Google/Yandex/Wordstat)
"""

import asyncio
import os
from dotenv import load_dotenv

from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient
from xmlriver_pro.wordstat import AsyncWordstatClient


async def main():
    """Демонстрация работы с балансом и стоимостью"""
    
    # Загружаем переменные окружения
    load_dotenv()
    user_id = int(os.getenv("XMLRIVER_USER_ID", "0"))
    api_key = os.getenv("XMLRIVER_API_KEY", "")

    if not user_id or not api_key:
        print("❌ Установите XMLRIVER_USER_ID и XMLRIVER_API_KEY в .env файле")
        return

    print("=" * 60)
    print("💰 ПРОВЕРКА БАЛАНСА И СТОИМОСТИ XMLRiver API")
    print("=" * 60)

    # 1. Проверяем баланс через Google клиент
    async with AsyncGoogleClient(user_id=user_id, api_key=api_key) as google:
        balance = await google.get_balance()
        google_cost = await google.get_cost()
        
        print(f"\n📊 Google Search:")
        print(f"   Баланс: {balance:.2f} руб. (единый для всего аккаунта)")
        print(f"   Стоимость: {google_cost:.2f} руб/1000 запросов")

    # 2. Проверяем стоимость через Yandex клиент (баланс тот же)
    async with AsyncYandexClient(user_id=user_id, api_key=api_key) as yandex:
        balance = await yandex.get_balance()
        yandex_cost = await yandex.get_cost()
        
        print(f"\n📊 Yandex Search:")
        print(f"   Баланс: {balance:.2f} руб. (тот же самый)")
        print(f"   Стоимость: {yandex_cost:.2f} руб/1000 запросов")

    # 3. Проверяем стоимость через Wordstat клиент
    async with AsyncWordstatClient(user_id=user_id, api_key=api_key) as wordstat:
        balance = await wordstat.get_balance()
        wordstat_cost = await wordstat.get_cost()
        
        print(f"\n📊 Yandex Wordstat:")
        print(f"   Баланс: {balance:.2f} руб. (тот же самый)")
        print(f"   Стоимость: {wordstat_cost:.2f} руб/1000 запросов")

    # 4. Сравнительная таблица
    print("\n" + "=" * 60)
    print("📋 СРАВНИТЕЛЬНАЯ ТАБЛИЦА")
    print("=" * 60)
    print(f"Единый баланс аккаунта: {balance:.2f} руб.")
    print(f"\nСтоимость запросов:")
    print(f"  - Google:   {google_cost:.2f} руб/1000 запросов")
    print(f"  - Yandex:   {yandex_cost:.2f} руб/1000 запросов")
    print(f"  - Wordstat: {wordstat_cost:.2f} руб/1000 запросов")
    
    # 5. Расчёт количества доступных запросов
    if google_cost > 0:
        google_requests = int((balance / google_cost) * 1000)
        print(f"\n💡 При текущем балансе доступно:")
        print(f"  - Google:   ~{google_requests:,} запросов")
    
    if yandex_cost > 0:
        yandex_requests = int((balance / yandex_cost) * 1000)
        print(f"  - Yandex:   ~{yandex_requests:,} запросов")
    
    if wordstat_cost > 0:
        wordstat_requests = int((balance / wordstat_cost) * 1000)
        print(f"  - Wordstat: ~{wordstat_requests:,} запросов")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

