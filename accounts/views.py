# accounts/views.py

from ai_security.models import SuspiciousActivity
from ai_security.detector import detect_failed_logins
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from dashboard.views import (
    soldier_dashboard, 
    officer_dashboard, 
    commander_dashboard, 
    admin_dashboard

)
from ai_security.detector import detect_failed_logins





def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            man_number = form.cleaned_data.get('man_number')
            
            # Check man number length
            if len(str(man_number)) != 6:
                form.add_error('man_number', 'Man number must be exactly 6 digits.')
            # Check uniqueness
            elif CustomUser.objects.filter(man_number=man_number).exists():
                form.add_error('man_number', f"A soldier with man number {man_number} already exists.")
            else:
                # Auto-generate username (just to satisfy unique constraint)
                from django.utils.crypto import get_random_string
                user = form.save(commit=False)
                user.username = get_random_string(10)
                user.save()
                
                # Optional: log the user in immediately
                # login(request, user)
                
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):

    if request.method == "POST":

        man_number = request.POST.get('man_number')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(man_number=man_number)

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

        except CustomUser.DoesNotExist:
            user = None
            user_obj = None

        # SUCCESSFUL LOGIN
        if user is not None:

            # reset failed attempts
            request.session['failed_attempts'] = 0

            login(request, user)

            # Redirect based on role
            if user.role == 'soldier':
                return redirect('dashboard_soldier')

            elif user.role == 'officer':
                return redirect('dashboard_officer')

            elif user.role == 'commander':
                return redirect('dashboard_commander')

            elif user.role == 'admin':
                return redirect('dashboard_admin')

        # FAILED LOGIN
        else:

            failed_attempts = request.session.get('failed_attempts', 0)
            failed_attempts += 1

            request.session['failed_attempts'] = failed_attempts

            # AI SECURITY DETECTION
            if user_obj:
                detect_failed_logins(user_obj, failed_attempts)

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid man number or password'
                }
            )

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):

    user = request.user

    # SECURITY ALERT COUNT
    security_alert_count = SuspiciousActivity.objects.filter(
        resolved=False
    ).count()

    context = {
        'user': user,
        'security_alert_count': security_alert_count,
    }

    # COMMANDER DASHBOARD
    if user.role == 'commander':

        soldiers_count = CustomUser.objects.filter(
            commander=user
        ).count()

        active_missions_count = Mission.objects.filter(
            commander=user,
            status='active'
        ).count()

        unread_messages_count = Message.objects.filter(
            recipient=user,
            read=False
        ).count()

        context.update({
            'role': 'commander',
            'soldiers_count': soldiers_count,
            'active_missions_count': active_missions_count,
            'unread_messages_count': unread_messages_count,
        })

    # OFFICER DASHBOARD
    elif user.role == 'officer':

        missions_count = Mission.objects.filter(
            officer=user
        ).count()

        completed_missions_count = Mission.objects.filter(
            officer=user,
            status='completed'
        ).count()

        unread_messages_count = Message.objects.filter(
            recipient=user,
            read=False
        ).count()

        context.update({
            'role': 'officer',
            'missions_count': missions_count,
            'completed_missions_count': completed_missions_count,
            'unread_messages_count': unread_messages_count,
        })

    # SOLDIER DASHBOARD
    elif user.role == 'soldier':

        missions_count = Mission.objects.filter(
            soldiers=user
        ).count()

        completed_missions_count = Mission.objects.filter(
            soldiers=user,
            status='completed'
        ).count()

        unread_messages_count = Message.objects.filter(
            recipient=user,
            read=False
        ).count()

        context.update({
            'role': 'soldier',
            'missions_count': missions_count,
            'completed_missions_count': completed_missions_count,
            'unread_messages_count': unread_messages_count,
        })

    return render(
        request,
        'dashboard.html',
        context
    )

