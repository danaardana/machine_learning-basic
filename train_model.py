import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from intent_data import training_sentences, labels

# Inisialisasi vectorizer & model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)
model = MultinomialNB()
model.fit(X, labels)

# Simpan ke file
joblib.dump(model, "chat_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model dan vectorizer berhasil disimpan ke folder ml_model/")
