import os
import re
import zipfile
from pathlib import Path
from django.conf import settings
from pdf_generator.service import PDFService

class AIEngineService:
    @staticmethod
    def extract_job_details(raw_text, url=None):
        text = raw_text.strip()
        title = "Ingénieur Logiciel / Développeur"
        company = "Entreprise"
        site_category = "acpe"
        abbreviation = "POSTE"

        if url:
            if "acpe.cg" in url:
                site_category = "acpe"
            elif "bluecollarcongo" in url:
                site_category = "bluecollarcongo"

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            title = lines[0]
            if len(lines) > 1:
                company = lines[1]

        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title).upper()
        words = clean_title.split()
        if 'DEVELOPPEUR' in words or 'DEV' in words or 'FULLSTACK' in words or 'MOBILE' in words:
            abbreviation = "DEV-FULLSTACK-MOBILE"
        elif 'RESEAUX' in words or 'TELECOM' in words or 'SYSTEMES' in words:
            abbreviation = "ING-RESEAUX-SYS-TELECOM"
        elif 'CHARGE' in words or 'WEB' in words or 'IT' in words:
            abbreviation = "CHARGE-IT-DEV-WEB"
        else:
            abbreviation = "-".join(words[:3]) if words else "POSTE"

        return {
            'title': title,
            'company': company,
            'site_category': site_category,
            'abbreviation': abbreviation,
            'cleaned_description': text
        }

    @staticmethod
    def generate_custom_application(user_profile, job_offer):
        site_cat = job_offer.site_category or 'acpe'
        title = job_offer.title or 'Développeur Full Stack'
        abbreviation = job_offer.abbreviation or 'POSTE'
        user_name = f"{user_profile.user.first_name} {user_profile.user.last_name}".strip() or "CHRIST DANY OBIEY"

        base_dir = Path(settings.MEDIA_ROOT) / 'applications' / 'generated' / site_cat / title
        base_dir.mkdir(parents=True, exist_ok=True)

        cv_filename = f"OBIEY-{abbreviation}-CV.pdf"
        lm_filename = f"OBIEY-{abbreviation}-LM.pdf"
        email_filename = f"OBIEY-{abbreviation}-EMAIL.txt"
        offer_filename = f"OBIEY-{abbreviation}-OFFRE.pdf"
        zip_filename = f"OBIEY-{abbreviation}-CANDIDATURE.zip"

        cv_path = str(base_dir / cv_filename)
        lm_path = str(base_dir / lm_filename)
        email_path = str(base_dir / email_filename)
        offer_path = str(base_dir / offer_filename)
        zip_path = str(base_dir / zip_filename)

        photo_path = None
        if user_profile.cropped_photo and os.path.exists(user_profile.cropped_photo.path):
            photo_path = user_profile.cropped_photo.path
        elif os.path.exists('image/profile_cropped.png'):
            photo_path = 'image/profile_cropped.png'

        cv_data = {
            'name': user_name,
            'title': f"{user_profile.title} | Spécialiste {title}",
            'location': user_profile.cities or "Brazzaville & Pointe-Noire, Congo",
            'phone': user_profile.phone or "+242 06 613 01 18",
            'email': user_profile.user.email or "obieydany@gmail.com",
            'photo_path': photo_path,
            'summary': f"Ingénieur Logiciel et Consultant IT expérimenté, spécialisé en architectures Web & Mobile robustes. Expert en Python (Django REST Framework), TypeScript (React) et Dart (Flutter). Parfaite maîtrise du sur-mesure technique aligné sur les besoins précis du poste de {title} chez {job_offer.company}.",
            'experiences': [
                {
                    'role': 'Ingénieur Logiciel Fullstack & Architecte Cloud',
                    'company': 'NOISIM ENGINEERING SERVICES',
                    'dates': '2026 - Présent',
                    'bullets': [
                        'Développement de plateformes d\'APIs backend Django REST et clients Flutter/React.',
                        'Intégration d\'architectures de paiements Mobile Money (Airtel, MTN, PayDunya).'
                    ]
                },
                {
                    'role': 'Consultant IT & Commercial KYC',
                    'company': 'AIRTEL CONGO B',
                    'dates': '2020 - 2025',
                    'bullets': [
                        'Gestion d\'équipes, stratégie commerciale et intégrations réseau/systèmes.'
                    ]
                }
            ],
            'skills': {
                'Backend & Cloud': ['Python', 'Django REST', 'PostgreSQL', 'Docker', 'Redis'],
                'Frontend & Mobile': ['Flutter (Dart)', 'React.js', 'TypeScript', 'Tailwind CSS'],
                'Fintech & USSD': ['Airtel Money', 'MTN MoMo', 'PayDunya', 'Architecture USSD']
            },
            'education': [
                {'degree': 'Licence Pro Systèmes & Réseaux', 'school': 'Université ESTAM', 'dates': '2020 - 2025'},
                {'degree': 'Passeport Numérique FATA', 'school': '10 000 Codeurs', 'dates': '2026'}
            ],
            'projects': [
                {'title': 'Directeur Technique - FoncierChain', 'desc': '1er Prix au MIABE Hackathon 2026. Architecture logicielle complète.'}
            ]
        }

        PDFService.generate_cv_pdf(cv_data, cv_path)

        lm_data = {
            'name': user_name,
            'location': user_profile.cities or "Brazzaville & Pointe-Noire, Congo",
            'phone': user_profile.phone or "+242 06 613 01 18",
            'email': user_profile.user.email or "obieydany@gmail.com",
            'company_name': job_offer.company or "Société",
            'job_title': title,
            'city': 'Pointe-Noire, Congo',
            'date': 'Octobre 2026',
            'letter_body': (
                f"C'est avec un vif intérêt que je vous adresse ma candidature pour le poste de {title} au sein de {job_offer.company}.\n\n"
                f"Fort de mon parcours d'Ingénieur Logiciel et Consultant IT, j'ai acquis une solide expérience dans le développement d'architectures applicatives modernes (Django REST, React, Flutter) et dans l'intégration de services tiers stratégiques.\n\n"
                f"Sûr de pouvoir apporter une contribution immédiate à vos projets, je reste à votre entière disposition pour un entretien."
            )
        }

        PDFService.generate_cover_letter_pdf(lm_data, lm_path)

        email_subject = f"Candidature au poste de {title} - {user_name}"
        email_body = (
            f"Objet : {email_subject}\n\n"
            f"Madame, Monsieur,\n\n"
            f"Veuillez trouver ci-joint mon dossier de candidature (CV et Lettre de Motivation) pour le poste de {title} au sein de {job_offer.company}.\n\n"
            f"Restant à votre disposition pour tout échange complémentaire.\n\n"
            f"Cordialement,\n{user_name}\n{user_profile.phone or '+242 06 613 01 18'}"
        )
        with open(email_path, 'w', encoding='utf-8') as f:
            f.write(email_body)

        offer_data = {
            'name': f"ARCHIVE OFFRE D'EMPLOI - {job_offer.company}",
            'company_name': job_offer.company,
            'job_title': title,
            'letter_body': job_offer.cleaned_description or job_offer.raw_text or "Descriptif de l'offre d'emploi originale."
        }
        PDFService.generate_cover_letter_pdf(offer_data, offer_path)

        cv_1_page = PDFService.verify_1_page_limit(cv_path)
        lm_1_page = PDFService.verify_1_page_limit(lm_path)

        if not (cv_1_page and lm_1_page):
            raise ValueError(f"Strict 1-page validation failed: CV 1-page={cv_1_page}, LM 1-page={lm_1_page}")

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(cv_path, arcname=f"{site_cat}/{title}/{cv_filename}")
            zipf.write(lm_path, arcname=f"{site_cat}/{title}/{lm_filename}")
            zipf.write(email_path, arcname=f"{site_cat}/{title}/{email_filename}")
            zipf.write(offer_path, arcname=f"{site_cat}/{title}/{offer_filename}")

        return {
            'cv_pdf': cv_path,
            'cover_letter_pdf': lm_path,
            'email_txt': email_path,
            'offer_pdf': offer_path,
            'zip_package': zip_path,
            'email_subject': email_subject,
            'email_body': email_body,
            'folder_path': str(base_dir)
        }
