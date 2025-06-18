from django.urls import path
from .views import (
    StartConversationView, 
    ConversationListView, 
    MessageListView, 
    SendMessageView, 
    MarkMessagesAsReadView,
    conversation_stats
)

app_name = 'chat'

urlpatterns = [
    # 🗂️ Voir toutes mes conversations
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    
    # 📥 Créer une conversation ou récupérer une existante
    path('conversations/start/', StartConversationView.as_view(), name='start-conversation'),
    
    # 💬 Liste des messages d'une conversation spécifique
    path('conversations/<uuid:conversation_id>/messages/', MessageListView.as_view(), name='message-list'),
    
    # 📊 Statistiques d'une conversation
    path('conversations/<uuid:conversation_id>/stats/', conversation_stats, name='conversation-stats'),
    
    # 📩 Marquer tous les messages d'une conversation comme lus
    path('conversations/<uuid:conversation_id>/mark-as-read/', MarkMessagesAsReadView.as_view(), name='mark-messages-as-read'),
    
    # ✉️ Envoyer un message (texte ou audio)
    path('messages/send/', SendMessageView.as_view(), name='send-message'),
]

# API Documentation for frontend developers:
"""
Chat API Endpoints:

1. GET /api/chat/conversations/
   - Liste toutes les conversations de l'utilisateur
   - Response: {conversations: [...], count: int}

2. POST /api/chat/conversations/start/
   - Body: {user_id: uuid}
   - Crée ou récupère une conversation avec un utilisateur
   - Response: {conversation: {...}, created: boolean}

3. GET /api/chat/conversations/{conversation_id}/messages/?page=1&page_size=50
   - Liste les messages d'une conversation (paginé)
   - Response: {messages: [...], pagination: {...}}

4. GET /api/chat/conversations/{conversation_id}/stats/
   - Statistiques d'une conversation
   - Response: {total_messages: int, unread_messages: int, ...}

5. POST /api/chat/conversations/{conversation_id}/mark-as-read/
   - Marque tous les messages de la conversation comme lus
   - Response: {status: string, updated_count: int}

6. POST /api/chat/messages/send/
   - Body: {conversation_id: uuid, content: string, message_type: "TEXT"|"AUDIO"}
   - Pour les messages audio: ajouter audio_file dans FormData
   - Response: message object

"""