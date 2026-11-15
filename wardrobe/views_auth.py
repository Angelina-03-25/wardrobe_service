from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User as ProfileUser, Wardrobe

def register_view(request):
    """Регистрация нового пользователя."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 1. Создаем стандартного пользователя Django
            user = form.save()
            
            # 2. Создаем пользователя в нашей предметной области
            profile_user = ProfileUser.objects.create(
                username=user.username,
                email=user.email or "no-email@example.com"
            )
            
            # 3. Создаем для него гардероб
            Wardrobe.objects.create(
                user=profile_user,
                name=f"Гардероб {user.username}"
            )
            
            # 4. Автоматически логиним пользователя
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            authenticated_user = authenticate(username=username, password=raw_password)
            login(request, authenticated_user)
            
            return redirect("homepage:index")
    else:
        form = UserCreationForm()
    return render(request, "wardrobe/register.html", {"form": form})


def login_view(request):
    """Вход в систему."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage:index")
    else:
        form = AuthenticationForm()
    return render(request, "wardrobe/login.html", {"form": form})


def logout_view(request):
    """Выход из системы."""
    logout(request)
    return redirect("wardrobe:login")