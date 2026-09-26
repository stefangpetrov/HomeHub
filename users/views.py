from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("property_list")

    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }

    return render(request, "users/register.html", context)