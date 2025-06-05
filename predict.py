import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load model dan vectorizer
model = joblib.load('chat_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Daftar motor matic yang tersedia
motor_tersedia = [
    "honda beat", "honda vario", "honda revo x",
    "yamaha vega force", "yamaha jupiter z1",
    "suzuki address fi", "suzuki smash fi",
    "tvs dazz", "viar star nx", "honda nmax", 
    "honda revo", "honda pcx", "honda aerox", 
    "honda scoopy", "honda vespa"
]

# Predefined response dictionary
answer_dict = {
    "harga": "💰 **HARGA & PAKET** | Untuk harga mounting & body atau lighting, sebutkan produk spesifiknya ya! Kami ada paket bundling, harga grosir untuk reseller, dan promo khusus member. Price list lengkap bisa di-chat via WhatsApp.",
    "daftar": "📝 **PENDAFTARAN MEMBER/RESELLER** | Daftar jadi member/reseller via WhatsApp atau formulir online. Benefit: harga khusus, prioritas stok, akses produk eksklusif, dan program kemitraan. Pendaftaran GRATIS!",
    "jam_operasional": "🕘 **JAM OPERASIONAL** | Buka setiap hari 09.00-17.00 WIB di Bandung. Workshop pemasangan jam yang sama. Libur nasional tutup. Weekend tetap buka normal, no break time!",
    "garansi": "🛡️ **GARANSI PRODUK** | Mounting & Body: garansi 1 bulan kerusakan pabrik. Lighting: garansi 1 bulan + after sales service. Pemasangan bergaransi hasil kerja teknisi. Syarat: nota pembelian + kartu garansi.",
    "booking_pemasangan": "🔧 **BOOKING PEMASANGAN** | Hubungi WhatsApp dengan info: jenis produk, tipe motor, alamat, jadwal. Layanan Bandung-Cimahi only. Teknisi berpengalaman + tools lengkap. Weekend available!",
    "kategori_mounting_body": "🏍️ **KATEGORI: MOUNTING & BODY** | Tersedia: mounting sport/universal/custom, body kit, fairing, undercowl, windshield, side panel. Material: carbon fiber, aluminium, ABS. Original & aftermarket. Custom design available!",
    "kategori_lighting": "💡 **KATEGORI: LIGHTING** | Tersedia: LED headlamp, DRL, lampu variasi, sein kristal, angel eyes, projector, RGB underglow, LED bar, emergency light. Hemat listrik, plug & play, waterproof!",
    "pengiriman": "🚚 **PENGIRIMAN** | Ke seluruh Indonesia via JNE/J&T/Sicepat. Bandung-Cimahi: COD/same day delivery/pickup toko. Packaging aman + asuransi. Instant delivery via Gojek/Grab tersedia!",
    "durasi_pengiriman": "⏱️ **DURASI PENGIRIMAN** | Dalam kota: 1 hari. Luar kota: 2-5 hari kerja. Same day (Bandung-Cimahi): 2-6 jam. Express/overnight shipping available. Cut off time: 14.00 WIB.",
    "wilayah_pemasangan": "📍 **WILAYAH PEMASANGAN** | Coverage: Kota Bandung & Cimahi (Rancaekek, Gedebage, Kopo, Cileunyi, Dayeuhkolot, Soreang, Margahayu, Dago, Antapani). Teknisi mobile berpengalaman!",
    "tipe_motor_matic": "🏍️ **MOTOR SUPPORT** | Honda: Beat, Vario 125/160, PCX, Scoopy. Yamaha: Aerox 155, Lexi, Freego, Mio. Support motor matic 110-160cc. Vespa modern OK. Cek compatibility via chat!",
    "stok_produk": "📦 **STOK & AVAILABILITY** | Most items ready stock! Kalau kosong, restock 2-3 hari. Limited edition/import stock tersedia. Indent order & waiting list available. Real-time stock update via WhatsApp!",
    "layanan_instalasi": "🔧 **LAYANAN INSTALASI** | Professional installation service: mounting, body kit, lighting system. Certified technician + full warranty hasil kerja. Mobile service/workshop. Tools lengkap + spare parts backup!"
}

# Keyword bank per intent (untuk bantu deteksi intent kedua)
keyword_bank = {
    "harga": [
        # Basic terms
        "harga", "biaya", "bayar", "diskon", "murah", "mahal", "tarif", "ongkir", "cost", "price",
        # Indonesian slang & variations
        "brp", "berapa", "berapaan", "duit", "dough", "budget", "kisaran", "range", "promo", "cicilan",
        "grosir", "wholesale", "member", "reseller", "paket", "bundling", "total", "keseluruhan",
        # Regional terms
        "ongkos", "biayanya", "harganya", "tarinya", "costnya", "pricenya", "second", "bekas"
    ],
    "daftar": [
        # Basic terms  
        "daftar", "gabung", "registrasi", "akun", "member", "reseller", "agen", "distributor", "register",
        # Extended terms
        "join", "signup", "sign up", "membership", "partner", "mitra", "dealer", "aplikasi", "app",
        "prosedur", "syarat", "formulir", "form", "kemitraan", "bisnis", "online", "website"
    ],
    "jam_operasional": [
        # Basic terms
        "jam", "buka", "tutup", "operasional", "jadwal", "weekend", "libur", "minggu", "sabtu",
        # Extended terms
        "schedule", "waktu", "time", "hours", "senin", "selasa", "rabu", "kamis", "jumat",
        "weekday", "hari", "kerja", "raya", "lebaran", "natal", "break", "istirahat", "24jam"
    ],
    "garansi": [
        # Basic terms
        "garansi", "jaminan", "warranty", "rusak", "cacat", "klaim", "tukar", "ganti",
        # Extended terms
        "claim", "pecah", "patah", "bengkok", "mati", "void", "extend", "coverage", "nota",
        "kartu", "sertifikat", "return", "refund", "policy", "internasional", "tahun", "bulan"
    ],
    "booking_pemasangan": [
        # Basic terms
        "booking", "book", "pesan", "jadwal", "pasang", "install", "teknisi", "tukang",
        # Extended terms
        "reservasi", "appointment", "schedule", "slot", "mobile", "service", "onsite", "home",
        "panggil", "datang", "standby", "available", "weekend", "online", "via", "charge"
    ],
    "kategori_mounting_body": [
        # Basic terms
        "mounting", "body", "bodi", "sport", "custom", "universal", "carbon", "fairing",
        # Extended terms
        "kit", "panel", "undercowl", "windshield", "aluminium", "plastik", "abs", "fiber",
        "racing", "adjustable", "phone", "holder", "gps", "waterproof", "action", "cam",
        "side", "samping", "copotan", "modifikasi", "request", "original", "aftermarket"
    ],
    "kategori_lighting": [
        # Basic terms
        "lampu", "led", "lighting", "variasi", "sein", "angel", "projector", "rgb", "terang",
        # Extended terms
        "headlamp", "headlight", "drl", "stop", "lamp", "kristal", "bar", "sorot", "bohlam",
        "emergency", "underglow", "rem", "strobo", "kabut", "hid", "cornering", "accent",
        "12v", "watt", "eyes", "strip", "dekorasi", "hazard", "listrik", "hemat"
    ],
    "pengiriman": [
        # Basic terms
        "kirim", "antar", "ekspedisi", "cod", "pickup", "ambil", "delivery", "shipping",
        # Extended terms
        "jne", "jnt", "sicepat", "pos", "grab", "gojek", "instant", "same", "day", "cargo",
        "darat", "udara", "resi", "tracking", "door", "express", "charge", "dalam", "kota"
    ],
    "durasi_pengiriman": [
        # Basic terms
        "lama", "berapa", "hari", "sampai", "estimasi", "cepat", "express", "same day",
        # Extended terms
        "lead", "time", "next", "overnight", "waktu", "tempuh", "tiba", "alamat", "processing",
        "cut", "off", "standard", "priority", "urgent", "rush", "fastest", "delay"
    ],
    "wilayah_pemasangan": [
        # Basic terms
        "area", "wilayah", "bandung", "cimahi", "coverage", "jangkauan", "radius", "lokasi",
        # Bandung area specific
        "rancaekek", "gedebage", "kopo", "cileunyi", "dayeuhkolot", "soreang", "margahayu",
        "dago", "antapani", "ujungberung", "lembang", "majalaya", "katapang", "timur", "barat",
        "selatan", "utara", "service", "meliputi", "masuk", "termasuk", "dijangkau"
    ],
    "tipe_motor_matic": [
        # Basic terms
        "motor", "matic", "beat", "vario", "aerox", "scoopy", "pcx", "mio", "lexi", "jupiter",
        # Extended terms
        "honda", "yamaha", "suzuki", "vespa", "freego", "fino", "soul", "gt", "street", "new",
        "old", "generasi", "lama", "modern", "china", "listrik", "gesits", "compatible",
        "support", "cocok", "150cc", "160cc", "110cc", "125cc", "155cc", "aksesoris"
    ],
    "stok_produk": [
        # Basic terms
        "stok", "stock", "ready", "ada", "habis", "kosong", "restock", "indent", "waiting",
        # Extended terms
        "inventory", "update", "availability", "langka", "limited", "edition", "discontinued",
        "import", "seasonal", "bestseller", "available", "arrival", "back", "order", "booking",
        "notification", "varian", "alternatif", "tersedia", "masih", "sudah", "belum"
    ],
    "layanan_instalasi": [
        # Basic terms
        "jasa", "pasang", "install", "teknisi", "service", "maintenance", "tutorial", "training",
        # Extended terms
        "installation", "technician", "spare", "part", "onsite", "bengkel", "workshop", "mobile",
        "mechanic", "professional", "installer", "certified", "custom", "setup", "technical",
        "support", "24/7", "garansi", "hasil", "tools", "lengkap", "konsultasi", "komplain"
    ]
}

def cek_motor_tersedia(user_input):
    kalimat = user_input.lower()
    for motor in motor_tersedia:
        if motor in kalimat:
            return f"Ya, produk tersedia untuk {motor.title()}. Silakan pilih kategori: Mounting & Body atau Lighting"
    if any(kata in kalimat for kata in ["motor", "matic", "vario", "beat", "pcx", "aerox", "scoopy", "nmax", "jupiter", "revo", "lexi", "smash", "vega", "dazz"]):
        return "Untuk motor tersebut saat ini produk belum tersedia. Silakan cek motor matic yang kami support di daftar produk."
    return None

def predict_intents(user_input):
    # Prediksi intent utama dari model
    X = vectorizer.transform([user_input])
    main_intent = model.predict(X)[0]

    # Cari intent tambahan berdasarkan keyword
    detected_intents = set([main_intent])
    lowered = user_input.lower()

    for intent, keywords in keyword_bank.items():
        if any(re.search(rf"\b{k}\b", lowered) for k in keywords):
            detected_intents.add(intent)

    return list(detected_intents)

def get_responses(user_input):
    # Cek apakah menyebutkan tipe motor langsung
    motor_check = cek_motor_tersedia(user_input)
    if motor_check:
        return [motor_check]
    
    # Prediksi multiple intents
    intents = predict_intents(user_input)
    responses = [answer_dict[i] for i in intents if i in answer_dict]
    
    if not responses:
        return ["Maaf, bisa ulangi pertanyaannya? Kami melayani produk Mounting & Body dan Lighting untuk motor matic di wilayah Bandung-Cimahi."]
    
    return responses

def prediksi_intent(user_input):
    """Fungsi compatibility untuk single response (backwards compatibility)"""
    responses = get_responses(user_input)
    return responses[0] if responses else "Maaf, bisa ulangi pertanyaannya?"

# Contoh penggunaan
if __name__ == "__main__":
    while True:
        user_input = input("Anda: ")
        if user_input.lower() in ["exit", "quit", "keluar"]:
            print("Bot: Terima kasih sudah mengunjungi toko kami!")
            break
        
        responses = get_responses(user_input)
        for i, response in enumerate(responses, 1):
            if len(responses) > 1:
                print(f"Bot ({i}): {response}")
            else:
                print(f"Bot: {response}")
