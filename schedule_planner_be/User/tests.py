from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import UserCreationForm
from .models import User


class UserManagersTests(TestCase):
    """Тестирование пользовательского Manager"""
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='Normal@user.com', password='123456Aa')
        self.assertEqual(user.email, 'Normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='123456Aa')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='Super@user.com', password='123456Aa')
        self.assertEqual(admin_user.email, 'Super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='Supertest@user.com', password='123456Aa', is_superuser=False)


class SignupPageTests(TestCase):
    """Тестирование регистрации"""
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'User/signup.html')
        self.assertContains(self.response, 'Sign Up')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_user_create_view(self):
        response = self.client.post(reverse('signup'), data={
            'email': 'test@mail.ru',
            'password1': '123456Aa',
            'password2': '123456Aa',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'role': 'Super Admin'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, "/user/confirm_email/")


class LoginPageTests(TestCase):
    """Тестирование входа"""
    def setUp(self):
        url = '/user/login/'
        self.response = self.client.get(url)

    def test_login_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/login.html')
        self.assertContains(self.response, 'Sign In')
