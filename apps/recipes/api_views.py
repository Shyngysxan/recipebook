"""
8-апта: бірнеше байланысқан модельге арналған API (DRF generic views).

Recipe   : GET/POST /api/drf/recipes/        GET/PUT/PATCH/DELETE /api/drf/recipes/<id>/
Category : GET/POST /api/drf/categories/     GET/PUT/PATCH/DELETE /api/drf/categories/<id>/
Cuisine  : GET/POST /api/drf/cuisines/       GET/PUT/PATCH/DELETE /api/drf/cuisines/<id>/
Review   : GET/POST /api/drf/reviews/        GET/PUT/PATCH/DELETE /api/drf/reviews/<id>/
Байланыс : GET /api/drf/categories/<id>/recipes/   – санат бойынша рецепттер
           GET /api/drf/cuisines/<id>/recipes/     – асхана бойынша рецепттер
           GET /api/drf/recipes/<id>/reviews/      – рецепт бойынша пікірлер
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Category, Cuisine, Recipe, Review
from .serializers import (CategorySerializer, CuisineSerializer, RecipeDetailSerializer,
                          RecipeSerializer, ReviewSerializer)


# ---------- Recipe ----------
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.select_related("category", "cuisine").order_by("-created_at", "-id")
    serializer_class = RecipeSerializer


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.select_related("category", "cuisine").prefetch_related("reviews")

    def get_serializer_class(self):
        # GET кезінде пікірлермен қоса, жазу кезінде қарапайым сериализатор
        return RecipeDetailSerializer if self.request.method == "GET" else RecipeSerializer


# ---------- Category ----------
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ---------- Cuisine ----------
class CuisineListCreateView(generics.ListCreateAPIView):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer


class CuisineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer


# ---------- Review ----------
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.select_related("recipe").order_by("-created_at", "-id")
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related("recipe")
    serializer_class = ReviewSerializer


# ---------- Байланыс бойынша алу (жоқ id болса – 404) ----------
class CategoryRecipesView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs["category_id"])
        return (Recipe.objects.select_related("category", "cuisine")
                .filter(category=category).order_by("-created_at", "-id"))


class CuisineRecipesView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        cuisine = get_object_or_404(Cuisine, pk=self.kwargs["cuisine_id"])
        return (Recipe.objects.select_related("category", "cuisine")
                .filter(cuisine=cuisine).order_by("-created_at", "-id"))


class RecipeReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        return Review.objects.select_related("recipe").filter(recipe=recipe).order_by("-created_at", "-id")
