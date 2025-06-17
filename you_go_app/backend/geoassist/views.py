from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
import requests
from .models import MeetingPoint
from offers.models import RideOffer, RideRequest


def reverse_geocode(lat, lon):
    """Utilise Nominatim pour convertir coordonnées en nom de lieu."""
    url = f"https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, headers={"User-Agent": "yougo-rdv-agent"})
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", f"{lat}, {lon}")
    except Exception:
        pass
    return f"{lat}, {lon}"


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_meeting_point(request, offer_id, request_id):
    """
    Calcule et suggère un point de rendez-vous intelligent entre le conducteur et le passager.
    """
    try:
        offer = RideOffer.objects.get(id=offer_id)
        ride_request = RideRequest.objects.get(id=request_id)
    except (RideOffer.DoesNotExist, RideRequest.DoesNotExist):
        return Response({"error": "Offre ou demande introuvable"}, status=404)

    # Vérification de la légitimité (l’utilisateur est conducteur ou passager concerné)
    if request.user != offer.driver and request.user != ride_request.passenger:
        return Response({"error": "Vous n’êtes pas autorisé à effectuer cette opération."}, status=403)

    # Récupérer les coordonnées de départ
    if not all([offer.start_latitude, offer.start_longitude, ride_request.start_latitude, ride_request.start_longitude]):
        return Response({"error": "Coordonnées GPS incomplètes."}, status=400)

    # Calcul du point médian
    lat_moy = (offer.start_latitude + ride_request.start_latitude) / 2
    lon_moy = (offer.start_longitude + ride_request.start_longitude) / 2

    # Géocodage inverse du point
    address = reverse_geocode(lat_moy, lon_moy)

    # Mise à jour ou création du point
    mp, created = MeetingPoint.objects.update_or_create(
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

    return Response({
        "message": "Point de rendez-vous suggéré avec succès.",
        "meeting_point": {
            "latitude": float(mp.latitude),
            "longitude": float(mp.longitude),
            "address": mp.address_label,
            "confirmed": mp.is_confirmed
        }
    }, status=201)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def confirm_meeting_point(request, offer_id, request_id):
    """
    Permet à un utilisateur (conducteur ou passager) de confirmer le point de RDV suggéré.
    """
    try:
        mp = MeetingPoint.objects.get(offer__id=offer_id, request__id=request_id)
    except MeetingPoint.DoesNotExist:
        return Response({"error": "Aucun point de rendez-vous trouvé."}, status=404)

    if request.user not in [mp.offer.driver, mp.request.passenger]:
        return Response({"error": "Non autorisé."}, status=403)

    mp.is_confirmed = True
    mp.confirmed_by = request.user
    mp.save()

    return Response({
        "message": "Point de rendez-vous confirmé.",
        "confirmed_by": request.user.username,
        "address": mp.address_label
    }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_eta_view(request):
    """
    Calcule l'estimation de la distance et du temps d’arrivée (ETA)
    entre deux points GPS à l’aide de OSRM.
    """

    try:
        from_lat = float(request.query_params.get("from_lat"))
        from_lon = float(request.query_params.get("from_lon"))
        to_lat = float(request.query_params.get("to_lat"))
        to_lon = float(request.query_params.get("to_lon"))
    except (TypeError, ValueError):
        return Response({"error": "Coordonnées GPS invalides ou manquantes."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{from_lon},{from_lat};{to_lon},{to_lat}?overview=false"
        headers = {"User-Agent": "ifri-comotorage/1.0"}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()

        if not data['routes']:
            raise ValueError("Pas de route disponible.")

        route = data['routes'][0]
        distance_km = round(route['distance'] / 1000, 2)
        duration_min = round(route['duration'] / 60)

        return Response({
            "distance_km": distance_km,
            "duration_minutes": duration_min,
            "message": "Estimation calculée avec succès."
        }, status=200)

    except Exception as e:
        return Response({
            "error": f"Erreur lors de la récupération de l'ETA : {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)