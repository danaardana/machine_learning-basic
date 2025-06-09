import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import sys
import os

# Add parent directory to path to import intent_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intent_data import get_training_data
import re

print("Starting Version B training with sub-intent detection...")

# Load training data
training_data = get_training_data()
training_sentences = [item[0] for item in training_data]
main_labels = [item[1] for item in training_data]

print(f"Loaded {len(training_sentences)} training sentences")

# Define sub-intent patterns for each main intent
sub_intent_patterns = {
    "harga": {
        "harga_produk": [
            r"\b(harga|berapa|brp|biaya)\s*(produk|barang|item)",
            r"\b(mounting|body|lampu|led|carbon|projector)\s*(berapa|harga)",
            r"\bharga\s*(mounting|body|lampu|led|carbon|projector)",
            r"\b(price|cost)\s*(list|produk)"
        ],
        "harga_promo": [
            r"\b(promo|diskon|discount|sale|flash|murah)",
            r"\b(ada\s*promo|promo\s*apa|promo\s*gak|diskon\s*berapa)",
            r"\b(potongan|cashback|voucher|kupon)",
            r"\b(special|bundling|paket)\s*(price|harga|promo)"
        ],
        "harga_grosir": [
            r"\b(grosir|wholesale|reseller|dealer|distributor)",
            r"\b(beli\s*banyak|pembelian\s*banyak|bulk|quantity)",
            r"\b(harga\s*khusus|member\s*price|partner\s*price)",
            r"\b(minimum\s*order|MOQ|quantity\s*discount)"
        ],
        "harga_ongkir": [
            r"\b(ongkir|ongkos|kirim|antar|delivery|shipping)",
            r"\b(biaya\s*kirim|cost\s*delivery|tarif\s*pengiriman)",
            r"\b(cod|same\s*day|express|overnight)",
            r"\b(grab|gojek|jne|j&t|sicepat)"
        ],
        "harga_instalasi": [
            r"\b(pasang|install|pemasangan|jasa|service)",
            r"\b(biaya\s*pasang|tarif\s*install|ongkos\s*teknisi)",
            r"\b(home\s*service|mobile\s*service|panggil\s*teknisi)",
            r"\b(weekend|sabtu|minggu)\s*(charge|biaya|tambahan)"
        ]
    },
    "stok_produk": {
        "stok_tersedia": [
            r"\b(ada|ready|tersedia|stock|stok)\s*(gak|tidak|nggak)?",
            r"\b(masih\s*ada|still\s*available|in\s*stock)",
            r"\b(availability|ketersediaan)",
            r"\b(bisa\s*pesan|bisa\s*beli|dapat\s*dibeli)"
        ],
        "stok_habis": [
            r"\b(habis|kosong|sold\s*out|out\s*of\s*stock)",
            r"\b(tidak\s*ada|nggak\s*ada|gak\s*ada)",
            r"\b(empty|discontinued|dihentikan)",
            r"\b(kapan\s*restock|when\s*restock|restock\s*kapan)"
        ],
        "stok_booking": [
            r"\b(booking|book|pesan|order|indent)",
            r"\b(waiting\s*list|pre\s*order|reservation)",
            r"\b(notification|notify|kabari|info)",
            r"\b(arrival|datang|masuk)\s*(baru|new)"
        ]
    },
    "kategori_lighting": {
        "lampu_led": [
            r"\b(led|LED|light\s*emitting)",
            r"\b(hemat\s*listrik|energy\s*saving|low\s*power)",
            r"\b(terang|bright|lumens|watt)",
            r"\b(strip|bar|bulb|headlamp)"
        ],
        "lampu_projector": [
            r"\b(projector|projektor|hid|xenon)",
            r"\b(angel\s*eyes|devil\s*eyes)",
            r"\b(sorot|focus|beam|spotlight)",
            r"\b(ballast|inverter|controller)"
        ],
        "lampu_variasi": [
            r"\b(variasi|dekorasi|hias|accent)",
            r"\b(rgb|warna\s*warni|color\s*changing)",
            r"\b(strobo|strobe|kelap\s*kelip|blinking)",
            r"\b(underglow|bawah\s*motor|chassis\s*light)"
        ],
        "lampu_emergency": [
            r"\b(emergency|darurat|hazard|warning)",
            r"\b(rem|stop|brake|sein|turn\s*signal)",
            r"\b(safety|keselamatan|visibility)",
            r"\b(fog\s*lamp|kabut|cornering)"
        ]
    },
    "kategori_mounting_body": {
        "mounting_phone": [
            r"\b(phone|hp|handphone|smartphone)",
            r"\b(holder|mount|bracket|cradle)",
            r"\b(gps|navigation|google\s*maps)",
            r"\b(waterproof|anti\s*air|tahan\s*hujan)"
        ],
        "mounting_camera": [
            r"\b(camera|kamera|gopro|action\s*cam)",
            r"\b(recording|rekam|video|photo)",
            r"\b(stabilizer|gimbal|steady)",
            r"\b(360|wide\s*angle|ultra\s*wide)"
        ],
        "body_kit": [
            r"\b(body\s*kit|fairing|full\s*body)",
            r"\b(undercowl|side\s*panel|cover)",
            r"\b(windshield|visor|deflector)",
            r"\b(original|aftermarket|custom|racing)"
        ],
        "material_carbon": [
            r"\b(carbon|karbon|fiber|serat)",
            r"\b(3k|1k|twill|plain\s*weave)",
            r"\b(dry\s*carbon|wet\s*carbon)",
            r"\b(lightweight|ringan|strong|kuat)"
        ]
    }
}

