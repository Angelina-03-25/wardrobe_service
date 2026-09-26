"""Модуль сохранения и загрузки данных в JSON-файлах."""

import json
import os
from typing import Any


def load_data(filename: str) -> dict[str, Any]:
    """Загрузить всё состояние приложения из JSON-файла.

    Если файла нет — вернуть пустую структуру.
    """
    empty: dict[str, Any] = {
        "user": None,
        "wardrobe": None,
        "categories": [],
        "seasons": [],
        "items": [],
    }
    if not os.path.exists(filename):
        return empty
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return empty


def save_data(filename: str, data: dict[str, Any]) -> None:
    """Сохранить всё состояние приложения в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")
