from django.db import models
from django.conf import settings
from django.utils.timezone import now
import uuid

class ConversationManager(models.Manager):
    def for_user(self, user):
        return self.filter(models.Q(user1=user) | models.Q(user2=user)).distinct()

class Conversation(models.Model):
    """
    Conversation entre deux utilisateurs
    """
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_started', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ConversationManager()

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Conversation entre {self.user1} et {self.user2}"

    def participants(self):
        return [self.user1, self.user2]
    
    @property
    def last_message(self):
        return self.messages.order_by('-timestamp').first()


    def save(self, *args, **kwargs):
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

class Message(models.Model):
    """
    Message texte ou audio entre deux utilisateurs
    """
    MESSAGE_TYPES = [
        ('TEXT', 'Texte'),
        ('AUDIO', 'Audio'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')

    content = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='chat/audio/', blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='TEXT')

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.message_type})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.message_type == 'TEXT' and not self.content:
            raise ValidationError("Un message texte doit avoir du contenu.")
        if self.message_type == 'AUDIO' and not self.audio_file:
            raise ValidationError("Un message audio doit contenir un fichier audio.")

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=['is_read', 'read_at'])
            return True
        return False
