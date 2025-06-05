# 🏍️ Multi-Intent Chatbot for Motorcycle Spare Parts Business

## 📋 Overview

This is an intelligent chatbot system designed specifically for a motorcycle spare parts business located in Bandung, Indonesia. The chatbot can understand and respond to customer inquiries in **Bahasa Indonesia** with **multi-intent detection**, meaning it can handle complex questions that involve multiple topics at once.

### 🎯 Business Context
- **Business Type**: Motorcycle Spare Parts Store
- **Location**: Bandung & Cimahi, West Java, Indonesia
- **Product Categories**: 
  - 🔧 **Mounting & Body** (mounting systems, body kits, fairings)
  - 💡 **Lighting** (LED lights, variasi, projectors, RGB)
- **Services**: Installation, delivery, technical support

---

## 🚀 Key Features

### 🧠 Multi-Intent Detection
- **Primary Intent**: Detected using Machine Learning (Naive Bayes + TF-IDF)
- **Secondary Intents**: Detected using keyword matching with regex
- **Fallback System**: Comprehensive error handling and motor compatibility checking

### 💬 Smart Response System
- **13 Different Intent Categories** with specialized responses
- **Multiple Responses**: Can provide several relevant answers for complex queries
- **Rich Formatting**: Professional responses with emojis and clear categorization
- **Indonesian Language**: Natural Bahasa Indonesia with slang and regional terms

### 🎌 Supported Intents
1. **harga** - Pricing and cost inquiries
2. **daftar** - Registration and membership
3. **jam_operasional** - Operating hours and schedule
4. **garansi** - Warranty and guarantee information
5. **booking_pemasangan** - Installation booking service
6. **kategori_mounting_body** - Mounting and body products
7. **kategori_lighting** - Lighting products
8. **pengiriman** - Shipping and delivery
9. **durasi_pengiriman** - Delivery time estimates
10. **wilayah_pemasangan** - Installation coverage area
11. **tipe_motor_matic** - Supported motorcycle types
12. **stok_produk** - Stock availability
13. **layanan_instalasi** - Installation services

---

## 📁 File Structure

```
ml_model/
├── 📄 predict.py          # Main prediction system with multi-intent logic
├── 📄 intent_data.py      # Training data (330+ Indonesian sentences)
├── 📄 train_model.py      # Model training script
├── 📄 test_multi_intent.py # Testing script for multi-intent functionality
├── 📄 chat_model.pkl      # Trained Naive Bayes model
├── 📄 vectorizer.pkl      # TF-IDF vectorizer
└── 📄 README.md           # This documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Required Python packages
pip install scikit-learn
pip install joblib
```

### 🔧 Quick Start

1. **Clone or Download** the project files to your local machine

2. **Train the Model** (first time only):
   ```bash
   python train_model.py
   ```
   ✅ Output: `Model dan vectorizer berhasil disimpan ke folder ml_model/`

3. **Test the System**:
   ```bash
   python test_multi_intent.py
   ```

4. **Run Interactive Chat**:
   ```bash
   python predict.py
   ```

---

## 💡 Usage Examples

### 📱 Interactive Mode
```bash
python predict.py
```
```
Anda: Berapa harga mounting LED untuk Beat?
Bot: 💰 **HARGA & PAKET** | Untuk harga mounting & body atau lighting...
Bot: 🏍️ **MOTOR SUPPORT** | Honda: Beat, Vario 125/160, PCX, Scoopy...
Bot: 💡 **KATEGORI: LIGHTING** | Tersedia: LED headlamp, DRL, lampu variasi...
```

### 🔗 Programmatic Usage
```python
from predict import get_responses, predict_intents

# Single intent query
user_input = "Jam berapa toko buka?"
responses = get_responses(user_input)
print(responses[0])  # 🕘 **JAM OPERASIONAL** | Buka setiap hari 09.00-17.00...

# Multi-intent query
user_input = "Mau beli lampu variasi, ada stok? Bisa pasang di Cimahi?"
responses = get_responses(user_input)
for i, response in enumerate(responses, 1):
    print(f"Response {i}: {response}")
```

---

## 🔬 Technical Details

### 🧮 Machine Learning Architecture

```
User Input → TF-IDF Vectorizer → Naive Bayes Classifier → Primary Intent
     ↓
Keyword Matching → Regex Pattern Detection → Secondary Intents
     ↓
Motor Compatibility Check → Fallback Responses
     ↓
Response Selection → Multi-Response Output
```

