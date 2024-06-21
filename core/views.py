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
    username = username = request.GET.get('username', 'Guest')
    if not request.user.is_authenticated:      
        user = User.objects.get(username='Guest')
        login(request, user)
        # if user is staff no chat room is created and current rooms are shown.
    else:
        user = User.objects.get(username=request.user)
    if user.is_staff:
        #return render(request, 'core/frontpage.html')
        rooms = Room.objects.all()
        return render(request, 'room/rooms.html', {'rooms': rooms})
    else:
        # create room to chat
        room_name = generate_random_room(K)
        the_room = Room.objects.create(name=room_name, slug=room_name, opened=False, nikname=username)
        return render(request, 'room/room.html', {'room': the_room, 'messages': [],\
                                            'username': user.username, 'nikname':username })

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

def home_page(request):
    return render(request, "core/home.html")

def generate_random_room(k):
    S = 10  # number of characters in the string.  
    ran = ''.join(random.choices(string.ascii_uppercase+string.digits, k=k)) 
    return ran