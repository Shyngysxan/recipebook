# Жобаны `apps/` құрылымына келтіру (3-сурет бойынша)

Мақсат: әр қосымша `apps/` ішінде тұрсын, ал `core/` тек баптаулар болсын,
сонда қосымшаны (`apps/recipes`) басқа жобаға папкамен көшіріп қоя салуға болады.

```
recipebook/
├── core/               # бұрынғы жоба папкасы (settings.py, urls.py, wsgi.py)
├── manage.py
├── apps/
│   ├── __init__.py     # бос файл
│   └── recipes/
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py  apps.py  models.py  views.py  tests.py
│       ├── serializers.py  api_views.py  api_urls.py   # 7-апта
├── templates/
├── static/
├── media/
└── venv/ (virtual_env)
```

## Қадамдар
1. `apps/` папкасын және ішіне бос `__init__.py` жаса.
2. Қосымша папкасын (`recipes`) `apps/recipes` ішіне жылжыт.
3. `apps/recipes/apps.py`:
   ```python
   class RecipesConfig(AppConfig):
       default_auto_field = "django.db.models.BigAutoField"
       name = "apps.recipes"
       label = "recipes"      # миграциялар мен БД кестелері бұзылмау үшін
   ```
4. `settings.py` → `INSTALLED_APPS`: `"recipes"` орнына `"apps.recipes"`.
5. Барлық импорттарды түзет: `from recipes.models import ...` → `from apps.recipes.models import ...`.
   (`core/urls.py`: `include("apps.recipes.urls")`.)
6. Шаблондар жоба түбіріндегі `templates/`, static – `static/` болса, settings-те:
   ```python
   TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
   STATICFILES_DIRS = [BASE_DIR / "static"]
   MEDIA_URL = "/media/"; MEDIA_ROOT = BASE_DIR / "media"
   ```
7. Егер жоба папкасын `core` деп атағың келсе: папканы ауыстырып, `manage.py`, `wsgi.py`, `asgi.py`-дағы
   `DJANGO_SETTINGS_MODULE` және `settings.py`-дағы `ROOT_URLCONF`, `WSGI_APPLICATION` мәндерін `core.*` деп өзгерт.
8. `python manage.py check` және `runserver` – қате болмаса, дайын.

`label = "recipes"` қалдырсаң, бар SQLite дерегің мен миграциялар сақталады.
