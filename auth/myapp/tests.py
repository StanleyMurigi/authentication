from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from myapp.models import Organisation
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AuthTests(APITestCase):

    def test_register_user_successfully(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "password2": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('user', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], 'John')
        self.assertEqual(Organisation.objects.count(), 1)
        self.assertEqual(Organisation.objects.first().name, "John's Organisation")

    def test_register_user_missing_fields(self):
        url = reverse('register')
        data = {
            "firstName": "",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "password2": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_register_user_password_mismatch(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "password2": "password124",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_login_user_successfully(self):
        user = User.objects.create_user(email="john@example.com", first_name="John", last_name="Doe", password="password123")
        url = reverse('login')
        data = {
            "email": "john@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('user', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], 'John')

    def test_login_user_invalid_credentials(self):
        user = User.objects.create_user(email="john@example.com", first_name="John", last_name="Doe", password="password123")
        url = reverse('login')
        data = {
            "email": "john@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Authentication failed')

class UserDetailTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email="john@example.com", first_name="John", last_name="Doe", password="password123")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    
    def test_get_user_details(self):
        url = reverse('user-detail', kwargs={'id': self.user.user_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['firstName'], 'John')

class OrganisationTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email="john@example.com", first_name="John", last_name="Doe", password="password123")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    
    def test_get_organisations(self):
        Organisation.objects.create(name="John's Organisation", description="Test Organisation")
        url = reverse('organisation-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('organisations', response.data['data'])
