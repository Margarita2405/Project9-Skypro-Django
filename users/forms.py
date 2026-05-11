from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "password1", "password2")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "avatar", "country")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }
