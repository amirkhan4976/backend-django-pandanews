from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]


class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ["owner"]
