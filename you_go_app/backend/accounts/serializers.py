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
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
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
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise ValidationError(_("Aucun utilisateur trouvé avec cet email."))
        return value

from django.contrib.auth import get_user_model
User = get_user_model()
# Serializer pour la modification du mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Les nouveaux mots de passe ne correspondent pas."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("L'ancien mot de passe est incorrect."))
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


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
            'default_start_point',
            'default_end_point',
            'default_start_time',
            'default_end_time',
            'brand',
            'model',
            'seats_available',
            'license_plate',
            'created_at',

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
            'default_start_point',
            'default_end_point',
            'default_start_time',
            'default_end_time',
            'brand',
            'model',
            'seats_available',
            'license_plate',

        ]
