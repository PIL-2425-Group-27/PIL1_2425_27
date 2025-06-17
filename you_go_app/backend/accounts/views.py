from django.shortcuts import render

# accounts/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from offers.models import RideOffer, RideRequest
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.core.mail import send_mail
from django.utils.timezone import now, timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from .models import UserProfile, Vehicle, KYC, TrackingGPS, GPSHistory
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import (
    RegisterSerializer,
    ResetPasswordSerializer,
    ProfileSerializer,
    VehicleSerializer,
    KYCSerializer,
    TrackingGPSSerializer,
    GPSHistorySerializer,
    DeleteAccountSerializer,
    roleSerializer
)

User = get_user_model()

# View pour l'inscription
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile_data = ProfileSerializer(user.profile).data
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"id": user.id, "email": user.email, "phone_number": user.phone_number, "role": user.role, "profile": profile_data}
        }, status=status.HTTP_201_CREATED)
    
    queryset = User.objects.all()

class roleView(generics.CreateAPIView):
    serializer_class = roleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = roleSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Rôle mis à jour avec succès."})
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        user = request.user
        role = request.data.get("role")
        if role not in ['PASSAGER', 'CONDUCTEUR']:
            return Response({"error": "Rôle invalide."}, status=400)
        user.role = role
        user.save()
        return Response({"message": "Rôle mis à jour avec succès.", "role": user.role}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")  # Peut être email ou téléphone
        password = request.data.get("password")
        profile_data = ProfileSerializer(user.profile).data
        if not identifier or not password:
            return Response({"error": "Email ou numéro de téléphone et mot de passe requis."}, status=400)
        user = User.objects.filter(email=identifier).first() or User.objects.filter(phone_number=identifier).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"id": user.id, "email": user.email, "phone_number": user.phone_number, "role": user.role, "profile": profile_data}
            })
        
        return Response({"error": "Identifiants invalides."}, status=400)
   


