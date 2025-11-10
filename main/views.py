from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from messaging.models import Message
from missions.models import Mission
from announcements.models import Announcement
from accounts.models import CustomUser

@login_required
def dashboard_soldier(request):
    user = request.user
    announcements = Announcement.objects.filter(visible_to_roles__contains=['soldier'])
    missions = Mission.objects.filter(assigned_to_roles__contains=['soldier'])
    messages = Message.objects.filter(receiver=user)
    return render(request, 'main/dashboard.html', {
        'user': user,
        'announcements': announcements,
        'missions': missions,
        'messages': messages
    })

@login_required
def dashboard_officer(request):
    user = request.user
    announcements = Announcement.objects.filter(visible_to_roles__contains=['officer'])
    missions = Mission.objects.filter(assigned_to_roles__contains=['officer'])
    messages = Message.objects.filter(receiver=user)
    return render(request, 'main/dashboard.html', {
        'user': user,
        'announcements': announcements,
        'missions': missions,
        'messages': messages
    })

@login_required
def dashboard_commander(request):
    user = request.user
    announcements = Announcement.objects.filter(visible_to_roles__contains=['commander'])
    missions = Mission.objects.filter(assigned_to_roles__contains=['commander'])
    messages = Message.objects.filter(receiver=user)
    return render(request, 'main/dashboard.html', {
        'user': user,
        'announcements': announcements,
        'missions': missions,
        'messages': messages
    })

@login_required
def dashboard_admin(request):
    user = request.user
    announcements = Announcement.objects.all()  # admin sees all
    missions = Mission.objects.all()
    messages = Message.objects.filter(receiver=user)
    return render(request, 'main/dashboard.html', {
        'user': user,
        'announcements': announcements,
        'missions': missions,
        'messages': messages
    })


def home(request):
    return render(request, 'main/home.html')


def slash(request):
    return render(request, 'main/slash.html')
