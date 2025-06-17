# offers/matching.py

from .models import RideOffer, RideRequest
from django.db.models import Q
from datetime import timedelta


def match_requests_for_offer(offer):
    """
    Trouve les demandes compatibles avec une offre donnée.
    """
    return RideRequest.objects.filter(
        date_trajet=offer.date_trajet,
        status='EN_ATTENTE',
        start_point__icontains=offer.start_point,
        end_point__icontains=offer.end_point,
        start_time__lte=offer.start_time + timedelta(minutes=30),
        end_time__gte=offer.end_time - timedelta(minutes=30),
        price_preference__in=['GRATUIT', 'ESTIME'] if offer.price_type == 'GRATUIT' else ['FIXE', 'ESTIME'],
    )


def match_offers_for_request(request):
    """
    Trouve les offres compatibles avec une demande donnée.
    """
    return RideOffer.objects.filter(
        status='ACTIF',
        date_trajet=request.date_trajet,
        seats_available__gte=1,
        start_point__icontains=request.start_point,
        end_point__icontains=request.end_point,
        start_time__lte=request.start_time + timedelta(minutes=30),
        end_time__gte=request.end_time - timedelta(minutes=30),
    ).order_by('price')  # Bonus : trie par prix
