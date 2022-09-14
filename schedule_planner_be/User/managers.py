import re
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Создание пользовательского Manager, который использует
    email в качестве уникального идентификатора вместо username"""
    def create_user(self, email, password, **extra_fields):
        """Создание и сохранение пользователя с введенным email и паролем"""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if len(password) != 8:
            raise ValueError(_('Password should have 8 symbols'))
        if (bool(re.search(r'[A-Z]', password))) is not True:
            raise ValueError(_('Password should have one uppercase letter'))
        if (bool(re.search(r'[a-z]', password))) is not True:
            raise ValueError(_('Password should have one lowercase letter'))
        if (bool(re.search(r'[0-9]', password))) is not True:
            raise ValueError(_('Password should have one digit'))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создание и сохранение суперпользователя с введенным email и паролем"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'Super Admin')
        extra_fields.setdefault('email_verify', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))
        return self.create_user(email, password, **extra_fields)


