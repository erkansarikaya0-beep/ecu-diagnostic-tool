import can
import time
from datetime import datetime

# CAN ID → ECU Bilgisi Sözlüğü (J1939 formatında)
can_id_veri_tabani = {
    0x18DAFA00: {
        "ad": "Motor Durumu",
        "hata_kodu": "50FD",
        "durum": "KRİTİK - ECU Sistemi",
        "seviye": "🔴 KRITIK"
    },
    0x18DAF00A: {
        "ad": "Elektrik Sistemi",
        "hata_kodu": "50FE",
        "durum": "UYARI - Sistem Durumu",
        "seviye": "🟡 UYARI"
    },
    0x18DAFA01: {
        "ad": "Yazılım Kimliği",
        "hata_kodu": "F180",
        "durum": "BİLGİ - Boot Yazılım",
        "seviye": "🔵 BİLGİ"
    },
    0x18DAFA02: {
        "ad": "VIN Numarası",
        "hata_kodu": "F190",
        "durum": "BİLGİ - VIN",
        "seviye": "🔵 BİLGİ"
    }
}


def can_id_decode(can_id):
    """CAN ID'yi ECU verisine çevir"""
    if can_id in can_id_veri_tabani:
        veri = can_id_veri_tabani[can_id]
        return veri
    else:
        return {
            "ad": "BİLİNMEYEN",
            "hata_kodu": "XXXX",
            "durum": "Tanımlı değil",
            "seviye": "⚪ UNKNOWN"
        }


# Test CAN Mesajları
test_mesajlari = [
    can.Message(arbitration_id=0x18DAFA00, data=[0x62, 0xA5, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00]),
    can.Message(arbitration_id=0x18DAF00A, data=[0x23, 0x24, 0x60, 0x00, 0x31, 0xAC, 0x00, 0x04]),
    can.Message(arbitration_id=0x18DAFA01, data=[0x7F, 0x23, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00]),
    can.Message(arbitration_id=0x18DAFA02, data=[0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
]


print("=" * 60)
print("ECU CAN BUS DECODER - SAMTEC GERÇEKLEŞTİRMESİ")
print("=" * 60)
print(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")

# Her CAN mesajını decode et
toplam_kritik = 0
toplam_uyari = 0
toplam_bilgi = 0

for i, msg in enumerate(test_mesajlari):
    veri = can_id_decode(msg.arbitration_id)
    
    print(f"\n[Mesaj {i+1}]")
    print(f"  CAN ID:      0x{msg.arbitration_id:X}")
    print(f"  Veri Hex:    {msg.data.hex()}")
    print(f"  Sistem:      {veri['ad']}")
    print(f"  Hata Kodu:   {veri['hata_kodu']}")
    print(f"  Açıklama:    {veri['durum']}")
    print(f"  Seviye:      {veri['seviye']}")
    
    # İstatistik topla
    if "KRITIK" in veri['seviye']:
        toplam_kritik += 1
    elif "UYARI" in veri['seviye']:
        toplam_uyari += 1
    elif "BİLGİ" in veri['seviye']:
        toplam_bilgi += 1


print("\n" + "=" * 60)
print("ÖZETLEMESİ")
print("=" * 60)
print(f"🔴 KRİTİK HATA:  {toplam_kritik}")
print(f"🟡 UYARI:        {toplam_uyari}")
print(f"🔵 BİLGİ:       {toplam_bilgi}")
print(f"TOPLAM MESAJ:   {len(test_mesajlari)}")
print("=" * 60)