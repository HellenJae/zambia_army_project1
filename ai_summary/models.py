from django.db import models
from django.conf import settings


class AISummary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_summaries"
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    seen = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title