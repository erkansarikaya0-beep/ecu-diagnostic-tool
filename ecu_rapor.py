import can
import time
from datetime import datetime

# PEAK USB bağlantı ayarları
try:
    bus = can.interface.Bus(channel='PCAN1', bustype='pcan', bitrate=250000)
    print("✓ PEAK USB başarıyla bağlandı!")
except Exception as e:
    print(f"✗ PEAK USB bağlantı hatası: {e}")
    print("→ Simülasyon modunda devam ediyoruz...\n")
    bus = None

# Test CAN Mesajları
test_mesajlari = [
    can.Message(arbitration_id=0x18DAFA00, data=[0x62, 0xA5, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00]),
    can.Message(arbitration_id=0x18DAF00A, data=[0x23, 0x24, 0x60, 0x00, 0x31, 0xAC, 0x00, 0x04]),
    can.Message(arbitration_id=0x18DAFA00, data=[0x7F, 0x23, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00]),
]

print("=" * 50)
print("CAN BUS SNIFFER - PEAK USB TEST")
print("=" * 50)
print(f"Başlangıç: {datetime.now().strftime('%H:%M:%S')}\n")

if bus:
    print("LIVE MOD - Gerçek CAN Verisi Dinleniyor...\n")
    try:
        for i, msg in enumerate(bus):
            print(f"[{i}] ID: 0x{msg.arbitration_id:X} | Data: {msg.data.hex()}")
            if i > 20:
                break
    except KeyboardInterrupt:
        print("\n✓ Durduruldu")
else:
    print("TEST MOD - Simüle Edilmiş CAN Verisi\n")
    for i, msg in enumerate(test_mesajlari):
        print(f"[{i}] ID: 0x{msg.arbitration_id:X} | Data: {msg.data.hex()}")
        time.sleep(0.5)

print("\n" + "=" * 50)
print("Test Tamamlandı")
print("=" * 50)
