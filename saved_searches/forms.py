from django import forms

from .models import SavedSearch


class SavedSearchForm(forms.ModelForm):

    class Meta:
        model = SavedSearch
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Sofia apartments under €250,000",
                }
            ),
        }