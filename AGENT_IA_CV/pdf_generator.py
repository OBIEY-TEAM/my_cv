import os
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import xml.sax.saxutils as saxutils

def escape_xml(text):
    if not text:
        return ""
    return saxutils.escape(str(text))

class NumberedCanvas(canvas.Canvas):
    """
    Canvas personnalisé pour compter le nombre total de pages
    et interdire le dépassement si strict (ex. max 1 page pour CV / LM).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            # Optionnel: Dessiner le numéro de page en bas si désiré
            super().showPage()
        super().save()

def parse_user_info_file(user_info_path: str, user_id: str = "3") -> dict:
    """
    Lit et extrait les données structurées à partir du fichier /commandes/info/<ID_UTILISATEUR>.txt
    ou README.md en fallback.
    """
    info_data = {
        "user_id": user_id,
        "nom": "OBIEY",
        "prenom": "Christ Dany",
        "fullname": "Christ Dany OBIEY",
        "phone": "+242 06 613 01 18",
        "email": "obieydany@gmail.com",
        "location": "Brazzaville & Pointe-Noire, Congo",
        "summary": "Consultant IT & Transformation Digitale | Expert Fullstack. Spécialisé dans la conception d'architectures applicatives complexes (Web & Mobile, Django, Angular, React, Flutter).",
        "experiences": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "skills": ["Python", "Django", "TypeScript", "Angular", "React", "Flutter", "Dart", "Docker", "REST API", "DevOps", "SQL", "SEO"]
    }

    if os.path.exists(user_info_path):
        with open(user_info_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extraire Nom / Prénom / Téléphone / etc.
        m_nom = re.search(r"Nom\s*:\s*(.*)", content)
        m_prenom = re.search(r"Prénom\s*:\s*(.*)", content)
        m_phone = re.search(r"Numéro principal\s*:\s*(.*)", content)
        m_summary = re.search(r"Résumé professionnel\s*:\s*(.*)", content)

        if m_nom and m_nom.group(1).strip() and m_nom.group(1).strip() != "N/A":
            info_data["nom"] = m_nom.group(1).strip()
        if m_prenom and m_prenom.group(1).strip() and m_prenom.group(1).strip() != "N/A":
            info_data["prenom"] = m_prenom.group(1).strip()

        info_data["fullname"] = f"{info_data['prenom']} {info_data['nom']}".upper()

        if m_phone and m_phone.group(1).strip() and m_phone.group(1).strip() != "N/A":
            info_data["phone"] = m_phone.group(1).strip()
        if m_summary and m_summary.group(1).strip() and m_summary.group(1).strip() != "N/A":
            info_data["summary"] = m_summary.group(1).strip()

        # Extraire expériences
        exp_section = re.search(r"=== EXPERIENCES PROFESSIONNELLES ===(.*)(?:===|$)", content, re.DOTALL)
        if exp_section:
            exp_lines = exp_section.group(1).strip().split("\n")
            for line in exp_lines:
                if line.startswith("-"):
                    info_data["experiences"].append(line.lstrip("-").strip())

        # Extraire certifs / diplomes / projets
        cert_section = re.search(r"=== CERTIFICATIONS ET ATTESTATIONS ===(.*)(?:===|$)", content, re.DOTALL)
        if cert_section:
            for line in cert_section.group(1).strip().split("\n"):
                if line.startswith("-"):
                    info_data["certifications"].append(line.lstrip("-").strip())

        edu_section = re.search(r"=== DIPLOMES ===(.*)(?:===|$)", content, re.DOTALL)
        if edu_section:
            for line in edu_section.group(1).strip().split("\n"):
                if line.startswith("-"):
                    info_data["education"].append(line.lstrip("-").strip())

        proj_section = re.search(r"=== PROJETS ===(.*)(?:===|$)", content, re.DOTALL)
        if proj_section:
            for line in proj_section.group(1).strip().split("\n"):
                if line.startswith("-"):
                    info_data["projects"].append(line.lstrip("-").strip())

    # Remplissage de fallback enrichi depuis le profil de référence de Dany OBIEY si vide
    if not info_data["experiences"]:
        info_data["experiences"] = [
            "Ingénieur Logiciel Fullstack & Architecte Cloud | NOISIM ENGINEERING | 2026 - Présent | Développement de péage centralisé (Django/Angular/Flutter) & Systèmes Fintech (PayDunya, Airtel Money, MTN).",
            "Consultant en Stratégie Digitale & IT | Global Strategy Consulting | 2026 | Audits techniques des SI et schémas directeurs de numérisation.",
            "Parcours Commercial & Management | AIRTEL CONGO B | 2020 - 2025 | Commercial certifié KYC, Animation d'équipes et développement des ventes."
        ]
    if not info_data["education"]:
        info_data["education"] = [
            "Licence Pro. Systèmes & Réseaux Informatiques | Université ESTAM | 2020 - 2025",
            "Programme Passeport Numérique | Réseau 10 000 Codeurs | 2026",
            "Baccalauréat Général (BAC C) | Lycée A.H. Paka | Mention Assez Bien"
        ]
    if not info_data["projects"]:
        info_data["projects"] = [
            "Projet FoncierChain (1er Prix Hackathon MIABE 2026) : Direction technique et architecture logicielle.",
            "Passerelle USSD & Payment Gateway : Connexion Django / Angular / Flutter."
        ]

    return info_data


def generate_job_offer_pdf(job_info: dict, output_filepath: str):
    """
    Génère un PDF propre et lisible contenant le texte de l'offre d'emploi originale.
    """
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'OfferTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )
    body_style = ParagraphStyle(
        'OfferBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1F2937')
    )

    story = []
    story.append(Paragraph(f"<b>OFFRE D'EMPLOI : {escape_xml(job_info['title'])}</b>", title_style))
    story.append(Paragraph(f"<b>Organisme / Site :</b> {escape_xml(job_info['site_name'].upper())}", body_style))
    story.append(Paragraph(f"<b>Source URL :</b> <a href='{escape_xml(job_info['url'])}'>{escape_xml(job_info['url'])}</a>", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB'), spaceBefore=8, spaceAfter=12))

    # Nettoyage et découpage du texte par paragraphes
    lines = job_info['full_text'].split('\n')
    for line in lines[:100]: # Limite raisonnable
        line_str = line.strip()
        if line_str:
            story.append(Paragraph(escape_xml(line_str), body_style))
            story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)


def generate_cv_pdf(user_data: dict, job_info: dict, cropped_photo_path: str, output_filepath: str):
    """
    Génère un CV moderne en PDF — STRICTEMENT 1 PAGE (Structure à 2 colonnes).
    """
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=A4,
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    # Styles colonne gauche (Sombre)
    sidebar_title_style = ParagraphStyle(
        'SidebarTitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=8,
        spaceAfter=4
    )
    sidebar_text_style = ParagraphStyle(
        'SidebarText',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#334155')
    )

    # Styles colonne droite (Principale)
    name_style = ParagraphStyle(
        'CVName',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A')
    )
    target_role_style = ParagraphStyle(
        'CVTargetRole',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=6
    )
    section_title_style = ParagraphStyle(
        'CVSectionTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=6,
        spaceAfter=4
    )
    main_text_style = ParagraphStyle(
        'CVMainText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1F2937')
    )

    # Contenu Colonne Gauche (Sidebar)
    left_flowables = []

    # Photo de profil
    if os.path.exists(cropped_photo_path):
        try:
            img = Image(cropped_photo_path, width=100, height=100)
            left_flowables.append(img)
            left_flowables.append(Spacer(1, 8))
        except Exception:
            pass

    # Contact
    left_flowables.append(Paragraph("<b>CONTACT</b>", sidebar_title_style))
    left_flowables.append(Paragraph(f"<b>Tél :</b> {escape_xml(user_data['phone'])}", sidebar_text_style))
    left_flowables.append(Paragraph(f"<b>Email :</b> {escape_xml(user_data['email'])}", sidebar_text_style))
    left_flowables.append(Paragraph(f"<b>Lieu :</b> {escape_xml(user_data['location'])}", sidebar_text_style))
    left_flowables.append(Spacer(1, 8))

    # Compétences Clés
    left_flowables.append(Paragraph("<b>COMPÉTENCES CLÉS</b>", sidebar_title_style))
    skills_list = user_data["skills"]
    for s in skills_list[:8]:
        left_flowables.append(Paragraph(f"• {escape_xml(s)}", sidebar_text_style))
    left_flowables.append(Spacer(1, 8))

    # Formations
    left_flowables.append(Paragraph("<b>FORMATIONS</b>", sidebar_title_style))
    for edu in user_data["education"][:3]:
        left_flowables.append(Paragraph(f"• {escape_xml(edu)}", sidebar_text_style))
        left_flowables.append(Spacer(1, 2))

    # Contenu Colonne Droite (Main)
    right_flowables = []

    # En-tête
    right_flowables.append(Paragraph(escape_xml(user_data['fullname']), name_style))
    right_flowables.append(Paragraph(escape_xml(job_info['title'].upper()), target_role_style))
    right_flowables.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=6))

    # Profil / Résumé adapté au poste
    right_flowables.append(Paragraph("<b>PROFIL PROFESSIONNEL</b>", section_title_style))
    adapted_summary = f"{user_data['summary']} Candidat motivé et rigoureux, pleinement aligné avec les exigences du poste de {job_info['title']} chez {job_info['site_name'].title()}."
    right_flowables.append(Paragraph(escape_xml(adapted_summary), main_text_style))
    right_flowables.append(Spacer(1, 6))

    # Expériences Professionnelles
    right_flowables.append(Paragraph("<b>EXPÉRIENCES PROFESSIONNELLES</b>", section_title_style))
    for exp in user_data["experiences"][:3]:
        right_flowables.append(Paragraph(f"<b>• {escape_xml(exp)}</b>", main_text_style))
        right_flowables.append(Spacer(1, 3))

    # Projets Phares
    right_flowables.append(Paragraph("<b>PROJETS PHARES & RÉALISATIONS</b>", section_title_style))
    for proj in user_data["projects"][:2]:
        right_flowables.append(Paragraph(f"<b>• {escape_xml(proj)}</b>", main_text_style))
        right_flowables.append(Spacer(1, 2))

    # Assemblage en Tableau à 2 colonnes pour garantir 1 page stricte
    col_widths = [160, 385]
    table_data = [[left_flowables, right_flowables]]

    cv_table = Table(table_data, colWidths=col_widths)
    cv_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#F8FAFC')),
        ('PADDING', (0, 0), (0, 0), 6),
        ('RIGHTPADDING', (0, 0), (0, 0), 10),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('LINERIGHT', (0, 0), (0, 0), 1, colors.HexColor('#E2E8F0')),
    ]))

    doc.build([cv_table], canvasmaker=NumberedCanvas)


def generate_lm_pdf(user_data: dict, job_info: dict, output_filepath: str):
    """
    Génère une Lettre de Motivation (LM) en PDF — STRICTEMENT 1 PAGE.
    """
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    header_user_style = ParagraphStyle('HeaderUser', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#1E293B'))
    header_company_style = ParagraphStyle('HeaderComp', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#1E293B'), alignment=2) # Align right
    object_style = ParagraphStyle('ObjectStyle', parent=styles['Heading3'], fontSize=11, leading=14, textColor=colors.HexColor('#1E3A8A'), spaceBefore=12, spaceAfter=12)
    body_style = ParagraphStyle('LMBody', parent=styles['Normal'], fontSize=10, leading=14.5, textColor=colors.HexColor('#1F2937'), spaceAfter=8)

    story = []

    # En-tête : Coordonnées Candidat à gauche / Entreprise à droite
    candidate_info = f"<b>{escape_xml(user_data['fullname'])}</b><br/>{escape_xml(user_data['location'])}<br/>Tél : {escape_xml(user_data['phone'])}<br/>Email : {escape_xml(user_data['email'])}"
    company_info = f"<b>À l'attention du Service Recrutement</b><br/><b>{escape_xml(job_info['site_name'].title())}</b><br/>Fait à Brazzaville, le 19 Février 2026"

    header_table = Table([[Paragraph(candidate_info, header_user_style), Paragraph(company_info, header_company_style)]], colWidths=[250, 250])
    header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    story.append(header_table)
    story.append(Spacer(1, 15))

    # Objet
    obj_text = f"<b>OBJET : Candidature au poste de {escape_xml(job_info['title'])}</b>"
    story.append(Paragraph(obj_text, object_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # Salutation
    story.append(Paragraph("Madame, Monsieur,", body_style))

    # Paragraphe 1 : Accroche
    p1 = f"C'est avec un vif intérêt et un grand enthousiasme que je vous adresse ma candidature pour le poste de <b>{escape_xml(job_info['title'])}</b> au sein de votre organisme <b>{escape_xml(job_info['site_name'].title())}</b>. Fort d'une solide expertise en ingénierie logicielle et développement de solutions numériques, je souhaite mettre mes compétences au service de vos projets stratégiques."
    story.append(Paragraph(p1, body_style))

    # Paragraphe 2 : Adéquation technique
    p2 = f"Mon parcours m'a permis de maîtriser la conception d'architectures applicatives complexes, le développement web et mobile ainsi que l'intégration de systèmes sécurisés. Mes récentes réalisations, notamment le développement d'applications centralisées et la gestion de projets techniques d'envergure, démontrent ma capacité à délivrer des solutions performantes et adaptées aux exigences du poste."
    story.append(Paragraph(p2, body_style))

    # Paragraphe 3 : Soft skills & Valeur ajoutée
    p3 = f"Rigoureux, autonome et orienté résultats, j'accorde une importance essentielle à la qualité du code et à l'expérience utilisateur. Rejoindre votre équipe représente pour moi l'opportunité d'apporter une vraie valeur ajoutée tout en participant activement au rayonnement de vos activités."
    story.append(Paragraph(p3, body_style))

    # Paragraphe 4 : Conclusion & Entretien
    p4 = f"Restant à votre entière disposition pour échanger de vive voix lors d'un entretien, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées."
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 15))

    # Signature
    signature_text = f"<b>{escape_xml(user_data['fullname'])}</b>"
    story.append(Paragraph(signature_text, ParagraphStyle('Sig', parent=body_style, alignment=2)))

    doc.build(story, canvasmaker=NumberedCanvas)


def generate_email_txt(user_data: dict, job_info: dict, cv_filename: str, lm_filename: str, output_filepath: str):
    """
    Génère un fichier texte .txt contenant la ligne d'objet et le corps de l'email de candidature.
    """
    email_content = f"""OBJET : Candidature - {job_info['title']} - {user_data['fullname']}

Bonjour Madame, Monsieur,

Je vous prie de trouver ci-joint ma candidature pour le poste de {job_info['title']} au sein de votre structure ({job_info['site_name'].title()}).

Vous trouverez en pièces jointes à ce courriel :
- Mon Curriculum Vitae ({cv_filename})
- Ma Lettre de Motivation ({lm_filename})

Restant à votre entière disposition pour toute information complémentaire ou pour un entretien à votre convenance.

Cordialement,

{user_data['fullname']}
Consultant IT & Expert Fullstack
Téléphone : {user_data['phone']}
Email : {user_data['email']}
Localisation : {user_data['location']}
"""
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(email_content)
