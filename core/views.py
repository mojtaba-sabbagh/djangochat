from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from room.models import Room

import string    
import random
K = 10 # Length of rooms' name

from .forms import SignUpForm

def frontpage(request):
    username = request.GET.get('username', 'Guest')
    user = User.objects.get(username=username)
    login(request, user)
    # if user is staff no chat room is created and current rooms are shown.
    if user.is_staff:
        #return render(request, 'core/frontpage.html')
        rooms = Room.objects.all()
        return render(request, 'room/rooms.html', {'rooms': rooms})
    else:
        # create room to chat
        room_name = generate_random_room(K)
        the_room = Room.objects.create(name=room_name, slug=room_name, opened=False)
        return render(request, 'room/room.html', {'room': the_room, 'messages': [],\
                                              'username': request.user.username })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return render(request, template_name='core/logout.html')

def generate_random_room(k):
    S = 10  # number of characters in the string.  
    ran = ''.join(random.choices(string.ascii_uppercase+string.digits, k=k)) 
    return ran