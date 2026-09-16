
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SuspiciousActivity(models.Model):

    RISK_CHOICES = (
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    description = models.TextField()
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES)
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.risk_level}"


class SecurityAccessLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class AISummary(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

