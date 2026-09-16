from django.utils import timezone
from django.db.models import Q

from missions.models import Mission
from messaging.models import Message
from announcements.models import Announcement
from ai_security.models import SuspiciousActivity
from accounts.models import CustomUser


def ask_ai(user, question):

    q = question.lower()


    # ==========================
    # MISSIONS
    # ==========================

    if "mission" in q:

        missions = Mission.objects.filter(
            assigned_to=user
        )

        active = missions.exclude(
            status="completed"
        ).count()

        overdue = missions.filter(
            due_date__lt=timezone.now().date()
        ).exclude(
            status="completed"
        ).count()


        if overdue > 0:
            return (
                f"ORION AI REPORT:\n"
                f"You have {active} active missions. "
                f"{overdue} mission(s) are overdue."
            )


        return (
            f"ORION AI REPORT:\n"
            f"You currently have {active} active missions."
        )


    # ==========================
    # MESSAGES
    # ==========================

    if "message" in q or "inbox" in q:

        unread = Message.objects.filter(
            recipient=user,
            read=False
        ).count()


        return (
            f"COMMUNICATION REPORT:\n"
            f"You have {unread} unread message(s)."
        )


    # ==========================
    # SECURITY
    # ==========================

    if "security" in q or "threat" in q:

        alerts = SuspiciousActivity.objects.filter(
            resolved=False
        )


        high = alerts.filter(
            risk_level="HIGH"
        ).count()


        return (
            f"SECURITY REPORT:\n"
            f"Total unresolved alerts: {alerts.count()}.\n"
            f"High risk alerts: {high}."
        )


    # ==========================
    # SOLDIERS UNDER COMMAND
    # ==========================

    if "soldier" in q or "personnel" in q:

        if user.role in ["commander", "officer"]:

            soldiers = CustomUser.objects.filter(
                commander=user
            ).count()


            return (
                f"PERSONNEL REPORT:\n"
                f"You have {soldiers} soldiers under supervision."
            )

        return "You do not have command personnel assigned."


    # ==========================
    # ANNOUNCEMENTS
    # ==========================

    if "announcement" in q or "notice" in q:

        announcements = Announcement.objects.filter(
            Q(target_unit=user.unit) |
            Q(target_unit=None)
        ).order_by("-created_at")[:5]


        if announcements.exists():

            result = "LATEST ANNOUNCEMENTS:\n"

            for a in announcements:
                result += f"- {a.title}\n"

            return result


        return "No announcements found for your unit."


    # ==========================
    # GENERAL
    # ==========================

    return (
        "ORION AI ONLINE.\n\n"
        "I can help with:\n"
        "- Missions\n"
        "- Messages\n"
        "- Security\n"
        "- Personnel\n"
        "- Announcements"
    )