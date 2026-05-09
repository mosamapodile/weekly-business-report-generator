import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

# Paths
DATA_PATH = 'data/salon_sales.csv'
CHART_PATH = 'charts/revenue_chart.png'
REPORT_PATH = 'reports/weekly_report.pdf'

def generate_report():
    if not os.path.exists(DATA_PATH):
        print("CSV not found.")
        return

    # 1. Data Analysis
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Aggregates
    total_rev = df['Revenue'].sum()
    service_breakdown = df.groupby('Service')['Revenue'].sum().reset_index()
    
    # 2. Visualization (Pie Chart for Service Mix)
    plt.figure(figsize=(6, 4))
    plt.pie(service_breakdown['Revenue'], labels=service_breakdown['Service'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title('Revenue by Service Type')
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()

    # 3. Build PDF with Platypus
    doc = SimpleDocTemplate(REPORT_PATH, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title & Intro
    elements.append(Paragraph("Weekly Salon Performance Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total Revenue for Period: R{total_rev:,.2f}", styles['Heading2']))
    elements.append(Spacer(1, 20))

    # Add Chart
    elements.append(Paragraph("Service Revenue Distribution", styles['Heading3']))
    img = Image(CHART_PATH, width=400, height=250)
    elements.append(img)
    elements.append(Spacer(1, 20))

    # Add Data Table
    elements.append(Paragraph("Detailed Breakdown", styles['Heading3']))
    
    # Prepare Table Data
    table_data = [['Service', 'Revenue (R)']]
    for _, row in service_breakdown.iterrows():
        table_data.append([row['Service'], f"R{row['Revenue']:.2f}"])
    
    t = Table(table_data, colWidths=[200, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)

    # Build PDF
    doc.build(elements)
    print(f"Report ready: {REPORT_PATH}")

if __name__ == "__main__":
    generate_report()