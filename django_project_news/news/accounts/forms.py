from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name="player")
        user.groups.add(authors)
        return user

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    first_name = forms.CharField(label="Ваше имя")
    last_name = forms.CharField(label="Ваша фамилия")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Повторите пароль")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )