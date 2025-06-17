# notifications/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from offers.models import RideRequest, RideOffer
from accounts.models import KYC
from billing.models import Invoice
from geoassist.models import TrackingSession
from notifications.utils import notify_user

# Quand une demande est créée ou mise à jour
@receiver(post_save, sender=RideRequest)
def notify_request_created_or_status_changed(sender, instance, created, **kwargs):
    if created and instance.offre_associee:
        conducteur = instance.offre_associee.driver
        notify_user(
            user=conducteur,
            notif_type="DEMANDE",
            context={
                "passager": instance.passenger.first_name,
                "destination": instance.end_point
            },
            data={"demande_id": instance.id}
        )
    elif not created:
        if instance.status == "ACCEPTEE":
            notify_user(
                user=instance.passenger,
                notif_type="VALIDATION",
                context={"conducteur": instance.offre_associee.driver.first_name},
                data={"offre_id": instance.offre_associee.id}
            )
        elif instance.status == "REFUSEE":
            notify_user(
                user=instance.passenger,
                notif_type="REFUS",
                context={"conducteur": instance.offre_associee.driver.first_name},
                data={"offre_id": instance.offre_associee.id}
            )

# KYC validé ou rejeté
@receiver(post_save, sender=KYC)
def notify_kyc_update(sender, instance, **kwargs):
    if instance.status == "APPROVED":
        statut = "validé"
    elif instance.status == "REJECTED":
        statut = "rejeté"
    else:
        return
    notify_user(
        user=instance.user,
        notif_type="KYC",
        context={"statut": statut},
        data={"kyc_id": instance.id}
    )

# Facture générée
@receiver(post_save, sender=Invoice)
def notify_invoice_created(sender, instance, created, **kwargs):
    if created:
        for user in [instance.conducteur, instance.passager]:
            notify_user(
                user=user,
                notif_type="FACTURE",
                context={"autre_user": instance.passager.first_name if user == instance.conducteur else instance.conducteur.first_name},
                data={"facture_id": instance.id}
            )

# Tracking activé
@receiver(post_save, sender=TrackingSession)
def notify_tracking_started(sender, instance, created, **kwargs):
    if created:
        receiver_user = instance.receiver
        notify_user(
            user=receiver_user,
            notif_type="TRACKING",
            context={"user": instance.sender.first_name},
            data={"tracking_id": instance.id}
        )
