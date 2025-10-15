#!/usr/bin/env python3
"""
Тест с использованием переменных окружения
"""

import asyncio
import os
from dotenv import load_dotenv
from xmlriver_pro import AsyncGoogleClient, AsyncYandexClient

# Загружаем переменные окружения
load_dotenv()

async def test_with_env_vars():
    """Тест с использованием переменных окружения"""
    
    # Получаем данные из переменных окружения
    user_id = int(os.getenv("XMLRIVER_USER_ID", "0"))
    api_key = os.getenv("XMLRIVER_API_KEY", "")
    
    if not user_id or not api_key:
        print("ERROR: XMLRIVER_USER_ID and XMLRIVER_API_KEY must be set in .env file")
        return
    
    print(f"Testing with User ID: {user_id}")
    print(f"API Key: {api_key[:10]}...")
    print()
    
    # Тест Google AsyncClient
    print("1. Testing Google AsyncClient...")
    async with AsyncGoogleClient(user_id, api_key) as google_client:
        try:
            response = await google_client.search("python programming", num_results=3)
            print(f"  OK Google Organic: {len(response.results)} results")
            print(f"  Query: {response.query}")
            print(f"  Total: {response.total_results}")
        except Exception as e:
            print(f"  ERROR Google: {e}")
    
    # Тест Yandex AsyncClient
    print("2. Testing Yandex AsyncClient...")
    async with AsyncYandexClient(user_id, api_key) as yandex_client:
        try:
            response = await yandex_client.search("python programming", num_results=3)
            print(f"  OK Yandex Organic: {len(response.results)} results")
            print(f"  Query: {response.query}")
            print(f"  Total: {response.total_results}")
        except Exception as e:
            print(f"  ERROR Yandex: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_with_env_vars())
