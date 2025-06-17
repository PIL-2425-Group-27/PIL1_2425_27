
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import now
from decimal import Decimal
import requests
import logging
logger = logging.getLogger(__name__)


# ____________________________________Offer____________________________________________________
class RideOffer(models.Model):
    PRICING_MODE_CHOICES = [
        ('FIXE', 'Prix fixe'),
        ('DYNAMIQUE', 'Estimation automatique'),
        ('GRATUIT', 'Gratuit')
    ]

    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('ANNULE', 'Annulé'),
        ('EXPIRE', 'Expiré')
    ]
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['driver', 'date_trajet', 'start_time'],
                name='unique_offer_per_driver_per_timeslot'
            )
        ]
    
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ride_offers')
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)

    start_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    start_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    end_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    end_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    date_trajet = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    seats_available = models.PositiveIntegerField(default=1)

    price_type = models.CharField(max_length=10, choices=PRICING_MODE_CHOICES, default='GRATUIT')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ACTIF')

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.price_type == 'FIXE' and self.price is None:
            raise ValidationError("Le prix est requis pour le mode FIXE.")
        if self.date_trajet < timezone.now().date():
            raise ValidationError("La date du trajet ne peut pas être dans le passé.")
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de départ doit être antérieure à l'heure d'arrivée.")
    def geocode_address(self, address):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        try:
            response = requests.get(url, params=params, headers={'User-Agent': 'you-go-app/1.0'},timeout=10)
            response.raise_for_status()
            results = response.json()
            if results:
                return float(results[0]['lat']), float(results[0]['lon'])
        except (requests.RequestException, ValueError) as e:
            print(f"[Erreur géocodage] {e}")
        return None, None

    def estimer_prix_osrm(self):
        if not all([self.start_latitude, self.start_longitude, self.end_latitude, self.end_longitude]):
            raise ValidationError("Coordonnées GPS incomplètes pour l'estimation.")

        try:
            url = f"http://router.project-osrm.org/route/v1/driving/{self.start_longitude},{self.start_latitude};{self.end_longitude},{self.end_latitude}?overview=false"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            distance_m = data['routes'][0]['distance']
            distance_km = Decimal(distance_m) / 1000
            tarif_base = Decimal(50)
            tarif_par_km = Decimal(100)
            prix = tarif_base + (distance_km * tarif_par_km)
            return round(prix, 2)
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.warning("[OSRM] ...")
            raise ValidationError("Impossible de calculer la distance avec OSRM.")
        if response.status_code != 200:
            raise ValidationError("Erreur lors de la requête OSRM.")

        data = response.json()
        try:
            distance_m = data['routes'][0]['distance']
            distance_km = Decimal(distance_m) / 1000
            tarif_base = int(50)
            tarif_par_km = int(100)
            prix = tarif_base + (distance_km * tarif_par_km)
            return round(prix, 2)
        except Exception:
            raise ValidationError("Impossible de calculer la distance avec OSRM.")

    def save(self, *args, **kwargs):
        # Géocode uniquement si l'adresse a changé ou si les coordonnées sont absentes
        if self.start_point and (self.start_latitude is None or self.start_longitude is None):
            lat, lon = self.geocode_address(self.start_point)
            if lat is not None and lon is not None:
                self.start_latitude = lat
                self.start_longitude = lon
        if self.end_point and (self.end_latitude is None or self.end_longitude is None):
            lat, lon = self.geocode_address(self.end_point)
            if lat is not None and lon is not None:
                self.end_latitude = lat
                self.end_longitude = lon

        # Set price according to price_type
        if self.price_type == 'GRATUIT':
            self.price = Decimal(0)
        elif self.price_type == 'DYNAMIQUE':
            try:
                estimated_price = self.estimer_prix_osrm()
                if estimated_price is not None:
                    self.price = estimated_price
                else:
                    self.price = None
            except ValidationError:
                self.price = None

        super().full_clean()  # Validate all fields before saving
        super().save(*args, **kwargs)

    # Référence au véhicule par défaut du conducteur
    vehicle = models.ForeignKey(
        'accounts.Vehicle',  # Assure-toi que ce modèle existe bien
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offers'
    )

    # Utiliser un véhicule personnalisé ?
    use_custom_vehicle_info = models.BooleanField(default=False)

    # Champs du véhicule personnalisé
    custom_vehicle_brand = models.CharField(max_length=100, null=True, blank=True)
    custom_vehicle_model = models.CharField(max_length=100, null=True, blank=True)
    custom_vehicle_plate = models.CharField(max_length=50, null=True, blank=True)
    custom_vehicle_seats = models.PositiveIntegerField(null=True, blank=True)

    def get_vehicle_info(self):
        if self.use_custom_vehicle_info:
            return {
                "brand": self.custom_vehicle_brand,
                "model": self.custom_vehicle_model,
                "plate": self.custom_vehicle_plate,
                "seats": self.custom_vehicle_seats
            }
        elif self.vehicle:
            return {
                "brand": self.vehicle.brand,
                "model": self.vehicle.model,
                "plate": self.vehicle.license_plate,
                "seats": self.vehicle.seats_available
            }
        return None
    def __str__(self):
        veh = self.get_vehicle_info()
        vstr = f"{veh['brand']} {veh['model']}" if veh else "Véhicule inconnu"
        return f"{self.driver.username} → {self.end_point} ({self.date_trajet}) avec {vstr}"


class RideRequest(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTEE', 'Acceptée'),
        ('REFUSEE', 'Refusée'),
        ('EXPIRE', 'Expirée')
    ]
    PRICE_PREFERENCE_CHOICES = [
        ('GRATUIT', 'Gratuit'),
        ('FIXE', 'Fixé'),
        ('ESTIME', 'Estimé')
    ]

    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ride_requests')
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    date_trajet = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE')

    offre_associee = models.ForeignKey(RideOffer, null=True, blank=True, on_delete=models.SET_NULL, related_name='demandes_associees')

    created_at = models.DateTimeField(auto_now_add=True)
    price_preference = models.CharField(max_length=10, choices=PRICE_PREFERENCE_CHOICES, default='GRATUIT')
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def clean(self):
        if self.offre_associee and self.offre_associee.status != 'ACTIF':
            raise ValidationError("L'offre associée n'est pas active.")
        if self.date_trajet < timezone.now().date():
            raise ValidationError("La date du trajet ne peut pas être dans le passé.")
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de départ doit être antérieure à l'heure d'arrivée.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# offers/models.py
class RideOfferManager(models.Manager):
    def active_valid(self):
        return self.filter(status='ACTIF', date_trajet__gte=now().date())
    def expired(self):
        return self.filter(status='EXPIRE', date_trajet__lt=now().date())
    def auto_expire(self):
        expired_offers = self.filter(status='ACTIF', date_trajet__lt=now().date())
        expired_offers.update(status='EXPIRE')
        return expired_offers
    