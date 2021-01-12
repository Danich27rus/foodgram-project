from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.EmailField(help_text='Required')

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')
        labels = {
            'first_name': 'Имя',
            'username': 'Имя пользователя',
            'email': 'Адрес электронной почты',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
