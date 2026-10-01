import os
import json
import urllib.request
import urllib.error

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class GroqCVAgent:
    """
    Agent IA connecté à l'API Groq Cloud pour rédiger le CV, la lettre de motivation (LM) et l'Email.
    Règle importante : Permettre la rédaction du CV UNIQUEMENT en l'absence de l'offre d'emploi.
    """

    def __init__(self, api_key: str = GROQ_API_KEY, model: str = DEFAULT_MODEL):
        self.api_key = api_key or GROQ_API_KEY
        self.model = model or DEFAULT_MODEL

    def _call_groq(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }).encode('utf-8')

        req = urllib.request.Request(
            GROQ_API_URL,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    res_data = json.loads(response.read().decode('utf-8'))
                    choices = res_data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"[GroqCVAgent] Connexion Groq API impossible : {e}")
        return ""

    def generate_cv_text(self, candidate_info: dict, job_offer_text: str = None) -> str:
        """
        Génère le texte structuré du CV.
        Si job_offer_text est None ou vide => Génération du CV uniquement (sans offre d'emploi).
        """
        system_prompt = (
            "Vous êtes un expert en rédaction de CV professionnels et optimisation ATS. "
            "Rédigez un CV clair, percutant et structuré en français."
        )

        prompt = f"Informations du candidat :\n{json.dumps(candidate_info, ensure_ascii=False, indent=2)}\n\n"
        if job_offer_text and job_offer_text.strip():
            prompt += f"Offre d'emploi ciblée :\n{job_offer_text}\n\n"
            prompt += "Rédigez un profil et un contenu de CV adaptés à cette offre d'emploi."
        else:
            prompt += "REDACTION DU CV UNIQUEMENT : Aucune offre d'emploi fournie. Rédigez un CV généraliste complet et valorisant basé sur le profil du candidat."

        result = self._call_groq(prompt, system_prompt)
        if not result:
            nom = candidate_info.get("fullname", candidate_info.get("first_name", "Candidat"))
            summary = candidate_info.get("professional_summary", "Professionnel qualifié et motivé.")
            result = f"CURRICULUM VITAE DE {nom}\n\nPROFIL PROFESSIONNEL:\n{summary}\n\nCOMPÉTENCES & EXPÉRIENCES:\nContenu structuré pour la candidature."

        return result

    def generate_cover_letter_text(self, candidate_info: dict, job_offer_text: str, job_title: str, company_name: str) -> str:
        """
        Génère le texte de la Lettre de Motivation (LM).
        Ne doit être généré QUE si l'offre d'emploi est présente.
        """
        if not job_offer_text or not job_offer_text.strip():
            return "LM non disponible : Aucune offre d'emploi fournie."

        system_prompt = (
            "Vous êtes un expert en recrutement. Rédigez une Lettre de Motivation professionnelle en français "
            "selon la structure Vous / Moi / Nous, directe et convaincante (strictement 1 page)."
        )

        prompt = (
            f"Candidat : {candidate_info.get('fullname', 'Candidat')}\n"
            f"Poste : {job_title}\n"
            f"Entreprise : {company_name}\n"
            f"Profil candidat : {json.dumps(candidate_info, ensure_ascii=False)}\n"
            f"Offre d'emploi :\n{job_offer_text}\n\n"
            "Rédigez la lettre de motivation complète."
        )

        result = self._call_groq(prompt, system_prompt)
        if not result:
            result = (
                f"Madame, Monsieur,\n\n"
                f"C'est avec un vif intérêt que je postule au poste de {job_title} au sein de {company_name}.\n\n"
                f"Fort de mon expérience, je suis convaincu de pouvoir contribuer efficacement à la réussite de vos projets.\n\n"
                f"Cordialement,\n{candidate_info.get('fullname', '')}"
            )
        return result

    def generate_email_text(self, candidate_info: dict, job_title: str, company_name: str) -> str:
        """
        Génère l'Email de candidature.
        """
        system_prompt = "Rédigez un email de candidature court, poli et professionnel en français."
        prompt = (
            f"Objet: Candidature - {job_title} - {candidate_info.get('fullname', '')}\n"
            f"Rédiger le corps du mail à l'attention du recruteur de {company_name}."
        )

        result = self._call_groq(prompt, system_prompt)
        if not result:
            result = (
                f"Objet : Candidature - {job_title} - {candidate_info.get('fullname', '')}\n\n"
                f"Madame, Monsieur,\n\n"
                f"Veuillez trouver ci-joint mon CV et ma lettre de motivation pour le poste de {job_title} chez {company_name}.\n\n"
                f"Bien cordialement,\n{candidate_info.get('fullname', '')}"
            )
        return result
