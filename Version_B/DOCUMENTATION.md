# Version B - Sub-Intent Detection System

## Overview
Version B introduces advanced sub-intent detection capabilities, allowing the chatbot to provide specific contextual responses based on detailed query analysis within main intent categories.

## System Architecture
- **Multi-Label Classification**: Uses OneVsRestClassifier + MultinomialNB for simultaneous multiple intent detection
- **Sub-Intent Detection**: Distinguishes between different types of inquiries within main intents
- **Hybrid Approach**: Combines ML prediction with regex pattern matching
- **Contextual Responses**: Tailored responses based on specific sub-intents and detected context

## Files
- `train_model_v2.py` - Trains the multi-label classification model with sub-intent patterns
- `predict_v2.py` - Enhanced prediction script with sub-intent detection and contextual responses

## Sub-Intent Categories

### HARGA (Price) Sub-Intents
- `harga_produk` - Specific product pricing
- `harga_promo` - Promotional pricing and discounts
- `harga_grosir` - Wholesale and bulk pricing
- `harga_ongkir` - Shipping cost inquiries
- `harga_instalasi` - Installation service pricing

### STOK_PRODUK (Stock) Sub-Intents
- `stok_tersedia` - Product availability queries
- `stok_habis` - Out of stock and restock inquiries
- `stok_booking` - Booking and pre-order requests

## Usage
```bash
# Train the Version B model
python train_model_v2.py

# Run the enhanced chatbot
python predict_v2.py
```

## Key Features
- **Multi-Intent Handling**: Processes complex queries with multiple intents simultaneously
- **Confidence Scoring**: Filters predictions based on confidence thresholds
- **Motor-Specific Context**: Automatically incorporates detected motor types in responses
- **Debug Mode**: Built-in debugging for development and testing
- **Pattern Enhancement**: Secondary regex-based detection for missed sub-intents

## Enhanced Capabilities
- Detects multiple intents in single query (e.g., price + promo inquiry)
- Provides multiple relevant responses for complex questions
- Context-aware responses based on detected motor types
- Specific responses for sub-categories within main intents

## Example Usage
```
Input: "Berapa harga mounting carbon dan ada promo gak?"
Output: 
1. Specific product pricing information
2. Current promotional offers and discounts

Input: "Lampu LED projector untuk Beat masih ada stok?"
Output: Motor-specific stock availability with product details
```

## Technical Improvements
- Multi-label classification with confidence scoring
- Regex pattern matching for 15+ sub-intent categories
- Enhanced TF-IDF vectorization with n-gram features
- Contextual response generation based on detected intents
- Real-time debug information for system analysis

## Models Generated
- `chat_model_v2.pkl` - Multi-label classifier
- `vectorizer_v2.pkl` - Enhanced TF-IDF vectorizer
- `label_encoder_v2.pkl` - Multi-label binarizer
- `sub_intent_patterns.pkl` - Regex patterns for sub-intents 