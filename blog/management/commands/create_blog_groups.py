from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Создаёт группу "Контент-менеджер" для блога'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Контент-менеджер')
        content_type = ContentType.objects.get_for_model(BlogPost)
        perms = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_blogpost', 'change_blogpost', 'delete_blogpost']
        )
        group.permissions.set(perms)
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" уже существовала, права обновлены'))
