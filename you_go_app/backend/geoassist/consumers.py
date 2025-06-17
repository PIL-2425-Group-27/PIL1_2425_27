import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from accounts.models import TrackingGPS
from offers.models import RideOffer, RideRequest
from django.utils.timezone import now, timezone

User = get_user_model()

class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.target_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.viewer = self.scope["user"]

        if not self.viewer.is_authenticated:
            await self.close()
            return

        is_allowed = await self.has_access(self.viewer.id, self.target_user_id)
        if not is_allowed:
            await self.close()
            return

        self.room_name = f"tracking_{self.target_user_id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
    async def notify_disconnect(self):
        """Déclenche la déconnexion WebSocket côté client."""
        await self.send(text_data=json.dumps({
            "type": "force_disconnect",
            "reason": "Trajet terminé ou expiré. Fin du tracking."
    }))
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        lat = data.get("latitude")
        lon = data.get("longitude")

        if lat and lon:
            await self.save_position(self.target_user_id, lat, lon)
            is_trip_active = await self.trip_still_active()
            if not is_trip_active:
                await self.notify_disconnect()
                return
            eta_data = await self.calculate_eta_for_viewer(lat, lon)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "tracking_update",
                    "latitude": lat,
                    "longitude": lon,
                    "timestamp": str(now()),
                    "eta": eta_data
                }
            )

    async def tracking_update(self, event):
        await self.send(text_data=json.dumps({
            "latitude": event["latitude"],
            "longitude": event["longitude"],
            "timestamp": event["timestamp"],
            "eta": event.get("eta")  # ETA live
        }))

    @database_sync_to_async
    def save_position(self, user_id, lat, lon):
        try:
            user = User.objects.get(id=user_id)
            gps, _ = TrackingGPS.objects.get_or_create(user=user)
            gps.last_latitude = lat
            gps.last_longitude = lon
            gps.save()
        except:
            pass

    @database_sync_to_async
    def has_access(self, viewer_id, target_id):
        if int(viewer_id) == int(target_id):
            return False  # Pas d’auto-tracking

        try:
            viewer = User.objects.get(id=viewer_id)
            target = User.objects.get(id=target_id)
            # Le tracking doit être activé par target
            tracking = getattr(target, "tracking", None)
            if not tracking or not tracking.consent_tracking:
                return False
            # Doivent être liés par un covoiturage
            match = RideOffer.objects.filter(
                driver__in=[viewer, target],
                demandes_associees__passenger__in=[viewer, target],
                demandes_associees__status='ACCEPTEE',
                date_trajet__gte=now().date()
            ).exists()
            return match
        except:
            return False
    
    @database_sync_to_async
    def trip_still_active(self):
        """
        Vérifie si un trajet en commun est encore valide entre viewer et target."""
        try:
            offer = RideOffer.objects.filter(
                driver__in=[self.viewer, self.target_user_id],
                demandes_associees__passenger__in=[self.viewer, self.target_user_id],
                demandes_associees__status='ACCEPTEE',
            ).order_by('-date_trajet').first()

            if not offer:
                return False

            now_time = timezone.now()
            trip_date = offer.date_trajet
            trip_end_time = timezone.make_aware(
                timezone.datetime.combine(trip_date, offer.end_time)
        )

        # On arrête le tracking si la fin du trajet est passée ou statut changé
            return trip_end_time >= now_time and offer.status == "ACTIF"
        except:
            return False
    @database_sync_to_async
    def get_viewer_position(self):
        try:
            viewer_tracking = TrackingGPS.objects.get(user=self.viewer)
            return viewer_tracking.last_latitude, viewer_tracking.last_longitude
        except TrackingGPS.DoesNotExist:
            return None, None

    async def calculate_eta_for_viewer(self, target_lat, target_lon):
        viewer_lat, viewer_lon = await self.get_viewer_position()
        if not viewer_lat or not viewer_lon:
            return None

        try:
            url = f"http://router.project-osrm.org/route/v1/driving/{viewer_lon},{viewer_lat};{target_lon},{target_lat}?overview=false"
            headers = {"User-Agent": "ifri-comotorage/1.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            route = data["routes"][0]
            return {
                "distance_km": round(route["distance"] / 1000, 2),
                "duration_minutes": round(route["duration"] / 60)
            }
        except:
            return None
