from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import SubscriptionPlan

class SubscriptionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='subuser', password='Password123!')
        self.client.force_authenticate(user=self.user)
        self.plan = SubscriptionPlan.objects.create(
            code='PACK_5',
            name='Formule Pack 5 Candidatures',
            price_fcfa=2000,
            credits_included=5
        )

    def test_initiate_payment(self):
        response = self.client.post('/api/subscriptions/pay/', {
            'plan_id': self.plan.id,
            'payment_method': 'AIRTEL_MONEY',
            'phone_number': '+242066130118'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['credits_remaining'], 6)
