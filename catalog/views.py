"""Views приложения catalog — категории и сезоны."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_data


DATA_FILE = "data/state.json"


def category_list(request):
    """Список категорий."""
    data = load_data(DATA_FILE)
    categories = data.get("categories", [])

    if not categories:
        rows = (
            '<li class="list-group-item">'
            'Список категорий пуст.</li>'
        )
    else:
        rows = "".join(
            f'<li class="list-group-item">{c["name"]}</li>'
            for c in categories
        )

    content = f"""
    <h1>Категории</h1>
    <ul class="list-group">{rows}</ul>
    """
    return HttpResponse(page("Категории", content))


def season_list(request):
    """Список сезонов."""
    data = load_data(DATA_FILE)
    seasons = data.get("seasons", [])

    if not seasons:
        rows = (
            '<li class="list-group-item">'
            'Список сезонов пуст.</li>'
        )
    else:
        rows = "".join(
            f'<li class="list-group-item">{s["name"]}</li>'
            for s in seasons
        )

    content = f"""
    <h1>Сезоны</h1>
    <ul class="list-group">{rows}</ul>
    """
    return HttpResponse(page("Сезоны", content))