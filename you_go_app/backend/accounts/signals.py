# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
from offers.models import RideOffer
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Créer automatiquement un profil lié au nouvel utilisateur
        UserProfile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name
        )
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Mettre à jour le profil de l'utilisateur à chaque fois que l'utilisateur est sauvegardé
    instance.save()
@receiver(post_save, sender=UserProfile)
def update_user_profile(sender, instance, **kwargs):
    # Mettre à jour les champs du profil utilisateur si nécessaire
    user = instance.user
    user.first_name = instance.first_name
    user.last_name = instance.last_name
    user.save()
@receiver(post_save, sender=UserProfile)
def update_last_modified_name(sender, instance, **kwargs):
    # Mettre à jour la date de dernière modification du nom si le nom a changé
    user = instance.user
    if instance.last_modified_name:
        user.last_modified_username = instance.last_modified_name
        user.save()
    else:
        user.last_modified_username = None
        user.save()
@receiver(post_save, sender=User)
def update_user_kyc_status(sender, instance, **kwargs):
    # Mettre à jour le statut KYC de l'utilisateur si le profil KYC est validé
    if hasattr(instance, 'kyc'):
        instance.is_kyc_validated = instance.kyc.is_kyc_validated
        instance.save()
    else:
        instance.is_kyc_validated = False
        instance.save()
@receiver(post_save, sender=RideOffer)
def update_user_score_on_offer(sender, instance, created, **kwargs):
    if created:
        instance.driver.update_reliability()

@receiver(post_save, sender=User)
def update_score_on_kyc_or_profile(sender, instance, **kwargs):
    instance.update_reliability()