# View pour la réinitialisation du mot de passe 
class RequestPasswordResetView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            user.generate_reset_code()  # Génère un code de réinitialisation
            user.save()
            send_transactional_email(
                subject="🔐 Réinitialisation de votre mot de passe",
                to_email=user.email,
                template_name="emails/reset_password.html",
                context={
                    "user": user,
                    "code": user.reset_code,
                    "now": now()
                    }
        )    

            return Response({"detail": "Un email de réinitialisation a été envoyé ."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Aucun utilisateur trouvé avec cet email."}, status=status.HTTP_404_NOT_FOUND)
from mailing.utils import send_transactional_email
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")

        user = User.objects.filter(email=request.data.get("email")).first() 
        
        if not user or not user.is_reset_code_valid(code):
            return Response({"error": "Code invalide ou expiré."}, status=400)
        
        user.set_password(new_password)
        user.reset_code = None  # Supprimer le code après réinitialisation
        user.save()
        
        return Response({"message": "Mot de passe mis à jour avec succès."})

# View pour la déconnexion
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Nécessite d'avoir activé la blacklist dans SimpleJWT

            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response( {"error": "Token invalide ou déjà expiré."},status=status.HTTP_400_BAD_REQUEST)

# View pour le profil utilisateur (GET + PUT/PATCH)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  # Récupère uniquement le profil de l’utilisateur connecté

    def perform_update(self, serializer):
        profile = self.get_object()

        # Vérification du nom (modification tous les 30 jours)
        if "first_name" in serializer.validated_data or "last_name" in serializer.validated_data:
            if profile.last_modified_name and (now() - profile.last_modified_name).days < 30:
                raise ValidationError("Vous ne pouvez modifier votre nom qu'une fois tous les 30 jours.")
            serializer.validated_data["last_modified_name"] = now()

        serializer.save()
 
class VehicleView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_object(self):
        user = self.request.user
        vehicle = vehicle.objects.filter(owner=user).first()
        if not vehicle:
            raise NotFound("Aucun véhicule enregistré.")
        return vehicle
    def get(self, request, *args, **kwargs):
        vehicle = self.get_object()
        serializer = self.get_serializer(vehicle)
        return Response(serializer.data)


#view api

class KYCView(generics.RetrieveUpdateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Vérifie si l'utilisateur a une demande KYC existante avant de la récupérer """
        try:
            return self.request.user.kyc  # Accès direct via related_name
        except KYC.DoesNotExist:
            raise NotFound("Aucune demande KYC trouvée. Veuillez en soumettre une.")
        kyc, _ = KYC.objects.get_or_create(user=self.request.user)
        send_transactional_email(
            subject="📥 KYC en cours de traitement",
            to_email=request.user.email,
            template_name="emails/kyc_submitted.html",
            context={"user": request.user}
            )
        return kyc
    
class KYCAdminView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            kyc = KYC.objects.get(user__id=user_id)
            action = request.data.get("action")
            reason = request.data.get("reason", "")

            if kyc.status == "APPROVED":
                return Response({"error": "Cette demande KYC est déjà validée."}, status=400)

            if action == "approve":
                kyc.approve()
                send_transactional_email(
                    subject="✅ Votre KYC a été validé",
                    to_email=kyc.user.email,
                    template_name="emails/kyc_validated.html",
                    context={"user": kyc.user}
                )
                return Response({"message": "KYC validé."}, status=HTTP_200_OK)
            elif action == "reject":
                kyc.reject(reason)
                send_transactional_email(
                    subject="❌ Votre KYC a été rejeté",
                    to_email=kyc.user.email,
                    template_name="emails/kyc_rejected.html",
                    context={"user": kyc.user, "reason": reason}
                )
                return Response({"message": "KYC rejeté."}, status=HTTP_200_OK)

            return Response({"error": "Action invalide."}, status=HTTP_400_BAD_REQUEST)
        except KYC.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé."}, status=HTTP_400_BAD_REQUEST)
        
class TrackingGPSView(generics.RetrieveUpdateAPIView):
    serializer_class = TrackingGPSSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Récupère l'objet TrackingGPS pour l'utilisateur connecté, ou en crée un s'il n'existe pas """
        # Vérifie si l'utilisateur a déjà un objet TrackingGPS
        tracking, _ = TrackingGPS.objects.get_or_create(user=self.request.user)
        return tracking

    def perform_update(self, serializer):
        tracking = self.get_object()

        # Sauvegarde de la position GPS dans l'historique
        if serializer.validated_data.get("last_latitude") and serializer.validated_data.get("last_longitude"):
            GPSHistory.objects.create(
                user=self.request.user,
                latitude=serializer.validated_data["last_latitude"],
                longitude=serializer.validated_data["last_longitude"]
            )
        
        serializer.save()
class GPSHistoryView(generics.ListAPIView):
    serializer_class = GPSHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GPSHistory.objects.filter(user=self.request.user).order_by("-timestamp")
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_tracking_consent(request):
    """
    Permet à un utilisateur d’activer ou désactiver le partage de sa position.
    """
    user = request.user
    consent = request.data.get("consent_tracking")

    if consent is None:
        return Response({"error": "Champ 'consent_tracking' requis."}, status=400)

    tracking, _ = TrackingGPS.objects.get_or_create(user=user)
    tracking.consent_tracking = bool(consent)
    tracking.save()

    return Response({
        "message": "Consentement mis à jour.",
        "consent_tracking": tracking.consent_tracking
    }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tracking_position(request, user_id):
    """
    Retourne la position d’un utilisateur si le tracking est activé
    et si l’utilisateur courant a une relation de covoiturage avec lui.
    """
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

    if target_user == request.user:
        return Response({"error": "Vous ne pouvez pas suivre votre propre position."}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier s’il existe une relation de covoiturage entre les deux (match actif)
    offer_match = RideOffer.objects.filter(
        driver__in=[request.user, target_user],
        demandes_associees__passenger__in=[request.user, target_user],
        demandes_associees__status='ACCEPTEE',
        date_trajet__gte=timezone.now().date()
    ).first()

    if not offer_match:
        return Response({"error": "Aucun trajet accepté en commun avec cet utilisateur."}, status=status.HTTP_403_FORBIDDEN)

    # Vérifie le consentement du suivi
    tracking = getattr(target_user, "tracking", None)
    if not tracking or not tracking.consent_tracking:
        return Response({"error": "Ce conducteur/passager n’a pas autorisé le suivi GPS."}, status=status.HTTP_403_FORBIDDEN)

    return Response({
        "user_id": target_user.id,
        "name": f"{target_user.first_name} {target_user.last_name}",
        "latitude": tracking.last_latitude,
        "longitude": tracking.last_longitude,
        "last_update": tracking.last_update,
    }, status=200)

class SecureDeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        email = request.user.email
        request.user.delete()

        return Response(
            {"detail": f"Le compte lié à {email} a été supprimé avec succès."},
            status=status.HTTP_204_NO_CONTENT
        )

class ThemePreferenceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        theme = request.data.get('theme_preference')
        if theme not in ['light', 'dark']:
            return Response({'error': 'Thème invalide'}, status=400)
        
        user = request.user
        user.theme_preference = theme
        user.save()
        return Response({'message': 'Thème mis à jour avec succès.', 'theme': theme})
