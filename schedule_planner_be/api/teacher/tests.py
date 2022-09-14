from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from . import views
from Teacher.models import Teacher


class TestTeacher(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            first_name='Тест',
            password='Pass1234',
            role='Super Admin'
        )
        self.user.save()
        self.teacher = Teacher.objects.create(
            surname='Зубрицкий',
            name='Александр',
            specialization='Питон',
            course_name='Python',
        )
        self.teacher.save()

    def test_list_teacher(self):
        request = self.factory.get('/api/v1/teachers/')
        request.user = self.user
        response = views.TeacherListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Александр')

    def test_detail_teacher(self):
        request = self.factory.get('/api/v1/teachers/')
        request.user = self.user
        response = views.TeacherDetailsView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Питон')

    def test_create_teacher(self):
        request = self.factory.post('/api/v1/teachers/new/', {
            "surname": 'Тестовое',
            "name": 'Создание',
            "specialization": 'Питон',
            "course_name": 'Основы разработки сайтов',
        })
        request.user = self.user
        response = views.TeacherCreateView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Teacher.objects.count(), 2)

    def test_teacher_update_view(self):
        request = self.factory.put('/api/v1/teachers/edit/', data={
            "surname": 'Тестовое',
            "name": 'Изменение',
            "specialization": 'Сайт',
            "course_name": ['Тестирование ПО']
        })
        request.user = self.user
        response = views.TeacherUpdateView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.specialization, 'Сайт')
        self.assertEqual(self.teacher.surname, 'Тестовое')

    def test_teacher_delete_view(self):
        request = self.factory.delete('/api/v1/teachers/delete/')
        request.user = self.user
        response = views.TeacherDeleteView.as_view()(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Teacher.objects.count(), 1)
