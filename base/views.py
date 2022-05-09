from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('Home Page')

# Another example route for practice
def room(request):
    return HttpResponse('Rooms')
