from django.shortcuts import render

from properties.models import Property


def home(request):
    featured_properties = Property.objects.filter(
        status=Property.Status.ACTIVE
    ).order_by("-created_at")[:6]

    context = {
        "featured_properties": featured_properties,
    }

    return render(request, "core/home.html", context)