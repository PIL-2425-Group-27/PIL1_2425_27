from django.utils.timezone import now
from .models import RideOffer, RideRequest

def expire_old_offers_and_requests():
    today = now().date()

    # Offres
    RideOffer.objects.filter(date_trajet__lt=today, status="ACTIF").update(status="EXPIRE")

    # Demandes
    RideRequest.objects.filter(date_trajet__lt=today, status="EN_ATTENTE").update(status="EXPIRE")
