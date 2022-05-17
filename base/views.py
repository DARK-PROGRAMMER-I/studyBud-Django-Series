from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.db.models import Q
from django.http import HttpResponse
from .models import Room , Topic
from .forms import RoomForm
# Time to pass data to the templates 
# rooms = [
#     {'id': 1, 'name': 'Lets learn python with me!'},
#     {'id': 2, 'name': 'Django for begginners!'},
#     {'id': 3, 'name': 'Frontend Developers!'}

# ] # Now we need to pass this data via home method below
def login_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if this user exists or not and throw flash message as an error
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request , "User Doesn't Exists")

        
        user = authenticate(request , username= username , password = password)
        if user != None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , 'Username OR Password is incorrect!')

    context = {}
    return render(request , 'base/login_page.html', context )


def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    q = request.GET.get('q')  if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains= q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q)
                                    ) # rooms from Database
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms , 'topics': topics , 'room_count':room_count} 
    return render(request, 'base/home.html', context)

# Another example route for practice
def room(request, pk): #lets make urls dynamic
    room = Room.objects.get(id= pk)
    context = {'room': room}

    return render(request, 'base/room.html', context)

# Method for creating room
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
    context = {'form': form}
    return render(request, 'base\create_room.html', context)


# Method for updating the room
def update_room(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request , 'base\create_room.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base\delete.html', {'room': room})





