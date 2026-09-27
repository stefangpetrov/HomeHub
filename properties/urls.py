from django.urls import path

from .views import( property_create,
    property_detail
    , property_edit,
    property_delete,
    property_list,
    property_image_delete,
)

from .api.views import (
    PropertyListAPIView,
    PropertyDetailAPIView,
)


urlpatterns = [
    path("", property_list, name="property_list"),
    path("create/", property_create, name="property_create"),
    path("<int:pk>/edit/", property_edit, name="property_edit"),
    path("<int:pk>/delete/", property_delete, name="property_delete"),
    path("images/<int:pk>/delete/", property_image_delete, name="property_image_delete"),
    path("<int:pk>/", property_detail, name="property_detail"),
    path("api/", PropertyListAPIView.as_view(), name="property_api_list"),
    path("api/<int:pk>/", PropertyDetailAPIView.as_view(), name="property_api_detail"),
]