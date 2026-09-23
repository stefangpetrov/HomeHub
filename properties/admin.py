from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "property_type",
        "status",
        "price",
        "area",
        "city",
        "owner",
        "created_at",
    )