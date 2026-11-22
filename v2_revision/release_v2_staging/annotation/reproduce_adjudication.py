"""Reproduce the adjudicated Study 1 split from the released files (no private inputs).
Checks the frozen hashes (FREEZE_ADJ.json; the key is frozen under its working name KEY_ADJ_PRIVATE_do_not_send.json and
released as adjudication_key.json with identical bytes), then applies the rule in ADJUDICATION_PROTOCOL.md."""
import json, hashlib
from pathlib import Path
H = Path(__file__).resolve().parent
fr = json.load(open(H / "FREEZE_ADJ.json", encoding="utf-8"))["sha256"]
alias = {"KEY_ADJ_PRIVATE_do_not_send.json": "adjudication_key.json"}
for f, h in fr.items():
    assert hashlib.sha256((H / alias.get(f, f)).read_bytes()).hexdigest() == h, "hash mismatch: " + f
print("FREEZE_ADJ: all", len(fr), "hashes MATCH")
key = json.load(open(H / "adjudication_key.json", encoding="utf-8"))
lab = json.load(open(H / "adjudicator_labels.json", encoding="utf-8"))
att_ok = all(lab[e["item_id"]]["r01"] == e["gold"]["r01"] for e in key if e["role"] == "attention")
print("attention:", "PASS" if att_ok else "FAIL")
ROWS = {"b18": 3, "b22": 7}
MAP = {"VIOLATED": "genuine miss", "CANNOT TELL": "ambiguous"}
final = {"ambiguous": 9, "genuine miss": 6, "unresolved (split)": 0}
for e in key:
    if e["role"] == "attention":
        continue
    x = lab[e["item_id"]][e["target_rule"]]
    print(e["case"], e["condition"], e["role"], "target", e["target_rule"], "->", x)
    if e["role"] == "contested":
        final[MAP[x] if (att_ok and x in MAP) else "unresolved (split)"] += ROWS[e["case"]]
print("adjudicated split of the 25 valid Study 1 omission nondetections:", final)
