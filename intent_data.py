# ml_model/intent_data.py

from data.harga import harga_sentences
from data.daftar import daftar_sentences  
from data.kategori_lighting import kategori_lighting_sentences
from data.kategori_mounting_body import kategori_mounting_body_sentences
from data.stok_produk import stok_produk_sentences
from data.jam_operasional import jam_operasional_sentences
from data.garansi import garansi_sentences
from data.booking_pemasangan import booking_pemasangan_sentences
from data.pengiriman import pengiriman_sentences
from data.durasi_pengiriman import durasi_pengiriman_sentences
from data.wilayah_pemasangan import wilayah_pemasangan_sentences
from data.tipe_motor_matic import tipe_motor_matic_sentences
from data.layanan_instalasi import layanan_instalasi_sentences

def get_training_data():
    """
    Returns comprehensive training data with 100+ examples per intent category
    Total sentences: 1300+ across 13 intent categories
    """
    
    # Combine all intent data with labels
    training_data = []
    
    # Add harga sentences (100+ examples)
    for sentence in harga_sentences:
        training_data.append((sentence, "harga"))
    
    # Add daftar sentences (100+ examples)
    for sentence in daftar_sentences:
        training_data.append((sentence, "daftar"))
    
    # Add jam_operasional sentences (100+ examples)
    for sentence in jam_operasional_sentences:
        training_data.append((sentence, "jam_operasional"))
    
    # Add garansi sentences (100+ examples)
    for sentence in garansi_sentences:
        training_data.append((sentence, "garansi"))
        
    # Add booking_pemasangan sentences (100+ examples)
    for sentence in booking_pemasangan_sentences:
        training_data.append((sentence, "booking_pemasangan"))
        
    # Add kategori_mounting_body sentences (100+ examples)
    for sentence in kategori_mounting_body_sentences:
        training_data.append((sentence, "kategori_mounting_body"))
        
    # Add kategori_lighting sentences (100+ examples)  
    for sentence in kategori_lighting_sentences:
        training_data.append((sentence, "kategori_lighting"))
        
    # Add pengiriman sentences (100+ examples)
    for sentence in pengiriman_sentences:
        training_data.append((sentence, "pengiriman"))
        
    # Add durasi_pengiriman sentences (100+ examples)
    for sentence in durasi_pengiriman_sentences:
        training_data.append((sentence, "durasi_pengiriman"))
        
    # Add wilayah_pemasangan sentences (100+ examples)
    for sentence in wilayah_pemasangan_sentences:
        training_data.append((sentence, "wilayah_pemasangan"))
        
    # Add tipe_motor_matic sentences (100+ examples)
    for sentence in tipe_motor_matic_sentences:
        training_data.append((sentence, "tipe_motor_matic"))
        
    # Add stok_produk sentences (100+ examples)
    for sentence in stok_produk_sentences:
        training_data.append((sentence, "stok_produk"))
        
    # Add layanan_instalasi sentences (100+ examples)
    for sentence in layanan_instalasi_sentences:
        training_data.append((sentence, "layanan_instalasi"))
    
    print(f"✅ Loaded training data: {len(training_data)} total sentences")
    print(f"📊 Distribution:")
    print(f"   - Harga: {len(harga_sentences)} sentences")
    print(f"   - Daftar: {len(daftar_sentences)} sentences") 
    print(f"   - Jam Operasional: {len(jam_operasional_sentences)} sentences")
    print(f"   - Garansi: {len(garansi_sentences)} sentences")
    print(f"   - Booking Pemasangan: {len(booking_pemasangan_sentences)} sentences")
    print(f"   - Kategori Mounting Body: {len(kategori_mounting_body_sentences)} sentences")
    print(f"   - Kategori Lighting: {len(kategori_lighting_sentences)} sentences")
    print(f"   - Pengiriman: {len(pengiriman_sentences)} sentences")
    print(f"   - Durasi Pengiriman: {len(durasi_pengiriman_sentences)} sentences")
    print(f"   - Wilayah Pemasangan: {len(wilayah_pemasangan_sentences)} sentences")
    print(f"   - Tipe Motor Matic: {len(tipe_motor_matic_sentences)} sentences")
    print(f"   - Stok Produk: {len(stok_produk_sentences)} sentences")
    print(f"   - Layanan Instalasi: {len(layanan_instalasi_sentences)} sentences")
    
    return training_data

# Expose the training data function
if __name__ == "__main__":
    data = get_training_data()
    print(f"\n🎯 Total training examples: {len(data)}")
    print(f"📈 Average per category: {len(data) / 13:.1f} sentences")
    print(f"🚀 Ready for high-performance training!")
