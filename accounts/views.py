# accounts/views.py
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
        
        # Authenticate using man_number
        try:
            user_obj = CustomUser.objects.get(man_number=man_number)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.role == 'soldier':
                return redirect('dashboard_soldier')
            elif user.role == 'officer':
                return redirect('dashboard_officer')
            elif user.role == 'commander':
                return redirect('dashboard_commander')
            elif user.role == 'admin':
                return redirect('dashboard_admin')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid man number or password'})

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,  # make sure user is passed
    }

    if user.role == 'commander':
        soldiers_count = CustomUser.objects.filter(commander=user).count()
        active_missions_count = Mission.objects.filter(commander=user, status='active').count()
        unread_messages_count = Message.objects.filter(recipient=user, read=False).count()

        context.update({
            'role': 'commander',
            'soldiers_count': soldiers_count,
            'active_missions_count': active_missions_count,
            'unread_messages_count': unread_messages_count,
        })

    elif user.role == 'officer':
        missions_count = Mission.objects.filter(officer=user).count()
        completed_missions_count = Mission.objects.filter(officer=user, status='completed').count()
        unread_messages_count = Message.objects.filter(recipient=user, read=False).count()

        context.update({
            'role': 'officer',
            'missions_count': missions_count,
            'completed_missions_count': completed_missions_count,
            'unread_messages_count': unread_messages_count,
        })

    elif user.role == 'soldier':
        missions_count = Mission.objects.filter(soldiers=user).count()
        completed_missions_count = Mission.objects.filter(soldiers=user, status='completed').count()
        unread_messages_count = Message.objects.filter(recipient=user, read=False).count()

        context.update({
            'role': 'soldier',
            'missions_count': missions_count,
            'completed_missions_count': completed_missions_count,
            'unread_messages_count': unread_messages_count,
        })

    return render(request, 'dashboard.html', context)