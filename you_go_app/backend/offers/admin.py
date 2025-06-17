from django.contrib import admin
from django.contrib import admin
from .models import RideOffer, RideRequest

@admin.register(RideOffer)
class RideOfferAdmin(admin.ModelAdmin):
    list_display = ('driver', 'start_point', 'end_point', 'date_trajet', 'price', 'price_type', 'status')
    list_filter = ('status', 'price_type')
    search_fields = ('start_point', 'end_point', 'driver__email')
    readonly_fields = ('created_at',)

@admin.register(RideRequest)
class RideRequestAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'start_point', 'end_point', 'date_trajet', 'status', 'price_preference')
    list_filter = ('status', 'price_preference')
    search_fields = ('passenger__email', 'start_point', 'end_point')
