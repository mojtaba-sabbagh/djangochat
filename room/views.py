from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.conf import settings

from .models import Room, Message
import shutil

@staff_member_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms, 'title_page': 'Rooms'})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    if request.user.is_staff:
        room.opened = True
        room.save()
    messages = Message.objects.filter(room=room)[0:25]
    return render(request, 'room/room.html', {'room': room, 'messages': messages,\
                                              'username': request.user.username,\
                                                'title_page': 'Chat Room'})
@staff_member_required
def delroom(request, slug):
    try:
        room = Room.objects.get(slug=slug)
        folder_path = f'{settings.MEDIA_ROOT}/{room.name}'
        try:
            shutil.rmtree(folder_path)
        except:
            pass
        room.delete()
    except Room.DoesNotExist:
        pass
    return redirect('rooms')
