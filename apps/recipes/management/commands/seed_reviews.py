"""
python manage.py seed_reviews            – бар рецепттерге демо-пікірлер қосады (рецепттерге тиіспейді)
python manage.py seed_reviews --clear    – тек осы команда қосқан демо-пікірлерді өшіреді
Қайта жүргізсе, қайталанбайды (get_or_create).
"""
from django.core.management.base import BaseCommand

from apps.recipes.models import Recipe, Review

DEMO = [
    ("Демо Айгерім", 5, "Өте дәмді, отбасыммен жедім."),
    ("Демо Бекзат", 4, "Оңай әрі жылдам дайындалады."),
]


class Command(BaseCommand):
    help = "Рецепттерге демо-пікірлер қосады"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="демо-пікірлерді өшіру")

    def handle(self, *args, **options):
        names = [n for n, _, _ in DEMO]
        if options["clear"]:
            deleted, _ = Review.objects.filter(author_name__in=names).delete()
            self.stdout.write(self.style.WARNING(f"Өшірілді: {deleted}"))
            return
        created = 0
        for recipe in Recipe.objects.all():
            for name, rating, comment in DEMO:
                _, is_new = Review.objects.get_or_create(
                    recipe=recipe, author_name=name,
                    defaults={"rating": rating, "comment": comment})
                created += is_new
        self.stdout.write(self.style.SUCCESS(
            f"Жаңа пікір: {created}. Барлығы: рецепт {Recipe.objects.count()}, пікір {Review.objects.count()}"))
