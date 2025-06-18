# accounts/views.py - Improved version
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.cache import cache
import logging

from offers.models import RideOffer, RideRequest
from .models import UserProfile, Vehicle, KYC, TrackingGPS, GPSHistory
from .serializers import (
    RegisterSerializer, ResetPasswordSerializer, ProfileSerializer,
    VehicleSerializer, KYCSerializer, TrackingGPSSerializer,
    GPSHistorySerializer, DeleteAccountSerializer, RoleSerializer, LoginSerializer, ChangePasswordSerializer
)
from mailing.utils import send_transactional_email

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create profile if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile_data = ProfileSerializer(profile).data

        refresh = RefreshToken.for_user(user)
        
        logger.info(f"New user registered: {user.email}")
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id, 
                "email": user.email, 
                "phone_number": user.phone_number, 
                "role": user.role, 
                "profile": profile_data
            }
        }, status=status.HTTP_201_CREATED)


class RoleView(generics.GenericAPIView):
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        role = request.data.get("role")
        if role not in ['PASSAGER', 'CONDUCTEUR']:
            return Response({"error": "Rôle invalide."}, status=400)
        
        request.user.role = role
        request.user.save(update_fields=['role'])
        
        logger.info(f"User {request.user.email} updated role to {role}")
        
        return Response({
            "message": "Rôle mis à jour avec succès.", 
            "role": request.user.role
        }, status=200)

    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Rôle mis à jour avec succès."}, status=200)
        return Response(serializer.errors, status=400)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Connexion réussie',
            'user': ProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
class RequestPasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email requis."}, status=400)
        
        # Rate limiting - 3 attempts per hour per email
        cache_key = f"password_reset_{email}"
        attempts = cache.get(cache_key, 0)
        if attempts >= 3:
            return Response({
                "error": "Trop de tentatives. Réessayez dans une heure."
            }, status=429)
        
        try:
            user = User.objects.get(email=email)
            user.generate_reset_code()
            user.save(update_fields=['reset_code', 'reset_code_expires'])
            
            send_transactional_email(
                subject="🔐 Réinitialisation de votre mot de passe",
                to_email=user.email,
                template_name="emails/reset_password.html",
                context={"user": user, "code": user.reset_code, "now": now()}
            )
            
            # Increment rate limit counter
            cache.set(cache_key, attempts + 1, 3600)  # 1 hour
            
            logger.info(f"Password reset requested for {email}")
            
            return Response({
                "detail": "Un email de réinitialisation a été envoyé."
            }, status=200)
            
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return Response({
                "detail": "Si cet email existe, un code de réinitialisation a été envoyé."
            }, status=200)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")

        if not all([email, code, new_password]):
            return Response({
                "error": "Email, code et nouveau mot de passe requis."
            }, status=400)

        try:
            user = User.objects.get(email=email)
            if not user.is_reset_code_valid(code):
                return Response({
                    "error": "Code invalide ou expiré."
                }, status=400)
            
            user.set_password(new_password)
            user.reset_code = None
            user.reset_code_expires = None
            user.save(update_fields=['password', 'reset_code', 'reset_code_expires'])
            
            logger.info(f"Password reset successful for {email}")
            
            return Response({
                "message": "Mot de passe mis à jour avec succès."
            }, status=200)
            
        except User.DoesNotExist:
            return Response({
                "error": "Code invalide ou expiré."
            }, status=400)
        
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        logger.info(f"Password changed successfully for user: {request.user.email}")
        
        return Response({
            "message": "Mot de passe changé avec succès."
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({
                    "error": "Token de rafraîchissement requis."
                }, status=400)
                
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "Déconnexion réussie."
            }, status=205)
            
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response({
                "error": "Token invalide ou déjà expiré."
            }, status=400)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer):
        profile = self.get_object()

        # Check name modification limit (once every 30 days)
        if any(field in serializer.validated_data for field in ["first_name", "last_name"]):
            if (profile.last_modified_name and 
                (now() - profile.last_modified_name).days < 30):
                raise ValidationError(
                    "Vous ne pouvez modifier votre nom qu'une fois tous les 30 jours."
                )
            serializer.validated_data["last_modified_name"] = now()

        serializer.save()

class VehicleView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return Vehicle.objects.get(owner=self.request.user)
        except Vehicle.DoesNotExist:
            raise NotFound("Aucun véhicule enregistré.")

    def perform_create(self, serializer):
        # Ensure user doesn't already have a vehicle
        if Vehicle.objects.filter(owner=self.request.user).exists():
            raise ValidationError("Vous avez déjà un véhicule enregistré.")
        serializer.save(owner=self.request.user)

