from django.shortcuts import render

# reviews/views.py

from rest_framework import generics, permissions
from .models import Review
from rest_framework.views import APIView
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from offers.models import RideOffer, RideRequest
from django.db.models import Sum, Q, Count
from django.utils.timezone import now
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Review.objects.filter(reviewed_user__id=self.kwargs['user_id'])

class GlobalUserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()

        # Liste des 7 derniers jours (de Lundi à aujourd’hui)
        week_dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        labels = [date.strftime('%A') for date in week_dates]  # ['Lundi', ..., 'Dimanche']

        trajet_counts = []
        km_by_day = []

        for date in week_dates:
            # Nombre de trajets validés ce jour-là
            demandes = RideRequest.objects.filter(passenger=user, status='ACCEPTEE', date_trajet=date)
            offres = RideOffer.objects.filter(driver=user, status='ACTIF', date_trajet=date)

            total_trajets = demandes.count() + offres.count()
            trajet_counts.append(total_trajets)

            # Distance estimée (2 km par trajet)
            km = total_trajets * 3 # 3 km par trajet en moyenne
            km_by_day.append(float(km))

        return Response({
            "labels": labels,  # ['Lundi', 'Mardi', ...]
            "total_trajets": trajet_counts,
            "total_km": km_by_day,
        })
