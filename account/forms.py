from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)

User = get_user_model()


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).count():
            raise forms.ValidationError(f"Пользователь c ящиком {email} "
                                        "уже существует.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).count():
            raise forms.ValidationError(f"Пользователь {username} "
                                        "уже существует.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user


class ResetForm(PasswordResetForm):

    help_text = ("Чтобы сбросить старый пароль — введите адрес "
                 "электронной почты, под которым вы регистрировались.")

    name = "Адрес электронной почты:"

    email = forms.EmailField(label=name, max_length=254, required=True,
                             help_text=help_text)


class SigninForm(AuthenticationForm):

    class Meta:

        model = User
        fields = {"username", "password", }

        error_messages = {
            "required": "Это поле необходимо заполнить.",
            "invalid_login": (
                "Имя и пароль не совпадают. Введите "
                "правильные данные."
            ),
            "inactive": "Этот аккаунт не активен.",
        }


class UserPasswordResetForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label="Пароль",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password",
                "type": "password",
                "id": "user_password",
            }
        )
    )

    new_password2 = forms.CharField(
        label="Confirm password",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "confirm password",
                "type": "password",
                "id": "user_password",
            }
        )
    )
