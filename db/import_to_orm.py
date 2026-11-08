import os
import sys
import sqlite3
import django

# Настраиваем окружение Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wardrobe_web.settings")
django.setup()

from wardrobe.models import User, Wardrobe, Item
from catalog.models import Category, Season

OLD_DB = os.path.join(BASE_DIR, "data", "wardrobe.sqlite")

def import_data():
    if not os.path.exists(OLD_DB):
        print("Старая база не найдена!")
        return

    conn = sqlite3.connect(OLD_DB)
    conn.row_factory = sqlite3.Row

    # 1. Пользователи
    for row in conn.execute("SELECT * FROM users"):
        User.objects.update_or_create(
            id=row["id"],
            defaults={"username": row["username"], "email": row["email"]}
        )

    # 2. Гардеробы
    for row in conn.execute("SELECT * FROM wardrobes"):
        Wardrobe.objects.update_or_create(
            id=row["id"],
            defaults={"user_id": row["user_id"], "name": row["name"]}
        )

    # 3. Категории
    for row in conn.execute("SELECT * FROM categories"):
        Category.objects.update_or_create(
            id=row["id"],
            defaults={"name": row["name"]}
        )

    # 4. Сезоны
    for row in conn.execute("SELECT * FROM seasons"):
        Season.objects.update_or_create(
            id=row["id"],
            defaults={"name": row["name"]}
        )

    # 5. Вещи
    for row in conn.execute("SELECT * FROM items"):
        Item.objects.update_or_create(
            id=row["id"],
            defaults={
                "wardrobe_id": row["wardrobe_id"],
                "category_id": row["category_id"],
                "season_id": row["season_id"],
                "name": row["name"],
                "min_temp": row["min_temp"]
            }
        )
    
    conn.close()
    print("Данные успешно перенесены в ORM!")

if __name__ == "__main__":
    import_data()