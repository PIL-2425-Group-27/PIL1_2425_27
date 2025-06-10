from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Champs supplémentaires requis par le cahier des charges
    
    # Unicité email + phone_number
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    
    # Rôle conducteur/passager
    role = models.CharField(
        max_length=10,
        choices=[('PASSENGER', 'Passenger'), ('DRIVER', 'Driver')],
        default='PASSENGER'
    )
    
    # Vérification identité (KYC)
    is_kyc_validated = models.BooleanField(default=False)
    
    # Consentement tracking par défaut
    consent_tracking_default = models.BooleanField(default=True)
    
    # Photo de profil (facultative)
    photo_profile = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Point de départ habituel
    point_depart_habituel = models.CharField(max_length=255, null=True, blank=True)
    
    # Horaires habituels
    horaire_depart_habituel = models.TimeField(null=True, blank=True)
    horaire_arrivee_habituel = models.TimeField(null=True, blank=True)
    
    # Dernière modification du pseudo (username)
    last_modified_username = models.DateTimeField(null=True, blank=True)

  # Ajout pour infos véhicule (si conducteur)
marque_vehicule = models.CharField(max_length=100, null=True, blank=True)
modele_vehicule = models.CharField(max_length=100, null=True, blank=True)
nombre_places_disponibles = models.PositiveIntegerField(null=True, blank=True)

    # Champs requis pour AbstractUser
REQUIRED_FIELDS = ['email', 'phone_number', 'first_name', 'last_name']

def __str__(self):
    return self.username
