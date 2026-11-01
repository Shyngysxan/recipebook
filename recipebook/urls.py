from django.contrib import admin
from django.urls import path

from recipes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/recipes/", views.recipe_list),
    path("api/recipes/<int:pk>/", views.recipe_detail),
]