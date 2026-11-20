from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from wardrobe.models import Item, Wardrobe, User as ProfileUser
from catalog.models import Category, Season
from .forms import ItemFilterForm, ItemForm


def get_user_wardrobe(user):
    """Находит или создает гардероб пользователя."""
    profile_user = ProfileUser.objects.filter(username=user.username).first()
    if not profile_user:
        profile_user = ProfileUser.objects.create(username=user.username, email=user.email or "no@mail.ru")
    
    wardrobe = Wardrobe.objects.filter(user=profile_user).first()
    if not wardrobe:
        wardrobe = Wardrobe.objects.create(user=profile_user, name=f"Гардероб {user.username}")
    return wardrobe


@login_required
def item_list(request):
    """Список вещей ТОЛЬКО из гардероба текущего пользователя."""
    wardrobe = get_user_wardrobe(request.user)
    
    # ВАЖНО: Берем вещи, ID которых записаны в item_ids нашего гардероба!
    items_qs = Item.objects.filter(id__in=wardrobe.item_ids).select_related("category", "season")

    form = ItemFilterForm(request.GET or None)
    form_valid = form.is_bound and form.is_valid()

    if form_valid:
        category = form.cleaned_data.get("category")
        season = form.cleaned_data.get("season")
        max_temp = form.cleaned_data.get("max_temp")
        sort_param = form.cleaned_data.get("sort")

        if category: items_qs = items_qs.filter(category=category)
        if season: items_qs = items_qs.filter(season=season)
        if max_temp is not None: items_qs = items_qs.filter(min_temp__lte=max_temp)
        
        if sort_param == "temp": items_qs = items_qs.order_by("min_temp")
        elif sort_param == "temp_desc": items_qs = items_qs.order_by("-min_temp")
        else: items_qs = items_qs.order_by("name")
    else:
        items_qs = items_qs.order_by("name")

    paginator = Paginator(items_qs, 3)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "wardrobe/item_list.html", {"page_obj": page_obj, "form": form})


@login_required
def item_detail(request, item_id: int):
    """Страница вещи (только из своего гардероба)."""
    wardrobe = get_user_wardrobe(request.user)
    
    # Проверяем, есть ли ID вещи в списке item_ids
    if item_id not in wardrobe.item_ids:
        return render(request, "404.html", status=404)
        
    item = get_object_or_404(Item.objects.select_related("category", "season"), pk=item_id)
    return render(request, "wardrobe/item_detail.html", {"item": item})


@login_required
def item_create(request):
    """Создание вещи и добавление её в гардероб."""
    wardrobe = get_user_wardrobe(request.user)

    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save() # Создаем вещь
            
            # ДОБАВЛЯЕМ ID ВЕЩИ В СПИСОК ГАРДЕРОБА
            current_ids = wardrobe.item_ids
            current_ids.append(item.id)
            wardrobe.item_ids = current_ids
            wardrobe.save()
            
            return redirect("wardrobe:item_list")
    else:
        form = ItemForm()

    return render(request, "wardrobe/item_form.html", {
        "form": form,
        "categories": Category.objects.all(),
        "seasons": Season.objects.all(),
    })


@login_required
def item_edit(request, item_id: int):
    """Редактирование вещи (только своей)."""
    wardrobe = get_user_wardrobe(request.user)
    
    # Проверяем, есть ли ID вещи в списке item_ids
    if item_id not in wardrobe.item_ids:
        return render(request, "404.html", status=404)
        
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("wardrobe:item_detail", item_id=item.id)
    else:
        form = ItemForm(instance=item)

    return render(request, "wardrobe/item_form.html", {
        "form": form,
        "item": item,
        "categories": Category.objects.all(),
        "seasons": Season.objects.all(),
    })