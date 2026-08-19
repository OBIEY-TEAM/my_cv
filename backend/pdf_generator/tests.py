from django.test import TestCase
from django.contrib.auth.models import User
from profile_manager.models import Profile, UserProfileInfo, Experience, Certification, Education, Project
from jobs.models import JobOffer
from ai_engine.service import AIEngineService
from pdf_generator.service import PDFService

class PDFGeneratorServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='pdfuser', password='Password123!')
        self.profile = Profile.objects.create(user=self.user, title="Ingénieur Fullstack", phone="+242060000000")

        # Add structured profile data
        UserProfileInfo.objects.create(
            user=self.user,
            first_name="Christ",
            last_name="Obiey",
            primary_phone="+242066130118",
            professional_summary="Ingénieur informatique senior avec 5 ans d'expérience."
        )
        Experience.objects.create(
            user=self.user,
            title="Développeur Lead",
            company="Société IT",
            industry="Informatique",
            start_date="2022-01-01",
            is_current=True,
            skills_acquired="Python, Django, React, Flutter"
        )
        Certification.objects.create(
            user=self.user,
            title="Certificat Cloud Architect",
            year=2025,
            institution="AWS",
            pdf_url="https://drive.google.com/file/d/test123/view"
        )
        Education.objects.create(
            user=self.user,
            title="Master Génie Logiciel",
            year=2024,
            institution="Université",
            degree_level="Master",
            pdf_url="https://drive.google.com/file/d/edu123/view"
        )
        Project.objects.create(
            user=self.user,
            name="Projet SaaS AI",
            industry="SaaS",
            description="Plateforme de génération automatique de CV."
        )

        self.job_offer = JobOffer.objects.create(
            user=self.user,
            title="Développeur Full Stack Senior",
            company="ACPE Congo",
            site_category="acpe",
            abbreviation="DEV-FULLSTACK",
            raw_text="Recherche Développeur Full Stack Senior maîtrisant Python Django REST et React."
        )

    def test_structured_cv_and_lm_generation(self):
        result = AIEngineService.generate_custom_application(self.profile, self.job_offer)
        self.assertTrue(PDFService.verify_1_page_limit(result['cv_pdf']))
        self.assertTrue(PDFService.verify_1_page_limit(result['cover_letter_pdf']))
