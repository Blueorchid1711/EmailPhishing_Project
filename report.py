from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_report(parsed, label, score, reasons, output_path="forensic_report.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Digital Forensic Email Analysis Report")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Case ID: CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    y -= 20
    c.drawString(40, y, f"Analysis Time: {datetime.now()}")
    y -= 30

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Classification Result")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Label: {label}")
    y -= 15
    c.drawString(40, y, f"Phishing Probability: {score}%")
    y -= 25

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Email Metadata")
    y -= 20

    for k, v in parsed["headers"].items():
        c.drawString(40, y, f"{k}: {v}")
        y -= 14

    y -= 15
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Extracted URLs")
    y -= 20

    if parsed["urls"]:
        for url in parsed["urls"]:
            c.drawString(40, y, url)
            y -= 14
    else:
        c.drawString(40, y, "No URLs found")
        y -= 14

    y -= 15
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Explainable Indicators")
    y -= 20

    if reasons:
        for r in reasons:
            c.drawString(40, y, f"- {r}")
            y -= 14
    else:
        c.drawString(40, y, "No major red flags detected")

    y -= 25
    c.setFont("Helvetica", 9)
    c.drawString(
        40,
        y,
        "Note: This report is auto-generated for cyber forensic and legal analysis purposes."
    )

    c.save()
    return output_path
