"""
PDF and CSV Report Generation
"""
import csv
import json
from io import BytesIO, StringIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def generate_pdf_report(scan_type, input_data, result, risk_score, user=None):
    """Generate PDF report for scan results"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph('PhishLab Security Report', title_style))
    
    # Header Info
    header_style = ParagraphStyle(
        'HeaderInfo',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', header_style))
    if user:
        story.append(Paragraph(f'User: {user.username}', header_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Scan Type Section
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph(f'Analysis Type: {scan_type.upper()}', heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Risk Score
    risk_color = colors.HexColor('#dc3545') if risk_score >= 70 else \
                 colors.HexColor('#ffc107') if risk_score >= 50 else \
                 colors.HexColor('#017d1a')
    
    score_data = [
        ['Risk Score', f'{risk_score}/100'],
        ['Risk Level', get_risk_level(risk_score)]
    ]
    score_table = Table(score_data, colWidths=[2.5*inch, 2.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (1, 0), (1, -1), risk_color),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Input Data
    story.append(Paragraph('Input Data:', heading_style))
    story.append(Paragraph(str(input_data)[:200], styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Results
    story.append(Paragraph('Analysis Results:', heading_style))
    
    # Format results as table
    if isinstance(result, dict):
        results_data = [['Field', 'Value']]
        for key, value in result.items():
            if key not in ['defense_recommendations']:
                key_display = key.replace('_', ' ').title()
                value_display = str(value)[:100]
                results_data.append([key_display, value_display])
        
        if len(results_data) > 1:
            results_table = Table(results_data, colWidths=[2*inch, 3*inch])
            results_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (1, 0), (1, -1), 'CJK')
            ]))
            story.append(results_table)
    
    story.append(Spacer(1, 0.2*inch))
    
    # Defense Recommendations
    if 'defense_recommendations' in result:
        story.append(PageBreak())
        story.append(Paragraph('Defense Recommendations:', heading_style))
        
        recs = result['defense_recommendations']
        if isinstance(recs, dict):
            for category, items in recs.items():
                story.append(Paragraph(f'<b>{category}:</b>', styles['Normal']))
                if isinstance(items, list):
                    for item in items:
                        story.append(Paragraph(f'• {item}', styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        'This report is for educational and awareness purposes only. '
        'PhishLab is a safe, offline simulation environment.',
        footer_style
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_csv_report(scans_list):
    """Generate CSV report from scan history"""
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Scan ID', 'Type', 'Input', 'Risk Score', 'Date', 'Status'])
    
    # Data
    for scan in scans_list:
        writer.writerow([
            scan.id,
            scan.scan_type,
            scan.input_data[:50],
            scan.risk_score,
            scan.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Completed'
        ])
    
    output.seek(0)
    return output


def get_risk_level(score):
    """Get risk level label"""
    if score >= 70:
        return 'CRITICAL'
    elif score >= 50:
        return 'HIGH'
    elif score >= 30:
        return 'MEDIUM'
    elif score > 0:
        return 'LOW'
    else:
        return 'SAFE'
