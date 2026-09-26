from django.conf import settings
from django.db import models

from properties.models import Property


class SavedSearch(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_searches"
    )

    name = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    property_type = models.CharField(
        max_length=20,
        choices=Property.PropertyType.choices,
        blank=True
    )

    min_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    max_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    min_bedrooms = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    

class Notification(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    saved_search = models.ForeignKey(
        SavedSearch,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.message}"