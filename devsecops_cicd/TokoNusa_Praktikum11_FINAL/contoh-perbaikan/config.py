"""
config.py (versi revisi)

Konfigurasi checkout-service TokoNusa, sudah diperbaiki: kredensial AWS
tidak lagi tertanam langsung di kode, melainkan diambil dari environment
variable. Nilai environment variable itu sendiri diisi di luar kode
(mis. lewat secret manager atau file .env yang tidak ikut di-commit).
"""

import os

DATABASE_URL = "postgresql://tokonusa_user@localhost:5432/tokonusa_db"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

APP_NAME = "checkout-service"
APP_PORT = int(os.environ.get("PORT", 8000))
