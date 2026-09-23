from django import forms

from .models import Property


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "price",
            "area",
            "bedrooms",
            "bathrooms",
            "floor",
            "total_floors",
            "city",
            "address",
            "property_type",
            "status",
        ]