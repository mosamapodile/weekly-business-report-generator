import os
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def ensure_directories():
    """Self-healing: Creates the folder structure for the pipeline."""
    for folder in ['reports', 'charts', 'data', 'configs']:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Created directory: {folder}")

def get_report_styles():
    styles = getSampleStyleSheet()
    
    # 1. Main Agency Header
    if 'BrandHeader' not in styles:
        styles.add(ParagraphStyle(
            name='BrandHeader',
            fontSize=22,
            textColor=colors.black,
            fontName='Helvetica-Bold',
            spaceAfter=5
        ))
    
    # 2. Section Headings (Strategic Insights)
    # Keeping this compact to ensure the one-page limit
    if 'Heading3' not in styles:
        styles.add(ParagraphStyle(
            name='Heading3',
            parent=styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceBefore=10,
            spaceAfter=8,
            underlineWidth=1
        ))

    # 3. Professional Subtle Footer
    if 'Footer' not in styles:
        styles.add(ParagraphStyle(
            name='Footer',
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceBefore=20
        ))

    # 4. Normal Body Text (Slightly smaller for more space)
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 12 # Line spacing

    return styles
