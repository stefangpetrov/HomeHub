from django import forms

from .models import Property, PropertyImage


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

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Modern 3-bedroom apartment",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Describe the property...",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 250000",
                    "step": "0.01",
                }
            ),

            "area": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 110",
                    "step": "0.01",
                }
            ),

            "bedrooms": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "e.g. 3",
                }
            ),

            "bathrooms": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "e.g. 2",
                }
            ),

            "floor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "e.g. 4",
                }
            ),

            "total_floors": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "e.g. 8",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Sofia",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 15 Example Street",
                }
            ),

            "property_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class PropertyImageForm(forms.ModelForm):

    class Meta:
        model = PropertyImage
        fields = ["image"]