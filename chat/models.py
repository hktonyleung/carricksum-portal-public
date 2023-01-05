# chat/models.py
from django.db import models
from portal.base._models import BaseModel
from .managers import ChatRoomManager, MessageManager, MembershipManager
from django.conf import settings

class ChatRoom(BaseModel):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, 
            through='Membership', 
            related_name='chatroom_members',
            through_fields=('chat_room', 'user'),
            )

    def __str__(self):
        return f'{self.name}'

    objects = ChatRoomManager()
    all_objects = ChatRoomManager(alive_only=False)

class Membership(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    last_online_time = models.DateTimeField(blank=True, null=True)
    last_offline_time = models.DateTimeField(blank=True, null=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} on {self.chat_room.name}'

    objects = MembershipManager()
    all_objects = MembershipManager(alive_only=False)

class Message(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    #timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.created_datetime}]'

    objects = MessageManager()
    all_objects = MessageManager(alive_only=False)
