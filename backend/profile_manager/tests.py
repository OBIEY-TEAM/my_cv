from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Experience, Certification, Education, Project

class ProfileStructuredAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='profileuser', password='Password123!')
        self.client.force_authenticate(user=self.user)

    def test_profile_info_get_and_update(self):
        res = self.client.get('/api/profile/info/')
        self.assertEqual(res.status_code, 200)

        res_update = self.client.patch('/api/profile/info/', {
            'first_name': 'Jean',
            'last_name': 'Makosso',
            'primary_phone': '+242060000000',
            'district': 'Makélékélé'
        }, format='json')
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(res_update.data['first_name'], 'Jean')

    def test_experience_crud(self):
        res = self.client.post('/api/profile/experiences/', {
            'title': 'Développeur Python',
            'company': 'Tech Congo',
            'industry': 'Informatique',
            'start_date': '2024-01-01',
            'is_current': True
        }, format='json')
        self.assertEqual(res.status_code, 201)
        exp_id = res.data['id']

        res_list = self.client.get('/api/profile/experiences/')
        self.assertEqual(len(res_list.data), 1)

        res_delete = self.client.delete(f'/api/profile/experiences/{exp_id}/')
        self.assertEqual(res_delete.status_code, 204)
        self.assertEqual(Experience.objects.count(), 0)

    def test_certification_crud(self):
        res = self.client.post('/api/profile/certifications/', {
            'title': 'Certificat AWS Architect',
            'year': 2025,
            'institution': 'Amazon AWS'
        }, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Certification.objects.count(), 1)
