from django.urls import path, include
from .views import (
    OfferCreateView,
    OfferListView,
    OfferDetailView,
    RequestCreateView,
    RequestListView,
    RequestDetailView,
    OfferSearchView,
    RequestSearchView,
    OfferTodayView,
    RequestTodayView,
    get_matching_offers,
    get_matching_requests,
    validate_ride_request
)

urlpatterns = [
    # ---------- OFFRES DE COVOITURAGE ----------
    # Liste / création
    path("", OfferListView.as_view(),   name="offer-list"),   # GET : toutes les offres actives
    path("create/", OfferCreateView.as_view(), name="offer-create"), # POST : publier une offre
    # Détail / mise à jour / suppression éventuelle (via PUT/PATCH/DELETE)
    path("<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),

    # ---------- DEMANDES DE COVOITURAGE ----------
    # Liste / création
    path("requests/", RequestListView.as_view(),   name="request-list"),   # GET : mes demandes
    path("requests/create/", RequestCreateView.as_view(), name="request-create"), # POST : créer une demande
    # Détail / mise à jour / suppression éventuelle
    path("requests/<int:pk>/", RequestDetailView.as_view(), name="request-detail"),
    # ---------- RECHERCHE AVANCEE ----------
    path("search/", OfferSearchView.as_view(), name="offer-search"),  # GET : recherche avancée d'offres
    path("requests/search/", RequestSearchView.as_view(), name="request-search"),  # GET : recherche avancée de demandes
    # ---------- OFFRES ET DEMANDES DU JOUR ----------
    path("today/", OfferTodayView.as_view(), name="offer-today"),  # GET : offres du jour
    path("requests/today/", RequestTodayView.as_view(), name="request-today"),  # GET : demandes du jour
    # ---------- MATCHING OFFRES/DEMANDES ----------
    path("requests/<int:request_id>/matches/", get_matching_offers, name="match-offers-for-request"),
    path("<int:offer_id>/matches/", get_matching_requests, name="match-requests-for-offer"),

    # ---------- VALIDATION DES DEMANDES ----------
    path("requests/<int:request_id>/validate/", validate_ride_request, name="validate-ride-request"),
]
