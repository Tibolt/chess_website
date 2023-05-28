from django import forms
from django.forms import ModelForm
from .models import Bracket, Player


class BracketForm(ModelForm):
    class Meta:
        model = Bracket
        fields = ('name', 'date', "numberOfRounds")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-element'}),
            'date': forms.DateInput(attrs={'class': 'form-element'}),
            "numberOfRounds": forms.NumberInput(attrs={'class': 'form-element'}),
        }

class PlayersForm(ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'last_name', 'age', 'rating', 'score')
