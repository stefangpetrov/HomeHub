from django.urls import path

from .views import (
    create_inquiry,
    inquiry_list,
    update_inquiry_status,
)


urlpatterns = [
    path(
        "",
        inquiry_list,
        name="inquiry_list"
    ),
    path(
        "<int:pk>/create/",
        create_inquiry,
        name="create_inquiry"
    ),
    path(
        "<int:pk>/status/",
        update_inquiry_status,
        name="update_inquiry_status"
    ),
]