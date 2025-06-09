#!/usr/bin/env python3
"""
Enhanced Version A Prediction with Database Integration
Maintains compatibility with existing predict.py while adding database capabilities
"""

import joblib
import re
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Add parent directory to access database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database_connector import BoysProjectDatabase
    DATABASE_AVAILABLE = True
    print("✅ Database integration available")
except ImportError:
    DATABASE_AVAILABLE = False
    print("⚠️ Database integration not available - using static responses")

# Load model dan vectorizer
try:
    model = joblib.load('../ml_model/chat_model.pkl')
    vectorizer = joblib.load('../ml_model/vectorizer.pkl')
    print("✅ ML models loaded successfully")
except FileNotFoundError:
    print("❌ ML models not found. Please train the model first.")
    model = None
    vectorizer = None

# Initialize database connection
db = None
if DATABASE_AVAILABLE:
    db = BoysProjectDatabase()
    if db.connect():
        print("✅ Database connected successfully")
    else:
        print("⚠️ Database connection failed - using static responses")
        DATABASE_AVAILABLE = False

# Daftar motor matic yang tersedia (fallback + database integration)
motor_tersedia = [
    "honda beat", "honda vario", "honda revo x",
    "yamaha vega force", "yamaha jupiter z1",
    "suzuki address fi", "suzuki smash fi",
    "tvs dazz", "viar star nx", "honda nmax", 
    "honda revo", "honda pcx", "honda aerox", 
    "honda scoopy", "honda vespa"
]

# Enhanced response dictionary with database integration capability
enhanced_answer_dict = {
    "harga": {
        "static": "💰 **HARGA & PAKET** | Untuk harga mounting & body atau lighting, sebutkan produk spesifiknya ya! Kami ada paket bundling, harga grosir untuk reseller, dan promo khusus member. Price list lengkap bisa di-chat via WhatsApp.",
        "use_database": True
    },
    "daftar": {
        "static": "📝 **PENDAFTARAN MEMBER/RESELLER** | Daftar jadi member/reseller via WhatsApp atau formulir online. Benefit: harga khusus, prioritas stok, akses produk eksklusif, dan program kemitraan. Pendaftaran GRATIS!",
        "use_database": True
    },
    "stok_produk": {
        "static": "📦 **STOK & AVAILABILITY** | Most items ready stock! Kalau kosong, restock 2-3 hari. Limited edition/import stock tersedia. Indent order & waiting list available. Real-time stock update via WhatsApp!",
        "use_database": True
    },
    "kategori_mounting_body": {
        "static": "🏍️ **KATEGORI: MOUNTING & BODY** | Tersedia: mounting sport/universal/custom, body kit, fairing, undercowl, windshield, side panel. Material: carbon fiber, aluminium, ABS. Original & aftermarket. Custom design available!",
        "use_database": True
    },
    "kategori_lighting": {
        "static": "💡 **KATEGORI: LIGHTING** | Tersedia: LED headlamp, DRL, lampu variasi, sein kristal, angel eyes, projector, RGB underglow, LED bar, emergency light. Hemat listrik, plug & play, waterproof!",
        "use_database": True
    },
    "tipe_motor_matic": {
        "static": "🏍️ **MOTOR SUPPORT** | Honda: Beat, Vario 125/160, PCX, Scoopy. Yamaha: Aerox 155, Lexi, Freego, Mio. Support motor matic 110-160cc. Vespa modern OK. Cek compatibility via chat!",
        "use_database": True
    },
    "jam_operasional": {
        "static": "🕘 **JAM OPERASIONAL** | Buka setiap hari 09.00-17.00 WIB di Bandung. Workshop pemasangan jam yang sama. Libur nasional tutup. Weekend tetap buka normal, no break time!",
        "use_database": False
    },
    "garansi": {
        "static": "🛡️ **GARANSI PRODUK** | Mounting & Body: garansi 1 bulan kerusakan pabrik. Lighting: garansi 1 bulan + after sales service. Pemasangan bergaransi hasil kerja teknisi. Syarat: nota pembelian + kartu garansi.",
        "use_database": False
    },
    "booking_pemasangan": {
        "static": "🔧 **BOOKING PEMASANGAN** | Hubungi WhatsApp dengan info: jenis produk, tipe motor, alamat, jadwal. Layanan Bandung-Cimahi only. Teknisi berpengalaman + tools lengkap. Weekend available!",
        "use_database": False
    },
    "pengiriman": {
        "static": "🚚 **PENGIRIMAN** | Ke seluruh Indonesia via JNE/J&T/Sicepat. Bandung-Cimahi: COD/same day delivery/pickup toko. Packaging aman + asuransi. Instant delivery via Gojek/Grab tersedia!",
        "use_database": False
    },
    "durasi_pengiriman": {
        "static": "⏱️ **DURASI PENGIRIMAN** | Dalam kota: 1 hari. Luar kota: 2-5 hari kerja. Same day (Bandung-Cimahi): 2-6 jam. Express/overnight shipping available. Cut off time: 14.00 WIB.",
        "use_database": False
    },
    "wilayah_pemasangan": {
        "static": "📍 **WILAYAH PEMASANGAN** | Coverage: Kota Bandung & Cimahi (Rancaekek, Gedebage, Kopo, Cileunyi, Dayeuhkolot, Soreang, Margahayu, Dago, Antapani). Teknisi mobile berpengalaman!",
        "use_database": False
    },
    "layanan_instalasi": {
        "static": "🔧 **LAYANAN INSTALASI** | Professional installation service: mounting, body kit, lighting system. Certified technician + full warranty hasil kerja. Mobile service/workshop. Tools lengkap + spare parts backup!",
        "use_database": False
    }
}