### 📊 Training Data Statistics
- **Total Sentences**: 330+
- **Intent Distribution**:
  - High Priority: 30 sentences (harga, mounting_body, lighting)
  - Standard: 25 sentences each (other intents)
- **Language Features**:
  - Indonesian slang: "brp", "gak", "gimana"
  - Regional terms: Bandung area locations
  - Technical terms: motorcycle and electronics vocabulary

### 🎯 Keyword Bank Structure
```python
keyword_bank = {
    "harga": ["harga", "biaya", "brp", "duit", "budget", "promo", ...],
    "kategori_lighting": ["lampu", "led", "variasi", "sein", "drl", ...],
    # ... 13 intent categories with 15-30 keywords each
}
```

---

## 🏍️ Supported Motorcycles

### ✅ Currently Supported
- **Honda**: Beat, Vario, Revo X, PCX, Scoopy, Vespa
- **Yamaha**: Vega Force, Jupiter Z1, Aerox
- **Suzuki**: Address FI, Smash FI
- **TVS**: Dazz
- **Viar**: Star NX

### 📍 Service Coverage
- **Installation Service**: Bandung City & Cimahi only
- **Delivery**: All Indonesia (via JNE/J&T/Sicepat)
- **Same Day Delivery**: Bandung-Cimahi area

---

## 🔧 Customization Guide

### 📝 Adding New Training Data
1. **Edit `intent_data.py`**:
   ```python
   # Add new sentences to existing intents
   training_sentences = [
       # Add your new Indonesian sentences here
       "Contoh kalimat baru untuk intent tertentu",
       # ...
   ]
   
   # Update labels count
   labels = (
       ["harga"] * 35 +  # Increased from 30
       # ...
   )
   ```

2. **Retrain the model**:
   ```bash
   python train_model.py
   ```

### 🆕 Adding New Intent Categories
1. **Add training data** in `intent_data.py`
2. **Add response** in `predict.py` → `answer_dict`
3. **Add keywords** in `predict.py` → `keyword_bank`
4. **Update motor list** if needed in `motor_tersedia`

### 🎨 Customizing Responses
Edit the `answer_dict` in `predict.py`:
```python
answer_dict = {
    "your_intent": "🎯 **YOUR CATEGORY** | Your custom response here...",
}
```

---

## 🧪 Testing & Quality Assurance

### 🔍 Running Tests
```bash
# Test multi-intent functionality
python test_multi_intent.py

# Test specific scenarios
python -c "from predict import get_responses; print(get_responses('your test query'))"
```

### ✅ Test Coverage
- ✅ Multi-intent detection
- ✅ Indonesian language processing  
- ✅ Keyword matching accuracy
- ✅ Motor compatibility checking
- ✅ Response formatting
- ✅ Fallback mechanisms

---

## 🚀 Deployment Options

### 🌐 Web Integration
```python
# Flask example
from flask import Flask, request, jsonify
from predict import get_responses

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    responses = get_responses(user_input)
    return jsonify({'responses': responses})
```

### 📱 WhatsApp Integration
- Use with WhatsApp Business API
- Integrate with Twilio/ChatAPI
- Support for rich formatting

### 🤖 Discord/Telegram Bot
- Easy integration with bot frameworks
- Multi-response handling
- Indonesian language support

---

## 📈 Performance Optimization

### 🚀 Speed Improvements
- Model loading: ~0.1s (one-time)
- Prediction time: ~0.01s per query
- Multi-intent processing: ~0.02s

### 💾 Memory Usage
- Model size: ~26KB (chat_model.pkl)
- Vectorizer: ~3.7KB (vectorizer.pkl)
- Runtime memory: ~10MB

---

## 🐛 Troubleshooting

### Common Issues

**❌ "Model file not found"**
```bash
# Solution: Train the model first
python train_model.py
```

**❌ "Import error: No module named 'sklearn'"**
```bash
# Solution: Install required packages
pip install scikit-learn joblib
```

**❌ "No responses generated"**
- Check if input contains supported keywords
- Verify motor compatibility
- Test with simpler queries

### 🔧 Debug Mode
```python
# Enable detailed logging
from predict import predict_intents
intents = predict_intents("your query")
print(f"Detected intents: {intents}")
```
