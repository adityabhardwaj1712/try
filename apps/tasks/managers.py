from django.db import models


class TaskQuerySet(models.QuerySet):

    def for_organization(self, organization):
        return self.filter(organization=organization)

    def with_related(self):
        return self.select_related(
            "project",
            "assignee",
            "organization"
        )

    def by_status(self, status):
        return self.filter(status=status)

    def assigned_to(self, user):
        return self.filter(assignee=user)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def for_organization(self, organization):
        return self.get_queryset().for_organization(organization)