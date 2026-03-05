from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task
from common.cache import invalidate_kanban_cache


@receiver(post_save, sender=Task)
def clear_cache_on_save(sender, instance, **kwargs):
    if instance.organization:
        invalidate_kanban_cache(instance.organization.id)


@receiver(post_delete, sender=Task)
def clear_cache_on_delete(sender, instance, **kwargs):
    if instance.organization:
        invalidate_kanban_cache(instance.organization.id)