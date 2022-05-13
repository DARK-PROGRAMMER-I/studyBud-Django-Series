from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
# Time to pass data to the templates 
# rooms = [
#     {'id': 1, 'name': 'Lets learn python with me!'},
#     {'id': 2, 'name': 'Django for begginners!'},
#     {'id': 3, 'name': 'Frontend Developers!'}

# ] # Now we need to pass this data via home method below

def home(request):
    rooms = Room.objects.all() # rooms from Database
    context = {'rooms': rooms} 
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






