"""
Скрипт для обновления географических данных
"""

import csv
import json
import os
from pathlib import Path


def update_yandex_regions():
    """Обновить регионы Yandex из CSV файла"""
    csv_path = Path("../yandex_geo.csv")
    if not csv_path.exists():
        print("Файл yandex_geo.csv не найден")
        return

    regions = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["id"] and row["id"].isdigit():
                regions[int(row["id"])] = {
                    "id": int(row["id"]),
                    "name": row["place"],
                    "parent_id": (
                        int(row["parent"])
                        if row["parent"] and row["parent"].isdigit()
                        else 0
                    ),
                    "country_code": row["country_code"] if row["country_code"] else "",
                }

    # Сохранить в JSON
    json_path = Path("xmlriver_pro/data/yandex_regions.json")
    json_path.parent.mkdir(exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(regions, f, ensure_ascii=False, indent=2)

    print(f"Обновлено {len(regions)} регионов Yandex")


def update_google_languages():
    """Обновить языки Google из Excel файла"""
    try:
        import pandas as pd

        excel_path = Path("../langs.xlsx")
        if not excel_path.exists():
            print("Файл langs.xlsx не найден")
            return

        df = pd.read_excel(excel_path)
        languages = {}

        for _, row in df.iterrows():
            languages[row["lang"]] = {"code": row["lang"], "name": row["name"]}

        # Сохранить в JSON
        json_path = Path("xmlriver_pro/data/google_languages.json")
        json_path.parent.mkdir(exist_ok=True)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(languages, f, ensure_ascii=False, indent=2)

        print(f"Обновлено {len(languages)} языков Google")

    except ImportError:
        print("pandas не установлен, пропускаем обновление языков")


def update_cities():
    """Обновить города из CSV файла"""
    csv_path = Path("../geo.csv")
    if not csv_path.exists():
        print("Файл geo.csv не найден")
        return

    cities = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Criteria ID"] and row["Criteria ID"].isdigit():
                cities[int(row["Criteria ID"])] = {
                    "id": int(row["Criteria ID"]),
                    "name": row["Name"],
                    "canonical_name": row["Canonical Name"],
                    "parent_id": (
                        int(row["Parent ID"])
                        if row["Parent ID"] and row["Parent ID"].isdigit()
                        else 0
                    ),
                    "country_code": row["Country Code"],
                    "target_type": row["Target Type"],
                    "status": row["Status"],
                }

    # Сохранить в JSON
    json_path = Path("xmlriver_pro/data/cities.json")
    json_path.parent.mkdir(exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)

    print(f"Обновлено {len(cities)} городов")


def main():
    """Основная функция обновления"""
    print("Обновление географических данных...")

    # Создать директорию для данных
    data_dir = Path("xmlriver_pro/data")
    data_dir.mkdir(exist_ok=True)

    # Обновить данные
    update_yandex_regions()
    update_google_languages()
    update_cities()

    print("Обновление завершено!")


if __name__ == "__main__":
    main()
