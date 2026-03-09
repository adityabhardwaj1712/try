from django.db import models
from apps.users.models import User
from apps.projects.models import Project


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ("GENERAL", "General"),
        ("TASK_ASSIGNED", "Task Assigned"),
        ("COMMENT", "Comment"),
        ("STATUS_CHANGE", "Status Change"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
        null=True,
        blank=True
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default="GENERAL"
    )

    url = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["is_read"]),
        ]

    def __str__(self):
        return self.message