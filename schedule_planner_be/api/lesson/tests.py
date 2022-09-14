from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from Teacher.models import Teacher
from User.models import User
from course.models import Course, Lesson
from schedule.models import SubwayStation, Classroom, Location


class TestLessonList(APITestCase):
    """
    Ensure we can view a list of Lesson objects.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        self.uri = '/api/v1/lessons/'

    def test_list_lesson(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestsLessonCreateSuperAdmin(APITestCase):
    """
    Ensure Super Admin can create a new Lesson object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        teacher = Teacher.objects.create(surname='Тестов', name='Тест', specialization='тесты',
                                         course_name=['IT-рекрутер', 'Бизнес-анализ'], is_active=True)
        subwaystation = SubwayStation.objects.create(station='Test station')
        location = Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)
        classroom = Classroom.objects.create(classroom="111", seats_number=111, pc_number=111, location=location)
        date_object = datetime.strptime('2022-09-01', '%Y-%m-%d')
        course = Course.objects.create(course_name='Тестовый курс', start_date=date_object,
                                       days_of_week=[1, 3], location=classroom, start_time='09:00',
                                       number_of_lessons=3, url='1')

    def test_create_lesson(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/lessons/new/"
        data = {
            'number': 1,
            'course': 1,
            'teacher': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 5)
        # self.assertEqual(Lesson.objects.get(pk=1).teacher, 1)



# class TestsLessonCreateAdministrator(APITestCase):
#     """
#     Ensure Administrator cannot create a new Lesson object.
#     """
#
#     def setUp(self):
#         self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Administrator")
#         self.factory = APIRequestFactory()
#         teacher = Teacher.objects.create(surname='Тестов', name='Тест', specialization='тесты',
#                                          course_name=['IT-рекрутер', 'Бизнес-анализ'], is_active=True, url='2')
#         subwaystation = SubwayStation.objects.create(station='Test station')
#         location = Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)
#         classroom = Classroom.objects.create(classroom="111", seats_number=111, pc_number=111, location=location)
#         date_object = datetime.strptime('2022-09-01', '%Y-%m-%d')
#         course = Course.objects.create(course_name='Тестовый курс', start_date=date_object,
#                                        days_of_week=[1, 3], location=classroom, start_time='09:00',
#                                        number_of_lessons=3, url='1')
#
#     def test_create_lesson(self):
#         self.client.login(email='test@gmail.com', password='Test1234')
#         url = "/api/v1/lessons/new/"
#         data = {
#             'number': 1,
#             'course': 1,
#             'teacher': 1,
#             'topic': 'Тестовая тема',
#             'description': 'Тестовое описание',
#             'date': '2022-09-01',
#             'start_time': '09:00',
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
=======

