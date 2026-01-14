import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def predict_phishing(text):
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0][1]
    label = "Phishing" if prob > 0.5 else "Safe"

    reasons = []
    if "urgent" in text.lower():
        reasons.append("Urgency language detected")
    if "verify" in text.lower():
        reasons.append("Credential verification request")
    if "click" in text.lower():
        reasons.append("Suspicious call-to-action")

    return label, round(prob * 100, 2), reasons
