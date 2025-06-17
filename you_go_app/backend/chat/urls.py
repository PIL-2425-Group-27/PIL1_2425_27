from django.urls import path
from . import views

urlpatterns = [
    # 📥 Créer une conversation ou récupérer une existante
    path('start/', views.StartConversationView.as_view(), name='start-conversation'),

    # 🗂️ Voir toutes mes conversations
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),

    # 💬 Liste des messages d’une conversation
    path('conversations/messages/', views.MessageListView.as_view(), name='message-list'),

    # ✉️ Envoyer un message (texte ou audio)
    path('messages/send/', views.SendMessageView.as_view(), name='send-message'),
    # 📩 Marquer un message comme lu
    path('messages/mark-as-read/<uuid:message_id>/', views.MarkMessagesAsReadView.as_view(), name='mark-message-as-read'),
]
