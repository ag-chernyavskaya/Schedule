from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from User.models import User
from schedule.models import SubwayStation


class TestSubwayStationList(APITestCase):
    """
    Ensure we can view a list of SubwayStation objects.
    """
    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        self.uri = '/api/v1/subwaystations/'

    def test_list(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestsSubwayStationCreateSuperAdmin(APITestCase):
    """
    Ensure Super Admin can create a new SubwayStation object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")

    def test_create_subwaystation(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/subwaystations/"
        data = {
            'station': 'Test station',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubwayStation.objects.count(), 1)
        self.assertEqual(SubwayStation.objects.get().station, 'Test station')


class TestsSubwayStationCreateAdministrator(APITestCase):
    """
    Ensure Administrator cannot create a new SubwayStation object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Administrator")

    def test_create_subwaystation(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/subwaystations/"
        data = {
            'station': 'Test station',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestsSubwayStationUpdateSuperAdmin(APITestCase):
    """
    Ensure Super Admin can update a SubwayStation object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        SubwayStation.objects.create(station="Test station")

    def test_update_subwaystation(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/subwaystations/1/"
        data = {
            'station': 'Test station renamed',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubwayStation.objects.count(), 1)
        self.assertEqual(SubwayStation.objects.get().station, 'Test station renamed')


class TestsSubwayStationUpdateAdministrator(APITestCase):
    """
    Ensure Administrator cannot update a SubwayStation object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Administrator")
        self.factory = APIRequestFactory()
        SubwayStation.objects.create(station="Test station")

    def test_update_subwaystation(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/subwaystations/1/"
        data = {
            'station': 'Test station renamed',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestsSubwayStationDestroySuperAdmin(APITestCase):
    """
    Ensure Super Admin can delete a SubwayStation object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Super Admin")
        self.factory = APIRequestFactory()
        SubwayStation.objects.create(station="Test station")

    def test_update_subwaystation(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/subwaystations/1/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestsSubwayStationDestroyAdministrator(APITestCase):
    """
    Ensure Administrator can delete a SubwayStation object.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="Test1234", role="Administrator")
        self.factory = APIRequestFactory()
        SubwayStation.objects.create(station="Test station")

    def test_update_subwaystation(self):
        self.client.login(email='test@gmail.com', password='Test1234')
        url = "/api/v1/subwaystations/1/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
