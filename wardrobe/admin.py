from django.contrib import admin
from .models import User, Wardrobe, Item

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")

@admin.register(Wardrobe)
class WardrobeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "item_ids")
    search_fields = ("name", "user__username")
    # Убрали filter_horizontal, так как поля items больше нет

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "season", "min_temp")
    search_fields = ("name",)
    list_filter = ("category", "season")