import sqlite3
from django.shortcuts import render

DB_PATH = "data/wardrobe.sqlite"

def category_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Выводим категории и считаем количество вещей в каждой
    categories = conn.execute("""
        SELECT categories.id, categories.name, COUNT(items.id) as cnt
        FROM categories
        LEFT JOIN items ON categories.id = items.category_id
        GROUP BY categories.id, categories.name
        ORDER BY categories.name
    """).fetchall()
    conn.close()
    return render(request, "catalog/category_list.html", {"categories": categories})

def season_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    seasons = conn.execute("SELECT id, name FROM seasons ORDER BY name").fetchall()
    conn.close()
    return render(request, "catalog/season_list.html", {"seasons": seasons})