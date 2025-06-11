from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Offer(models.Model):
    from django.conf import settings

    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    vehicle = models.CharField(max_length=100)
    preferences = models.TextField(blank=True)  # Ce qu’il aime/n’aime pas
    description = models.TextField(blank=True)  # Comment ça va se passer
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    client_proposes_price = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.departure_city} à {self.arrival_city} avec {self.driver.username}"