class KYCView(generics.RetrieveUpdateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        kyc, created = KYC.objects.get_or_create(user=self.request.user)
        if created:
            send_transactional_email(
                subject="📥 KYC en cours de traitement",
                to_email=self.request.user.email,
                template_name="emails/kyc_submitted.html",
                context={"user": self.request.user}
            )
        return kyc

class KYCAdminView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            kyc = KYC.objects.get(user__id=user_id)
        except KYC.DoesNotExist:
            return Response({
                "error": "Demande KYC non trouvée."
            }, status=404)

        if kyc.status == "APPROVED":
            return Response({
                "error": "Cette demande KYC est déjà validée."
            }, status=400)

        action = request.data.get("action")
        reason = request.data.get("reason", "")

        if action == "approve":
            kyc.approve()
            send_transactional_email(
                subject="✅ Votre KYC a été validé",
                to_email=kyc.user.email,
                template_name="emails/kyc_validated.html",
                context={"user": kyc.user}
            )
            return Response({"message": "KYC validé."}, status=200)
            
        elif action == "reject":
            kyc.reject(reason)
            send_transactional_email(
                subject="❌ Votre KYC a été rejeté",
                to_email=kyc.user.email,
                template_name="emails/kyc_rejected.html",
                context={"user": kyc.user, "reason": reason}
            )
            return Response({"message": "KYC rejeté."}, status=200)

        return Response({"error": "Action invalide."}, status=400)

class TrackingGPSView(generics.RetrieveUpdateAPIView):
    serializer_class = TrackingGPSSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        tracking, _ = TrackingGPS.objects.get_or_create(user=self.request.user)
        return tracking

    @transaction.atomic
    def perform_update(self, serializer):
        tracking = self.get_object()

        # Save GPS history if coordinates are provided
        latitude = serializer.validated_data.get("last_latitude")
        longitude = serializer.validated_data.get("last_longitude")
        
        if latitude and longitude:
            GPSHistory.objects.create(
                user=self.request.user,
                latitude=latitude,
                longitude=longitude
            )
        
        serializer.save()

class GPSHistoryView(generics.ListAPIView):
    serializer_class = GPSHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GPSHistory.objects.filter(
            user=self.request.user
        ).order_by("-timestamp")[:50]  # Limit to 50 recent entries

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_tracking_consent(request):
    """Allow user to enable/disable location sharing."""
    consent = request.data.get("consent_tracking")

    if consent is None:
        return Response({
            "error": "Champ 'consent_tracking' requis."
        }, status=400)

    tracking, _ = TrackingGPS.objects.get_or_create(user=request.user)
    tracking.consent_tracking = bool(consent)
    tracking.save(update_fields=['consent_tracking'])

    return Response({
        "message": "Consentement mis à jour.",
        "consent_tracking": tracking.consent_tracking
    }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tracking_position(request, user_id):
    """Return user position if tracking is enabled and there's an active ride relationship."""
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            "error": "Utilisateur introuvable."
        }, status=404)

    if target_user == request.user:
        return Response({
            "error": "Vous ne pouvez pas suivre votre propre position."
        }, status=400)

    # Check for active ride relationship
    has_active_ride = RideOffer.objects.filter(
        driver__in=[request.user, target_user],
        demandes_associees__passenger__in=[request.user, target_user],
        demandes_associees__status='ACCEPTEE',
        date_trajet__gte=timezone.now().date()
    ).exists()

    if not has_active_ride:
        return Response({
            "error": "Aucun trajet accepté en commun avec cet utilisateur."
        }, status=403)

    # Check tracking consent
    try:
        tracking = target_user.tracking
        if not tracking.consent_tracking:
            return Response({
                "error": "Ce conducteur/passager n'a pas autorisé le suivi GPS."
            }, status=403)
    except TrackingGPS.DoesNotExist:
        return Response({
            "error": "Aucune donnée de géolocalisation disponible."
        }, status=404)

    return Response({
        "user_id": target_user.id,
        "name": f"{target_user.first_name} {target_user.last_name}",
        "latitude": tracking.last_latitude,
        "longitude": tracking.last_longitude,
        "last_update": tracking.last_update,
    }, status=200)

class SecureDeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request):
        serializer = DeleteAccountSerializer(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        email = request.user.email
        user_id = request.user.id
        
        # Log before deletion
        logger.info(f"Account deletion requested for user_id: {user_id}, email: {email}")
        
        request.user.delete()

        return Response({
            "detail": f"Le compte lié à {email} a été supprimé avec succès."
        }, status=204)

class ThemePreferenceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        theme = request.data.get('theme_preference')
        if theme not in ['light', 'dark']:
            return Response({
                'error': 'Thème invalide. Choisissez "light" ou "dark".'
            }, status=400)
        
        request.user.theme_preference = theme
        request.user.save(update_fields=['theme_preference'])
        
        return Response({
            'message': 'Thème mis à jour avec succès.', 
            'theme': theme
        }, status=200)