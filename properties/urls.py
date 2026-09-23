from django.urls import path

from .views import property_create, property_detail, property_edit, property_delete, property_list


urlpatterns = [
    path("", property_list, name="property_list"),
    path("create/", property_create, name="property_create"),
    path("<int:pk>/edit/", property_edit, name="property_edit"),
    path("<int:pk>/delete/", property_delete, name="property_delete"),
    path("<int:pk>/", property_detail, name="property_detail"),
]