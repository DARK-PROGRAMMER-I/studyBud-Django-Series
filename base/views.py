from django.shortcuts import render
from django.http import HttpResponse

# Time to pass data to the templates 
rooms = [
    {'id': 1, 'name': 'Lets learn python with me!'},
    {'id': 2, 'name': 'Django for begginners!'},
    {'id': 3, 'name': 'Frontend Developers!'}

] # Now we need to pass this data via home method below

bugs = [
    [1],
    [2],
    [3]
]

def home(request):
    context = {'rooms': rooms, 'bugs': bugs} 
    return render(request, 'base/home.html', context)

# Another example route for practice
def room(request, pk): #lets make urls dynamic
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i

    context = {'room': room}

    return render(request, 'base/room.html', context)
