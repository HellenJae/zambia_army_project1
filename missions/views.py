from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mission
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ Add this line

@login_required
def mission_list(request):
    user = request.user
    missions = Mission.objects.all().order_by('-created_at')

    if request.method == "POST" and user.role in ['commander', 'officer']:
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        assigned_ids = request.POST.getlist('assigned_to')
        due_date = request.POST.get('due_date') or None
        status = request.POST.get('status', 'pending')

        if not title or not description:
            messages.error(request, "Title and description are required.")
        else:
            mission = Mission.objects.create(
                title=title,
                description=description,
                status=status,
                due_date=due_date
            )
            if assigned_ids:
                users_to_assign = User.objects.filter(id__in=assigned_ids)
                mission.assigned_to.set(users_to_assign)
            messages.success(request, "Mission added successfully!")
            return redirect('missions:mission_list')

    users = User.objects.all() if user.role in ['commander', 'officer'] else None

    return render(request, 'missions/mission_list.html', {
        'missions': missions,
        'can_add': user.role in ['commander', 'officer'],
        'users': users,
    })


@login_required
def mark_completed(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    if request.user.role in ['commander', 'officer']:
        mission.status = "completed"
        mission.save()
        messages.success(request, f"Mission '{mission.title}' marked as completed.")
    else:
        messages.error(request, "You do not have permission to complete this mission.")
    return redirect('missions:mission_list')
