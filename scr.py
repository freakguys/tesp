import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# --- KONFIGURASI ---
# GANTI URL DI BAWAH INI DENGAN WEBSITE TARGET ANDA
URL_TARGET = "https://paid.fridom.qzz.io/api/v1/sub?vpn=vless&port=443&cc=ID&domain=bug.com&format=raw&limit=10"
OUTPUT_FILE = "tes.txt"
# -------------------

try:
    # Mengambil konten halaman
    print(f"Mengambil konten dari: {URL_TARGET}")
    response = requests.get(URL_TARGET)
    response.raise_for_status() # Akan memunculkan error untuk kode status HTTP yang buruk (4xx atau 5xx)

    soup = BeautifulSoup(response.text, 'html.parser')

    # --- EKSTRAKSI KONTEN ---
    # Ganti bagian di bawah ini sesuai dengan data yang ingin Anda ambil.
    # Contoh ini mengambil judul halaman dan semua teks dalam tag <p> (paragraf).
    title = soup.find('title').get_text() if soup.find('title') else 'Judul Tidak Ditemukan'
    
    # Mengumpulkan teks dari semua paragraf
    all_paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    
    # Membuat struktur data JSON
    data_scraped = {
        "url": URL_TARGET,
        "timestamp": datetime.now().isoformat(),
        "page_title": title,
        "total_paragraphs": len(all_paragraphs),
        "sample_content": all_paragraphs[:5] # Menyimpan 5 paragraf pertama sebagai sampel
    }
    # ------------------------

    # Menyimpan data ke file JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_scraped, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Data berhasil disimpan ke {OUTPUT_FILE}")

except requests.exceptions.RequestException as e:
    print(f"❌ Error HTTP atau Koneksi: {e}")
    # Keluar dengan kode status error agar Action gagal
    exit(1)
except Exception as e:
    print(f"❌ Terjadi Error saat Scraping/Parsing: {e}")
    exit(1)
