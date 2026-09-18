"""
Модуль сохранения и загрузки данных в JSON-файлах.
"""

import json
import os


def load_items(filename: str) -> list[dict]:
    """Загрузить вещи из JSON-файла. Если файла нет — вернуть пустой список."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return []


def save_items(filename: str, items: list[dict]) -> None:
    """Сохранить вещи в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")
