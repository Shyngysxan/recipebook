from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Cuisine, Recipe, Review


# ---------------- Category / Cuisine ----------------
class CategorySerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class CuisineSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Cuisine
        fields = "__all__"

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class CategoryShortSerializer(serializers.ModelSerializer):
    """Рецепттің ішінде көрсетуге арналған қысқа нұсқа."""

    class Meta:
        model = Category
        fields = ["id", "name", "icon"]


class CuisineShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ["id", "name"]


# ---------------- Review ----------------
class ReviewSerializer(serializers.ModelSerializer):
    recipe_title = serializers.CharField(source="recipe.title", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["id", "created_at"]
    # rating (1–5) және recipe (бар id) тексерулерін модель мен ModelSerializer өзі жасайды


# ---------------- Recipe ----------------
class RecipeSerializer(serializers.ModelSerializer):
    """
    Жазу кезінде:  "category": 2, "cuisine": 1   (ForeignKey id-лері)
    Оқу кезінде:   category_name, category_detail, cuisine_detail, average_rating, reviews_count
    """
    category_name = serializers.SerializerMethodField(read_only=True)
    cuisine_name = serializers.SerializerMethodField(read_only=True)
    category_detail = CategoryShortSerializer(source="category", read_only=True)
    cuisine_detail = CuisineShortSerializer(source="cuisine", read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    reviews_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_cuisine_name(self, obj):
        return obj.cuisine.name if obj.cuisine else None

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(a=Avg("rating"))["a"]
        return round(avg, 1) if avg is not None else None

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Рецепт атауы кемінде 2 таңбадан тұруы керек.")
        return value


class RecipeDetailSerializer(RecipeSerializer):
    """Бір рецептті ашқанда – пікірлер тізімі де қосылады."""
    reviews = ReviewSerializer(many=True, read_only=True)
