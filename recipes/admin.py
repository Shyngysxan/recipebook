from django.contrib import admin

from .models import Category, Cuisine, Recipe, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("icon", "name", "recipe_count")
    search_fields = ("name",)

    @admin.display(description="Рецепт саны")
    def recipe_count(self, obj):
        return obj.recipes.count()


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ("name", "recipe_count")
    search_fields = ("name",)

    @admin.display(description="Рецепт саны")
    def recipe_count(self, obj):
        return obj.recipes.count()


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "cuisine", "difficulty", "cooking_time", "created_at")
    list_filter = ("category", "cuisine", "difficulty")
    raw_id_fields = ("author",)
    search_fields = ("title", "description")
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("recipe", "author_name", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("author_name", "comment")
