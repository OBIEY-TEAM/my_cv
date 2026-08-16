from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from pdf_generator.service import PDFService
import tempfile
import os

class PDFAndAIEngineTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='pdfuser', password='Password123!')
        self.client.force_authenticate(user=self.user)

    def test_pdf_1_page_strict_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cv_path = os.path.join(tmpdir, "test_cv.pdf")
            lm_path = os.path.join(tmpdir, "test_lm.pdf")

            cv_data = {
                'name': 'Christ Dany Obiey',
                'title': 'Consultant IT',
                'summary': 'Résumé de profil court et concis.',
                'skills': {'Tech': ['Python', 'Django']},
                'experiences': [{'role': 'Dev', 'company': 'Co', 'dates': '2026', 'bullets': ['Bullet 1']}],
                'education': [{'degree': 'BAC', 'school': 'Lycée', 'dates': '2020'}],
                'projects': [{'title': 'Project', 'desc': 'Desc'}]
            }

            PDFService.generate_cv_pdf(cv_data, cv_path)
            self.assertTrue(PDFService.verify_1_page_limit(cv_path))

            lm_data = {
                'name': 'Christ Dany Obiey',
                'company_name': 'Entreprise Test',
                'job_title': 'Développeur Fullstack',
                'letter_body': 'Corps de la lettre de motivation court.'
            }

            PDFService.generate_cover_letter_pdf(lm_data, lm_path)
            self.assertTrue(PDFService.verify_1_page_limit(lm_path))
