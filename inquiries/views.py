from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Property

from .forms import InquiryForm
from .models import Inquiry


@login_required
def create_inquiry(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        form = InquiryForm(request.POST)

        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.property = property
            inquiry.save()

            return redirect(
                "property_detail",
                pk=property.pk
            )

    else:
        form = InquiryForm()

    context = {
        "form": form,
        "property": property,
    }

    return render(
        request,
        "inquiries/inquiry_form.html",
        context
    )

@login_required
def inquiry_list(request):

    if request.user.role not in [
        request.user.Role.AGENT,
        request.user.Role.ADMIN,
    ]:
        return HttpResponseForbidden()

    if request.user.role == request.user.Role.ADMIN:
        inquiries = Inquiry.objects.all()
    else:
        inquiries = Inquiry.objects.filter(
            property__owner=request.user
        )

    inquiries = inquiries.select_related(
        "property",
        "user"
    ).order_by("-created_at")

    context = {
        "inquiries": inquiries,
    }

    return render(
        request,
        "inquiries/inquiry_list.html",
        context
    )

@login_required
def update_inquiry_status(request, pk):

    inquiry = get_object_or_404(
        Inquiry,
        pk=pk
    )

    if request.user.role == request.user.Role.ADMIN:
        can_update = True

    elif (
        request.user.role == request.user.Role.AGENT
        and inquiry.property.owner == request.user
    ):
        can_update = True

    else:
        can_update = False

    if not can_update:
        return HttpResponseForbidden()

    if request.method == "POST":

        status = request.POST.get("status")

        valid_statuses = [
            choice[0]
            for choice in Inquiry.Status.choices
        ]

        if status in valid_statuses:
            inquiry.status = status
            inquiry.save(update_fields=["status"])

    return redirect("inquiry_list")