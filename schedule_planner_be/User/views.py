import datetime
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View
from .forms import UserCreationForm, UserAuthenticationForm, MySetPasswordForm
from .service import send
import pytz


utc = pytz.UTC
User = get_user_model()


class SendRepeatMessage(View):
    """Повторная отправка ссылки для потвеждения регистрации"""
    def get(self, request):
        email = self.request.GET.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValueError('No user with such email')
        last_mail = user.last_send_mail.replace(tzinfo=utc) + datetime.timedelta(hours=3)
        now = (datetime.datetime.now() - datetime.timedelta(minutes=1)).replace(tzinfo=utc)
        if user.email_verify:
            return redirect('complete_verify_email')
        else:
            if now > last_mail:
                send(request, user)
                user.last_send_mail = datetime.datetime.now()
                user.save()
                return redirect('send_message')
            else:
                raise ValueError('Wait for 60 seconds to pass')


class MyLoginView(LoginView):
    """Логин"""
    form_class = UserAuthenticationForm
    template_name = 'registration/login.html'
    success_url = "/courses/lesson/"


class EmailVerify(View):
    """Верификация email"""

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            # login(request, user)
            return redirect('login')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user


class SignUp(generic.CreateView):
    """Регистрация"""
    form_class = UserCreationForm
    template_name = 'User/signup.html'
    success_url = "/courses/lesson/"

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """Сброс пароля"""
    form_class = MySetPasswordForm
