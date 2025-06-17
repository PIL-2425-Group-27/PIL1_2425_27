# notifications/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            self.user = user
            self.group_name = f"user_{user.id}_notifications"

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # On retire l’utilisateur du groupe WebSocket
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Reçoit les notifications envoyées depuis utils.py ou les signaux
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "notification": event["notification"]
    }))