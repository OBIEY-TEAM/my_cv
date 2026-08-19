import os
import shutil
import tempfile
import unittest
from pathlib import Path
from AGENT_IA_CV.image_processor import ImageProcessor
from AGENT_IA_CV.job_scraper import JobScraper
from AGENT_IA_CV.pdf_generator import PDFGenerator
from AGENT_IA_CV.main import CVApplicationAgent

class TestAgentIACV(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.commandes_info_dir = Path(self.test_dir) / "commandes" / "info"
        self.commandes_photo_dir = Path(self.test_dir) / "commandes" / "photo"
        self.resultat_dir = Path(self.test_dir) / "resultat"

        self.commandes_info_dir.mkdir(parents=True, exist_ok=True)
        self.commandes_photo_dir.mkdir(parents=True, exist_ok=True)
        self.resultat_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_job_scraper(self):
        job_data = JobScraper.scrape_job("Développeur Full Stack Mobile\nACPE Congo\nRecherche développeur Flutter et Django REST.")
        self.assertEqual(job_data['title'], "Développeur Full Stack Mobile")
        self.assertEqual(job_data['company'], "ACPE Congo")
        self.assertEqual(job_data['abbreviation'], "DEV-FULLSTACK-MOBILE")
        self.assertIn("Django", job_data['keywords'])

    def test_pdf_generator_strict_1_page(self):
        cv_path = os.path.join(self.test_dir, "test_cv.pdf")
        lm_path = os.path.join(self.test_dir, "test_lm.pdf")

        cv_data = {
            'name': 'TEST USER',
            'title': 'Développeur Fullstack',
            'location': 'Brazzaville',
            'phone': '+242060000000',
            'email': 'test@example.com',
            'skills': {'Tech': ['Python', 'Django']},
            'experiences': [{'role': 'Dev', 'company': 'TestCorp', 'dates': '2026', 'bullets': ['API REST']}],
            'education': [{'degree': 'Licence', 'school': 'University', 'dates': '2025'}]
        }
        PDFGenerator.generate_cv_pdf(cv_data, cv_path)
        self.assertTrue(PDFGenerator.verify_1_page_limit(cv_path))

        lm_data = {
            'name': 'TEST USER',
            'company_name': 'TestCorp',
            'job_title': 'Développeur Fullstack'
        }
        PDFGenerator.generate_cover_letter_pdf(lm_data, lm_path)
        self.assertTrue(PDFGenerator.verify_1_page_limit(lm_path))

    def test_agent_pipeline(self):
        # Create test info file
        info_file = self.commandes_info_dir / "99.txt"
        with open(info_file, "w", encoding="utf-8") as f:
            f.write("=== INFORMATIONS UTILISATEUR (ID: 99) ===\nNom : TEST\nPrénom : User\n")

        agent = CVApplicationAgent(base_dir=self.test_dir)
        results = agent.run_pipeline()

        self.assertGreater(len(results), 0)
        user_res_dir = self.resultat_dir / "99"
        self.assertTrue(user_res_dir.exists())

if __name__ == "__main__":
    unittest.main()
