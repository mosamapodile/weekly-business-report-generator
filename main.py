import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

# Updated Paths & Column Names
DATA_PATH = 'data/salon_sales.csv'
CHART_PATH = 'charts/service_breakdown.png'
REPORT_PATH = 'reports/weekly_summary.pdf'

def create_business_report():
    # 1. Load Data with your 'Amount' structure
    df = pd.read_csv(DATA_PATH)
    
    # Calculate Business Insights
    total_revenue = df['Amount'].sum()
    service_totals = df.groupby('Service')['Amount'].sum().sort_values(ascending=False)
    
    # Identify the "MVP" (Most Valuable Performer)
    top_service = service_totals.idxmax()
    top_revenue = service_totals.max()

    # 2. Create the Visual (A clean bar chart)
    plt.figure(figsize=(7, 5))
    service_totals.plot(kind='bar', color='#4A90E2')
    plt.title('Revenue Contribution by Service', fontsize=14, fontweight='bold')
    plt.ylabel('Total Amount (R)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()

    # 3. Build the PDF
    doc = SimpleDocTemplate(REPORT_PATH, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Brand Style
    brand_style = ParagraphStyle('Brand', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    
    elements = []

    # Human-Friendly Header
    elements.append(Paragraph("Weekly Revenue Insight", styles['Title']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>Executive Summary:</b> Excellent work! This week the salon brought in a total of <b>R{total_revenue:,.2f}</b>.", styles['Normal']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"The standout service was <b>{top_service}</b>, which generated <b>R{top_revenue:,.2f}</b>.", styles['Normal']))
    
    # Add the Chart
    elements.append(Spacer(1, 20))
    elements.append(Image(CHART_PATH, width=400, height=280))
    
    # Professional Data Table
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Detailed Service Breakdown</b>", styles['Heading3']))
    
    table_data = [['Service Type', 'Total Revenue']]
    for service, amt in service_totals.items():
        table_data.append([service, f"R{amt:,.2f}"])

    report_table = Table(table_data, colWidths=[150, 100])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    
    elements.append(report_table)
    
    # Branding Footer
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("Generated via MyPath Business Automation", brand_style))

    doc.build(elements)
    print(f"Success! Report saved to {REPORT_PATH}")

if __name__ == "__main__":
    create_business_report()