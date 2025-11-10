from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


User = get_user_model()
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)

    # Separate attachment fields
    attachment_doc = models.FileField(upload_to='attachments/docs/', null=True, blank=True)
    attachment_photo = models.ImageField(upload_to='attachments/photos/', null=True, blank=True)
    attachment_audio = models.FileField(upload_to='attachments/audio/', null=True, blank=True)

    voice_note = models.FileField(upload_to='voice_notes/', null=True, blank=True)
    
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.content[:20]}"