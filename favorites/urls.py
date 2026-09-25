from django.urls import path

from .views import toggle_favorite


urlpatterns = [
    path(
        "<int:pk>/toggle/",
        toggle_favorite,
        name="toggle_favorite"
    ),
]