#!/usr/bin/env python3
"""
Simple Database Integration for Version A
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database_connector import BoysProjectDatabase
    from predict import get_responses as original_get_responses
    DATABASE_OK = True
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    DATABASE_OK = False

class VersionADB:
    def __init__(self):
        self.db = None
        if DATABASE_OK:
            self.db = BoysProjectDatabase()
            self.connected = self.db.connect()
        else:
            self.connected = False
    
    def get_enhanced_response(self, user_input):
        """Get enhanced response with database data"""
        if not self.connected:
            return original_get_responses(user_input)
        
        # Simple product search enhancement
        user_lower = user_input.lower()
        
        # Check for price inquiries
        if any(word in user_lower for word in ['harga', 'berapa', 'price']):
            products = self.db.get_all_products()
            matching = [p for p in products if any(w in user_lower for w in p['name'].lower().split())]
            
            if matching:
                product = matching[0]
                response = f"💰 **{product['name']}**\n"
                response += f"📦 Stok: {product['stock']:,} unit\n"
                response += f"⭐ Rating: {product['average_rating']}/5.0\n"
                response += f"🏆 Terjual: {product['sold']:,} unit\n\n"
                response += "📞 Info harga detail: WhatsApp 08211990442"
                return [response]
        
        # Check for stock inquiries
        elif any(word in user_lower for word in ['stok', 'stock', 'ada']):
            products = self.db.get_all_products()
            in_stock = [p for p in products if p['stock'] > 0]
            
            response = f"📦 **STOK TERSEDIA** ({len(in_stock)} produk)\n\n"
            for product in in_stock:
                response += f"✅ {product['name']} - {product['stock']:,} unit\n"
            response += "\n📞 Cek detail: WhatsApp 08211990442"
            return [response]
        
        # Check for product listing
        elif any(word in user_lower for word in ['produk', 'daftar', 'catalog']):
            products = self.db.get_all_products()
            stats = self.db.get_database_stats()
            
            response = f"📋 **KATALOG BOYS PROJECT**\n\n"
            response += f"📊 {stats['total_products']} produk • {stats['total_stock']:,} unit stock\n\n"
            
            for product in products:
                stock_icon = "✅" if product['stock'] > 0 else "⏳"
                response += f"{stock_icon} **{product['name']}**\n"
                response += f"   📦 {product['stock']:,} unit | ⭐ {product['average_rating']}/5\n"
            
            response += "\n🛒 Order: shopee.co.id/boyprojectsasli"
            return [response]
        
        # Fallback to original response
        return original_get_responses(user_input)

# Demo function
def demo():
    print("🤖 Version A + Database Integration Demo")
    print("=" * 50)
    
    vdb = VersionADB()
    print(f"Database: {'✅ Connected' if vdb.connected else '❌ Offline'}")
    
    if vdb.connected:
        test_queries = [
            "Berapa harga mounting vario?",
            "Produk apa saja yang ada?",
            "Stok mounting masih ada?",
        ]
        
        for query in test_queries:
            print(f"\n👤 {query}")
            responses = vdb.get_enhanced_response(query)
            print(f"🤖 {responses[0]}")
            print("-" * 30)

if __name__ == "__main__":
    demo() 