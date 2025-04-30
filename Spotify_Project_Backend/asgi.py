"""
ASGI config for Spotify_Project_Backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Spotify_Project_Backend.settings")
django.setup()  # Đảm bảo gọi setup() sau khi đặt biến môi trường

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})

