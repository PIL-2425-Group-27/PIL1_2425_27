from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    """Serializer for displaying user identity in conversations"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'photo_profile']


class MessageSimpleSerializer(serializers.ModelSerializer):
    """Simplified message serializer for conversation lists"""
    sender = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'content', 'message_type', 'timestamp', 
            'is_read', 'delivery_status', 'sender'
        ]


class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for conversation list view"""
    user1 = UserSimpleSerializer(read_only=True)
    user2 = UserSimpleSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'user1', 'user2', 'other_participant',
            'created_at', 'updated_at', 'last_message', 
            'unread_count', 'is_active'
        ]

    def get_last_message(self, obj):
        """Get the last message in the conversation"""
        last_message = obj.last_message
        if last_message:
            return MessageSimpleSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        """Get unread message count for current user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.unread_count_for_user(request.user)
        return 0

    def get_other_participant(self, obj):
        """Get the other participant (not the current user)"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other_user = obj.get_other_participant(request.user)
            if other_user:
                return UserSimpleSerializer(other_user).data
        return None


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Detailed conversation serializer"""
    user1 = UserSimpleSerializer(read_only=True)
    user2 = UserSimpleSerializer(read_only=True)
    participants = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'user1', 'user2', 'participants',
            'title', 'created_at', 'updated_at', 
            'is_active', 'messages_count'
        ]

    def get_participants(self, obj):
        return UserSimpleSerializer(obj.participants(), many=True).data

    def get_messages_count(self, obj):
        return obj.messages.count()


class MessageReplySerializer(serializers.ModelSerializer):
    """Serializer for replied-to messages"""
    sender = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'message_type', 'timestamp', 'sender']


class MessageSerializer(serializers.ModelSerializer):
    """Complete message serializer"""
    sender = UserSimpleSerializer(read_only=True)
    receiver = UserSimpleSerializer(read_only=True)
    reply_to = MessageReplySerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'receiver',
            'content', 'audio_file', 'image_file', 'file_attachment',
            'message_type', 'is_read', 'read_at', 'delivered_at',
            'delivery_status', 'timestamp', 'reply_to', 'replies_count',
            'edited_at', 'is_edited', 'file_url'
        ]
        read_only_fields = [
            'id', 'timestamp', 'sender', 'receiver', 'is_read', 
            'read_at', 'delivered_at', 'delivery_status', 'edited_at', 
            'is_edited'
        ]

    def get_replies_count(self, obj):
        """Get count of replies to this message"""
        return obj.replies.count()

    def get_file_url(self, obj):
        """Get the appropriate file URL based on message type"""
        request = self.context.get('request')
        if not request:
            return None
            
        if obj.message_type == 'AUDIO' and obj.audio_file:
            return request.build_absolute_uri(obj.audio_file.url)
        elif obj.message_type == 'IMAGE' and obj.image_file:
            return request.build_absolute_uri(obj.image_file.url)
        elif obj.message_type == 'FILE' and obj.file_attachment:
            return request.build_absolute_uri(obj.file_attachment.url)
        return None

    def validate(self, data):
        """Validate message data based on type"""
        message_type = data.get("message_type", "TEXT")

        if message_type == "TEXT" and not data.get("content"):
            raise serializers.ValidationError({
                "content": "Le contenu du message texte est requis."
            })
        elif message_type == "AUDIO" and not data.get("audio_file"):
            raise serializers.ValidationError({
                "audio_file": "Le fichier audio est requis pour ce type de message."
            })
        elif message_type == "IMAGE" and not data.get("image_file"):
            raise serializers.ValidationError({
                "image_file": "Le fichier image est requis pour ce type de message."
            })
        elif message_type == "FILE" and not data.get("file_attachment"):
            raise serializers.ValidationError({
                "file_attachment": "Le fichier est requis pour ce type de message."
            })

        # Validate content length for text messages
        if message_type == "TEXT" and data.get("content"):
            content = data["content"].strip()
            if len(content) > 5000:  # Max 5000 characters
                raise serializers.ValidationError({
                    "content": "Le message est trop long (maximum 5000 caractères)."
                })
            data["content"] = content

        return data

    def create(self, validated_data):
        """Create message with automatic delivery status"""
        validated_data['delivery_status'] = 'SENT'
        return Message.objects.create(**validated_data)

'''def get_average_rating(self, obj):

        return obj.average_rating'''
class MessageUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating message content (editing)"""
    
    class Meta:
        model = Message
        fields = ['content']

    def validate_content(self, value):
        """Validate content for editing"""
        if not value or not value.strip():
            raise serializers.ValidationError("Le contenu ne peut pas être vide.")
        
        if len(value.strip()) > 5000:
            raise serializers.ValidationError("Le message est trop long (maximum 5000 caractères).")
            
        return value.strip()

    def update(self, instance, validated_data):
        """Update message content and mark as edited"""
        if instance.message_type != 'TEXT':
            raise serializers.ValidationError("Seuls les messages texte peuvent être modifiés.")
        
        instance.edit_content(validated_data['content'])
        return instance


class ConversationCreateSerializer(serializers.Serializer):
    """Serializer for creating new conversations"""
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        """Validate that the user exists and is not the current user"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Utilisateur non authentifié.")

        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")

        if user == request.user:
            raise serializers.ValidationError("Vous ne pouvez pas créer une conversation avec vous-même.")

        return value

    def create(self, validated_data):
        """Create or get existing conversation"""
        request = self.context['request']
        user1 = request.user
        user2 = User.objects.get(id=validated_data['user_id'])

        # Try to get existing conversation
        conversation = Conversation.objects.between_users(user1, user2)
        
        if not conversation:
            # Create new conversation
            conversation = Conversation.objects.create(user1=user1, user2=user2)

        return conversation


class MessageReadStatusSerializer(serializers.Serializer):
    """Serializer for marking messages as read"""
    message_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        help_text="List of message IDs to mark as read (optional)"
    )
    conversation_id = serializers.IntegerField(
        required=False,
        help_text="Conversation ID to mark all messages as read (optional)"
    )

    def validate(self, data):
        """Ensure at least one field is provided"""
        if not data.get('message_ids') and not data.get('conversation_id'):
            raise serializers.ValidationError(
                "Soit message_ids soit conversation_id doit être fourni."
            )
        return data