from django import forms
from django.forms import ImageField

from beerFriends.models import Beer


class BeerForm(forms.ModelForm):
    image = ImageField()

    class Meta:
        model = Beer
        fields = ('name', 'origin', 'alcoholContent')
