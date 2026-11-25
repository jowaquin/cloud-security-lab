"""
config.py

Konfigurasi checkout-service TokoNusa.

PERHATIAN: file ini sengaja berisi API key yang bocor, dipakai sebagai
bahan latihan Pertemuan 11 (secret scanning). Kredensial di bawah ini
adalah contoh resmi milik AWS sendiri yang dipublikasikan di dokumentasi
AWS sebagai placeholder aman (bukan kredensial sungguhan), tapi format
angka dan hurufnya sengaja dibuat identik dengan AWS Access Key asli
supaya bisa terdeteksi oleh scanner secret seperti Trivy.
"""

import os

DATABASE_URL = "postgresql://tokonusa_user@localhost:5432/tokonusa_db"

# Baris di bawah ini adalah penyebab masalahnya: API key tertanam
# langsung di kode, bukan diambil dari environment variable.
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

APP_NAME = "checkout-service"
APP_PORT = int(os.environ.get("PORT", 8000))
