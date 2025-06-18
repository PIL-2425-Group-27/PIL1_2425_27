from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db.models import Q, Max
import uuid

class ConversationManager(models.Manager):
    def for_user(self, user):
        """Get all conversations for a specific user"""
        return self.filter(Q(user1=user) | Q(user2=user)).distinct()
    
    def between_users(self, user1, user2):
        """Get conversation between two specific users"""
        return self.filter(
            (Q(user1=user1) & Q(user2=user2)) |
            (Q(user1=user2) & Q(user2=user1))
        ).first()
    
    def with_last_message(self):
        """Annotate conversations with last message timestamp for efficient ordering"""
        return self.annotate(
            last_message_time=Max('messages__timestamp')
        ).order_by('-last_message_time')

class Conversation(models.Model):
    """
    Conversation entre deux utilisateurs
    """
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='conversations_started', 
        on_delete=models.CASCADE,
        db_index=True  # Add index for performance
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='conversations_received', 
        on_delete=models.CASCADE,
        db_index=True  # Add index for performance
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    
    # Optional: Add a flag to indicate if conversation is active
    is_active = models.BooleanField(default=True)
    
    # Optional: Add conversation title for group chats in the future
    title = models.CharField(max_length=255, blank=True, null=True)

    objects = ConversationManager()

    class Meta:
        unique_together = ('user1', 'user2')
        indexes = [
            models.Index(fields=['user1', 'user2']),
            models.Index(fields=['-updated_at']),
        ]

    def __str__(self):
        return f"Conversation entre {self.user1} et {self.user2}"

    def participants(self):
        """Return list of conversation participants"""
        return [self.user1, self.user2]
    
    def get_other_participant(self, user):
        """Get the other participant in the conversation"""
        if user == self.user1:
            return self.user2
        elif user == self.user2:
            return self.user1
        return None
    
    @property
    def last_message(self):
        """Get the last message in the conversation"""
        return self.messages.select_related('sender', 'receiver').order_by('-timestamp').first()
    
    def unread_count_for_user(self, user):
        """Get count of unread messages for a specific user"""
        return self.messages.filter(receiver=user, is_read=False).count()
    
    def mark_all_as_read_for_user(self, user):
        """Mark all messages as read for a specific user"""
        updated_count = self.messages.filter(
            receiver=user, 
            is_read=False
        ).update(is_read=True, read_at=now())
        return updated_count

    def clean(self):
        """Validate that users are different"""
        if self.user1 == self.user2:
            raise ValidationError("Un utilisateur ne peut pas avoir une conversation avec lui-même.")

    def save(self, *args, **kwargs):
        # Ensure user1.id < user2.id for consistency
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        
        self.full_clean()  # Run validation
        super().save(*args, **kwargs)

class MessageManager(models.Manager):
    def unread_for_user(self, user):
        """Get all unread messages for a user"""
        return self.filter(receiver=user, is_read=False)
    
    def in_conversation(self, conversation):
        """Get messages in a specific conversation with related data"""
        return self.filter(conversation=conversation).select_related(
            'sender', 'receiver', 'conversation'
        ).order_by('timestamp')

class Message(models.Model):
    """
    Message texte ou audio entre deux utilisateurs
    """
    MESSAGE_TYPES = [
        ('TEXT', 'Texte'),
        ('AUDIO', 'Audio'),
        ('IMAGE', 'Image'),  # Future support for images
        ('FILE', 'Fichier'),  # Future support for files
    ]
    
    DELIVERY_STATUS = [
        ('SENT', 'Envoyé'),
        ('DELIVERED', 'Livré'),
        ('READ', 'Lu'),
        ('FAILED', 'Échec'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages',
        db_index=True
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages',
        db_index=True
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_messages',
        db_index=True
    )

    content = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='chat/audio/%Y/%m/', blank=True, null=True)
    image_file = models.ImageField(upload_to='chat/images/%Y/%m/', blank=True, null=True)
    file_attachment = models.FileField(upload_to='chat/files/%Y/%m/', blank=True, null=True)
    
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='TEXT')
    
    # Enhanced read status
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Message status
    delivery_status = models.CharField(
        max_length=10, 
        choices=DELIVERY_STATUS, 
        default='SENT',
        db_index=True
    )
    
    timestamp = models.DateTimeField(default=now, db_index=True)
    
    # Optional: Reply to another message
    reply_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='replies'
    )
    
    # Optional: Message editing
    edited_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)

    objects = MessageManager()

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['conversation', '-timestamp']),
            models.Index(fields=['receiver', 'is_read']),
            models.Index(fields=['sender', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]

    def __str__(self):
        content_preview = (self.content[:30] + '...') if self.content and len(self.content) > 30 else self.content
        return f"{self.sender} → {self.receiver}: {content_preview} ({self.message_type})"

    def clean(self):
        """Validate message content based on type"""
        if self.message_type == 'TEXT' and not self.content:
            raise ValidationError("Un message texte doit avoir du contenu.")
        if self.message_type == 'AUDIO' and not self.audio_file:
            raise ValidationError("Un message audio doit contenir un fichier audio.")
        if self.message_type == 'IMAGE' and not self.image_file:
            raise ValidationError("Un message image doit contenir un fichier image.")
        if self.message_type == 'FILE' and not self.file_attachment:
            raise ValidationError("Un message fichier doit contenir un fichier.")
        
        # Validate that sender and receiver are in the conversation
        if self.conversation and self.sender not in self.conversation.participants():
            raise ValidationError("L'expéditeur doit être un participant de la conversation.")
        if self.conversation and self.receiver not in self.conversation.participants():
            raise ValidationError("Le destinataire doit être un participant de la conversation.")

    def mark_as_read(self):
        """Mark message as read and update delivery status"""
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.delivery_status = 'READ'
            self.save(update_fields=['is_read', 'read_at', 'delivery_status'])
            return True
        return False
    
    def mark_as_delivered(self):
        """Mark message as delivered"""
        if self.delivery_status == 'SENT':
            self.delivered_at = now()
            self.delivery_status = 'DELIVERED'
            self.save(update_fields=['delivered_at', 'delivery_status'])
            return True
        return False
    
    def edit_content(self, new_content):
        """Edit message content (only for text messages)"""
        if self.message_type != 'TEXT':
            raise ValidationError("Seuls les messages texte peuvent être modifiés.")
        
        self.content = new_content
        self.edited_at = now()
        self.is_edited = True
        self.save(update_fields=['content', 'edited_at', 'is_edited'])
    
    @property
    def is_reply(self):
        """Check if this message is a reply to another message"""
        return self.reply_to is not None
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation
        super().save(*args, **kwargs)
        
        # Update conversation's updated_at timestamp
        self.conversation.updated_at = self.timestamp
        self.conversation.save(update_fields=['updated_at'])