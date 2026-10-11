"""Маршруты приложения catalog."""

from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.category_list, name="category_list"),
    path("seasons/", views.season_list, name="season_list"),
]