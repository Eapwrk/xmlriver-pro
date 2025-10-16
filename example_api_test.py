#!/usr/bin/env python3
"""
Пример тестирования API с использованием переменных окружения
БЕЗОПАСНО: Не содержит реальных API ключей
"""

import os
from dotenv import load_dotenv
from xmlriver_pro import GoogleClient, YandexClient

# Загружаем переменные окружения из .env файла
load_dotenv()

def test_api_with_env():
    """Пример безопасного тестирования API"""
    
    # Получаем credentials из переменных окружения
    user_id = os.getenv("XMLRIVER_USER_ID")
    api_key = os.getenv("XMLRIVER_API_KEY")
    
    # Проверяем что credentials заданы
    if not user_id or not api_key:
        print("❌ Ошибка: Не заданы XMLRIVER_USER_ID и XMLRIVER_API_KEY в .env файле")
        print("📝 Создайте .env файл на основе .env.example")
        return
    
    try:
        # Инициализируем клиенты
        google = GoogleClient(user_id=int(user_id), api_key=api_key)
        yandex = YandexClient(user_id=int(user_id), api_key=api_key)
        
        # Тестируем Google поиск
        print("🔍 Тестируем Google поиск...")
        google_results = google.search("python programming", groupby=5)
        print(f"✅ Google: {google_results.total_results} результатов")
        
        # Тестируем Yandex поиск
        print("🔍 Тестируем Yandex поиск...")
        yandex_results = yandex.search("программирование python", groupby=5)
        print(f"✅ Yandex: {yandex_results.total_results} результатов")
        
        print("🎉 Все тесты прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    test_api_with_env()
