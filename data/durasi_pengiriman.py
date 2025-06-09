# data/durasi_pengiriman.py - Delivery Duration

durasi_pengiriman_sentences = [
    # Basic delivery time inquiries
    "Berapa lama barang sampai?",
    "Estimasi pengiriman ke Bekasi berapa hari?",
    "Kalau pesan sekarang, kapan sampai?",
    "Lama pengiriman dalam kota berapa hari?",
    "Pengiriman weekend tetap jalan?",
    "Bisa urgent delivery gak?",
    "Express delivery ada gak?",
    "Estimasi ke luar Jawa berapa hari?",
    "Kalau same day, jam berapa sampai?",
    "Regular shipping butuh berapa hari?",
    
    # Holiday and weekend timing
    "Pengiriman hari libur delay gak?",
    "Fastest delivery option apa?",
    "Weekend order dikirim hari apa?",
    "Overnight shipping tersedia?",
    "Rush order bisa diatur?",
    "Lead time pengiriman berapa?",
    "Next day delivery ada?",
    "Waktu tempuh ke Bogor berapa hari?",
    "Kirim hari ini sampai kapan?",
    "Delivery time luar kota gimana?",
    
    # Processing and scheduling
    "Estimasi tiba di alamat kapan?",
    "Processing time berapa lama?",
    "Cut off time order jam berapa?",
    "Standard delivery berapa hari?",
    "Priority shipping butuh berapa hari?",
    "Durasi pengiriman ekonomis berapa?",
    "Timeframe delivery budget?",
    "Kecepatan shipping premium?",
    "Durasi pengiriman kilat?",
    "Waktu accelerated shipping?",
    
    # Express and fast delivery
    "Kecepatan fast track delivery?",
    "Timeframe super express?",
    "Lightning delivery tersedia?",
    "Instant delivery time?",
    "Opsi pengiriman langsung?",
    "Layanan delivery real-time?",
    "Kecepatan on-demand delivery?",
    "Timeframe scheduled delivery?",
    "Durasi planned shipping?",
    "Layanan timed delivery?",
    
    # Appointment and guaranteed delivery
    "Slot delivery tersedia?",
    "Window delivery time?",
    "Layanan appointment delivery?",
    "Timeframe delivery terkonfirmasi?",
    "Guaranteed delivery time?",
    "Tanggal pengiriman terjamin?",
    "Durasi shipping berkomitmen?",
    "Timeframe delivery terjamin?",
    "Kecepatan shipping terpercaya?",
    "Waktu delivery konsisten?",
    
    # External factors affecting delivery
    "Durasi shipping yang bisa diprediksi?",
    "Timeframe delivery stabil?",
    "Pengiriman tergantung cuaca?",
    "Season pengaruh delivery?",
    "Holiday delayed shipping?",
    "Peak season delivery time?",
    "Kecepatan shipping off-peak?",
    "Durasi delivery low season?",
    "High demand shipping delay?",
    "Capacity limited delivery?",
    
    # Route and logistics timing
    "Route optimized shipping?",
    "Direct delivery service?",
    "Hub routing delivery?",
    "Multi-stop shipping time?",
    "Consolidation delivery delay?",
    "Sorting facility time?",
    "Transit hub durasi?",
    "Transfer point delay?",
    "Customs processing time?",
    "Border crossing durasi?",
    
    # International and documentation
    "International shipping delay?",
    "Documentation processing time?",
    "Inspection delay mungkin?",
    "Quarantine processing time?",
    "Health check durasi?",
    "Security screening delay?",
    "Quality control time?",
    "Verification process durasi?",
    "Confirmation delay mungkin?",
    "Authentication processing time?",
    
    # Tracking and communication
    "Tracking update frequency?",
    "Status notification timing?",
    "Progress report interval?",
    "Information update schedule?",
    "Communication frequency delivery?",
    "Customer notification timing?",
    "Alert system delivery?",
    "Reminder service timing?",
    "Update pengiriman kapan?",
    "Notifikasi status berapa sering?",
    
    # Specific city and region timing
    "Berapa lama sampai Jakarta?",
    "Durasi kirim ke Surabaya?",
    "Waktu pengiriman ke Medan?",
    "Estimasi sampai Yogyakarta?",
    "Lama kirim ke Semarang?",
    "Durasi pengiriman ke Bali?",
    "Waktu sampai Makassar?",
    "Estimasi kirim ke Palembang?",
    "Lama pengiriman ke Malang?",
    "Durasi sampai Banjarmasin?",
    
    # Local area timing specifics
    "Waktu kirim Bandung-Cimahi?",
    "Durasi delivery dalam kota?",
    "Estimasi pengiriman Jabodetabek?",
    "Lama kirim Greater Bandung?",
    "Durasi pengiriman metropolitan?",
    "Waktu delivery suburban?",
    "Estimasi sampai pinggiran kota?",
    "Lama kirim daerah terpencil?",
    "Durasi pengiriman rural?",
    "Waktu delivery ke pelosok?",
    
    # Specific problematic patterns - pengiriman ke Bandung variations
    "Kalau pengiriman ke Bandung berapa lama?",
    "Pengiriman ke Bandung brp lama?",
    "Bila pengiriman ke bandung berapa hari?",
    "Bila memasukan kirim ke bandung bisa?",
    "Mau pesan, kirim ke bandung bisa?",
    "Kirim ke Bandung berapa hari sampai?",
    "Kalau mau kirim ke Bandung kapan sampai?",
    "Delivery ke Bandung butuh berapa lama?",
    "Pengiriman Bandung estimasi berapa hari?",
    "Kirim barang ke Bandung berapa lama?",
    
    # More variations with different cities to strengthen the pattern
    "Kalau pengiriman ke Jakarta berapa lama?",
    "Bila memasukan kirim ke Jakarta bisa?",
    "Mau pesan, kirim ke Jakarta bisa?",
    "Kalau pengiriman ke Surabaya berapa lama?",
    "Bila memasukan kirim ke Surabaya bisa?",
    "Mau pesan, kirim ke Surabaya bisa?",
    "Kalau pengiriman ke Yogya berapa lama?",
    "Bila memasukan kirim ke Yogya bisa?",
    "Mau pesan, kirim ke Yogya bisa?",
    
    # Order + shipping time combinations
    "Kalau order sekarang, ke Bandung berapa hari?",
    "Pesan hari ini ke Bandung kapan sampai?",
    "Order barang ke Bandung berapa lama?",
    "Beli sekarang ke Bandung kapan tiba?",
    "Checkout hari ini ke Bandung estimasi kapan?",
    "Purchase ke Bandung delivery time berapa?",
    "Transaksi hari ini ke Bandung kapan nyampe?",
    "Bayar sekarang ke Bandung sampai kapan?",
    
    # Question patterns that might be misclassified
    "Ongkir ke Bandung berapa dan berapa lama?",
    "Biaya kirim ke Bandung dan estimasi waktu?",
    "Tarif pengiriman Bandung plus durasi?",
    "Cost delivery Bandung sama time estimate?",
    "Harga kirim ke Bandung berapa lama sampai?",
    "Fee pengiriman Bandung dan eta berapa?",
    
    # Informal and conversational patterns
    "Ke Bandung nyampe berapa hari sih?",
    "Bandung butuh berapa hari ya?",
    "Kirim Bandung lama ga?",
    "Ke Bandung berapa lama dong?",
    "Bandung estimasi berapa hari ya?",
    "Delivery Bandung fast ga?",
    "Kirim ke Bandung express ada?",
    "Ke Bandung same day bisa?",
    "Bandung overnight shipping ada?",
    "Rush delivery ke Bandung bisa?"
]

# Total: 150+ sentences for durasi_pengiriman intent
# Added specific patterns for "pengiriman ke [city]" variations
# to prevent misclassification to product intent 