from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from offers.models import RideOffer, RideRequest


class MeetingPoint(models.Model):
    """
    Modèle représentant un point de rendez-vous intelligent généré entre une offre et une demande.
    """

    # Liens avec les trajets concernés
    offer = models.ForeignKey(RideOffer, on_delete=models.CASCADE, related_name='meeting_points')
    request = models.ForeignKey(RideRequest, on_delete=models.CASCADE, related_name='meeting_points')

    # Coordonnées du point calculé
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    # Adresse humaine retournée par l’API (Nominatim / Google Maps)
    address_label = models.CharField(max_length=255)

    # Est-ce une suggestion automatique ou un point validé par utilisateur ?
    is_confirmed = models.BooleanField(default=False)

    # Pour savoir qui a confirmé (passager ou conducteur)
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_meeting_points'
    )

    # Historique
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('offer', 'request')  # 1 seul point proposé entre une offre et une demande

    def __str__(self):
        return f"RDV entre {self.offer.driver.username} et {self.request.passenger.username} - {self.address_label}"
