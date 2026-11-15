from django.contrib import admin
from .models import User, Wardrobe, Item


class ItemInline(admin.TabularInline):
    """Позволяет видеть и редактировать вещи прямо внутри гардероба."""
    model = Item
    extra = 1  # Количество пустых форм для добавления новых вещей


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")
    ordering = ("username",)


@admin.register(Wardrobe)
class WardrobeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "user__username")
    list_filter = ("user",)
    inlines = [ItemInline]  # Подключаем вещи внутрь гардероба


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "season", "min_temp", "wardrobe")
    search_fields = ("name",)
    list_filter = ("category", "season", "wardrobe")
    ordering = ("name",)