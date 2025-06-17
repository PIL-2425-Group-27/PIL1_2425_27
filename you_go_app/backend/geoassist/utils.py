from decimal import Decimal
from .models import MeetingPoint
from offers.models import RideOffer, RideRequest
import requests


def reverse_geocode(lat, lon):
    """Convertit des coordonnées en adresse lisible via Nominatim."""
    url = f"https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, headers={"User-Agent": "yougo-rdv-bot"})
        if response.status_code == 200:
            return response.json().get("display_name", f"{lat}, {lon}")
    except Exception:
        pass
    return f"{lat}, {lon}"


def generate_intelligent_meeting_point(offer, ride_request):
    """Crée ou met à jour un point de rendez-vous entre une offre et une demande."""
    if not all([
        offer.start_latitude, offer.start_longitude,
        ride_request.start_latitude, ride_request.start_longitude
    ]):
        return None

    lat_moy = (offer.start_latitude + ride_request.start_latitude) / 2
    lon_moy = (offer.start_longitude + ride_request.start_longitude) / 2
    address = reverse_geocode(lat_moy, lon_moy)

    mp, _ = MeetingPoint.objects.update_or_create(
        offer=offer,
        request=ride_request,
        defaults={
            "latitude": round(Decimal(lat_moy), 6),
            "longitude": round(Decimal(lon_moy), 6),
            "address_label": address,
            "is_confirmed": False,
            "confirmed_by": None
        }
    )
    return mp
