import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
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
    Canvas personnalisé pour s'assurer que le nombre de pages est comptabilisé.
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
            super().showPage()
        super().save()

def parse_user_info_file(user_info_path: str, user_id: str = "3") -> dict:
    """
    Lit et extrait les données structurées à partir du fichier /commandes/info/<ID_UTILISATEUR>.txt
    ou fournit un profil d'excellence pour la génération de CV/LM.
    """
    info_data = {
        "user_id": user_id,
        "nom": "MAKOSSO",
        "prenom": "Jean",
        "fullname": "Jean MAKOSSO",
        "phone": "+242 06 000 00 00",
        "email": "jean.makosso@email.com",
        "location": "Brazzaville & Pointe-Noire, Congo",
        "summary": "Consultant IT & Expert Fullstack certifié, spécialisé en ingénierie logicielle, infrastructures réseau et transformation digitale. Fort de plus de 6 ans d'expérience dans le déploiement d'architectures web, mobiles et d'infrastructures télécoms à fort impact. Expert reconnu pour maximiser l'efficience opérationnelle et la sécurisation des systèmes d'information.",
        "experiences": [
            {
                "title": "Ingénieur Logiciel Fullstack & Architecte Cloud",
                "company": "NOISIM ENGINEERING",
                "dates": "2023 - Présent",
                "achievements": [
                    "Conception et déploiement d'un système centralisé de péage réduisant les temps de traitement de 45% et sécurisant +1M$ de transactions.",
                    "Développement d'une passerelle USSD/API connectant Django, Angular et Flutter pour +50 000 utilisateurs actifs.",
                    "Intégration d'agrégateurs Fintech (MTN, Airtel, PayDunya) avec un taux de disponibilité système de 99,9%."
                ]
            },
            {
                "title": "Consultant en Stratégie Digitale & IT",
                "company": "Global Strategy Consulting",
                "dates": "2021 - 2023",
                "achievements": [
                    "Réalisation de 12 audits SI approfondis et refonte de schémas directeurs IT pour des grandes structures d'Afrique Centrale.",
                    "Optimisation des coûts d'infrastructures serveur et réseaux de 30% grâce à la conteneurisation Docker et automatisation DevOps.",
                    "Supervision d'équipes pluridisciplinaires (10+ ingénieurs) en méthodologie Agile/Scrum."
                ]
            },
            {
                "title": "Responsable Technique Systèmes & Réseaux",
                "company": "Airtel Congo B",
                "dates": "2019 - 2021",
                "achievements": [
                    "Supervision de l'interconnexion de 15+ sites distants avec tolérance aux pannes renforcée et sécurité VPN SSL.",
                    "Déploiement d'outils de monitoring temps réel réduisant le délai moyen de résolution des incidents (MTTR) de 60%.",
                    "Gestion et formation d'une équipe de support client et technicien sur le terrain."
                ]
            }
        ],
        "education": [
            "Licence Pro. Systèmes & Réseaux Informatiques | Université ESTAM (2020)",
            "Programme Passeport Numérique | Réseau 10 000 Codeurs (2022)",
            "Baccalauréat Scientifique (BAC C) | Mention Assez Bien"
        ],
        "certifications": [
            "Certification Cisco CCNA / DevOps Docker Specialist",
            "Certificat Expert Agile & Scrum Master"
        ],
        "projects": [
            "FoncierChain (1er Prix Hackathon 2026) : Architecture Blockchain & Cloud pour la sécurisation cadastrale.",
            "Passerelle Fintech Multi-pays : Intégration d'APIs de paiements Mobiles et Webhooks sécurisés."
        ],
        "hard_skills": ["Python / Django / DRF", "TypeScript / Angular / React", "Flutter / Dart (Mobile)", "Linux / Docker / Nginx / CI-CD", "Réseaux, VPN & Sécurité SI", "SQL / PostgreSQL / Redis"],
        "soft_skills": ["Leadership & Gestion de Projet", "Résolution complexe de problèmes", "Esprit d'analyse & Riguer", "Communication interpersonnelle"],
        "languages": ["Français (Natif/Courant)", "Anglais (Professionnel technique)"]
    }

    if os.path.exists(user_info_path):
        with open(user_info_path, "r", encoding="utf-8") as f:
            content = f.read()

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
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        'OfferBody',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1F2937')
    )

    story = []
    story.append(Paragraph(f"<b>OFFRE D'EMPLOI : {escape_xml(job_info['title'])}</b>", title_style))
    story.append(Paragraph(f"<b>Organisme / Site :</b> {escape_xml(job_info['site_name'].upper())}", body_style))
    story.append(Paragraph(f"<b>Source URL :</b> <a href='{escape_xml(job_info['url'])}'>{escape_xml(job_info['url'])}</a>", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB'), spaceBefore=8, spaceAfter=10))

    lines = job_info['full_text'].split('\n')
    for line in lines[:100]:
        line_str = line.strip()
        if line_str:
            story.append(Paragraph(escape_xml(line_str), body_style))
            story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=NumberedCanvas)


def generate_cv_pdf(user_data: dict, job_info: dict, cropped_photo_path: str, output_filepath: str):
    """
    Génère un CV moderne en PDF — STRICTEMENT 1 PAGE.
    Structure 2 colonnes (32% Gauche / 68% Droite).
    Calibrage dynamique pour un rendu remplissant parfaitement la page sans débordement.
    """
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=A4,
        leftMargin=18,
        rightMargin=18,
        topMargin=18,
        bottomMargin=18
    )

    # Styles colonne gauche
    sidebar_heading_style = ParagraphStyle(
        'SideHeading',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=6,
        spaceAfter=3
    )
    sidebar_item_style = ParagraphStyle(
        'SideItem',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#334155')
    )

    # Styles colonne principale (droite)
    name_style = ParagraphStyle(
        'CVName',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=19,
        textColor=colors.HexColor('#0F172A')
    )
    target_role_style = ParagraphStyle(
        'CVTargetRole',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=4
    )
    section_title_style = ParagraphStyle(
        'CVSectionTitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=5,
        spaceAfter=3
    )
    main_summary_style = ParagraphStyle(
        'CVSummary',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1F2937')
    )
    exp_title_style = ParagraphStyle(
        'CVExpTitle',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#111827')
    )
    exp_bullet_style = ParagraphStyle(
        'CVExpBullet',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#374151')
    )

    # --- CONTENU COLONNE GAUCHE (32%) ---
    left_flowables = []

    # 1. Photo de profil recadrée
    if os.path.exists(cropped_photo_path):
        try:
            img = Image(cropped_photo_path, width=90, height=90)
            left_flowables.append(img)
            left_flowables.append(Spacer(1, 6))
        except Exception:
            pass

    # 2. Coordonnées
    left_flowables.append(Paragraph("<b>COORDONNÉES</b>", sidebar_heading_style))
    left_flowables.append(Paragraph(f"<b>Tél :</b> {escape_xml(user_data['phone'])}", sidebar_item_style))
    left_flowables.append(Paragraph(f"<b>Email :</b> {escape_xml(user_data['email'])}", sidebar_item_style))
    left_flowables.append(Paragraph(f"<b>Lieu :</b> {escape_xml(user_data['location'])}", sidebar_item_style))
    left_flowables.append(Spacer(1, 5))

    # 3. Compétences Clés (Hard & Soft Skills avec mots-clés ATS)
    left_flowables.append(Paragraph("<b>HARD SKILLS</b>", sidebar_heading_style))
    for hs in user_data["hard_skills"]:
        left_flowables.append(Paragraph(f"• {escape_xml(hs)}", sidebar_item_style))
    left_flowables.append(Spacer(1, 4))

    left_flowables.append(Paragraph("<b>SOFT SKILLS</b>", sidebar_heading_style))
    for ss in user_data["soft_skills"]:
        left_flowables.append(Paragraph(f"• {escape_xml(ss)}", sidebar_item_style))
    left_flowables.append(Spacer(1, 5))

    # 4. Langues
    left_flowables.append(Paragraph("<b>LANGUES</b>", sidebar_heading_style))
    for lang in user_data["languages"]:
        left_flowables.append(Paragraph(f"• {escape_xml(lang)}", sidebar_item_style))
    left_flowables.append(Spacer(1, 5))

    # 5. Formations & Certifications
    left_flowables.append(Paragraph("<b>FORMATIONS</b>", sidebar_heading_style))
    for edu in user_data["education"]:
        left_flowables.append(Paragraph(f"• {escape_xml(edu)}", sidebar_item_style))
        left_flowables.append(Spacer(1, 2))


    # --- CONTENU COLONNE DROITE (68%) ---
    right_flowables = []

    # 1. En-tête (Nom + Poste visé exact)
    right_flowables.append(Paragraph(escape_xml(user_data['fullname']), name_style))
    right_flowables.append(Paragraph(escape_xml(job_info['title'].upper()), target_role_style))
    right_flowables.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=5))

    # 2. Profil / Accroche sur-mesure (3 phrases max)
    right_flowables.append(Paragraph("<b>PROFIL PROFESSIONNEL</b>", section_title_style))
    job_keywords = ", ".join(job_info.get("keywords", [])[:5])
    tailored_summary = (
        f"Expert confirmé et passionné, je cumule plus de 6 ans d'expérience dans la mise en œuvre de solutions à forte valeur ajoutée. "
        f"Spécialisé en {job_keywords if job_keywords else 'ingénierie et systèmes d abord'}, j apporte une rigueur éprouvée et une maîtrise technique pointue adaptée aux défis de {job_info['site_name'].title()}. "
        f"Orienté résultats, mon objectif est d optimiser l efficience opérationnelle de vos projets stratégiques en tant que {job_info['title']}."
    )
    right_flowables.append(Paragraph(escape_xml(tailored_summary), main_summary_style))
    right_flowables.append(Spacer(1, 5))

    # 3. Expériences Professionnelles (Réalisations chiffrées / impactantes)
    right_flowables.append(Paragraph("<b>EXPÉRIENCES PROFESSIONNELLES</b>", section_title_style))
    for exp in user_data["experiences"]:
        title_line = f"<b>{escape_xml(exp['title'])}</b> — {escape_xml(exp['company'])} ({escape_xml(exp['dates'])})"
        right_flowables.append(Paragraph(title_line, exp_title_style))
        for ach in exp["achievements"]:
            right_flowables.append(Paragraph(f"• {escape_xml(ach)}", exp_bullet_style))
        right_flowables.append(Spacer(1, 3))

    # 4. Projets Phares Pertinents
    right_flowables.append(Paragraph("<b>PROJETS PHARES & RÉALISATIONS</b>", section_title_style))
    for proj in user_data["projects"]:
        right_flowables.append(Paragraph(f"• <b>{escape_xml(proj)}</b>", exp_bullet_style))
        right_flowables.append(Spacer(1, 2))


    # Assemblage en Tableau à 2 colonnes (A4 imprimable = 559 pt de largeur totale utilisable)
    # 32% = 175 pt, 68% = 384 pt
    col_widths = [170, 384]
    table_data = [[left_flowables, right_flowables]]

    cv_table = Table(table_data, colWidths=col_widths)
    cv_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#F8FAFC')),
        ('PADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), 8),
        ('LEFTPADDING', (1, 0), (1, 0), 8),
        ('LINERIGHT', (0, 0), (0, 0), 1, colors.HexColor('#E2E8F0')),
    ]))

    doc.build([cv_table], canvasmaker=NumberedCanvas)


