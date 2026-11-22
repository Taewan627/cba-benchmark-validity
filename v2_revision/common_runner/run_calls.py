"""Shared resumable runner for Study 2c and the Study 2b reruns.
Every finished call is appended to the study's raw_attempts.jsonl; restarts skip finished calls.
Usage: python run_calls.py --study 2c|2brerun [--dry] [--limit N] [--workers N] [--max-seconds N]
Modes: 's3'   = Study 3 request body (reasoning-disable flag sent, dropped on a 400 that mentions reasoning).
       'orig' = original Study 2b request body (model, messages, temperature 0, max_tokens 6000, seed, json_object).
No key is ever printed or written."""
import argparse, hashlib, json, re, sys, threading, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

V2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V2 / "study3_minimal_repair" / "src"))
from frozen import protocol_construction as pc  # frozen v1 renderer

KEYFILE = V2 / ".secrets" / "openrouter_key.txt"
URL = "https://openrouter.ai/api/v1/chat/completions"
S3_MODELS = ["google/gemini-3.8-flash", "anthropic/claude-sonnet-5", "openai/gpt-6.1-sol",
             "deepseek/deepseek-v4.1-flash-1017", "qwen/qwen3.8-27b"]
ORIG_MODELS = ["google/gemini-3.8-flash", "anthropic/claude-sonnet-5"]
NO_TEMPERATURE = {"openai/gpt-6.1-sol", "anthropic/claude-sonnet-5"}

STUDIES = {
    "2c": dict(cases=V2 / "study2c" / "data" / "study2c_cases.jsonl",
               raw=V2 / "study2c" / "outputs" / "raw_attempts.jsonl", budget=7.0,
               plan=[("s3", S3_MODELS, [0, 1])]),
    "2brerun": dict(cases=V2.parent / "public_release" / "data" / "study2b_scope_cases.jsonl",
                    raw=V2 / "study2b_reruns" / "outputs" / "raw_attempts.jsonl", budget=4.0,
                    plan=[("orig", ORIG_MODELS, [1, 2]), ("s3", S3_MODELS[2:] + [], [0])]),
}
# note: 2brerun s3 extra evaluators = the 3 models not used in original 2b; Gemini/Claude get 'orig' reps only.


def key():
    return re.search(r"sk-or-[A-Za-z0-9_-]+", KEYFILE.read_text()).group(0)


def ph(msgs):
    return hashlib.sha256(json.dumps(msgs, sort_keys=True).encode()).hexdigest()[:16]


def plan(cfg):
    cases = [json.loads(l) for l in cfg["cases"].open(encoding="utf-8")]
    jobs = {}
    for c in cases:
        msgs = pc.build_messages(c, "P2")
        cid = "%s|%s" % (c["base_case_id"], c["condition"])
        for mode, models, reps in cfg["plan"]:
            for m in models:
                for r in reps:
                    jobs[(cid, m, r, mode, ph(msgs))] = msgs
    return jobs


def call(k, model, msgs, rep, mode, reasoning_off):
    if mode == "orig":
        body = {"model": model, "messages": msgs, "temperature": 0, "max_tokens": 6000,
                "seed": 1731 + rep, "response_format": {"type": "json_object"}, "usage": {"include": True}}
    else:
        body = {"model": model, "messages": msgs, "max_tokens": 6000,
                "response_format": {"type": "json_object"}, "seed": 1731 + rep, "usage": {"include": True}}
        if model not in NO_TEMPERATURE:
            body["temperature"] = 0
        if reasoning_off:
            body["reasoning"] = {"enabled": False}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json",
                                          "X-Title": "CBA validity study"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return body, json.loads(r.read().decode())


def do_job(k, job, msgs):
    cid, model, rep, mode, h = job
    rec = {"case": cid, "model": model, "rep": rep, "mode": mode, "protocol": "P2", "prompt_hash": h,
           "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "attempts": []}
    reasoning_off = mode == "s3"
    for _ in range(3):
        try:
            body, resp = call(k, model, msgs, rep, mode, reasoning_off)
            ch = (resp.get("choices") or [{}])[0]
            rec.update(ok=True, reasoning_off_sent=reasoning_off,
                       request={a: b for a, b in body.items() if a != "messages"},
                       returned_model=resp.get("model"), provider=resp.get("provider"),
                       content=(ch.get("message") or {}).get("content"),
                       finish_reason=ch.get("finish_reason"), usage=resp.get("usage"), error=resp.get("error"))
            if resp.get("error") and not rec["content"]:
                rec["ok"] = False
                rec["attempts"].append({"resp_error": str(resp.get("error"))[:300]})
                time.sleep(3); continue
            return rec
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            rec["attempts"].append({"http": e.code, "body": msg})
            if e.code == 400 and reasoning_off and "reason" in msg.lower():
                reasoning_off = False; continue
            if e.code in (401, 402, 403):
                rec.update(ok=False, fatal=True); return rec
        except Exception as e:
            rec["attempts"].append({"exception": repr(e)[:300]})
        time.sleep(3)
    rec["ok"] = False
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--study", required=True, choices=list(STUDIES))
    ap.add_argument("--dry", action="store_true"); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8); ap.add_argument("--max-seconds", type=int, default=0)
    a = ap.parse_args()
    cfg = STUDIES[a.study]
    jobs = plan(cfg)
    done, spent = set(), 0.0
    if cfg["raw"].exists():
        for l in cfg["raw"].open(encoding="utf-8"):
            r = json.loads(l)
            spent += float(((r.get("usage") or {}).get("cost")) or 0)
            if r.get("ok"):
                done.add((r["case"], r["model"], r["rep"], r["mode"], r["prompt_hash"]))
    todo = [j for j in jobs if j not in done]
    if a.limit:
        todo = todo[:a.limit]
    print("study=%s planned=%d done=%d todo=%d spent=$%.4f budget=$%.1f" % (a.study, len(jobs), len(done), len(todo), spent, cfg["budget"]), flush=True)
    if a.dry:
        return
    cfg["raw"].parent.mkdir(parents=True, exist_ok=True)
    k, lock, t0, stop, n = key(), threading.Lock(), time.time(), threading.Event(), 0
    with ThreadPoolExecutor(a.workers) as ex, cfg["raw"].open("a", encoding="utf-8") as out:
        futs, it = {}, iter(todo)

        def nxt():
            if stop.is_set():
                return
            j = next(it, None)
            if j:
                futs[ex.submit(do_job, k, j, jobs[j])] = j
        for _ in range(a.workers):
            nxt()
        while futs:
            for f in as_completed(list(futs)):
                futs.pop(f); r = f.result()
                with lock:
                    out.write(json.dumps(r, ensure_ascii=False) + "\n"); out.flush()
                    spent += float(((r.get("usage") or {}).get("cost")) or 0); n += 1
                if r.get("fatal") or spent >= cfg["budget"]:
                    stop.set(); print("STOP budget/fatal spent=%.3f" % spent, flush=True)
                if a.max_seconds and time.time() - t0 > a.max_seconds:
                    stop.set()
                if n % 100 == 0:
                    print("%d calls $%.3f %ds" % (n, spent, time.time() - t0), flush=True)
                nxt()
                break
    print("batch done: %d calls, total spent $%.4f" % (n, spent), flush=True)


if __name__ == "__main__":
    main()
