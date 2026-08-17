import os
import shutil
from pathlib import Path
from django.conf import settings
from .models import UserProfileInfo, Experience, Certification, Education, Project, Profile

class CommandesSyncService:
    @staticmethod
    def sync_user_commandes(user):
        base_dir = Path(settings.BASE_DIR).parent if hasattr(settings, 'BASE_DIR') else Path.cwd()
        info_dir = base_dir / "commandes" / "info"
        photo_dir = base_dir / "commandes" / "photo"

        info_dir.mkdir(parents=True, exist_ok=True)
        photo_dir.mkdir(parents=True, exist_ok=True)

        user_id = str(user.id)
        info_file_path = info_dir / f"{user_id}.txt"
        photo_file_path = photo_dir / f"{user_id}.png"

        # Fetch profile models
        info = UserProfileInfo.objects.filter(user=user).first()
        exps = Experience.objects.filter(user=user)
        certs = Certification.objects.filter(user=user)
        edus = Education.objects.filter(user=user)
        projs = Project.objects.filter(user=user)
        profile = Profile.objects.filter(user=user).first()

        lines = []
        lines.append(f"=== INFORMATIONS UTILISATEUR (ID: {user_id}) ===")
        if info:
            lines.append(f"Nom : {info.last_name}")
            lines.append(f"Prénom : {info.first_name}")
            lines.append(f"Genre : {info.gender}")
            lines.append(f"Date de naissance : {info.birth_date or 'N/A'}")
            lines.append(f"Numéro principal : {info.primary_phone}")
            lines.append(f"Numéro secondaire : {info.secondary_phone}")
            lines.append(f"Adresse : {info.address}")
            lines.append(f"Pays : {info.country}")
            lines.append(f"Arrondissement : {info.district}")
            lines.append(f"Quartier : {info.neighborhood}")
            lines.append(f"Résumé professionnel : {info.professional_summary}")
        else:
            lines.append(f"Nom : {user.last_name or 'N/A'}")
            lines.append(f"Prénom : {user.first_name or 'N/A'}")

        lines.append("\n=== EXPERIENCES PROFESSIONNELLES ===")
        for exp in exps:
            is_current_str = "Oui" if exp.is_current else "Non"
            lines.append(f"- Poste : {exp.title} | Structure : {exp.company} | Secteur : {exp.industry} | Lieu : {exp.location} | Début : {exp.start_date} | Fin : {exp.end_date or 'N/A'} | Jusqu'à présent : {is_current_str} | Compétences acquises : {exp.skills_acquired}")

        lines.append("\n=== CERTIFICATIONS ET ATTESTATIONS ===")
        for cert in certs:
            lines.append(f"- Libellé : {cert.title} | Année : {cert.year} | Institution : {cert.institution} | Lieu : {cert.location} | PDF Drive : {cert.pdf_url or 'N/A'} | Description : {cert.description}")

        lines.append("\n=== DIPLOMES ===")
        for edu in edus:
            lines.append(f"- Libellé : {edu.title} | Année : {edu.year} | Institution : {edu.institution} | Niveau d'étude : {edu.degree_level} | Spécialité : {edu.field_of_study} | PDF Drive : {edu.pdf_url or 'N/A'} | Compétences acquises : {edu.skills_acquired}")

        lines.append("\n=== PROJETS ===")
        for proj in projs:
            lines.append(f"- Nom : {proj.name} | Secteur : {proj.industry} | Bénéficiaire : {proj.beneficiary} | Lien : {proj.link_url} | Description : {proj.description}")

        with open(info_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        # Copy cropped photo if exists
        if profile and profile.cropped_photo and os.path.exists(profile.cropped_photo.path):
            shutil.copy2(profile.cropped_photo.path, photo_file_path)

        return info_file_path, photo_file_path
