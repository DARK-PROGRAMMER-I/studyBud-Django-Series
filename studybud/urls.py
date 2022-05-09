from django.contrib import admin
from django.urls import path , include

# # We normally dont create views here, its just for practice
# def home(request):
#     return HttpResponse('Home Page')

# # Another example route for practice
# def room(request):
#     return HttpResponse('Rooms')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))    
]
