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
    def generate_cv_docx(data, output_path):
        """Generates an editable Word (.docx) version of the CV."""
        from docx import Document
        from docx.shared import Pt, RGBColor, Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH

        doc = Document()
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            section.left_margin = Inches(0.6)
            section.right_margin = Inches(0.6)

        # Header Name & Title
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_after = Pt(2)
        run_name = title_p.add_run(data.get('name', 'CHRIST DANY OBIEY') + '\n')
        run_name.bold = True
        run_name.font.size = Pt(18)
        run_name.font.color.rgb = RGBColor(11, 31, 58)

        run_sub = title_p.add_run(data.get('title', 'Consultant IT & Expert Fullstack'))
        run_sub.bold = True
        run_sub.font.size = Pt(11)
        run_sub.font.color.rgb = RGBColor(24, 95, 165)

        # Contact Info Line
        contact_p = doc.add_paragraph()
        contact_p.paragraph_format.space_after = Pt(10)
        contact_info = f"📍 {data.get('location', 'Brazzaville, Congo')}  |  📞 {data.get('phone', '+242 06 613 01 18')}  |  ✉️ {data.get('email', 'obieydany@gmail.com')}"
        run_contact = contact_p.add_run(contact_info)
        run_contact.font.size = Pt(9)
        run_contact.font.color.rgb = RGBColor(51, 65, 85)

        # Summary Section
        sum_head = doc.add_paragraph()
        sum_head.paragraph_format.space_after = Pt(2)
        r_sum_head = sum_head.add_run("RÉSUMÉ PROFESSIONNEL")
        r_sum_head.bold = True
        r_sum_head.font.size = Pt(12)
        r_sum_head.font.color.rgb = RGBColor(11, 31, 58)

        sum_body = doc.add_paragraph()
        sum_body.paragraph_format.space_after = Pt(10)
        r_sum_body = sum_body.add_run(data.get('summary', ''))
        r_sum_body.font.size = Pt(9.5)
        r_sum_body.font.color.rgb = RGBColor(51, 65, 85)

        # Experiences Section
        exp_head = doc.add_paragraph()
        exp_head.paragraph_format.space_after = Pt(2)
        r_exp_head = exp_head.add_run("PARCOURS PROFESSIONNEL")
        r_exp_head.bold = True
        r_exp_head.font.size = Pt(12)
        r_exp_head.font.color.rgb = RGBColor(11, 31, 58)

        for exp in data.get('experiences', []):
            p_exp = doc.add_paragraph()
            p_exp.paragraph_format.space_after = Pt(2)
            r_role = p_exp.add_run(f"{exp.get('role')} — ")
            r_role.bold = True
            r_role.font.size = Pt(10)
            r_comp = p_exp.add_run(f"{exp.get('company')} ")
            r_comp.bold = True
            r_comp.font.color.rgb = RGBColor(24, 95, 165)
            r_dates = p_exp.add_run(f"({exp.get('dates')})")
            r_dates.font.size = Pt(9)

            for bullet in exp.get('bullets', []):
                p_b = doc.add_paragraph(style='List Bullet')
                p_b.paragraph_format.space_after = Pt(2)
                r_b = p_b.add_run(bullet)
                r_b.font.size = Pt(9)

        # Skills
        skills_head = doc.add_paragraph()
        skills_head.paragraph_format.space_before = Pt(8)
        skills_head.paragraph_format.space_after = Pt(2)
        r_sk = skills_head.add_run("COMPÉTENCES CLÉS")
        r_sk.bold = True
        r_sk.font.size = Pt(12)
        r_sk.font.color.rgb = RGBColor(11, 31, 58)

        skills_dict = data.get('skills', {})
        for cat, items in skills_dict.items():
            p_sk = doc.add_paragraph()
            p_sk.paragraph_format.space_after = Pt(2)
            r_cat = p_sk.add_run(f"{cat}: ")
            r_cat.bold = True
            r_cat.font.size = Pt(9)
            r_items = p_sk.add_run(", ".join(items))
            r_items.font.size = Pt(9)

        # Education / Certifications
        edu_head = doc.add_paragraph()
        edu_head.paragraph_format.space_before = Pt(8)
        edu_head.paragraph_format.space_after = Pt(2)
        r_ed = edu_head.add_run("FORMATIONS & CERTIFICATIONS")
        r_ed.bold = True
        r_ed.font.size = Pt(12)
        r_ed.font.color.rgb = RGBColor(11, 31, 58)

        for edu in data.get('education', []):
            p_ed = doc.add_paragraph()
            p_ed.paragraph_format.space_after = Pt(2)
            r_deg = p_ed.add_run(f"{edu.get('degree')} - {edu.get('school')} ({edu.get('dates')})")
            r_deg.font.size = Pt(9)

        doc.save(output_path)
        return output_path

    @staticmethod
    def generate_cover_letter_docx(data, output_path):
        """Generates an editable Word (.docx) version of the Cover Letter."""
        from docx import Document
        from docx.shared import Pt, RGBColor, Inches

        doc = Document()
        for section in doc.sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(0.8)
            section.right_margin = Inches(0.8)

        # Header - Sender Info
        sender_p = doc.add_paragraph()
        sender_p.paragraph_format.space_after = Pt(12)
        r_name = sender_p.add_run(data.get('name', 'CHRIST DANY OBIEY') + '\n')
        r_name.bold = True
        r_name.font.size = Pt(11)
        r_name.font.color.rgb = RGBColor(11, 31, 58)

        r_details = sender_p.add_run(
            f"{data.get('location', 'Brazzaville, Congo')}\n"
            f"📞 {data.get('phone', '+242 06 613 01 18')}\n"
            f"✉️ {data.get('email', 'obieydany@gmail.com')}"
        )
        r_details.font.size = Pt(9.5)

        # Recipient Info
        rec_p = doc.add_paragraph()
        rec_p.paragraph_format.space_after = Pt(16)
        r_rec = rec_p.add_run(
            f"À l'attention du Recruteur\n"
            f"{data.get('company_name', 'L\'Entreprise')}\n"
            f"{data.get('city', 'Pointe-Noire, Congo')}\n"
            f"Date : {data.get('date', 'Octobre 2026')}"
        )
        r_rec.font.size = Pt(10)
        r_rec.bold = True

        # Subject
        sub_p = doc.add_paragraph()
        sub_p.paragraph_format.space_after = Pt(14)
        r_sub = sub_p.add_run(f"OBJET : Candidature au poste de {data.get('job_title', 'Ingénieur / Développeur')}")
        r_sub.bold = True
        r_sub.font.size = Pt(11)
        r_sub.font.color.rgb = RGBColor(24, 95, 165)

        # Body
        paragraphs = data.get('letter_body', '').split('\n\n')
        for p in paragraphs:
            if p.strip():
                bp = doc.add_paragraph()
                bp.paragraph_format.space_after = Pt(10)
                r_body = bp.add_run(p.strip())
                r_body.font.size = Pt(10)

        # Closing
        close_p = doc.add_paragraph()
        close_p.paragraph_format.space_before = Pt(10)
        close_p.paragraph_format.space_after = Pt(16)
        r_close = close_p.add_run("Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.")
        r_close.font.size = Pt(10)

        sig_p = doc.add_paragraph()
        r_sig = sig_p.add_run(data.get('name', 'CHRIST DANY OBIEY'))
        r_sig.bold = True
        r_sig.font.size = Pt(11)

        doc.save(output_path)
        return output_path

    @staticmethod
    def verify_1_page_limit(pdf_path):
        reader = PdfReader(pdf_path)
        return len(reader.pages) == 1
