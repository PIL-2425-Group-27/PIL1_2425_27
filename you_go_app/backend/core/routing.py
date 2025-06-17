from django.urls import re_path
from geoassist.consumers import TrackingConsumer

websocket_urlpatterns = [
    re_path(r'ws/tracking/(?P<user_id>\d+)/$', TrackingConsumer.as_asgi())
]

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
