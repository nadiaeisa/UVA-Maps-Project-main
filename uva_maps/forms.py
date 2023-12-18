from django import forms
from .models import Feedback
from .models import PlaceRating

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['place','address','justification']

class PlaceRatingForm(forms.ModelForm):
    class Meta:
        model = PlaceRating
        fields = ['rating']
