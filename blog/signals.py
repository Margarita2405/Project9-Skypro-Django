from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from blog.models import BlogPost

@receiver(pre_save, sender=BlogPost)
def check_views(sender, instance, **kwargs):
    if instance.pk:
        old = sender.objects.get(pk=instance.pk).views_count
        if old < 100 <= instance.views_count:
            send_mail(
                subject='Статья набрала 100 просмотров!',
                message=f'Статья "{instance.title}" набрала 100 просмотров. Ура!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_BACKEND],
                fail_silently=True,
            )
