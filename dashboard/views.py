from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from ai_security.models import SuspiciousActivity
from accounts.models import CustomUser
from missions.models import Mission
from messaging.models import Message
from ai_summary.models import AISummary


# ==============================
# ROLE CHECKS
# ==============================

def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == 'admin'
    )(view_func)


def officer_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == 'officer'
    )(view_func)


def soldier_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == 'soldier'
    )(view_func)


# ==============================
# ADMIN DASHBOARD
# ==============================

@login_required
@admin_required
def admin_dashboard(request):

    context = {

        "security_alert_count":
            SuspiciousActivity.objects.filter(
                resolved=False
            ).count(),

        "users_count":
            CustomUser.objects.count(),

        "unread_messages_count":
            Message.objects.filter(
                recipient=request.user,
                read=False
            ).count(),

    }


    return render(
        request,
        "dashboard/admin_dashboard.html",
        context
    )


# ==============================
# COMMANDER DASHBOARD
# ==============================

@login_required
def commander_dashboard(request):

    user = request.user


    soldiers_count = CustomUser.objects.filter(
        commander=user
    ).count()


    active_missions_count = Mission.objects.filter(
        assigned_to=user,
        status="in_progress"
    ).count()


    completed_missions_count = Mission.objects.filter(
        assigned_to=user,
        status="completed"
    ).count()



    unread_messages_count = Message.objects.filter(
        recipient=user,
        read=False
    ).count()



    security_alert_count = SuspiciousActivity.objects.filter(
        resolved=False
    ).count()



    context = {

        "soldiers_count": soldiers_count,

        "active_missions_count":
            active_missions_count,

        "completed_missions_count":
            completed_missions_count,

        "unread_messages_count":
            unread_messages_count,

        "security_alert_count":
            security_alert_count,

    }


    return render(
        request,
        "dashboard/commander_dashboard.html",
        context
    )



# ==============================
# OFFICER DASHBOARD
# ==============================

@login_required
@officer_required
def officer_dashboard(request):

    user = request.user


    missions_count = Mission.objects.filter(
        assigned_to=user
    ).count()



    completed_missions_count = Mission.objects.filter(
        assigned_to=user,
        status="completed"
    ).count()



    unread_messages_count = Message.objects.filter(
        recipient=user,
        read=False
    ).count()



    security_alert_count = SuspiciousActivity.objects.filter(
        resolved=False
    ).count()



    context = {

        "missions_count":
            missions_count,


        "completed_missions_count":
            completed_missions_count,


        "unread_messages_count":
            unread_messages_count,


        "security_alert_count":
            security_alert_count,

    }



    return render(
        request,
        "dashboard/officer_dashboard.html",
        context
    )



# ==============================
# SOLDIER DASHBOARD
# ==============================

@login_required
@soldier_required
def soldier_dashboard(request):

    user = request.user


    missions_count = Mission.objects.filter(
        assigned_to=user
    ).count()



    completed_missions_count = Mission.objects.filter(
        assigned_to=user,
        status="completed"
    ).count()



    unread_messages_count = Message.objects.filter(
        recipient=user,
        read=False
    ).count()



    context = {

        "missions_count":
            missions_count,


        "completed_missions_count":
            completed_missions_count,


        "unread_messages_count":
            unread_messages_count,

    }



    return render(
        request,
        "dashboard/soldier_dashboard.html",
        context
    )



# ==============================
# PROFILE
# ==============================

@login_required
def profile(request):

    return render(
        request,
        "dashboard/profile.html"
    )



@login_required
def profile_update(request):

    if request.method == "POST":

        user=request.user

        user.first_name=request.POST.get("first_name")

        user.last_name=request.POST.get("last_name")

        user.save()


        messages.success(
            request,
            "Profile updated successfully!"
        )


        return redirect("profile")


    return render(
        request,
        "dashboard/profile.html"
    )