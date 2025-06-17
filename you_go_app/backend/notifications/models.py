from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ("DEMANDE", "Demande"),
        ("VALIDATION", "Validation"),
        ("REFUS", "Refus"),
        ("KYC", "KYC"),
        ("MESSAGE", "Message instantané"),
        ("FACTURE", "Facture"),
        ("TRACKING", "Tracking"),
        ("RENDEZ_VOUS", "Point de RDV"),
        ("ETA", "ETA"),
        ("SYSTEME", "Système"),
    ]

    # Utilisateur cible de la notification
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    # Type d’événement
    notif_type = models.CharField(
        max_length=30,
        choices=NOTIF_TYPE_CHOICES
    )

    # Titre court (affiché dans l’interface)
    title = models.CharField(max_length=255)

    # Message détaillé de la notification
    message = models.TextField()

    # Statut de lecture
    is_read = models.BooleanField(default=False)

    # Données supplémentaires liées à la notification
    data = models.JSONField(null=True, blank=True)

    # Pour les systèmes futurs : est-ce une notification importante ?
    is_critical = models.BooleanField(default=False)

    # Date de création
    created_at = models.DateTimeField(auto_now_add=True)

    # Date de lecture
    read_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ['-created_at']

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

    def __str__(self):
        user_email = getattr(self.user, 'email', 'Utilisateur inconnu')
        return f"[{self.notif_type}] {self.title} → {user_email} ({'Lu' if self.is_read else 'Non lu'})"
