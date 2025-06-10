# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# Serializer pour l'inscription
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'role',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Serializer pour la réinitialisation du mot de passe
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Serializer pour lecture du profil
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'role',
            'is_kyc_validated',
            'consent_tracking_default',
            'photo_profile',
            'point_depart_habituel',
            'horaire_depart_habituel',
            'horaire_arrivee_habituel',
            'marque_vehicule',
            'modele_vehicule',
            'nombre_places_disponibles',
        ]

# Serializer pour modification du profil
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'photo_profile',
            'role',
            'consent_tracking_default',
            'point_depart_habituel',
            'horaire_depart_habituel',
            'horaire_arrivee_habituel',
            'marque_vehicule',
            'modele_vehicule',
            'nombre_places_disponibles',

        ]
