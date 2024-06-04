from django.urls import path, re_path

from . import consumers, refresh

websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
     re_path(r"ws/(?P<user_name>\w+)/$", refresh.RefreshRoom.as_asgi()),
]