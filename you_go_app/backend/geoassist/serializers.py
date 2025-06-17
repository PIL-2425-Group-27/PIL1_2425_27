from rest_framework import serializers
from .models import MeetingPoint


class MeetingPointSerializer(serializers.ModelSerializer):
    driver = serializers.CharField(source="offer.driver.username", read_only=True)
    passenger = serializers.CharField(source="request.passenger.username", read_only=True)
    confirmed_by = serializers.CharField(source="confirmed_by.username", read_only=True)

    class Meta:
        model = MeetingPoint
        fields = [
            'id',
            'offer',
            'request',
            'latitude',
            'longitude',
            'address_label',
            'is_confirmed',
            'confirmed_by',
            'created_at',
            'updated_at',
            'driver',
            'passenger'
        ]
        read_only_fields = ['created_at', 'updated_at', 'confirmed_by']
