'''import json
import tempfile
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from unittest.mock import patch, MagicMock
import asyncio
from django.utils import timezone

from chat.models import Conversation, Message
from chat.consumers import ChatConsumer

User = get_user_model()


class ChatModelTests(TestCase):
    """Tests pour les modèles Chat"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        
    def test_conversation_creation(self):
        """Test création d'une conversation"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        self.assertEqual(conversation.user1, self.user1)
        self.assertEqual(conversation.user2, self.user2)
        self.assertIsNotNone(conversation.id)
        self.assertIsNotNone(conversation.created_at)
        
    def test_conversation_str_method(self):
        """Test méthode __str__ de Conversation"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        expected = f"Conversation between {self.user1.username} and {self.user2.username}"
        self.assertEqual(str(conversation), expected)
        
    def test_message_creation(self):
        """Test création d'un message"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        message = Message.objects.create(
            conversation=conversation,
            sender=self.user1,
            receiver=self.user2,
            content="Hello World!",
            message_type="TEXT"
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, "Hello World!")
        self.assertFalse(message.is_read)
        self.assertIsNone(message.read_at)
        
    def test_message_mark_as_read(self):
        """Test marquage d'un message comme lu"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        message = Message.objects.create(
            conversation=conversation,
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Marquer comme lu
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        
        self.assertTrue(message.is_read)
        self.assertIsNotNone(message.read_at)


class ChatAPITests(APITestCase):
    """Tests pour les APIs Chat"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='testpass123'
        )
        
        # Créer des tokens JWT
        self.token1 = str(RefreshToken.for_user(self.user1).access_token)
        self.token2 = str(RefreshToken.for_user(self.user2).access_token)
        
        self.client1 = APIClient()
        self.client1.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        
        self.client2 = APIClient()
        self.client2.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        
    def test_start_conversation_success(self):
        """Test démarrage d'une nouvelle conversation"""
        url = reverse('chat:start-conversation')
        data = {'user_id': str(self.user2.id)}
        
        response = self.client1.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['created'])
        self.assertIn('conversation', response.data)
        
        # Vérifier que la conversation existe en base
        conversation = Conversation.objects.get(id=response.data['conversation']['id'])
        self.assertIn(self.user1, [conversation.user1, conversation.user2])
        self.assertIn(self.user2, [conversation.user1, conversation.user2])
        
    def test_start_conversation_existing(self):
        """Test récupération d'une conversation existante"""
        # Créer une conversation existante
        existing_conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        url = reverse('chat:start-conversation')
        data = {'user_id': str(self.user2.id)}
        
        response = self.client1.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['created'])
        self.assertEqual(response.data['conversation']['id'], str(existing_conversation.id))
        
    def test_start_conversation_with_self(self):
        """Test erreur lors de création conversation avec soi-même"""
        url = reverse('chat:start-conversation')
        data = {'user_id': str(self.user1.id)}
        
        response = self.client1.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_start_conversation_user_not_found(self):
        """Test erreur utilisateur non trouvé"""
        url = reverse('chat:start-conversation')
        data = {'user_id': '12345678-1234-5678-9012-123456789012'}
        
        response = self.client1.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_conversation_list(self):
        """Test liste des conversations"""
        # Créer quelques conversations
        conv1 = Conversation.objects.create(user1=self.user1, user2=self.user2)
        conv2 = Conversation.objects.create(user1=self.user1, user2=self.user3)
        
        # Ajouter quelques messages
        Message.objects.create(
            conversation=conv1,
            sender=self.user2,
            receiver=self.user1,
            content="Hello from user2"
        )
        
        url = reverse('chat:conversation-list')
        response = self.client1.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('conversations', response.data)
        self.assertEqual(len(response.data['conversations']), 2)
        
    def test_send_message_success(self):
        """Test envoi d'un message réussi"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        url = reverse('chat:send-message')
        data = {
            'conversation_id': str(conversation.id),
            'content': 'Hello, this is a test message!',
            'message_type': 'TEXT'
        }
        
        with patch('chat.views.create_notification') as mock_notification:
            response = self.client1.post(url, data, format='json')
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], data['content'])
        self.assertEqual(response.data['sender'], str(self.user1.id))
        
        # Vérifier que le message existe en base
        message = Message.objects.get(id=response.data['id'])
        self.assertEqual(message.content, data['content'])
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        
        # Vérifier que la notification a été créée
        mock_notification.assert_called_once()
        
    def test_send_message_unauthorized(self):
        """Test envoi message dans conversation non autorisée"""
        # Créer une conversation entre user2 et user3
        conversation = Conversation.objects.create(
            user1=self.user2,
            user2=self.user3
        )
        
        url = reverse('chat:send-message')
        data = {
            'conversation_id': str(conversation.id),
            'content': 'Unauthorized message',
            'message_type': 'TEXT'
        }
        
        response = self.client1.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_send_empty_message(self):
        """Test envoi message vide"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        url = reverse('chat:send-message')
        data = {
            'conversation_id': str(conversation.id),
            'content': '',
            'message_type': 'TEXT'
        }
        
        response = self.client1.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_message_list(self):
        """Test récupération liste des messages"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        # Créer quelques messages
        for i in range(5):
            Message.objects.create(
                conversation=conversation,
                sender=self.user1 if i % 2 == 0 else self.user2,
                receiver=self.user2 if i % 2 == 0 else self.user1,
                content=f"Message {i}"
            )
            
        url = reverse('chat:message-list', kwargs={'conversation_id': conversation.id})
        response = self.client1.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('messages', response.data)
        self.assertEqual(len(response.data['messages']), 5)
        self.assertIn('pagination', response.data)
        
    def test_message_list_pagination(self):
        """Test pagination des messages"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        # Créer 25 messages
        for i in range(25):
            Message.objects.create(
                conversation=conversation,
                sender=self.user1,
                receiver=self.user2,
                content=f"Message {i}"
            )
            
        url = reverse('chat:message-list', kwargs={'conversation_id': conversation.id})
        response = self.client1.get(url, {'page': 1, 'page_size': 10})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['messages']), 10)
        self.assertEqual(response.data['pagination']['total_messages'], 25)
        self.assertEqual(response.data['pagination']['total_pages'], 3)
        
    def test_mark_messages_as_read(self):
        """Test marquage des messages comme lus"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        # Créer des messages non lus
        for i in range(3):
            Message.objects.create(
                conversation=conversation,
                sender=self.user2,
                receiver=self.user1,
                content=f"Unread message {i}"
            )
            
        url = reverse('chat:mark-messages-as-read', kwargs={'conversation_id': conversation.id})
        response = self.client1.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 3)
        
        # Vérifier que les messages sont marqués comme lus
        unread_count = Message.objects.filter(
            conversation=conversation,
            receiver=self.user1,
            is_read=False
        ).count()
        self.assertEqual(unread_count, 0)
        
    def test_conversation_stats(self):
        """Test statistiques de conversation"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        # Créer quelques messages
        Message.objects.create(
            conversation=conversation,
            sender=self.user2,
            receiver=self.user1,
            content="Unread message 1"
        )
        Message.objects.create(
            conversation=conversation,
            sender=self.user1,
            receiver=self.user2,
            content="Read message"
        )
        
        url = reverse('chat:conversation-stats', kwargs={'conversation_id': conversation.id})
        response = self.client1.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_messages'], 2)
        self.assertEqual(response.data['unread_messages'], 1)
        self.assertIn('last_message', response.data)
        
    def test_send_audio_message(self):
        """Test envoi d'un message audio"""
        conversation = Conversation.objects.create(
            user1=self.user1,
            user2=self.user2
        )
        
        # Créer un fichier audio factice
        audio_content = b"fake audio content"
        audio_file = SimpleUploadedFile(
            "test_audio.wav",
            audio_content,
            content_type="audio/wav"
        )
        
        url = reverse('chat:send-message')
        data = {
            'conversation_id': str(conversation.id),
            'message_type': 'AUDIO',
            'audio_file': audio_file
        }
        
        with patch('chat.views.create_notification'):
            response = self.client1.post(url, data, format='multipart')
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message_type'], 'AUDIO')
        
    def test_unauthorized_access(self):
        """Test accès non autorisé aux APIs"""
        client = APIClient()  # Client sans token
        
        url = reverse('chat:conversation-list')
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChatWebSocketTests(TransactionTestCase):
    """Tests pour le WebSocket ChatConsumer"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        
        # Créer un token JWT
        self.token = str(RefreshToken.for_user(self.user1).access_token)
        
    async def test_websocket_connection_success(self):
        """Test connexion WebSocket réussie"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/chat/?token={self.token}"
        )
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        await communicator.disconnect()
        
    async def test_websocket_connection_no_token(self):
        """Test connexion WebSocket sans token"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            "/ws/chat/"
        )
        
        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected)
        
    async def test_websocket_ping_pong(self):
        """Test ping/pong WebSocket"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/chat/?token={self.token}"
        )
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Envoyer ping
        await communicator.send_json_to({"type": "ping"})
        
        # Recevoir pong
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "pong")
        
        await communicator.disconnect()
        
    async def test_websocket_join_conversation(self):
        """Test rejoindre une conversation via WebSocket"""
        # Créer une conversation
        conversation = await database_sync_to_async(Conversation.objects.create)(
            user1=self.user1,
            user2=self.user2
        )
        
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/chat/?token={self.token}"
        )
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Rejoindre la conversation
        await communicator.send_json_to({
            "action": "join_conversation",
            "conversation_id": str(conversation.id)
        })
        
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "success")
        
        await communicator.disconnect()
        
    async def test_websocket_send_message(self):
        """Test envoi de message via WebSocket"""
        # Créer une conversation
        conversation = await database_sync_to_async(Conversation.objects.create)(
            user1=self.user1,
            user2=self.user2
        )
        
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/chat/?token={self.token}"
        )
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Rejoindre la conversation d'abord
        await communicator.send_json_to({
            "action": "join_conversation",
            "conversation_id": str(conversation.id)
        })
        await communicator.receive_json_from()  # Confirmation
        
        # Envoyer un message
        with patch('chat.consumers.create_notification'):
            await communicator.send_json_to({
                "action": "send_message",
                "conversation_id": str(conversation.id),
                "content": "Hello via WebSocket!",
                "message_type": "TEXT"
            })
        
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "success")
        self.assertIn("message", response)
        
        await communicator.disconnect()


class ChatIntegrationTests(TestCase):
    """Tests d'intégration pour le système de chat complet"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        
    def test_complete_chat_flow(self):
        """Test complet d'un flux de chat"""
        client1 = APIClient()
        client2 = APIClient()
        
        # Authentification
        token1 = str(RefreshToken.for_user(self.user1).access_token)
        token2 = str(RefreshToken.for_user(self.user2).access_token)
        
        client1.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        client2.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')
        
        # 1. User1 démarre une conversation avec User2
        start_url = reverse('chat:start-conversation')
        response = client1.post(start_url, {'user_id': str(self.user2.id)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        conversation_id = response.data['conversation']['id']
        
        # 2. User1 envoie un message
        send_url = reverse('chat:send-message')
        with patch('chat.views.create_notification'):
            response = client1.post(send_url, {
                'conversation_id': conversation_id,
                'content': 'Hello User2!',
                'message_type': 'TEXT'
            }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 3. User2 récupère ses conversations
        conv_list_url = reverse('chat:conversation-list')
        response = client2.get(conv_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['conversations']), 1)
        
        # 4. User2 récupère les messages de la conversation
        msg_list_url = reverse('chat:message-list', kwargs={'conversation_id': conversation_id})
        response = client2.get(msg_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['messages']), 1)
        self.assertEqual(response.data['messages'][0]['content'], 'Hello User2!')
        
        # 5. User2 répond
        with patch('chat.views.create_notification'):
            response = client2.post(send_url, {
                'conversation_id': conversation_id,
                'content': 'Hello User1!',
                'message_type': 'TEXT'
            }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 6. Vérifier que la conversation a maintenant 2 messages
        response = client1.get(msg_list_url)
        self.assertEqual(len(response.data['messages']), 2)


# Test runner personnalisé pour les tests WebSocket
def run_websocket_tests():
    """Fonction helper pour exécuter les tests WebSocket"""
    import asyncio
    
    async def run_tests():
        test_instance = ChatWebSocketTests()
        test_instance.setUp()
        
        await test_instance.test_websocket_connection_success()
        await test_instance.test_websocket_ping_pong()
        await test_instance.test_websocket_join_conversation()
        await test_instance.test_websocket_send_message()
        
        print("Tous les tests WebSocket sont passés!")
    
    asyncio.run(run_tests())


if __name__ == '__main__':
    # Pour exécuter les tests WebSocket séparément
    run_websocket_tests()'''