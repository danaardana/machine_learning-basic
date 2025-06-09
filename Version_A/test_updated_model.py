#!/usr/bin/env python3
"""
Test Updated Version A Model
Check if shipping inquiries are correctly classified
"""

import sys
import os
sys.path.append('..')
from predict import predict_intents

def test_problematic_queries():
    """Test queries that were previously misclassified"""
    
    test_queries = [
        "Kalau pengiriman ke Bandung brp lama?",
        "bila memasukan kirim ke bandung bisa?", 
        "mau pesan, kirim ke bandung bisa?",
        "Kirim ke Bandung berapa hari sampai?",
        "Pengiriman ke Bandung tersedia?",
        "Order ke Bandung bisa diproses?"
    ]
    
    print("🧪 **TESTING UPDATED VERSION A MODEL**")
    print("=" * 50)
    print("Testing queries that should go to shipping/delivery intents:")
    print("-" * 50)
    
    for query in test_queries:
        intent = predict_intents(query)[0]
        
        # Check if it's correctly classified as shipping-related
        if intent in ['durasi_pengiriman', 'pengiriman']:
            status = "✅ CORRECT"
        else:
            status = "❌ WRONG"
            
        print(f"{status} '{query}' → {intent}")
    
    print("\n📊 **EXPECTED CLASSIFICATION:**")
    print("   • 'pengiriman ke [city] brp lama?' → durasi_pengiriman")
    print("   • 'kirim ke [city] bisa?' → pengiriman") 
    print("   • 'mau pesan, kirim ke [city] bisa?' → pengiriman/durasi_pengiriman")

if __name__ == "__main__":
    test_problematic_queries() 