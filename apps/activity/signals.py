from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.tasks.models import Task
from .models import ActivityLog


@receiver(post_save, sender=Task)
def log_task_activity(sender, instance, created, **kwargs):

    action = "Created" if created else "Updated"

    ActivityLog.objects.create(
        organization=instance.organization,
        user=instance.assignee or instance.organization.owner,
        action=f"{action} task: {instance.title}",
    )