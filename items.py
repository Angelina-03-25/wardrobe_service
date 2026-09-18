"""
Модуль работы с вещами гардероба.
"""


def add_item(
    items: list[dict],
    name: str,
    category: str,
    season: str,
    min_temp: int,
) -> dict:
    """Добавить вещь в список items и вернуть её словарь."""
    item = {
        "id": len(items) + 1,
        "name": name,
        "category": category,
        "season": season,
        "min_temp": min_temp,
    }
    items.append(item)
    return item


def find_items(items: list[dict], query: str) -> list[dict]:
    """Найти вещи по подстроке в названии (без учёта регистра)."""
    result = []
    for item in items:
        if query.lower() in item["name"].lower():
            result.append(item)
    return result


def filter_by_season(items: list[dict], season: str) -> list[dict]:
    """Отобрать вещи по сезону. Учитывает всесезонные вещи."""
    result = []
    for item in items:
        if item["season"] == season or item["season"] == "Всесезон":
            result.append(item)
    return result


def filter_by_category(items: list[dict], category: str) -> list[dict]:
    """Отобрать вещи по категории."""
    result = []
    for item in items:
        if item["category"] == category:
            result.append(item)
    return result


def filter_by_min_temp(items: list[dict], max_min_temp: int) -> list[dict]:
    """Отобрать вещи, у которых min_temp не выше указанного значения."""
    result = []
    for item in items:
        if item["min_temp"] <= max_min_temp:
            result.append(item)
    return result


def sort_by_min_temp(items: list[dict]) -> list[dict]:
    """Отсортировать вещи по минимальной температуре (от тёплых к лёгким)."""
    return sorted(items, key=lambda item: item["min_temp"])


def is_item_suitable(
    item: dict,
    current_season: str,
    current_temp: int,
) -> bool:
    """Проверить, подходит ли вещь для текущего сезона и температуры."""
    season_ok = (item["season"] == current_season
                 or item["season"] == "Всесезон")
    temp_ok = current_temp >= item["min_temp"]
    return season_ok and temp_ok


def get_recommendation(item: dict, current_season: str,
                       current_temp: int) -> str:
    """Вернуть текстовую рекомендацию по вещи."""
    if is_item_suitable(item, current_season, current_temp):
        return f"{item['name']} подходит для носки сегодня."
    return f"{item['name']} не подходит для носки сегодня."
