from django.urls import path
from . import views

app_name = "wardrobe"

urlpatterns = [
    path("items/", views.item_list, name="item_list"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
]
