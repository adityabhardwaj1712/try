from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from common.cache import cache_kanban, get_cached_kanban


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(
            organization=self.request.organization
        ).select_related("project", "assignee")

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization)

    @action(detail=False, methods=["get"])
    def kanban(self, request):
        org = request.organization

        if not org:
            return Response({"error": "Organization header missing"}, status=400)

        cached = get_cached_kanban(org.id)
        if cached:
            return Response(cached)

        tasks = Task.objects.filter(organization=org)

        data = {
            "TODO": TaskSerializer(tasks.filter(status="TODO"), many=True).data,
            "IN_PROGRESS": TaskSerializer(tasks.filter(status="IN_PROGRESS"), many=True).data,
            "DONE": TaskSerializer(tasks.filter(status="DONE"), many=True).data,
        }

        cache_kanban(org.id, data)

        return Response(data)