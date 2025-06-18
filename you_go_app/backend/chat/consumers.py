import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings
from .models import Conversation, Message
from .serializers import MessageSerializer
from notifications.utils import create_notification
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # First authenticate the user
        self.user = await self.get_user_from_token()
        if self.user is None or self.user.is_anonymous:
            await self.close(code=4001)  # Custom close code for authentication failure
            return

        # Add user to their personal room for direct messages
        self.user_room_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_room_name, self.channel_name)
        
        # Initialize conversation-specific rooms list
        self.conversation_rooms = set()
        
        await self.accept()
        logger.info(f"User {self.user.id} connected to chat")

    async def disconnect(self, close_code):
        # Leave user room
        if hasattr(self, 'user_room_name'):
            await self.channel_layer.group_discard(self.user_room_name, self.channel_name)
        
        # Leave all conversation rooms
        if hasattr(self, 'conversation_rooms'):
            for room in self.conversation_rooms:
                await self.channel_layer.group_discard(room, self.channel_name)
        
        logger.info(f"User {getattr(self, 'user', {}).get('id', 'unknown')} disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            message_type = data.get("type")
            action = data.get('action')
            
            # Handle ping/pong for connection health
            if message_type == "ping":
                await self.send(text_data=json.dumps({"type": "pong"}))
                return
            
            # Handle different actions
            if action == 'send_message':
                await self.send_message(data)
            elif action == 'join_conversation':
                await self.join_conversation(data)
            elif action == 'mark_as_read':
                await self.mark_messages_as_read(data)
            else:
                await self.send_error("Unknown action")
                
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")
            await self.send_error("Internal server error")

    async def join_conversation(self, data):
        """Join a specific conversation room"""
        conversation_id = data.get("conversation_id")
        if not conversation_id:
            await self.send_error("Conversation ID required")
            return
            
        conversation = await self.get_conversation(conversation_id)
        if conversation is None:
            await self.send_error("Conversation not found or access denied")
            return
            
        # Join conversation room
        room_name = f"conversation_{conversation_id}"
        await self.channel_layer.group_add(room_name, self.channel_name)
        self.conversation_rooms.add(room_name)
        
        await self.send_success("Joined conversation")

    async def send_message(self, data):
        conversation_id = data.get("conversation_id")
        content = data.get("content", "").strip()
        message_type = data.get("message_type", "TEXT")

        # Validate input
        if not conversation_id:
            await self.send_error("Conversation ID required")
            return
            
        if not content and message_type == "TEXT":
            await self.send_error("Message content required")
            return

        conversation = await self.get_conversation(conversation_id)
        if conversation is None:
            await self.send_error("Conversation not found or access denied")
            return

        # Determine receiver
        receiver = conversation.user2 if self.user.id == conversation.user1.id else conversation.user1

        # Create message
        message = await self.create_message(conversation, self.user, receiver, content, message_type)
        if message is None:
            await self.send_error("Failed to create message")
            return

        # Serialize message
        serialized = await self.serialize_message(message)

        # Send to conversation room (all participants)
        conversation_room = f"conversation_{conversation_id}"
        await self.channel_layer.group_send(
            conversation_room,
            {
                'type': 'chat_message',
                'message': serialized
            }
        )

        # Also send to receiver's personal room (for notifications when not in conversation)
        await self.channel_layer.group_send(
            f"user_{receiver.id}",
            {
                'type': 'new_message_notification',
                'message': serialized
            }
        )

        # Send confirmation to sender
        await self.send_success("Message sent", {"message": serialized})

    async def mark_messages_as_read(self, data):
        """Mark messages in a conversation as read"""
        conversation_id = data.get("conversation_id")
        if not conversation_id:
            await self.send_error("Conversation ID required")
            return
            
        conversation = await self.get_conversation(conversation_id)
        if conversation is None:
            await self.send_error("Conversation not found or access denied")
            return
            
        await self.mark_conversation_messages_as_read(conversation)
        await self.send_success("Messages marked as read")

    async def chat_message(self, event):
        """Handle chat message from group"""
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event['message']
        }))

    async def new_message_notification(self, event):
        """Handle new message notification"""
        await self.send(text_data=json.dumps({
            "type": "new_message_notification", 
            "message": event['message']
        }))

    async def send_error(self, message):
        """Send error message to client"""
        await self.send(text_data=json.dumps({
            "type": "error",
            "message": message
        }))

    async def send_success(self, message, data=None):
        """Send success message to client"""
        response = {
            "type": "success",
            "message": message
        }
        if data:
            response.update(data)
        await self.send(text_data=json.dumps(response))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        """Get conversation if user has access"""
        try:
            conversation = Conversation.objects.select_related('user1', 'user2').get(id=conversation_id)
            if self.user not in [conversation.user1, conversation.user2]:
                return None
            return conversation
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, conversation, sender, receiver, content, message_type):
        """Create a new message and notification"""
        try:
            message = Message.objects.create(
                conversation=conversation,
                sender=sender,
                receiver=receiver,
                content=content,
                message_type=message_type
            )
            
            # Create notification for receiver
            create_notification(
                user=receiver,
                notif_type="MESSAGE",
                title=f"📩 Nouveau message de {sender.first_name or sender.username}",
                message=content[:50] + "..." if len(content) > 50 else content,
                data={"conversation_id": conversation.id}
            )
            
            return message
        except Exception as e:
            logger.error(f"Error creating message: {str(e)}")
            return None

    @database_sync_to_async
    def mark_conversation_messages_as_read(self, conversation):
        """Mark all unread messages in conversation as read"""
        from django.utils import timezone
        Message.objects.filter(
            conversation=conversation,
            receiver=self.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())

    @database_sync_to_async
    def serialize_message(self, message):
        """Serialize message for JSON response"""
        return MessageSerializer(message).data

    async def get_user_from_token(self):
        """Extract and validate user from JWT token"""
        try:
            query_string = parse_qs(self.scope["query_string"].decode())
            token_list = query_string.get("token")
            
            if not token_list:
                logger.warning("No token provided in WebSocket connection")
                return AnonymousUser()
                
            token = token_list[0]
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_data.get("user_id")
            
            if not user_id:
                logger.warning("No user_id in token")
                return AnonymousUser()
                
            user = await database_sync_to_async(User.objects.get)(id=user_id)
            return user
            
        except jwt_decode.ExpiredSignatureError:
            logger.warning("Expired token in WebSocket connection")
            return AnonymousUser()
        except jwt_decode.InvalidTokenError:
            logger.warning("Invalid token in WebSocket connection")
            return AnonymousUser()
        except User.DoesNotExist:
            logger.warning(f"User with id {user_id} not found")
            return AnonymousUser()
        except Exception as e:
            logger.error(f"Error getting user from token: {str(e)}")
            return AnonymousUser()

# Frontend JavaScript example:
# const socket = new WebSocket('ws://yourserver.com/chat?
