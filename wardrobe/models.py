from django.db import models
from catalog.models import Category, Season

class User(models.Model):
    username = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.username

class Wardrobe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wardrobe")
    name = models.CharField(max_length=100, verbose_name="Название гардероба")
    item_ids = models.JSONField(default=list, verbose_name="Список ID вещей")

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название вещи")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    season = models.ForeignKey(Season, on_delete=models.PROTECT, related_name="items")
    min_temp = models.IntegerField(verbose_name="Минимальная температура")

    def __str__(self):
        return self.name