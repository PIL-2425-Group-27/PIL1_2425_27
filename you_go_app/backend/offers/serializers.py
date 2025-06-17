from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import RideOffer, RideRequest


class RideOfferSerializer(serializers.ModelSerializer):
    # Lecture des informations de véhicule unifié
    vehicle_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RideOffer
        fields = [
            'id',
            'driver',
            'start_point',
            'end_point',
            'start_latitude',
            'start_longitude',
            'end_latitude',
            'end_longitude',
            'date_trajet',
            'start_time',
            'end_time',
            'seats_available',
            'price_type',
            'price',
            'description',
            'status',
            'created_at',
            'vehicle',
            'use_custom_vehicle_info',
            'custom_vehicle_brand',
            'custom_vehicle_model',
            'custom_vehicle_plate',
            'custom_vehicle_seats',
            'vehicle_info',
        ]
        read_only_fields = ['id', 'created_at', 'status', 'price', 'vehicle_info', 'driver','start_latitude','start_longitude',
            'end_latitude',
            'end_longitude',]

    def get_vehicle_info(self, obj):
        """Retourne les infos du véhicule actif (custom ou lié)"""
        return obj.get_vehicle_info()

    def validate(self, data):
        price_type = data.get("price_type", getattr(self.instance, "price_type", None))
        price = data.get("price", getattr(self.instance, "price", None))
        if price_type == "FIXE" and not price:
            raise serializers.ValidationError("Le prix est requis pour le mode FIXE.")
        if price_type == "DYNAMIQUE":
            start_latitude = data.get("start_latitude", getattr(self.instance, "start_latitude", None))
            start_longitude = data.get("start_longitude", getattr(self.instance, "start_longitude", None))
            end_latitude = data.get("end_latitude", getattr(self.instance, "end_latitude", None))
            end_longitude = data.get("end_longitude", getattr(self.instance, "end_longitude", None))
            if not all([start_latitude, start_longitude, end_latitude, end_longitude]):
                raise serializers.ValidationError("Coordonnées GPS requises pour l'estimation automatique.")
        return data

    def create(self, validated_data):
        instance = RideOffer(**validated_data)
        try:
            instance.full_clean()
            instance.save()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            instance.full_clean()
            instance.save()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return instance

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = [
            'id',
            'passenger',
            'start_point',
            'end_point',
            'date_trajet',
            'start_time',
            'end_time',
            'status',
            'offre_associee',
            'created_at',
            'price_preference',
            'max_price'
        ]
        read_only_fields = ['id', 'created_at', 'status']

    def validate(self, data):
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("L'heure de départ doit précéder l'heure d'arrivée.")

        price_preference = data.get('price_preference', getattr(self.instance, 'price_preference', None))
        max_price = data.get('max_price', getattr(self.instance, 'max_price', None))
        if price_preference == 'FIXE' and not max_price:
            raise serializers.ValidationError("Le prix maximum est requis si vous choisissez 'Fixé'.")

        return data
    def create(self, validated_data):
        instance = RideRequest(**validated_data)
        try:
            instance.full_clean()
            instance.save()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            instance.full_clean()
            instance.save()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return instance
