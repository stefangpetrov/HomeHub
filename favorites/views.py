from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from properties.models import Property

from .models import Favorite


@login_required
def toggle_favorite(request, pk):
    property = get_object_or_404(Property, pk=pk)

    favorite = Favorite.objects.filter(
        user=request.user,
        property=property
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            property=property
        )

    return redirect("property_detail", pk=property.pk)