"""Сущность Пользователь."""

from datetime import datetime


class User:
    """Пользователь сервиса учета одежды.

    У каждого пользователя ровно один гардероб.
    """

    def __init__(self, user_id: int, username: str, email: str) -> None:
        self.id = user_id
        self.username = username
        self.email = email
        self.created_at = datetime.now()

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"

    def to_dict(self) -> dict:
        """Сериализация в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }
