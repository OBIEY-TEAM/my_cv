import os
import glob
from pathlib import Path
from AGENT_IA_CV.image_processor import ImageProcessor
from AGENT_IA_CV.job_scraper import JobScraper
from AGENT_IA_CV.pdf_generator import PDFGenerator

class CVApplicationAgent:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.commandes_info_dir = self.base_dir / "commandes" / "info"
        self.commandes_photo_dir = self.base_dir / "commandes" / "photo"
        self.resultat_dir = self.base_dir / "resultat"

    def parse_user_info(self, info_filepath):
        """Parses /commandes/info/<USER_ID>.txt into structured user profile dictionary."""
        info = {
            'user_id': Path(info_filepath).stem,
            'name': 'CHRIST DANY OBIEY',
            'first_name': 'CHRIST DANY',
            'last_name': 'OBIEY',
            'phone': '+242 06 613 01 18',
            'email': 'obieydany@gmail.com',
            'location': 'Brazzaville, Congo',
            'summary': 'Consultant IT et Ingénieur Logiciel Fullstack spécialisé en Django REST, React, Flutter et Fintech.',
            'experiences': [],
            'education': [],
            'skills': {
                'Backend & Cloud': ['Python', 'Django REST', 'PostgreSQL', 'Docker', 'Redis'],
                'Frontend & Mobile': ['Flutter (Dart)', 'React.js', 'TypeScript', 'Tailwind CSS'],
                'Fintech & USSD': ['Airtel Money', 'MTN MoMo', 'PayDunya', 'Architecture USSD']
            },
            'projects': []
        }

        if not os.path.exists(info_filepath):
            return info

        with open(info_filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip()]

        current_section = None
        for line in lines:
            if "INFORMATIONS UTILISATEUR" in line:
                current_section = "INFO"
            elif "EXPERIENCES PROFESSIONNELLES" in line:
                current_section = "EXP"
            elif "DIPLOMES" in line or "CERTIFICATIONS" in line:
                current_section = "EDU"
            elif "PROJETS" in line:
                current_section = "PROJ"
            else:
                if current_section == "INFO" and ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip().lower(), v.strip()
                    if "nom" in k and "prénom" not in k:
                        info['last_name'] = v
                    elif "prénom" in k:
                        info['first_name'] = v
                    elif "numéro principal" in k or "téléphone" in k:
                        info['phone'] = v
                    elif "adresse" in k or "pays" in k:
                        info['location'] = v
                    elif "résumé" in k:
                        info['summary'] = v
                elif current_section == "EXP" and line.startswith("-"):
                    parts = line.lstrip("-").split("|")
                    role = "Poste"
                    company = "Entreprise"
                    dates = "2026"
                    bullets = []
                    for p in parts:
                        if ":" in p:
                            pk, pv = p.split(":", 1)
                            pk, pv = pk.strip().lower(), pv.strip()
                            if "poste" in pk:
                                role = pv
                            elif "structure" in pk or "entreprise" in pk:
                                company = pv
                            elif "début" in pk or "fin" in pk:
                                bullets.append(f"{pk.capitalize()}: {pv}")
                            elif "compétences" in pk:
                                bullets.append(pv)
                    info['experiences'].append({
                        'role': role,
                        'company': company,
                        'dates': dates,
                        'bullets': bullets or ["Développement et gestion d'architectures applicatives."]
                    })
                elif current_section == "EDU" and line.startswith("-"):
                    parts = line.split("|")
                    degree = "Diplôme"
                    school = "Université"
                    dates = "2025"
                    pdf_url = ""
                    for p in parts:
                        if ":" in p:
                            pk, pv = p.split(":", 1)
                            pk, pv = pk.strip().lower(), pv.strip()
                            if "libellé" in pk:
                                degree = pv
                            elif "institution" in pk:
                                school = pv
                            elif "année" in pk:
                                dates = pv
                            elif "pdf drive" in pk and pv != "N/A":
                                pdf_url = pv
                    info['education'].append({
                        'degree': degree,
                        'school': school,
                        'dates': dates,
                        'pdf_url': pdf_url
                    })
                elif current_section == "PROJ" and line.startswith("-"):
                    parts = line.split("|")
                    title = "Projet"
                    desc = "Projet technique"
                    for p in parts:
                        if ":" in p:
                            pk, pv = p.split(":", 1)
                            pk, pv = pk.strip().lower(), pv.strip()
                            if "nom" in pk:
                                title = pv
                            elif "description" in pk or "secteur" in pk:
                                desc = f"{pv}"
                    info['projects'].append({'title': title, 'desc': desc})

        if not info['projects']:
            info['projects'] = [
                {'title': 'Directeur Technique - FoncierChain', 'desc': '1er Prix au MIABE Hackathon 2026. Architecture logicielle complète.'}
            ]

        info['name'] = f"{info.get('first_name', '')} {info.get('last_name', '')}".strip() or "CHRIST DANY OBIEY"
        return info

    def process_user_command(self, user_id, job_sources=None):
        """
        Process single user command ID:
        1. Crop photo /commandes/photo/<ID>.png -> /commandes/photo/<ID>_cropped.png
        2. Parse /commandes/info/<ID>.txt
        3. Scrap/parse job sources & inject ATS keywords
        4. Generate deliverables into /resultat/<ID>/<site>/<poste>/
        """
        photo_orig = self.commandes_photo_dir / f"{user_id}.png"
        photo_cropped = self.commandes_photo_dir / f"{user_id}_cropped.png"

        if photo_orig.exists():
            ImageProcessor.crop_profile_picture(str(photo_orig), str(photo_cropped))
        elif os.path.exists("image/profile_cropped.png"):
            photo_cropped = Path("image/profile_cropped.png")

        info_file = self.commandes_info_dir / f"{user_id}.txt"
        user_data = self.parse_user_info(str(info_file))
        user_data['photo_path'] = str(photo_cropped) if photo_cropped.exists() else None

        if not job_sources:
            job_sources = [
                "Développeur Full Stack Mobile\nACPE Congo\nRecherche développeur Flutter et Django REST.",
                "Chargé(e) IT & Développement Web\nBlueCollar Congo\nPoste basé à Pointe-Noire.",
                "Ingénieur Réseaux, Systèmes et Télécoms (H-F)\nACPE Congo\nProjets télécoms et réseaux."
            ]

        results = []
        for src in job_sources:
            job_info = JobScraper.scrape_job(src)

            site_name = job_info['site_name']
            job_title = job_info['title']
            abbr = job_info['abbreviation']
            user_name_prefix = user_data['last_name'].upper() if user_data.get('last_name') else "OBIEY"

            out_dir = self.resultat_dir / str(user_id) / site_name / job_title
            out_dir.mkdir(parents=True, exist_ok=True)

            cv_file = out_dir / f"{user_name_prefix}-{abbr}-CV.pdf"
            lm_file = out_dir / f"{user_name_prefix}-{abbr}-LM.pdf"
            email_file = out_dir / f"{user_name_prefix}-{abbr}-EMAIL.txt"
            offer_file = out_dir / f"{user_name_prefix}-{abbr}-OFFRE.pdf"

            # Customize CV data with ATS keywords
            cv_data = dict(user_data)
            cv_data['title'] = f"Consultant IT | Spécialiste {job_title}"
            cv_data['skills'] = dict(user_data.get('skills', {}))
            cv_data['skills']['Mots-Clés Offre (ATS)'] = job_info.get('keywords', [])
            PDFGenerator.generate_cv_pdf(cv_data, str(cv_file))

            # Customize LM data with ATS keywords
            lm_data = {
                'name': user_data['name'],
                'location': user_data['location'],
                'phone': user_data['phone'],
                'email': user_data['email'],
                'company_name': job_info['company'],
                'job_title': job_title,
                'city': 'Pointe-Noire, Congo',
                'date': 'Octobre 2026',
                'keywords': job_info.get('keywords', [])
            }
            PDFGenerator.generate_cover_letter_pdf(lm_data, str(lm_file))

            # Generate Email
            email_data = {
                'name': user_data['name'],
                'job_title': job_title,
                'company_name': job_info['company'],
                'phone': user_data['phone']
            }
            PDFGenerator.generate_email_txt(email_data, str(email_file))

            # Generate Offer PDF
            PDFGenerator.generate_offer_pdf(job_info, str(offer_file))

            results.append({
                'user_id': user_id,
                'site': site_name,
                'job_title': job_title,
                'dir': str(out_dir),
                'files': [str(cv_file), str(lm_file), str(email_file), str(offer_file)]
            })

        return results

    def run_pipeline(self):
        """Scans /commandes/info/ for all user commands and processes them."""
        processed = []
        if not self.commandes_info_dir.exists():
            return processed

        for info_file in self.commandes_info_dir.glob("*.txt"):
            user_id = info_file.stem
            res = self.process_user_command(user_id)
            processed.extend(res)

        return processed

def main():
    agent = CVApplicationAgent()
    results = agent.run_pipeline()
    print(f"AGENT_IA_CV terminé avec succès. {len(results)} dossiers de candidatures générés.")

if __name__ == "__main__":
    main()
