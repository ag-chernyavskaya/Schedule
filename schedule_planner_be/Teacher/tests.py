from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Teacher


class TeacherTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='Pass1234',
            role='Super Admin'
        )
        self.teacher = Teacher.objects.create(
            surname='Зубрицкий',
            name='Александр',
            specialization='Питон',
            course_name='Python',
        )

    def test_string_representation(self):
        teacher = Teacher(surname='Тестовый', name='Преподаватель')
        self.assertEqual(str(teacher), f'{teacher.surname} {teacher.name}')

    def test_get_absolute_url(self):
        self.assertEqual(self.teacher.get_absolute_url(), '/teachers/1/')

    def test_teacher_content(self):
        self.assertEqual(f'{self.teacher.surname}', 'Зубрицкий')
        self.assertEqual(f'{self.teacher.name}', 'Александр')
        self.assertEqual(f'{self.teacher.specialization}', 'Питон')
        self.assertEqual(f'{self.teacher.course_name}', 'Python')

    def test_teacher_list_view(self):
        self.client.login(email='test@email.com', password='Pass1234')
        response = self.client.get(reverse('teacher_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Зубрицкий')
        self.assertTemplateUsed(response, 'Teacher/teacher_list.html')

    def test_teacher_detail_view(self):
        self.client.login(email='test@email.com', password='Pass1234')
        response = self.client.get('/teachers/1/')
        no_response = self.client.get('/teachers/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Зубрицкий')
        self.assertTemplateUsed(response, 'Teacher/teacher_detail.html')

    def test_teacher_create_view(self):
        self.client.login(email='test@email.com', password='Pass1234')
        response = self.client.post(reverse('teacher_form'), data={
            'surname': 'Новый',
            'name': 'Преподаватель',
            'specialization': 'Питон',
            'course_name': ['Основы разработки сайтов', 'Python'],
        })
        self.assertEqual(Teacher.objects.count(), 2)
        self.assertRedirects(response, "/teachers/")

    def test_teacher_update_view(self):
        self.client.login(email='test@email.com', password='Pass1234')
        response = self.client.post(reverse('teacher_edit', args='1'), {
            'surname': 'Изменение',
            'name': 'Преподавателя',
            'specialization': 'Стажировка',
            'course_name': ['Python']
        })
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.specialization, 'Стажировка')
        self.assertEqual(self.teacher.name, 'Преподавателя')
        self.assertRedirects(response, "/teachers/")

    def test_teacher_delete_view(self):
        self.client.login(email='test@email.com', password='Pass1234')
        response = self.client.get(
            reverse('teacher_confirm_delete', args='1'))
        self.assertContains(response, 'Вы уверены, что хотите удалить профиль')