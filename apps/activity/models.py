from django.db import models
from django.conf import settings


class ActivityLog(models.Model):
    
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    action = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization"]),
        ]

    def __str__(self):
        return self.action