from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Time to pass data to the templates 
rooms = [
    {'id': 1, 'name': 'Lets learn python with me!'},
    {'id': 2, 'name': 'Django for begginners!'},
    {'id': 3, 'name': 'Frontend Developers!'}

] # Now we need to pass this data via home method below

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms} 
    return render(request, 'base/home.html', context)

# Another example route for practice
def room(request, pk): #lets make urls dynamic
    room = Room.objects.get(id= pk)
    context = {'room': room}

    return render(request, 'base/room.html', context)
