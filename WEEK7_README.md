# 7-апта: Django REST Framework және сериализаторлар (Recipebook)

Бұл қосымша **сайттың дизайнына, шаблондарына, static файлдарына тиіспейді**.
Тек жаңа 3 файл қосылады, ескі CRUD маршруттар (6-апта) өз орнында қалады.
Жаңа API `/api/` префиксімен істейді.

## 1. Орнату
```bash
pip install djangorestframework
pip freeze > requirements.txt
```

## 2. Файлдарды көшіру
`apps/recipes/` ішіне осы 3 файлды көшір:
- `serializers.py`
- `api_views.py`
- `api_urls.py`

(Егер қазір қосымшаң `apps/` ішінде емес, `recipes/` түбірінде тұрса – сол папкаға көшір. `MOVE_TO_APPS.md` қара.)

Файлдағы `from .models import Category, Recipe` жолын өз модель атауларыңа сәйкес өзгерт.

## 3. settings.py
```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "apps.recipes",   # (apps/ құрылымында; әйтпесе "recipes")
]
```

## 4. Басты urls.py (core/urls.py)
```python
from django.urls import path, include

urlpatterns = [
    # ... бұрынғы маршруттар өзгеріссіз ...
    path("api/", include("apps.recipes.api_urls")),
]
```

## 5. Тексеру
```bash
python manage.py runserver
```
Браузерде: http://127.0.0.1:8000/api/recipes/  (DRF Browsable API ашылады)

curl / Postman:
```bash
# тізім
curl http://127.0.0.1:8000/api/recipes/
# бір рецепт
curl http://127.0.0.1:8000/api/recipes/1/
# жасау (өз өрістеріңе қарай)
curl -X POST http://127.0.0.1:8000/api/recipes/ -H "Content-Type: application/json" \
     -d '{"title": "Плов", "description": "Қазақша плов", "category": 1}'
# өзгерту
curl -X PATCH http://127.0.0.1:8000/api/recipes/1/ -H "Content-Type: application/json" -d '{"title": "Жаңа атау"}'
# жою
curl -X DELETE http://127.0.0.1:8000/api/recipes/1/
# қате: міндетті өріс жоқ -> 400, жоқ id -> 404
curl -X POST http://127.0.0.1:8000/api/recipes/ -H "Content-Type: application/json" -d '{}'
curl http://127.0.0.1:8000/api/recipes/9999/
```

## Тапсырма пункттерін орындау
| Пункт | Қайда |
|---|---|
| DRF орнату, INSTALLED_APPS | 1, 3 қадам |
| ModelSerializer | `serializers.py` |
| GET және POST DRF-ке көшіру | `RecipeListCreateView` |
| Бір жазбаны алу/өзгерту/жою | `RecipeDetailView` |
| Валидация, қате жауаптары | `validate_title` + ModelSerializer міндетті өрістері (400) |
| Postman және Browsable API | 5 қадам |

