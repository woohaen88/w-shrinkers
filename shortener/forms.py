import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from shortener.models import Users as UserModel


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=False, help_text='Optional', label= "이름")
    username = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required', label= "e-mail")   

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

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
    email = forms.CharField(
        max_length=100, required=True, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "이메일"})
    )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"}),
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input", "id": "_loginRememberMe"}),
        required=False,
        disabled=False,
    )

    class Meta:
        model = UserModel
        fields = (
            'email',
            'password',
            'remember_me',
        )