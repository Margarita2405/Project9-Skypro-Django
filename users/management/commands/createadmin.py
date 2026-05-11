import os
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if not admin_password:
            self.stdout.write(self.style.ERROR('ADMIN_PASSWORD not set in environment'))
            return

        user, created = User.objects.get_or_create(email=admin_email)
        if created:
            user.set_password(admin_password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user {admin_email} created'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user {admin_email} already exists'))
