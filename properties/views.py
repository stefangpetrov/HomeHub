from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

from .models import Property, PropertyImage
from .forms import PropertyForm


def property_list(request):
    properties = Property.objects.all()

    search_query = request.GET.get("search", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    property_type = request.GET.get("property_type", "")
    city = request.GET.get("city", "")
    min_bedrooms = request.GET.get("min_bedrooms", "")

    if search_query:
        properties = properties.filter(
            title__icontains=search_query
        )

    if min_price:
        properties = properties.filter(
            price__gte=min_price
        )

    if max_price:
        properties = properties.filter(
            price__lte=max_price
        )

    if property_type:
        properties = properties.filter(
            property_type=property_type
        )

    if city:
        properties = properties.filter(
            city__icontains=city
        )

    if min_bedrooms:
        properties = properties.filter(
            bedrooms__gte=min_bedrooms
        )

    paginator = Paginator(properties, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "properties": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "min_price": min_price,
        "max_price": max_price,
        "property_type": property_type,
        "city": city,
        "min_bedrooms": min_bedrooms,
        "property_types": Property.PropertyType.choices,
    }

    return render(request, "properties/property_list.html", context)

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    context = {
        "property": property,
    }

    return render(request, "properties/property_detail.html", context)

@login_required
def property_create(request):
    if request.user.role not in [
        request.user.Role.AGENT,
        request.user.Role.ADMIN,
    ]:
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = PropertyForm(request.POST)

        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save() 

            for image in request.FILES.getlist("images"):
                PropertyImage.objects.create(
                property=property,
                image=image
            )

            return redirect("property_detail", pk=property.pk)

    else:
        form = PropertyForm()

    context = {
        "form": form,
    }

    return render(request, "properties/property_form.html", context)

@login_required
def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if request.user.role == request.user.Role.ADMIN:
        can_edit = True
    elif (
        request.user.role == request.user.Role.AGENT
        and property.owner == request.user
    ):
        can_edit = True
    else:
        can_edit = False

    if not can_edit:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property)

        if form.is_valid():
            form.save()

            for image in request.FILES.getlist("images"):
                PropertyImage.objects.create(
                    property=property,
                    image=image
                )

            return redirect("property_detail", pk=property.pk)

    else:
        form = PropertyForm(instance=property)

    context = {
        "form": form,
        "property": property,
    }

    return render(request, "properties/property_form.html", context)

@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if request.user.role == request.user.Role.ADMIN:
        can_edit = True
    elif (
        request.user.role == request.user.Role.AGENT
        and property.owner == request.user
    ):
        can_edit = True
    else:
        can_edit = False
    
    if not can_edit:
        return HttpResponseForbidden()

    if property.owner != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        property.delete()
        return redirect("property_list")

    context = {
        "property": property,
    }

    return render(request, "properties/property_confirm_delete.html", context)


@login_required
def property_image_delete(request, pk):
    image = get_object_or_404(PropertyImage, pk=pk)
    property = image.property

    if request.user.role == request.user.Role.ADMIN:
        can_delete = True
    elif (
        request.user.role == request.user.Role.AGENT
        and property.owner == request.user
    ):
        can_delete = True
    else:
        can_delete = False

    if not can_delete:
        return HttpResponseForbidden()

    if request.method == "POST":
        image.delete()

    return redirect("property_detail", pk=property.pk)