import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_application_pdf(submission_data: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        textColor=colors.HexColor('#0B2545')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#555555')
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1D3557')
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1F2937')
    )

    elements = []

    # Government Header
    elements.append(Paragraph("GOVERNMENT CITIZEN SERVICE PORTAL", title_style))
    elements.append(Paragraph("VoiceForm AI — Digital India e-Governance Initiative", subtitle_style))
    elements.append(Paragraph("OFFICIAL APPLICATION ACKNOWLEDGMENT RECEIPT", ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        alignment=1,
        textColor=colors.HexColor('#E76F51')
    )))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0B2545'), spaceAfter=15))

    # Application Metadata Banner
    app_id = submission_data.get("id", "VF-2026-UNKNOWN")
    form_name = submission_data.get("form_name", "Government Service Application")
    sub_date = submission_data.get("submitted_at", datetime.now().strftime("%d-%m-%Y %H:%M:%S UTC"))
    status = submission_data.get("status", "SUBMITTED")

    meta_data = [
        [
            Paragraph("<b>Application Ref No:</b>", bold_label),
            Paragraph(f"<font color='#0B2545'><b>{app_id}</b></font>", bold_label),
            Paragraph("<b>Submission Date:</b>", bold_label),
            Paragraph(str(sub_date)[:19], body_style)
        ],
        [
            Paragraph("<b>Form Applied:</b>", bold_label),
            Paragraph(form_name, body_style),
            Paragraph("<b>Current Status:</b>", bold_label),
            Paragraph(f"<font color='green'><b>{status}</b></font>", bold_label)
        ]
    ]

    meta_table = Table(meta_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2.0*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F6F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 15))

    # Applicant Details
    elements.append(Paragraph("APPLICANT PARTICULARS", section_heading))
    elements.append(Spacer(1, 6))

    form_data = submission_data.get("form_data", {})
    
    rows = []
    # Build readable key-value pairs
    for key, val in form_data.items():
        if val is not None and str(val).strip() != "":
            label_text = key.replace("_", " ").title()
            rows.append([
                Paragraph(f"<b>{label_text}</b>", bold_label),
                Paragraph(str(val), body_style)
            ])

    if not rows:
        rows.append([Paragraph("No form details provided", body_style), Paragraph("", body_style)])

    # Format in pairs if possible or 2-column table
    app_table = Table(rows, colWidths=[2.8*inch, 4.7*inch])
    app_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EBF2FA')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(app_table)
    elements.append(Spacer(1, 15))

    # Next Steps & Declaration
    elements.append(Paragraph("IMPORTANT NOTICE & NEXT STEPS", section_heading))
    elements.append(Spacer(1, 5))
    notice_text = (
        "1. This computer-generated receipt serves as provisional acknowledgment for your application.<br/>"
        "2. Please keep your Application Reference Number safe for online status tracking.<br/>"
        "3. If required, present this acknowledgment along with original documents during physical verification "
        "at your local Tehsil / CSC center.<br/>"
        "4. Status updates will be sent via SMS to your registered mobile number."
    )
    elements.append(Paragraph(notice_text, body_style))
    elements.append(Spacer(1, 20))

    # Footer signature placeholder
    footer_data = [
        [
            Paragraph("<b>Digitally Generated by VoiceForm AI Engine</b><br/>Valid e-Acknowledgment", subtitle_style),
            Paragraph("<b>System Verification Seal</b><br/>Official e-Governance Stamp", subtitle_style)
        ]
    ]
    footer_table = Table(footer_data, colWidths=[4*inch, 3.5*inch])
    footer_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_draft_pdf(form_def: dict, form_data: dict, validation_result: dict = None) -> io.BytesIO:
    """
    Generates a draft PDF preview for applicant review before confirmation.
    Preserves original filled fields and highlights any missing required fields.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DraftTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor('#0B2545')
    )
    subtitle_style = ParagraphStyle(
        'DraftSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#D97706') # Amber
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1D3557')
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12
    )
    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )
    warn_style = ParagraphStyle(
        'WarnStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#991B1B')
    )

    elements = []
    elements.append(Paragraph("VOICEFORM AI - CITIZEN SERVICE GATEWAY", title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(f"<b>DRAFT APPLICATION PREVIEW</b> — {form_def.get('title', 'Application')}", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#D97706'), spaceBefore=2, spaceAfter=12))

    # Missing Required Fields Warning (if any)
    missing_fields = (validation_result or {}).get("missing_fields", [])
    if missing_fields:
        warn_elements = [
            Paragraph("<b>⚠️ ATTENTION: REQUIRED FIELDS PENDING COMPLETION</b>", ParagraphStyle('WH', parent=warn_style, fontName='Helvetica-Bold')),
            Paragraph("The following mandatory fields must be completed before official submission:", warn_style)
        ]
        for mf in missing_fields:
            warn_elements.append(Paragraph(f"• <b>{mf.get('field_label')}</b> ({mf.get('section_title')})", warn_style))

        warn_table = Table([[warn_elements]], colWidths=[7.5*inch])
        warn_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F59E0B')),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(warn_table)
        elements.append(Spacer(1, 12))

    # Form metadata table
    meta_data = [
        [
            Paragraph("<b>Form Name:</b>", bold_label),
            Paragraph(form_def.get('title', ''), body_style),
            Paragraph("<b>Department:</b>", bold_label),
            Paragraph(form_def.get('department', ''), body_style)
        ],
        [
            Paragraph("<b>Preview Date:</b>", bold_label),
            Paragraph(datetime.now().strftime("%d %B %Y, %I:%M %p"), body_style),
            Paragraph("<b>Status:</b>", bold_label),
            Paragraph("<b>UNCONFIRMED DRAFT</b>", ParagraphStyle('D', parent=body_style, textColor=colors.HexColor('#D97706')))
        ]
    ]
    meta_table = Table(meta_data, colWidths=[1.4*inch, 2.3*inch, 1.4*inch, 2.4*inch])
    meta_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 14))

    # Field data table
    elements.append(Paragraph("ENTERED FORM PARTICULARS", section_heading))
    elements.append(Spacer(1, 6))

    rows = []
    for section in form_def.get("sections", []):
        for field in section.get("fields", []):
            val = form_data.get(field["id"])
            has_val = val is not None and str(val).strip() != ""
            req_marker = " *" if field.get("required") else ""
            label_text = f"{field['label']}{req_marker}"

            if has_val:
                val_cell = Paragraph(str(val), body_style)
            else:
                val_cell = Paragraph("<font color='#DC2626'><i>[Not Provided]</i></font>", body_style)

            rows.append([
                Paragraph(f"<b>{label_text}</b>", bold_label),
                val_cell
            ])

    if not rows:
        rows.append([Paragraph("No details entered", body_style), Paragraph("", body_style)])

    fields_table = Table(rows, colWidths=[3.0*inch, 4.5*inch])
    fields_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(fields_table)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph(
        "<i>Note: This draft preview is for verification purposes only. Return to the application to edit or submit.</i>",
        ParagraphStyle('N', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#64748B'), alignment=1)
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer

