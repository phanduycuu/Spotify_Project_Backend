from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ChatRoom, Chat
from rest_framework.decorators import api_view

@api_view(["GET"])
def get_chat_history(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    Chats = Chat.objects.filter(room=room).order_by("timestamp")

    return JsonResponse(
        [{ "sender": msg.sender.email, "chat": msg.content, "timestamp": msg.timestamp} for msg in Chats],
        safe=False,
    )
