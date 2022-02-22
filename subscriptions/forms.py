from django import forms
from .models import Subscriptions


class SubscriptionsForm(forms.ModelForm):
    """ форма для email подписки """
    class Meta:
        model = Subscriptions
        fields = ('email', )
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})

        }
        labels = {
            'email': ''
        }