import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Email Forensics Dashboard",
    layout="wide"
)

# ----------------------------
# TITLE
# ----------------------------
st.title("📧 Email Forensics & Phishing Evidence Dashboard")
st.caption("Explainable AI-based analysis for cyber forensics and legal investigation")

st.divider()

# ----------------------------
# TOP METRICS
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Emails", 120)
col2.metric("Phishing Detected", 34, delta="+3")
col3.metric("Safe Emails", 86)
col4.metric("High Risk Alerts", 12, delta="+2", delta_color="inverse")

st.divider()

# ----------------------------
# CHARTS ROW
# ----------------------------
left, right = st.columns(2)

with left:
    st.subheader("📊 Email Classification Status")
    status_df = pd.DataFrame({
        "Category": ["Safe", "Phishing"],
        "Count": [86, 34]
    })
    fig = px.bar(status_df, x="Category", y="Count", color="Category")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("⚠️ Risk Level Distribution")
    risk_df = pd.DataFrame({
        "Risk": ["Low", "Medium", "High"],
        "Count": [60, 48, 12]
    })
    fig2 = px.pie(risk_df, names="Risk", values="Count", hole=0.5)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ----------------------------
# FORENSIC ALERTS
# ----------------------------
st.subheader("🚨 Forensic Alerts")

a1, a2, a3 = st.columns(3)
a1.success("✔ No warranty or system alerts")
a2.warning("⚠ 5 suspicious domains detected")
a3.error("❌ 2 emails failed authentication checks")

st.divider()

# ----------------------------
# EVIDENCE TABLE
# ----------------------------
st.subheader("🧾 Email Evidence Tracker")

data = {
    "Sender": ["security@paypaI.com", "admin@bank-alerts.com", "hr@company.com"],
    "Subject": ["Verify Account", "Urgent Action Required", "Meeting Reminder"],
    "Risk Score (%)": [92, 88, 12],
    "Status": ["Phishing", "Phishing", "Safe"],
    "Links Found": [2, 1, 0]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

st.divider()

# ----------------------------
# EXPLAINABLE AI PANEL
# ----------------------------
st.subheader("🧠 Explainable AI – Why was this email flagged?")

with st.expander("View Explanation for High-Risk Email"):
    st.markdown("""
    **Reasons Identified:**
    - Suspicious sender domain mismatch
    - Urgency-based language detected
    - Embedded URL redirects to unknown domain
    - Authentication (SPF/DKIM) missing

    **Forensic Note:**  
    These indicators collectively increase the phishing probability and are
    relevant for cybercrime investigation and legal evidence.
    """)

st.divider()

# ----------------------------
# REPORT DOWNLOAD (PLACEHOLDER)
# ----------------------------
st.subheader("📄 Forensic Report")

st.download_button(
    label="Download Sample Forensic Report",
    data="This is a placeholder forensic report.",
    file_name="forensic_report.txt"
)

from parser import parse_email
from classifier import predict_phishing
from report import generate_pdf_report
import os

st.divider()
st.header("🔎 Analyze a New Email")

email_input = st.text_area(
    "Paste the full email content below for forensic analysis",
    height=220
)

if st.button("Analyze Email"):
    if email_input.strip() == "":
        st.warning("Please paste an email to analyze.")
    else:
        parsed = parse_email(email_input)
        label, score, reasons = predict_phishing(parsed["body"])

        st.subheader("📌 Analysis Result")
        st.metric("Classification", label)
        st.metric("Phishing Probability (%)", score)

        st.subheader("🧠 Explainable Indicators")
        if reasons:
            for r in reasons:
                st.write("•", r)
        else:
            st.write("No major red flags detected")

        st.subheader("🔗 Extracted Links")
        if parsed["urls"]:
            for url in parsed["urls"]:
                st.write(url)
        else:
            st.write("No links found")

        st.subheader("🧾 Email Metadata")
        st.json(parsed["headers"])

        # Generate PDF
        pdf_path = generate_pdf_report(parsed, label, score, reasons)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Forensic PDF Report",
                data=f,
                file_name="email_forensic_report.pdf",
                mime="application/pdf"
            )
