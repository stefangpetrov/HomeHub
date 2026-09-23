from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.



class Property(models.Model):

    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    bedrooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    bathrooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    floor = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    total_floors = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    floor = models.PositiveIntegerField()
    total_floors = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="properties"
    )

    class PropertyType(models.TextChoices):
        APARTMENT = "APARTMENT", "Apartment"
        HOUSE = "HOUSE", "House"
        STUDIO = "STUDIO", "Studio"
        OFFICE = "OFFICE", "Office"
        LAND = "LAND", "Land"

    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices
    )

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SOLD = "SOLD", "Sold"
        RENTED = "RENTED", "Rented"
        INACTIVE = "INACTIVE", "Inactive"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    def clean(self):
            if self.floor > self.total_floors:
                raise ValidationError({
                    "floor": "Floor cannot be greater than total floors."
                })

    def __str__(self):
        return self.title


