from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Champs supplémentaires requis par le cahier des charges
    first_name = models.CharField(max_length=30, blank=True, null=False)
    last_name = models.CharField(max_length=30, blank=True, null=False)
    # Champs requis pour l'authentification
    password = models.CharField(max_length=128, blank=False, null=False)
   

    
    # Unicité email + phone_number + username
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True)
    
    # Rôle conducteur/passager
    role = models.CharField(
        max_length=10,
        choices=[('PASSAGER', 'Passager'), ('CONDUCTEUR', 'Conducteur')],
        default='PASSAGER'
    )
    
    # Vérification identité (KYC)
    is_kyc_validated = models.BooleanField(default=False)
    
    # Consentement tracking par défaut
    consent_tracking_default = models.BooleanField(default=True)
    
    # Photo de profil (facultative)
    photo_profile = models.ImageField(upload_to='profile/', null=True, blank=True)
    
    # Point de départ habituel
    default_start_point = models.CharField(max_length=255, null=True, blank=True)

    # Point d'arrivee habituel
    default_end_point = models.CharField(max_length=255, null=True, blank=True)

    # Horaires habituels
    default_start_time = models.TimeField(null=True, blank=True)
    default_end_time = models.TimeField(null=True, blank=True)
    
    # Dernière modification du pseudo (username)
    last_modified_username = models.DateTimeField(null=True, blank=True)

  # Ajout pour infos véhicule (si conducteur)
brand = models.CharField(max_length=100, null=True, blank=True)
model = models.CharField(max_length=100, null=True, blank=True)
seats_available = models.PositiveIntegerField(null=True, blank=True)
created_at = models.DateTimeField(auto_now_add=True)
license_plate = models.CharField(max_length=20, null=True, blank=True)
    
    # Champs requis pour AbstractUser
REQUIRED_FIELDS = ['email', 'phone_number', 'first_name', 'last_name', 'role', 'password','username']

def __str__(self):
    return self.username
