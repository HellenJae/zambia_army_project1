
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SuspiciousActivity
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def security_center(request):

    alerts = SuspiciousActivity.objects.all().order_by('-detected_at')

    return render(request, 'ai_security/security_center.html', {
        'alerts': alerts
    })

@login_required
def mark_alert_seen(request, alert_id):
    alert = get_object_or_404(SuspiciousActivity, id=alert_id)

    alert.resolved = True
    alert.save()

    return redirect('security_center')
