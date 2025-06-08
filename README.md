# 🏍️ Multi-Intent Chatbot for Motorcycle Spare Parts Business

## 📋 Overview

This is an intelligent chatbot system designed specifically for a motorcycle spare parts business located in Bandung, Indonesia. The chatbot can understand and respond to customer inquiries in **Bahasa Indonesia** with **multi-intent detection**, meaning it can handle complex questions that involve multiple topics at once.

### 🚀 **Current Systems: Version A & Version B**

This project now includes **two distinct systems** with different capabilities:

- **Version A**: Basic intent detection with predefined responses
- **Version B**: Advanced sub-intent detection with contextual responses

### 📌 Latest Updates (June 2025)
- ✅ **Version B Implementation**: Advanced sub-intent detection system
- ✅ **Major Dataset Expansion**: 1,550+ sentences across 13 intent categories  
- ✅ **Enhanced Architecture**: Multi-label classification with contextual responses
- ✅ **Organized Structure**: Clear separation between Version A and Version B systems

### 🎯 Business Context
- **Business Type**: Motorcycle Spare Parts Store
- **Location**: Bandung & Cimahi, West Java, Indonesia
- **Product Categories**: 
  - 🔧 **Mounting & Body** (mounting systems, body kits, fairings)
  - 💡 **Lighting** (LED lights, variasi, projectors, RGB)
- **Services**: Installation, delivery, technical support

---

## ⚡ System Comparison: Version A vs Version B

### 🏗️ **Architecture Overview**

| **Aspect** | **Version A** | **Version B** |
|------------|---------------|---------------|
| **Intent Detection** | Single main intent per query | Multiple sub-intents simultaneously |
| **Classification Model** | Naive Bayes + TF-IDF | OneVsRestClassifier + MultinomialNB |
| **Response Type** | Generic predefined responses | Contextual & specific responses |
| **Query Complexity** | Simple single-intent queries | Complex multi-intent queries |
| **Pattern Matching** | Basic keyword matching | Advanced regex patterns (60+) |
| **Confidence Scoring** | Not available | Decision function based |
| **Debug Features** | Limited | Comprehensive debug mode |
| **Motor Context** | Basic compatibility check | Integrated contextual responses |

### 🎯 **Key Differences**

#### **Version A - Basic Intent Detection**
- ✅ Simple and reliable single-intent detection
- ✅ Fast processing with minimal complexity
- ✅ Generic responses cover all scenarios
- ✅ Easy to maintain and understand
- ❌ Limited contextual understanding
- ❌ Cannot handle multi-topic queries effectively

#### **Version B - Advanced Sub-Intent Detection**  
- ✅ Sophisticated multi-intent detection
- ✅ Contextual responses based on sub-intents
- ✅ Can handle complex queries like "Berapa harga mounting carbon dan ada promo gak?"
- ✅ Motor-specific contextual responses
- ✅ Built-in debug and confidence scoring
- ❌ More complex system architecture
- ❌ Higher computational requirements

### 🔄 **Use Case Recommendations**

| **Scenario** | **Recommended Version** | **Reason** |
|--------------|------------------------|------------|
| Simple business queries | Version A | Fast, reliable, sufficient for basic needs |
| Complex customer inquiries | Version B | Better understanding of multi-topic questions |
| High-volume simple requests | Version A | Lower computational overhead |
| Premium customer service | Version B | More sophisticated and contextual responses |
| Development/Testing | Version B | Better debugging and analysis tools |

## 🚀 **Core Features (Both Versions)**

### 🧠 Multi-Intent Detection
- **Version A**: Primary ML + Secondary keyword matching
- **Version B**: Multi-label ML + Enhanced pattern matching
- **Fallback System**: Comprehensive error handling and motor compatibility checking

### 💬 Smart Response System
- **13 Different Intent Categories** with specialized responses
- **Multiple Responses**: Complex queries get multiple relevant answers
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

## 📁 **Project Structure**

