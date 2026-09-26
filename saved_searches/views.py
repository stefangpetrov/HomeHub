from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib import messages

from .forms import SavedSearchForm
from .models import Notification, SavedSearch


@login_required
def save_search(request):

    if request.method == "POST":

        form = SavedSearchForm(request.POST)

        if form.is_valid():

            city = request.POST.get("city", "")
            property_type = request.POST.get(
                "property_type",
                ""
            )
            min_price = request.POST.get("min_price", "")
            max_price = request.POST.get("max_price", "")
            min_bedrooms = request.POST.get("min_bedrooms", "")

            if not any([
                city,
                property_type,
                min_price,
                max_price,
                min_bedrooms,
            ]):
                messages.error(
                    request,
                    "Please select at least one filter before saving this search."
                )
                return redirect("property_list")

            saved_search = form.save(commit=False)

            saved_search.user = request.user
            saved_search.city = city
            saved_search.property_type = property_type
            saved_search.min_price = min_price or None
            saved_search.max_price = max_price or None
            saved_search.min_bedrooms = min_bedrooms or None

            saved_search.save()

            return redirect("saved_search_list")

    return redirect("property_list")


@login_required
def saved_search_list(request):

    saved_searches = SavedSearch.objects.filter(
        user=request.user
    ).order_by("-created_at")

    context = {
        "saved_searches": saved_searches,
    }

    return render(
        request,
        "saved_searches/saved_search_list.html",
        context
    )


@login_required
def delete_saved_search(request, pk):

    saved_search = get_object_or_404(
        SavedSearch,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        saved_search.delete()

    return redirect("saved_search_list")


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).select_related(
        "property",
        "saved_search"
    ).order_by("-created_at")

    context = {
        "notifications": notifications,
    }

    return render(
        request,
        "saved_searches/notification_list.html",
        context
    )

@login_required
def mark_notification_as_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    return redirect("notification_list")


def unread_notification_count(request):

    if not request.user.is_authenticated:
        return {
            "unread_notification_count": 0
        }

    return {
        "unread_notification_count": request.user.notifications.filter(
            is_read=False
        ).count()
    }

@login_required
def delete_notification(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        notification.delete()

    return redirect("notification_list")