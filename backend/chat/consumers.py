import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from asgiref.sync import sync_to_async

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope["user"]

        # Reject if not authenticated
        if not self.user.is_authenticated:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get("text")

        if not message_text:
            return

        # Save message to DB
        message = await self.save_message(message_text)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender": self.user.username,
                "timestamp": str(message.timestamp),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))

    @sync_to_async
    def save_message(self, message_text):
        room = ChatRoom.objects.get(id=self.room_id)
        return Message.objects.create(
            room=room,
            sender=self.user,
            text=message_text
        )
