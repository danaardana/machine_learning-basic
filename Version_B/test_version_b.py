#!/usr/bin/env python3
"""
Simple test script for Version B sub-intent detection system
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the prediction function
from predict_v2 import get_enhanced_response

def test_version_b():
    """Test Version B with sample queries"""
    print("🧪 TESTING VERSION B - SUB-INTENT DETECTION")
    print("="*60)
    
    test_cases = [
        "Berapa harga mounting carbon dan ada promo gak?",
        "Lampu LED projector untuk Beat masih ada stok?", 
        "Body kit Aerox ready stock berapa harga?",
        "Biaya pasang lampu DRL di rumah weekend berapa ya?",
        "Mounting phone holder waterproof harga grosir berapa?"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case}")
        print("-" * 50)
        
        try:
            responses, labels = get_enhanced_response(test_case)
            print(f"🏷️  Detected Labels: {labels}")
            print("💬 Bot Responses:")
            for j, response in enumerate(responses, 1):
                # Truncate long responses for readability
                truncated = response[:80] + "..." if len(response) > 80 else response
                print(f"   {j}. {truncated}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    test_version_b() 