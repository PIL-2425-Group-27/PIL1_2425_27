import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings
from .models import Conversation, Message
from .serializers import MessageSerializer
from notifications.utils import create_notification

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        user1, user2 = sorted([self.scope["user"], self.other_user], key=lambda x: x.id)
        self.conversation, _ = Conversation.objects.get_or_create(user1=user1, user2=user2)

        self.user = await self.get_user_from_token()
        if self.user is None or self.user.is_anonymous:
            await self.close()
        else:
            self.room_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data.get('action')
        if data.get("type") == "ping":
            await self.send(text_data=json.dumps({"type": "pong"}))
        
            return
        if action == 'send_message':
            await self.send_message(data)

    async def send_message(self, data):
        conversation_id = data.get("conversation")
        content = data.get("content", "")
        message_type = data.get("message_type", "TEXT")

        conversation = await self.get_conversation(conversation_id)
        if conversation is None:
            await self.send_json({"error": "Conversation introuvable"})
            return

        receiver = conversation.user2 if self.user == conversation.user1 else conversation.user1

        message = await self.create_message(conversation, self.user, receiver, content, message_type)

        serialized = await self.serialize_message(message)

        # Envoie au receveur
        await self.channel_layer.group_send(
            f"user_{receiver.id}",
            {
                'type': 'chat_message',
                'message': serialized
            }
        )

        # Envoie au sender aussi (pour mise à jour instantanée côté frontend)
        await self.send(text_data=json.dumps({
            "message": serialized
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event['message']
        }))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        try:
            conv = Conversation.objects.get(id=conversation_id)
            if self.user not in [conv.user1, conv.user2]:
                return None
            return conv
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, conversation, sender, receiver, content, message_type):
        return Message.objects.create(
            conversation=conversation,
            sender=sender,
            receiver=receiver,
            content=content,
            message_type=message_type
        )
        create_notification(
            user=receiver,  # la personne qui reçoit le message
            notif_type="MESSAGE",
            title=f"📩 Nouveau message de {sender.first_name}",
            message=content,
            data={"conversation_id": conversation.id}
)
    

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

    async def get_user_from_token(self):
        try:
            query_string = parse_qs(self.scope["query_string"].decode())
            token = query_string.get("token")[0]
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_data.get("user_id")
            user = await database_sync_to_async(User.objects.get)(id=user_id)
            return user
        except Exception:
            return AnonymousUser()
# Example usage in a frontend JavaScript file:
#const socket = new WebSocket(`ws://localhost:8000/ws/chat/?token=${userAccessToken}`);
