# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.db import models
from .models import UserProfile, Vehicle, KYC, TrackingGPS, GPSHistory
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'role', 'is_kyc_validated']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})
        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "Ce numéro est déjà utilisé."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Ce nom d'utilisateur est déjà pris."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.role = 'NON_ATTRIBUE'  # Force initial role
        user.set_password(password)
        user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']

    def validate_role(self, value):
        if value not in ['PASSAGER', 'CONDUCTEUR']:
            raise serializers.ValidationError("Rôle invalide.")
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Identifiants invalides.')
            if not user.is_active:
                raise serializers.ValidationError('Compte désactivé.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email et mot de passe requis.')

      
class ResetPasswordSerializer(serializers.Serializer):
    contact = serializers.CharField()

    def validate_contact(self, value):
        user = None
        if '@' in value:
            user = User.objects.filter(email=value).first()
        else:
            user = User.objects.filter(phone_number=value).first()
        if not user:
            raise serializers.ValidationError(_("Aucun utilisateur trouvé avec cet email ou téléphone."))
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='user.role', read_only=True)
    is_kyc_validated = serializers.BooleanField(source='user.is_kyc_validated', read_only=True)
    reliability_score = serializers.IntegerField(source='user.reliability_score', read_only=True)
    reliability_badge = serializers.CharField(source='user.reliability_badge', read_only=True)
    last_modified_name = serializers.DateTimeField(source='user.last_modified_username', read_only=True)
    theme_preference = serializers.CharField(source='user.theme_preference', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'photo_profile',
            'default_start_point', 'default_end_point',
            'default_start_time', 'default_end_time',
            'consent_tracking', 'role', 'is_kyc_validated',
            'reliability_score', 'reliability_badge', 'theme_preference',
            'average_rating'
        ]

    def get_average_rating(self, obj):
        return obj.user.average_rating


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    is_kyc_validated = serializers.BooleanField(source='user.is_kyc_validated', read_only=True)
    average_rating = serializers.SerializerMethodField()
    reliability_score = serializers.IntegerField(source='user.reliability_score', read_only=True)
    reliability_badge = serializers.CharField(source='user.reliability_badge', read_only=True)
    last_modified_name = serializers.DateTimeField(source='user.last_modified_username', read_only=True)
    theme_preference = serializers.CharField(source='user.theme_preference', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'photo_profile',
            'default_start_point', 'default_end_point',
            'default_start_time', 'default_end_time',
            'consent_tracking', 'last_modified_name',
            'email', 'phone_number', 'role', 'is_kyc_validated',
            'reliability_score', 'reliability_badge', 'average_rating', 'theme_preference'
        ]

    def validate_first_name(self, value):
        profile = self.instance
        if profile and not profile.can_modify_name():
            raise serializers.ValidationError("Vous ne pouvez modifier votre nom qu'une fois tous les 30 jours.")
        return value

    def validate_last_name(self, value):
        profile = self.instance
        if profile and not profile.can_modify_name():
            raise serializers.ValidationError("Vous ne pouvez modifier votre nom qu'une fois tous les 30 jours.")
        return value

    def get_average_rating(self, obj):
        try:
            return obj.average_rating
        except (AttributeError, TypeError):
            return 0.0



class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'license_plate', 'seats_available']

    def validate_license_plate(self, value):
        # Check if updating existing vehicle
        if self.instance:
            if Vehicle.objects.filter(license_plate=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Cette plaque d'immatriculation est déjà utilisée.")
        else:
            if Vehicle.objects.filter(license_plate=value).exists():
                raise serializers.ValidationError("Cette plaque d'immatriculation est déjà utilisée.")
        return value

    def validate_seats_available(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le nombre de sièges disponibles doit être supérieur à zéro.")
        return value

    def validate(self, data):
        # Check user role
        request = self.context.get('request')
        if request and request.user.role != "CONDUCTEUR":
            raise serializers.ValidationError("Seuls les conducteurs peuvent enregistrer un véhicule.")
        
        # Check required fields
        if not data.get('brand') or not data.get('model'):
            raise serializers.ValidationError("La marque et le modèle du véhicule sont requis.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Vehicle.objects.create(owner=user, **validated_data)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        if not attrs.get('refresh'):
            raise serializers.ValidationError("Le token de rafraîchissement est requis.")
        return attrs


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = [
            "user", "document_file", "status", "created_at", 
            "validated_at", "rejection_reason", "is_kyc_validated"
        ]
        read_only_fields = [
            "user", "status", "created_at", "validated_at", 
            "rejection_reason", "is_kyc_validated"
        ]

    def validate_document_file(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Le fichier ne doit pas dépasser 5 Mo.")
        return value


class TrackingGPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingGPS
        fields = ["consent_tracking", "last_latitude", "last_longitude", "last_update"]
        read_only_fields = ["last_update"]


class GPSHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSHistory
        fields = ["latitude", "longitude", "timestamp"]


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mot de passe incorrect.")
        return value