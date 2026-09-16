from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Announcement(models.Model):

    ROLE_CHOICES = [
        ("all", "All"),
        ("commander", "Commander"),
        ("officer", "Officer"),
        ("soldier", "Soldier"),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()

    attachment = models.FileField(
        upload_to="announcements/",
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    target_unit = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    target_role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="all"
    )

    def __str__(self):
        return self.title