from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Создание модели пользователя"""
    email = models.EmailField(_('Email'), max_length=150, unique=True,
                              help_text=_('Enter email in format example@gmail.ru'), validators=[
        RegexValidator(
            regex="^([A-Za-z0-9]{1}[-!#$%&'*+./=?^_`{}|~A-Za-z0-9]{1,63})@([A-za-z0-9]{1,}\.){1,2}[A-za-z0-9-]{2,63}$",
            message=_('Invalid email'),
            code=_('invalid_email')
        ),
    ], error_messages={
            "unique": _("The email has been already registered. Please, sign in using this email")})
    ROLE_CHOICES = [
        ('Super Admin', 'Super Admin'),
        ('Administrator', 'Administrator'),
        ('Manager', 'Manager'),
    ]
    role = models.CharField(_('Role'), max_length=15, choices=ROLE_CHOICES, default='Manager')
    first_name = models.CharField(_('Name'), validators=[
        RegexValidator(
            regex="^[А-Яа-я0-9]{,50}$",
            message=_('Invalid name'),
            code=_('invalid_name')
        )], max_length=50)
    last_name = models.CharField(_('Surname'), max_length=100, blank=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now=True)
    image = models.ImageField(_('Photo'), upload_to='Users/', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verify = models.BooleanField(default=False)
    last_send_mail = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



