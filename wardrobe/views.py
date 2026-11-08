"""Views приложения wardrobe — работа с вещами."""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from wardrobe.models import Item
from catalog.models import Category


def item_list(request):
    """Список вещей с фильтрацией, сортировкой и пагинацией."""
    # 1. Базовая выборка (сразу подтягиваем связанные таблицы для оптимизации)
    items_qs = Item.objects.select_related('category', 'season')

    # 2. Поиск по названию
    query = request.GET.get('q', '').strip()
    if query:
        items_qs = items_qs.filter(name__icontains=query)

    # 3. Фильтрация по категории
    category_id = request.GET.get('category', '')
    if category_id.isdigit():
        items_qs = items_qs.filter(category_id=int(category_id))

    # 4. Сортировка
    sort_param = request.GET.get('sort', 'name')
    if sort_param == 'temp':
        items_qs = items_qs.order_by('min_temp')
    elif sort_param == 'temp_desc':
        items_qs = items_qs.order_by('-min_temp')
    else:
        items_qs = items_qs.order_by('name')

    # 5. Пагинация (по 3 вещи на страницу)
    paginator = Paginator(items_qs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем категории для выпадающего списка в фильтре
    categories = Category.objects.all()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "q": query,
        "selected_category": category_id,
        "sort": sort_param,
    }
    return render(request, "wardrobe/item_list.html", context)


def item_detail(request, item_id: int):
    """Страница одной вещи."""
    # get_object_or_404 автоматически вернет 404, если вещи нет
    item = get_object_or_404(
        Item.objects.select_related('category', 'season'),
        pk=item_id
    )
    return render(request, "wardrobe/item_detail.html", {"item": item})