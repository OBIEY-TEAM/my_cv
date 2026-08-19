import os
import re
import zipfile
from pathlib import Path
from django.conf import settings
from pdf_generator.service import PDFService
from profile_manager.models import UserProfileInfo, Experience, Certification, Education, Project

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
        user = user_profile.user
        site_cat = job_offer.site_category or 'acpe'
        title = job_offer.title or 'Développeur Full Stack'
        abbreviation = job_offer.abbreviation or 'POSTE'

        # Fetch structured profile info if present
        info = getattr(user, 'profile_info', None)
        if info:
            user_name = f"{info.first_name} {info.last_name}".strip()
            user_phone = info.primary_phone or user_profile.phone
            user_summary = info.professional_summary or user_profile.readme_content
        else:
            user_name = f"{user.first_name} {user.last_name}".strip() or "CHRIST DANY OBIEY"
            user_phone = user_profile.phone or "+242 06 613 01 18"
            user_summary = user_profile.readme_content or "Consultant IT & Expert Fullstack."

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

        # Fetch structured lists
        exp_qs = Experience.objects.filter(user=user)
        experiences_list = []
        if exp_qs.exists():
            for exp in exp_qs:
                dates_str = f"{exp.start_date.strftime('%Y')} - {'Présent' if exp.is_current else (exp.end_date.strftime('%Y') if exp.end_date else '')}"
                bullets = [exp.industry]
                if exp.skills_acquired:
                    bullets.append(f"Compétences: {exp.skills_acquired}")
                experiences_list.append({
                    'role': exp.title,
                    'company': exp.company,
                    'dates': dates_str,
                    'bullets': bullets
                })
        else:
            experiences_list = [
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
            ]

        cert_qs = Certification.objects.filter(user=user)
        certifications_list = []
        for cert in cert_qs:
            certifications_list.append({
                'degree': cert.title,
                'school': f"{cert.institution} ({cert.year})",
                'dates': str(cert.year),
                'pdf_url': cert.pdf_url
            })

        edu_qs = Education.objects.filter(user=user)
        education_list = []
        if edu_qs.exists():
            for edu in edu_qs:
                education_list.append({
                    'degree': f"{edu.title} ({edu.degree_level})",
                    'school': edu.institution,
                    'dates': str(edu.year),
                    'pdf_url': edu.pdf_url
                })
        else:
            education_list = [
                {'degree': 'Licence Pro Systèmes & Réseaux', 'school': 'Université ESTAM', 'dates': '2020 - 2025'},
                {'degree': 'Passeport Numérique FATA', 'school': '10 000 Codeurs', 'dates': '2026'}
            ]

        # Merge certifications with education for display
        education_list.extend(certifications_list)

        proj_qs = Project.objects.filter(user=user)
        projects_list = []
        if proj_qs.exists():
            for proj in proj_qs:
                projects_list.append({
                    'title': proj.name,
                    'desc': f"{proj.industry} - {proj.description or 'Projet technique'}"
                })
        else:
            projects_list = [
                {'title': 'Directeur Technique - FoncierChain', 'desc': '1er Prix au MIABE Hackathon 2026. Architecture logicielle complète.'}
            ]

        cv_data = {
            'name': user_name,
            'title': f"{user_profile.title} | Spécialiste {title}",
            'location': user_profile.cities or "Brazzaville & Pointe-Noire, Congo",
            'phone': user_phone,
            'email': user.email or "obieydany@gmail.com",
            'photo_path': photo_path,
            'summary': user_summary[:300] if user_summary else f"Ingénieur Logiciel et Consultant IT expérimenté pour le poste de {title}.",
            'experiences': experiences_list[:2],
            'skills': {
                'Backend & Cloud': ['Python', 'Django REST', 'PostgreSQL', 'Docker', 'Redis'],
                'Frontend & Mobile': ['Flutter (Dart)', 'React.js', 'TypeScript', 'Tailwind CSS'],
                'Fintech & USSD': ['Airtel Money', 'MTN MoMo', 'PayDunya', 'Architecture USSD']
            },
            'education': education_list[:3],
            'projects': projects_list[:1]
        }

        PDFService.generate_cv_pdf(cv_data, cv_path)

        lm_data = {
            'name': user_name,
            'location': user_profile.cities or "Brazzaville & Pointe-Noire, Congo",
            'phone': user_phone,
            'email': user.email or "obieydany@gmail.com",
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
            f"Cordialement,\n{user_name}\n{user_phone}"
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
