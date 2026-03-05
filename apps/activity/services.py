from .models import ActivityLog


class ActivityService:

    @staticmethod
    def log(organization, user, action):
        return ActivityLog.objects.create(
            organization=organization,
            user=user,
            action=action
        )