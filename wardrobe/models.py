from django.db import models
from catalog.models import Category, Season

class User(models.Model):
    username = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Wardrobe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wardrobe")
    name = models.CharField(max_length=100, verbose_name="Название гардероба")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Гардероб"
        verbose_name_plural = "Гардеробы"

class Item(models.Model):
    wardrobe = models.ForeignKey(Wardrobe, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    season = models.ForeignKey(Season, on_delete=models.PROTECT, related_name="items")
    name = models.CharField(max_length=100, verbose_name="Название вещи")
    min_temp = models.IntegerField(verbose_name="Минимальная температура")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"