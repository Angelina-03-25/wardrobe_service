"""
Сервис учета одежды.

ПР1: базовый сценарий проверки одной вещи.
ПР2: коллекции, циклы, модули, JSON, меню, обработка исключений.
ПР3: ООП-модели, сущность Гардероб, связь пользователя и вещей.

Точка запуска приложения.
"""

from datetime import date
from typing import Any

from models import User, Wardrobe, Item, Category, Season
from storage import load_data, save_data
from utils import input_int, input_str


DATA_FILE = "data/state.json"


# ---------------------------------------------------------------------------
# Восстановление объектов из JSON
# ---------------------------------------------------------------------------

def build_user(raw: dict | None) -> User | None:
    """Восстановить объект User из словаря."""
    if raw is None:
        return None
    return User(
        user_id=raw["id"],
        username=raw["username"],
        email=raw["email"],
    )


def build_wardrobe(raw: dict | None) -> Wardrobe | None:
    """Восстановить объект Wardrobe из словаря."""
    if raw is None:
        return None
    return Wardrobe(
        wardrobe_id=raw["id"],
        user_id=raw["user_id"],
        name=raw["name"],
    )


def build_categories(raw_list: list[dict]) -> list[Category]:
    """Восстановить список категорий."""
    return [Category(c["id"], c["name"]) for c in raw_list]


def build_seasons(raw_list: list[dict]) -> list[Season]:
    """Восстановить список сезонов."""
    return [Season(s["id"], s["name"]) for s in raw_list]


def build_items(raw_list: list[dict]) -> list[Item]:
    """Восстановить список вещей."""
    result: list[Item] = []
    for raw in raw_list:
        result.append(
            Item(
                item_id=raw["id"],
                wardrobe_id=raw["wardrobe_id"],
                category_id=raw["category_id"],
                season_id=raw["season_id"],
                name=raw["name"],
                min_temp=raw["min_temp"],
            )
        )
    return result


def serialize_state(
    user: User | None,
    wardrobe: Wardrobe | None,
    categories: list[Category],
    seasons: list[Season],
    items: list[Item],
) -> dict[str, Any]:
    """Собрать всё состояние приложения в словарь для JSON."""
    return {
        "user": user.to_dict() if user else None,
        "wardrobe": wardrobe.to_dict() if wardrobe else None,
        "categories": [c.to_dict() for c in categories],
        "seasons": [s.to_dict() for s in seasons],
        "items": [i.to_dict() for i in items],
    }


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def find_category_by_name(
    categories: list[Category], name: str
) -> Category | None:
    """Найти категорию по имени (без учёта регистра)."""
    for category in categories:
        if category.name.lower() == name.lower():
            return category
    return None


def find_season_by_name(seasons: list[Season], name: str) -> Season | None:
    """Найти сезон по имени (без учёта регистра)."""
    for season in seasons:
        if season.name.lower() == name.lower():
            return season
    return None


def get_or_create_category(
    categories: list[Category], name: str
) -> Category:
    """Найти категорию по имени или создать новую."""
    existing = find_category_by_name(categories, name)
    if existing:
        return existing
    new_id = len(categories) + 1
    category = Category(new_id, name)
    categories.append(category)
    return category


def get_or_create_season(seasons: list[Season], name: str) -> Season:
    """Найти сезон по имени или создать новый."""
    existing = find_season_by_name(seasons, name)
    if existing:
        return existing
    new_id = len(seasons) + 1
    season = Season(new_id, name)
    seasons.append(season)
    return season


# ---------------------------------------------------------------------------
# Вывод
# ---------------------------------------------------------------------------

