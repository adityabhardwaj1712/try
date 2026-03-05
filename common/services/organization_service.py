from apps.organizations.models import Membership


class OrganizationService:

    @staticmethod
    def add_member(user, organization, role="DEVELOPER"):
        return Membership.objects.create(
            user=user,
            organization=organization,
            role=role,
        )