def get_database_motor_list():
    """Get motor compatibility list from database"""
    if not DATABASE_AVAILABLE or not db:
        return motor_tersedia
    
    try:
        products = db.get_all_products()
        motor_types = set()
        
        for product in products:
            product_detail = db.get_product_with_options(product['id'])
            if 'options' in product_detail:
                for option in product_detail['options']:
                    if 'motor' in option['option_name'].lower():
                        for value in option['values']:
                            if value['is_available']:
                                # Convert to lowercase format matching existing system
                                motor_name = value['display_value'].lower()
                                motor_types.add(motor_name)
        
        # Combine with static list for compatibility
        combined_motors = list(set(list(motor_types) + motor_tersedia))
        return combined_motors
    except:
        return motor_tersedia

def cek_motor_tersedia(user_input):
    """Enhanced motor checking with database integration"""
    kalimat = user_input.lower()
    
    # Get motors from database if available
    available_motors = get_database_motor_list()
    
    for motor in available_motors:
        if motor in kalimat:
            motor_display = motor.title()
            
            # If database available, get specific compatibility info
            if DATABASE_AVAILABLE and db:
                try:
                    # Check which products support this motor
                    products = db.get_all_products()
                    compatible_products = []
                    
                    for product in products:
                        product_detail = db.get_product_with_options(product['id'])
                        if 'options' in product_detail:
                            for option in product_detail['options']:
                                if 'motor' in option['option_name'].lower():
                                    motor_values = [v['display_value'].lower() for v in option['values'] if v['is_available']]
                                    if any(motor.lower() in mv for mv in motor_values):
                                        compatible_products.append(product['name'])
                    
                    if compatible_products:
                        return f"✅ **{motor_display} SUPPORTED!**\n\nProduk kompatibel:\n" + "\n".join([f"• {p}" for p in compatible_products]) + f"\n\n📞 Info detail: WhatsApp 08211990442"
                except:
                    pass
            
            return f"Ya, produk tersedia untuk {motor_display}. Silakan pilih kategori: Mounting & Body atau Lighting"
    
    if any(kata in kalimat for kata in ["motor", "matic", "vario", "beat", "pcx", "aerox", "scoopy", "nmax", "jupiter", "revo", "lexi", "smash", "vega", "dazz"]):
        return "Untuk motor tersebut saat ini produk belum tersedia. Silakan cek motor matic yang kami support di daftar produk."
    return None

