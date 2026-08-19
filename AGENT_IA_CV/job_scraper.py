import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class JobOfferScraper:
    @staticmethod
    def scrape_url(url: str) -> dict:
        """
        Analyse une URL d'offre d'emploi et extrait les détails (poste, entreprise, site_name, etc.)
        """
        domain = urlparse(url).netloc
        site_name = domain.replace("www.", "").split(".")[0].lower()
        if not site_name:
            site_name = "organisme"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            # Extraction du titre : chercher d'abord h1, h2 dans le body, puis title
            title = None
            for h in soup.find_all(["h1", "h2"]):
                t = h.get_text(strip=True)
                if t and len(t) > 3 and "ACPE" not in t and "CONNEXION" not in t.upper() and "RECHERCHE" not in t.upper():
                    title = t
                    break

            if not title:
                h_any = soup.find(["h1", "h2"])
                if h_any:
                    title = h_any.get_text(strip=True)

            if not title and soup.title:
                title = soup.title.get_text(strip=True)

            if not title:
                title = "Poste non spécifié"

            # Nettoyage du titre si présence de pipes ou tirets superflus
            if "|" in title:
                title = title.split("|")[0].strip()

            # Extraction du texte complet
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.extract()

            text_content = soup.get_text(separator="\n", strip=True)

        except Exception as e:
            print(f"[JobScraper] Attention: impossible de Fetch {url} ({e}). Utilisation d'un profil par défaut d'offre.")
            title = JobOfferScraper._guess_title_from_url(url)
            text_content = f"Offre d'emploi accessible à l'adresse : {url}\n\nDétails de l'offre non récupérables automatiquement (Erreur réseau/accès)."

        # Abréviation du poste
        abbreviation = JobOfferScraper.generate_abbreviation(title)

        return {
            "url": url,
            "site_name": site_name,
            "title": title,
            "abbreviation": abbreviation,
            "full_text": text_content
        }

    @staticmethod
    def _guess_title_from_url(url: str) -> str:
        path = urlparse(url).path
        slug = path.strip("/").split("/")[-1]
        if slug:
            clean_slug = re.sub(r"[-_]", " ", slug)
            clean_slug = re.sub(r"\d+", "", clean_slug).strip()
            if clean_slug:
                return clean_slug.title()
        return "Chargé De Mission"

    @staticmethod
    def generate_abbreviation(title: str) -> str:
        """
        Génère une abréviation courte pour le nom du fichier (ex: DEV-FULLSTACK-MOBILE, CHARGE-IT-DEV-WEB, ING-RESEAUX-SYS-TELECOM)
        """
        t = title.upper()
        # Normalisation
        t = re.sub(r"[ÉÈÊË]", "E", t)
        t = re.sub(r"[ÀÂ]", "A", t)
        t = re.sub(r"[ÎÏ]", "I", t)
        t = re.sub(r"[ÔÖ]", "O", t)
        t = re.sub(r"[ÛÜÙ]", "U", t)
        t = re.sub(r"[Ç]", "C", t)

        if "FULL STACK" in t or "FULLSTACK" in t:
            if "MOBILE" in t:
                return "DEV-FULLSTACK-MOBILE"
            return "DEV-FULLSTACK"
        if "IT" in t or "DEVELOPPEMENT WEB" in t:
            return "CHARGE-IT-DEV-WEB"
        if "RESEAUX" in t or "TELECOM" in t or "SYSTEMES" in t:
            return "ING-RESEAUX-SYS-TELECOM"
        if "DEVELOPPEUR" in t or "DEVELOPPER" in t:
            return "DEV-LOGICIEL"

        # Génération automatique par mots clés principaux
        words = re.findall(r"\b[A-Z]{3,}\b", t)
        ignored = {"POUR", "AVEC", "DANS", "DES", "LES", "UNE", "UNE", "CHEZ", "HAUT", "HF", "H-F"}
        words = [w for w in words if w not in ignored]
        if words:
            return "-".join(words[:4])
        return "POSTE"
