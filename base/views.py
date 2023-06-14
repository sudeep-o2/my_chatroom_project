from django.http import HttpResponse
from django.shortcuts import render,redirect
from . models import Room,Topic,Messages,User,MessageLikes
from .forms import RoomForm,UserForm,myUserCreationForm
from django.db.models import Q
#from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
 


# Create your views here.

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username=q) |
        Q(description__icontains=q)
         )
    
    topics=Topic.objects.all()[0:5]

    room_count=rooms.count()

    room_messages=Messages.objects.filter(Q(room__topic__name__icontains=q))

    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}


    return render(request,'base/home.html',context)


def room(request,pk):

    rooms=Room.objects.get(id=pk)
    room_messages=rooms.messages_set.all().order_by('-created')
    participants=rooms.participants.all()


    if request.method=='POST':
        Messages.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('comment')
        )
        rooms.participants.add(request.user)
        return redirect('room',pk=rooms.id)

    context={'rooms':rooms,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)  


def room_profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()

    room_messages=user.messages_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),

        )
        # form=RoomForm(request.POST)
        #if form.is_valid():
        #   room=form.save(commit=False)
        #   room.host=request.user
        #   room.save()
        return redirect('home')

    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    topics=Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You cannot do This')

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.topic=topic
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')

    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You cannot do This')

    if request.method=='POST':
        room.delete()
        return redirect('home')

    return render(request,'base/delete.html',{'obj':room})


def Loginview(request):

    stat='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request, "User not found.")

        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "password is incorrect.")
    
    context={'stat':stat}
    return render(request,'base/login_reg.html',context)

def Logoutview(request):
    
    logout(request)
    return redirect('home')

def Register(request):
    form=myUserCreationForm()

    if request.method=='POST':
        form=myUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'some error occurred in registration')

    context={'form':form}
    return render(request,'base/login_reg.html',context)


@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Messages.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You cannot do This')

    if request.method=='POST':
        message.delete()
        return redirect('home')

    return render(request,'base/delete.html',{'obj':message})


def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method=='POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid:
            form.save()
            return redirect('room-profile', pk=user.id)
    return render(request,'base/update-user.html',{'form':form})

def topicsView(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})


def activityView(request):
    room_messages=Messages.objects.all()
    return render(request,'base/activity.html',{'room_messages': room_messages})


def likemessages(request,pk):

    #total_likes=MessageLikes.objects.all().count()
    p=Messages.objects.get(id=pk)
    #total_likes=p.messagelikes_set.all().count()
    
    new_like,created=MessageLikes.objects.get_or_create(liker=request.user,message=p)

    new_like.save()
    return redirect(request.META['HTTP_REFERER'])

    context={'total_likes':total_likes,'p':p}

    return render(request,'base/room.html',context)
    