"""Тесты сохранения и загрузки состояния приложения."""

# import os

from storage import load_data, save_data


def test_save_and_load(tmp_path):
    """Проверить, что данные сохраняются и загружаются без изменений."""
    filename = str(tmp_path / "state.json")
    data = {
        "user": {"id": 1, "username": "Анна", "email": "anna@example.com"},
        "wardrobe": {"id": 1, "user_id": 1, "name": "Мой гардероб"},
        "categories": [{"id": 1, "name": "Верхняя одежда"}],
        "seasons": [{"id": 1, "name": "Зима"}],
        "items": [
            {
                "id": 1,
                "wardrobe_id": 1,
                "category_id": 1,
                "season_id": 1,
                "name": "Пальто",
                "min_temp": -15,
            }
        ],
    }

    save_data(filename, data)
    loaded = load_data(filename)

    assert loaded == data


def test_load_missing_file(tmp_path):
    """Если файла нет — вернуть пустую структуру."""
    filename = str(tmp_path / "no_file.json")
    loaded = load_data(filename)

    assert loaded["user"] is None
    assert loaded["wardrobe"] is None
    assert loaded["categories"] == []
    assert loaded["seasons"] == []
    assert loaded["items"] == []
