from django.shortcuts import render
from storage import load_data


DATA_FILE = "data/state.json"


def category_list(request):

    data = load_data(DATA_FILE)
    context = {"categories": data.get("categories", [])}
    return render(request, "catalog/category_list.html", context)


def season_list(request):

    data = load_data(DATA_FILE)
    context = {"seasons": data.get("seasons", [])}
    return render(request, "catalog/season_list.html", context)
