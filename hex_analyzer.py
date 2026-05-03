import os
import re

# HEX dosyasını bul
hex_files = [f for f in os.listdir('.') if f.endswith('.hex')]
dosya = hex_files[0] if hex_files else None

if not dosya:
    print("HEX dosyası bulunamadı!")
    exit()

print(f"📂 Dosya: {dosya}\n")

with open(dosya, encoding="latin-1") as f:
    lines = f.readlines()

print(f"✓ Toplam satır: {len(lines)}")
print(f"✓ Dosya boyutu: {os.path.getsize(dosya) / 1024 / 1024:.2f} MB\n")

# HEX analizi
toplam_byte = 0
adresler = set()

for i, line in enumerate(lines[:20]):  # İlk 20 satırı analiz et
    line = line.strip()
    if not line:
        continue
    
    # Intel HEX format: :LLAAAATTDD...CC
    # LL = byte sayısı, AAAA = adres
    if line.startswith(':'):
        byte_count = int(line[1:3], 16)
        address = int(line[3:7], 16)
        record_type = int(line[7:9], 16)
        
        toplam_byte += byte_count
        adresler.add(address)
        
        print(f"[{i}] Adres: 0x{address:04X} | Byte: {byte_count} | Tip: {record_type}")

print(f"\n📊 İstatistik:")
print(f"  Toplam Byte: {toplam_byte}")
print(f"  Farklı Adresler: {len(adresler)}")
print(f"  Min Adres: 0x{min(adresler):04X}")
print(f"  Max Adres: 0x{max(adresler):04X}")
