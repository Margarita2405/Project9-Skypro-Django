from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстур"

    def handle(self, *args, **kwargs):
        # Очистка БД
        self.stdout.write(self.style.WARNING("Очистка базы данных..."))
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("База данных очищена"))

        # Загрузка фикстур
        self.stdout.write(self.style.WARNING("Загрузка фикстур..."))
        call_command("loaddata", "catalog/fixtures/categories.json")
        call_command("loaddata", "catalog/fixtures/products.json")
        self.stdout.write(self.style.SUCCESS("Фикстуры загружены"))
