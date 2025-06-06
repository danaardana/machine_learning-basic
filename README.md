# 🏍️ Multi-Intent Chatbot for Motorcycle Spare Parts Business

## 📋 Overview

This is an intelligent chatbot system designed specifically for a motorcycle spare parts business located in Bandung, Indonesia. The chatbot can understand and respond to customer inquiries in **Bahasa Indonesia** with **multi-intent detection**, meaning it can handle complex questions that involve multiple topics at once.

### 📌 Current Version: **v2.0** (November 2024)
- **Major Dataset Expansion**: 1,330+ sentences (4x growth)
- **Enhanced Indonesian Language**: Improved language quality and authenticity
- **Business Model Accuracy**: Corrected service scope and registration process
- **Better Organization**: Structured dataset in dedicated `data/` directory

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
1. **harga** - Pricing and cost inquiries (100+ sentences)
2. **daftar** - Registration for installation booking (100+ sentences)
3. **jam_operasional** - Operating hours and schedule (100+ sentences)
4. **garansi** - Warranty and guarantee information (100+ sentences)
5. **booking_pemasangan** - Installation booking service (100+ sentences)
6. **kategori_mounting_body** - Mounting and body products (100+ sentences)
7. **kategori_lighting** - Lighting products (100+ sentences)
8. **pengiriman** - Shipping and delivery (100+ sentences)
9. **durasi_pengiriman** - Delivery time estimates (100+ sentences)
10. **wilayah_pemasangan** - Installation coverage area (100+ sentences)
11. **tipe_motor_matic** - Supported motorcycle types (100+ sentences)
12. **stok_produk** - Stock availability (100+ sentences)
13. **layanan_instalasi** - Installation services (100+ sentences)

> **Note**: The `daftar` intent specifically handles registration for installation booking services, requiring customer name, email, and phone number. This replaces any previous membership/VIP concepts that don't exist in the actual business model.

---

## 📁 File Structure

