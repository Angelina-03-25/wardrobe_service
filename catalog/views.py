from django.shortcuts import render
from django.db.models import Count
from catalog.models import Category, Season

def category_list(request):
    # Используем annotate для подсчета вещей в каждой категории (аналог GROUP BY)
    categories = Category.objects.annotate(items_count=Count('items')).order_by('name')
    return render(request, "catalog/category_list.html", {"categories": categories})

def season_list(request):
    seasons = Season.objects.annotate(items_count=Count('items')).order_by('name')
    return render(request, "catalog/season_list.html", {"seasons": seasons})