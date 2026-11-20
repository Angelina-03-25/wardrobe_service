from django.urls import path
from . import views, views_auth
app_name = "wardrobe"

urlpatterns = [
    path("items/", views.item_list, name="item_list"),
    path("items/create/", views.item_create, name="item_create"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("items/<int:item_id>/edit/", views.item_edit, name="item_edit"),
    path("register/", views_auth.register_view, name="register"),
    path("login/", views_auth.login_view, name="login"),
    path("logout/", views_auth.logout_view, name="logout"),
]