import json
from db.database import get_connection

STATE_FILE = "data/state.json"

def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)

def import_data(conn):
    data = load_json(STATE_FILE)
    
    # Пользователь
    user = data.get("user")
    if user:
        conn.execute(
            "INSERT INTO users (id, username, email) VALUES (?, ?, ?)",
            (user["id"], user["username"], user["email"])
        )
        
    # Гардероб
    wardrobe = data.get("wardrobe")
    if wardrobe:
        conn.execute(
            "INSERT INTO wardrobes (id, user_id, name) VALUES (?, ?, ?)",
            (wardrobe["id"], wardrobe["user_id"], wardrobe["name"])
        )
        
    # Категории
    for c in data.get("categories", []):
        conn.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (c["id"], c["name"]))
        
    # Сезоны
    for s in data.get("seasons", []):
        conn.execute("INSERT INTO seasons (id, name) VALUES (?, ?)", (s["id"], s["name"]))
        
    # Вещи
    for i in data.get("items", []):
        conn.execute(
            "INSERT INTO items (id, wardrobe_id, category_id, season_id, name, min_temp) VALUES (?, ?, ?, ?, ?, ?)",
            (i["id"], i["wardrobe_id"], i["category_id"], i["season_id"], i["name"], i["min_temp"])
        )

def main():
    conn = get_connection()
    try:
        import_data(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()