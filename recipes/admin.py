from django.contrib import admin

from .models import Category, Ingredient, Recipe, RecipeIngredient, Review


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "cooking_time", "created_at")
    list_filter = ("category",)
    search_fields = ("title",)
    inlines = [RecipeIngredientInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "rating", "created_at")
    list_filter = ("rating",)