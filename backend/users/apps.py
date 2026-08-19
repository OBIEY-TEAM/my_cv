from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_user(sender, **kwargs):
    from django.contrib.auth.models import User
    from profile_manager.models import Profile
    from subscriptions.models import UserSubscription, SubscriptionPlan

    try:
        plan, _ = SubscriptionPlan.objects.get_or_create(
            code='PACK_5',
            defaults={
                'name': 'Formule Pack 5 Candidatures',
                'price_fcfa': 2000,
                'credits_included': 5,
                'description': '5 candidatures générées sur mesure.'
            }
        )

        # Create default admin user (admin / admin1234)
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@lukamosala.cg',
                password='admin1234',
                first_name='Admin',
                last_name='Luka Mosala'
            )
            Profile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'title': 'Consultant IT & Expert Fullstack',
                    'phone': '+242 06 613 01 18',
                    'cities': 'Brazzaville & Pointe-Noire, Congo',
                    'readme_content': '# CV | ADMIN TEST\nExpert Fullstack & Consultant IT',
                }
            )
            UserSubscription.objects.get_or_create(
                user=admin_user,
                defaults={'plan': plan, 'credits_remaining': 10, 'is_active': True}
            )

        # Create obieydany user for testing
        if not User.objects.filter(username='obieydany').exists():
            user = User.objects.create_user(
                username='obieydany',
                email='obieydany@gmail.com',
                password='Password123!',
                first_name='Christ Dany',
                last_name='Obiey'
            )
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'title': 'Consultant IT & Expert Fullstack',
                    'phone': '+242 06 613 01 18',
                    'cities': 'Brazzaville & Pointe-Noire, Congo',
                    'readme_content': '# CV | CHRIST DANY OBIEY\nConsultant IT & Transformation Digitale',
                }
            )
            UserSubscription.objects.get_or_create(
                user=user,
                defaults={'plan': plan, 'credits_remaining': 5, 'is_active': True}
            )
    except Exception as e:
        print(f"Post-migrate seeding note: {e}")


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        post_migrate.connect(create_default_user, sender=self)
