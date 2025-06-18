# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={
                'first_name': instance.first_name,
                'last_name': instance.last_name
            }
        )


@receiver(post_save, sender=UserProfile)
def sync_user_names(sender, instance, **kwargs):
    """Sync user first_name and last_name with profile"""
    user = instance.user
    updated = False
    
    if user.first_name != instance.first_name:
        user.first_name = instance.first_name
        updated = True
        
    if user.last_name != instance.last_name:
        user.last_name = instance.last_name
        updated = True
        
    if updated:
        user.save(update_fields=['first_name', 'last_name'])


@receiver(post_save, sender=UserProfile)
def sync_last_modified_name(sender, instance, **kwargs):
    """Sync last_modified_name to user model"""
    user = instance.user
    if user.last_modified_username != instance.last_modified_name:
        user.last_modified_username = instance.last_modified_name
        user.save(update_fields=['last_modified_username'])


# Signal for updating reliability when offers are created
@receiver(post_save, sender='offers.RideOffer')
def update_reliability_on_offer(sender, instance, created, **kwargs):
    """Update driver reliability when ride offer is created"""
    if created and hasattr(instance, 'driver'):
        instance.driver.update_reliability()


# Signal for updating reliability when reviews are created
@receiver(post_save, sender='reviews.Review')
def update_reliability_on_review(sender, instance, created, **kwargs):
    """Update user reliability when review is created"""
    if created and hasattr(instance, 'reviewed_user'):
        instance.reviewed_user.update_reliability()