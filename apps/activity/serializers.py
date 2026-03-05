from rest_framework import serializers
from .models import ActivityLog


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityLog
        fields = "__all__"
        read_only_fields = ("organization", "user")