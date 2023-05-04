from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=75)
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        fields = ('first_name','last_name','email','password1')