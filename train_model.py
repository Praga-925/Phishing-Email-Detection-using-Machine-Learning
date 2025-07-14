import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
df = pd.read_csv("emails.csv")

# Use appropriate columns
X = df["Email Text"].fillna("")
y = df["Email Type"].map({"Phishing Email": 1, "Safe Email": 0})  # Convert to 0 and s1

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# XGBoost model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)
print("✅ Model Accuracy:", accuracy_score(y_test, pred))

# Save model and vectorizer
pickle.dump(model, open("phishing_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
