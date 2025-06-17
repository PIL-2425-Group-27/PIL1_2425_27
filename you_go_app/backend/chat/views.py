from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ConversationListView(generics.ListAPIView):
    """
    Liste des conversations de l'utilisateur connecté
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-updated_at')


class StartConversationView(generics.CreateAPIView):
    """
    Crée une nouvelle conversation 1-à-1 si elle n'existe pas déjà
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")
        if not other_user_id:
            return Response({"error": "ID utilisateur requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        conversation = Conversation.objects.filter(
            (Q(user1=user) & Q(user2=other_user)) |
            (Q(user1=other_user) & Q(user2=user))
        ).first()

        if not conversation:
            conversation = Conversation.objects.create(user1=user, user2=other_user)

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageListView(generics.ListAPIView):
    """
    Liste des messages d'une conversation
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in [conversation.user1, conversation.user2]:
            return Message.objects.none()
          # 🔄 Marquer les messages reçus comme lus
        Message.objects.filter(
            conversation=conversation,
            receiver=self.request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return conversation.messages.all()


class SendMessageView(generics.CreateAPIView):
    """
    Envoi d'un message texte ou audio dans une conversation existante
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        content = request.data.get("content")
        audio_file = request.FILES.get("audio_file")
        message_type = request.data.get("message_type", "TEXT")

        conversation = get_object_or_404(Conversation, id=conversation_id)

        if request.user not in [conversation.user1, conversation.user2]:
            return Response({"error": "Non autorisé"}, status=status.HTTP_403_FORBIDDEN)

        receiver = conversation.user2 if request.user == conversation.user1 else conversation.user1

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            receiver=receiver,
            content=content,
            audio_file=audio_file,
            message_type=message_type
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
class MarkMessagesAsReadView(generics.UpdateAPIView):
    """
    Marque tous les messages d'une conversation comme lus
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if request.user not in [conversation.user1, conversation.user2]:
            return Response({"error": "Non autorisé"}, status=status.HTTP_403_FORBIDDEN)

        # Marquer les messages comme lus
        Message.objects.filter(
            conversation=conversation,
            receiver=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())

        return Response({"status": "Messages marqués comme lus"}, status=status.HTTP_200_OK)