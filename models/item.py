"""Сущность Вещь."""

from datetime import datetime


class Item:
    """Вещь в гардеробе."""

    def __init__(
        self,
        item_id: int,
        wardrobe_id: int,
        category_id: int,
        season_id: int,
        name: str,
        min_temp: int,
    ) -> None:
        self.id = item_id
        self.wardrobe_id = wardrobe_id
        self.category_id = category_id
        self.season_id = season_id
        self.name = name
        self.min_temp = min_temp
        self.created_at = datetime.now()

    def __repr__(self) -> str:
        return f"Item(id={self.id}, name={self.name})"

    def is_suitable(self, current_temp: int) -> bool:
        """Подходит ли вещь по температуре."""
        return current_temp >= self.min_temp

    def to_dict(self) -> dict:
        """Сериализация в словарь."""
        return {
            "id": self.id,
            "wardrobe_id": self.wardrobe_id,
            "category_id": self.category_id,
            "season_id": self.season_id,
            "name": self.name,
            "min_temp": self.min_temp,
            "created_at": self.created_at.isoformat(),
        }
