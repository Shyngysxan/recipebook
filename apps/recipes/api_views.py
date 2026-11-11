"""
7-апта: DRF generic views.
GET /api/recipes/          – тізім        | POST – жаңа рецепт
GET /api/recipes/<id>/     – бір рецепт   | PUT/PATCH – өзгерту | DELETE – жою
GET /api/categories/       – санаттар тізімі
"""
from rest_framework import generics

from .models import Category, Recipe
from .serializers import CategorySerializer, RecipeSerializer


class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
