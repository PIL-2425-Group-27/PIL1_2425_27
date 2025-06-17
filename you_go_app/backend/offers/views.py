from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from geoassist.utils import generate_intelligent_meeting_point
from mailing.utils import send_transactional_email
from django.utils import timezone
from datetime import timedelta

from .models import RideOffer, RideRequest
from .serializers import RideOfferSerializer, RideRequestSerializer
from .filters import RideOfferFilter, RideRequestFilter
from .utils import expire_old_offers_and_requests

# ==========================
#     OFFRES DE COVOITURAGE
# ==========================

class OfferCreateView(generics.CreateAPIView):
    queryset = RideOffer.objects.all()
    serializer_class = RideOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

class OfferListView(generics.ListAPIView):
    serializer_class = RideOfferSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        expire_old_offers_and_requests()
        return RideOffer.objects.filter(status='ACTIF', date_trajet__gte=timezone.now().date()).order_by('-created_at')

class OfferDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = RideOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        expire_old_offers_and_requests()
        return RideOffer.objects.filter(driver=self.request.user)

    def get_object(self):
        offer = super().get_object()
        if offer.driver != self.request.user:
            raise PermissionDenied("Vous ne pouvez consulter ou modifier que vos propres offres.")
        return offer

    def perform_update(self, serializer):
        if self.get_object().status == 'EXPIRE':
            raise PermissionDenied("Impossible de modifier une offre expirée.")
        serializer.save()


# ==========================
#     DEMANDES DE COVOITURAGE
# ==========================

class RequestCreateView(generics.CreateAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(passenger=self.request.user)
        # Envoi d'un email au conducteur associé si l'offre existe
        # et que la demande est créée avec succès
        if instance.offre_associee:
            conducteur = instance.offre_associee.driver
            send_transactional_email(
                subject="💬 Nouvelle demande de covoiturage",
                to_email=conducteur.email,
                template_name="emails/request_received.html",
                context={
                    "user": conducteur,
                    "passenger": self.request.user,
                    "offre": instance.offre_associee
                }
            )

class RequestListView(generics.ListAPIView):
    serializer_class = RideRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        self._auto_expire_requests()
        return RideRequest.objects.filter(passenger=self.request.user).order_by('-created_at')

    def _auto_expire_requests(self):
        RideRequest.objects.filter(
            passenger=self.request.user,
            status='EN_ATTENTE',
            date_trajet__lt=timezone.now().date()
        ).update(status='EXPIRE')

class RequestDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = RideRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RideRequest.objects.filter(passenger=self.request.user)

    def get_object(self):
        req = super().get_object()
        if req.passenger != self.request.user:
            raise PermissionDenied("Vous ne pouvez consulter ou modifier que vos propres demandes.")
        return req

    def perform_update(self, serializer):
        if self.get_object().status == 'EXPIRE':
            raise PermissionDenied("Impossible de modifier une demande expirée.")
        serializer.save()


# ==========================
#     FILTRAGE ET RECHERCHE
# ==========================

class OfferSearchView(generics.ListAPIView):
    queryset = RideOffer.objects.all()
    serializer_class = RideOfferSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['start_point', 'end_point']
    ordering_fields = ['start_time', 'date_trajet']
    filterset_class = RideOfferFilter

class RequestSearchView(generics.ListAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['start_point', 'end_point']
    ordering_fields = ['start_time', 'date_trajet']
    filterset_class = RideRequestFilter


# ==========================
#     JOURNALIERS
# ==========================

class OfferTodayView(generics.ListAPIView):
    serializer_class = RideOfferSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return RideOffer.objects.filter(date_trajet=timezone.now().date(), status='ACTIF')

class RequestTodayView(generics.ListAPIView):
    serializer_class = RideRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RideRequest.objects.filter(date_trajet=timezone.now().date(), status='EN_ATTENTE')


# ==========================
#     MATCHING INTELLIGENT
# ==========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_matching_offers(request, request_id):
    try:
        ride_request = RideRequest.objects.get(id=request_id, passenger=request.user)
    except RideRequest.DoesNotExist:
        return Response({"error": "Demande introuvable."}, status=404)

    offres = RideOffer.objects.filter(
        status='ACTIF',
        date_trajet=ride_request.date_trajet,
        seats_available__gte=1,
        start_point__icontains=ride_request.start_point,
        end_point__icontains=ride_request.end_point,
        start_time__lte=ride_request.start_time + timedelta(minutes=30),
        end_time__gte=ride_request.end_time - timedelta(minutes=30)
    )

    if ride_request.price_preference == 'FIXE' and ride_request.max_price:
        offres = offres.filter(price__lte=ride_request.max_price)

    serializer = RideOfferSerializer(offres, many=True, context={"request": request})
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_matching_requests(request, offer_id):
    try:
        offer = RideOffer.objects.get(id=offer_id, driver=request.user)
    except RideOffer.DoesNotExist:
        return Response({"error": "Offre introuvable ou non autorisée."}, status=404)

    demandes = RideRequest.objects.filter(
        status='EN_ATTENTE',
        date_trajet=offer.date_trajet,
        start_point__icontains=offer.start_point,
        end_point__icontains=offer.end_point,
        start_time__lte=offer.start_time + timedelta(minutes=30),
        end_time__gte=offer.end_time - timedelta(minutes=30),
    )

    if offer.price_type == 'FIXE':
        demandes = demandes.filter(price_preference__in=['FIXE', 'ESTIME'], max_price__gte=offer.price)
    elif offer.price_type == 'GRATUIT':
        demandes = demandes.filter(price_preference__in=['GRATUIT', 'ESTIME'])

    serializer = RideRequestSerializer(demandes, many=True, context={"request": request})
    return Response(serializer.data, status=200)


# ==========================
#     VALIDATION DE DEMANDE
# ==========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_ride_request(request, request_id):
    action = request.data.get("action")  # "accept" ou "refuse"

    try:
        ride_request = RideRequest.objects.get(id=request_id)
    except RideRequest.DoesNotExist:
        return Response({"error": "Demande introuvable."}, status=404)

    # Vérifie que l'utilisateur est bien conducteur ou passager concerné
    if ride_request.passenger != request.user and (
        not ride_request.offre_associee or ride_request.offre_associee.driver != request.user
    ):
        return Response({"error": "Action non autorisée."}, status=403)

    if ride_request.status in ["ACCEPTEE", "REFUSEE", "EXPIRE"]:
        return Response({"error": f"Cette demande est déjà {ride_request.status.lower()}."}, status=400)

    if action == "accept":
        ride_request.status = "ACCEPTEE"
        ride_request.save()
        generate_intelligent_meeting_point(offer, ride_request)
        # Envoi d'un email de confirmation au passager
        send_transactional_email(
            subject="✅ Covoiturage accepté",
            to_email=ride_request.passenger.email,
            template_name="emails/covoiturage_confirmed.html",
            context={
                "user": ride_request.passenger,
                "offer": ride_request.offre_associee,
                "request": ride_request
            }
        )
        if ride_request.offre_associee:
            offer = ride_request.offre_associee
            offer.seats_available = max(offer.seats_available - 1, 0)
            offer.save()

        return Response({"message": "Covoiturage accepté."}, status=200)

    elif action == "refuse":
        ride_request.status = "REFUSEE"
        ride_request.save()
        
        return Response({"message": "Demande refusée."}, status=200)

    return Response({"error": "Action invalide. Utilisez 'accept' ou 'refuse'."}, status=400)
