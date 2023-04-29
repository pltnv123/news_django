from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django.utils.translation import gettext as _

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name=_("player"))
        user.groups.add(authors)
        return user

class SignUpForm(UserCreationForm):
    username = forms.CharField(label=_("Имя пользователя"))
    first_name = forms.CharField(label=_("Ваше имя"))
    last_name = forms.CharField(label=_("Ваша фамилия"))
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(label=_("Пароль"))
    password2 = forms.CharField(label=_("Повторите пароль"))

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