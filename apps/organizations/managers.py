from django.db import models


class MembershipQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class MembershipManager(models.Manager):
    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db)
    