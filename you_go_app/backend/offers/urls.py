# backend/offers/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='offers-index'),
    path('create/', views.create_offer, name='create-offer'),
]
from django.http import HttpResponse

def index(request):
    return HttpResponse("Bienvenue sur la page des offres !")
