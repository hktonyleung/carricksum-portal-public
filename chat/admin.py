from django.contrib import admin
from portal.base._admin import BaseAdmin
from chat.models import ChatRoom, Message, Membership

# Register your models here.
class ChatRoomAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class MessageAdmin(BaseAdmin):
    list_display = ('user', 'room', 'content')
    search_fields = ('user', 'room', 'content')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class MembershipAdmin(BaseAdmin):
    list_display = ('user', 'chat_room', 'online')
    search_fields = ('user', 'chat_room', 'online')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Membership, MembershipAdmin)

