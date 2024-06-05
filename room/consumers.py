import json
import base64
from pathlib import Path
import os

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message

BASE_DIR = Path(__file__).parent.parent

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        payam = ''
        kind = 1
        username = data['username']
        room = data['room']
        if 'message' in data:
            message = data['message']
            payam = message
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': payam,
                    'username': username
                }
            )
        elif 'file' in data:
            file_data = data['file']
            file_name = data['file_name']
            payam = file_name
            kind = 2
            with open(os.path.join(BASE_DIR, f'media/{file_name}'), 'wb') as f:
                f.write(base64.b64decode(file_data))
            # ارسال نام فایل به گروه چت
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_file',
                    'file_name': file_name,
                    'username': username
                }
            )

        await self.save_message(username, room, payam, kind)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    async def chat_file(self, event):
        file_name = event['file_name']
        username = event['username']
        # ارسال نام فایل به WebSocket
        await self.send(text_data=json.dumps({
            'file_name': file_name,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room, message, kind):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message, kind=kind)