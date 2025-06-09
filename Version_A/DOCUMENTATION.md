# Version A - Basic Intent Detection System

## Overview
Version A is the original chatbot system with basic intent detection that provides predefined responses for each main intent category.

## System Architecture
- **Single Intent Detection**: Uses Naive Bayes + TF-IDF for one intent per query
- **Predefined Responses**: Fixed responses for each of the 13 main intents
- **Basic Keyword Matching**: Simple keyword bank for secondary intent detection
- **Motor Compatibility Check**: Basic validation for supported motor types

## Files
- `train_model.py` - Trains the basic Naive Bayes model
- `predict.py` - Main prediction script with intent detection and response generation

## Main Intents (13 categories)
1. `harga` - Price inquiries
2. `daftar` - Registration/membership
3. `jam_operasional` - Operating hours
4. `garansi` - Warranty information
5. `booking_pemasangan` - Installation booking
6. `kategori_mounting_body` - Mounting & body products
7. `kategori_lighting` - Lighting products
8. `pengiriman` - Shipping information
9. `durasi_pengiriman` - Delivery duration
10. `wilayah_pemasangan` - Service area coverage
11. `tipe_motor_matic` - Supported motor types
12. `stok_produk` - Product stock
13. `layanan_instalasi` - Installation services

## Usage
```bash
# Train the model
python train_model.py

# Run the chatbot
python predict.py
```

## Features
- Multi-intent detection using keyword matching
- Indonesian language support with slang terms
- Motor type compatibility checking
- Professional business responses with emojis
- Fallback system for unrecognized queries

## Limitations
- Single main intent per query limitation
- Generic responses without context specificity
- No sub-intent differentiation within categories
- Limited handling of complex multi-topic queries 