import can
import time
from datetime import datetime

# ECU Veri Tabanı
ecu_veri = {
    "Marka": "Bosch",
    "Yazılım": "v61",
    "VIN": "5802245368",
    "Seri No": "065816740361040",
    "Durum": "OK"
}

# CAN ID → ECU Bilgisi
can_id_veri_tabani = {
    0x18DAFA00: {"ad": "Motor Durumu", "hata_kodu": "50FD", "durum": "KRİTİK - ECU Sistemi", "seviye": "🔴 KRITIK"},
    0x18DAF00A: {"ad": "Elektrik Sistemi", "hata_kodu": "50FE", "durum": "UYARI - Sistem Durumu", "seviye": "🟡 UYARI"},
    0x18DAFA01: {"ad": "Yazılım Kimliği", "hata_kodu": "F180", "durum": "BİLGİ - Boot Yazılım", "seviye": "🔵 BİLGİ"},
    0x18DAFA02: {"ad": "VIN Numarası", "hata_kodu": "F190", "durum": "BİLGİ - VIN", "seviye": "🔵 BİLGİ"},
}

def can_id_decode(can_id):
    """CAN ID'yi ECU verisine çevir"""
    if can_id in can_id_veri_tabani:
        return can_id_veri_tabani[can_id]
    else:
        return {"ad": "BİLİNMEYEN", "hata_kodu": "XXXX", "durum": "Tanımlı değil", "seviye": "⚪ UNKNOWN"}

# Test CAN Mesajları
test_mesajlari = [
    can.Message(arbitration_id=0x18DAFA00, data=[0x62, 0xA5, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00]),
    can.Message(arbitration_id=0x18DAF00A, data=[0x23, 0x24, 0x60, 0x00, 0x31, 0xAC, 0x00, 0x04]),
    can.Message(arbitration_id=0x18DAFA01, data=[0x7F, 0x23, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00]),
    can.Message(arbitration_id=0x18DAFA02, data=[0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
]

# Rapor oluştur
rapor = []
rapor.append("=" * 70)
rapor.append("TÜRK TRAKTÖR - ECU DIAGNOSTIC RAPOR")
rapor.append("=" * 70)
rapor.append(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")

rapor.append(">>> ECU KİMLİK BİLGİSİ:")
for anahtar, deger in ecu_veri.items():
    rapor.append(f"  {anahtar}: {deger}")

rapor.append("\n>>> BULUNAN HATALAR:\n")

toplam_kritik = 0
toplam_uyari = 0
toplam_bilgi = 0

for i, msg in enumerate(test_mesajlari):
    veri = can_id_decode(msg.arbitration_id)
    rapor.append(f"[{i+1}] {veri['seviye']} {veri['hata_kodu']} - {veri['durum']}")
    rapor.append(f"    CAN ID: 0x{msg.arbitration_id:X} | Veri: {msg.data.hex()}")
    
    if "KRITIK" in veri['seviye']:
        toplam_kritik += 1
    elif "UYARI" in veri['seviye']:
        toplam_uyari += 1
    elif "BİLGİ" in veri['seviye']:
        toplam_bilgi += 1

rapor.append("\n" + "=" * 70)
rapor.append("ÖZETLEMESİ")
rapor.append("=" * 70)
rapor.append(f"🔴 KRİTİK HATA:  {toplam_kritik}")
rapor.append(f"🟡 UYARI:        {toplam_uyari}")
rapor.append(f"🔵 BİLGİ:        {toplam_bilgi}")
rapor.append(f"TOPLAM MESAJ:    {len(test_mesajlari)}")
rapor.append("=" * 70)

# Raporu ekranda yazdır
for satir in rapor:
    print(satir)

# Raporu dosyaya kaydet
with open("ECU_RAPOR.txt", "w", encoding="utf-8") as f:
    for satir in rapor:
        f.write(satir + "\n")

print("\n✓ Rapor kaydedildi: ECU_RAPOR.txt")