from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Mission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
