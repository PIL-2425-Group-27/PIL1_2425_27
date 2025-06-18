from django.urls import re_path
from . import consumers

# WebSocket URL patterns matching your chat architecture
websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi(), name='chat-websocket'),
    
]