def show_items(
    items: list[Item],
    categories: list[Category],
    seasons: list[Season],
) -> None:
    """Вывести список вещей в виде таблицы."""
    if not items:
        print("Список вещей пуст.")
        return

    cat_by_id = {c.id: c.name for c in categories}
    season_by_id = {s.id: s.name for s in seasons}

    print("-" * 78)
    print(
        f"{'ID':<4}{'Название':<20}"
        f"{'Категория':<20}{'Сезон':<12}{'Мин. t°C':<8}"
    )
    print("-" * 78)
    for item in items:
        category_name = cat_by_id.get(item.category_id, "—")
        season_name = season_by_id.get(item.season_id, "—")
        print(
            f"{item.id:<4}"
            f"{item.name:<20}"
            f"{category_name:<20}"
            f"{season_name:<12}"
            f"{item.min_temp:<8}"
        )
    print("-" * 78)


def show_recommendations(
    items: list[Item],
    seasons: list[Season],
    season_name: str,
    temp: int,
) -> None:
    """Вывести рекомендации по всем вещам."""
    if not items:
        print("Список вещей пуст.")
        return

    season_by_id = {s.id: s.name for s in seasons}
    print(f"\nТекущий сезон: {season_name}, текущая температура: {temp}°C")

    for item in items:
        item_season = season_by_id.get(item.season_id, "")
        season_ok = (
            item_season.lower() == season_name.lower()
            or item_season.lower() == "всесезон"
        )
        temp_ok = item.is_suitable(temp)
        if season_ok and temp_ok:
            verdict = "подходит для носки сегодня."
        elif not season_ok:
            verdict = "не подходит по сезону."
        else:
            verdict = "не подходит по температуре."
        print(f"  • {item.name}: {verdict}")


# ---------------------------------------------------------------------------
# Демонстрация логики ПР1
# ---------------------------------------------------------------------------

def demo_pr1_scenario() -> None:
    """Показать базовый сценарий из ПР1: одна вещь, одна проверка."""
    user = User(1, "Анна", "anna@example.com")
    category = Category(1, "Верхняя одежда")
    season = Season(1, "Зима")
    wardrobe = Wardrobe(1, user.id, "Мой гардероб")
    item = Item(
        item_id=1,
        wardrobe_id=wardrobe.id,
        category_id=category.id,
        season_id=season.id,
        name="Зимнее пальто",
        min_temp=-15,
    )

    current_temp = -5

    print("\n=== Демонстрация сценария ПР1 ===")
    print(f"Пользователь: {user.username}")
    print(f"Гардероб: {wardrobe.name}")
    print(f"Вещь: {item.name}")
    print(f"Категория: {category.name}")
    print(f"Сезон вещи: {season.name}")
    print(f"Мин. температура вещи: {item.min_temp}°C")
    print(f"Текущая температура: {current_temp}°C")
    status = 'да' if item.is_suitable(current_temp) else 'нет'
    print(f"Подходит по температуре: {status}")


# ---------------------------------------------------------------------------
# Меню
# ---------------------------------------------------------------------------

def print_menu() -> None:
    """Вывести главное меню приложения."""
    print("\n=== Сервис учета одежды ===")
    print("1. Показать все вещи")
    print("2. Добавить вещь")
    print("3. Найти вещь по названию")
    print("4. Показать вещи по сезону")
    print("5. Показать вещи по категории")
    print("6. Показать вещи с температурой не выше указанной")
    print("7. Отсортировать вещи по температуре")
    print("8. Получить рекомендации на сегодня")
    print("9. Показать сценарий ПР1 (демонстрация)")
    print("0. Выход")


def handle_add_item(
    wardrobe: Wardrobe,
    items: list[Item],
    categories: list[Category],
    seasons: list[Season],
) -> None:
    """Добавить новую вещь в гардероб."""
    name = input_str("Название вещи: ")
    category_name = input_str("Категория: ")
    season_name = input_str("Сезон (Лето/Зима/Демисезон/Всесезон): ")
    min_temp = input_int("Минимальная температура: ")

    category = get_or_create_category(categories, category_name)
    season = get_or_create_season(seasons, season_name)

    new_id = max((i.id for i in items), default=0) + 1
    item = Item(
        item_id=new_id,
        wardrobe_id=wardrobe.id,
        category_id=category.id,
        season_id=season.id,
        name=name,
        min_temp=min_temp,
    )
    items.append(item)
    print(f"Вещь добавлена с ID={item.id}.")


