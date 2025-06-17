from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review

@receiver(post_save, sender=Review)
def update_reviewed_user_badge(sender, instance, created, **kwargs):
    if created:
        instance.reviewed_user.update_reliability()
        instance.reviewed_user.save()
        