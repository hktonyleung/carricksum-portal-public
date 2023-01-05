from django.shortcuts import render
from chat.models import ChatRoom, Membership, Message
from django.contrib.auth.decorators import login_required
from .decorators import chat_room_access_right_required

# Create your views here.
@login_required
def index_view(request):
    return render(request, 'chat/index.html', {
        'chat_rooms': ChatRoom.objects.get_my_rooms_summary(request.user.username),
        
    })

@chat_room_access_right_required
def room_view(request, room_name):
    chat_room = ChatRoom.objects.get(name=room_name)
    onlines = Membership.objects.onlines(room_name)
    offlines = Membership.objects.offlines(room_name)
    messages = Message.objects.messages(room_name)
    return render(request, 'chat/chat_room.html', {
        'room': chat_room,
        'onlines': onlines,
        'offlines': offlines,
        'messages': messages,
    })
