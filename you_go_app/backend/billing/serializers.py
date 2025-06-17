from rest_framework import serializers
from billing.models import RideInvoice


class RideInvoiceSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    passenger_name = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    trajet = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = RideInvoice
        fields = [
            'id',
            'ride_request',
            'ride_offer',
            'passenger_name',
            'driver_name',
            'vehicle',
            'trajet',
            'date_trajet',
            'start_time',
            'end_time',
            'price_type',
            'price_applied',
            'eta_minutes',
            'generated_at',
            'pdf_url',
        ]
        read_only_fields = fields

    def get_driver_name(self, obj):
        return obj.driver.get_full_name() if obj.driver else None

    def get_passenger_name(self, obj):
        return obj.passenger.get_full_name() if obj.passenger else None

    def get_vehicle(self, obj):
        return {
            "brand": obj.vehicle_brand,
            "model": obj.vehicle_model,
            "plate": obj.vehicle_plate
        }

    def get_trajet(self, obj):
        return {
            "start_point": obj.start_point,
            "end_point": obj.end_point,
            "latitude_depart": obj.start_latitude,
            "longitude_depart": obj.start_longitude,
            "latitude_arrivee": obj.end_latitude,
            "longitude_arrivee": obj.end_longitude
        }

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf and hasattr(obj.pdf, 'url'):
            return request.build_absolute_uri(obj.pdf.url) if request else obj.pdf.url
        return None
