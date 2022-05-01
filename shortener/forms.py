import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from shortener.models import Users as UserModel


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=False, help_text='Optional', label= "이름")
    username = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required', label= "e-mail")


    class Meta:
        model = UserModel
        fields = (
            "username",
            "full_name",
            "email",
            "password1",
            "password2",
        )

class SigninForm(forms.ModelForm):
    email = forms.CharField(max_length=254, help_text="Required", label="email", widget=forms.EmailInput())
    password = forms.CharField(max_length=20, help_text="Required", label="password", widget=forms.PasswordInput())

    class Meta:
        model = UserModel
        fields = (
            "email",
            "password"
        )