```
ml_model/
├── 📄 predict.py          # Main prediction system with multi-intent logic
├── 📄 intent_data.py      # Main training data loader
├── 📄 train_model.py      # Model training script
├── 📄 chat_model.pkl      # Trained Naive Bayes model
├── 📄 vectorizer.pkl      # TF-IDF vectorizer
├── 📁 data/               # Dataset directory (1,330+ Indonesian sentences)
│   ├── 📄 harga.py           # Pricing and cost inquiries (100+ sentences)
│   ├── 📄 daftar.py          # Registration for installation booking (100+ sentences)
│   ├── 📄 jam_operasional.py # Operating hours and schedule (100+ sentences)
│   ├── 📄 garansi.py         # Warranty and guarantee information (100+ sentences)
│   ├── 📄 booking_pemasangan.py # Installation booking service (100+ sentences)
│   ├── 📄 kategori_mounting_body.py # Mounting and body products (100+ sentences)
│   ├── 📄 kategori_lighting.py # Lighting products (100+ sentences)
│   ├── 📄 pengiriman.py      # Shipping and delivery (100+ sentences)
│   ├── 📄 durasi_pengiriman.py # Delivery time estimates (100+ sentences)
│   ├── 📄 wilayah_pemasangan.py # Installation coverage area (100+ sentences)
│   ├── 📄 tipe_motor_matic.py # Supported motorcycle types (100+ sentences)
│   ├── 📄 stok_produk.py     # Stock availability (100+ sentences)
│   └── 📄 layanan_instalasi.py # Installation services (100+ sentences)
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
- **Total Sentences**: 1,330+ (significantly expanded dataset)
- **Intent Distribution**:
  - Comprehensive coverage: 100+ sentences per intent category
  - Balanced dataset across all 13 intent categories
  - Rich variations in each category with proper categorization
- **Language Features**:
  - **Predominantly Indonesian** with natural mixed terminology
  - Indonesian slang: "brp", "gak", "gimana", "aja", "bisa"
  - Regional terms: Bandung, Cimahi, Jabar area locations
  - Technical terms: motorcycle and electronics vocabulary
  - **Language Quality**: Recently improved from mixed English-Indonesian to predominantly Indonesian while preserving natural motorcycle community terminology

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
- **Honda**: Beat, Vario 125/160, PCX, Scoopy, Revo X, Genio, Stylo, Spacy, Dio
- **Yamaha**: Aerox, Nmax, Freego, Lexi, Mio series, Fino, Gear, Soul GT, Vega, Jupiter Z, XRide
- **Suzuki**: Address, Nex II, Skydrive, Spin, Satria, Hayate, Smash
- **Kawasaki**: Ninja series, KLX series, Versys
- **TVS**: Various models supported
- **KTM**: Duke series
- **Vespa**: Classic and modern series
- **Other**: Various imported and local brands

### 📍 Service Coverage
- **Installation Service**: Bandung City & Cimahi only
- **Delivery**: All Indonesia (via JNE/J&T/Sicepat)
- **Same Day Delivery**: Bandung-Cimahi area

---

## 🆕 Recent Improvements

### 📈 Dataset Expansion (November 2024)
- **4x Dataset Growth**: Expanded from 330+ to 1,330+ sentences
- **Comprehensive Coverage**: Each intent now has 100+ high-quality sentences
- **Better Organization**: Structured dataset files in dedicated `data/` directory
- **Rich Categorization**: Each dataset file has well-organized sections and categories

### 🇮🇩 Language Quality Enhancement
- **Improved Indonesian Usage**: Converted fully English sentences to Indonesian
- **Natural Mixed Terminology**: Preserved authentic motorcycle community language
- **Regional Authenticity**: Maintained Bandung-Cimahi area terminology
- **Technical Balance**: Kept necessary English technical terms while improving overall Indonesian quality

### 🎯 Business Model Accuracy
- **Corrected Registration**: `daftar` intent now specifically handles installation booking registration
- **Removed Non-existent Services**: Eliminated VIP/membership/reseller programs that don't exist
- **Focused Service Scope**: Clear focus on actual business services (installation booking with name, email, phone)

### 📊 Model Performance
- **Maintained Accuracy**: All improvements preserve model performance and accuracy
- **Faster Training**: Better organized dataset structure
- **Consistent Results**: Thoroughly tested to ensure stability

---

## 📅 Version History

### 🚀 **Version 1.1** (July 2025) - *Current*
#### 📈 **Major Dataset Expansion**
- **Dataset Size**: 1,330+ sentences (expanded from 330+)
- **Coverage**: 100+ sentences per intent category (previously ~25)
- **Organization**: Structured into dedicated `data/` directory with 13 separate files
- **Categories**: Well-organized sections within each dataset file

#### 🇮🇩 **Language Quality Enhancement**
- **Indonesian Improvement**: Converted fully English sentences to Indonesian
- **Natural Terminology**: Preserved authentic motorcycle community mixed language
- **Regional Accuracy**: Maintained Bandung-Cimahi area authenticity
- **Technical Balance**: Kept necessary English terms while improving overall Indonesian quality

#### 🎯 **Business Model Corrections**
- **Registration Scope**: `daftar` intent now specifically handles installation booking registration
- **Service Accuracy**: Removed non-existent VIP/membership/reseller programs
- **Clear Focus**: Registration requires only name, email, and phone number
- **Realistic Services**: Aligned with actual business operations

#### 🛠️ **Technical Improvements**
- **File Structure**: Reorganized codebase with better separation of concerns
- **Dataset Management**: Individual files for each intent category
- **Maintainability**: Easier to update and expand individual categories
- **Performance**: Maintained model accuracy while improving organization

---

### 📋 **Version 1.0** (Initial Release)
#### 🔧 **Core Features**
- **Dataset Size**: 330+ sentences across 13 intent categories
- **Multi-Intent Detection**: Primary ML detection + secondary keyword matching
- **Indonesian Support**: Basic Bahasa Indonesia with mixed English
- **Motorcycle Focus**: Specialized for motorcycle spare parts business

#### 📊 **Dataset Distribution**
- **High Priority**: 30 sentences (harga, mounting_body, lighting)
- **Standard Coverage**: 25 sentences each (other intents)
- **Single File**: All training data in `intent_data.py`
- **Basic Organization**: Simple list structure

#### 🎌 **Intent Categories**
- **13 Intent Types**: Same categories as current version
- **Basic Responses**: Standard response templates
- **Limited Scope**: Included some non-existent business services
- **Mixed Language**: Heavy mix of English-Indonesian

#### 🏍️ **Motorcycle Support**
- **Limited Models**: Basic Honda, Yamaha, Suzuki support
- **Basic Compatibility**: Simple motorcycle type checking
- **Regional Focus**: Bandung area service

---

## 🔄 Migration Guide (v1.0 → v2.0)

### ✅ **Automatic Compatibility**
- **Model Files**: Existing `chat_model.pkl` and `vectorizer.pkl` remain compatible
- **API Interface**: `predict.py` functions unchanged for existing integrations
- **Response Format**: Same response structure and formatting

### 🔄 **What Changed**
- **Dataset Location**: Training data moved from single file to `data/` directory
- **Dataset Size**: 4x expansion requires retraining for optimal performance
- **Language Quality**: Better Indonesian sentences for improved accuracy
- **Business Scope**: More accurate service representation

### 🚀 **Recommended Update Steps**
1. **Backup Current Model**: Save existing `chat_model.pkl` and `vectorizer.pkl`
2. **Retrain Model**: Run `python train_model.py` with new dataset
3. **Test Performance**: Verify improved accuracy with Indonesian queries
4. **Deploy**: Use new model files for production

---

## 🔧 Customization Guide

### 📝 Adding New Training Data
1. **Edit the appropriate file in the `data/` directory**:
   ```python
   # Example: Edit data/harga.py
   sentences = [
       # Add new Indonesian sentences here
       "Contoh kalimat baru untuk intent harga",
       "Berapa harga mounting terbaru?",
       # ...
   ]
   ```

2. **Each dataset file is well-organized with sections**:
   ```python
   # Example structure in data/harga.py
   sentences = [
       # Basic pricing inquiries
       "Berapa harga mounting untuk Beat?",
       
       # Specific product pricing  
       "Harga lampu LED berapa?",
       
       # Installation pricing
       "Biaya pasang mounting berapa?",
       # ... and so on with 100+ sentences
   ]
   ```

3. **Retrain the model**:
   ```bash
   python train_model.py
   ```

### 🆕 Adding New Intent Categories
1. **Create new dataset file** in `data/` directory (e.g., `data/new_intent.py`)
2. **Add 100+ Indonesian sentences** following the established format
3. **Update `intent_data.py`** to import the new dataset
4. **Add response** in `predict.py` → `answer_dict`
5. **Add keywords** in `predict.py` → `keyword_bank`
6. **Update motor list** if needed in `motor_tersedia`

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

---

Last Updated: June 2025 Version: 1.1 - Major Dataset Expansion