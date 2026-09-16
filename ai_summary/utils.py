from django.utils import timezone

from accounts.models import CustomUser
from missions.models import Mission
from messaging.models import Message
from announcements.models import Announcement
from ai_security.models import SuspiciousActivity, AISummary



def generate_summary(user):

    today = timezone.now().date()

    report = []


    # =====================================================
    # COMMANDER REPORT
    # =====================================================

    if user.role == "commander":

        report.append("COMMAND REPORT")
        report.append("--------------------------------")


        # Personnel
        soldiers = CustomUser.objects.filter(
            commander=user
        )


        report.append(
            f"Personnel: {soldiers.count()} soldiers under command supervision."
        )


        # Operations

        active_missions = Mission.objects.filter(
            assigned_to=user,
            status="in_progress"
        )


        overdue_missions = Mission.objects.filter(
            assigned_to=user,
            due_date__lt=today
        )


        due_today = Mission.objects.filter(
            assigned_to=user,
            due_date=today
        )


        report.append(
            f"Operations: {active_missions.count()} active missions."
        )


        if overdue_missions.exists():

            report.append(
                f"WARNING: {overdue_missions.count()} mission(s) overdue."
            )


        if due_today.exists():

            report.append(
                f"Attention: {due_today.count()} mission(s) due today."
            )



        # Communications

        unread_messages = Message.objects.filter(
            recipient=user,
            read=False
        ).count()


        report.append(
            f"Communications: {unread_messages} unread messages."
        )



        # Security

        high_alerts = SuspiciousActivity.objects.filter(
            risk_level="HIGH",
            resolved=False
        ).count()


        report.append(
            f"Security: {high_alerts} high-risk alert(s)."
        )



    # =====================================================
    # OFFICER REPORT
    # =====================================================

    elif user.role == "officer":


        report.append("OFFICER REPORT")
        report.append("--------------------------------")


        missions = Mission.objects.filter(
            assigned_to=user
        )


        report.append(
            f"Assigned missions: {missions.count()}."
        )


        for mission in missions[:5]:

            report.append(
                f"- {mission.title}"
            )



        announcements = Announcement.objects.filter(
            target_unit=user.unit
        ).order_by(
            "-created_at"
        )[:5]


        report.append(
            "Unit announcements:"
        )


        for announcement in announcements:

            report.append(
                f"- {announcement.title}"
            )



        unread = Message.objects.filter(
            recipient=user,
            read=False
        ).count()


        report.append(
            f"Communications: {unread} unread message(s)."
        )



    # =====================================================
    # SOLDIER REPORT
    # =====================================================

    else:


        report.append("FIELD REPORT")
        report.append("--------------------------------")


        missions = Mission.objects.filter(
            assigned_to=user
        )


        report.append(
            "Your missions:"
        )


        for mission in missions[:5]:

            if mission.due_date:

                report.append(
                    f"- {mission.title} (Due {mission.due_date})"
                )

            else:

                report.append(
                    f"- {mission.title}"
                )



        unread = Message.objects.filter(
            recipient=user,
            read=False
        ).count()


        report.append(
            f"Messages: {unread} new instruction(s)."
        )



        announcements = Announcement.objects.filter(
            target_unit=user.unit
        ).order_by(
            "-created_at"
        )[:5]


        report.append(
            "Announcements:"
        )


        for announcement in announcements:

            report.append(
                f"- {announcement.title}"
            )



    final_report = "\n".join(report)



    # Save AI briefing

    AISummary.objects.create(
        user=user,
        title="Orion AI Military Briefing",
        summary=final_report
    )


    return final_report