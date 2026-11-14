from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from apps.recipes import views
from apps.recipes.forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/<int:pk>/", views.recipe_page),

    # Авторизация
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="recipes/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
            next_page="home",  # кіргеннен кейін басты бетке (settings-те LOGIN_REDIRECT_URL керек емес)
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register, name="register"),

    path("admin/", admin.site.urls),
    path("api/recipes/", views.recipe_list),
    path("api/recipes/<int:pk>/", views.recipe_detail),
    path("api/drf/", include("apps.recipes.api_urls")),
]
