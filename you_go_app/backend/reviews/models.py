# reviews/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from offers.models import RideOffer

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    # Review types for better categorization
    REVIEW_TYPE_CHOICES = [
        ('DRIVER', _('Driver Review')),
        ('PASSENGER', _('Passenger Review')),
    ]

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given',
        verbose_name=_('Reviewer')
    )
    reviewed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received',
        verbose_name=_('Reviewed User')
    )
    offer = models.ForeignKey(
        RideOffer,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Ride Offer')
    )

    # Enhanced rating system
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Rating')
    )
    
    # Detailed rating categories
    punctuality_rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name=_('Punctuality')
    )
    
    communication_rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name=_('Communication')
    )
    
    vehicle_condition_rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name=_('Vehicle Condition'),
        help_text=_('Only for driver reviews')
    )

    comment = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name=_('Comment')
    )
    
    review_type = models.CharField(
        max_length=10,
        choices=REVIEW_TYPE_CHOICES,
        verbose_name=_('Review Type')
    )
    
    # Moderation fields
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Verified Review')
    )
    
    is_flagged = models.BooleanField(
        default=False,
        verbose_name=_('Flagged for Review')
    )
    
    flagged_reason = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Flag Reason')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('reviewer', 'reviewed_user', 'offer')
        ordering = ['-created_at']
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        indexes = [
            models.Index(fields=['reviewed_user', '-created_at']),
            models.Index(fields=['rating']),
            models.Index(fields=['review_type']),
        ]

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewed_user.username} ({self.rating}⭐)"
    
    @property
    def average_detailed_rating(self):
        """Calculate average of detailed ratings if available"""
        ratings = [r for r in [self.punctuality_rating, self.communication_rating, 
                              self.vehicle_condition_rating] if r is not None]
        return sum(ratings) / len(ratings) if ratings else self.rating
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Ensure reviewer and reviewed_user are different
        if self.reviewer == self.reviewed_user:
            raise ValidationError(_("You cannot review yourself."))
        
        # Validate vehicle condition rating only for driver reviews
        if self.review_type == 'PASSENGER' and self.vehicle_condition_rating:
            raise ValidationError(_("Vehicle condition rating only applies to driver reviews."))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ReviewFlag(models.Model):
    """Model for handling review flags/reports"""
    FLAG_REASONS = [
        ('INAPPROPRIATE', _('Inappropriate Content')),
        ('SPAM', _('Spam')),
        ('FALSE', _('False Information')),
        ('HARASSMENT', _('Harassment')),
        ('OTHER', _('Other')),
    ]
    
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='flags'
    )
    
    flagger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_flags'
    )
    
    reason = models.CharField(
        max_length=20,
        choices=FLAG_REASONS
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        max_length=300
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('review', 'flagger')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Flag for {self.review} by {self.flagger.username}"


class UserReviewSummary(models.Model):
    """Cached summary of user reviews for performance"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_summary'
    )
    
    total_reviews = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, null=True, blank=True)
    
    # Detailed averages
    avg_punctuality = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    avg_communication = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    avg_vehicle_condition = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    # Rating distribution
    five_star_count = models.PositiveIntegerField(default=0)
    four_star_count = models.PositiveIntegerField(default=0)
    three_star_count = models.PositiveIntegerField(default=0)
    two_star_count = models.PositiveIntegerField(default=0)
    one_star_count = models.PositiveIntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Review Summary')
        verbose_name_plural = _('User Review Summaries')
    
    def update_summary(self):
        """Update the cached summary from actual reviews"""
        from django.db.models import Avg, Count
        
        reviews = Review.objects.filter(reviewed_user=self.user)
        
        if reviews.exists():
            stats = reviews.aggregate(
                total=Count('id'),
                avg_rating=Avg('rating'),
                avg_punctuality=Avg('punctuality_rating'),
                avg_communication=Avg('communication_rating'),
                avg_vehicle=Avg('vehicle_condition_rating'),
                five_stars=Count('id', filter=models.Q(rating=5)),
                four_stars=Count('id', filter=models.Q(rating=4)),
                three_stars=Count('id', filter=models.Q(rating=3)),
                two_stars=Count('id', filter=models.Q(rating=2)),
                one_star=Count('id', filter=models.Q(rating=1)),
            )
            
            self.total_reviews = stats['total']
            self.average_rating = round(stats['avg_rating'] or 0, 2)
            self.avg_punctuality = round(stats['avg_punctuality'] or 0, 2) if stats['avg_punctuality'] else None
            self.avg_communication = round(stats['avg_communication'] or 0, 2) if stats['avg_communication'] else None
            self.avg_vehicle_condition = round(stats['avg_vehicle'] or 0, 2) if stats['avg_vehicle'] else None
            
            self.five_star_count = stats['five_stars']
            self.four_star_count = stats['four_stars']
            self.three_star_count = stats['three_stars']
            self.two_star_count = stats['two_stars']
            self.one_star_count = stats['one_star']
        else:
            # Reset to defaults
            self.total_reviews = 0
            self.average_rating = 0.00
            self.avg_punctuality = None
            self.avg_communication = None
            self.avg_vehicle_condition = None
            self.five_star_count = 0
            self.four_star_count = 0
            self.three_star_count = 0
            self.two_star_count = 0
            self.one_star_count = 0
        
        self.save()
    
    def __str__(self):
        return f"{self.user.username} - {self.average_rating}⭐ ({self.total_reviews} reviews)"