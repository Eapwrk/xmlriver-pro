"""
Пример использования модуля geo_data
"""

from xmlriver_pro.utils import (
    get_yandex_region,
    find_yandex_regions,
    get_google_country,
    find_google_countries,
    get_google_language,
    find_google_languages,
    get_google_domain,
    find_google_domains,
    find_cities,
    get_geo_stats,
    search_place,
    get_region_for_yandex_search,
    get_country_code_for_google_search,
)


def main():
    """Основная функция с примерами использования"""

    print("🌍 Примеры работы с географическими данными XMLRiver Pro")
    print("=" * 60)

    # 1. Статистика данных
    print("\n📊 Статистика загруженных данных:")
    stats = get_geo_stats()
    for key, value in stats.items():
        print(f"  {key}: {value:,}")

    # 2. Работа с регионами Yandex
    print("\n🗺️ Регионы Yandex:")

    # Поиск Москвы
    moscow_regions = find_yandex_regions("Москва", exact=True)
    if moscow_regions:
        moscow = moscow_regions[0]
        print(f"  Найден регион: {moscow.name} (ID: {moscow.id})")

        # Получение региона по ID
        region = get_yandex_region(moscow.id)
        if region:
            print(f"  Подтверждение: {region.name}")

    # 3. Работа со странами Google
    print("\n🌍 Страны Google:")

    # Поиск России
    russia_countries = find_google_countries("Russia", exact=True)
    if russia_countries:
        russia = russia_countries[0]
        print(f"  Найдена страна: {russia.name} ({russia.code})")

    # 4. Работа с языками Google
    print("\n🗣️ Языки Google:")

    # Получение русского языка
    russian_lang = get_google_language("ru")
    if russian_lang:
        print(f"  Русский язык: {russian_lang.name} ({russian_lang.code})")

    # Поиск английского языка
    english_langs = find_google_languages("English", exact=True)
    if english_langs:
        english = english_langs[0]
        print(f"  Английский язык: {english.name} ({english.code})")

    # 5. Работа с доменами Google
    print("\n🌐 Домены Google:")

    # Получение российского домена
    ru_domain = get_google_domain("ru")
    if ru_domain:
        print(f"  Российский домен: {ru_domain.name} ({ru_domain.code})")

    # Поиск американского домена
    us_domains = find_google_domains("United States", exact=True)
    if us_domains:
        us_domain = us_domains[0]
        print(f"  Американский домен: {us_domain.name} ({us_domain.code})")

    # 6. Работа с городами
    print("\n🏙️ Города:")

    # Поиск Москвы среди городов
    moscow_cities = find_cities("Moscow", exact=True)
    if moscow_cities:
        moscow_city = moscow_cities[0]
        print(f"  Найден город: {moscow_city.name} ({moscow_city.country_code})")
        print(f"    Полное название: {moscow_city.canonical_name}")
        print(f"    Статус: {moscow_city.status}")

    # 7. Универсальный поиск
    print("\n🔍 Универсальный поиск места 'Moscow':")
    search_results = search_place("Moscow")

    print(f"  Yandex регионы: {len(search_results['yandex_regions'])}")
    for region in search_results["yandex_regions"][:3]:  # Первые 3
        print(f"    - {region.name} (ID: {region.id})")

    print(f"  Google страны: {len(search_results['google_countries'])}")
    for country in search_results["google_countries"][:3]:  # Первые 3
        print(f"    - {country.name} ({country.code})")

    print(f"  Города: {len(search_results['cities'])}")
    for city in search_results["cities"][:3]:  # Первые 3
        print(f"    - {city.name} ({city.country_code})")

    # 8. Получение параметров для поиска
    print("\n🎯 Параметры для поисковых запросов:")

    # ID региона для Yandex
    yandex_region_id = get_region_for_yandex_search("Москва")
    if yandex_region_id:
        print(f"  ID региона Yandex для 'Москва': {yandex_region_id}")

    # Код страны для Google
    google_country_code = get_country_code_for_google_search("Moscow")
    if google_country_code:
        print(f"  Код страны Google для 'Moscow': {google_country_code}")

    # 9. Демонстрация работы с разными типами поиска
    print("\n🔎 Демонстрация различных типов поиска:")

    # Точный поиск
    exact_regions = find_yandex_regions("Москва", exact=True)
    print(f"  Точный поиск 'Москва': {len(exact_regions)} результатов")

    # Частичный поиск
    partial_regions = find_yandex_regions("Москва", exact=False)
    print(f"  Частичный поиск 'Москва': {len(partial_regions)} результатов")

    # 10. Пример интеграции с XMLRiver Pro
    print("\n🚀 Пример интеграции с XMLRiver Pro:")
    print("  # Код для использования в поисковых запросах:")
    print("  from xmlriver_pro import YandexClient, GoogleClient")
    print("  ")
    print("  # Определение параметров")
    print("  yandex_region_id = get_region_for_yandex_search('Москва')")
    print("  google_country_code = get_country_code_for_google_search('Moscow')")
    print("  ")
    print("  # Поиск в Yandex")
    print("  if yandex_region_id:")
    print("      yandex = YandexClient(user_id=123, api_key='your_key')")
    print("      results = yandex.search('python', lr=yandex_region_id)")
    print("  ")
    print("  # Поиск в Google")
    print("  if google_country_code:")
    print("      google = GoogleClient(user_id=123, api_key='your_key')")
    print("      results = google.search('python', gl=google_country_code)")

    print("\n✅ Примеры завершены!")


if __name__ == "__main__":
    main()