def extract_sub_intents(sentence, main_intent):
    """Extract sub-intents based on pattern matching"""
    sub_intents = []
    sentence_lower = sentence.lower()
    
    if main_intent in sub_intent_patterns:
        for sub_intent, patterns in sub_intent_patterns[main_intent].items():
            for pattern in patterns:
                if re.search(pattern, sentence_lower):
                    sub_intents.append(f"{main_intent}_{sub_intent}")
                    break
    
    # Always include the main intent
    if not sub_intents:
        sub_intents.append(main_intent)
    else:
        sub_intents.append(main_intent)
    
    return sub_intents

# Create multi-label training data
print("Creating multi-label training data...")
multi_label_data = []
for sentence, main_intent in zip(training_sentences, main_labels):
    sub_intents = extract_sub_intents(sentence, main_intent)
    multi_label_data.append((sentence, sub_intents))

# Prepare data for multi-label classification
sentences = [item[0] for item in multi_label_data]
label_sets = [item[1] for item in multi_label_data]

# Convert labels to binary format
mlb = MultiLabelBinarizer()
y_multilabel = mlb.fit_transform(label_sets)

print(f"Training multi-label classifier with {len(mlb.classes_)} possible labels...")

# Train TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X = vectorizer.fit_transform(sentences)

# Train multi-label classifier
classifier = OneVsRestClassifier(MultinomialNB())
classifier.fit(X, y_multilabel)

# Save Version B models
joblib.dump(classifier, "../ml_model/chat_model_v2.pkl")
joblib.dump(vectorizer, "../ml_model/vectorizer_v2.pkl")
joblib.dump(mlb, "../ml_model/label_encoder_v2.pkl")
joblib.dump(sub_intent_patterns, "../ml_model/sub_intent_patterns.pkl")

print("✅ Version B models saved successfully!")
print("   - Multi-label model: chat_model_v2.pkl")
print("   - Multi-label vectorizer: vectorizer_v2.pkl") 
print("   - Label encoder: label_encoder_v2.pkl")
print("   - Sub-intent patterns: sub_intent_patterns.pkl")

print(f"\n📊 Training Statistics:")
print(f"   - Total training sentences: {len(sentences)}")
print(f"   - Unique labels: {len(mlb.classes_)}")
print(f"   - Main intents: {len(set(main_labels))}")

# Show some example classifications
print(f"\n🔍 Example Sub-Intent Classifications:")
test_sentences = [
    "Berapa harga mounting carbon dan ada promo gak?",
    "Lampu LED projector masih ada stok?",
    "Body kit untuk Beat ada yang ready stock?",
    "Biaya pasang lampu DRL berapa ya?"
]

for sentence in test_sentences:
    X_test = vectorizer.transform([sentence])
    predicted_labels = classifier.predict(X_test)
    predicted_intents = mlb.inverse_transform(predicted_labels)[0]
    print(f"   '{sentence}' -> {list(predicted_intents)}") 