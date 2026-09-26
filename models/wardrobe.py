"""Сущность Гардероб — связывает пользователя и вещи."""

from datetime import datetime


class Wardrobe:
    """Гардероб пользователя.

    У одного пользователя ровно один гардероб,
    в одном гардеробе может быть много вещей.
    """

    def __init__(self, wardrobe_id: int, user_id: int, name: str) -> None:
        self.id = wardrobe_id
        self.user_id = user_id
        self.name = name
        self.created_at = datetime.now()

    def __repr__(self) -> str:
        return (
            f"Wardrobe(id={self.id}, "
            f"user_id={self.user_id}, "
            f"name={self.name})"
        )

    def to_dict(self) -> dict:
        """Сериализация в словарь."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
        }
