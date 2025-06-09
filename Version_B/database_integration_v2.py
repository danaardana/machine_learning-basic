#!/usr/bin/env python3
"""
Database Integration for Version B
Connects the existing Version B chatbot with Boys Project MySQL database
Enhanced with sub-intent detection and real product data
"""

import sys
import os
# Add parent directory to access database_connector
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_connector import BoysProjectDatabase
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

class VersionBDatabaseIntegrator:
    """
    Advanced database integration for Version B chatbot
    Combines sub-intent detection with real product database queries
    """
    
    def __init__(self):
        self.db = BoysProjectDatabase()
        self.connected = False
        
        # Load existing Version B models
        try:
            self.classifier = joblib.load('../ml_model/chat_model_v2.pkl')
            self.vectorizer = joblib.load('../ml_model/vectorizer_v2.pkl')
            self.label_encoder = joblib.load('../ml_model/label_encoder_v2.pkl')
            self.sub_intent_patterns = joblib.load('../ml_model/sub_intent_patterns.pkl')
            print("✅ Version B ML models loaded successfully!")
        except FileNotFoundError as e:
            print(f"❌ Error loading Version B models: {e}")
            print("Please run train_model_v2.py first.")
            sys.exit(1)
    
    def connect_database(self):
        """Connect to database"""
        self.connected = self.db.connect()
        return self.connected
    
    def disconnect_database(self):
        """Disconnect from database"""
        if self.connected:
            self.db.disconnect()
            self.connected = False
    
    def predict_sub_intents(self, user_input):
        """Predict sub-intents using Version B model"""
        # Transform input
        X = self.vectorizer.transform([user_input])
        
        # Predict using multi-label classifier
        predicted_binary = self.classifier.predict(X)
        predicted_labels = self.label_encoder.inverse_transform(predicted_binary)[0]
        
        # Get confidence scores
        try:
            decision_scores = self.classifier.decision_function(X)[0]
            label_confidence = {}
            for i, label in enumerate(self.label_encoder.classes_):
                confidence = max(0, decision_scores[i])
                label_confidence[label] = confidence
        except:
            label_confidence = {label: 0.5 for label in predicted_labels}
        
        # Filter confident predictions
        confident_labels = [label for label in predicted_labels if label_confidence.get(label, 0) > 0.1]
        if not confident_labels:
            confident_labels = list(predicted_labels)
        
        return confident_labels, label_confidence
    
    def enhance_with_pattern_matching(self, user_input, predicted_labels):
        """Enhance predictions with pattern matching"""
        enhanced_labels = set(predicted_labels)
        user_lower = user_input.lower()
        
        for main_intent, sub_patterns in self.sub_intent_patterns.items():
            for sub_intent, patterns in sub_patterns.items():
                full_label = f"{main_intent}_{sub_intent}"
                if full_label not in enhanced_labels:
                    for pattern in patterns:
                        if re.search(pattern, user_lower):
                            enhanced_labels.add(full_label)
                            break
        
        return list(enhanced_labels)
    
    def get_enhanced_response(self, user_input):
        """Get enhanced response with database integration"""
        if not self.connected:
            return ["Maaf, sistem database sedang tidak tersedia. Silakan coba lagi nanti."]
        
        print(f"🔍 Analyzing: '{user_input}'")
        
        # Predict sub-intents
        predicted_labels, confidence_scores = self.predict_sub_intents(user_input)
        print(f"🎯 ML Predictions: {predicted_labels}")
        
        # Enhance with pattern matching
        enhanced_labels = self.enhance_with_pattern_matching(user_input, predicted_labels)
        print(f"🔧 Enhanced Labels: {enhanced_labels}")
        
        # Generate database-enhanced responses
        responses = self._generate_database_responses(enhanced_labels, user_input)
        
        # Show confidence scores
        top_confidences = sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"📊 Top Confidences: {[(label, f'{conf:.2f}') for label, conf in top_confidences]}")
        
        return responses
    
    def _generate_database_responses(self, labels, user_input):
        """Generate responses using database data based on detected labels"""
        responses = []
        
        for label in labels:
            if 'harga' in label:
                responses.append(self._handle_harga_responses(label, user_input))
            elif 'stok' in label:
                responses.append(self._handle_stok_responses(label, user_input))
            elif 'kategori_lighting' in label:
                responses.append(self._handle_lighting_responses(label))
            elif 'kategori_mounting' in label:
                responses.append(self._handle_mounting_responses(label))
            elif 'tipe_motor' in label:
                responses.append(self._handle_motor_responses(label))
            elif 'daftar' in label:
                responses.append(self._handle_daftar_responses(label))
            elif 'jam_operasional' in label:
                responses.append(self._handle_operasional_responses(label))
            elif 'garansi' in label:
                responses.append(self._handle_garansi_responses(label))
            elif 'booking' in label or 'pemasangan' in label:
                responses.append(self._handle_booking_responses(label))
            elif 'pengiriman' in label:
                responses.append(self._handle_pengiriman_responses(label))
            elif 'wilayah' in label:
                responses.append(self._handle_wilayah_responses(label))
            elif 'layanan' in label or 'instalasi' in label:
                responses.append(self._handle_instalasi_responses(label))
        
        # Remove duplicates and None responses
        responses = [r for r in responses if r]
        if not responses:
            responses = [self._handle_general_inquiry()]
        
        return responses
    
    def _handle_harga_responses(self, label, user_input):
        """Handle price-related responses with database data"""
        products = self.db.get_all_products()
        
        # Extract product mentions
        user_lower = user_input.lower()
        matching_products = []
        for product in products:
            if any(word in user_lower for word in product['name'].lower().split()):
                matching_products.append(product)
        
        if 'harga_produk' in label:
            if matching_products:
                response = "💰 **HARGA PRODUK SPESIFIK**\n\n"
                for product in matching_products[:2]:
                    response += f"📦 **{product['name']}**\n"
                    response += f"   • Kategori: {product['category']}\n"
                    response += f"   • Stok: {product['stock']:,} unit tersedia\n"
                    response += f"   • Rating: ⭐ {product['average_rating']}/5.0 ({product['ratings']} review)\n"
                    response += f"   • Track record: {product['sold']:,} unit terjual\n"
                    
                    # Add detailed product options
                    product_detail = self.db.get_product_with_options(product['id'])
                    if 'options' in product_detail and product_detail['options']:
                        response += f"   • Varian tersedia:\n"
                        for option in product_detail['options']:
                            values = [v['display_value'] for v in option['values'][:4]]
                            response += f"     - {option['display_name']}: {', '.join(values)}\n"
                    response += "\n"
                response += "📞 **Nego harga & info detail:** WhatsApp 08211990442"
            else:
                response = self._get_general_price_info()
            
        elif 'harga_promo' in label:
            response = self._get_promo_info_with_products()
        elif 'harga_grosir' in label:
            response = self._get_grosir_info_with_stats()
        elif 'harga_ongkir' in label:
            response = self._get_shipping_cost_info()
        elif 'harga_instalasi' in label:
            response = self._get_installation_cost_info()
        else:
            response = self._get_general_price_info()
        
        return response
    
    def _handle_stok_responses(self, label, user_input):
        """Handle stock-related responses with real data"""
        user_lower = user_input.lower()
        products = self.db.get_all_products()
        
        # Find mentioned products
        matching_products = []
        for product in products:
            if any(word in user_lower for word in product['name'].lower().split()):
                matching_products.append(product)
        
        if 'stok_tersedia' in label or matching_products:
            if matching_products:
                response = "✅ **STATUS STOK PRODUK**\n\n"
                for product in matching_products:
                    stock_info = self.db.get_stock_info(product['id'])
                    status_icon = "✅" if product['stock'] > 0 else "⏳"
                    status_text = "Ready Stock" if product['stock'] > 0 else "Perlu Restock"
                    
                    response += f"{status_icon} **{product['name']}**\n"
                    response += f"   📊 Stok: {stock_info['stock']:,} unit\n"
                    response += f"   🎯 Status: {status_text}\n"
                    response += f"   📈 Total terjual: {stock_info['sold']:,} unit\n"
                    response += f"   ⭐ Customer rating: {stock_info['average_rating']}/5.0\n"
                    
                    if product['stock'] > 100:
                        response += f"   🚀 Stock melimpah - siap kirim!\n"
                    elif product['stock'] > 0:
                        response += f"   ⚠️ Stock terbatas - buruan order!\n"
                    else:
                        response += f"   ⏰ Restock dalam 2-3 hari kerja\n"
                    response += "\n"
            else:
                # General stock overview
                in_stock = [p for p in products if p['stock'] > 0]
                response = f"📊 **OVERVIEW STOK READY**\n\n"
                response += f"✅ **Produk Tersedia:** {len(in_stock)} item\n\n"
                for product in in_stock:
                    response += f"   • {product['name']} ({product['stock']:,} unit)\n"
                
        elif 'stok_habis' in label:
            out_of_stock = [p for p in products if p['stock'] == 0]
            if out_of_stock:
                response = "⏳ **JADWAL RESTOCK**\n\n"
                for product in out_of_stock:
                    response += f"   • {product['name']} - Restock 2-3 hari\n"
                response += "\n🔔 Join waiting list untuk notifikasi!"
            else:
                response = "🎉 **GOOD NEWS!** Semua produk saat ini ready stock!"
                
        elif 'stok_booking' in label:
            response = "📝 **BOOKING & PRE-ORDER**\n\n"
            response += "🎯 **Sistem Booking:**\n"
            response += "   • DP 30% untuk booking stock\n"
            response += "   • Berlaku 7 hari\n"
            response += "   • Notifikasi otomatis saat ready\n\n"
            response += "📦 **Stock Ready:**\n"
            for product in products:
                if product['stock'] > 0:
                    response += f"   ✅ {product['name']} - Langsung available\n"
        else:
            # General stock response
            stats = self.db.get_database_stats()
            response = f"📊 **RINGKASAN STOK BOYS PROJECT**\n\n"
            response += f"📦 Total produk: {stats['total_products']} item\n"
            response += f"📋 Total stok: {stats['total_stock']:,} unit\n"
            response += f"🏆 Total terjual: {stats['total_sold']:,} unit\n"
        
        response += "\n📞 **Cek stok real-time:** WhatsApp 08211990442"
        return response
    
    def _handle_lighting_responses(self, label):
        """Handle lighting category with database data"""
        lighting_products = self.db.get_products_by_category('Lampu')
        
        response = "💡 **KATEGORI LIGHTING BOYS PROJECT**\n\n"
        
        if lighting_products:
            for product in lighting_products:
                response += f"🔆 **{product['name']}**\n"
                response += f"   📝 {product['description']}\n"
                response += f"   📦 Stok: {product['stock']:,} unit\n"
                response += f"   ⭐ Rating: {product['average_rating']}/5.0\n"
                
                # Show product options from database
                product_detail = self.db.get_product_with_options(product['id'])
                if 'options' in product_detail and product_detail['options']:
                    response += f"   🔧 **Opsi Pembelian:**\n"
                    for option in product_detail['options']:
                        values = []
                        for value in option['values']:
                            if value['is_available']:
                                price_text = f" (+${value['price_adjustment']})" if value['price_adjustment'] > 0 else ""
                                values.append(f"{value['display_value']}{price_text}")
                        response += f"      • {option['display_name']}: {', '.join(values)}\n"
                response += "\n"
        else:
            response += "⏳ Produk lighting sedang restock. Hubungi kami untuk info terbaru!\n\n"
        
        response += "⚡ **Keunggulan LED Boys Project:**\n"
        response += "   • Teknologi LED terdepan\n"
        response += "   • Hemat daya, awet & terang\n"
        response += "   • Plug & play installation\n"
        response += "   • Waterproof rating IP67\n"
        response += "   • Garansi resmi\n\n"
        response += "🛒 **Order:** shopee.co.id/boyprojectsasli"
        
        return response
    
    def _handle_mounting_responses(self, label):
        """Handle mounting category with database data"""
        mounting_products = self.db.get_products_by_category('Mounting & Body')
        
        response = "🔧 **KATEGORI MOUNTING & BODY**\n\n"
        
        for product in mounting_products:
            response += f"🏍️ **{product['name']}**\n"
            response += f"   📝 {product['description']}\n"
            response += f"   📦 Stok: {product['stock']:,} unit (Hot item! 🔥)\n"
            response += f"   ⭐ Rating: {product['average_rating']}/5.0 dari {product['ratings']} review\n"
            response += f"   🏆 Proven quality: {product['sold']:,} unit terjual\n"
            
            # Show detailed compatibility from database
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail and product_detail['options']:
                response += f"   🏍️ **Kompatibilitas Motor:**\n"
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        available_motors = [v['display_value'] for v in option['values'] if v['is_available']]
                        response += f"      ✅ {', '.join(available_motors[:6])}"
                        if len(available_motors) > 6:
                            response += f" + {len(available_motors)-6} motor lainnya"
                        response += "\n"
                    elif 'size' in option['option_name'].lower():
                        sizes = [v['display_value'] for v in option['values'] if v['is_available']]
                        response += f"      📏 Ukuran tersedia: {', '.join(sizes)}\n"
            response += "\n"
        
        response += "✨ **Why Choose Boys Project Mounting:**\n"
        response += "   • Presisi CNC machining\n"
        response += "   • Material grade A\n"
        response += "   • Fitment guarantee 100%\n"
        response += "   • No drilling, plug & play\n"
        response += "   • Garansi 1 tahun\n\n"
        response += "📞 **Konsultasi fitting:** WhatsApp 08211990442"
        
        return response
    
    def _handle_motor_responses(self, label):
        """Handle motor compatibility with comprehensive database data"""
        products = self.db.get_all_products()
        all_motors = set()
        motor_product_map = {}
        
        # Extract all motor compatibility data
        for product in products:
            product_detail = self.db.get_product_with_options(product['id'])
            if 'options' in product_detail:
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        for value in option['values']:
                            if value['is_available']:
                                motor = value['display_value']
                                all_motors.add(motor)
                                if motor not in motor_product_map:
                                    motor_product_map[motor] = []
                                motor_product_map[motor].append(product['name'])
        
        # Categorize motors by brand
        yamaha_motors = sorted([m for m in all_motors if any(y in m.lower() for y in ['aerox', 'nmax', 'lexi', 'mio', 'jupiter', 'yamaha'])])
        honda_motors = sorted([m for m in all_motors if any(h in m.lower() for h in ['vario', 'beat', 'scoopy', 'pcx', 'honda'])])
        other_motors = sorted([m for m in all_motors if m not in yamaha_motors + honda_motors])
        
        response = "🏍️ **MOTOR COMPATIBILITY BOYS PROJECT**\n\n"
        
        if yamaha_motors:
            response += "🔵 **YAMAHA SUPPORT:**\n"
            for motor in yamaha_motors:
                compatible_products = len(motor_product_map.get(motor, []))
                response += f"   ✅ {motor} ({compatible_products} produk)\n"
            response += "\n"
        
        if honda_motors:
            response += "🔴 **HONDA SUPPORT:**\n"
            for motor in honda_motors:
                compatible_products = len(motor_product_map.get(motor, []))
                response += f"   ✅ {motor} ({compatible_products} produk)\n"
            response += "\n"
        
        if other_motors:
            response += "⚪ **BRAND LAINNYA:**\n"
            for motor in other_motors:
                compatible_products = len(motor_product_map.get(motor, []))
                response += f"   ✅ {motor} ({compatible_products} produk)\n"
            response += "\n"
        
        # Statistics from database
        stats = self.db.get_database_stats()
        response += f"📊 **COMPATIBILITY STATS:**\n"
        response += f"   • {len(all_motors)} tipe motor didukung\n"
        response += f"   • {stats['total_products']} produk tersedia\n"
        response += f"   • {stats['total_option_values']} varian pilihan\n"
        response += f"   • Success rate: 95%+ compatibility\n\n"
        
        response += "❓ **Motor Anda tidak terdaftar?**\n"
        response += "   📞 WhatsApp: 08211990442\n"
        response += "   Kami cek compatibility & sediakan custom solution!\n\n"
        response += "🔧 **Custom Fitting Service:**\n"
        response += "   Available untuk motor rare/modifikasi"
        
        return response
    
    def _get_general_price_info(self):
        """Get general price info with database stats"""
        stats = self.db.get_database_stats()
        popular_products = sorted(self.db.get_all_products(), key=lambda x: x['sold'], reverse=True)[:2]
        
        response = "💰 **INFORMASI HARGA BOYS PROJECT**\n\n"
        response += "🔥 **Best Seller Products:**\n"
        for product in popular_products:
            response += f"   • {product['name']} - {product['sold']:,} terjual\n"
        
        response += f"\n📊 **Range Harga Kategori:**\n"
        response += f"   • Mounting: Rp 450K - 650K\n"
        response += f"   • Lampu LED: Rp 350K - 550K\n"
        response += f"   • Body Kit: Rp 800K - 1.2M\n"
        response += f"   • Instalasi: Rp 50K - 100K\n\n"
        response += f"💳 **Payment Options:**\n"
        response += f"   • Transfer Bank • COD Area Bandung\n"
        response += f"   • Shopee/Tokopedia • Cicilan 0%\n\n"
        response += f"📞 **Nego harga:** WhatsApp 08211990442"
        
        return response
    
    def _get_promo_info_with_products(self):
        """Get promo info with current stock data"""
        in_stock_products = [p for p in self.db.get_all_products() if p['stock'] > 0]
        
        response = "🎉 **PROMO & DISKON TERKINI**\n\n"
        response += "⚡ **Flash Sale Products:**\n"
        for product in in_stock_products[:3]:
            response += f"   🔥 {product['name']} - Stock: {product['stock']} unit\n"
        
        response += "\n🎁 **Promo Berlaku:**\n"
        response += "   • Bundling discount 15%\n"
        response += "   • Member exclusive 10%\n"
        response += "   • Flash sale Jumat 19:00\n"
        response += "   • Free ongkir Bandung-Cimahi\n\n"
        response += "📱 **Update promo:** Follow IG @boyprojects"
        
        return response
    
    def _get_grosir_info_with_stats(self):
        """Get wholesale info with database statistics"""
        stats = self.db.get_database_stats()
        
        response = "🏪 **HARGA GROSIR & RESELLER**\n\n"
        response += f"📊 **Catalog Size:** {stats['total_products']} produk\n"
        response += f"📦 **Total Stock:** {stats['total_stock']:,} unit\n\n"
        response += "💼 **Paket Reseller:**\n"
        response += "   • Discount 20-30%\n"
        response += "   • MOQ: 10 pcs\n"
        response += "   • Dropship system\n"
        response += "   • Marketing support\n\n"
        response += "🎯 **Benefits:**\n"
        response += "   • Price list khusus\n"
        response += "   • Priority stock\n"
        response += "   • Training produk\n\n"
        response += "📞 **Daftar partner:** WhatsApp 08211990442"
        
        return response
    
    def _get_shipping_cost_info(self):
        """Get shipping cost information"""
        return """🚚 **BIAYA PENGIRIMAN BOYS PROJECT**

💰 **Ongkir Rates:**
   • Bandung-Cimahi: GRATIS 🆓
   • Jabodetabek: Rp 15.000
   • Pulau Jawa: Rp 20.000 - 25.000
   • Luar Jawa: Rp 30.000 - 50.000

⚡ **Express Options:**
   • Same day delivery: +Rp 10.000
   • Overnight service: +Rp 20.000
   • Instant Grab/Gojek: +Rp 15.000

🎁 **Free Ongkir Promo:**
   • Min. belanja Rp 500.000
   • Member exclusive benefit
   • Weekend special (Sabtu-Minggu)

📦 **Ekspedisi Partner:**
   JNE • J&T • SiCepat • Grab • Gojek"""
    
    def _get_installation_cost_info(self):
        """Get installation cost information"""
        return """🔧 **BIAYA PEMASANGAN BOYS PROJECT**

💰 **Tarif Instalasi:**
   • Mounting install: Rp 50.000
   • LED setup: Rp 75.000  
   • Body kit fitting: Rp 100.000
   • Custom work: Rp 150.000+

🏠 **Home Service:**
   • Dalam kota: +Rp 30.000
   • Luar kota: +Rp 50.000
   • Weekend: Normal rate

🎁 **Special Offer:**
   • Beli produk + pasang: Diskon 50%
   • Paket bundling: Free install
   • Member rate: Diskon 20%

⏰ **Estimasi Waktu:**
   • Simple install: 30-60 menit
   • Complex fitting: 1-2 jam"""
    
    def _handle_daftar_responses(self, label):
        """Handle product listing with comprehensive database data"""
        products = self.db.get_all_products()
        categories = self.db.get_product_categories()
        stats = self.db.get_database_stats()
        
        response = f"📋 **COMPLETE CATALOG BOYS PROJECT**\n\n"
        response += f"📊 **Overview:** {stats['total_products']} produk • {stats['total_stock']:,} unit stock • {stats['total_sold']:,} terjual\n\n"
        
        for category in categories:
            category_products = self.db.get_products_by_category(category)
            response += f"🏷️ **{category.upper()}** ({len(category_products)} item):\n"
            
            for product in category_products:
                stock_icon = "✅" if product['stock'] > 0 else "⏳"
                popularity = "🔥" if product['sold'] > 1000 else "⭐" if product['sold'] > 100 else ""
                
                response += f"   {stock_icon} **{product['name']}** {popularity}\n"
                response += f"      📦 Stock: {product['stock']:,} | 📈 Sold: {product['sold']:,}\n"
                response += f"      ⭐ {product['average_rating']}/5.0 • 📝 {product['description'][:60]}...\n"
                
                # Show compatibility preview
                product_detail = self.db.get_product_with_options(product['id'])
                if 'options' in product_detail and product_detail['options']:
                    motor_option = next((opt for opt in product_detail['options'] if 'motor' in opt['option_name'].lower()), None)
                    if motor_option:
                        motors = [v['display_value'] for v in motor_option['values'][:3] if v['is_available']]
                        response += f"      🏍️ Support: {', '.join(motors)}\n"
                response += "\n"
        
        response += "🛒 **Order Channel:**\n"
        response += "   • Shopee: shopee.co.id/boyprojectsasli\n"
        response += "   • WhatsApp: 08211990442\n"
        response += "   • Visit toko: Cimahi, Bandung"
        
        return response
    
    def _handle_operasional_responses(self, label):
        """Handle operational hours"""
        return """⏰ **JAM OPERASIONAL BOYS PROJECT**

🏪 **STORE HOURS:**
   • Senin-Jumat: 08:00 - 17:00 WIB
   • Sabtu-Minggu: 10:00 - 16:00 WIB
   • Libur nasional: TUTUP

📞 **CUSTOMER SERVICE:**
   • WhatsApp: 08211990442
   • Response time: < 5 menit (jam kerja)
   • Emergency: 24/7 (untuk customer)

🔧 **WORKSHOP SERVICE:**
   • Install service: Sesuai jam buka
   • Home service: By appointment
   • Emergency repair: Call dulu

📍 **LOKASI:**
   Workshop & Store: Cimahi, Bandung
   (Maps location via WhatsApp)"""
    
    def _handle_garansi_responses(self, label):
        """Handle warranty information"""
        return """🛡️ **GARANSI BOYS PROJECT**

✅ **PRODUCT WARRANTY:**
   • Mounting products: 1 tahun
   • LED lighting: 6 bulan  
   • Body parts: 6 bulan
   • Installation work: 30 hari

📋 **WARRANTY TERMS:**
   • Manufacturing defects covered
   • Normal wear & tear excluded
   • Misuse/accident not covered
   • Original receipt required

🔧 **CLAIM PROCESS:**
   1. Contact via WhatsApp: 08211990442
   2. Send photo/video issue
   3. Bring product + receipt
   4. Free assessment & repair

🏪 **SERVICE CENTER:**
   Workshop Cimahi, Bandung
   Mon-Fri: 08:00-17:00"""
    
    def _handle_booking_responses(self, label):
        """Handle booking and installation"""
        return """📅 **BOOKING PEMASANGAN BOYS PROJECT**

🔧 **INSTALLATION SERVICES:**
   • Mounting installation
   • LED lighting setup
   • Body kit fitting
   • Custom modification
   • Troubleshooting service

📞 **BOOKING PROCESS:**
   1. WhatsApp: 08211990442
   2. Info: produk + motor type
   3. Pilih jadwal appointment
   4. Konfirmasi via chat

⏰ **AVAILABLE SLOTS:**
   • Weekdays: 09:00 - 16:00
   • Weekends: 10:00 - 15:00
   • Duration: 30 min - 2 jam

💰 **SERVICE RATES:**
   Workshop: Standard rate
   Home service: +Rp 30K
   Weekend: Normal rate"""
    
    def _handle_pengiriman_responses(self, label):
        """Handle shipping information"""
        return """📦 **SHIPPING BOYS PROJECT**

🚚 **COURIER PARTNERS:**
   • JNE (REG/YES/TRUCKING)
   • J&T Express
   • SiCepat (REG/HALU)
   • Instant: Grab/Gojek

💰 **SHIPPING COSTS:**
   • Bandung-Cimahi: FREE
   • Java Island: Rp 15K-25K
   • Outside Java: Rp 25K-50K
   • Same day: +Rp 10K

📦 **PACKAGING:**
   • Bubble wrap protection
   • Cardboard box
   • Fragile item handling
   • Include manual/warranty

⏰ **PROCESSING:**
   • Order < 14:00 = same day ship
   • Order > 14:00 = next day ship"""
    
    def _handle_wilayah_responses(self, label):
        """Handle service area coverage"""
        return """📍 **WILAYAH LAYANAN BOYS PROJECT**

🏪 **MAIN WORKSHOP:**
   • Address: Cimahi, Bandung
   • Parking: Motor & mobil available
   • Facilities: AC, waiting area, tools lengkap

🏍️ **HOME SERVICE COVERAGE:**
   • Kota Bandung (all area)
   • Kota Cimahi (all area)  
   • Bandung Barat: Lembang, Parongpong
   • Bandung: Dayeuhkolot, Baleendah, Soreang

💰 **SERVICE CHARGES:**
   • Workshop: FREE (customer datang)
   • Home service Bandung: +Rp 30K
   • Home service luar: +Rp 50K

📞 **AREA CHECK:**
   WhatsApp 08211990442 untuk konfirmasi coverage area Anda"""
    
    def _handle_instalasi_responses(self, label):
        """Handle installation service information"""
        return """🔧 **LAYANAN INSTALASI BOYS PROJECT**

⚡ **SERVICE TYPES:**
   • Mounting installation (plug & play)
   • LED lighting system setup
   • Body kit professional fitting
   • Custom modification work
   • Electrical troubleshooting

👨‍🔧 **TECHNICIAN EXPERTISE:**
   • 5+ years experience
   • Certified for motorcycle electronics
   • Specialized in matic scooters
   • Complete professional tools

💰 **INSTALLATION RATES:**
   • Simple mounting: Rp 50K
   • LED setup: Rp 75K
   • Body kit: Rp 100K
   • Complex mod: Rp 150K+

🛡️ **SERVICE GUARANTEE:**
   • 30-day workmanship warranty
   • Free minor adjustments
   • Technical support included"""
    
    def _handle_general_inquiry(self):
        """Handle general inquiries with database stats"""
        stats = self.db.get_database_stats() if self.connected else {}
        
        response = "👋 **WELCOME TO BOYS PROJECT**\n\n"
        response += "🏍️ **SPECIALIST MOTOR MATIC PARTS**\n"
        
        if stats:
            response += f"📊 **Our Scale:**\n"
            response += f"   • {stats.get('total_products', 0)} products available\n"
            response += f"   • {stats.get('total_stock', 0):,} units in stock\n"
            response += f"   • {stats.get('total_sold', 0):,} satisfied customers\n"
            response += f"   • {stats.get('total_option_values', 0)} product variants\n\n"
        
        response += "🎯 **ASK US ABOUT:**\n"
        response += "   • Product prices & promos\n"
        response += "   • Stock availability\n" 
        response += "   • Motor compatibility\n"
        response += "   • Installation booking\n"
        response += "   • Warranty & service\n\n"
        
        response += "📞 **CONTACT US:**\n"
        response += "   • WhatsApp: 08211990442\n"
        response += "   • IG: @boyprojects\n"
        response += "   • Shop: shopee.co.id/boyprojectsasli"
        
        return response

def main():
    """Demo Version B with database integration"""
    print("🤖 VERSION B - ADVANCED DATABASE INTEGRATION DEMO")
    print("=" * 70)
    
    integrator = VersionBDatabaseIntegrator()
    
    if not integrator.connect_database():
        print("❌ Cannot connect to database. Please check XAMPP MySQL.")
        return
    
    try:
        # Demo conversations with sub-intent detection
        demo_queries = [
            "Berapa harga mounting vario dan bisa nego ga?",
            "Stok lampu LED untuk aerox masih ada?",
            "Motor beat bisa pake mounting yang mana?",
            "Mau lihat semua produk yang ready stock",
            "Promo bulan ini apa aja?",
            "Biaya pasang mounting berapa ya?",
        ]
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n{i}. 👤 User: {query}")
            responses = integrator.get_enhanced_response(query)
            for j, response in enumerate(responses, 1):
                if len(responses) > 1:
                    print(f"🤖 Bot Response {j}:\n{response}")
                else:
                    print(f"🤖 Bot Response:\n{response}")
            print("-" * 50)
    
    finally:
        integrator.disconnect_database()
    
    print("\n✅ Version B Advanced Database Integration Demo Complete!")

if __name__ == "__main__":
    main() 