import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Tell everyone that this user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "user_id": self.scope["user"].id,
                "username": self.scope["user"].username,
                "status": "online",
            }
        )


    async def disconnect(self, close_code):

        # Tell everyone that this user is offline
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "user_id": self.scope["user"].id,
                "username": self.scope["user"].username,
                "status": "offline",
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):

        data = json.loads(text_data)

        message_text = data["message"]

        # Save message to database
        message_data = await self.save_message(message_text)

        # Send message to everyone
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_data["message"],
                "sender_id": message_data["sender_id"],
                "sender_username": message_data["sender_username"],
                "timestamp": message_data["timestamp"],
            }
        )


    @database_sync_to_async
    def save_message(self, message_text):

        conversation = Conversation.objects.get(
            id=self.conversation_id
        )

        message = Message.objects.create(
            conversation=conversation,
            sender=self.scope["user"],
            content=message_text
        )

        return {
            "message": message.content,
            "sender_id": message.sender.id,
            "sender_username": message.sender.username,
            "timestamp": message.created_at.isoformat(),
        }


    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "sender_id": event["sender_id"],
                "sender_username": event["sender_username"],
                "timestamp": event["timestamp"],
            })
        )


    async def user_status(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "status",
                "user_id": event["user_id"],
                "username": event["username"],
                "status": event["status"],
            })
        )