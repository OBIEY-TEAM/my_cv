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

    def generate_cv_text(self, candidate_info: dict, job_offer_text: str = None, language: str = "fr") -> str:
        """
        Génère le texte structuré du CV.
        Si job_offer_text est None ou vide => Génération du CV uniquement (sans offre d'emploi).
        """
        lang_names = {
            "fr": "français", "en": "english", "ar": "arabic (العربية)",
            "pt": "portuguese", "es": "spanish", "sw": "swahili", "zh": "chinese (中文)"
        }
        lang_str = lang_names.get(language, "français")

        system_prompt = (
            f"You are an expert in writing professional CVs and ATS optimization. "
            f"Write a clear, impactful, and structured CV strictly in {lang_str}."
        )

        prompt = f"Candidate info:\n{json.dumps(candidate_info, ensure_ascii=False, indent=2)}\n\n"
        if job_offer_text and job_offer_text.strip():
            prompt += f"Job Offer:\n{job_offer_text}\n\n"
            prompt += f"Write a tailored profile and CV content strictly in {lang_str} for this job offer."
        else:
            prompt += f"CV ONLY: No job offer provided. Write a full generalist CV strictly in {lang_str}."

        result = self._call_groq(prompt, system_prompt)
        if not result:
            nom = candidate_info.get("fullname", candidate_info.get("first_name", "Candidat"))
            summary = candidate_info.get("professional_summary", "Professionnel qualifié et motivé.")
            result = f"CURRICULUM VITAE DE {nom}\n\nPROFIL PROFESSIONNEL:\n{summary}\n\nCOMPÉTENCES & EXPÉRIENCES:\nContenu structuré pour la candidature."

        return result

    def generate_cover_letter_text(self, candidate_info: dict, job_offer_text: str, job_title: str, company_name: str, language: str = "fr") -> str:
        """
        Génère le texte de la Lettre de Motivation (LM).
        Ne doit être généré QUE si l'offre d'emploi est présente.
        """
        if not job_offer_text or not job_offer_text.strip():
            return "LM non disponible : Aucune offre d'emploi fournie."

        lang_names = {
            "fr": "français", "en": "english", "ar": "arabic (العربية)",
            "pt": "portuguese", "es": "spanish", "sw": "swahili", "zh": "chinese (中文)"
        }
        lang_str = lang_names.get(language, "français")

        system_prompt = (
            f"You are a recruitment expert. Write a professional Cover Letter strictly in {lang_str} "
            "following a direct, convincing structure (strictly 1 page)."
        )

        prompt = (
            f"Candidate : {candidate_info.get('fullname', 'Candidate')}\n"
            f"Job Title : {job_title}\n"
            f"Company : {company_name}\n"
            f"Candidate Profile : {json.dumps(candidate_info, ensure_ascii=False)}\n"
            f"Job Offer :\n{job_offer_text}\n\n"
            f"Write the full cover letter strictly in {lang_str}."
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

    def generate_email_text(self, candidate_info: dict, job_title: str, company_name: str, language: str = "fr") -> str:
        """
        Génère l'Email de candidature.
        """
        lang_names = {
            "fr": "français", "en": "english", "ar": "arabic (العربية)",
            "pt": "portuguese", "es": "spanish", "sw": "swahili", "zh": "chinese (中文)"
        }
        lang_str = lang_names.get(language, "français")

        system_prompt = f"Write a short, polite, and professional application email strictly in {lang_str}."
        prompt = (
            f"Subject/Topic: Application - {job_title} - {candidate_info.get('fullname', '')}\n"
            f"Write the email body to the recruiter at {company_name} in {lang_str}."
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
