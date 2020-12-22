from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Stock


class ShareForm(forms.Form):
    error_css_class = "alert alert-danger"

    amount = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Amount"
    )

    value = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Value"
    )

    stock = forms.ModelChoiceField(queryset=Stock.objects.all())


    def clean_title(self):
        data = self.cleaned_data['title']

        if data == "error":
            raise ValidationError(_('Validation Error !!'))

        return 