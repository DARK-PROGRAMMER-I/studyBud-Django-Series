from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # we can also specify specific filed like this ['name'] etc
        exclude = ['host' , 'participants']