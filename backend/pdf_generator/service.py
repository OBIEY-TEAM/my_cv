import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from pypdf import PdfReader

class PDFService:
    @staticmethod
    def generate_cv_pdf(data, output_path):
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=0.8*cm,
            rightMargin=0.8*cm,
            topMargin=0.8*cm,
            bottomMargin=0.8*cm
        )

        styles = getSampleStyleSheet()
        PRIMARY_COLOR = colors.HexColor('#1E3A8A')
        SECONDARY_COLOR = colors.HexColor('#0284C7')
        TEXT_DARK = colors.HexColor('#1F2937')
        TEXT_MUTED = colors.HexColor('#4B5563')

        title_style = ParagraphStyle(
            'CVTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=18,
            textColor=PRIMARY_COLOR,
            alignment=TA_LEFT
        )

        subtitle_style = ParagraphStyle(
            'CVSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=SECONDARY_COLOR,
            alignment=TA_LEFT
        )

        contact_style = ParagraphStyle(
            'CVContact',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=TEXT_MUTED
        )

        section_heading = ParagraphStyle(
            'CVSectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=PRIMARY_COLOR,
            spaceAfter=3
        )

        body_style = ParagraphStyle(
            'CVBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=TEXT_DARK
        )

        body_bold = ParagraphStyle(
            'CVBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        left_header = [
            Paragraph(f"<b>{data.get('name', 'CHRIST DANY OBIEY').upper()}</b>", title_style),
            Paragraph(data.get('title', 'Consultant IT & Expert Fullstack'), subtitle_style),
            Spacer(1, 0.15*cm),
            Paragraph(f"📍 {data.get('location', 'Brazzaville & Pointe-Noire, Congo')} | 📞 {data.get('phone', '+242 06 613 01 18')} | ✉️ {data.get('email', 'obieydany@gmail.com')}", contact_style),
        ]

        if data.get('photo_path') and os.path.exists(data.get('photo_path')):
            try:
                img = Image(data['photo_path'], width=2.4*cm, height=2.4*cm)
                header_table_data = [[left_header, img]]
            except Exception:
                header_table_data = [[left_header, ""]]
        else:
            header_table_data = [[left_header, ""]]

        header_table = Table(header_table_data, colWidths=[16*cm, 3*cm])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ]))

        col_left = []
        col_right = []

        col_left.append(Paragraph("PROFIL PROFESSIONNEL", section_heading))
        col_left.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=4))
        col_left.append(Paragraph(data.get('summary', ''), body_style))
        col_left.append(Spacer(1, 0.2*cm))

        col_left.append(Paragraph("EXPÉRIENCES PROFESSIONNELLES", section_heading))
        col_left.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=4))
        for exp in data.get('experiences', []):
            col_left.append(Paragraph(f"<b>{exp.get('role')}</b> | {exp.get('company')} ({exp.get('dates')})", body_bold))
            for bullet in exp.get('bullets', []):
                col_left.append(Paragraph(f"• {bullet}", body_style))
            col_left.append(Spacer(1, 0.15*cm))

        col_left.append(Paragraph("PROJETS PHARES", section_heading))
        col_left.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=4))
        for proj in data.get('projects', []):
            col_left.append(Paragraph(f"<b>{proj.get('title')}</b>", body_bold))
            col_left.append(Paragraph(proj.get('desc'), body_style))
            col_left.append(Spacer(1, 0.1*cm))

        col_right.append(Paragraph("COMPÉTENCES CLÉS", section_heading))
        col_right.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=4))
        for category, skills_list in data.get('skills', {}).items():
            col_right.append(Paragraph(f"<b>{category} :</b>", body_bold))
            col_right.append(Paragraph(", ".join(skills_list), body_style))
            col_right.append(Spacer(1, 0.15*cm))

        col_right.append(Paragraph("FORMATIONS & DIPLÔMES", section_heading))
        col_right.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=4))
        for edu in data.get('education', []):
            col_right.append(Paragraph(f"<b>{edu.get('degree')}</b>", body_bold))
            col_right.append(Paragraph(f"{edu.get('school')} ({edu.get('dates')})", body_style))
            col_right.append(Spacer(1, 0.15*cm))

        main_table = Table([[col_left, col_right]], colWidths=[12.2*cm, 6.8*cm])
        main_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('RIGHTPADDING', (0,0), (0,0), 8),
            ('LEFTPADDING', (1,0), (1,0), 8),
        ]))

        elements = [
            header_table,
            Spacer(1, 0.2*cm),
            HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=6),
            main_table
        ]

        doc.build(elements)
        return output_path

    @staticmethod
    def generate_cover_letter_pdf(data, output_path):
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )

        styles = getSampleStyleSheet()
        PRIMARY_COLOR = colors.HexColor('#1E3A8A')
        TEXT_DARK = colors.HexColor('#1F2937')

        sender_style = ParagraphStyle(
            'LMSender',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=PRIMARY_COLOR
        )

        recipient_style = ParagraphStyle(
            'LMRecipient',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=TEXT_DARK,
            alignment=TA_RIGHT
        )

        subject_style = ParagraphStyle(
            'LMSubject',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=PRIMARY_COLOR,
            spaceBefore=10,
            spaceAfter=10
        )

        body_style = ParagraphStyle(
            'LMBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=TEXT_DARK,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        )

        sender_text = [
            Paragraph(f"<b>{data.get('name', 'CHRIST DANY OBIEY')}</b>", sender_style),
            Paragraph(f"📍 {data.get('location', 'Brazzaville & Pointe-Noire, Congo')}", styles['Normal']),
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
