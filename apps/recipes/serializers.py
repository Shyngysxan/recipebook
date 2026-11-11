"""
7-апта: Django REST Framework сериализаторлары.
Модель атаулары өзгеше болса, тек төмендегі import-ты түзет.
"""
from rest_framework import serializers

from .models import Category, Recipe   # <-- өз модельдеріңе сәйкес өзгерт


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    # Оқуға арналған қосымша өрістер (дизайнға әсер етпейді, тек API жауабында)
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def get_category_name(self, obj):
        category = getattr(obj, "category", None)
        return str(category) if category else None

    # ---- Валидация (тапсырма: міндетті өрістер + дұрыс қате жауаптары) ----
    def validate_title(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Рецепт атауы кемінде 2 таңбадан тұруы керек.")
        return value
