#!/usr/bin/env python3
"""Nilai laporan Trivy JSON: 0 = no findings; 1 = findings / invalid."""
import json
import sys
from pathlib import Path

def evaluate(path: Path) -> int:
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(report, dict)
        # Trivy JSON biasa memiliki SchemaVersion dan Results, Results dapat kosong.
        assert isinstance(report.get("SchemaVersion"), int)
        results = report.get("Results", [])
        assert isinstance(results, list)
        found = sum(len(result.get("Secrets") or []) for result in results)
    except (OSError, ValueError, AssertionError, AttributeError, TypeError) as exc:
        print(f"ERROR: laporan Trivy tidak valid ({exc}).", file=sys.stderr)
        return 1
    if found:
        print(f"TEMUAN: {found} secret terdeteksi.")
        for result in results:
            for secret in result.get("Secrets") or []:
                print(f"  {result.get('Target','?')}:{secret.get('StartLine','?')} "
                      f"- {secret.get('RuleID', secret.get('Title','secret'))}")
        return 1
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: evaluate_report.py REPORT.json", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(evaluate(Path(sys.argv[1])))
