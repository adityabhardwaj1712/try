from celery import shared_task
from django.utils import timezone
from .models import Notification


@shared_task
def daily_cleanup():
    Notification.objects.filter(
        is_read=True,
        created_at__lt=timezone.now() - timezone.timedelta(days=30)
    ).delete()