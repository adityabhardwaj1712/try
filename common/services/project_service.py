from apps.projects.models import Project


class ProjectService:

    @staticmethod
    def create_project(name, organization, description=""):
        return Project.objects.create(
            name=name,
            organization=organization,
            description=description,
        )