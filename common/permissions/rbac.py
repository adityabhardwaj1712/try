from rest_framework.permissions import BasePermission


class IsOrganizationMember(BasePermission):
    def has_permission(self, request, view):
        return request.organization is not None


class IsOrganizationAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.membership is not None
            and request.membership.role == "ADMIN"
        )


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.membership is not None
            and request.membership.role in ["ADMIN", "MANAGER"]
        )