from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from User.models import User
from schedule.models import SubwayStation, Classroom, Location


class TestClassroomList(APITestCase):
    """
    Ensure we can view a list of Classroom objects.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        self.uri = '/api/v1/classrooms/'

    def test_list_classroom(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestsClassroomCreateSuperAdmin(APITestCase):
    """
    Ensure Super Admin can create a new Classroom object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        subwaystation = SubwayStation.objects.create(station='Test station')
        Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)

    def test_create_classroom(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/classrooms/"
        data = {
            'classroom': '111',
            'seats_number': 111,
            'pc_number': 111,
            'location': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 1)
        self.assertEqual(Classroom.objects.get().classroom, '111')


class TestsClassroomCreateAdministrator(APITestCase):
    """
    Ensure Administrator cannot create a new Classroom object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Administrator")
        self.factory = APIRequestFactory()
        subwaystation = SubwayStation.objects.create(station='Test station')
        Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)

    def test_create_classroom(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/classrooms/"
        data = {
            'classroom': '111',
            'seats_number': 111,
            'pc_number': 111,
            'location': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestsClassroomUpdateSuperAdmin(APITestCase):
    """
    Ensure Super Admin can update a Classroom object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        subwaystation = SubwayStation.objects.create(station='Test station')
        location = Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)
        Classroom.objects.create(classroom="111", location=location, seats_number=111, pc_number=111, )

    def test_update_classroom(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/classrooms/1/"
        data = {
            'classroom': 333,
            'pc_number': 333,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Classroom.objects.count(), 1)
        self.assertEqual(Classroom.objects.get().classroom, '333')
        self.assertEqual(Classroom.objects.get().pc_number, 333)


class TestsClassroomUpdateAdministrator(APITestCase):
    """
    Ensure Administrator cannot update a Classroom object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Administrator")
        self.factory = APIRequestFactory()
        subwaystation = SubwayStation.objects.create(station='Test station')
        location = Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)
        Classroom.objects.create(classroom="111", seats_number=111, pc_number=111, location=location)

    def test_update_classroom(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/classrooms/1/"
        data = {
            'classroom': '222',
            'pc_number': 333,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestsClassroomDestroySuperAdmin(APITestCase):
    """
    Ensure Super Admin can delete a Classroom object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        subwaystation = SubwayStation.objects.create(station='Test station')
        location = Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)
        Classroom.objects.create(classroom="111", seats_number=111, pc_number=111, location=location)

    def test_update_classroom(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/classrooms/1/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestsClassroomDestroyAdministrator(APITestCase):
    """
    Ensure Administrator can delete a Classroom object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Administrator")
        self.factory = APIRequestFactory()
        subwaystation = SubwayStation.objects.create(station='Test station')
        location = Location.objects.create(city='Test city', street='Test street', building='1', subway=subwaystation)
        Classroom.objects.create(classroom="111", seats_number=111, pc_number=111, location=location)

    def test_update_classroom(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/classrooms/1/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
