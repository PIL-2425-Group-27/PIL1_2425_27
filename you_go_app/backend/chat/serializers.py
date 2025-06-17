from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    """ Utilisé pour afficher l'identité des participants """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'photo_profile']


class ConversationSerializer(serializers.ModelSerializer):
    user1 = UserSimpleSerializer(read_only=True)
    user2 = UserSimpleSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'user1', 'user2', 'created_at', 'updated_at', 'last_message']

    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return MessageSerializer(last).data
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSimpleSerializer(read_only=True)
    receiver = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'receiver',
            'content', 'audio_file', 'message_type',
            'is_read', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp', 'sender', 'receiver', 'is_read']

    def validate(self, data):
        msg_type = data.get("message_type")

        if msg_type == "TEXT" and not data.get("content"):
            raise serializers.ValidationError("Le contenu du message texte est vide.")
        if msg_type == "AUDIO" and not data.get("audio_file"):
            raise serializers.ValidationError("Le fichier audio est requis pour ce type de message.")
        return data

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
