import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = f'chat_{self.room_name}'
        self.ping_pong_group = "ping_pong_group"
        self.user = self.scope['user']

        # Join room group
        print(self.channel_name)
        await self.channel_layer.group_add(
            self.ping_pong_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.ping_pong_group,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        user = self.scope.get('user', '')
        if user.is_anonymous:
            user = None
        else:
            user = user.email
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        # Send message to room group
        await self.channel_layer.group_send(
            self.ping_pong_group,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'user': user,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'user': user,
        }))
