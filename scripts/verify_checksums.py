"""Verify SHA256SUMS.csv against the files in this repository (offline, stdlib only).

    python scripts/verify_checksums.py
"""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
bad = 0
with open(ROOT / "SHA256SUMS.csv", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        data = (ROOT / row["path"]).read_bytes()
        ok = hashlib.sha256(data).hexdigest() == row["sha256"] and len(data) == int(row["bytes"])
        if not ok:
            bad += 1
            print("MISMATCH:", row["path"])
print("CHECKSUM VERIFICATION:", "PASS" if bad == 0 else "FAIL")
raise SystemExit(bad)
