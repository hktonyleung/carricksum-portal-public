from datetime import date
from portal.base._managers import BaseModelManager
from datetime import datetime, timedelta, time
from django.db.models import Count, Q

today = datetime.now().date()
tomorrow = today + timedelta(1)
today_start = datetime.combine(today, time())
today_end = datetime.combine(tomorrow, time())

class ChatRoomManager(BaseModelManager):

    def get_all_room_summary(self):
        online_count = Count('members', filter=Q(membership__online=True))
        total_count = Count('members')
        return self.values('name').annotate(online_count=online_count).annotate(total_count=total_count)

    #TODO
    def get_my_rooms_summary(self, username):
        online_count = Count('members', filter=Q(membership__online=True))
        total_count = Count('members')
        return self.values('name').annotate(online_count=online_count).annotate(total_count=total_count).filter(membership__user__username=username)
        

class MessageManager(BaseModelManager):
    def create_message(self, user, room, content):
        message = self.create(user=user, room=room, content=content, created_by=user)
    
    def messages(self, chat_room):
        return super().get_queryset().filter(room__name=chat_room, created_datetime__lte=today_end, created_datetime__gte=today_start).order_by('created_datetime')

class MembershipManager(BaseModelManager):
    def onlines(self, chat_room):
        return super().get_queryset().filter(chat_room__name=chat_room, online=True).order_by('last_online_time')

    def offlines(self, chat_room):
        return super().get_queryset().filter(chat_room__name=chat_room, online=False).order_by('last_offline_time')

    def update_member_status(self, chat_room, user, online):
        membership = super().get_queryset().get(chat_room__name=chat_room, user=user)
        membership.online = online
        if online:
            membership.last_online_time = datetime.now()
        else:
            membership.last_offline_time = datetime.now()
        membership.save()

    
