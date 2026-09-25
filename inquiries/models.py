from django.conf import settings
from django.db import models

from properties.models import Property


class Inquiry(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="inquiries"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inquiries"
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CONTACTED = "CONTACTED", "Contacted"
        CLOSED = "CLOSED", "Closed"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NEW
    )

    def __str__(self):
        return f"Inquiry from {self.user.username} - {self.property.title}"