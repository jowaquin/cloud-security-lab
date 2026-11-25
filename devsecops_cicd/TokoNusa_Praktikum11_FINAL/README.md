# Praktikum 11 TokoNusa | DevSecOps & CI/CD Security

**Untuk:** mahasiswa S1 Informatika, Ubuntu di WSL2 + Docker Desktop. Tidak memakai AWS nyata.

## Struktur

```text
TokoNusa_Praktikum11_FINAL/
  ci-gate.sh                  # status PASS/BLOCKED/ERROR
  trivy-secret.yaml           # aturan demo untuk placeholder AWS
  repo-dummy/
    config.py                 # KONDISI AWAL: hardcoded key pada baris 20–21
    app.py
    .gitignore
  contoh-perbaikan/config.py # KONDISI AKHIR: os.environ.get(...)
  tests/evaluate_report.py    # memeriksa laporan JSON Trivy
  tests/test_evaluate_report.py
```

## Langkah

```bash
cd ~/cloudsecurity/TokoNusa_Praktikum11_FINAL
export TRIVY_IMAGE=aquasec/trivy:0.75.0   # opsional: kunci versi Trivy
python3 repo-dummy/app.py
docker info
chmod +x ci-gate.sh
./ci-gate.sh; echo $?          # seharusnya BLOCKED, 1
cp contoh-perbaikan/config.py repo-dummy/config.py
python3 repo-dummy/app.py
./ci-gate.sh; echo $?          # seharusnya PASS, 0
python3 -m unittest discover -s tests -v
```

Jika folder diekstrak di lokasi lain, masuklah ke lokasi tersebut. Script menentukan lokasi dari dirinya sendiri, bukan dari `pwd`.

## Prinsip

* Trivy punya allow rule bawaan `examples` yang mengabaikan teks yang mengandung kata "example" (termasuk `AKIAIOSFODNN7EXAMPLE`). Karena itu `trivy-secret.yaml` memakai `disable-allow-rules` dengan `examples`. Tanpa baris itu, Trivy 0.75.0 melaporkan PASS pada kunci contoh.
* Aturan custom menangkap assignment kunci AWS-format pada **file Python** sebagai simulasi agar placeholder publik tidak dilewatkan aturan bawaan. Ini **bukan pengganti konfigurasi produksi**.
* CLI Trivy `fs` di sini mengaudit **working tree** dan tidak membuktikan riwayat Git bersih.
* PASS tidak berarti aman untuk deploy: artinya tidak ada temuan pada cakupan pemeriksaan ini.
* Jika ini kredensial sungguhan: segera nonaktifkan/cabut, investigasi penyalahgunaan, rotasi, kemudian sanitasi riwayat bersama tim.
* Saat Docker atau Trivy gagal, gate mengeluarkan ERROR dan status 1, bukan keliru menyatakan secret terdeteksi.
* Contoh file `.env` tidak digunakan. Jangan masukkan kredensial sungguhan ke praktikum.

Rujukan: https://trivy.dev/docs/latest/scanner/secret/ | https://csrc.nist.gov/pubs/sp/800/218/final
