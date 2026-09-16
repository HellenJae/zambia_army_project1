
from django.urls import path
from . import views

urlpatterns = [
    path(
        'security-center/',
        views.security_center,
        name='security_center'
    ),
    path('alert/<int:alert_id>/seen/', views.mark_alert_seen, name='mark_alert_seen'),
]

