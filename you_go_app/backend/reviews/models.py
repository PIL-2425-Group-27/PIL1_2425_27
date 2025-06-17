# reviews/models.py

from django.db import models
from django.conf import settings
from offers.models import RideOffer

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    reviewed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    offer = models.ForeignKey(
        RideOffer,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'reviewed_user', 'offer')  # Empêche double avis
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewed_user.username} ({self.rating}⭐)"
