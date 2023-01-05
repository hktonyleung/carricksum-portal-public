import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import ChatRoom, Membership, Message
#from datetime import datetime
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = ChatRoom.objects.get(name=self.room_name)

        Membership.objects.update_member_status(self.room_name, self.user, True)

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # notify for new online member
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'online_member_notify',
                'user_id': self.user.id,
                'username': self.user.username,
                'online_datetime': timezone.now().strftime("%d/%m/%Y %I:%M %p"),
            }
        )

    def disconnect(self, close_code):

        Membership.objects.update_member_status(self.room_name, self.user, False)

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        # notify for new offline member
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'offline_member_notify',
                'user_id': self.user.id,
                'username': self.user.username,
                'offline_datetime': timezone.now().strftime("%d/%m/%Y %I:%M %p"),
            }
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']


        Message.objects.create_message(self.user, self.room, message)

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'receive_datetime': timezone.now().strftime("%d/%m/%Y %I:%M %p"),
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def online_member_notify(self, event):
        self.send(text_data=json.dumps(event))

    def offline_member_notify(self, event):
        self.send(text_data=json.dumps(event))
