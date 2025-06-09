#!/usr/bin/env python3
"""
ML Model Database Integration for Boys Project
This module integrates intent classification with real product database queries
"""

from database_connector import BoysProjectDatabase
from intent_data import get_training_data
from typing import Dict, List, Optional
import random

class MLDatabaseIntegration:
    """
    Integration class that combines ML intent classification with database queries
    to provide real product information responses
    """
    
    def __init__(self):
        self.db = BoysProjectDatabase()
        self.intent_responses = {
            'harga': self._handle_harga_intent,
            'daftar': self._handle_daftar_intent,
            'kategori_lighting': self._handle_kategori_lighting_intent,
            'kategori_mounting_body': self._handle_kategori_mounting_body_intent,
            'stok_produk': self._handle_stok_produk_intent,
            'jam_operasional': self._handle_jam_operasional_intent,
            'garansi': self._handle_garansi_intent,
            'booking_pemasangan': self._handle_booking_pemasangan_intent,
            'pengiriman': self._handle_pengiriman_intent,
            'durasi_pengiriman': self._handle_durasi_pengiriman_intent,
            'wilayah_pemasangan': self._handle_wilayah_pemasangan_intent,
            'tipe_motor_matic': self._handle_tipe_motor_matic_intent,
            'layanan_instalasi': self._handle_layanan_instalasi_intent
        }
    
    def connect_database(self) -> bool:
        """Connect to the database"""
        return self.db.connect()
    
    def disconnect_database(self):
        """Disconnect from the database"""
        self.db.disconnect()
    
    def get_intent_response(self, intent: str, user_message: str = "") -> str:
        """
        Get appropriate response based on classified intent
        
        Args:
            intent: Classified intent from ML model
            user_message: Original user message for context
            
        Returns:
            Response string with real data from database
        """
        if intent in self.intent_responses:
            return self.intent_responses[intent](user_message)
        else:
            return "Maaf, saya belum bisa memahami pertanyaan Anda. Bisa diulang dengan kata lain?"
    
    def _handle_harga_intent(self, user_message: str) -> str:
        """Handle price-related inquiries"""
        products = self.db.get_all_products()
        if not products:
            return "Maaf, data produk sedang tidak tersedia. Silakan hubungi admin."
        
        # Check if user mentions specific product
        user_lower = user_message.lower()
        matching_products = []
        
        for product in products:
            if any(word in user_lower for word in product['name'].lower().split()):
                matching_products.append(product)
        
        if matching_products:
            response = "💰 Informasi Harga Produk:\n"
            for product in matching_products[:3]:  # Limit to 3 products
                response += f"\n📦 {product['name']}\n"
                response += f"   Kategori: {product['category']}\n"
                response += f"   Rating: {product['average_rating']}/5.0 ({product['ratings']} review)\n"
                response += f"   Stok: {product['stock']} unit\n"
                if product['description']:
                    response += f"   Deskripsi: {product['description'][:100]}...\n"
            
            response += f"\n📞 Untuk info harga detail, hubungi WhatsApp: 08211990442"
            return response
        else:
            # Show popular products
            popular_products = sorted(products, key=lambda x: x['sold'], reverse=True)[:3]
            response = "💰 Produk Terpopuler Kami:\n"
            for product in popular_products:
                response += f"\n📦 {product['name']}\n"
                response += f"   Kategori: {product['category']}\n"
                response += f"   Rating: {product['average_rating']}/5.0\n"
                response += f"   Terjual: {product['sold']} unit\n"
            
            response += f"\n📞 Untuk info harga lengkap, hubungi WhatsApp: 08211990442"
            return response
    
    def _handle_daftar_intent(self, user_message: str) -> str:
        """Handle product listing inquiries"""
        products = self.db.get_all_products()
        categories = self.db.get_product_categories()
        
        if not products:
            return "Maaf, data produk sedang tidak tersedia."
        
        response = f"📋 Daftar Produk Boys Project ({len(products)} produk):\n"
        
        # Group by category
        for category in categories:
            category_products = self.db.get_products_by_category(category)
            if category_products:
                response += f"\n🏷️ {category}:\n"
                for product in category_products:
                    stock_status = "✅ Tersedia" if product['stock'] > 0 else "❌ Stok Habis"
                    response += f"   • {product['name']} - {stock_status}\n"
        
        response += f"\n🛒 Lihat koleksi lengkap: shopee.co.id/boyprojectsasli"
        response += f"\n📞 Info lebih lanjut: WhatsApp 08211990442"
        
        return response
    
    def _handle_kategori_lighting_intent(self, user_message: str) -> str:
        """Handle lighting category inquiries"""
        lighting_products = self.db.get_products_by_category('Lampu')
        
        if not lighting_products:
            return "Maaf, produk lampu sedang tidak tersedia."
        
        response = "💡 Kategori Lampu Boys Project:\n"
        
        for product in lighting_products:
            response += f"\n🔆 {product['name']}\n"
            response += f"   📝 {product['description']}\n"
            response += f"   📦 Stok: {product['stock']} unit\n"
            response += f"   ⭐ Rating: {product['average_rating']}/5.0\n"
            
            # Get product options
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail and product_detail['options']:
                response += f"   🔧 Opsi tersedia:\n"
                for option in product_detail['options']:
                    response += f"      • {option['display_name']}: "
                    values = [v['display_value'] for v in option['values']]
                    response += ', '.join(values) + "\n"
        
        response += f"\n🛒 Order: shopee.co.id/boyprojectsasli"
        return response
    
    def _handle_kategori_mounting_body_intent(self, user_message: str) -> str:
        """Handle mounting & body category inquiries"""
        mounting_products = self.db.get_products_by_category('Mounting & Body')
        
        if not mounting_products:
            return "Maaf, produk mounting sedang tidak tersedia."
        
        response = "🔧 Kategori Mounting & Body Boys Project:\n"
        
        for product in mounting_products:
            response += f"\n🔩 {product['name']}\n"
            response += f"   📝 {product['description']}\n"
            response += f"   📦 Stok: {product['stock']} unit\n"
            response += f"   ⭐ Rating: {product['average_rating']}/5.0\n"
            response += f"   🏆 Terjual: {product['sold']} unit\n"
            
            # Get product options
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail and product_detail['options']:
                response += f"   🏍️ Kompatibilitas:\n"
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        values = [v['display_value'] for v in option['values'] if v['is_available']]
                        response += f"      • {', '.join(values)}\n"
        
        response += f"\n🛒 Order: shopee.co.id/boyprojectsasli"
        return response
    
    def _handle_stok_produk_intent(self, user_message: str) -> str:
        """Handle stock inquiry"""
        products = self.db.get_all_products()
        
        # Check if user asks about specific product
        user_lower = user_message.lower()
        matching_products = []
        
        for product in products:
            if any(word in user_lower for word in product['name'].lower().split()):
                matching_products.append(product)
        
        if matching_products:
            response = "📦 Informasi Stok Produk:\n"
            for product in matching_products:
                stock_info = self.db.get_stock_info(product['id'])
                response += f"\n📱 {stock_info['product_name']}\n"
                response += f"   📦 Stok: {stock_info['stock']} unit\n"
                response += f"   ✅ Status: {stock_info['availability']}\n"
                response += f"   📊 Terjual: {stock_info['sold']} unit\n"
                response += f"   ⭐ Rating: {stock_info['average_rating']}/5.0\n"
        else:
            # Show general stock summary
            in_stock = [p for p in products if p['stock'] > 0]
            out_of_stock = [p for p in products if p['stock'] == 0]
            
            response = f"📊 Ringkasan Stok Boys Project:\n"
            response += f"✅ Produk Tersedia: {len(in_stock)} item\n"
            response += f"❌ Stok Habis: {len(out_of_stock)} item\n"
            
            if in_stock:
                response += f"\n📦 Produk Ready Stock:\n"
                for product in in_stock[:5]:  # Show top 5
                    response += f"   • {product['name']} ({product['stock']} unit)\n"
        
        response += f"\n📞 Cek stok terkini: WhatsApp 08211990442"
        return response
    
    def _handle_jam_operasional_intent(self, user_message: str) -> str:
        """Handle operational hours inquiry"""
        return """⏰ Jam Operasional Boys Project:

📅 Senin - Jumat: 08:00 - 17:00 WIB
📅 Sabtu - Minggu: 10:00 - 16:00 WIB

📞 Customer Service 24/7:
   WhatsApp: 08211990442

🏪 Alamat Workshop:
   Cimahi, Bandung

💬 Fast Response via WhatsApp untuk:
   • Konsultasi produk
   • Booking pemasangan
   • Info stok & harga"""
    
    def _handle_garansi_intent(self, user_message: str) -> str:
        """Handle warranty inquiry"""
        return """🛡️ Informasi Garansi Boys Project:

✅ Garansi Produk:
   • Lampu: 6 bulan garansi
   • Mounting: 1 tahun garansi
   • Spare parts: 3-12 bulan (tergantung jenis)

✅ Garansi Pemasangan:
   • Garansi workmanship 30 hari
   • Jika ada masalah akibat kesalahan pemasangan

📋 Syarat Garansi:
   • Produk dibeli dari Boys Project
   • Kerusakan bukan akibat pemakaian tidak wajar
   • Menyertakan bukti pembelian

📞 Klaim Garansi:
   WhatsApp: 08211990442
   
📍 Alamat Service:
   Cimahi, Bandung"""
    
    def _handle_booking_pemasangan_intent(self, user_message: str) -> str:
        """Handle installation booking inquiry"""
        return """📅 Booking Pemasangan Boys Project:

🔧 Layanan Pemasangan:
   • Pemasangan lampu motor
   • Pemasangan mounting
   • Custom installation
   • Konsultasi modifikasi

⏰ Jam Pemasangan:
   Senin - Jumat: 08:00 - 17:00
   Sabtu - Minggu: 10:00 - 16:00

📞 Cara Booking:
   1. WhatsApp: 08211990442
   2. Sebutkan jenis motor & produk
   3. Tentukan waktu kedatangan
   4. Konfirmasi booking

💰 Biaya Pemasangan:
   • Varies by product type
   • Free installation untuk pembelian tertentu
   • Konsultasi biaya via WhatsApp

📍 Lokasi Workshop:
   Cimahi, Bandung
   
⚡ Fast booking via WhatsApp untuk slot terbaik!"""
    
    def _handle_pengiriman_intent(self, user_message: str) -> str:
        """Handle shipping inquiry"""
        return """📦 Informasi Pengiriman Boys Project:

🚚 Metode Pengiriman:
   • JNE Regular & Express
   • J&T Express
   • SiCepat
   • Grab/Gojek (area Bandung)

💰 Ongkos Kirim:
   • Sesuai tarif ekspedisi
   • Free ongkir untuk pembelian min. tertentu
   • Promo free ongkir berkala

📦 Packaging:
   • Bubble wrap & kardus tebal
   • Packing aman untuk spare parts
   • Include invoice & manual

⏰ Proses Pengiriman:
   • Same day untuk order sebelum 14:00
   • H+1 untuk order setelah 14:00
   • Estimasi tiba 1-3 hari (Pulau Jawa)

📞 Tracking & Info:
   WhatsApp: 08211990442
   
🛒 Order langsung: shopee.co.id/boyprojectsasli"""
    
    def _handle_durasi_pengiriman_intent(self, user_message: str) -> str:
        """Handle shipping duration inquiry"""
        return """⏰ Durasi Pengiriman Boys Project:

🏃‍♂️ Same Day Bandung:
   • Grab/Gojek: 1-2 jam
   • Anteraja: 4-6 jam
   
🚚 Pulau Jawa:
   • JNE REG: 1-2 hari
   • JNE YES: 1 hari
   • J&T Express: 1-2 hari
   • SiCepat: 1-2 hari

🛫 Luar Pulau Jawa:
   • JNE REG: 2-4 hari
   • JNE YES: 1-2 hari
   • Tergantung akses wilayah

⚡ Express Service:
   • JNE YES, SiCepat Halu
   • Tiba keesokan hari
   • Biaya tambahan

📍 Area Khusus:
   • Pedalaman: +1-2 hari
   • Pulau terpencil: 3-7 hari

📞 Estimasi akurat per wilayah:
   WhatsApp: 08211990442"""
    
    def _handle_wilayah_pemasangan_intent(self, user_message: str) -> str:
        """Handle installation area inquiry"""
        products = self.db.get_all_products()
        total_sold = sum(p['sold'] for p in products)
        
        return f"""📍 Wilayah Pemasangan Boys Project:

🏪 Workshop Utama:
   📍 Cimahi, Bandung
   ⏰ Senin-Jumat: 08:00-17:00
   ⏰ Sabtu-Minggu: 10:00-16:00

🏍️ Home Service Area:
   • Bandung Raya (Bandung, Cimahi, Bandung Barat)
   • Biaya transport sesuai jarak
   • Minimum order berlaku

🤝 Partner Workshop:
   • Jakarta (Partner terpilih)
   • Surabaya (Partner terpilih)
   • Info partner: WhatsApp

📊 Pengalaman Kami:
   • {total_sold}+ unit terpasang
   • Berbagai tipe motor
   • Customer dari seluruh Indonesia

📞 Konsultasi Wilayah:
   WhatsApp: 08211990442
   
💡 Tip: Banyak customer yang pasang sendiri dengan panduan video kami!"""
    
    def _handle_tipe_motor_matic_intent(self, user_message: str) -> str:
        """Handle motorcycle type compatibility"""
        # Get product options to show compatible motorcycles
        products = self.db.get_all_products()
        motor_types = set()
        
        for product in products:
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail:
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        for value in option['values']:
                            if value['is_available']:
                                motor_types.add(value['display_value'])
        
        response = "🏍️ Tipe Motor yang Didukung Boys Project:\n"
        
        # Categorize motor types
        yamaha_types = [m for m in motor_types if any(y in m.lower() for y in ['aerox', 'nmax', 'lexy'])]
        honda_types = [m for m in motor_types if any(h in m.lower() for h in ['vario', 'beat', 'scoopy'])]
        
        if yamaha_types:
            response += f"\n🔵 Yamaha:\n"
            for motor in sorted(yamaha_types):
                response += f"   • {motor}\n"
        
        if honda_types:
            response += f"\n🔴 Honda:\n"
            for motor in sorted(honda_types):
                response += f"   • {motor}\n"
        
        response += f"\n✅ Keunggulan Produk Kami:\n"
        response += f"   • Plug & Play installation\n"
        response += f"   • Presisi tinggi, tidak miring\n"
        response += f"   • Compatible dengan berbagai tipe\n"
        response += f"   • Garansi kesesuaian produk\n"
        
        response += f"\n❓ Motor Anda tidak ada di list?\n"
        response += f"   WhatsApp: 08211990442\n"
        response += f"   Kami cek kompatibilitas untuk Anda!"
        
        return response
    
    def _handle_layanan_instalasi_intent(self, user_message: str) -> str:
        """Handle installation service inquiry"""
        return """🔧 Layanan Instalasi Boys Project:

⚡ Jenis Layanan:
   • Pemasangan lampu LED motor
   • Pemasangan mounting body
   • Custom installation
   • Konsultasi modifikasi
   • Troubleshooting

👨‍🔧 Keunggulan Tim Kami:
   • Teknisi berpengalaman 5+ tahun
   • Spesialisasi motor matic
   • Tools professional lengkap
   • Garansi workmanship

💰 Biaya Instalasi:
   • Lampu: Mulai 50rb
   • Mounting: Mulai 30rb
   • Paket combo: Diskon special
   • Free install untuk pembelian tertentu

⏰ Estimasi Waktu:
   • Lampu sederhana: 30-60 menit
   • Mounting: 45-90 menit
   • Custom work: 1-3 jam

📍 Tempat Instalasi:
   • Workshop Cimahi, Bandung
   • Home service (area terbatas)
   • Partner workshop (kota besar)

📞 Booking Instalasi:
   WhatsApp: 08211990442
   
🎥 DIY Tutorial:
   Follow Instagram: @boyprojects
   Video tutorial pemasangan tersedia!"""

def main():
    """Demonstrate ML Database Integration"""
    print("🤖 Boys Project ML Database Integration Demo")
    print("=" * 60)
    
    # Initialize integration
    ml_db = MLDatabaseIntegration()
    
    if ml_db.connect_database():
        try:
            # Test various intents with database responses
            test_cases = [
                ("harga", "Berapa harga mounting aerox?"),
                ("daftar", "Mau lihat daftar produk yang tersedia"),
                ("stok_produk", "Apakah mounting vario masih ada stok?"),
                ("kategori_lighting", "Produk lampu apa saja yang ada?"),
                ("kategori_mounting_body", "Mounting untuk motor apa saja?"),
                ("jam_operasional", "Kapan buka tutupnya?"),
                ("booking_pemasangan", "Mau booking pasang lampu"),
            ]
            
            for intent, user_message in test_cases:
                print(f"\n🎯 Intent: {intent}")
                print(f"👤 User: {user_message}")
                print(f"🤖 Bot Response:")
                response = ml_db.get_intent_response(intent, user_message)
                print(response)
                print("-" * 40)
            
        finally:
            ml_db.disconnect_database()
    
    else:
        print("❌ Failed to connect to database")

if __name__ == "__main__":
    main() 