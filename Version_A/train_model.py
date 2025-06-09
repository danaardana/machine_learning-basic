import joblib
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Add parent directory to path for intent_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intent_data import get_training_data

# Load expanded training data
training_data = get_training_data()
training_sentences = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

# Inisialisasi vectorizer & model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)
model = MultinomialNB()
model.fit(X, labels)

# Simpan ke file
joblib.dump(model, "../ml_model/chat_model.pkl")
joblib.dump(vectorizer, "../ml_model/vectorizer.pkl")

print("✅ Model dan vectorizer berhasil disimpan ke folder ml_model")
