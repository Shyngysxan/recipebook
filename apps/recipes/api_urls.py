from django.urls import path

from . import api_views as v

app_name = "recipes_api"

urlpatterns = [
    # Recipe
    path("recipes/", v.RecipeListCreateView.as_view(), name="recipe-list"),
    path("recipes/<int:pk>/", v.RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipes/<int:recipe_id>/reviews/", v.RecipeReviewsView.as_view(), name="recipe-reviews"),
    # Category
    path("categories/", v.CategoryListCreateView.as_view(), name="category-list"),
    path("categories/<int:pk>/", v.CategoryDetailView.as_view(), name="category-detail"),
    path("categories/<int:category_id>/recipes/", v.CategoryRecipesView.as_view(), name="category-recipes"),
    # Cuisine
    path("cuisines/", v.CuisineListCreateView.as_view(), name="cuisine-list"),
    path("cuisines/<int:pk>/", v.CuisineDetailView.as_view(), name="cuisine-detail"),
    path("cuisines/<int:cuisine_id>/recipes/", v.CuisineRecipesView.as_view(), name="cuisine-recipes"),
    # Review
    path("reviews/", v.ReviewListCreateView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", v.ReviewDetailView.as_view(), name="review-detail"),
]