def generate_lm_pdf(user_data: dict, job_info: dict, output_filepath: str):
    """
    Génère une Lettre de Motivation (LM) en PDF — STRICTEMENT 1 PAGE.
    Structure Vous / Moi / Nous avec ton direct et confiant.
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

    header_user_style = ParagraphStyle('HeaderUser', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#1E293B'))
    header_company_style = ParagraphStyle('HeaderComp', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#1E293B'), alignment=2)
    object_style = ParagraphStyle('ObjectStyle', parent=styles['Heading3'], fontSize=10.5, leading=13.5, textColor=colors.HexColor('#1E3A8A'), spaceBefore=10, spaceAfter=10)
    body_style = ParagraphStyle('LMBody', parent=styles['Normal'], fontSize=9.5, leading=14, textColor=colors.HexColor('#1F2937'), spaceAfter=8)

    story = []

    # En-tête : Coordonnées Expéditeur / Destinataire
    candidate_info = f"<b>{escape_xml(user_data['fullname'])}</b><br/>{escape_xml(user_data['location'])}<br/>Tél : {escape_xml(user_data['phone'])}<br/>Email : {escape_xml(user_data['email'])}"
    company_info = f"<b>À l'attention de la Direction des Ressources Humaines</b><br/><b>{escape_xml(job_info['site_name'].title())}</b><br/>Fait à Brazzaville, le 19 Février 2026"

    header_table = Table([[Paragraph(candidate_info, header_user_style), Paragraph(company_info, header_company_style)]], colWidths=[260, 260])
    header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Objet
    obj_text = f"<b>OBJET : Candidature au poste de {escape_xml(job_info['title'])}</b>"
    story.append(Paragraph(obj_text, object_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2563EB'), spaceAfter=10))

    # Salutation
    story.append(Paragraph("Madame, Monsieur,", body_style))

    # Paragraphe 1 : L'entreprise & L'accroche (VOUS)
    p1 = f"Votre structure, <b>{escape_xml(job_info['site_name'].title())}</b>, s'impose comme un acteur clé nécessitant une excellence technique et une agilité constante. Le poste de <b>{escape_xml(job_info['title'])}</b> que vous proposez correspond exactement aux défis stratégiques que je souhaite relever au quotidien."
    story.append(Paragraph(p1, body_style))

    # Paragraphe 2 : Mon profil & Mes réalisations (MOI)
    p2 = f"Fort de plus de 6 ans d'expérience dans la conception d'architectures applicatives complexes, la gestion d'infrastructures et l'intégration de systèmes sécurisés, j'ai piloté des projets majeurs ayant permis d'accroître l'efficience opérationnelle de plus de 45%. Ma maîtrise des technologies modernes et ma rigueur professionnelle constituent des atouts directement transposables à vos besoins."
    story.append(Paragraph(p2, body_style))

    # Paragraphe 3 : La collaboration future (NOUS)
    p3 = f"Ensemble, nous pourrons accélérer le déploiement de vos solutions, garantir la haute disponibilité de vos systèmes et apporter une valeur ajoutée mesurable à vos utilisateurs. Mon approche pragmatique et orientée résultats saura s'intégrer rapidement au sein de vos équipes."
    story.append(Paragraph(p3, body_style))

    # Paragraphe 4 : Conclusion & Demande d'entretien
    p4 = f"Je me tiens à votre entière disposition pour échanger de vive voix lors d'un entretien afin de vous exposer plus en détail la pertinence de ma démarche. Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées."
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 12))

    # Signature
    signature_text = f"<b>{escape_xml(user_data['fullname'])}</b><br/>Consultant IT & Expert Fullstack"
    story.append(Paragraph(signature_text, ParagraphStyle('Sig', parent=body_style, alignment=2)))

    doc.build(story, canvasmaker=NumberedCanvas)


def generate_email_txt(user_data: dict, job_info: dict, cv_filename: str, lm_filename: str, output_filepath: str):
    """
    Génère un fichier texte .txt d'email au format strict :
    [Candidature - Intitulé du poste - Nom Prénom]
    """
    email_content = f"""Objet : Candidature - {job_info['title']} - {user_data['fullname']}

Madame, Monsieur,

C'est avec un grand intérêt que je vous soumets ma candidature pour le poste de {job_info['title']} au sein de {job_info['site_name'].title()}.

Fort de mon expertise en ingénierie logicielle et transformation digitale, je suis convaincu de pouvoir apporter une contribution significative et immédiate à vos projets. Vous trouverez ci-joint mon Curriculum Vitae ({cv_filename}) ainsi que ma Lettre de Motivation ({lm_filename}).

Je me tiens à votre disposition pour un échange téléphonique ou un entretien à votre convenance afin de vous exposer mes motivations.

Cordialement,

{user_data['fullname']}
Consultant IT & Expert Fullstack
Tél : {user_data['phone']}
Email : {user_data['email']}
{user_data['location']}
"""
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(email_content)
