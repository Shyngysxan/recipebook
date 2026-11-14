from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField("Атауы", max_length=100, unique=True)
    icon = models.CharField("Белгіше (эмодзи)", max_length=8, default="🍽️")

    class Meta:
        verbose_name = "Санат"
        verbose_name_plural = "Санаттар"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField("Атауы", max_length=100, unique=True)

    class Meta:
        verbose_name = "Ұлттық асхана"
        verbose_name_plural = "Ұлттық асханалар"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Жеңіл"),
        ("medium", "Орташа"),
        ("hard", "Қиын"),
    ]

    title = models.CharField("Атауы", max_length=200)
    description = models.TextField("Қысқаша сипаттама", blank=True)
    ingredients = models.TextField(
        "Ингредиенттер", help_text="Әр ингредиентті жаңа жолдан жазыңыз"
    )
    instructions = models.TextField(
        "Дайындау жолы", help_text="Әр қадамды жаңа жолдан жазыңыз"
    )
    cooking_time = models.PositiveIntegerField("Дайындау уақыты (мин)")
    servings = models.PositiveSmallIntegerField("Порция саны", default=2)
    difficulty = models.CharField(
        "Күрделілігі", max_length=10, choices=DIFFICULTY_CHOICES, default="medium"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Санат",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
    )
    cuisine = models.ForeignKey(
        Cuisine,
        verbose_name="Ұлттық асхана",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
    )
    created_at = models.DateTimeField("Қосылған уақыты", auto_now_add=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепттер"

    def __str__(self):
        return self.title


class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author_name = models.CharField("Аты", max_length=100)
    rating = models.PositiveSmallIntegerField(
        "Баға (1-5)", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField("Пікір", blank=True)
    created_at = models.DateTimeField("Уақыты", auto_now_add=True)

    class Meta:
        verbose_name = "Пікір"
        verbose_name_plural = "Пікірлер"

    def __str__(self):
        return f"{self.recipe} — {self.rating}/5 ({self.author_name})"