from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class AccountsAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='securepassword123'
        )

    def test_login_successful(self):
        response = self.client.post('/api/login/', {
            'email': 'johndoe@example.com',
            'password': 'securepassword123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_password(self):
        response = self.client.post('/api/login/', {
            'email': 'johndoe@example.com',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_successful(self):
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'phone': '9876543210'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

