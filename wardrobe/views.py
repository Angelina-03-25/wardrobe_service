import sqlite3
from django.shortcuts import render
from django.http import HttpResponse

DB_PATH = "data/wardrobe.sqlite"

def item_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    items = conn.execute("""
        SELECT items.id, items.name, items.min_temp, 
               categories.name AS category, seasons.name AS season
        FROM items
        JOIN categories ON items.category_id = categories.id
        JOIN seasons ON items.season_id = seasons.id
        ORDER BY items.name
    """).fetchall()
    conn.close()
    return render(request, "wardrobe/item_list.html", {"items": items})

def item_detail(request, item_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    item = conn.execute("""
        SELECT items.id, items.name, items.min_temp, 
               categories.name AS category, seasons.name AS season
        FROM items
        JOIN categories ON items.category_id = categories.id
        JOIN seasons ON items.season_id = seasons.id
        WHERE items.id = ?
    """, (item_id,)).fetchone()
    conn.close()
    
    return render(request, "wardrobe/item_detail.html", {
        "item": item,
    }, status=404 if item is None else 200)