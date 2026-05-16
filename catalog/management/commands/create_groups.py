from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает нужные права'

    def handle(self, *args, **options):
        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        content_type = ContentType.objects.get_for_model(Product)

        # Получаем нужные права: кастомное can_unpublish_product и стандартное delete_product
        perms = Permission.objects.filter(
            content_type=content_type, codename__in=["can_unpublish_product", "delete_product"]
        )

        # Назначаем права группе
        group.permissions.set(perms)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана и права назначены'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" уже существовала, права обновлены'))