def get_database_response(intent, user_input):
    """Get enhanced response from database for specific intents"""
    if not DATABASE_AVAILABLE or not db:
        return None
    
    try:
        if intent == "harga":
            return get_database_harga_response(user_input)
        elif intent == "daftar":
            return get_database_daftar_response()
        elif intent == "stok_produk":
            return get_database_stok_response(user_input)
        elif intent == "kategori_mounting_body":
            return get_database_mounting_response()
        elif intent == "kategori_lighting":
            return get_database_lighting_response()
        elif intent == "tipe_motor_matic":
            return get_database_motor_response()
    except Exception as e:
        print(f"Database error: {e}")
        return None
    
    return None

def get_database_harga_response(user_input):
    """Get price response with real product data"""
    products = db.get_all_products()
    user_lower = user_input.lower()
    
    # Find mentioned products
    matching_products = []
    for product in products:
        product_words = product['name'].lower().split()
        if any(word in user_lower for word in product_words):
            matching_products.append(product)
    
    if matching_products:
        response = "💰 **HARGA PRODUK REAL-TIME**\n\n"
        for product in matching_products[:2]:
            response += f"📦 **{product['name']}**\n"
            response += f"   • Kategori: {product['category']}\n"
            response += f"   • Stock: {product['stock']:,} unit\n"
            response += f"   • Rating: ⭐ {product['average_rating']}/5.0\n"
            response += f"   • Terjual: {product['sold']:,} unit\n"
            
            # Add product options
            product_detail = db.get_product_with_options(product['id'])
            if 'options' in product_detail and product_detail['options']:
                response += f"   • Varian: "
                options = []
                for option in product_detail['options']:
                    values = [v['display_value'] for v in option['values'][:3]]
                    options.append(f"{option['display_name']} ({', '.join(values)})")
                response += "; ".join(options) + "\n"
            response += "\n"
        
        response += "📞 **Info harga detail:** WhatsApp 08211990442\n"
        response += "🛒 **Order langsung:** shopee.co.id/boyprojectsasli"
        return response
    else:
        # General price with popular products
        popular = sorted(products, key=lambda x: x['sold'], reverse=True)[:2]
        response = "💰 **HARGA & PROMO BOYS PROJECT**\n\n"
        response += "🔥 **Best Seller:**\n"
        for product in popular:
            response += f"   • {product['name']} ({product['sold']:,} terjual)\n"
        response += "\n📞 Nego harga: WhatsApp 08211990442"
        return response

def get_database_daftar_response():
    """Get product listing with database data"""
    products = db.get_all_products()
    categories = db.get_product_categories()
    stats = db.get_database_stats()
    
    response = f"📋 **KATALOG BOYS PROJECT** ({stats['total_products']} produk)\n\n"
    
    for category in categories:
        category_products = db.get_products_by_category(category)
        response += f"🏷️ **{category}** ({len(category_products)} item):\n"
        
        for product in category_products:
            stock_icon = "✅" if product['stock'] > 0 else "⏳"
            response += f"   {stock_icon} {product['name']}\n"
            response += f"      Stock: {product['stock']:,} | Rating: {product['average_rating']}/5\n"
        response += "\n"
    
    response += f"📊 **Total Stock:** {stats['total_stock']:,} unit\n"
    response += f"🏆 **Total Terjual:** {stats['total_sold']:,} unit\n\n"
    response += "🛒 **Order:** shopee.co.id/boyprojectsasli\n"
    response += "📞 **Info:** WhatsApp 08211990442"
    
    return response

