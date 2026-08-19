import os
import sys
import argparse
from pathlib import Path

from AGENT_IA_CV.image_processor import process_profile_photo
from AGENT_IA_CV.job_scraper import JobOfferScraper
from AGENT_IA_CV.pdf_generator import (
    parse_user_info_file,
    generate_job_offer_pdf,
    generate_cv_pdf,
    generate_lm_pdf,
    generate_email_txt
)

DEFAULT_URLS = [
    "https://www.acpe.cg/details-offre-emplois/4200",
    "https://www.bluecollarcongo.com/en/jobs/charge-e-it-developpement-web-717",
    "https://www.acpe.cg/details-offre-emplois/4191"
]

def sanitize_foldername(name: str) -> str:
    """
    Sanitize folder name while keeping valid directory characters.
    """
    # Replace invalid chars but keep spaces or standard job title formatting
    clean = name.replace("/", "-").replace("\\", "-").strip()
    return clean

def run_agent(user_id: str = "3", urls: list = None, root_dir: str = "."):
    if not urls:
        urls = DEFAULT_URLS

    print(f"=== DEMARRAGE AGENT IA CV [UTILISATEUR: {user_id}] ===")

    # ÉTAPE 3 — Traitement professionnel de la photo de profil
    print("\n--- ÉTAPE 3 : Traitement photo de profil ---")
    cropped_photo = process_profile_photo(user_id=user_id, root_dir=root_dir)

    # Récupération des informations utilisateur
    user_info_file = os.path.join(root_dir, "commandes", "info", f"{user_id}.txt")
    user_data = parse_user_info_file(user_info_file, user_id=user_id)
    nom_user = user_data["nom"].upper()

    # Traitement de chaque offre d'emploi
    for idx, url in enumerate(urls, 1):
        print(f"\n--- ÉTAPE 1 & 2 & 4 : Traitement Offre {idx}/{len(urls)} ({url}) ---")
        job_info = JobOfferScraper.scrape_url(url)

        site_name = job_info["site_name"]
        job_title = job_info["title"]
        abbreviation = job_info["abbreviation"]

        # Arborescence : /resultat/<ID_UTILISATEUR>/<nom_site>/<Intitulé du Poste>
        target_dir = os.path.join(root_dir, "resultat", user_id, site_name, sanitize_foldername(job_title))
        os.makedirs(target_dir, exist_ok=True)
        print(f"Dossier cible : {target_dir}")

        # Noms des fichiers
        # NOM_UTILISATEUR-[ABRÉVIATION-POSTE]-OFFRE.pdf
        offer_pdf_name = f"{nom_user}-{abbreviation}-OFFRE.pdf"
        cv_pdf_name = f"{nom_user}-{abbreviation}-CV.pdf"
        lm_pdf_name = f"{nom_user}-{abbreviation}-LM.pdf"
        email_txt_name = f"{nom_user}-{abbreviation}-EMAIL.txt"

        offer_pdf_path = os.path.join(target_dir, offer_pdf_name)
        cv_pdf_path = os.path.join(target_dir, cv_pdf_name)
        lm_pdf_path = os.path.join(target_dir, lm_pdf_name)
        email_txt_path = os.path.join(target_dir, email_txt_name)

        # Génération des livrables
        print(f"Génération Offre PDF : {offer_pdf_name}")
        generate_job_offer_pdf(job_info, offer_pdf_path)

        print(f"Génération CV PDF (1 page) : {cv_pdf_name}")
        generate_cv_pdf(user_data, job_info, cropped_photo, cv_pdf_path)

        print(f"Génération LM PDF (1 page) : {lm_pdf_name}")
        generate_lm_pdf(user_data, job_info, lm_pdf_path)

        print(f"Génération Email TXT : {email_txt_name}")
        generate_email_txt(user_data, job_info, cv_pdf_name, lm_pdf_name, email_txt_path)

    print("\n=== TRAITEMENT DE TOUTES LES OFFRES ERFFECTUÉ AVEC SUCCÈS ===")

def main():
    parser = argparse.ArgumentParser(description="Agent IA CV - Automatisation de candidatures")
    parser.add_argument("--user-id", type=str, default="3", help="Identifiant utilisateur dans /commandes/info/<ID>.txt")
    parser.add_argument("--urls", nargs="*", default=DEFAULT_URLS, help="Liste des URLs des offres d'emploi à traiter")
    args = parser.parse_args()

    run_agent(user_id=args.user_id, urls=args.urls)

if __name__ == "__main__":
    main()
