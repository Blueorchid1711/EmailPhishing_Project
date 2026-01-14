from datetime import datetime

def generate_report(parsed, label, score, reasons):
    report = f"""
DIGITAL FORENSIC EMAIL REPORT
============================

Case ID: CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}
Analysis Time: {datetime.now()}

Classification: {label}
Phishing Probability: {score}%

--- HEADERS ---
From: {parsed['headers']['From']}
To: {parsed['headers']['To']}
Subject: {parsed['headers']['Subject']}
Date: {parsed['headers']['Date']}

--- URLS ---
{parsed['urls']}

--- EVIDENCE ---
SHA-256 Hash: {parsed['hash']}

--- EXPLANATION ---
{', '.join(reasons) if reasons else 'No major red flags detected'}

This report is auto-generated for cyber-forensic investigation.
"""
    return report
