import os
import zipfile
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from pypdf import PdfReader

class PDFGenerator:
    @staticmethod
    def verify_1_page_limit(pdf_path):
        """Verifies strictly that the generated PDF has exactly 1 page."""
        reader = PdfReader(pdf_path)
        return len(reader.pages) == 1

    @staticmethod
    def generate_cv_pdf(cv_data, output_path):
        """
        Generates a modern 2-column strictly 1-page CV PDF using ReportLab.
        32% Left Sidebar (#0B1F3A navy): photo, contact, skills (ATS optimized), education/certifications.
        68% Right Column: Name, title, 3-sentence hook summary, experiences with metrics/impact, key projects.
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=0.4 * cm,
            rightMargin=0.4 * cm,
            topMargin=0.4 * cm,
            bottomMargin=0.4 * cm
        )

        styles = getSampleStyleSheet()

        left_header_style = ParagraphStyle(
            'LeftHeader', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=9.5, leading=11,
            textColor=colors.HexColor('#FFFFFF'), spaceAfter=3
        )

        left_text_style = ParagraphStyle(
            'LeftText', parent=styles['Normal'],
            fontName='Helvetica', fontSize=7.5, leading=9.5,
            textColor=colors.HexColor('#E2E8F0')
        )

        right_title_style = ParagraphStyle(
            'RightTitle', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=17, leading=19,
            textColor=colors.HexColor('#0B1F3A')
        )

        right_subtitle_style = ParagraphStyle(
            'RightSubtitle', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=10.5, leading=12,
            textColor=colors.HexColor('#185FA5')
        )

        right_section_style = ParagraphStyle(
            'RightSection', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=11, leading=13,
            textColor=colors.HexColor('#0B1F3A'), spaceAfter=3
        )

        right_body_style = ParagraphStyle(
            'RightBody', parent=styles['Normal'],
            fontName='Helvetica', fontSize=8, leading=10,
            textColor=colors.HexColor('#334155')
        )

        right_bold_style = ParagraphStyle(
            'RightBold', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=9, leading=11,
            textColor=colors.HexColor('#0B1F3A')
        )

        left_elements = []

        photo_path = cv_data.get('photo_path')
        if photo_path and os.path.exists(photo_path):
            try:
                img = Image(photo_path, width=3.6*cm, height=3.6*cm)
                left_elements.append(img)
                left_elements.append(Spacer(1, 0.2*cm))
            except Exception:
                pass

        left_elements.append(Paragraph("CONTACT", left_header_style))
        left_elements.append(Paragraph(f"📍 {cv_data.get('location', 'Brazzaville, Congo')}", left_text_style))
        left_elements.append(Paragraph(f"📞 {cv_data.get('phone', '+242 06 613 01 18')}", left_text_style))
        left_elements.append(Paragraph(f"✉️ {cv_data.get('email', 'obieydany@gmail.com')}", left_text_style))
        left_elements.append(Spacer(1, 0.3*cm))

        left_elements.append(Paragraph("COMPÉTENCES CLÉS", left_header_style))
        skills_dict = cv_data.get('skills', {})
        for cat, items in skills_dict.items():
            left_elements.append(Paragraph(f"<b>{cat}:</b>", left_text_style))
            left_elements.append(Paragraph(", ".join(items[:6]), left_text_style))
            left_elements.append(Spacer(1, 0.1*cm))
        left_elements.append(Spacer(1, 0.2*cm))

        left_elements.append(Paragraph("FORMATIONS & CERTIFS", left_header_style))
        for edu in cv_data.get('education', [])[:4]:
            pdf_link = edu.get('pdf_url', '')
            link_html = f" - <a href='{pdf_link}'><u>[Voir PDF]</u></a>" if pdf_link else ""
            left_elements.append(Paragraph(f"<b>{edu['degree']}</b>{link_html}", left_text_style))
            left_elements.append(Paragraph(f"{edu['school']} ({edu['dates']})", left_text_style))
            left_elements.append(Spacer(1, 0.1*cm))

        right_elements = [
            Paragraph(cv_data.get('name', 'CHRIST DANY OBIEY'), right_title_style),
            Paragraph(cv_data.get('title', 'Consultant IT & Expert Fullstack'), right_subtitle_style),
            Spacer(1, 0.15*cm),
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#185FA5'), spaceAfter=5),
            Paragraph("RÉSUMÉ PROFESSIONNEL", right_section_style),
            Paragraph(cv_data.get('summary', ''), right_body_style),
            Spacer(1, 0.2*cm),
            Paragraph("PARCOURS PROFESSIONNEL", right_section_style),
            HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=4),
        ]

        for exp in cv_data.get('experiences', [])[:3]:
            right_elements.append(Paragraph(f"<b>{exp['role']}</b> — <font color='#185FA5'><b>{exp['company']}</b></font> ({exp['dates']})", right_bold_style))
            for bullet in exp.get('bullets', [])[:3]:
                right_elements.append(Paragraph(f"• {bullet}", right_body_style))
            right_elements.append(Spacer(1, 0.15*cm))

        if cv_data.get('projects'):
            right_elements.append(Spacer(1, 0.1*cm))
            right_elements.append(Paragraph("PROJETS PHARES", right_section_style))
            HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=4)
            for proj in cv_data.get('projects', [])[:2]:
                right_elements.append(Paragraph(f"<b>{proj['title']}</b> : {proj['desc']}", right_body_style))

        # 32% (5.8cm) / 68% (13.7cm) Layout Table
        layout_table = Table([[left_elements, right_elements]], colWidths=[5.8*cm, 13.7*cm])
        layout_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#0B1F3A')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (0,0), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))

        doc.build([layout_table])

        if not PDFGenerator.verify_1_page_limit(output_path):
            raise ValueError(f"Le CV généré dépasse 1 page : {output_path}")

        return output_path

    @staticmethod
    def generate_cover_letter_pdf(lm_data, output_path):
        """
        Generates a strictly 1-page Cover Letter (LM) PDF with Vous / Moi / Nous structure.
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=1.2 * cm,
            rightMargin=1.2 * cm,
            topMargin=1.2 * cm,
            bottomMargin=1.2 * cm
        )

        styles = getSampleStyleSheet()

        sender_style = ParagraphStyle('Sender', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#0B1F3A'))
        recipient_style = ParagraphStyle('Recipient', fontName='Helvetica', fontSize=9.5, leading=12, textColor=colors.HexColor('#334155'))
        subject_style = ParagraphStyle('Subject', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor('#185FA5'))
        body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#1E293B'))

        sender_text = [
            Paragraph(f"<b>{lm_data.get('name', 'CHRIST DANY OBIEY')}</b>", sender_style),
            Paragraph(f"{lm_data.get('location', 'Brazzaville, Congo')}", styles['Normal']),
            Paragraph(f"📞 {lm_data.get('phone', '+242 06 613 01 18')}", styles['Normal']),
            Paragraph(f"✉️ {lm_data.get('email', 'obieydany@gmail.com')}", styles['Normal']),
        ]

        recipient_text = [
            Paragraph(f"<b>À l'attention du Responsable des Recrutements</b>", recipient_style),
            Paragraph(f"<b>{lm_data.get('company_name', 'L\'Entreprise')}</b>", recipient_style),
            Paragraph(f"{lm_data.get('city', 'Pointe-Noire, Congo')}", recipient_style),
            Paragraph(f"Date : {lm_data.get('date', 'Octobre 2026')}", recipient_style),
        ]

        header_table = Table([[sender_text, recipient_text]], colWidths=[9.3*cm, 9.3*cm])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))

        elements = [
            header_table,
            Spacer(1, 0.4*cm),
            Paragraph(f"<b>OBJET : Candidature au poste de {lm_data.get('job_title', 'Ingénieur / Développeur')}</b>", subject_style),
            Spacer(1, 0.3*cm),
        ]

        body = lm_data.get('letter_body')
        if not body:
            job = lm_data.get('job_title', 'Développeur')
            comp = lm_data.get('company_name', 'votre entreprise')
            keywords_str = ", ".join(lm_data.get('keywords', ['Django', 'Flutter', 'React', 'REST']))
            body = (
                f"VOUS : Votre entreprise {comp} recherche un profil hautement qualifié pour occuper le poste de {job} et dynamiser vos projets technologiques.\n\n"
                f"MOI : Ingenerie logicielle, architecture Cloud et intégration Fintech ({keywords_str}), je maîtrise les écosystèmes modernes pour délivrer des applications performantes et fiables.\n\n"
                f"NOUS : En combinant mon expertise technique et ma vision stratégique, nous accélérerons le déploiement de vos solutions tout en garantissant une qualité irréprochable.\n\n"
                f"Disponible immédiatement, je serais ravi de vous rencontrer lors d'un entretien."
            )

        paragraphs = body.split('\n\n')
        for p in paragraphs:
            if p.strip():
                elements.append(Paragraph(p.strip(), body_style))
                elements.append(Spacer(1, 0.25*cm))

        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.", body_style))
        elements.append(Spacer(1, 0.5*cm))
        elements.append(Paragraph(f"<b>{lm_data.get('name', 'CHRIST DANY OBIEY')}</b>", sender_style))

        doc.build(elements)

        if not PDFGenerator.verify_1_page_limit(output_path):
            raise ValueError(f"La lettre de motivation dépasse 1 page : {output_path}")

        return output_path

    @staticmethod
    def generate_email_txt(email_data, output_path):
        """Generates email TXT file."""
        name = email_data.get('name', 'CHRIST DANY OBIEY')
        job = email_data.get('job_title', 'Poste')
        company = email_data.get('company_name', 'Entreprise')
        phone = email_data.get('phone', '+242 06 613 01 18')

        subject = f"[Objet : Candidature - {job} - {name}]"
        body = (
            f"{subject}\n\n"
            f"Madame, Monsieur,\n\n"
            f"C'est avec un vif intérêt que je vous transmets ma candidature pour le poste de {job} au sein de {company}.\n\n"
            f"Vous trouverez ci-joint mon Curriculum Vitae (CV) ainsi que ma Lettre de Motivation (LM) résumant mes compétences et mes réalisations.\n\n"
            f"Restant à votre entière disposition pour convenir d'un entretien.\n\n"
            f"Cordialement,\n"
            f"{name}\n"
            f"Tél : {phone}"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(body)

        return output_path

    @staticmethod
    def generate_offer_pdf(offer_data, output_path):
        """
        Generates standalone archived PDF of the job offer.
        Allows multi-page documents without 1-page restriction or cover letter header/footer.
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('OfferTitle', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#0B1F3A'))
        meta_style = ParagraphStyle('OfferMeta', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#185FA5'))
        body_style = ParagraphStyle('OfferBody', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor('#1E293B'))

        elements = [
            Paragraph(f"ARCHIVE OFFRE D'EMPLOI : {offer_data.get('job_title', 'Poste')}", title_style),
            Spacer(1, 0.2*cm),
            Paragraph(f"Organisme / Entreprise : {offer_data.get('company_name', 'Entreprise')} | Source : {offer_data.get('site_name', 'Officiel')}", meta_style),
            Spacer(1, 0.3*cm),
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#185FA5'), spaceAfter=10),
        ]

        full_text = offer_data.get('full_text', offer_data.get('letter_body', "Descriptif de l'offre d'emploi."))
        for line in full_text.split('\n'):
            if line.strip():
                elements.append(Paragraph(line.strip(), body_style))
                elements.append(Spacer(1, 0.15*cm))

        doc.build(elements)
        return output_path
