from django.shortcuts import render,redirect
from base.models import Message, Room, Topic
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from .forms import MessageForm, RoomForm
from django.http import HttpResponse
from django.db.models import Q 



# Create your views here.
def signin(req):
    if req.user.is_authenticated:
        return redirect('home')
    if req.method == 'POST':
        username = req.POST.get('username').lower()
        password = req.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(req,username=username,password=password )
            if user is not None:
                login(req,user,)
                return redirect('home')
            else:
                messages.error(req,'Bad Credentials.')
        except:
             messages.error(req,'Bad Credentials')
        

    return render(req,'base/signin.html',{'page':'Signin'})


def register(req):
    form = UserCreationForm()
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 
            authenticate(req,username=user.username,password=user.password)
            login(req,user)
            return redirect('home')
        
        for m in form.error_messages:
            messages.error(req,m)
    context = {'form':form,'page':'Register'}#
    return render(req,'base/signin.html',context)

def logoutUser(req):
    logout(req)
    return redirect('signin')

def home(req):
    topic = req.GET.get('q')
    name = req.GET.get('name')
    # Room.objects.get(topic=1)
    rooms = None
    if topic:
        rooms = Room.objects.filter(topic=topic)
    elif name:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=name) |
            Q(name__icontains=name) |
            Q(desc__icontains=name)
        )
    else: 
        rooms = Room.objects.all()
    topics = Topic.objects.all()
    context = {'rooms':rooms,'topics':topics}
    return render(req,'base/home.html',context)

@login_required(login_url='signin')
def createRoom(req):
    form = RoomForm()
    if req.method == 'POST':
        # name = req.POST.get('name') # get spesific fileds
        form = RoomForm(req.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.host = req.user
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(req,'base/room_form.html',context)

@login_required(login_url='signin')
def updateRoom(req,id):
    room = Room.objects.get(id=id)
    if req.user != room.host:
        return HttpResponse('You are not allow to update this room')

    form  = RoomForm(instance=room)
    context = {'form':form}
    if req.method == 'POST':
        form = RoomForm(req.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(req,'base/room_form.html',context)

@login_required(login_url='signin')
def deleteRoom(req,id):
    room = Room.objects.get(id=id)

    if req.user != room.host:
        return HttpResponse('You are not allow to delete this room')
    if req.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(req,'base/delete.html',{'obj':room})



def room(req,id):
    # form = MessageForm()
    room = Room.objects.get(id = id)
    msgs = Message.objects.filter(room__id=id)
    if req.method == 'POST':
        if req.user.is_authenticated:
            form = MessageForm(req.POST)
            if form.is_valid():
                form.save()
            else:
                messages.error(req,"form is not valid")
                for m in form.errors:
                    messages.error(req,m)    
        else: return redirect('signin',)

    context = {"room":room,'msgs':msgs} # 'form': form
    return render(req,'base/room.html',context)



def about(req):
    return render(req,'base/about.html')




'''
room = Room.objects.get()
otherrooms = Room.objects.filter()
onlyroom = Room.objects.exclude()
'''