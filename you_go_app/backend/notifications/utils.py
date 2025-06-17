from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.timezone import now
from .models import Notification




NOTIF_TEMPLATES = {
    "DEMANDE": {
        "title": "Nouvelle demande reçue",
        "message": lambda ctx: f"{ctx['passager']} souhaite rejoindre votre trajet vers {ctx['destination']}."
    },
    "VALIDATION": {
        "title": "Demande de covoiturage acceptée",
        "message": lambda ctx: f"Votre demande a été acceptée par {ctx['conducteur']}."
    },
    "REFUS": {
        "title": "Demande de covoiturage refusée",
        "message": lambda ctx: f"{ctx['conducteur']} a refusé votre demande de covoiturage."
    },
    "KYC": {
        "title": "Statut KYC mis à jour",
        "message": lambda ctx: f"Votre document KYC a été {ctx['statut']}."
    },
    "FACTURE": {
        "title": "Nouvelle facture générée",
        "message": lambda ctx: f"Votre trajet avec {ctx['autre_user']} a généré une facture disponible en PDF."
    },
    "ETA": {
        "title": "Estimation du temps d'arrivée",
        "message": lambda ctx: f"{ctx['conducteur']} sera à destination dans environ {ctx['temps']} minutes."
    },
    "TRACKING": {
        "title": "Suivi GPS activé",
        "message": lambda ctx: f"{ctx['user']} a partagé sa localisation en temps réel."
    },
    "RENDEZ_VOUS": {
        "title": "Point de rendez-vous défini",
        "message": lambda ctx: f"Votre point de RDV est situé à {ctx['lieu_nom']}."
    },
    "MESSAGE": {
        "title": "Nouveau message reçu",
        "message": lambda ctx: f"{ctx['from']} vous a envoyé un message : “{ctx['preview']}...”"
    },
    "SYSTEME": {
        "title": "Mise à jour du système",
        "message": lambda ctx: ctx['message']
    }
}
def notify_user(user, notif_type, context=None, data=None, critical=False):
    """
    Crée une notification et l’envoie à l’utilisateur via WebSocket
    :param user: utilisateur cible
    :param notif_type: type de notification (ex: "KYC", "DEMANDE")
    :param context: dictionnaire pour les templates dynamiques
    :param data: payload optionnel (ex: ID offre, lien, etc.)
    :param critical: importance critique (bool)
    """

    # Vérification du gabarit
    template = NOTIF_TEMPLATES.get(notif_type)
    if not template:
        raise ValueError(f"Aucun template défini pour le type '{notif_type}'")

    title = template["title"]
    message = template["message"](context or {})

    # Création en base
    notif = Notification.objects.create(
        user=user,
        notif_type=notif_type,
        title=title,
        message=message,
        data=data or {},
        is_critical=critical
    )

    # Envoi WebSocket
    try:
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}_notifications",
                {
                    "type": "send_notification",
                    "content": {
                        "id": notif.id,
                        "notif_type": notif.notif_type,
                        "title": notif.title,
                        "message": notif.message,
                        "data": notif.data,
                        "created_at": str(notif.created_at),
                        "is_critical": notif.is_critical
                    }
                }
            )
        else:
            print("⚠️ channel_layer is None, WebSocket notification not sent.")
    except Exception as e:
        print("⚠️ WebSocket non envoyé :", e)

    return notif

def create_notification(user, notif_type, title, message, data=None, is_critical=False):
    notif = Notification.objects.create(
        user=user,
        notif_type=notif_type,
        title=title,
        message=message,
        data=data,
        is_critical=is_critical
    )

    # === Diffusion en WebSocket en live ===
    channel_layer = get_channel_layer()
    group_name = f"user_{user.id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "notification": {
                "id": notif.id,
                "title": title,
                "message": message,
                "notif_type": notif_type,
                "data": data,
                "created_at": str(notif.created_at),
            },
        }
    )

    return notif
