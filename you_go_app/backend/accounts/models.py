from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now 
import random
from datetime import timedelta
from django.utils import timezone

BADGE_CHOICES = [
    ('BRONZE', 'Bronze'),
    ('ARGENT', 'Argent'),
    ('OR', 'Or'),
]

THEME_CHOICES = [
    ('light', 'Clair'),
    ('dark', 'Sombre'),
]

ROLE_CHOICES = [
    ('NON_ATTRIBUE', 'Non attribué'),
    ('PASSAGER', 'Passager'), 
    ('CONDUCTEUR', 'Conducteur')
]


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    # Fixed: Single role field definition
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='NON_ATTRIBUE'
    )

    is_active = models.BooleanField(default=True)
    is_kyc_validated = models.BooleanField(default=False)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    reset_code_expiration = models.DateTimeField(null=True, blank=True)
    last_modified_username = models.DateTimeField(null=True, blank=True)
    
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='light'
    )
    reliability_score = models.PositiveIntegerField(default=0)
    reliability_badge = models.CharField(max_length=10, choices=BADGE_CHOICES, default='BRONZE')

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

    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        try:
            from reviews.models import Review
            notes = Review.objects.filter(reviewed_user=self).aggregate(models.Avg('rating'))
            return round(notes['rating__avg'], 2) if notes['rating__avg'] else None
        except ImportError:
            return None

    def update_reliability(self):
        """Update user reliability score and badge"""
        score = 0

        # KYC validation bonus
        if self.is_kyc_validated:
            score += 30
            
        # Average rating bonus
        if self.average_rating and self.average_rating >= 4.5:
            score += 20

        # Completed rides bonus
        try:
            from offers.models import RideOffer
            trajets_realises = RideOffer.objects.filter(driver=self, status='COMPLETED').count()
            score += trajets_realises * 5
        except ImportError:
            pass

        # Review average bonus
        try:
            from reviews.models import Review
            moyenne = Review.objects.filter(reviewed_user=self).aggregate(models.Avg('rating'))['rating__avg'] or 0
            if moyenne >= 4:
                score += 20
        except ImportError:
            pass

        # Complete profile bonus
        if hasattr(self, 'profile') and self.profile.photo_profile and self.vehicle_set.exists():
            score += 15

        # Account age bonus
        if (timezone.now() - self.date_joined).days >= 30:
            score += 10

        # Update score and badge
        self.reliability_score = score
        if score >= 90:
            self.reliability_badge = 'OR'
        elif score >= 50:
            self.reliability_badge = 'ARGENT'
        else:
            self.reliability_badge = 'BRONZE'

        self.save(update_fields=['reliability_score', 'reliability_badge'])


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal data
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    photo_profile = models.ImageField(
        upload_to="profiles/", 
        null=True, 
        blank=True, 
        help_text="Photo de profil de l'utilisateur"
    )

    # Location & schedule
    default_start_point = models.CharField(max_length=255, null=True, blank=True)
    default_end_point = models.CharField(max_length=255, null=True, blank=True)
    default_start_time = models.TimeField(null=True, blank=True)
    default_end_time = models.TimeField(null=True, blank=True)

    # Consent & tracking
    consent_tracking = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_name = models.DateTimeField(null=True, blank=True)

    def can_modify_name(self):
        """Check if user can modify their name (30-day cooldown)"""
        if self.last_modified_name:
            return (now() - self.last_modified_name).days >= 30
        return True

    def save(self, *args, **kwargs):
        """Update last_modified_name when name changes"""
        if self.pk:
            try:
                original = UserProfile.objects.get(pk=self.pk)
                if original.first_name != self.first_name or original.last_name != self.last_name:
                    self.last_modified_name = now()
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profil de {self.user.email}"


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicle_set")
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=50, unique=True)
    seats_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate} ({self.seats_available} places)"


class KYC(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "En attente"), 
        ("APPROVED", "Validé"), 
        ("REJECTED", "Rejeté")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="kyc")
    document_file = models.FileField(upload_to="kyc_documents/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    rejection_reason = models.TextField(null=True, blank=True)
    is_kyc_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)

    def approve(self):
        """Approve KYC and update user status"""
        self.status = "APPROVED"
        self.validated_at = now()
        self.is_kyc_validated = True
        self.rejection_reason = None
        self.save()
        
        # Update user KYC status
        self.user.is_kyc_validated = True
        self.user.save(update_fields=['is_kyc_validated'])

    def reject(self, reason):
        """Reject KYC with reason"""
        self.status = "REJECTED"
        self.is_kyc_validated = False
        self.rejection_reason = reason
        self.validated_at = None
        self.save()
        
        # Update user KYC status
        self.user.is_kyc_validated = False
        self.user.save(update_fields=['is_kyc_validated'])

    def __str__(self):
        return f"KYC - {self.user.email} : {self.status} : {'Validé' if self.is_kyc_validated else 'Non validé'}"


class TrackingGPS(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tracking")
    consent_tracking = models.BooleanField(default=True)

    # Real-time location
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

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "GPS History"
        verbose_name_plural = "GPS Histories"

    def __str__(self):
        return f"Position enregistrée ({self.latitude}, {self.longitude}) - {self.timestamp}"