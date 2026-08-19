import re
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pypdf
from PIL import Image

class JobScraper:
    @staticmethod
    def scrape_job(input_source):
        """
        Accepts input_source which can be:
        - URL string (e.g., https://www.acpe.cg/...)
        - PDF file path
        - Image file path (e.g., screenshot)
        - Text file path or Raw text string

        Returns a dictionary containing:
        - title: Job Title
        - company: Organization / Company name
        - site_name: Name of site / domain (e.g. 'acpe', 'bluecollarcongo')
        - abbreviation: Normalized abbreviation (e.g. 'DEV-FULLSTACK-MOBILE', 'CHARGE-IT-DEV-WEB', 'ING-RESEAUX-SYS-TELECOM')
        - full_text: Full raw job offer text
        - keywords: Extracted technical and ATS keywords
        """
        raw_text = ""
        site_name = "acpe"
        source_url = None

        is_image_file = isinstance(input_source, str) and os.path.exists(input_source) and input_source.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))

        if isinstance(input_source, str) and (input_source.startswith("http://") or input_source.startswith("https://")):
            source_url = input_source
            if "bluecollarcongo" in input_source:
                site_name = "bluecollarcongo"
            elif "acpe" in input_source:
                site_name = "acpe"
            else:
                site_name = input_source.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]

            try:
                resp = requests.get(input_source, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    for script in soup(["script", "style"]):
                        script.extract()
                    raw_text = soup.get_text(separator="\n")
            except Exception:
                raw_text = f"Offre d'emploi disponible sur {input_source}"
        elif isinstance(input_source, str) and os.path.exists(input_source) and input_source.lower().endswith(".pdf"):
            try:
                reader = pypdf.PdfReader(input_source)
                raw_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            except Exception:
                raw_text = "Offre d'emploi issue d'un document PDF."
        elif is_image_file:
            raw_text = f"Offre d'emploi fournie sous forme d'image/capture d'écran : {Path(input_source).name}"
        elif isinstance(input_source, str) and os.path.exists(input_source):
            with open(input_source, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
        else:
            raw_text = str(input_source)

        raw_text = raw_text.strip()
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

        title = "Ingénieur Logiciel / Développeur"
        company = "Entreprise"

        if lines:
            title = lines[0]
            if len(lines) > 1:
                company = lines[1]

        # Generate normalized abbreviation
        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title).upper()
        words = clean_title.split()

        if any(w in words for w in ['DEVELOPPEUR', 'DEV', 'FULLSTACK', 'MOBILE']):
            abbreviation = "DEV-FULLSTACK-MOBILE"
        elif any(w in words for w in ['RESEAUX', 'TELECOM', 'SYSTEMES', 'TELECOMS']):
            abbreviation = "ING-RESEAUX-SYS-TELECOM"
        elif any(w in words for w in ['CHARGE', 'WEB', 'IT']):
            abbreviation = "CHARGE-IT-DEV-WEB"
        else:
            abbreviation = "-".join(words[:3]) if words else "POSTE"

        # Extract technical keywords for ATS optimization
        tech_words = [
            "Python", "Django", "React", "Flutter", "TypeScript", "Angular", "Dart",
            "REST", "API", "Docker", "Linux", "SQL", "PostgreSQL", "SEO", "USSD",
            "Airtel Money", "MTN Mobile Money", "PayDunya", "Réseaux", "Télécoms",
            "Gestion de projet", "DevOps", "Fullstack", "Mobile", "Web"
        ]
        found_keywords = [kw for kw in tech_words if kw.lower() in raw_text.lower()]
        if not found_keywords:
            found_keywords = ["Python", "Django", "Flutter", "React", "REST API", "DevOps"]

        return {
            'title': title,
            'company': company,
            'site_name': site_name,
            'abbreviation': abbreviation,
            'full_text': raw_text,
            'keywords': found_keywords,
            'source_url': source_url
        }
