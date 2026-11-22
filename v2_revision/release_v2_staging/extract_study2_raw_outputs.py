"""Write sanitized raw model outputs for Study 2 v1 and Study 2b (reviewer request: raw responses incl. q026)
and check them against the frozen parser and frozen scores.

Input: the private raw-attempt archives (provider envelopes, not published), whose SHA-256 equals the value in
the frozen result manifests. Output keeps only the returned assistant text and non-identifying fields
(no prompts, headers, request/generation ids, billing, or timestamps), in the same schema as the released
Study 1 extract. Usage:
    python extract_study2_raw_outputs.py <private_outputs_dir> <public_release_dir> <out_dir>
"""
import hashlib, importlib.util, json, re, sys
from pathlib import Path

SRC, PUB, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("cba_parser", PUB / "code" / "parser.py")
parser = importlib.util.module_from_spec(spec); spec.loader.exec_module(parser)
jl = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
STUDIES = {"study2_v1": ("study2_scope_v1", "study2_scope_cases.jsonl"),
           "study2b": ("study2b_scope_v1", "study2b_scope_cases.jsonl")}
ok_all = True
for name, (srcdir, cases) in STUDIES.items():
    raw_path = SRC / srcdir / "raw_attempts.jsonl"
    h = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    manifest = json.loads((PUB / "results" / name / "result_manifest.json").read_text(encoding="utf-8"))
    hash_ok = h in json.dumps(manifest)
    rules = {c["base_case_id"]: set(re.findall(r"\((r\d+)\)", c["setup"])) for c in jl(PUB / "data" / cases)}
    scores = {(s["model"], s["protocol"], s["condition"], s["base_case_id"]): s["valid"] for s in jl(PUB / "results" / name / "scores.jsonl")}
    out, mism = [], 0
    for r in jl(raw_path):
        if not r.get("final_attempt", True):
            continue
        text, fin = None, r.get("finish_reason")
        if r.get("raw_response"):
            env = json.loads(r["raw_response"])
            ch = (env.get("choices") or [{}])[0]
            text = (ch.get("message") or {}).get("content")
            fin = ch.get("finish_reason", fin)
        err = None if not r.get("error") else str(r["error"]).split(":")[0][:60]
        key = (r["requested_model"], r["protocol"], r["condition"], r["base_case_id"])
        valid = parser.parse(text, rules[r["base_case_id"]], r["protocol"])["valid"] if text else False
        if valid != scores[key]:
            mism += 1; print("MISMATCH", name, key)
        out.append(dict(base_case_id=r["base_case_id"], condition=r["condition"], protocol=r["protocol"], model=r["requested_model"],
                        prompt_hash=r.get("prompt_hash"), finish_reason=fin, error_type=err, response_text=text, frozen_parse_valid=scores[key]))
    dst = OUT / f"{name}_raw_model_outputs_public.jsonl"
    dst.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out), encoding="utf-8")
    txt = dst.read_text(encoding="utf-8")
    leak = any(t in txt for t in ("sk-or-", "Bearer", "gen-1", "Authorization"))
    print(f"{name}: rows {len(out)}, archive hash matches frozen manifest: {hash_ok}, parse mismatches: {mism}, leak tokens: {leak}")
    ok_all &= hash_ok and mism == 0 and not leak and len(out) == len(scores)
print("STUDY 2 RAW EXTRACT CHECK:", "PASS" if ok_all else "FAIL")
