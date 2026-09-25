from django import forms

from .models import Inquiry


class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ["message"]

        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Write your message..."
                }
            )
        }