from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from . import views
from User.models import User


class TestUser(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            first_name='Тест',
            email='test@email.com',
            password='Pass1234',
            role='Super Admin'
        )
        self.user.save()

    def test_list_user(self):
        request = self.factory.get('/api/v1/')
        request.user = self.user
        response = views.UserListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test@email.com')

    def test_create_user(self):
        request = self.factory.post('/api/v1/new/', {
            "email": 'test1@mail.ru',
            "first_name": 'Тестовый',
            "role": 'Manager',
            "password": 'Pass1234'
        })
        request.user = self.user
        response = views.UserCreateView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
