import json
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

r = settings.REDIS


class CoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = f'chat_{self.room_name}'
        self.ping_pong_group = "ping_pong_group"
        self.user = self.scope["user"]

        # Join room group
        print(self.channel_name)  # noqa
        await self.channel_layer.group_add(
            self.ping_pong_group, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.ping_pong_group, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("received message")
        user = self.scope.get("user", "")
        if user.is_anonymous:
            user = None
        else:
            user = user.email
        cached_value = r.incr("cached_value", amount=3)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        ts = text_data_json["ts"]
        sender = text_data_json["sender"]
        # Send message to room group
        await self.channel_layer.group_send(
            self.ping_pong_group,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "user": user,
                "cached_value": cached_value,
                "vue_ping": ts,
                "server_recv_ping": time.time() * 1000,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        user = event["user"]
        vue_ping = event["vue_ping"]
        cached_value = event["cached_value"]
        server_recv_ping = event["server_recv_ping"]
        print(cached_value)
        print("sending ws response")
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                    "user": user,
                    "cached_value": cached_value,
                    "server_recv_ping": server_recv_ping,
                    "server_send_pong": time.time() * 1000,
                    "vue_ping": vue_ping,
                }
            )
        )
