#!/usr/bin/env python3
"""
Boys Project Chatbot Demo
Demonstrates integration between intent classification and database responses
"""

from database_connector import BoysProjectDatabase
from intent_data import get_training_data
import random

class BoysProjectChatbot:
    """
    Simple chatbot demo for Boys Project using database integration
    """
    
    def __init__(self):
        self.db = BoysProjectDatabase()
        self.connected = False
        
        # Simple keyword-based intent mapping for demo
        self.intent_keywords = {
            'harga': ['harga', 'berapa', 'biaya', 'cost', 'price'],
            'daftar': ['daftar', 'list', 'katalog', 'produk', 'semua'],
            'stok': ['stok', 'stock', 'tersedia', 'ada'],
            'lampu': ['lampu', 'light', 'lighting', 'led'],
            'mounting': ['mounting', 'mount', 'bracket'],
            'motor': ['motor', 'bike', 'aerox', 'vario', 'nmax', 'beat'],
            'jam': ['jam', 'buka', 'tutup', 'operasional'],
            'garansi': ['garansi', 'warranty', 'jaminan'],
            'pasang': ['pasang', 'install', 'pemasangan', 'booking'],
            'kirim': ['kirim', 'ongkir', 'pengiriman', 'delivery']
        }
        
    def connect(self):
        """Connect to database"""
        self.connected = self.db.connect()
        return self.connected
    
    def disconnect(self):
        """Disconnect from database"""
        if self.connected:
            self.db.disconnect()
            self.connected = False
    
    def classify_intent(self, message):
        """
        Simple keyword-based intent classification for demo
        In production, use ML model for classification
        """
        message_lower = message.lower()
        
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return 'general'
    
    def get_response(self, user_message):
        """Get chatbot response based on user message"""
        if not self.connected:
            return "Maaf, sistem sedang tidak tersedia. Silakan coba lagi nanti."
        
        intent = self.classify_intent(user_message)
        
        if intent == 'harga':
            return self._handle_price_inquiry(user_message)
        elif intent == 'daftar':
            return self._handle_product_list()
        elif intent == 'stok':
            return self._handle_stock_inquiry(user_message)
        elif intent == 'lampu':
            return self._handle_lighting_products()
        elif intent == 'mounting':
            return self._handle_mounting_products()
        elif intent == 'motor':
            return self._handle_motor_compatibility(user_message)
        elif intent == 'jam':
            return self._handle_operating_hours()
        elif intent == 'garansi':
            return self._handle_warranty_info()
        elif intent == 'pasang':
            return self._handle_installation()
        elif intent == 'kirim':
            return self._handle_shipping()
        else:
            return self._handle_general_inquiry()
    
    def _handle_price_inquiry(self, message):
        """Handle price-related questions"""
        products = self.db.get_all_products()
        
        # Check if specific product mentioned
        message_lower = message.lower()
        matching_products = []
        
        for product in products:
            if any(word in message_lower for word in product['name'].lower().split()):
                matching_products.append(product)
        
        if matching_products:
            response = "💰 Informasi Produk:\n\n"
            for product in matching_products[:2]:
                response += f"📦 **{product['name']}**\n"
                response += f"   • Kategori: {product['category']}\n"
                response += f"   • Rating: {product['average_rating']}/5.0\n"
                response += f"   • Stok: {product['stock']} unit\n\n"
            
            response += "📞 Untuk info harga detail, hubungi:\n"
            response += "   WhatsApp: 08211990442"
        else:
            response = "💰 Untuk informasi harga produk Boys Project:\n\n"
            response += "📱 Hubungi WhatsApp: 08211990442\n"
            response += "🛒 Kunjungi: shopee.co.id/boyprojectsasli\n\n"
            response += "Produk populer kami:\n"
            
            popular = sorted(products, key=lambda x: x['sold'], reverse=True)[:2]
            for product in popular:
                response += f"• {product['name']} (Terjual: {product['sold']})\n"
        
        return response
    
    def _handle_product_list(self):
        """Handle product listing requests"""
        products = self.db.get_all_products()
        categories = self.db.get_product_categories()
        
        response = f"📋 **Katalog Boys Project** ({len(products)} produk):\n\n"
        
        for category in categories:
            category_products = self.db.get_products_by_category(category)
            response += f"🏷️ **{category}**:\n"
            
            for product in category_products:
                stock_status = "✅" if product['stock'] > 0 else "❌"
                response += f"   {stock_status} {product['name']}\n"
                response += f"      Rating: {product['average_rating']}/5.0\n"
            response += "\n"
        
        response += "🛒 Order: shopee.co.id/boyprojectsasli\n"
        response += "📞 Info: WhatsApp 08211990442"
        
        return response
    
    def _handle_stock_inquiry(self, message):
        """Handle stock-related questions"""
        products = self.db.get_all_products()
        message_lower = message.lower()
        
        # Check for specific product
        matching_products = []
        for product in products:
            if any(word in message_lower for word in product['name'].lower().split()):
                matching_products.append(product)
        
        if matching_products:
            response = "📦 **Status Stok**:\n\n"
            for product in matching_products:
                availability = "✅ Tersedia" if product['stock'] > 0 else "❌ Stok Habis"
                response += f"📱 **{product['name']}**\n"
                response += f"   Status: {availability}\n"
                response += f"   Stok: {product['stock']} unit\n"
                response += f"   Terjual: {product['sold']} unit\n\n"
        else:
            # General stock overview
            in_stock = [p for p in products if p['stock'] > 0]
            response = f"📊 **Ringkasan Stok**:\n\n"
            response += f"✅ Produk Tersedia: {len(in_stock)} item\n"
            response += f"📦 Total Stok: {sum(p['stock'] for p in products):,} unit\n\n"
            
            response += "📱 **Ready Stock**:\n"
            for product in in_stock:
                response += f"• {product['name']} ({product['stock']} unit)\n"
        
        response += "\n📞 Cek stok real-time: WhatsApp 08211990442"
        return response
    
    def _handle_lighting_products(self):
        """Handle lighting product inquiries"""
        lighting_products = self.db.get_products_by_category('Lampu')
        
        if not lighting_products:
            return "Maaf, produk lampu sedang tidak tersedia."
        
        response = "💡 **Produk Lampu Boys Project**:\n\n"
        
        for product in lighting_products:
            response += f"🔆 **{product['name']}**\n"
            response += f"   📝 {product['description']}\n"
            response += f"   📦 Stok: {product['stock']} unit\n"
            response += f"   ⭐ Rating: {product['average_rating']}/5.0\n\n"
            
            # Show available options
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail and product_detail['options']:
                response += "   🔧 **Pilihan tersedia**:\n"
                for option in product_detail['options']:
                    values = [v['display_value'] for v in option['values']]
                    response += f"      • {option['display_name']}: {', '.join(values)}\n"
                response += "\n"
        
        response += "🛒 Order: shopee.co.id/boyprojectsasli\n"
        response += "📞 Konsultasi: WhatsApp 08211990442"
        
        return response
    
    def _handle_mounting_products(self):
        """Handle mounting product inquiries"""
        mounting_products = self.db.get_products_by_category('Mounting & Body')
        
        response = "🔧 **Produk Mounting Boys Project**:\n\n"
        
        for product in mounting_products:
            response += f"🔩 **{product['name']}**\n"
            response += f"   📝 {product['description']}\n"
            response += f"   📦 Stok: {product['stock']} unit\n"
            response += f"   ⭐ Rating: {product['average_rating']}/5.0\n"
            response += f"   🏆 Terjual: {product['sold']} unit\n\n"
        
        response += "✨ **Keunggulan**:\n"
        response += "• Plug & Play installation\n"
        response += "• Presisi tinggi, tidak miring\n"
        response += "• Compatible berbagai motor\n"
        response += "• Garansi kesesuaian\n\n"
        
        response += "🛒 Order: shopee.co.id/boyprojectsasli"
        
        return response
    
    def _handle_motor_compatibility(self, message):
        """Handle motorcycle compatibility questions"""
        products = self.db.get_all_products()
        motor_types = set()
        
        # Extract motor types from product options
        for product in products:
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail:
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        for value in option['values']:
                            if value['is_available']:
                                motor_types.add(value['display_value'])
        
        response = "🏍️ **Motor yang Didukung Boys Project**:\n\n"
        
        # Categorize by brand
        yamaha_types = [m for m in motor_types if any(y in m.lower() for y in ['aerox', 'nmax', 'lexy'])]
        honda_types = [m for m in motor_types if any(h in m.lower() for h in ['vario', 'beat', 'scoopy'])]
        
        if yamaha_types:
            response += "🔵 **Yamaha**:\n"
            for motor in sorted(yamaha_types):
                response += f"   • {motor}\n"
            response += "\n"
        
        if honda_types:
            response += "🔴 **Honda**:\n"
            for motor in sorted(honda_types):
                response += f"   • {motor}\n"
            response += "\n"
        
        response += "❓ **Motor tidak ada di list?**\n"
        response += "WhatsApp: 08211990442\n"
        response += "Kami bantu cek kompatibilitas!"
        
        return response
    
    def _handle_operating_hours(self):
        """Handle operating hours inquiry"""
        return """⏰ **Jam Operasional Boys Project**:

📅 **Senin - Jumat**: 08:00 - 17:00 WIB
📅 **Sabtu - Minggu**: 10:00 - 16:00 WIB

📞 **Customer Service 24/7**:
   WhatsApp: 08211990442

🏪 **Alamat Workshop**:
   Cimahi, Bandung

💬 **Fast Response** untuk:
• Konsultasi produk
• Booking pemasangan  
• Info stok & harga"""
    
    def _handle_warranty_info(self):
        """Handle warranty information"""
        return """🛡️ **Garansi Boys Project**:

✅ **Garansi Produk**:
• Lampu: 6 bulan
• Mounting: 1 tahun
• Spare parts: 3-12 bulan

✅ **Garansi Pemasangan**:
• Workmanship: 30 hari
• Jika rusak akibat kesalahan pemasangan

📋 **Syarat Garansi**:
• Dibeli dari Boys Project resmi
• Bukan kerusakan karena pemakaian tidak wajar
• Ada bukti pembelian

📞 **Klaim Garansi**:
WhatsApp: 08211990442"""
    
    def _handle_installation(self):
        """Handle installation service inquiry"""
        return """🔧 **Layanan Pemasangan Boys Project**:

⚡ **Jenis Layanan**:
• Pemasangan lampu LED
• Pemasangan mounting
• Custom installation
• Konsultasi modifikasi

💰 **Biaya**:
• Lampu: Mulai 50rb
• Mounting: Mulai 30rb
• Paket combo: Diskon khusus

⏰ **Estimasi Waktu**:
• Lampu: 30-60 menit
• Mounting: 45-90 menit

📍 **Lokasi**:
Workshop Cimahi, Bandung

📞 **Booking**:
WhatsApp: 08211990442"""
    
    def _handle_shipping(self):
        """Handle shipping inquiry"""
        return """📦 **Pengiriman Boys Project**:

🚚 **Ekspedisi**:
• JNE (Regular & Express)
• J&T Express  
• SiCepat
• Grab/Gojek (Bandung)

⏰ **Estimasi**:
• Same day (order < 14:00)
• 1-3 hari (Pulau Jawa)
• 2-4 hari (Luar Jawa)

💰 **Ongkir**:
• Sesuai tarif ekspedisi
• Free ongkir promo berkala

📞 **Info Pengiriman**:
WhatsApp: 08211990442"""
    
    def _handle_general_inquiry(self):
        """Handle general inquiries"""
        return """👋 **Halo! Selamat datang di Boys Project**

🏍️ Spesialis sparepart motor berkualitas tinggi

📞 **Hubungi Kami**:
   WhatsApp: 08211990442

🛒 **Belanja Online**:
   shopee.co.id/boyprojectsasli

💬 **Tanya apa saja tentang**:
• Harga produk
• Stok tersedia  
• Kompatibilitas motor
• Pemasangan
• Garansi

Ketik pertanyaan Anda atau pilih topik di atas! 😊"""