def handle_find(
    items: list[Item],
    categories: list[Category],
    seasons: list[Season],
) -> None:
    """Найти вещи по подстроке названия."""
    query = input_str("Поиск по названию: ").lower()
    found = [i for i in items if query in i.name.lower()]
    show_items(found, categories, seasons)


def handle_filter_season(
    items: list[Item],
    categories: list[Category],
    seasons: list[Season],
) -> None:
    """Показать вещи по сезону."""
    season_name = input_str("Сезон: ")
    season = find_season_by_name(seasons, season_name)
    if season is None:
        print(f"Сезон «{season_name}» не найден.")
        return
    found = [i for i in items if i.season_id == season.id]
    show_items(found, categories, seasons)


def handle_filter_category(
    items: list[Item],
    categories: list[Category],
    seasons: list[Season],
) -> None:
    """Показать вещи по категории."""
    category_name = input_str("Категория: ")
    category = find_category_by_name(categories, category_name)
    if category is None:
        print(f"Категория «{category_name}» не найдена.")
        return
    found = [i for i in items if i.category_id == category.id]
    show_items(found, categories, seasons)


def handle_filter_temp(
    items: list[Item],
    categories: list[Category],
    seasons: list[Season],
) -> None:
    """Показать вещи с минимальной температурой не выше указанной."""
    max_temp = input_int("Показать вещи с минимальной температурой не выше: ")
    found = [i for i in items if i.min_temp <= max_temp]
    show_items(found, categories, seasons)


def handle_sort_temp(
    items: list[Item],
    categories: list[Category],
    seasons: list[Season],
) -> None:
    """Отсортировать вещи по минимальной температуре."""
    sorted_items = sorted(items, key=lambda i: i.min_temp)
    show_items(sorted_items, categories, seasons)


def handle_recommendations(
    items: list[Item],
    seasons: list[Season],
) -> None:
    """Вывести рекомендации по всем вещам."""
    season_name = input_str("Текущий сезон: ")
    temp = input_int("Текущая температура: ")
    show_recommendations(items, seasons, season_name, temp)


# ---------------------------------------------------------------------------
# Точка запуска
# ---------------------------------------------------------------------------

def main() -> None:
    """Точка запуска приложения."""
    raw = load_data(DATA_FILE)

    user = build_user(raw["user"])
    wardrobe = build_wardrobe(raw["wardrobe"])
    categories = build_categories(raw["categories"])
    seasons = build_seasons(raw["seasons"])
    items = build_items(raw["items"])

    if user is None:
        print("Первый запуск. Создадим пользователя и гардероб.")
        username = input_str("Имя пользователя: ")
        email = input_str("Email: ")
        user = User(1, username, email)
        wardrobe = Wardrobe(1, user.id, f"Гардероб {username}")
        print(f"Создан {wardrobe.name}.")

    today = date.today()
    print(f"Сегодня: {today.strftime('%d.%m.%Y')}")

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_items(items, categories, seasons)
        elif choice == "2":
            if wardrobe is None:
                print("Гардероб не найден.")
                continue
            handle_add_item(wardrobe, items, categories, seasons)
        elif choice == "3":
            handle_find(items, categories, seasons)
        elif choice == "4":
            handle_filter_season(items, categories, seasons)
        elif choice == "5":
            handle_filter_category(items, categories, seasons)
        elif choice == "6":
            handle_filter_temp(items, categories, seasons)
        elif choice == "7":
            handle_sort_temp(items, categories, seasons)
        elif choice == "8":
            handle_recommendations(items, seasons)
        elif choice == "9":
            demo_pr1_scenario()
        elif choice == "0":
            state = serialize_state(
                user, wardrobe, categories, seasons, items
            )
            save_data(DATA_FILE, state)
            print("Данные сохранены. Выход.")
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
