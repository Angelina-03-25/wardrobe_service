"""
Вспомогательные функции безопасного ввода.
"""


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число. Повторять при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Некорректный ввод. Введите целое число.")


def input_str(prompt: str) -> str:
    """Запросить у пользователя непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Строка не может быть пустой.")
