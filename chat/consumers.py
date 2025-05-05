import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Chat, ChatRoom
from account.models import Account
from django.db import models
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Tạo phòng chat nếu chưa tồn tại
        await self.get_or_create_room(self.room_name)

        # Thêm user vào nhóm chat
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Xóa user khỏi nhóm chat
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat = data["message"]  # Đổi từ "chat" thành "message"
        sender_email = data["sender"]
        print(f"Received message: {chat}, from: {sender_email}") 
        # Kiểm tra bạn bè trước khi gửi tin nhắn
        sender = await sync_to_async(lambda: Account.objects.get(email=sender_email))()
        print(f"sender: {sender.email}") 
        # Đảm bảo sender tồn tại trước khi sử dụng
        if not sender:
            print(f"Sender with email {sender_email} not found!")
            return  # Dừng lại nếu không tìm thấy sender

        # receiver = await self.get_friend(sender)
        # print(f"receiver: {receiver}") 
        # if receiver:
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": chat, "sender": sender.email},
        )
        await self.save_message(self.room_name, sender.email, chat)  # Đảm bảo đúng tham số

    async def chat_message(self, event):
        message = event["message"]
        sender_email = event["sender"]  # Lấy email thay vì object

        # Gửi tin nhắn qua WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender_email}))


    @sync_to_async
    def get_or_create_room(self, room_name):
        """Tạo phòng chat nếu chưa tồn tại"""
        ChatRoom.objects.get_or_create(name=room_name)

    @sync_to_async
    def save_message(self, room_name, sender_email, message):
        """Lưu tin nhắn vào database"""
        room = ChatRoom.objects.get(name=room_name)
        sender, _ = User.objects.get_or_create(email=sender_email)
        Chat.objects.create(room=room, sender=sender, content=message)

    async def get_friend(self, user):
        """Kiểm tra xem có phải bạn bè không"""
        room_users = self.room_name.split("_")
        if len(room_users) != 2:
            return None

        friend_email = room_users[1] if room_users[0] == user.email else room_users[0]
        return await sync_to_async(lambda: Account.objects.filter(
            models.Q(friends1__user2=user, friends1__status="accepted", friends1__user1__email=friend_email) |
            models.Q(friends2__user1=user, friends2__status="accepted", friends2__user2__email=friend_email)
        ).first())()
