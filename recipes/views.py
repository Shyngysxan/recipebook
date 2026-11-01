import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Category, Recipe

User = get_user_model()


def error(message, status, **extra):
    return JsonResponse({"status": "error", "message": message, **extra}, status=status)


def serialize_recipe(recipe):
    return {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "instructions": recipe.instructions,
        "cooking_time": recipe.cooking_time,
        "servings": recipe.servings,
        "category_id": recipe.category_id,
        "author_id": recipe.author_id,
        "created_at": recipe.created_at.isoformat(),
    }


def parse_json(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def is_positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def validate_recipe(data, creating):
    errors = {}
    cleaned = {}

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        errors["title"] = "Міндетті өріс: бос емес мәтін"
    elif len(title.strip()) > 200:
        errors["title"] = "200 таңбадан аспауы керек"
    else:
        cleaned["title"] = title.strip()

    instructions = data.get("instructions")
    if not isinstance(instructions, str) or not instructions.strip():
        errors["instructions"] = "Міндетті өріс: бос емес мәтін"
    else:
        cleaned["instructions"] = instructions.strip()

    cooking_time = data.get("cooking_time")
    if not is_positive_int(cooking_time):
        errors["cooking_time"] = "Міндетті өріс: 0-ден үлкен бүтін сан (минут)"
    else:
        cleaned["cooking_time"] = cooking_time

    servings = data.get("servings", 2)
    if not is_positive_int(servings):
        errors["servings"] = "0-ден үлкен бүтін сан болуы керек"
    else:
        cleaned["servings"] = servings

    description = data.get("description", "")
    if not isinstance(description, str):
        errors["description"] = "Мәтін болуы керек"
    else:
        cleaned["description"] = description

    category_id = data.get("category_id")
    if category_id is None:
        cleaned["category_id"] = None
    elif not is_positive_int(category_id) or not Category.objects.filter(pk=category_id).exists():
        errors["category_id"] = "Мұндай санат жоқ"
    else:
        cleaned["category_id"] = category_id

    if creating:
        author_id = data.get("author_id")
        if not is_positive_int(author_id) or not User.objects.filter(pk=author_id).exists():
            errors["author_id"] = "Міндетті өріс: бар пайдаланушының id-і"
        else:
            cleaned["author_id"] = author_id

    return cleaned, errors


@csrf_exempt
@require_http_methods(["GET", "POST"])
def recipe_list(request):
    if request.method == "GET":
        recipes = Recipe.objects.all().order_by("-created_at")
        return JsonResponse([serialize_recipe(r) for r in recipes], safe=False)

    data = parse_json(request)
    if data is None:
        return error("Дұрыс емес JSON", 400)

    cleaned, errors = validate_recipe(data, creating=True)
    if errors:
        return error("Валидация қатесі", 400, errors=errors)

    recipe = Recipe.objects.create(**cleaned)
    return JsonResponse(serialize_recipe(recipe), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return error("Рецепт табылмады", 404)

    if request.method == "GET":
        return JsonResponse(serialize_recipe(recipe))

    if request.method == "PUT":
        data = parse_json(request)
        if data is None:
            return error("Дұрыс емес JSON", 400)

        cleaned, errors = validate_recipe(data, creating=False)
        if errors:
            return error("Валидация қатесі", 400, errors=errors)

        for field, value in cleaned.items():
            setattr(recipe, field, value)
        recipe.save()
        return JsonResponse(serialize_recipe(recipe))

    recipe.delete()
    return JsonResponse({"status": "ok", "message": "Рецепт өшірілді"})