def get_database_stok_response(user_input):
    """Get stock response with real data"""
    products = db.get_all_products()
    user_lower = user_input.lower()
    
    # Find mentioned products
    matching_products = []
    for product in products:
        if any(word in user_lower for word in product['name'].lower().split()):
            matching_products.append(product)
    
    if matching_products:
        response = "📦 **STATUS STOK REAL-TIME**\n\n"
        for product in matching_products:
            stock_info = db.get_stock_info(product['id'])
            status = "✅ Ready Stock" if product['stock'] > 0 else "⏳ Restock Soon"
            
            response += f"📱 **{product['name']}**\n"
            response += f"   📊 Stok: {stock_info['stock']:,} unit\n"
            response += f"   🎯 Status: {status}\n"
            response += f"   📈 Terjual: {stock_info['sold']:,} unit\n"
            response += f"   ⭐ Rating: {stock_info['average_rating']}/5.0\n\n"
    else:
        # General stock overview
        in_stock = [p for p in products if p['stock'] > 0]
        response = f"📊 **RINGKASAN STOK**\n\n"
        response += f"✅ Produk Ready: {len(in_stock)} item\n\n"
        for product in in_stock:
            response += f"   • {product['name']} ({product['stock']:,} unit)\n"
    
    response += "\n📞 **Cek stok real-time:** WhatsApp 08211990442"
    return response

def get_database_mounting_response():
    """Get mounting products with database data"""
    mounting_products = db.get_products_by_category('Mounting & Body')
    
    response = "🔧 **KATEGORI: MOUNTING & BODY**\n\n"
    
    for product in mounting_products:
        response += f"🏍️ **{product['name']}**\n"
        response += f"   📝 {product['description']}\n"
        response += f"   📦 Stock: {product['stock']:,} unit\n"
        response += f"   ⭐ Rating: {product['average_rating']}/5.0 ({product['ratings']} review)\n"
        response += f"   🏆 Terjual: {product['sold']:,} unit\n"
        
        # Show compatibility
        product_detail = db.get_product_with_options(product['id'])
        if 'options' in product_detail and product_detail['options']:
            response += f"   🏍️ **Support:**\n"
            for option in product_detail['options']:
                if 'motor' in option['option_name'].lower():
                    motors = [v['display_value'] for v in option['values'] if v['is_available']][:4]
                    response += f"      • {', '.join(motors)}\n"
        response += "\n"
    
    response += "🛒 **Order:** shopee.co.id/boyprojectsasli"
    return response

def get_database_lighting_response():
    """Get lighting products with database data"""
    lighting_products = db.get_products_by_category('Lampu')
    
    response = "💡 **KATEGORI: LIGHTING**\n\n"
    
    for product in lighting_products:
        response += f"🔆 **{product['name']}**\n"
        response += f"   📝 {product['description']}\n"
        response += f"   📦 Stock: {product['stock']:,} unit\n"
        response += f"   ⭐ Rating: {product['average_rating']}/5.0\n"
        
        # Show options
        product_detail = db.get_product_with_options(product['id'])
        if 'options' in product_detail and product_detail['options']:
            response += f"   🔧 **Pilihan:**\n"
            for option in product_detail['options']:
                values = [v['display_value'] for v in option['values'] if v['is_available']]
                response += f"      • {option['display_name']}: {', '.join(values)}\n"
        response += "\n"
    
    response += "🛒 **Order:** shopee.co.id/boyprojectsasli"
    return response

def get_database_motor_response():
    """Get motor compatibility with database data"""
    products = db.get_all_products()
    motor_types = set()
    
    for product in products:
        product_detail = db.get_product_with_options(product['id'])
        if 'options' in product_detail:
            for option in product_detail['options']:
                if 'motor' in option['option_name'].lower():
                    for value in option['values']:
                        if value['is_available']:
                            motor_types.add(value['display_value'])
    
    # Categorize by brand
    yamaha = [m for m in motor_types if any(y in m.lower() for y in ['aerox', 'nmax', 'lexi', 'mio'])]
    honda = [m for m in motor_types if any(h in m.lower() for h in ['vario', 'beat', 'scoopy', 'pcx'])]
    
    response = "🏍️ **MOTOR SUPPORT BOYS PROJECT**\n\n"
    
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
    
    response += f"📊 **Total Support:** {len(motor_types)} tipe motor\n"
    response += "❓ **Cek compatibility:** WhatsApp 08211990442"
    
    return response

