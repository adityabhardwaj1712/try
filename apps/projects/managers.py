from django.db import models


class ProjectQuerySet(models.QuerySet):

    def for_organization(self, organization):
        return self.filter(organization=organization)

    def with_related(self):
        return self.select_related("organization")


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def for_organization(self, organization):
        return self.get_queryset().for_organization(organization)