```
ml_model/
├── 📁 Version A/              # Basic Intent Detection System
│   ├── 📄 train_model.py         # Basic Naive Bayes training
│   ├── 📄 predict.py             # Single intent detection with keyword matching
│   └── 📄 [DOCUMENTATION.md](Version%20A/DOCUMENTATION.md)       # Version A documentation
│
├── 📁 Version B/              # Advanced Sub-Intent Detection System  
│   ├── 📄 train_model_v2.py      # Multi-label classification training
│   ├── 📄 predict_v2.py          # Sub-intent detection with contextual responses
│   ├── 📄 test_version_b.py      # Testing and validation script
│   └── 📄 [DOCUMENTATION.md](Version%20B/DOCUMENTATION.md)       # Version B documentation
│
├── 📁 ml_model/               # Model Files (Generated)
│   ├── 📄 chat_model.pkl         # Version A: Basic Naive Bayes model
│   ├── 📄 vectorizer.pkl         # Version A: TF-IDF vectorizer
│   ├── 📄 chat_model_v2.pkl      # Version B: Multi-label classifier
│   ├── 📄 vectorizer_v2.pkl      # Version B: Enhanced TF-IDF vectorizer
│   ├── 📄 label_encoder_v2.pkl   # Version B: Multi-label binarizer
│   └── 📄 sub_intent_patterns.pkl # Version B: Regex patterns for sub-intents
│
├── 📁 data/                   # Training Dataset (1,550+ Indonesian sentences)
│   ├── 📄 harga.py               # Pricing and cost inquiries (120+ sentences)
│   ├── 📄 daftar.py              # Registration for installation booking (120+ sentences)  
│   ├── 📄 jam_operasional.py     # Operating hours and schedule (100+ sentences)
│   ├── 📄 garansi.py             # Warranty and guarantee information (110+ sentences)
│   ├── 📄 booking_pemasangan.py  # Installation booking service (110+ sentences)
│   ├── 📄 kategori_mounting_body.py # Mounting and body products (140+ sentences)
│   ├── 📄 kategori_lighting.py   # Lighting products (140+ sentences)
│   ├── 📄 pengiriman.py          # Shipping and delivery (110+ sentences)
│   ├── 📄 durasi_pengiriman.py   # Delivery time estimates (110+ sentences)
│   ├── 📄 wilayah_pemasangan.py  # Installation coverage area (110+ sentences)
│   ├── 📄 tipe_motor_matic.py    # Supported motorcycle types (120+ sentences)
│   ├── 📄 stok_produk.py         # Stock availability (130+ sentences)
│   └── 📄 layanan_instalasi.py   # Installation services (130+ sentences)
│
├── 📄 intent_data.py          # Main training data loader (shared)
├── 📄 README.md               # This comprehensive documentation
```

### 🎯 **Version B Sub-Intent Categories**

**Version B** introduces advanced sub-intent detection with **16 specialized categories**:

#### **HARGA (Price) - 5 Sub-Intents**
- `harga_produk` - Specific product pricing inquiries
- `harga_promo` - Promotional pricing and discounts  
- `harga_grosir` - Wholesale and bulk pricing
- `harga_ongkir` - Shipping cost inquiries
- `harga_instalasi` - Installation service pricing

#### **STOK_PRODUK (Stock) - 3 Sub-Intents**
- `stok_tersedia` - Product availability queries
- `stok_habis` - Out of stock and restock inquiries
- `stok_booking` - Booking and pre-order requests

#### **KATEGORI_LIGHTING - 4 Sub-Intents**
- `lampu_led` - LED lighting products
- `lampu_projector` - Projector and HID lighting
- `lampu_variasi` - Decorative and accent lighting
- `lampu_emergency` - Safety and emergency lighting

#### **KATEGORI_MOUNTING_BODY - 4 Sub-Intents**
- `mounting_phone` - Phone holder mounts
- `mounting_camera` - Camera and action cam mounts
- `body_kit` - Body kits and fairings
- `material_carbon` - Carbon fiber materials

---

## 🛠️ **Installation & Setup**

### Prerequisites
```bash
# Required Python packages
pip install scikit-learn
pip install joblib
pip install numpy
```

### 🔧 **Quick Start Guide**

#### **🚀 Version A - Basic System**
📖 **[View Version A Documentation](Version%20A/DOCUMENTATION.md)**

1. **Navigate to Version A**:
   ```bash
   cd "Version A"
   ```

2. **Train the Model**:
   ```bash
   python train_model.py
   ```
   ✅ Output: `Model dan vectorizer berhasil disimpan ke folder ml_model/`

3. **Run Interactive Chat**:
   ```bash
   python predict.py
   ```

#### **🚀 Version B - Advanced System**
📖 **[View Version B Documentation](Version%20B/DOCUMENTATION.md)**

1. **Navigate to Version B**:
   ```bash
   cd "Version B"
   ```

2. **Train the Multi-Label Model**:
   ```bash
   python train_model_v2.py
   ```
   ✅ Output: `Version B models saved successfully!`

3. **Run Enhanced Interactive Chat**:
   ```bash
   python predict_v2.py
   ```

4. **Test Sub-Intent Detection**:
   ```bash
   python test_version_b.py
   ```

### 📊 **System Testing**
```bash
# Quick system verification (from main directory)
python test_version_b_simple.py
```

---

## 💡 **Usage Examples**

### 📱 **Version A - Basic Interactive Mode**
```bash
cd "Version A"
python predict.py
```
```
Anda: Berapa harga mounting LED untuk Beat?
Bot: 💰 **HARGA & PAKET** | Untuk harga mounting & body atau lighting...
Bot: 🏍️ **MOTOR SUPPORT** | Honda: Beat, Vario 125/160, PCX, Scoopy...
Bot: 💡 **KATEGORI: LIGHTING** | Tersedia: LED headlamp, DRL, lampu variasi...
```

### 🚀 **Version B - Advanced Interactive Mode**
```bash
cd "Version B"  
python predict_v2.py
```
```
Anda: Berapa harga mounting carbon dan ada promo gak?

🔍 Analyzing: 'Berapa harga mounting carbon dan ada promo gak?'
🎯 ML Predictions: ['harga_harga_produk', 'harga_harga_promo']
🔧 Enhanced Labels: ['harga_harga_produk', 'harga_harga_promo', 'harga']

Bot Responses:
1. 💰 **HARGA PRODUK SPESIFIK** | Harga mounting carbon: Rp 450.000-650.000...
2. 🎉 **PROMO & DISKON TERKINI** | Saat ini ada promo bundling mounting + lampu diskon 15%!...
```

