"""Views приложения homepage."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-каркас страницы с Bootstrap и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{bootstrap}">
</head>
<body>
<nav class="nav mb-4">
  <a class="nav-link" href="/">Главная</a>
  <a class="nav-link" href="/items/">Вещи</a>
  <a class="nav-link" href="/categories/">Категории</a>
  <a class="nav-link" href="/seasons/">Сезоны</a>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Сервис учета одежды</h1>
    <p class="lead">Веб-интерфейс личного гардероба.</p>
    <p>Основные разделы:</p>
    <a href="/items/" class="btn btn-primary me-2">Вещи</a>
    <a href="/categories/" class="btn btn-secondary me-2">Категории</a>
    <a href="/seasons/" class="btn btn-secondary">Сезоны</a>
    """
    return HttpResponse(page("Сервис учета одежды", content))


def page_not_found(request, exception):
    """Собственная страница 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )