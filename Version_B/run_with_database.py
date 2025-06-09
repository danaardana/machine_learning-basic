#!/usr/bin/env python3
"""
Version B Runner with Advanced Database Integration
"""

import sys
import os

# Add parent directory for database access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database_connector import BoysProjectDatabase
    from db_integration import VersionBDB
    DATABASE_AVAILABLE = True
except ImportError:
    print("⚠️ Database integration tidak tersedia")
    # Fallback to original predict_v2
    try:
        from predict_v2 import get_enhanced_response
        DATABASE_AVAILABLE = False
    except ImportError:
        print("❌ Error loading prediction module")
        sys.exit(1)

def main():
    print("🤖 **BOYS PROJECT CHATBOT - VERSION B**")
    print("🔬 **Advanced Sub-Intent Detection + Database Integration**")
    print("=" * 65)
    
    if DATABASE_AVAILABLE:
        chatbot = VersionBDB()
        print(f"Database: {'✅ Connected' if chatbot.connected else '❌ Fallback Mode'}")
    else:
        print("Database: ❌ Static Mode")
        chatbot = None
    
    print("\nKetik 'exit' untuk keluar, 'debug' untuk mode debug")
    print("-" * 65)
    
    debug_mode = False
    
    while True:
        try:
            user_input = input("\n👤 Anda: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'keluar']:
                print("🤖 Bot: Terima kasih sudah menggunakan Boys Project Version B! 👋")
                break
            
            if user_input.lower() == 'debug':
                debug_mode = not debug_mode
                print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
                continue
            
            if not user_input:
                continue
            
            # Get response
            if DATABASE_AVAILABLE and chatbot:
                responses, labels = chatbot.get_advanced_response(user_input)
                
                if debug_mode:
                    print(f"🎯 Detected Labels: {labels}")
                
            else:
                try:
                    responses, labels = get_enhanced_response(user_input)
                    if debug_mode:
                        print(f"🎯 Detected Labels: {labels}")
                except:
                    responses = ["Sistem tidak tersedia saat ini."]
                    labels = []
            
            # Display response(s)
            for i, response in enumerate(responses, 1):
                if len(responses) > 1:
                    print(f"🤖 Bot ({i}):\n{response}")
                else:
                    print(f"🤖 Bot:\n{response}")
                    
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Sampai jumpa! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Silakan coba lagi.")

def demo_advanced_features():
    """Demo advanced features of Version B"""
    print("🔬 **VERSION B ADVANCED FEATURES DEMO**")
    print("=" * 50)
    
    if DATABASE_AVAILABLE:
        chatbot = VersionBDB()
        print(f"Database: {'✅ Connected' if chatbot.connected else '❌ Offline'}")
        
        if chatbot.connected:
            demo_queries = [
                "Berapa harga mounting vario dan bisa nego ga?",
                "Stok lampu LED untuk aerox masih ada?",
                "Motor beat bisa pake mounting yang mana?",
                "Semua produk yang ready stock dong",
                "Promo bulan ini apa aja sih?",
                "Biaya pasang mounting berapa ya?",
            ]
            
            for i, query in enumerate(demo_queries, 1):
                print(f"\n{i}. 👤 {query}")
                responses, labels = chatbot.get_advanced_response(query)
                print(f"🎯 Sub-intents: {labels}")
                print(f"🤖 {responses[0]}")
                print("-" * 50)
        else:
            print("⚠️ Database tidak tersedia untuk demo")
    else:
        print("❌ Database integration tidak tersedia")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo_advanced_features()
    else:
        main() 