from django import forms
from django.forms import ModelForm
from .models import Bracket, Player


class BracketForm(ModelForm):
    class Meta:
        model = Bracket
        fields = ('name', 'size', 'date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-element'}),
            'size': forms.NumberInput(attrs={'class': 'form-element'}),
            'date': forms.DateInput(attrs={'class': 'form-element'}),
        }
