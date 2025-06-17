# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ResetPasswordView, RequestPasswordResetView, LogoutView, ProfileView, VehicleView, KYCView, KYCAdminView, TrackingGPSView, GPSHistoryView, update_tracking_consent, get_user_tracking_position, SecureDeleteAccountView, ThemePreferenceUpdateView

urlpatterns = [
    # Endpoint pour l'inscription
    path('register/', RegisterView.as_view(), name='register'),

    # Endpoint pour la connexion (JWT)
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # Rafraîchissement du token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Réinitialisation du mot de passe
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    # Déconnexion (invalider le token / gérer la session)
    path('logout/', LogoutView.as_view(), name='logout'),

    # Gestion du profil utilisateur
    path('profile/', ProfileView.as_view(), name='profile'),
    
    path("vehicle/", VehicleView.as_view(), name="vehicle"),  # Pour récupérer les infos du véhicule
   
    path("kyc/", KYCView.as_view(), name="kyc"),  # Consultation/modification utilisateur
    path("kyc/admin/<int:user_id>/", KYCAdminView.as_view(), name="kyc-admin"),  # Validation admin
    # Endpoint pour la validation KYC par l'admin
    
    path("gps/", TrackingGPSView.as_view(), name="gps"),
    path("gps/history/", GPSHistoryView.as_view(), name="gps-history"),
    path("gps/consent/", update_tracking_consent, name="update-tracking-consent"),

    path("gps/user/<int:user_id>/", get_user_tracking_position, name="get-user-tracking"),
    path("delete/", SecureDeleteAccountView.as_view(), name="delete-account"),

    # Endpoint pour mettre à jour les préférences de thème
    path("theme/", ThemePreferenceUpdateView.as_view(), name="theme-preference"),
]

