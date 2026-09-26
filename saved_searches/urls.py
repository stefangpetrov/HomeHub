from django.urls import path

from .views import (
    delete_saved_search,
    delete_notification,
    mark_notification_as_read,
    notification_list,
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
    path(
        "notifications/",
        notification_list,
        name="notification_list"
    ),
    path(
        "notifications/<int:pk>/read/",
        mark_notification_as_read,
        name="mark_notification_as_read"
    ),
    path(
        "notifications/<int:pk>/delete/",
        delete_notification,
        name="delete_notification"
    ),
]