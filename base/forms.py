from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm
from .models import Message, Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name','desc','topic']
        # fields
        # fields = '__all__'

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


