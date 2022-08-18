from django import forms
from .models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))

    class Meta:
        model = User
        fields = [
            "phone_number",
            "username",
            "email",
            "password",
            "password2",

        ]

    def clean_password2(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]

        if password == password2:
            return password2
        raise forms.ValidationError("password donot match")


class LoginForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))

    class Meta:
        model = User
        fields = ["username", "password"]


class UserUpdateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "image"]


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))

    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))

    class Meta:
        model = User
        fields = ["old_password", "new_password", "password_confirmation"]
