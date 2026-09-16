# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    man_number = models.CharField(max_length=20, unique=True)

    UNIT_CHOICES = [
        ('engineering', 'Engineering'),
        ('logistics', 'Logistics'),
        ('infantry', 'Infantry'),
    ]
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='engineering')

    ROLE_CHOICES = [
        ('soldier', 'Soldier'),
        ('officer', 'Officer'),
        ('commander', 'Commander'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='soldier')

    commander = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='soldiers'
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username or self.email