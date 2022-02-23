from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Reviews, Rating, RatingStar


class ReviewFrom(forms.ModelForm):
    """ форма для добавления отзыва """
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


class RatingForm(forms.ModelForm):
    """ добавление рейтинга """  
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )      


    class Meta:
        model =Rating
        fields = ('star',)