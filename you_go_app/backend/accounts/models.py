from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now 
import random
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save

BADGE_CHOICES = [
    ('BRONZE', 'Bronze'),
    ('ARGENT', 'Argent'),
    ('OR', 'Or'),
]
THEME_CHOICES = [
    ('light', 'Clair'),
    ('dark', 'Sombre'),
]
role = models.CharField(
    max_length=15,
    choices=[
        ('NON_ATTRIBUE', 'Non attribué'),
        ('PASSAGER', 'Passager'),
        ('CONDUCTEUR', 'Conducteur')
    ],
    default='NON_ATTRIBUE'
)


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True)
  
    username = models.CharField(max_length=150, unique=True, db_index=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    role = models.CharField(
        max_length=10,
        choices=[('PASSAGER', 'Passager'), ('CONDUCTEUR', 'Conducteur')],
        default='PASSAGER'
    )

    is_active = models.BooleanField(default=True)
    is_kyc_validated = models.BooleanField(default=False)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    reset_code_expiration = models.DateTimeField(null=True, blank=True)
    last_modified_username = models.DateTimeField(null=True, blank=True)

    def generate_reset_code(self):
        self.reset_code = str(random.randint(1000, 9999))
        self.reset_code_expiration = now() + timedelta(minutes=10)
        self.save()

    def __str__(self):
        return f"{self.email} ({self.role})"
    
    def is_reset_code_valid(self, code):
        return (
            self.reset_code == code and 
            self.reset_code_expiration and 
            now() <= self.reset_code_expiration
    )

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='light'
)
    reliability_score = models.PositiveIntegerField(default=0)
    reliability_badge = models.CharField(max_length=10, choices=BADGE_CHOICES, default='BRONZE')
    def update_reliability(self):
        score = 0

        if self.is_kyc_validated:
            score += 30
        if self.average_rating and self.average_rating >= 4.5:
            score += 20
        # Nombre de trajets réalisés
        from offers.models import RideOffer
        trajets_realises = RideOffer.objects.filter(driver=self, status='ACTIF').count()
        score += trajets_realises * 5

         # Note moyenne (si module d'avis)
        from reviews.models import Review
        moyenne = Review.objects.filter(reviewed_user=self).aggregate(models.Avg('rating'))['rating__avg'] or 0
        if moyenne >= 4:
            score += 20

        # Profil complet
        if self.photo_profile and self.vehicle_set.exists():
            score += 15

        # Ancienneté
        if (timezone.now() - self.date_joined).days >= 30:
            score += 10

        # Mise à jour
        self.reliability_score = score
        if score >= 90:
            self.reliability_badge = 'OR'
        elif score >= 50:
            self.reliability_badge = 'ARGENT'
        else:
            self.reliability_badge = 'BRONZE'

        self.save()
    # Données personnelles étendues
    first_name = models.CharField(max_length=30, blank=True, null=False)
    last_name = models.CharField(max_length=30, blank=True, null=False)
    photo_profile = models.ImageField(upload_to="profiles/", null=True, blank=True, help_text="Photo de profil de l'utilisateur")

    # Localisation & horaires
    default_start_point = models.CharField(max_length=255, null=True, blank=True)
    default_end_point = models.CharField(max_length=255, null=True, blank=True)
    default_start_time = models.TimeField(null=True, blank=True)
    default_end_time = models.TimeField(null=True, blank=True)

    

    # Consentement & KYC
    consent_tracking = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Historique modification du pseudo
    last_modified_name = models.DateTimeField(null=True, blank=True)

    def can_modify_name(self):
        """ Vérifie si l’utilisateur peut modifier son nom """
        if self.last_modified_name:
            return (now() - self.last_modified_name).days >= 30
        return True

    def save(self, *args, **kwargs):
        """ Logique : si prénom ou nom change → update date """
        if self.pk:
            original = UserProfile.objects.get(pk=self.pk)
            if original.first_name != self.first_name or original.last_name != self.last_name:
                self.last_modified_name = now()
        

    def __str__(self):
        return f"Profil de {self.email}"
class Vehicle(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Vehicle")
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=50, unique=True)
    seats_available = models.IntegerField()

    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate} ({self.seats_available} places)"

class KYC(models.Model):
    STATUS_CHOICES = [("PENDING", "En attente"), ("APPROVED", "Validé"), ("REJECTED", "Rejeté")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="kyc")
    document_file = models.FileField(upload_to="kyc_documents/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    rejection_reason = models.TextField(null=True, blank=True)  # Pour les refus
    is_kyc_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)

    def approve(self):
        self.status = "APPROVED"
        self.validated_at = now()
        self.is_kyc_validated = True
        self.user.is_kyc_validated = True  # Mettre à jour le champ is_kyc_validated de l'utilisateur
        self.user.save()  # Sauvegarder l'utilisateur pour que le changement prenne effet
        self.rejection_reason = None # Réinitialiser la raison de rejet si approuvé
        self.save()

    def reject(self, reason):
        self.status = "REJECTED"
        self.is_kyc_validated = False
        self.user.is_kyc_validated = False  # Mettre à jour le champ is_kyc_validated de l'utilisateur
        self.user.save()  # Sauvegarder l'utilisateur pour que le changement prenne effet
        self.rejection_reason = reason
        self.validated_at = None
        self.save()

    def __str__(self):
        return f"KYC - {self.user.email} : {self.status} : {'Validé' if self.is_kyc_validated else 'Non validé'}"

class TrackingGPS(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tracking")
    consent_tracking = models.BooleanField(default=True)

    # Localisation en temps réel
    last_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    last_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking GPS - {self.user.email} : {'Activé' if self.consent_tracking else 'Désactivé'}"

class GPSHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gps_history")
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Position enregistrée ({self.latitude}, {self.longitude}) - {self.timestamp}"

@property
def average_rating(self):
    from reviews.models import Review
    notes = Review.objects.filter(reviewed_user=self).aggregate(models.Avg('rating'))
    return round(notes['rating__avg'], 2) if notes['rating__avg'] else None
