from django.urls import path

from . import api_views

app_name = "recipes_api"

urlpatterns = [
    path("recipes/", api_views.RecipeListCreateView.as_view(), name="recipe-list"),
    path("recipes/<int:pk>/", api_views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("categories/", api_views.CategoryListView.as_view(), name="category-list"),
]
