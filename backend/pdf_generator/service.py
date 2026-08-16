import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from pypdf import PdfReader

class PDFService:
    @staticmethod
    def generate_cv_pdf(data, output_path):
        """
        Generates a modern 2-column strictly 1-page CV PDF using ReportLab.
        Columns:
        - Left Sidebar (navy blue background): Contact, Skills, Education / Certifications (with clickable PDF links), Projects
        - Right Content: Header, Summary, Professional Experiences
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=0.5 * cm,
            rightMargin=0.5 * cm,
            topMargin=0.5 * cm,
            bottomMargin=0.5 * cm
        )

        styles = getSampleStyleSheet()

        # Styles definition
        left_header_style = ParagraphStyle(
            'LeftHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=colors.HexColor('#FFFFFF'),
            spaceAfter=4
        )

        left_text_style = ParagraphStyle(
            'LeftText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#E2E8F0')
        )

        left_link_style = ParagraphStyle(
            'LeftLink',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=7,
            leading=9,
            textColor=colors.HexColor('#93C5FD')
        )

        right_title_style = ParagraphStyle(
            'RightTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=20,
            textColor=colors.HexColor('#0B1F3A')
        )

        right_subtitle_style = ParagraphStyle(
            'RightSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=13,
            textColor=colors.HexColor('#185FA5')
        )

        right_section_style = ParagraphStyle(
            'RightSection',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=14,
            textColor=colors.HexColor('#0B1F3A'),
            spaceAfter=4
        )

        right_body_style = ParagraphStyle(
            'RightBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor('#334155')
        )

        right_bold_style = ParagraphStyle(
            'RightBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor('#0B1F3A')
        )

        # 1. Left Sidebar Content
        left_elements = []

        if data.get('photo_path') and os.path.exists(data['photo_path']):
            try:
                img = Image(data['photo_path'], width=3.8*cm, height=3.8*cm)
                left_elements.append(img)
                left_elements.append(Spacer(1, 0.3*cm))
            except Exception:
                pass

        left_elements.append(Paragraph("CONTACT", left_header_style))
        left_elements.append(Paragraph(f"📍 {data.get('location', 'Brazzaville, Congo')}", left_text_style))
        left_elements.append(Paragraph(f"📞 {data.get('phone', '+242 06 613 01 18')}", left_text_style))
        left_elements.append(Paragraph(f"✉️ {data.get('email', 'obieydany@gmail.com')}", left_text_style))
        left_elements.append(Spacer(1, 0.4*cm))

        left_elements.append(Paragraph("COMPÉTENCES CLÉS", left_header_style))
        skills_dict = data.get('skills', {})
        for cat, items in skills_dict.items():
            left_elements.append(Paragraph(f"<b>{cat}:</b>", left_text_style))
            left_elements.append(Paragraph(", ".join(items), left_text_style))
            left_elements.append(Spacer(1, 0.15*cm))
        left_elements.append(Spacer(1, 0.2*cm))

        left_elements.append(Paragraph("FORMATIONS & CERTIFS", left_header_style))
        for edu in data.get('education', []):
            pdf_link = edu.get('pdf_url', '')
            link_html = f" - <a href='{pdf_link}'><u>[Voir PDF]</u></a>" if pdf_link else ""
            left_elements.append(Paragraph(f"<b>{edu['degree']}</b>{link_html}", left_text_style))
            left_elements.append(Paragraph(f"{edu['school']} ({edu['dates']})", left_text_style))
            left_elements.append(Spacer(1, 0.15*cm))
        left_elements.append(Spacer(1, 0.2*cm))

        if data.get('projects'):
            left_elements.append(Paragraph("PROJETS MAJEURS", left_header_style))
            for proj in data.get('projects', []):
                left_elements.append(Paragraph(f"<b>{proj['title']}</b>", left_text_style))
                left_elements.append(Paragraph(proj['desc'], left_text_style))
                left_elements.append(Spacer(1, 0.15*cm))

        # 2. Right Column Content
        right_elements = [
            Paragraph(data.get('name', 'CHRIST DANY OBIEY'), right_title_style),
            Paragraph(data.get('title', 'Consultant IT & Expert Fullstack'), right_subtitle_style),
            Spacer(1, 0.25*cm),
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#185FA5'), spaceAfter=8),
            Paragraph("RÉSUMÉ PROFESSIONNEL", right_section_style),
            Paragraph(data.get('summary', ''), right_body_style),
            Spacer(1, 0.3*cm),
            Paragraph("PARCOURS PROFESSIONNEL", right_section_style),
            HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6),
        ]

        for exp in data.get('experiences', []):
            right_elements.append(Paragraph(f"<b>{exp['role']}</b> — <font color='#185FA5'><b>{exp['company']}</b></font> ({exp['dates']})", right_bold_style))
            for bullet in exp.get('bullets', []):
                right_elements.append(Paragraph(f"• {bullet}", right_body_style))
            right_elements.append(Spacer(1, 0.2*cm))

        # Combine into 2-column Layout Table
        layout_table = Table([[left_elements, right_elements]], colWidths=[5.5*cm, 14.0*cm])
        layout_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#0B1F3A')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (0,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))

        doc.build([layout_table])
        return output_path

    @staticmethod
    def generate_cover_letter_pdf(data, output_path):
        """Generates a strictly 1-page targeted cover letter PDF."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm
        )

        styles = getSampleStyleSheet()

        sender_style = ParagraphStyle('Sender', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#0B1F3A'))
        recipient_style = ParagraphStyle('Recipient', fontName='Helvetica', fontSize=10, leading=13, textColor=colors.HexColor('#334155'))
        subject_style = ParagraphStyle('Subject', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.HexColor('#185FA5'))
        body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#1E293B'))

        sender_text = [
            Paragraph(f"<b>{data.get('name', 'CHRIST DANY OBIEY')}</b>", sender_style),
            Paragraph(f"{data.get('location', 'Brazzaville, Congo')}", styles['Normal']),
            Paragraph(f"📞 {data.get('phone', '+242 06 613 01 18')}", styles['Normal']),
            Paragraph(f"✉️ {data.get('email', 'obieydany@gmail.com')}", styles['Normal']),
        ]

        recipient_text = [
            Paragraph(f"<b>À l'attention du Recruteur</b>", recipient_style),
            Paragraph(f"<b>{data.get('company_name', 'L\'Entreprise')}</b>", recipient_style),
            Paragraph(f"{data.get('city', 'Pointe-Noire, Congo')}", recipient_style),
            Paragraph(f"Date : {data.get('date', 'Octobre 2026')}", recipient_style),
        ]

        header_table = Table([[sender_text, recipient_text]], colWidths=[9*cm, 9*cm])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))

        elements = [
            header_table,
            Spacer(1, 0.5*cm),
            Paragraph(f"<b>OBJET : Candidature au poste de {data.get('job_title', 'Ingénieur / Développeur')}</b>", subject_style),
            Spacer(1, 0.2*cm),
        ]

        paragraphs = data.get('letter_body', '').split('\n\n')
        for p in paragraphs:
            if p.strip():
                elements.append(Paragraph(p.strip(), body_style))

        elements.append(Spacer(1, 0.4*cm))
        elements.append(Paragraph("Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.", body_style))
        elements.append(Spacer(1, 0.6*cm))
        elements.append(Paragraph(f"<b>{data.get('name', 'CHRIST DANY OBIEY')}</b>", sender_style))

        doc.build(elements)
        return output_path

    @staticmethod
    def verify_1_page_limit(pdf_path):
        reader = PdfReader(pdf_path)
        return len(reader.pages) == 1
