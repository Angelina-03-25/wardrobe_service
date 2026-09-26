"""Тесты классов предметной области."""

from models import User, Wardrobe, Item, Category, Season


def test_user_creation():
    user = User(1, "Анна", "anna@example.com")
    assert user.id == 1
    assert user.username == "Анна"
    assert user.email == "anna@example.com"


def test_wardrobe_creation():
    wardrobe = Wardrobe(1, 1, "Мой гардероб")
    assert wardrobe.id == 1
    assert wardrobe.user_id == 1
    assert wardrobe.name == "Мой гардероб"


def test_category_creation():
    category = Category(1, "Верхняя одежда")
    assert category.id == 1
    assert category.name == "Верхняя одежда"


def test_season_creation():
    season = Season(1, "Зима")
    assert season.id == 1
    assert season.name == "Зима"


def test_item_creation():
    item = Item(1, 1, 1, 1, "Пальто", -15)
    assert item.id == 1
    assert item.wardrobe_id == 1
    assert item.category_id == 1
    assert item.season_id == 1
    assert item.name == "Пальто"
    assert item.min_temp == -15


def test_item_is_suitable():
    item = Item(1, 1, 1, 1, "Пальто", -15)
    assert item.is_suitable(-5)
    assert item.is_suitable(-15)
    assert not item.is_suitable(-20)


def test_to_dict_user():
    user = User(1, "Анна", "anna@example.com")
    data = user.to_dict()
    assert data["id"] == 1
    assert data["username"] == "Анна"
    assert "created_at" in data


def test_to_dict_item():
    item = Item(1, 1, 1, 1, "Пальто", -15)
    data = item.to_dict()
    assert data["name"] == "Пальто"
    assert data["min_temp"] == -15
    assert data["wardrobe_id"] == 1
