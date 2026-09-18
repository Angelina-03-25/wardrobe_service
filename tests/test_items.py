

from items import (
    add_item,
    find_items,
    filter_by_season,
    filter_by_category,
    is_item_suitable,
)


def test_add_item():
    items = []
    add_item(items, "Пальто", "Верхняя одежда", "Зима", -15)
    assert len(items) == 1
    assert items[0]["name"] == "Пальто"


def test_find_items():
    items = []
    add_item(items, "Пальто", "Верхняя одежда", "Зима", -15)
    result = find_items(items, "паль")
    assert len(result) == 1


def test_filter_by_season():
    items = []
    add_item(items, "Пальто", "Верхняя одежда", "Зима", -15)
    add_item(items, "Шорты", "Верхняя одежда", "Лето", 25)
    result = filter_by_season(items, "Зима")
    assert len(result) == 1


def test_filter_by_category():
    items = []
    add_item(items, "Пальто", "Верхняя одежда", "Зима", -15)
    result = filter_by_category(items, "Верхняя одежда")
    assert len(result) == 1


def test_is_item_suitable():
    item = {
        "id": 1,
        "name": "Пальто",
        "category": "Верхняя одежда",
        "season": "Зима",
        "min_temp": -15,
    }
    assert is_item_suitable(item, "Зима", -5)
    assert not is_item_suitable(item, "Лето", 25)
