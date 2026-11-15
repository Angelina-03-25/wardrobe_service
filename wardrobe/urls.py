from django.urls import path
from . import views, views_auth
from django.contrib.auth.decorators import login_required

app_name = "wardrobe"

urlpatterns = [
    path("items/", views.item_list, name="item_list"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("register/", views_auth.register_view, name="register"),
    path("login/", views_auth.login_view, name="login"),
    path("logout/", views_auth.logout_view, name="logout"),
]