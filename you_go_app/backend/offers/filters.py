import django_filters
from .models import RideOffer, RideRequest
from django.utils.timezone import now


class RideOfferFilter(django_filters.FilterSet):
    date_trajet = django_filters.DateFilter(field_name='date_trajet', lookup_expr='exact')
    start_point = django_filters.CharFilter(lookup_expr='icontains')
    end_point = django_filters.CharFilter(lookup_expr='icontains')
    start_time = django_filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = django_filters.TimeFilter(field_name='end_time', lookup_expr='lte')
    price_type = django_filters.ChoiceFilter(choices=RideOffer.PRICING_MODE_CHOICES)
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    seats_available = django_filters.NumberFilter(field_name='seats_available', lookup_expr='gte')
    is_today = django_filters.BooleanFilter(method='filter_today')

    ordering = django_filters.OrderingFilter(
        fields=(('price', 'price'), ('date_trajet', 'date'), ('start_time', 'start_time')),
        field_labels={'price': 'Prix', 'date': 'Date', 'start_time': 'Départ'}
    )

    class Meta:
        model = RideOffer
        fields = ['date_trajet', 'start_point', 'end_point', 'start_time', 'end_time', 'price_type', 'max_price', 'seats_available']

    def filter_today(self, queryset, name, value):
        if value:
            return queryset.filter(date_trajet=now().date())
        return queryset
    is_upcoming = django_filters.BooleanFilter(method='filter_upcoming')
    def filter_upcoming(self, queryset, name, value):
        if value:
            return queryset.filter(date_trajet__gt=now().date())
        return queryset
    is_active = django_filters.BooleanFilter(method='filter_active')
    def filter_active(self, queryset, name, value):
        if value:
            return queryset.filter(status='ACTIF')
        return queryset

class RideRequestFilter(django_filters.FilterSet):
    date_trajet = django_filters.DateFilter(field_name='date_trajet', lookup_expr='exact')
    start_point = django_filters.CharFilter(lookup_expr='icontains')
    end_point = django_filters.CharFilter(lookup_expr='icontains')
    start_time = django_filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = django_filters.TimeFilter(field_name='end_time', lookup_expr='lte')
    price_preference = django_filters.ChoiceFilter(choices=RideRequest.PRICE_PREFERENCE_CHOICES)
    max_price = django_filters.NumberFilter(field_name='max_price', lookup_expr='lte')
    is_today = django_filters.BooleanFilter(method='filter_today')
    
    ordering = django_filters.OrderingFilter(
        fields=(('price', 'price'), ('date_trajet', 'date'), ('start_time', 'start_time')),
        field_labels={'price': 'Prix', 'date': 'Date', 'start_time': 'Départ'}
    )

    class Meta:
        model = RideRequest
        fields = ['date_trajet', 'start_point', 'end_point', 'start_time', 'end_time', 'price_preference', 'max_price']

    def filter_today(self, queryset, name, value):
        if value:
            return queryset.filter(date_trajet=now().date())
        return queryset
    is_upcoming = django_filters.BooleanFilter(method='filter_upcoming')
    def filter_upcoming(self, queryset, name, value):
        if value:
            return queryset.filter(date_trajet__gt=now().date())
        return queryset
    is_active = django_filters.BooleanFilter(method='filter_active')
    def filter_active(self, queryset, name, value):
        if value:
            return queryset.filter(status='EN_ATTENTE')
        return queryset

    