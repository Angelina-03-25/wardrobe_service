"""Views приложения wardrobe — работа с вещами."""

from django.http import HttpResponse

from homepage.views import page
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
    return [
        Category(c["id"], c["name"])
        for c in data.get("categories", [])
    ]


def build_seasons(data: dict) -> list[Season]:
    return [
        Season(s["id"], s["name"])
        for s in data.get("seasons", [])
    ]


def item_list(request):
    data = load_data(DATA_FILE)
    items = build_items(data)
    categories = {c.id: c.name for c in build_categories(data)}
    seasons = {s.id: s.name for s in build_seasons(data)}

    if not items:
        rows = (
            '<li class="list-group-item">'
            'Список вещей пуст.</li>'
        )
    else:
        rows = ""
        for item in items:
            cat = categories.get(item.category_id, "—")
            season = seasons.get(item.season_id, "—")
            rows += (
                f'<li class="list-group-item d-flex '
                f'justify-content-between">'
                f'<span>{item.name} — {cat}, {season}</span>'
                f'<a href="/items/{item.id}/" '
                f'class="btn btn-sm btn-outline-primary">'
                f'Открыть</a>'
                f'</li>'
            )

    content = f"""
    <h1>Вещи</h1>
    <ul class="list-group">{rows}</ul>
    """
    return HttpResponse(page("Список вещей", content))


def item_detail(request, item_id: int):
    data = load_data(DATA_FILE)
    items = build_items(data)
    categories = {c.id: c.name for c in build_categories(data)}
    seasons = {s.id: s.name for s in build_seasons(data)}

    item = next((i for i in items if i.id == item_id), None)

    if item is None:
        content = """
        <h1 class="text-danger">Вещь не найдена</h1>
        <a href="/items/" class="btn btn-outline-secondary">
        ← к списку вещей
        </a>
        """
        return HttpResponse(
            page("Вещь не найдена", content),
            status=404,
        )

    cat = categories.get(item.category_id, "—")
    season = seasons.get(item.season_id, "—")

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{item.name}</h5>
        <p class="card-text"><strong>ID:</strong> {item.id}</p>
        <p class="card-text">
          <strong>Категория:</strong> {cat}
        </p>
        <p class="card-text"><strong>Сезон:</strong> {season}</p>
        <p class="card-text">
          <strong>Минимальная температура:</strong>
          {item.min_temp}°C
        </p>
        <a href="/items/" class="btn btn-outline-secondary">
        ← к списку вещей
        </a>
      </div>
    </div>
    """
    return HttpResponse(page(item.name, content))