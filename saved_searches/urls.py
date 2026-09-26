from django.urls import path

from .views import (
    delete_saved_search,
    save_search,
    saved_search_list,
)


urlpatterns = [
    path(
        "save/",
        save_search,
        name="save_search"
    ),
    path(
        "",
        saved_search_list,
        name="saved_search_list"
    ),
    path(
        "<int:pk>/delete/",
        delete_saved_search,
        name="delete_saved_search"
    ),
]