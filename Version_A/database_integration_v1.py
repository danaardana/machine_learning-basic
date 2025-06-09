#!/usr/bin/env python3
"""
Database Integration for Version A
Connects the existing Version A chatbot with Boys Project MySQL database
"""

import sys
import os
# Add parent directory to access database_connector
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_connector import BoysProjectDatabase
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class VersionADatabaseIntegrator:
    """
    Database integration for Version A chatbot
    Enhances existing responses with real product data
    """
    
    def __init__(self):
        self.db = BoysProjectDatabase()
        self.connected = False
        
        # Load existing model
        try:
            self.model = joblib.load('../ml_model/chat_model.pkl')
            self.vectorizer = joblib.load('../ml_model/vectorizer.pkl')
            print("✅ Version A ML models loaded successfully!")
        except FileNotFoundError:
            print("❌ ML models not found. Please train the model first.")
            self.model = None
            self.vectorizer = None
    
    def connect_database(self):
        """Connect to database"""
        self.connected = self.db.connect()
        return self.connected
    
    def disconnect_database(self):
        """Disconnect from database"""
        if self.connected:
            self.db.disconnect()
            self.connected = False
    
    def predict_intent(self, user_input):
        """Predict intent using existing Version A model"""
        if not self.model or not self.vectorizer:
            return "general"
        
        X = self.vectorizer.transform([user_input])
        intent = self.model.predict(X)[0]
        return intent
    
    def get_enhanced_response(self, user_input):
        """Get enhanced response with database data"""
        if not self.connected:
            return "Maaf, sistem sedang tidak tersedia. Silakan coba lagi nanti."
        
        # Get intent from existing model
        intent = self.predict_intent(user_input)
        print(f"🎯 Detected Intent: {intent}")
        
        # Generate response based on intent with database data
        if intent == 'harga':
            return self._handle_harga_intent(user_input)
        elif intent == 'daftar':
            return self._handle_daftar_intent()
        elif intent == 'stok_produk':
            return self._handle_stok_produk_intent(user_input)
        elif intent == 'kategori_mounting_body':
            return self._handle_mounting_intent()
        elif intent == 'kategori_lighting':
            return self._handle_lighting_intent()
        elif intent == 'tipe_motor_matic':
            return self._handle_motor_compatibility()
        elif intent == 'jam_operasional':
            return self._handle_jam_operasional()
        elif intent == 'garansi':
            return self._handle_garansi()
        elif intent == 'booking_pemasangan':
            return self._handle_booking_pemasangan()
        elif intent == 'pengiriman':
            return self._handle_pengiriman()
        elif intent == 'durasi_pengiriman':
            return self._handle_durasi_pengiriman()
        elif intent == 'wilayah_pemasangan':
            return self._handle_wilayah_pemasangan()
        elif intent == 'layanan_instalasi':
            return self._handle_layanan_instalasi()
        else:
            return self._handle_general_inquiry()
    
    def _handle_harga_intent(self, user_input):
        """Handle price inquiry with real product data"""
        products = self.db.get_all_products()
        
        # Check for specific product mentions
        user_lower = user_input.lower()
        matching_products = []
        
        for product in products:
            product_words = product['name'].lower().split()
            if any(word in user_lower for word in product_words):
                matching_products.append(product)
        
        if matching_products:
            response = "💰 **INFORMASI HARGA PRODUK**\n\n"
            for product in matching_products[:2]:  # Limit to 2 products
                response += f"📦 **{product['name']}**\n"
                response += f"   • Kategori: {product['category']}\n"
                response += f"   • Stok: {product['stock']:,} unit\n"
                response += f"   • Rating: {product['average_rating']}/5.0 ({product['ratings']} reviews)\n"
                response += f"   • Terjual: {product['sold']:,} unit\n"
                
                # Get product options for detailed info
                product_detail = self.db.get_product_with_options(product['id'])
                if 'options' in product_detail and product_detail['options']:
                    response += f"   • Pilihan: "
                    option_info = []
                    for option in product_detail['options']:
                        values = [v['display_value'] for v in option['values'][:3]]  # Show first 3 values
                        option_info.append(f"{option['display_name']} ({', '.join(values)})")
                    response += "; ".join(option_info) + "\n"
                response += "\n"
            
            response += "📞 **Info harga detail & nego:**\n"
            response += "   WhatsApp: 08211990442\n"
            response += "🛒 **Order langsung:** shopee.co.id/boyprojectsasli"
        else:
            # General price response with popular products
            popular_products = sorted(products, key=lambda x: x['sold'], reverse=True)[:2]
            response = "💰 **HARGA & PAKET BOYS PROJECT**\n\n"
            response += "🔥 **Produk Terpopuler:**\n"
            for product in popular_products:
                response += f"   • {product['name']} - Terjual: {product['sold']:,} unit\n"
            
            response += "\n💳 **Pilihan Pembayaran:**\n"
            response += "   • Transfer Bank • COD Bandung-Cimahi\n"
            response += "   • Shopee/Tokopedia • Cicilan 0%\n\n"
            response += "🎁 **Promo Terkini:**\n"
            response += "   • Paket bundling diskon 15%\n"
            response += "   • Member discount 10%\n"
            response += "   • Free ongkir Bandung-Cimahi\n\n"
            response += "📞 Nego harga: WhatsApp 08211990442"
        
        return response
    
    def _handle_daftar_intent(self):
        """Handle product listing with real database data"""
        products = self.db.get_all_products()
        categories = self.db.get_product_categories()
        stats = self.db.get_database_stats()
        
        response = f"📋 **KATALOG BOYS PROJECT** ({stats['total_products']} produk)\n\n"
        
        for category in categories:
            category_products = self.db.get_products_by_category(category)
            response += f"🏷️ **{category.upper()}** ({len(category_products)} item):\n"
            
            for product in category_products:
                stock_icon = "✅" if product['stock'] > 0 else "⏳"
                response += f"   {stock_icon} **{product['name']}**\n"
                response += f"      📊 Stok: {product['stock']:,} | Terjual: {product['sold']:,}\n"
                response += f"      ⭐ Rating: {product['average_rating']}/5.0\n"
                response += f"      📝 {product['description'][:80]}...\n\n"
        
        response += f"📊 **Statistik Toko:**\n"
        response += f"   • Total Stok: {stats['total_stock']:,} unit\n"
        response += f"   • Total Terjual: {stats['total_sold']:,} unit\n"
        response += f"   • Varian Produk: {stats['total_option_values']} pilihan\n\n"
        response += "🛒 **Belanja Online:** shopee.co.id/boyprojectsasli\n"
        response += "📞 **Konsultasi:** WhatsApp 08211990442"
        
        return response
    
    def _handle_stok_produk_intent(self, user_input):
        """Handle stock inquiry with real data"""
        user_lower = user_input.lower()
        products = self.db.get_all_products()
        
        # Find mentioned products
        matching_products = []
        for product in products:
            if any(word in user_lower for word in product['name'].lower().split()):
                matching_products.append(product)
        
        if matching_products:
            response = "📦 **STATUS STOK PRODUK**\n\n"
            for product in matching_products:
                stock_info = self.db.get_stock_info(product['id'])
                availability = "✅ Ready Stock" if product['stock'] > 0 else "⏳ Perlu Restock"
                
                response += f"📱 **{product['name']}**\n"
                response += f"   📊 Stok: {stock_info['stock']:,} unit\n"
                response += f"   🎯 Status: {availability}\n"
                response += f"   📈 Terjual: {stock_info['sold']:,} unit\n"
                response += f"   ⭐ Rating: {stock_info['average_rating']}/5.0\n"
                
                if product['stock'] > 0:
                    response += f"   🚀 Siap kirim today!\n"
                else:
                    response += f"   ⏰ Restock 2-3 hari kerja\n"
                response += "\n"
        else:
            # General stock overview
            in_stock = [p for p in products if p['stock'] > 0]
            low_stock = [p for p in products if p['stock'] < 100 and p['stock'] > 0]
            
            response = "📊 **RINGKASAN STOK BOYS PROJECT**\n\n"
            response += f"✅ **Ready Stock:** {len(in_stock)} produk\n"
            if low_stock:
                response += f"⚠️ **Stok Terbatas:** {len(low_stock)} produk\n"
            
            response += "\n📦 **Produk Ready Stock:**\n"
            for product in in_stock:
                response += f"   • {product['name']} ({product['stock']:,} unit)\n"
            
            if low_stock:
                response += "\n⚠️ **Stok Terbatas (buruan!):**\n"
                for product in low_stock:
                    response += f"   • {product['name']} ({product['stock']} unit)\n"
        
        response += "\n📞 **Cek stok real-time:** WhatsApp 08211990442\n"
        response += "🔔 **Notifikasi restock:** Follow IG @boyprojects"
        
        return response
    
    def _handle_mounting_intent(self):
        """Handle mounting products with database data"""
        mounting_products = self.db.get_products_by_category('Mounting & Body')
        
        response = "🔧 **KATEGORI: MOUNTING & BODY**\n\n"
        
        for product in mounting_products:
            response += f"🏍️ **{product['name']}**\n"
            response += f"   📝 {product['description']}\n"
            response += f"   📦 Stok: {product['stock']:,} unit\n"
            response += f"   ⭐ Rating: {product['average_rating']}/5.0 ({product['ratings']} reviews)\n"
            response += f"   🏆 Terjual: {product['sold']:,} unit\n"
            
            # Show compatibility info
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail and product_detail['options']:
                response += f"   🏍️ **Kompatibilitas:**\n"
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        motor_values = [v['display_value'] for v in option['values'] if v['is_available']]
                        response += f"      • {', '.join(motor_values[:5])}"
                        if len(motor_values) > 5:
                            response += f" + {len(motor_values)-5} lainnya"
                        response += "\n"
                    elif 'size' in option['option_name'].lower():
                        size_values = [v['display_value'] for v in option['values'] if v['is_available']]
                        response += f"      • Ukuran: {', '.join(size_values)}\n"
            response += "\n"
        
        response += "✨ **Keunggulan Mounting Boys Project:**\n"
        response += "   • Plug & Play installation\n"
        response += "   • Presisi tinggi, tidak miring\n"
        response += "   • Material berkualitas tinggi\n"
        response += "   • Garansi kesesuaian\n\n"
        response += "🛒 **Order:** shopee.co.id/boyprojectsasli\n"
        response += "📞 **Konsultasi:** WhatsApp 08211990442"
        
        return response
    
    def _handle_lighting_intent(self):
        """Handle lighting products with database data"""
        lighting_products = self.db.get_products_by_category('Lampu')
        
        response = "💡 **KATEGORI: LIGHTING**\n\n"
        
        for product in lighting_products:
            response += f"🔆 **{product['name']}**\n"
            response += f"   📝 {product['description']}\n"
            response += f"   📦 Stok: {product['stock']:,} unit\n"
            response += f"   ⭐ Rating: {product['average_rating']}/5.0\n"
            
            # Show product options
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail and product_detail['options']:
                response += f"   🔧 **Pilihan:**\n"
                for option in product_detail['options']:
                    values = [v['display_value'] for v in option['values'] if v['is_available']]
                    response += f"      • {option['display_name']}: {', '.join(values)}\n"
            response += "\n"
        
        response += "⚡ **Keunggulan Lampu Boys Project:**\n"
        response += "   • LED berkualitas tinggi\n"
        response += "   • Hemat listrik aki motor\n"
        response += "   • Plug & Play installation\n"
        response += "   • Waterproof & tahan lama\n"
        response += "   • Garansi produk\n\n"
        response += "🛒 **Order:** shopee.co.id/boyprojectsasli\n"
        response += "📞 **Konsultasi:** WhatsApp 08211990442"
        
        return response
    
    def _handle_motor_compatibility(self):
        """Handle motor compatibility with database data"""
        products = self.db.get_all_products()
        motor_types = set()
        
        # Extract motor types from database
        for product in products:
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail:
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        for value in option['values']:
                            if value['is_available']:
                                motor_types.add(value['display_value'])
        
        # Categorize by brand
        yamaha_motors = [m for m in motor_types if any(y in m.lower() for y in ['aerox', 'nmax', 'lexi', 'mio', 'jupiter'])]
        honda_motors = [m for m in motor_types if any(h in m.lower() for h in ['vario', 'beat', 'scoopy', 'pcx'])]
        other_motors = [m for m in motor_types if m not in yamaha_motors + honda_motors]
        
        response = "🏍️ **MOTOR SUPPORT BOYS PROJECT**\n\n"
        
        if yamaha_motors:
            response += "🔵 **YAMAHA:**\n"
            for motor in sorted(yamaha_motors):
                response += f"   ✅ {motor}\n"
            response += "\n"
        
        if honda_motors:
            response += "🔴 **HONDA:**\n"
            for motor in sorted(honda_motors):
                response += f"   ✅ {motor}\n"
            response += "\n"
        
        if other_motors:
            response += "⚪ **BRAND LAIN:**\n"
            for motor in sorted(other_motors):
                response += f"   ✅ {motor}\n"
            response += "\n"
        
        # Add product-specific compatibility
        mounting_products = self.db.get_products_by_category('Mounting & Body')
        if mounting_products:
            response += f"📊 **STATISTIK KOMPATIBILITAS:**\n"
            response += f"   • {len(motor_types)} tipe motor didukung\n"
            response += f"   • {len(mounting_products)} produk mounting tersedia\n"
            response += f"   • Tingkat kompatibilitas: 95%+\n\n"
        
        response += "❓ **Motor tidak ada di list?**\n"
        response += "   WhatsApp: 08211990442\n"
        response += "   Kami bantu cek kompatibilitas motor Anda!\n\n"
        response += "🔧 **Custom Fitting:**\n"
        response += "   Tersedia untuk motor langka/modif"
        
        return response
    
    def _handle_jam_operasional(self):
        """Handle operating hours - use static data"""
        return """⏰ **JAM OPERASIONAL BOYS PROJECT**

📅 **JADWAL BUKA:**
   • Senin - Jumat: 08:00 - 17:00 WIB
   • Sabtu - Minggu: 10:00 - 16:00 WIB

📞 **CUSTOMER SERVICE:**
   • WhatsApp: 08211990442 (24/7 response)
   • Fast response: 09:00 - 17:00 WIB

🏪 **WORKSHOP & TOKO:**
   • Alamat: Cimahi, Bandung
   • Pemasangan: Sesuai jam operasional
   • Home service: By appointment

🎯 **FAST RESPONSE:**
   • Order & konsultasi via WhatsApp
   • Cek stok real-time
   • Booking pemasangan"""
    
    def _handle_garansi(self):
        """Handle warranty info"""
        return """🛡️ **GARANSI BOYS PROJECT**

✅ **GARANSI PRODUK:**
   • Mounting: 1 tahun garansi
   • Lampu LED: 6 bulan garansi
   • Body kit: 6 bulan garansi

✅ **GARANSI PEMASANGAN:**
   • Workmanship: 30 hari
   • Hasil kerja teknisi dijamin

📋 **SYARAT GARANSI:**
   • Produk dibeli dari Boys Project resmi
   • Kerusakan bukan akibat pemakaian tidak wajar
   • Menyertakan bukti pembelian

📞 **KLAIM GARANSI:**
   WhatsApp: 08211990442

📍 **SERVICE CENTER:**
   Workshop Cimahi, Bandung"""
    
    def _handle_booking_pemasangan(self):
        """Handle installation booking"""
        return """📅 **BOOKING PEMASANGAN BOYS PROJECT**

🔧 **LAYANAN PEMASANGAN:**
   • Mounting installation
   • Lampu LED setup
   • Body kit fitting
   • Custom modification

⏰ **JAM PEMASANGAN:**
   • Senin - Jumat: 08:00 - 17:00
   • Sabtu - Minggu: 10:00 - 16:00

📞 **CARA BOOKING:**
   1. WhatsApp: 08211990442
   2. Sebutkan: jenis produk + tipe motor
   3. Pilih waktu appointment
   4. Konfirmasi kedatangan

💰 **BIAYA INSTALASI:**
   • Mounting: Rp 50,000
   • Lampu: Rp 75,000
   • Body kit: Rp 100,000
   • Home service: +Rp 30,000

📍 **LOKASI:**
   Workshop Cimahi, Bandung"""
    
    def _handle_pengiriman(self):
        """Handle shipping info"""
        return """📦 **PENGIRIMAN BOYS PROJECT**

🚚 **EKSPEDISI PARTNER:**
   • JNE (Regular & Express)
   • J&T Express
   • SiCepat
   • Grab/Gojek (Bandung area)

💰 **ONGKOS KIRIM:**
   • Bandung-Cimahi: GRATIS
   • Luar kota: Sesuai tarif ekspedisi
   • Same day delivery: +Rp 10,000

📦 **PACKAGING:**
   • Bubble wrap + kardus tebal
   • Packing aman untuk spare parts
   • Include manual pemasangan

⏰ **PROCESSING TIME:**
   • Same day (order < 14:00 WIB)
   • H+1 (order > 14:00 WIB)

🛒 **ORDER:**
   WhatsApp: 08211990442
   Shopee: shopee.co.id/boyprojectsasli"""
    
    def _handle_durasi_pengiriman(self):
        """Handle shipping duration"""
        return """⏱️ **DURASI PENGIRIMAN BOYS PROJECT**

🏃‍♂️ **SAME DAY (BANDUNG-CIMAHI):**
   • Grab/Gojek: 1-2 jam
   • Kurir toko: 2-4 jam

🚚 **PULAU JAWA:**
   • JNE REG: 1-2 hari
   • JNE YES: 1 hari
   • J&T Express: 1-2 hari
   • SiCepat: 1-2 hari

🛫 **LUAR PULAU JAWA:**
   • JNE REG: 2-4 hari
   • JNE YES: 1-2 hari
   • Tergantung akses wilayah

⚡ **EXPRESS SERVICE:**
   • Overnight delivery available
   • Premium shipping +50% tarif

📞 **TRACKING INFO:**
   WhatsApp: 08211990442"""
    
    def _handle_wilayah_pemasangan(self):
        """Handle installation area coverage"""
        return """📍 **WILAYAH PEMASANGAN BOYS PROJECT**

🏪 **WORKSHOP UTAMA:**
   • Alamat: Cimahi, Bandung
   • Fasilitas: Tools lengkap + parking luas

🏍️ **HOME SERVICE AREA:**
   • Bandung Raya
   • Cimahi & sekitarnya
   • Minimum order berlaku

🤝 **COVERAGE AREA:**
   • Bandung Timur/Barat/Selatan/Utara
   • Cimahi Utara/Selatan
   • Margahayu, Katapang, Soreang
   • Lembang, Parongpong

💰 **BIAYA HOME SERVICE:**
   • Dalam kota: +Rp 30,000
   • Luar kota: Nego via WhatsApp

📞 **BOOKING HOME SERVICE:**
   WhatsApp: 08211990442"""
    
    def _handle_layanan_instalasi(self):
        """Handle installation service info"""
        return """🔧 **LAYANAN INSTALASI BOYS PROJECT**

⚡ **JENIS LAYANAN:**
   • Mounting installation
   • LED lighting setup
   • Body kit fitting
   • Custom modification
   • Troubleshooting

👨‍🔧 **KEUNGGULAN TIM:**
   • Teknisi berpengalaman 5+ tahun
   • Spesialisasi motor matic
   • Tools professional lengkap
   • Garansi hasil kerja

💰 **TARIF INSTALASI:**
   • Mounting: Rp 50,000
   • Lampu LED: Rp 75,000
   • Body kit: Rp 100,000
   • Custom work: Nego

⏰ **ESTIMASI WAKTU:**
   • Mounting: 45-90 menit
   • Lampu: 30-60 menit
   • Body kit: 1-2 jam

📍 **LOKASI SERVICE:**
   • Workshop: Cimahi, Bandung
   • Home service: Area Bandung Raya

📞 **BOOKING:**
   WhatsApp: 08211990442"""
    
    def _handle_general_inquiry(self):
        """Handle general inquiries"""
        stats = self.db.get_database_stats() if self.connected else {}
        
        response = "👋 **SELAMAT DATANG DI BOYS PROJECT**\n\n"
        response += "🏍️ **SPESIALIS SPAREPART MOTOR MATIC**\n"
        response += "   • Mounting & Body Kit\n"
        response += "   • LED Lighting System\n"
        response += "   • Custom Modification\n\n"
        
        if stats:
            response += f"📊 **STATS TOKO:**\n"
            response += f"   • {stats.get('total_products', 0)} produk tersedia\n"
            response += f"   • {stats.get('total_stock', 0):,} unit stock\n"
            response += f"   • {stats.get('total_sold', 0):,} unit terjual\n\n"
        
        response += "📞 **HUBUNGI KAMI:**\n"
        response += "   • WhatsApp: 08211990442\n"
        response += "   • IG: @boyprojects\n"
        response += "   • Shopee: shopee.co.id/boyprojectsasli\n\n"
        response += "💬 **TANYA TENTANG:**\n"
        response += "   • Harga & promo\n"
        response += "   • Stok produk\n"
        response += "   • Kompatibilitas motor\n"
        response += "   • Booking pemasangan"
        
        return response

def main():
    """Demo Version A with database integration"""
    print("🤖 VERSION A - DATABASE INTEGRATION DEMO")
    print("=" * 60)
    
    integrator = VersionADatabaseIntegrator()
    
    if not integrator.connect_database():
        print("❌ Cannot connect to database. Please check XAMPP MySQL.")
        return
    
    try:
        # Demo conversations
        demo_queries = [
            "Berapa harga mounting vario?",
            "Produk apa saja yang tersedia?", 
            "Apakah mounting aerox masih ada stok?",
            "Motor apa saja yang didukung?",
            "Jam buka tutup kapan?",
        ]
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n{i}. 👤 User: {query}")
            response = integrator.get_enhanced_response(query)
            print(f"🤖 Bot: {response}")
            print("-" * 40)
    
    finally:
        integrator.disconnect_database()
    
    print("\n✅ Version A Database Integration Demo Complete!")

if __name__ == "__main__":
    main() 