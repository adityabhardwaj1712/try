from apps.organizations.models import Organization, Membership


class OrganizationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # default values
        request.organization = None
        request.membership = None
        request.role = None

        org_slug = request.headers.get("X-ORG")

        if request.user.is_authenticated and org_slug:

            try:
                org = Organization.objects.get(slug=org_slug)

                membership = Membership.objects.select_related(
                    "organization",
                    "user"
                ).filter(
                    user=request.user,
                    organization=org
                ).first()

                if membership:
                    request.organization = org
                    request.membership = membership
                    request.role = membership.role

            except Organization.DoesNotExist:
                pass

        response = self.get_response(request)

        return response