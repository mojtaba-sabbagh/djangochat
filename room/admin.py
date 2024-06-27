from django.contrib import admin
from .models import Room, Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    css = {
             'all': ('templates/css/admin-extra.css ',)
        }
    list_filter = ('room',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    css = {
             'all': ('templates/css/admin-extra.css ',)
        }
    readonly_fields = ('id',)