from django.urls import path

from .views import favorite_list, toggle_favorite


urlpatterns = [
    path("", favorite_list, name="favorite_list"),
    path(
        "<int:pk>/toggle/",
        toggle_favorite,
        name="toggle_favorite"
    ),
]