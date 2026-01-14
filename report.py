from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf_report(parsed, label, score, reasons, output_path="forensic_report.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 40

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Digital Forensic Email Analysis Report")
    y -= 30

    # Meta
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Case ID: CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    y -= 15
    c.drawString(40, y, f"Analysis Time: {datetime.now()}")
    y -= 25

    # Classification
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Classification Result")
    y -= 18

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Label: {label}")
    y -= 14
    c.drawString(40, y, f"Phishing Probability: {score}%")
    y -= 25

    # Risk category (derived safely here)
    if score >= 80:
        risk_level = "High"
    elif score >= 50:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    c.drawString(40, y, f"Risk Category: {risk_level}")
    y -= 25

    # Headers
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Email Metadata")
    y -= 18

    c.setFont("Helvetica", 10)
    for k, v in parsed["headers"].items():
        c.drawString(40, y, f"{k}: {v}")
        y -= 14

    y -= 15

    # URLs
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Extracted URLs")
    y -= 18

    if parsed["urls"]:
        for url in parsed["urls"]:
            c.drawString(40, y, url)
            y -= 14
    else:
        c.drawString(40, y, "No URLs found")
        y -= 14

    y -= 15

    # Explainability
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Explainable Indicators")
    y -= 18

    c.setFont("Helvetica", 10)
    if reasons:
        for r in reasons:
            c.drawString(40, y, f"- {r}")
            y -= 14
    else:
        c.drawString(40, y, "No major red flags detected")
        y -= 14

    y -= 25

    # Legal note
    c.setFont("Helvetica", 9)
    c.drawString(
        40,
        y,
        "Note: This report is auto-generated for cyber forensic and legal analysis purposes."
    )

    c.save()
    return output_path
