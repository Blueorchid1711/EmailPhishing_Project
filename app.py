import streamlit as st
import pandas as pd
import plotly.express as px
from parser import parse_email
from classifier import predict_phishing
from report import generate_pdf_report

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Email Forensics Dashboard", layout="wide")

# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}
h1, h2, h3 {
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: -0.5px;
}
div[data-testid="metric-container"] {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    border: 1px solid #e0e0e0;
}
.section-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e6e6e6;
    margin-bottom: 20px;
}
.stButton > button {
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
left, right = st.columns([4, 1])
with left:
    st.markdown("## 📧 Email Forensics & Phishing Evidence Dashboard")
    st.caption("AI-powered email investigation for cyber law & digital forensics")
with right:
    st.write("")  # spacing
    st.write("")

st.divider()

# ----------------------------
# STATIC DASHBOARD (DEMO VIEW)
# ----------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Emails", 120)
c2.metric("Phishing Detected", 34, delta="+3")
c3.metric("Safe Emails", 86)
c4.metric("High Risk Alerts", 12, delta="+2", delta_color="inverse")

left, right = st.columns(2)

with left:
    status_df = pd.DataFrame({
        "Category": ["Safe", "Phishing"],
        "Count": [86, 34]
    })
    fig = px.bar(status_df, x="Category", y="Count", color="Category")
    st.plotly_chart(fig, width="stretch")

with right:
    risk_df = pd.DataFrame({
        "Risk": ["Low", "Medium", "High"],
        "Count": [60, 48, 12]
    })
    fig2 = px.pie(risk_df, names="Risk", values="Count", hole=0.5)
    st.plotly_chart(fig2, width="stretch")

st.divider()

# ----------------------------
# LIVE EMAIL ANALYSIS
# ----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🔎 Analyze an Email (Live Forensic Analysis)")

email_input = st.text_area(
    "Paste the complete email content below",
    height=180,
    placeholder="From: ...\nTo: ...\nSubject: ...\n\nEmail body here"
)

if st.button("Analyze Email"):
    if email_input.strip() == "":
        st.warning("Please paste an email to analyze.")
    else:
        parsed = parse_email(email_input)
        label, score, reasons = predict_phishing(parsed["body"])

        # Risk level
        if score >= 80:
            risk_level = "High"
        elif score >= 50:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        domains = list(set([
            url.split("/")[2] for url in parsed["urls"] if "://" in url
        ]))

        st.subheader("📌 Analysis Result")
        r1, r2, r3 = st.columns(3)
        r1.metric("Classification", label)
        r2.metric("Phishing Probability (%)", score)
        r3.metric("Risk Level", risk_level)

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

        pdf_path = generate_pdf_report(parsed, label, score, reasons)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download Forensic PDF Report",
                f,
                file_name="email_forensic_report.pdf",
                mime="application/pdf"
            )

st.markdown('</div>', unsafe_allow_html=True)