### 🔗 **Programmatic Usage**

#### **Version A - Basic Usage**
```python
# Add to Python path
import sys
sys.path.append('Version A')
from predict import get_responses

# Single intent query
responses = get_responses("Jam berapa toko buka?")
print(responses[0])  # 🕘 **JAM OPERASIONAL** | Buka setiap hari 09.00-17.00...
```

#### **Version B - Advanced Usage**
```python
# Add to Python path
import sys
sys.path.append('Version B')
from predict_v2 import get_enhanced_response

# Multi-intent query with sub-intent detection
user_input = "Lampu LED projector untuk Beat masih ada stok?"
responses, labels = get_enhanced_response(user_input)

print(f"Detected Labels: {labels}")
for i, response in enumerate(responses, 1):
    print(f"Response {i}: {response}")
```

### 🎯 **Example Comparison**

| **Query** | **Version A Response** | **Version B Response** |
|-----------|------------------------|------------------------|
| "Berapa harga mounting carbon dan ada promo gak?" | Generic price response | 1. Specific carbon mounting price<br/>2. Current promotional offers |
| "Lampu LED untuk Beat masih ada stok?" | Generic stock + lighting info | Motor-specific LED stock with Beat compatibility |
| "Biaya pasang lampu di rumah weekend?" | Basic installation info | Specific weekend installation pricing + home service details |

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

### 📈 Dataset Expansion (June 2025)
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

## 📅 **Version History & Evolution**

### 🚀 **Current Release** (June 2025) - **Dual System Architecture**

#### 🏗️ **Version B - Advanced Sub-Intent Detection** *(New)*
- **Architecture**: Multi-label classification with OneVsRestClassifier + MultinomialNB
- **Sub-Intent Detection**: 16 specialized sub-categories across 4 main intents
- **Pattern Matching**: 60+ advanced regex patterns for enhanced detection
- **Contextual Responses**: Motor-specific and sub-intent specific responses
- **Debug Features**: Comprehensive debugging and confidence scoring
- **Model Files**: 4 specialized pickle files (classifier, vectorizer, encoder, patterns)

#### 🔧 **Version A - Stable Basic System** *(Preserved)*
- **Architecture**: Single Naive Bayes classifier with TF-IDF
- **Intent Detection**: Reliable single main intent per query
- **Keyword Matching**: Enhanced secondary detection with regex
- **Fast Processing**: Optimized for high-volume simple queries
- **Compatibility**: Maintained backward compatibility for existing integrations

#### 📊 **Dataset Enhancement**
- **Total Sentences**: 1,550+ (expanded from 1,330+)
- **Distribution**: 100-140 sentences per intent category
- **Quality Improvement**: Enhanced Indonesian language authenticity
- **Organization**: Maintained structured `data/` directory with 13 files

---

### 📋 **Version 2.0** (June 2025) - *Dataset Expansion*
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

---

### 📋 **Version 1.0** (Initial Release) - *Foundation*
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

## 🎯 **Which Version Should You Use?**

### 🚀 **Choose Version B if you need:**
- ✅ Advanced multi-intent detection
- ✅ Specific contextual responses  
- ✅ Complex query handling ("Berapa harga mounting carbon dan ada promo gak?")
- ✅ Motor-specific contextual responses
- ✅ Development and debugging tools
- ✅ Premium customer service experience

### ⚡ **Choose Version A if you need:**
- ✅ Simple, reliable intent detection
- ✅ Fast processing for high-volume requests
- ✅ Minimal computational requirements
- ✅ Easy maintenance and deployment
- ✅ Backward compatibility with existing systems

### 🔧 **Production Deployment Considerations**

| **Factor** | **Version A** | **Version B** |
|------------|---------------|---------------|
| **Response Time** | ~10ms | ~50ms |
| **Memory Usage** | ~15MB | ~50MB |
| **Model Size** | ~30KB | ~2MB |
| **Complexity** | Low | High |
| **Maintenance** | Easy | Moderate |
| **Accuracy** | Good | Excellent |

---

## 📞 **Support & Documentation**

### 📖 **Quick Links to Documentation**
- **[📄 Version A Documentation](Version%20A/DOCUMENTATION.md)** - Basic intent detection system guide
- **[📄 Version B Documentation](Version%20B/DOCUMENTATION.md)** - Advanced sub-intent detection system guide  
- **📁 Training Data**: `data/` directory (shared between versions)

### 🔗 **Additional Resources**
- **System Comparison**: See architecture table above
- **Technical Details**: Individual documentation files in each version folder
- **Installation Guide**: Quick start section above

---

**Last Updated**: June 2025  
**Current Systems**: Version A (Basic) + Version B (Advanced)  
**Total Training Data**: 1,550+ Indonesian sentences across 13 intent categories