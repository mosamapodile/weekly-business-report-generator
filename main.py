import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from utils import get_report_styles, ensure_directories

def run_business_pipeline(client_id):
    # --- 1. DATA EXTRACTION & ANALYTICS ---
    with open(f'configs/{client_id}.json', 'r') as f:
        config = json.load(f)
    
    df = pd.read_csv(f'data/{client_id}_sales.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    start_date = df['Date'].min().strftime('%d %b')
    end_date = df['Date'].max().strftime('%d %b %Y')
    
    total_revenue = df['Amount'].sum()
    avg_ticket = df['Amount'].mean()
    total_sales = len(df)
    
    daily_sales = df.groupby(df['Date'].dt.day_name())['Amount'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).fillna(0)
    
    worst_day = daily_sales[daily_sales > 0].idxmin() if not daily_sales[daily_sales > 0].empty else "N/A"
    service_summary = df.groupby('Service')['Amount'].sum().sort_values(ascending=False)
    top_service = service_summary.index[0]
    
    # --- 2. CHART GENERATION ---
    plt.figure(figsize=(6, 3)) 
    service_summary.plot(kind='barh', color=config.get('report_color', '#333333'))
    plt.title(f"Revenue Analysis", fontsize=10)
    plt.tight_layout()
    
    chart_path = f"charts/{client_id}_breakdown.png"
    plt.savefig(chart_path)
    plt.close()

    # --- 3. PDF BUILDING (The "Centered & Spacious" Layout) ---
    pdf_path = f"reports/{client_id}_weekly_report.pdf"
    
    # Using generous 50pt margins for that "gentle" feel
    doc = SimpleDocTemplate(
        pdf_path, 
        pagesize=letter, 
        leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50
    )
    styles = get_report_styles()
    
    # Create a specific Centered Style for the Header
    centered_header = styles['BrandHeader']
    centered_header.alignment = TA_CENTER
    
    centered_normal = styles['Normal']
    centered_normal.alignment = TA_CENTER

    elements = []

    # --- HEADER SECTION ---
    elements.append(Paragraph(f"LocalFlow Agency: {config['business_name']}", centered_header))
    
    # This is the "Human Spacing" gap you requested
    elements.append(Spacer(1, 15)) 
    
    elements.append(Paragraph(f"<b>Reporting Window:</b> {start_date} - {end_date}", centered_normal))
    
    # Space before the Stats Box
    elements.append(Spacer(1, 30))

    # --- STATS BOX (Centered) ---
    stats_data = [[
        Paragraph(f"<b>Revenue</b><br/>R{total_revenue:,.2f}", centered_normal),
        Paragraph(f"<b>Avg Spend</b><br/>R{avg_ticket:.2f}", centered_normal),
        Paragraph(f"<b>Customers</b><br/>{total_sales}", centered_normal)
    ]]
    stats_table = Table(stats_data, colWidths=[150, 150, 150])
    stats_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
        ('BOX', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    elements.append(stats_table)
    
    elements.append(Spacer(1, 35))

    # --- INSIGHTS SECTION ---
    elements.append(Paragraph("Strategic Business Insights", styles['Heading3']))
    elements.append(Spacer(1, 10))
    insights = [
        f"• <b>The {worst_day} Gap:</b> Your slowest day was {worst_day}. Action: Run a {worst_day} promo to cover overhead.",
        f"• <b>Focus Service:</b> {top_service} is your star earner. Action: Create a loyalty program for this service.",
        f"• <b>Upsell Potential:</b> An R20 add-on per sale would have earned you <b>R{total_sales * 20:,.2f}</b> extra."
    ]
    for line in insights:
        elements.append(Paragraph(line, styles['Normal']))
        elements.append(Spacer(1, 6))

    # --- VISUALIZATION (Centered) ---
    elements.append(Spacer(1, 25))
    img = Image(chart_path, width=420, height=200)
    img.hAlign = 'CENTER'
    elements.append(img)

    # --- FOOTER ---
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("<hr/>", styles['Normal']))
    elements.append(Paragraph("<b>LocalFlow Agency</b> • <i>Optimizing Local Business Intelligence</i>", styles['Footer']))

    doc.build(elements)
    print(f"✅ Gentle One-Pager Complete: {config['business_name']}")

if __name__ == "__main__":
    ensure_directories()
    active_clients = ['salon', 'kota_shop']
    
    print("🚀 LocalFlow Agency: Pipeline Running...")
    for client in active_clients:
        try:
            run_business_pipeline(client)
        except Exception as e:
            print(f"❌ Error with {client}: {e}")
    print("-" * 50)
    print("🏁 SUCCESS: Masterfully spaced reports are ready in '/reports'.")