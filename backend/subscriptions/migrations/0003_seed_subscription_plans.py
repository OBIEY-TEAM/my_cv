from django.db import migrations

def create_initial_plans(apps, schema_editor):
    SubscriptionPlan = apps.get_model('subscriptions', 'SubscriptionPlan')
    SubscriptionPlan.objects.all().delete()
    plans = [
        SubscriptionPlan(code='CREDIT_1', name='1 Crédit', price_fcfa=200, credits_included=1, description='Achat de 1 crédit à 200 FCFA'),
        SubscriptionPlan(code='CREDIT_5', name='5 Crédits', price_fcfa=500, credits_included=5, description='Achat de 5 crédits à 500 FCFA'),
        SubscriptionPlan(code='CREDIT_25', name='25 Crédits', price_fcfa=1000, credits_included=25, description='Achat de 25 crédits à 1000 FCFA'),
    ]
    SubscriptionPlan.objects.bulk_create(plans)

def remove_initial_plans(apps, schema_editor):
    SubscriptionPlan = apps.get_model('subscriptions', 'SubscriptionPlan')
    SubscriptionPlan.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_alter_subscriptionplan_code'),
    ]

    operations = [
        migrations.RunPython(create_initial_plans, reverse_code=remove_initial_plans),
    ]
