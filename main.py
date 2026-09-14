"""
ПР1. Начальный сценарий индивидуального проекта.
Тема: Сервис учета одежды.
"""

from datetime import date

username = "Анна"
item_name = "Зимнее пальто"
category = "Верхняя одежда"
season = "Зима"
min_temp = -15 
current_temp = -5     
is_clean = True        


def is_season_match(item_season: str, current_season: str) -> bool:
    """Проверяет, подходит ли вещь для текущего сезона."""
    if item_season == current_season or item_season == "Всесезон":
        return True
    return False



def is_temp_suitable(item_min_temp: int, current_temp: int) -> bool:
    """Проверяет, подходит ли вещь по температуре."""
    if current_temp >= item_min_temp:
        return True
    return False



def get_recommendation(season_ok: bool, temp_ok: bool, clean: bool) -> str:
    """Формирует текстовую рекомендацию по вещи."""
    if not clean:
        return "Вещь нужно постирать перед ноской."
    if season_ok and temp_ok:
        return "Вещь подходит для носки сегодня."
    if not season_ok:
        return "Вещь не подходит по сезону."
    return "Вещь не подходит по температуре."



def main() -> None:
    current_season = "Зима"

    season_ok = is_season_match(season, current_season)
    temp_ok = is_temp_suitable(min_temp, current_temp)
    recommendation = get_recommendation(season_ok, temp_ok, is_clean)

    print(f"Пользователь: {username}")
    print(f"Вещь: {item_name}")
    print(f"Категория: {category}")
    print(f"Сезон: {season}")
    print(f"Мин. температура: {min_temp}°C")
    print(f"Текущая температура: {current_temp}°C")
    print(f"Рекомендация: {recommendation}")


if __name__ == "__main__":
    main()