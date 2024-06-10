from django.shortcuts import render, redirect, reverse
from django.db.models import Q, Count
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.
def logout_view(request):
    
    logout(request)
    return redirect('login')

def login_view(request, *args, **kwargs):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect("home")
    error = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            error['message'] = 'Email and Password is required'
        else:
            try:
                if User.objects.get(email__iexact=email):
                    user = authenticate(request, email=email, password=password)
                    
                    if user is not None:
                        login(request, user)
                        return redirect('home') 
                    else:
                        error['message'] = 'Invalid email or password'
            except User.DoesNotExist:
                error['message'] = 'user does not exist'
    context = {
        "error": error,
        "page": page,
    }
    return render(request, "event/login_reg.html", context)


def register(request, *args, **kwargs):
    
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
         
        if form.is_valid():  
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        
    return render(request, 'event/login_reg.html', {'form': form} )


def home(request, *args, **kwargs):
    
    q = request.GET.get('q') if request.GET.get('q') else ''
    
    event_qs = Event.objects.filter(Q(topic__name__icontains=q) |
                                    Q(name__icontains=q) |
                                    Q(description__icontains=q)
                                    )
    msg_qs = Message.objects.filter(Q(event__name__icontains=q) |
                                    Q(event__topic__name__icontains=q) |
                                    Q(event__description__icontains=q)
                                    )
    topic_qs = Topic.objects.all().annotate(event_count=Count('event')).order_by('-event_count')[:5]
    top_hosts = User.objects.all().annotate(event_count=Count('event')).order_by('-event_count')[:5]
    
    event_count = event_qs.count()
    context = {
        "events" : event_qs,
        "topics" : topic_qs,
        "msgs" : msg_qs,
        "event_count" : event_count,
        "top_hosts": top_hosts,
    }
    
    return render(request, "event/home.html", context)

@login_required(login_url="login")
def create_event(request, *args, **kwargs):
    form = EventForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("event__topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Event.objects.create(
            user=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect('home')
    
    context = {
        "form": form,
        "topics": topics,
    }
    
    return render(request, "event/event_form.html", context)

@login_required(login_url="login")
def edit_event(request, id, *args, **kwargs):
    
    try: 
        event = Event.objects.get(id=id)
        form = EventForm(instance=event)
        topics = Topic.objects.all()
        if request.method == "POST":
            topic_name = request.POST.get("event__topic")
            topic, created = Topic.objects.get_or_create(name=topic_name)
            event.topic = topic
            event.name = request.POST.get("name")
            event.description = request.POST.get("description")
            event.save()
            return redirect('home')
            
    except Event.DoesNotExist:
        return HttpResponse("No such event")
    
    context = {
        "form": form,
        "topics": topics,
        "event": event,
    }
    
    return render(request, "event/event_form.html", context)

def event_detail(request, id, *args, **kwargs):
    
    try:
        event = Event.objects.get(id=id)
        event_msgs = event.message_set.all()
        
        if request.method == 'POST':
            Message.objects.create(
                user=request.user,
                event=event,
                body=request.POST.get('body'),
            )
            return redirect('event-detail', event.id)
        
    except Event.DoesNotExist:
        return HttpResponse("No such event")
    
    context = {
        "event": event,
        "event_msgs": event_msgs
    }
    
    return render(request, "event/event.html", context)


def delete_view(request, id, instance, template, *args, **kwargs):
    
    try:
        obj = instance.objects.get(id=id)
        if request.method == 'POST':
            obj.delete()
            return redirect("home")
    except instance.DoesNotExist:
        return HttpResponse("No such Object")
    
    context = {
        "obj": obj,
    }
    
    return render(request, template, context)

@login_required(login_url="login")
def event_delete(request, id, *args, **kwargs):
 return delete_view(request, id, Event, "event/delete.html", *args, **kwargs)

@login_required(login_url="login")
def message_delete(request, id, *args, **kwargs):
   return delete_view(request, id, Message, "event/delete.html", *args, **kwargs)
    
@login_required(login_url="login")
def join_event(request, id, *args, **kwargs):
    
    try:
        event = Event.objects.get(id=id)
        event.members.add(request.user)
    except Event.DoesNotExist:
        return HttpResponse("No such Object")
    
    return redirect("event-detail", event.id)

@login_required(login_url="login")
def leave_event(request, id, *args, **kwargs):
    
    try:
        event = Event.objects.get(id=id)
        event.members.remove(request.user)
    except Event.DoesNotExist:
        return HttpResponse("No such Object")
    
    return redirect("event-detail", event.id)


@login_required(login_url="login")
def follow_user(request, id, *args, **kwargs):
    try:
        user = User.objects.get(id=id)
        user.followers.add(request.user)
        request.user.following.add(user)
    except User.DoesNotExist:
        return HttpResponse("No User Object")
    
    url = reverse('profile', args=(user.username, user.id))
    return redirect(url)

@login_required(login_url="login")
def un_follow_user(request, id, *args, **kwargs):
    try:
        user = User.objects.get(id=id)
        user.followers.remove(request.user)
        request.user.following.remove(user)
    except User.DoesNotExist:
        return HttpResponse("No User Object")
    
    url = reverse('profile', args=(user.username, user.id))
    return redirect(url)

def topics(request, *args, **kwargs):
    
    q = request.GET.get('q') if request.GET.get('q') else ''
    
    topic_qs = Topic.objects.filter(name__icontains=q).annotate(event_count=Count('event')).order_by('-event_count')[:5]
    return render(request, 'event/topics.html', {'topics': topic_qs})


def activities(request, *args, **kwargs):
    
    msg_qs = Message.objects.all()[:7]
    return render(request, 'event/activities.html', {'msgs': msg_qs})



def profile(request, id, *args, **kwargs):
    
    user = User.objects.get(id=id)
    
    topics = Topic.objects.all().annotate(event_count=Count('event')).order_by('-event_count')[:5]
    msgs = user.message_set.all()[:7]
    events = user.event_set.all()
    
    context = {
        "events": events,
        "msgs": msgs,
        "topics": topics,
        "user": user
    }
    
    return render(request, 'event/profile.html', context)

@login_required(login_url="login")
def settings_page(request, *args, **kwargs):
    form = UpdateUserForm(instance=request.user)
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            url = reverse('profile', args=(user.username, user.id))
            return redirect(url) 
    
    context = {
        "form": form,
    }
    return render(request, 'event/settings.html', context)