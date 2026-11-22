import json, sys, io
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2] / "public_release"
sys.path.insert(0, str(ROOT/"code"))
def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
