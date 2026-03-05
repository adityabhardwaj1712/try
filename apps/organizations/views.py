from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Organization, Membership
from .serializers import OrganizationSerializer, MembershipSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(
            membership__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        org = serializer.save(owner=self.request.user)

        Membership.objects.create(
            user=self.request.user,
            organization=org,
            role="ADMIN"
        )


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Membership.objects.filter(
            organization=self.request.organization
        )