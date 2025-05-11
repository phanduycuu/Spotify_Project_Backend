from django.urls import re_path
from .consumers import FriendListConsumer

websocket_urlpatterns = [
    re_path(r'^ws/friends/$', FriendListConsumer.as_asgi()),
]