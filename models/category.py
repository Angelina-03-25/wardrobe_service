"""Сущность Категория."""


class Category:
    """Категория вещи (например, верхняя одежда, обувь)."""

    def __init__(self, category_id: int, name: str) -> None:
        self.id = category_id
        self.name = name

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"

    def to_dict(self) -> dict:
        """Сериализация в словарь."""
        return {"id": self.id, "name": self.name}
