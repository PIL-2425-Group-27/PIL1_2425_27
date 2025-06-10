# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ResetPasswordView, LogoutView, ProfileView

urlpatterns = [
    # Endpoint pour l'inscription
    path('register/', RegisterView.as_view(), name='register'),

    # Endpoint pour la connexion (JWT)
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # Rafraîchissement du token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Réinitialisation du mot de passe
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    # Déconnexion (invalider le token / gérer la session)
    path('logout/', LogoutView.as_view(), name='logout'),

    # Gestion du profil utilisateur
    path('profile/', ProfileView.as_view(), name='profile'),
    # Endpoint pour mettre à jour le profil (PUT/PATCH)
    path('profile/update/', ProfileView.as_view(), name='update_profile'),
   
]
