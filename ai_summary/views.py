from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from missions.models import Mission
from messaging.models import Message
from ai_security.models import SuspiciousActivity

from .services import build_ai_message, get_user_summary

from .models import AISummary
from .chat import ask_ai
from .utils import generate_summary


@login_required
def ai_summary_dashboard(request):

    answer = None


    if request.method == "POST":

        question = request.POST.get("question")


        if question:

            answer = ask_ai(
                request.user,
                question
            )


    return render(
        request,
        "ai_summary/dashboard.html",
        {
            "answer": answer
        }
    )

@login_required
def ai_panel(request):

    user = request.user

    summary = {
        "missions_active": Mission.objects.filter(
            assigned_to=user,
            status="active"
        ).count(),

        "unread_messages": Message.objects.filter(
            recipient=user,
            read=False
        ).count(),

        "security_alerts": SuspiciousActivity.objects.filter(
            resolved=False
        ).count(),
    }

    ai_message = build_ai_message(user, summary)

    return render(request, "ai_summary/panel.html", {
        "ai_message": ai_message
    })

@login_required
def meta_assistant(request):

    user = request.user

    summary = {
        "missions_active": Mission.objects.filter(
            assigned_to=user,
            status="active"
        ).count(),

        "unread_messages": Message.objects.filter(
            recipient=user,
            read=False
        ).count(),

        "security_alerts": SuspiciousActivity.objects.filter(
            resolved=False
        ).count(),
    }

    message = build_ai_message(user, summary)

    return render(
        request,
        "ai_summary/meta.html",
        {
            "message": message
        }
    )


