from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       UserCreationForm, SetPasswordForm)
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if (User.objects
                .exclude(pk=self.instance.pk)
                .filter(email=email).filter(is_active=True).exists()):
            raise forms.ValidationError(f"Пользователь c ящиком {email} " +
                                        "уже существует.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if (User.objects
                .exclude(pk=self.instance.pk)
                .filter(username=username).exists()):
            raise forms.ValidationError(f"Пользователь {username} "
                                        "уже существует.")
        return username


class ResetForm(PasswordResetForm):
    help_text = ("Чтобы сбросить старый пароль — введите адрес " +
                 "электронной почты, под которым вы регистрировались.")
    name = "Адрес электронной почты."
    email = forms.EmailField(label=name, max_length=254, required=True,
                             help_text=help_text)


class SigninForm(AuthenticationForm):

    error_messages = {
        'required': "Это поле необходимо заполнить.",
        'invalid_login': _(
            "Имя и пароль не совпадают. Введите "
            "правильные данные."
        ),
        'inactive': "Этот аккаунт не активен.",
    }

    class Meta:

        model = User
        fields = {'username', 'password', }

        error_messages = {
            'required': "Это поле необходимо заполнить.",
            'invalid_login': _(
                "Имя и пароль не совпадают. Введите "
                "правильные данные."
            ),
            'inactive': "Этот аккаунт не активен.",
        }


class UserPasswordResetForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label='Пароль',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
                'type': 'password',
                'id': 'user_password',
            })
        )

    new_password2 = forms.CharField(
        label='Confirm password',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'confirm password',
                'type': 'password',
                'id': 'user_password',
            })
        )
