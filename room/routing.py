from django.urls import path, re_path

from room import consumers

websocket_urlpatterns = [
    re_path(r"chat/ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]