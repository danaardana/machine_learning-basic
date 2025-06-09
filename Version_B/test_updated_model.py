#!/usr/bin/env python3
"""
Test Updated Version B Model
Check if shipping inquiries are correctly classified with sub-intent detection
"""

import sys
import os
sys.path.append('..')
from predict_v2 import predict_sub_intents

def test_problematic_queries():
    """Test queries that were previously misclassified"""
    
    test_queries = [
        "Kalau pengiriman ke Bandung brp lama?",
        "bila memasukan kirim ke bandung bisa?", 
        "mau pesan, kirim ke bandung bisa?",
        "Kirim ke Bandung berapa hari sampai?",
        "Pengiriman ke Bandung tersedia?",
        "Order ke Bandung bisa diproses?",
        "Berapa harga mounting dan ongkir ke Bandung?"
    ]
    
    print("🧪 **TESTING UPDATED VERSION B MODEL**")
    print("=" * 60)
    print("Testing queries with sub-intent detection:")
    print("-" * 60)
    
    for query in test_queries:
        try:
            labels, confidence = predict_sub_intents(query)
            main_intent = labels[0] if labels else "unknown"
            
            # Check if it's correctly classified as shipping-related
            shipping_related = any(intent in ['durasi_pengiriman', 'pengiriman'] 
                                 for intent in labels)
            
            if shipping_related:
                status = "✅ CORRECT"
            else:
                status = "❌ WRONG"
                
            print(f"{status} '{query}'")
            print(f"      → Main: {main_intent}")
            print(f"      → All labels: {labels[:3]}")  # Show top 3
            print()
            
        except Exception as e:
            print(f"❌ ERROR '{query}' → {e}")
    
    print("📊 **EXPECTED CLASSIFICATION:**")
    print("   • Shipping duration queries → durasi_pengiriman")
    print("   • Shipping capability queries → pengiriman") 
    print("   • Mixed queries → both intents detected")

if __name__ == "__main__":
    test_problematic_queries() 