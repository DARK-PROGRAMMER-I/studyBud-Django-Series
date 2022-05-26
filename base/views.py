from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm
# Time to pass data to the templates
# rooms = [
#     {'id': 1, 'name': 'Lets learn python with me!'},
#     {'id': 2, 'name': 'Django for begginners!'},
#     {'id': 3, 'name': 'Frontend Developers!'}

# ] # Now we need to pass this data via home method below


def login_page(request):
    page = 'login'

    # if already logged In, dont allow to login again
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Check if this user exists or not and throw flash message as an error
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Doesn't Exists")

        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorrect!')

    context = {'page': page}
    return render(request, 'base/login_page.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


# Register page
def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error occured, please try again!')

    context = {'page': page, 'form': form}
    return render(request, 'base\login_page.html', context)


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )  # rooms from Database
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains = q)
    )

    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages }
    return render(request, 'base/home.html', context)

# Another example route for practice


def room(request, pk):  # lets make urls dynamic
    room = Room.objects.get(id=pk)
    message_user = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        mesasge = Message.objects.create(
            user=request.user,
            room=room,
            # 'body' is from input tag's name field.
            body=request.POST.get('body')
        )

        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'message_user': message_user,
               'participants': participants }

    return render(request, 'base/room.html', context)

# Method for creating room
# Restricting User to create room if he's loggedOut


@login_required(login_url='login')
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
@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # Only admin can update the room
    if request.user != room.host:
        return HttpResponse('Only Admin is allowed to edit the room!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base\create_room.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    # restrict user deleting the room if he/she is not owner of it!
    if request.user != room.host:
        return HttpResponse("Only Admin can delete the room!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base\delete.html', {'room': room})


def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    # room = Room.objects.get(id  = pk)
    if request.user != message.user:
        return HttpResponse('Only Admin can delete this message')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base\delete.html', {'message': message})
