from django import forms

from beerFriends.models import Review


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('creator',)
        fields = ['rating', 'text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ReviewCreateForm, self).__init__(*args, **kwargs)
