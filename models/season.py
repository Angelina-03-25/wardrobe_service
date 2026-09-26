"""Сущность Сезон."""


class Season:
    """Сезон, к которому относится вещь."""

    def __init__(self, season_id: int, name: str) -> None:
        self.id = season_id
        self.name = name

    def __repr__(self) -> str:
        return f"Season(id={self.id}, name={self.name})"

    def to_dict(self) -> dict:
        """Сериализация в словарь."""
        return {"id": self.id, "name": self.name}
