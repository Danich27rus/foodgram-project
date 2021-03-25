from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.decorators.http import require_http_methods

from recipes.models import Recipe, Tag

from .forms import ResetForm, SignupForm, UserPasswordResetForm
from .tokens import account_activation_token

User = get_user_model()

@require_http_methods(["GET", "POST"])
def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Активируйте Ваш foodgram аккаунт."
            message = render_to_string(
                "account/password/activateEmail.html", {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            msg_confirm = ("Инструкция по активации была отправлена на ящик "
                           f"{to_email}")
            return render(
                request,
                "account/signin.html",
                {'msg': msg_confirm}
            )
    else:
        form = SignupForm()
    return render(request, "account/signup.html", {'form': form})


@require_http_methods(["GET", "POST"])
def signin(request):

    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user.is_active:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, "account/signin.html", {'form': form})


def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        msg_success = "Успешная активация аккаунта."
        return render(
            request, "account/signup.html", {'msg': msg_success}
        )
    else:
        msg_failed = "Ссылка не действительна."
        return render(request, "account/signup.html", {'msg': msg_failed})


@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, "Ваш пароль успешно изменен!")
            return redirect('signin')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки.")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request, 'account/password/change.html',
        {'form': form, 'title': 'Изменение пароля'}
    )


@require_http_methods(["GET", "POST"])
def reset_password(request):

    msg = ''
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            qs = list(form.get_users(to_email))
            if len(qs):
                user = qs[0]
                user.is_active = False
                user.save()
                site = get_current_site(request)
                mail_subject = "Сброс пароля foodgram аккаунта."
                message = render_to_string(
                    "account/password/resetEmail.html", {
                        'user': user,
                        'protocol': 'http',
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                msg = "Сообщение отправлено. Проверьте почтовый ящик."
                return render(request, "account/signin.html",
                              {'form': form, 'msg': msg})
            else:
                msg = "Почтовый ящик не найден."
        else:
            return render(request, "account/signin.html",
                          {'form': form, 'msg': msg})
    return render(request, "account/password/resetPassword.html",
                  {'form': ResetForm, 'msg': msg})


@require_http_methods(["GET", "POST"])
def reset_confirm(request, uidb64, token):

    if request.method == 'POST':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = UserPasswordResetForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                user.is_active = True
                user.save()
                return redirect('index')
            else:
                msg = "Пароль не может быть сброшен."
                return render(request, "account/signin.html",
                              {'form': form, 'msg': msg})
        else:
            msg = "Неверная ссылка. Пожалуйста, запросите новый сброс пароля."
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        return render(request, 'account/password/resetPasswordConfirm.html', {
            'form': UserPasswordResetForm(user),
            'uid': uidb64,
            'token': token}
        )
    else:
        msg = "Неверная ссылка. Пожалуйста, запросите новый сброс пароля."
        return render(request, "account/password/resetPassword.html",
                      {'form': ResetForm, 'msg': msg})
    return render(request, "account/signin.html",
                  {'form': form, 'msg': msg})


class ProfileView(View):

    def get_queryset(self, request, author):

        tags = request.GET.getlist('filters')
        if not tags:
            recipes = Recipe.objects.filter(author=author).exclude(
                tags__slug__in=tags)
        else:
            recipes = Recipe.objects.filter(author=author).filter(
                tags__slug__in=tags)
        return recipes

    def get(self, request, user_id):

        author = get_object_or_404(User, id=user_id)
        recipes = self.get_queryset(request, author)
        paginator = Paginator(recipes.filter(author=author), 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        tags = Tag.objects.all()
        context = {'author': author,
                   'page': page,
                   'paginator': paginator,
                   'tags': tags,
                   }
        return render(request, "recipes/profile.html", context)
