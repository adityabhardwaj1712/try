from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import Notification

@shared_task
def daily_cleanup():
    """
    Remove old read notifications older than 30 days
    """

    Notification.objects.filter(
        is_read=True,
        created_at__lt=timezone.now() - timedelta(days=30)
    ).delete()