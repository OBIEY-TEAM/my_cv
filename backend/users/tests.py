from django.test import TestCase
from rest_framework.test import APIClient

class UserAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123!',
            'first_name': 'Test',
            'last_name': 'User'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)
