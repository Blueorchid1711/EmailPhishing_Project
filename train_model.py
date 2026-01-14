import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Simple sample dataset (replace later if needed)
texts = [
    "Verify your account immediately click here",
    "Your account has been suspended urgently",
    "Meeting scheduled tomorrow at 10am",
    "Invoice attached for your reference"
]

labels = [1, 1, 0, 0]  # 1 = phishing, 0 = safe

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model trained successfully")
