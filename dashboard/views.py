from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Helper decorators for role-based access
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')(view_func)

def officer_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'officer')(view_func)

def soldier_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'soldier')(view_func)


@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')


@login_required
@officer_required
def officer_dashboard(request):
    return render(request, 'dashboard/officer_dashboard.html')


@login_required
@soldier_required
def soldier_dashboard(request):
    return render(request, 'dashboard/soldier_dashboard.html')
@login_required
def commander_dashboard(request):
    return render(request, 'dashboard/commander_dashboard.html')

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'dashboard/profile.html')