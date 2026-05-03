import os

# Klasördeki tüm HEX dosyalarını bul
hex_files = [f for f in os.listdir('.') if f.endswith('.hex')]

print(f"Bulunan HEX dosyaları: {len(hex_files)}\n")

for dosya in hex_files:
    with open(dosya, encoding='latin-1') as f:
        lines = f.readlines()
    
    print(f"📄 {dosya}")
    print(f"   Satır: {len(lines)} | Boyut: {os.path.getsize(dosya) / 1024:.1f} KB")
    print(f"   İlk satır: {lines[0][:80] if lines else 'Boş'}")
    print()
    