# notifications/serializers.py

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'notif_type',
            'title',
            'message',
            'data',
            'is_read',
            'is_critical',
            'created_at',
            'read_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'read_at',
            'notif_type',
            'title',
            'message',
            'data',
            'is_critical',
        ]

class MarkNotificationReadSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField()

    def validate_notification_id(self, value):
        try:
            Notification.objects.get(id=value)
        except Notification.DoesNotExist:
            raise serializers.ValidationError("Notification introuvable.")
        return value
