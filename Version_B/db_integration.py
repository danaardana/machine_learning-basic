#!/usr/bin/env python3
"""
Simple Database Integration for Version B
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database_connector import BoysProjectDatabase
    from predict_v2 import get_enhanced_response as original_get_response
    DATABASE_OK = True
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    DATABASE_OK = False

class VersionBDB:
    def __init__(self):
        self.db = None
        if DATABASE_OK:
            self.db = BoysProjectDatabase()
            self.connected = self.db.connect()
        else:
            self.connected = False
    
    def get_advanced_response(self, user_input):
        """Get advanced response with database + sub-intent detection"""
        if not self.connected:
            try:
                return original_get_response(user_input)
            except:
                return ["Sistem tidak tersedia. Coba lagi nanti."], []
        
        user_lower = user_input.lower()
        
        # Enhanced price responses with sub-intent detection
        if any(word in user_lower for word in ['harga', 'berapa', 'price']):
            products = self.db.get_all_products()
            
            # Check for specific product mentions
            matching = []
            for product in products:
                if any(w in user_lower for w in product['name'].lower().split()):
                    matching.append(product)
            
            if matching:
                response = "💰 **HARGA PRODUK SPESIFIK**\n\n"
                for product in matching[:2]:
                    response += f"📦 **{product['name']}**\n"
                    response += f"   📊 Stok: {product['stock']:,} unit\n"
                    response += f"   ⭐ Rating: {product['average_rating']}/5.0\n"
                    response += f"   🏆 Terjual: {product['sold']:,} unit\n"
                    
                    # Get product options for detailed pricing
                    detail = self.db.get_product_with_options(product['id'])
                    if 'options' in detail and detail['options']:
                        response += f"   🔧 **Varian tersedia:**\n"
                        for option in detail['options']:
                            values = [v['display_value'] for v in option['values'][:3]]
                            response += f"      • {option['display_name']}: {', '.join(values)}\n"
                    response += "\n"
                
                response += "📞 **Nego harga:** WhatsApp 08211990442"
                return [response], ["harga_harga_produk"]
            
            # Check for promo inquiries
            elif any(word in user_lower for word in ['promo', 'diskon', 'murah']):
                popular = sorted(products, key=lambda x: x['sold'], reverse=True)[:2]
                response = "🎉 **PROMO & DISKON TERKINI**\n\n"
                response += "🔥 **Flash Sale Products:**\n"
                for product in popular:
                    response += f"   • {product['name']} - {product['sold']:,} terjual\n"
                response += "\n💰 **Promo Berlaku:**\n"
                response += "   • Bundling discount 15%\n"
                response += "   • Member exclusive 10%\n"
                response += "📱 Follow IG @boyprojects untuk update!"
                return [response], ["harga_harga_promo"]
        
        # Enhanced stock responses
        elif any(word in user_lower for word in ['stok', 'stock', 'ada', 'tersedia']):
            products = self.db.get_all_products()
            
            # Check for specific product stock
            matching = [p for p in products if any(w in user_lower for w in p['name'].lower().split())]
            
            if matching:
                response = "✅ **STATUS STOK PRODUK**\n\n"
                for product in matching:
                    status = "Ready Stock" if product['stock'] > 0 else "Perlu Restock"
                    icon = "✅" if product['stock'] > 0 else "⏳"
                    
                    response += f"{icon} **{product['name']}**\n"
                    response += f"   📊 Stok: {product['stock']:,} unit\n"
                    response += f"   🎯 Status: {status}\n"
                    response += f"   📈 Terjual: {product['sold']:,} unit\n\n"
                
                return [response], ["stok_produk_stok_tersedia"]
            
            # General stock overview
            else:
                in_stock = [p for p in products if p['stock'] > 0]
                response = f"📊 **OVERVIEW STOK READY**\n\n"
                response += f"✅ **Produk Tersedia:** {len(in_stock)} item\n\n"
                for product in in_stock:
                    response += f"   • {product['name']} ({product['stock']:,} unit)\n"
                
                response += "\n📞 **Update real-time:** WhatsApp 08211990442"
                return [response], ["stok_produk_stok_tersedia"]
        
        # Enhanced product listing
        elif any(word in user_lower for word in ['produk', 'daftar', 'catalog', 'list']):
            products = self.db.get_all_products()
            categories = self.db.get_product_categories()
            stats = self.db.get_database_stats()
            
            response = f"📋 **COMPLETE CATALOG BOYS PROJECT**\n\n"
            response += f"📊 **Overview:** {stats['total_products']} produk • {stats['total_stock']:,} unit\n\n"
            
            for category in categories:
                cat_products = self.db.get_products_by_category(category)
                response += f"🏷️ **{category}** ({len(cat_products)} item):\n"
                
                for product in cat_products:
                    stock_icon = "✅" if product['stock'] > 0 else "⏳"
                    popularity = "🔥" if product['sold'] > 1000 else ""
                    
                    response += f"   {stock_icon} **{product['name']}** {popularity}\n"
                    response += f"      📦 {product['stock']:,} unit | ⭐ {product['average_rating']}/5\n"
                response += "\n"
            
            response += "🛒 **Order:** shopee.co.id/boyprojectsasli"
            return [response], ["daftar"]
        
        # Motor compatibility check
        elif any(word in user_lower for word in ['motor', 'cocok', 'support', 'bisa']):
            products = self.db.get_all_products()
            motor_types = set()
            
            for product in products:
                detail = self.db.get_product_with_options(product['id'])
                if 'options' in detail:
                    for option in detail['options']:
                        if 'motor' in option['option_name'].lower():
                            for value in option['values']:
                                if value['is_available']:
                                    motor_types.add(value['display_value'])
            
            response = "🏍️ **MOTOR COMPATIBILITY**\n\n"
            yamaha = [m for m in motor_types if 'yamaha' in m.lower() or any(y in m.lower() for y in ['aerox', 'nmax', 'lexi'])]
            honda = [m for m in motor_types if 'honda' in m.lower() or any(h in m.lower() for h in ['vario', 'beat', 'scoopy'])]
            
            if yamaha:
                response += "🔵 **YAMAHA:**\n"
                for motor in sorted(yamaha):
                    response += f"   ✅ {motor}\n"
                response += "\n"
            
            if honda:
                response += "🔴 **HONDA:**\n"
                for motor in sorted(honda):
                    response += f"   ✅ {motor}\n"
                response += "\n"
            
            response += f"📊 **Total:** {len(motor_types)} tipe motor didukung\n"
            response += "❓ **Cek spesifik:** WhatsApp 08211990442"
            
            return [response], ["tipe_motor_matic"]
        
        # Fallback to original Version B response
        try:
            return original_get_response(user_input)
        except:
            return ["Sistem sedang maintenance. Hubungi WhatsApp 08211990442"], ["general"]

# Demo function
def demo():
    print("🤖 Version B + Advanced Database Integration Demo")
    print("=" * 60)
    
    vdb = VersionBDB()
    print(f"Database: {'✅ Connected' if vdb.connected else '❌ Offline'}")
    
    if vdb.connected:
        test_queries = [
            "Berapa harga mounting vario dan bisa nego?",
            "Stok lampu LED masih ada?",
            "Motor beat bisa pake mounting apa?",
            "Semua produk yang ready stock",
            "Promo bulan ini apa aja?",
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. 👤 {query}")
            responses, labels = vdb.get_advanced_response(query)
            print(f"🎯 Labels: {labels}")
            print(f"🤖 {responses[0]}")
            print("-" * 40)

if __name__ == "__main__":
    demo() 