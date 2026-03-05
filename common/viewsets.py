from rest_framework import viewsets


class OrganizationScopedModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return self.queryset.filter(
            organization=self.request.organization
        )

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization)