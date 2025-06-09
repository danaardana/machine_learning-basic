#!/usr/bin/env python3
"""
Version A Runner with Database Integration
"""

import sys
import os

# Add parent directory for database access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database_connector import BoysProjectDatabase
    from db_integration import VersionADB
    DATABASE_AVAILABLE = True
except ImportError:
    print("⚠️ Database integration tidak tersedia")
    # Fallback to original predict
    try:
        from predict import get_responses
        DATABASE_AVAILABLE = False
    except ImportError:
        print("❌ Error loading prediction module")
        sys.exit(1)

def main():
    print("🤖 **BOYS PROJECT CHATBOT - VERSION A**")
    print("=" * 50)
    
    if DATABASE_AVAILABLE:
        chatbot = VersionADB()
        print(f"Database: {'✅ Connected' if chatbot.connected else '❌ Fallback Mode'}")
    else:
        print("Database: ❌ Static Mode")
        chatbot = None
    
    print("\nKetik 'exit' untuk keluar")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n👤 Anda: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'keluar']:
                print("🤖 Bot: Terima kasih sudah mengunjungi Boys Project! 👋")
                break
            
            if not user_input:
                continue
            
            # Get response
            if DATABASE_AVAILABLE and chatbot:
                responses = chatbot.get_enhanced_response(user_input)
            else:
                responses = get_responses(user_input)
            
            # Display response(s)
            for i, response in enumerate(responses, 1):
                if len(responses) > 1:
                    print(f"🤖 Bot ({i}): {response}")
                else:
                    print(f"🤖 Bot: {response}")
                    
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Sampai jumpa! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Silakan coba lagi.")

if __name__ == "__main__":
    main() 