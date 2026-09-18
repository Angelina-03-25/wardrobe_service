"""
Сервис учета одежды.

ПР1: базовый сценарий проверки одной вещи.
ПР2: коллекции, циклы, модули, JSON, меню, обработка исключений.

Точка запуска приложения.
"""

from datetime import date

from items import (
    add_item,
    find_items,
    filter_by_season,
    filter_by_category,
    filter_by_min_temp,
    sort_by_min_temp,
    is_item_suitable,
    get_recommendation,
)
from storage import load_items, save_items
from utils import input_int, input_str


DATA_FILE = "data/items.json"


# ---------------------------------------------------------------------------
# Функции вывода (ПР2)
# ---------------------------------------------------------------------------

def show_items(items: list[dict]) -> None:
    """Вывести список вещей в виде таблицы."""
    if not items:
        print("Список вещей пуст.")
        return

    print("-" * 70)
    print(
        f"{'ID':<4}{'Название':<20}"
        f"{'Категория':<18}{'Сезон':<12}{'Мин. t°C':<8}"
    )
    print("-" * 70)
    for item in items:
        print(
            f"{item['id']:<4}"
            f"{item['name']:<20}"
            f"{item['category']:<18}"
            f"{item['season']:<12}"
            f"{item['min_temp']:<8}"
        )
    print("-" * 70)


def show_recommendations(items: list[dict],
                         season: str, temp: int) -> None:
    """Вывести рекомендации по всем вещам
    (логика из ПР1, расширенная на список)."""
    if not items:
        print("Список вещей пуст.")
        return

    print(f"\nТекущий сезон: {season}, текущая температура: {temp}°C")
    for item in items:
        recommendation = get_recommendation(item, season, temp)
        print(f"  • {recommendation}")


# ---------------------------------------------------------------------------
# Демонстрация логики ПР1 (сохранена в проекте)
# ---------------------------------------------------------------------------

def demo_pr1_scenario() -> None:
    """Показать базовый сценарий из ПР1: одна вещь, одна проверка."""
    username = "Анна"
    item_name = "Зимнее пальто"
    category = "Верхняя одежда"
    season = "Зима"
    min_temp = -15
    current_temp = -5
    is_clean = True
    current_season = "Зима"

    item = {
        "id": 0,
        "name": item_name,
        "category": category,
        "season": season,
        "min_temp": min_temp,
    }

    season_ok = is_item_suitable(item, current_season, current_temp)

    print("\n=== Демонстрация сценария ПР1 ===")
    print(f"Пользователь: {username}")
    print(f"Вещь: {item_name}")
    print(f"Категория: {category}")
    print(f"Сезон вещи: {season}")
    print(f"Мин. температура вещи: {min_temp}°C")
    print(f"Текущая температура: {current_temp}°C")
    print(f"Вещь чистая: {'да' if is_clean else 'нет'}")
    print(f"Подходит по сезону и температуре: {'да' if season_ok else 'нет'}")
    recommendation = get_recommendation(
        item, current_season, current_temp
    )
    print(f"Рекомендация: {recommendation}")


# ---------------------------------------------------------------------------
# Меню (ПР2)
# ---------------------------------------------------------------------------

def print_menu() -> None:
    """Вывести главное меню приложения."""
    print("\n=== Сервис учета одежды ===")
    print("1. Показать все вещи")
    print("2. Добавить вещь")
    print("3. Найти вещь по названию")
    print("4. Показать вещи по сезону")
    print("5. Показать вещи по категории")
    print("6. Показать вещи по минимальной температуре")
    print("7. Отсортировать вещи по температуре")
    print("8. Получить рекомендации на сегодня")
    print("9. Показать сценарий ПР1 (демонстрация)")
    print("0. Выход")


def handle_show_all(items: list[dict]) -> None:
    show_items(items)


def handle_add_item(items: list[dict]) -> None:
    name = input_str("Название вещи: ")
    category = input_str("Категория: ")
    season = input_str("Сезон (Лето/Зима/Демисезон/Всесезон): ")
    min_temp = input_int("Минимальная температура: ")
    item = add_item(items, name, category, season, min_temp)
    save_items(DATA_FILE, items)
    print(f"Вещь добавлена с ID={item['id']}.")


def handle_find(items: list[dict]) -> None:
    query = input_str("Поиск по названию: ")
    show_items(find_items(items, query))


def handle_filter_season(items: list[dict]) -> None:
    season = input_str("Сезон: ")
    show_items(filter_by_season(items, season))


def handle_filter_category(items: list[dict]) -> None:
    category = input_str("Категория: ")
    show_items(filter_by_category(items, category))


def handle_filter_temp(items: list[dict]) -> None:
    min_temp = input_int("Показать вещи с минимальной температурой не выше: ")
    show_items(filter_by_min_temp(items, min_temp))


def handle_sort_temp(items: list[dict]) -> None:
    show_items(sort_by_min_temp(items))


def handle_recommendations(items: list[dict]) -> None:
    season = input_str("Текущий сезон: ")
    temp = input_int("Текущая температура: ")
    show_recommendations(items, season, temp)


def main() -> None:
    """Точка запуска приложения."""
    items = load_items(DATA_FILE)
    today = date.today()
    print(f"Сегодня: {today.strftime('%d.%m.%Y')}")

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            handle_show_all(items)
        elif choice == "2":
            handle_add_item(items)
        elif choice == "3":
            handle_find(items)
        elif choice == "4":
            handle_filter_season(items)
        elif choice == "5":
            handle_filter_category(items)
        elif choice == "6":
            handle_filter_temp(items)
        elif choice == "7":
            handle_sort_temp(items)
        elif choice == "8":
            handle_recommendations(items)
        elif choice == "9":
            demo_pr1_scenario()
        elif choice == "0":
            save_items(DATA_FILE, items)
            print("Данные сохранены. Выход.")
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