def main():
    """Demo chatbot interaction"""
    print("🤖 Boys Project Chatbot Demo")
    print("=" * 50)
    
    chatbot = BoysProjectChatbot()
    
    if not chatbot.connect():
        print("❌ Cannot connect to database. Please check XAMPP MySQL is running.")
        return
    
    # Demo conversations
    demo_messages = [
        "Halo, apa saja produk yang tersedia?",
        "Berapa harga mounting aerox?", 
        "Apakah mounting vario masih ada stok?",
        "Produk lampu apa saja yang ada?",
        "Motor apa saja yang didukung?",
        "Jam buka tutupnya kapan?",
        "Bagaimana dengan garansi produk?",
    ]
    
    try:
        print("Demo conversations:")
        print("-" * 50)
        
        for i, message in enumerate(demo_messages, 1):
            print(f"\n{i}. 👤 User: {message}")
            response = chatbot.get_response(message)
            print(f"🤖 Bot: {response}")
            print("-" * 30)
    
    finally:
        chatbot.disconnect()
    
    print("\n✅ Chatbot demo completed!")
    print("\n📝 To implement:")
    print("1. Replace simple keyword matching with ML intent classification")
    print("2. Add more sophisticated NLP processing")
    print("3. Implement conversation state management")
    print("4. Add user session tracking")

if __name__ == "__main__":
    main() 