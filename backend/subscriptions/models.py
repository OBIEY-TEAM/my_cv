from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    PLAN_TYPES = (
        ('FREE', 'Formule Découverte (Gratuit)'),
        ('PACK_5', 'Formule Pack 5 Candidatures'),
        ('UNLIMITED', 'Formule Illimitée Mensuelle'),
    )

    code = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    name = models.CharField(max_length=100)
    price_fcfa = models.IntegerField(default=0)
    credits_included = models.IntegerField(default=1)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.price_fcfa} FCFA)"

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    credits_remaining = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.credits_remaining} crédits"

class Transaction(models.Model):
    PAYMENT_METHODS = (
        ('AIRTEL_MONEY', 'Airtel Money Congo'),
        ('MTN_MOMO', 'MTN Mobile Money Congo'),
        ('PAYDUNYA', 'PayDunya / Carte'),
        ('SANKMONEY', 'SankMoney'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('SUCCESS', 'Réussi'),
        ('FAILED', 'Échoué'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    phone_number = models.CharField(max_length=20, blank=True)
    amount_fcfa = models.IntegerField()
    transaction_ref = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    receipt_pdf = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx {self.transaction_ref} - {self.user.username} ({self.status})"