def predict_intents(user_input):
    """Enhanced predict function with database integration"""
    if not model or not vectorizer:
        return ["general"]
    
    # Prediksi intent utama dari model
    X = vectorizer.transform([user_input])
    main_intent = model.predict(X)[0]
    
    # Return as list for compatibility
    return [main_intent]

def get_responses(user_input):
    """Enhanced response function with database integration"""
    # Cek apakah menyebutkan tipe motor langsung
    motor_check = cek_motor_tersedia(user_input)
    if motor_check:
        return [motor_check]
    
    # Prediksi intent
    intents = predict_intents(user_input)
    responses = []
    
    for intent in intents:
        if intent in enhanced_answer_dict:
            # Try database response first if enabled
            if enhanced_answer_dict[intent].get("use_database", False):
                db_response = get_database_response(intent, user_input)
                if db_response:
                    responses.append(db_response)
                else:
                    # Fallback to static response
                    responses.append(enhanced_answer_dict[intent]["static"])
            else:
                # Use static response
                responses.append(enhanced_answer_dict[intent]["static"])
    
    if not responses:
        if DATABASE_AVAILABLE and db:
            try:
                stats = db.get_database_stats()
                fallback = f"Maaf, bisa ulangi pertanyaannya? Kami melayani {stats['total_products']} produk Mounting & Body dan Lighting untuk motor matic di Bandung-Cimahi. 📞 WhatsApp: 08211990442"
                return [fallback]
            except:
                pass
        
        return ["Maaf, bisa ulangi pertanyaannya? Kami melayani produk Mounting & Body dan Lighting untuk motor matic di wilayah Bandung-Cimahi."]
    
    return responses

def prediksi_intent(user_input):
    """Fungsi compatibility untuk single response (backwards compatibility)"""
    responses = get_responses(user_input)
    return responses[0] if responses else "Maaf, bisa ulangi pertanyaannya?"

# Demo function
def demo_enhanced_system():
    """Demo the enhanced system with database integration"""
    print("🤖 **VERSION A ENHANCED - DATABASE INTEGRATION**")
    print("=" * 60)
    print(f"Database Status: {'✅ Connected' if DATABASE_AVAILABLE and db else '❌ Static Mode'}")
    print("-" * 60)
    
    demo_queries = [
        "Berapa harga mounting vario?",
        "Produk apa saja yang tersedia?",
        "Stok mounting aerox masih ada?",
        "Motor beat bisa pake mounting ga?",
        "Jam operasional kapan?",
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i}. 👤 User: {query}")
        responses = get_responses(query)
        for j, response in enumerate(responses, 1):
            if len(responses) > 1:
                print(f"🤖 Bot ({j}): {response}")
            else:
                print(f"🤖 Bot: {response}")
        print("-" * 40)

# Contoh penggunaan
if __name__ == "__main__":
    # Demo enhanced system
    demo_enhanced_system()
    
    print("\n" + "=" * 60)
    print("🎯 **INTERACTIVE MODE** (type 'exit' to quit)")
    print("=" * 60)
    
    while True:
        user_input = input("\n👤 Anda: ")
        if user_input.lower() in ["exit", "quit", "keluar"]:
            print("🤖 Bot: Terima kasih sudah mengunjungi Boys Project! 👋")
            break
        
        responses = get_responses(user_input)
        for i, response in enumerate(responses, 1):
            if len(responses) > 1:
                print(f"🤖 Bot ({i}): {response}")
            else:
                print(f"🤖 Bot: {response}")
    
    # Cleanup
    if DATABASE_AVAILABLE and db:
        db.disconnect() 