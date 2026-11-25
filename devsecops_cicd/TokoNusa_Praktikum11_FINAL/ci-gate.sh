#!/usr/bin/env bash
# Praktikum TokoNusa. 0: PASS; 1: temuan atau kegagalan scan (fail-closed).
set -uo pipefail
BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$BASE_DIR/repo-dummy"
RULES="$BASE_DIR/trivy-secret.yaml"
TRIVY_IMAGE="${TRIVY_IMAGE:-aquasec/trivy:latest}"

if [[ ! -f "$TARGET/config.py" || ! -f "$RULES" ]]; then
  echo 'ERROR: config.py atau trivy-secret.yaml tidak ditemukan.' >&2
  exit 1
fi
if ! command -v docker >/dev/null 2>&1; then
  echo 'ERROR: perintah docker tidak ditemukan.' >&2
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo 'ERROR: Docker Engine belum berjalan atau tidak dapat diakses.' >&2
  exit 1
fi

REPORT="$(mktemp)" || exit 1
trap 'rm -f "$REPORT"' EXIT
printf 'Memindai: %s\n' "$TARGET"
# JSON ditulis ke file sementara untuk membedakan temuan dan error scanner.
# Jika Trivy tidak selesai normal, gate tetap memblokir (fail-closed).
if docker run --rm \
    --mount "type=bind,src=$TARGET,dst=/work,readonly" \
    --mount "type=bind,src=$RULES,dst=/trivy-secret.yaml,readonly" \
    "$TRIVY_IMAGE" fs --scanners secret \
    --secret-config /trivy-secret.yaml --format json \
    --output /dev/stdout /work >"$REPORT"; then
  :
else
  status=$?
  echo "ERROR: Trivy/Docker gagal dijalankan (exit $status). Pipeline diblokir." >&2
  exit 1
fi

# Format JSON diperiksa agar laporan kosong/rusak tidak dianggap lolos.
if ! python3 "$BASE_DIR/tests/evaluate_report.py" "$REPORT"; then
  echo 'BLOCKED: laporan mengandung temuan atau tidak dapat divalidasi.' >&2
  exit 1
fi
echo 'PASS: tidak ada temuan secret pada berkas saat ini (cakupan scan terbatas).'
exit 0
