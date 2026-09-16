
from .models import SuspiciousActivity
from django.contrib.auth.models import User


def detect_failed_logins(user, failed_attempts):

    if failed_attempts >= 5:

        SuspiciousActivity.objects.create(
            user=user,
            activity_type="Failed Login Attempts",
            description=f"{failed_attempts} failed login attempts detected.",
            risk_level="HIGH"
        )

        return True

    return False

