from django.shortcuts import render
from models import Item, Category, Season
from storage import load_data


DATA_FILE = "data/state.json"


def build_items(data: dict) -> list[Item]:
    return [
        Item(
            item_id=raw["id"],
            wardrobe_id=raw["wardrobe_id"],
            category_id=raw["category_id"],
            season_id=raw["season_id"],
            name=raw["name"],
            min_temp=raw["min_temp"],
        )
        for raw in data.get("items", [])
    ]


def build_categories(data: dict) -> list[Category]:
    return [Category(c["id"], c["name"]) for c in data.get("categories", [])]


def build_seasons(data: dict) -> list[Season]:
    return [Season(s["id"], s["name"]) for s in data.get("seasons", [])]


def item_list(request):
    data = load_data(DATA_FILE)
    items = build_items(data)
    context = {"items": items}
    return render(request, "wardrobe/item_list.html", context)


def item_detail(request, item_id: int):
    data = load_data(DATA_FILE)
    items = build_items(data)
    categories = {c.id: c.name for c in build_categories(data)}
    seasons = {s.id: s.name for s in build_seasons(data)}

    item = next((i for i in items if i.id == item_id), None)

    context = {
        "item": item,
        "category_name": categories.get(item.category_id, "—") if item else "",
        "season_name": seasons.get(item.season_id, "—") if item else "",
    }
    return render(
        request,
        "wardrobe/item_detail.html",
        context,
        status=404 if item is None else 200
    )
