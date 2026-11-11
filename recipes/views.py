import json

from django.contrib.auth import login
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods

from .forms import RegisterForm
from .models import Category, Cuisine, Recipe


# ---------- Сайттың беттері (қолданушы көреді) ----------

@require_GET
@ensure_csrf_cookie
def home(request):
    return render(request, "recipes/home.html")


@require_GET
@ensure_csrf_cookie
def recipe_page(request, pk):
    return render(request, "recipes/recipe_detail.html", {"recipe_id": pk})


# ---------- Авторизация: тіркелу ----------
# Кіру (login) мен шығу (logout) — urls.py ішінде Django-ның дайын LoginView/LogoutView арқылы.

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)  # тіркелген бойда аккаунтқа кіргізіп жібереміз
        return redirect("home")

    return render(request, "recipes/register.html", {"form": form})


# ---------- API көмекші функциялары ----------

def error(message, status, **extra):
    return JsonResponse({"status": "error", "message": message, **extra}, status=status)


def recipes_queryset():
    return Recipe.objects.select_related("category", "cuisine", "author").annotate(
        rating_avg=Avg("reviews__rating"),
        reviews_count=Count("reviews"),
    )


def can_modify(user, recipe):
    """Рецептті автор немесе админ (staff) өзгерте/өшіре алады."""
    if not user.is_authenticated:
        return False
    return user.is_staff or (recipe.author_id is not None and recipe.author_id == user.id)


def serialize_recipe(recipe, full=False, user=None):
    category, cuisine = recipe.category, recipe.cuisine
    rating = getattr(recipe, "rating_avg", None)
    data = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "cooking_time": recipe.cooking_time,
        "servings": recipe.servings,
        "difficulty": recipe.difficulty,
        "difficulty_label": recipe.get_difficulty_display(),
        "category_id": recipe.category_id,
        "category_name": category.name if category else None,
        "category_icon": category.icon if category else None,
        "cuisine_id": recipe.cuisine_id,
        "cuisine_name": cuisine.name if cuisine else None,
        "rating_avg": round(rating, 1) if rating is not None else None,
        "reviews_count": getattr(recipe, "reviews_count", 0),
        "author_id": recipe.author_id,
        "author_name": recipe.author.username if recipe.author_id else None,
        "can_edit": bool(user and can_modify(user, recipe)),
        "created_at": recipe.created_at.isoformat(),
    }
    if full:
        data["ingredients"] = recipe.ingredients
        data["instructions"] = recipe.instructions
        data["reviews"] = [
            {
                "id": review.id,
                "author_name": review.author_name,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat(),
            }
            for review in recipe.reviews.order_by("-created_at", "-id")
        ]
    return data


def parse_json(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def is_positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def check_text(data, key, errors, cleaned, required, max_length=None):
    value = data.get(key, "")
    if not isinstance(value, str):
        errors[key] = "Мәтін болуы керек"
    elif required and not value.strip():
        errors[key] = "Міндетті өріс: бос емес мәтін"
    elif max_length and len(value.strip()) > max_length:
        errors[key] = f"{max_length} таңбадан аспауы керек"
    else:
        cleaned[key] = value.strip()


def check_foreign_key(data, key, model, errors, cleaned):
    value = data.get(key)
    if value is None:
        cleaned[key] = None
    elif not is_positive_int(value) or not model.objects.filter(pk=value).exists():
        errors[key] = "Мұндай жазба жоқ"
    else:
        cleaned[key] = value


def validate_recipe(data):
    errors = {}
    cleaned = {}

    check_text(data, "title", errors, cleaned, required=True, max_length=200)
    check_text(data, "description", errors, cleaned, required=False)
    check_text(data, "ingredients", errors, cleaned, required=True)
    check_text(data, "instructions", errors, cleaned, required=True)

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

    difficulty = data.get("difficulty", "medium")
    if difficulty not in dict(Recipe.DIFFICULTY_CHOICES):
        errors["difficulty"] = "easy, medium немесе hard болуы керек"
    else:
        cleaned["difficulty"] = difficulty

    check_foreign_key(data, "category_id", Category, errors, cleaned)
    check_foreign_key(data, "cuisine_id", Cuisine, errors, cleaned)

    return cleaned, errors


# ---------- API: /api/recipes/ және /api/recipes/<id>/ ----------

@require_http_methods(["GET", "POST"])
def recipe_list(request):
    if request.method == "GET":
        recipes = recipes_queryset().order_by("-created_at", "-id")
        return JsonResponse([serialize_recipe(r, user=request.user) for r in recipes], safe=False)

    if not request.user.is_authenticated:
        return error("Рецепт қосу үшін аккаунтқа кіріңіз", 401)

    data = parse_json(request)
    if data is None:
        return error("Дұрыс емес JSON", 400)

    cleaned, errors = validate_recipe(data)
    if errors:
        return error("Валидация қатесі", 400, errors=errors)

    recipe = Recipe.objects.create(author=request.user, **cleaned)
    recipe = recipes_queryset().get(pk=recipe.pk)
    return JsonResponse(serialize_recipe(recipe, full=True, user=request.user), status=201)


@require_http_methods(["GET", "PUT", "DELETE"])
def recipe_detail(request, pk):
    try:
        recipe = recipes_queryset().get(pk=pk)
    except Recipe.DoesNotExist:
        return error("Рецепт табылмады", 404)

    if request.method == "GET":
        return JsonResponse(serialize_recipe(recipe, full=True, user=request.user))

    if not request.user.is_authenticated:
        return error("Бұл әрекет үшін аккаунтқа кіріңіз", 401)
    if not can_modify(request.user, recipe):
        return error("Тек рецепт авторы өзгерте алады", 403)

    if request.method == "PUT":
        data = parse_json(request)
        if data is None:
            return error("Дұрыс емес JSON", 400)

        cleaned, errors = validate_recipe(data)
        if errors:
            return error("Валидация қатесі", 400, errors=errors)

        for field, value in cleaned.items():
            setattr(recipe, field, value)
        recipe.save()
        recipe = recipes_queryset().get(pk=pk)
        return JsonResponse(serialize_recipe(recipe, full=True, user=request.user))

    recipe.delete()
    return JsonResponse({"status": "ok", "message": "Рецепт өшірілді"})
