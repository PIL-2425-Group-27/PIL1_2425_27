from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q, Count, Max, Prefetch
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Conversation, Message
from .serializers import ConversationListSerializer, MessageSerializer
from notifications.utils import create_notification
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class ConversationListView(generics.ListAPIView):
    """
    Liste des conversations de l'utilisateur connecté avec optimisations
    """
    serializer_class = ConversationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).select_related(
            'user1', 'user2'
        ).prefetch_related(
            Prefetch(
                'messages',
                queryset=Message.objects.select_related('sender', 'receiver').order_by('-created_at')[:1]
            )
        ).annotate(
            message_count=Count('messages'),
            unread_count=Count('messages', filter=Q(messages__receiver=user, messages__is_read=False)),
            last_message_time=Max('messages__created_at')
        ).order_by('-last_message_time', '-updated_at')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'conversations': serializer.data,
                'count': queryset.count()
            })
        except Exception as e:
            logger.error(f"Error fetching conversations for user {request.user.id}: {str(e)}")
            return Response(
                {'error': 'Erreur lors de la récupération des conversations'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StartConversationView(generics.CreateAPIView):
    """
    Crée une nouvelle conversation 1-à-1 si elle n'existe pas déjà
    """
    serializer_class = ConversationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")
        
        # Validation
        if not other_user_id:
            return Response(
                {"error": "ID utilisateur requis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier qu'on ne crée pas une conversation avec soi-même
        if str(other_user_id) == str(request.user.id):
            return Response(
                {"error": "Impossible de créer une conversation avec soi-même"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        
        # Chercher une conversation existante (dans les deux sens)
        conversation = Conversation.objects.filter(
            (Q(user1=user) & Q(user2=other_user)) |
            (Q(user1=other_user) & Q(user2=user))
        ).select_related('user1', 'user2').first()

        created = False
        if not conversation:
            # Créer une nouvelle conversation
            conversation = Conversation.objects.create(
                user1=user, 
                user2=other_user
            )
            created = True

        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response({
            'conversation': ConversationListSerializer(conversation).data,
            'created': created
        }, status=response_status)


class MessageListView(generics.ListAPIView):
    """
    Liste paginée des messages d'une conversation avec marquage automatique comme lu
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        
        if not conversation_id:
            return Message.objects.none()
            
        conversation = get_object_or_404(
            Conversation.objects.select_related('user1', 'user2'), 
            id=conversation_id
        )

        # Vérifier l'accès
        if self.request.user not in [conversation.user1, conversation.user2]:
            return Message.objects.none()

        # Marquer les messages reçus comme lus
        self._mark_messages_as_read(conversation)
        
        return conversation.messages.select_related(
            'sender', 'receiver'
        ).order_by('-created_at')

    def _mark_messages_as_read(self, conversation):
        """Marquer les messages non lus comme lus"""
        Message.objects.filter(
            conversation=conversation,
            receiver=self.request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            # Pagination
            page_size = int(request.query_params.get('page_size', 50))
            page_size = min(page_size, 100)  # Limite maximale
            
            paginator = Paginator(queryset, page_size)
            page_number = request.query_params.get('page', 1)
            page_obj = paginator.get_page(page_number)
            
            serializer = self.get_serializer(page_obj.object_list, many=True)
            
            return Response({
                'messages': serializer.data,
                'pagination': {
                    'current_page': page_obj.number,
                    'total_pages': paginator.num_pages,
                    'total_messages': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                }
            })
        except Exception as e:
            logger.error(f"Error fetching messages: {str(e)}")
            return Response(
                {'error': 'Erreur lors de la récupération des messages'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendMessageView(generics.CreateAPIView):
    """
    Envoi d'un message texte ou audio dans une conversation existante
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id")
        content = request.data.get("content", "").strip()
        audio_file = request.FILES.get("audio_file")
        message_type = request.data.get("message_type", "TEXT")

        # Validation
        if not conversation_id:
            return Response(
                {"error": "ID de conversation requis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if message_type == "TEXT" and not content:
            return Response(
                {"error": "Contenu du message requis pour les messages texte"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if message_type == "AUDIO" and not audio_file:
            return Response(
                {"error": "Fichier audio requis pour les messages audio"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = get_object_or_404(
                Conversation.objects.select_related('user1', 'user2'), 
                id=conversation_id
            )
        except Exception:
            return Response(
                {"error": "Conversation introuvable"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier l'accès
        if request.user not in [conversation.user1, conversation.user2]:
            return Response(
                {"error": "Non autorisé"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Déterminer le destinataire
        receiver = conversation.user2 if request.user == conversation.user1 else conversation.user1

        try:
            # Créer le message
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                receiver=receiver,
                content=content,
                audio_file=audio_file,
                message_type=message_type
            )

            # Créer la notification
            self._create_notification(request.user, receiver, content, conversation.id)

            # Mettre à jour le timestamp de la conversation
            conversation.updated_at = timezone.now()
            conversation.save(update_fields=['updated_at'])

            return Response(
                MessageSerializer(message).data, 
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error(f"Error creating message: {str(e)}")
            return Response(
                {"error": "Erreur lors de l'envoi du message"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _create_notification(self, sender, receiver, content, conversation_id):
        """Créer une notification pour le destinataire"""
        try:
            notification_content = content[:50] + "..." if len(content) > 50 else content
            create_notification(
                user=receiver,
                notif_type="MESSAGE",
                title=f"📩 Nouveau message de {sender.first_name or sender.username}",
                message=notification_content,
                data={"conversation_id": str(conversation_id)}
            )
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}")


class MarkMessagesAsReadView(generics.GenericAPIView):
    """
    Marque tous les messages d'une conversation comme lus
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        try:
            conversation = get_object_or_404(
                Conversation.objects.select_related('user1', 'user2'), 
                id=conversation_id
            )
        except Exception:
            return Response(
                {"error": "Conversation introuvable"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier l'accès
        if request.user not in [conversation.user1, conversation.user2]:
            return Response(
                {"error": "Non autorisé"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Marquer les messages comme lus
            updated_count = Message.objects.filter(
                conversation=conversation,
                receiver=request.user,
                is_read=False
            ).update(is_read=True, read_at=timezone.now())

            return Response({
                "status": "Messages marqués comme lus",
                "updated_count": updated_count
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error marking messages as read: {str(e)}")
            return Response(
                {"error": "Erreur lors du marquage des messages"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def conversation_stats(request, conversation_id):
    """
    Statistiques d'une conversation (nombre de messages, messages non lus, etc.)
    """
    try:
        conversation = get_object_or_404(
            Conversation.objects.select_related('user1', 'user2'), 
            id=conversation_id
        )
        
        # Vérifier l'accès
        if request.user not in [conversation.user1, conversation.user2]:
            return Response(
                {"error": "Non autorisé"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        stats = {
            'total_messages': conversation.messages.count(),
            'unread_messages': conversation.messages.filter(
                receiver=request.user, 
                is_read=False
            ).count(),
            'last_message': None,
            'conversation_started': conversation.created_at,
            'last_activity': conversation.updated_at
        }

        # Dernier message
        last_message = conversation.messages.select_related('sender').first()
        if last_message:
            stats['last_message'] = {
                'content': last_message.content[:100] + "..." if len(last_message.content) > 100 else last_message.content,
                'sender': last_message.sender.username,
                'created_at': last_message.created_at,
                'message_type': last_message.message_type
            }

        return Response(stats)

    except Exception as e:
        logger.error(f"Error getting conversation stats: {str(e)}")
        return Response(
            {"error": "Erreur lors de la récupération des statistiques"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )