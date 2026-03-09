from .models import Notification

class NotificationService:

    @staticmethod
    def create_notification(user, message):
        return Notification.objects.create(
            user=user,
            message=message
        )

    @staticmethod
    def mark_as_read(notification):
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return notification