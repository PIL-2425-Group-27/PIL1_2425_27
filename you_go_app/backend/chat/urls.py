from django.urls import path
from .views import StartConversationView, ConversationListView, MessageListView, SendMessageView, MarkMessagesAsReadView

urlpatterns = [
    # 📥 Créer une conversation ou récupérer une existante
    path('start/', StartConversationView.as_view(), name='start-conversation'),

    # 🗂️ Voir toutes mes conversations
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),

    # 💬 Liste des messages d’une conversation
    path('conversations/messages/', MessageListView.as_view(), name='message-list'),

    # ✉️ Envoyer un message (texte ou audio)
    path('messages/send/', SendMessageView.as_view(), name='send-message'),
    # 📩 Marquer un message comme lu
    path('messages/mark-as-read/<uuid:message_id>/', MarkMessagesAsReadView.as_view(), name='mark-message-as-read'),
]
