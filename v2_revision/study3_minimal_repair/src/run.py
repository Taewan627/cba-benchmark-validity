"""Study 3 runner. Resumable: every finished call is appended to
outputs/raw_attempts.jsonl and skipped on restart. Budget stop at USD 9.
Usage: python3 src/run.py [--dry] [--max-seconds N] [--limit N] [--workers N]"""
import argparse, hashlib, json, sys, threading, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from frozen import protocol_construction as pc

BASE = HERE.parent
CASES = BASE / "data" / "study3_cases.jsonl"
RAW = BASE / "outputs" / "raw_attempts.jsonl"
KEYFILE = BASE.parent / ".secrets" / "openrouter_key.txt"
MODELS = ["google/gemini-3.8-flash", "anthropic/claude-sonnet-5", "openai/gpt-6.1-sol",
          "deepseek/deepseek-v4.1-flash-1017", "qwen/qwen3.8-27b"]
NO_TEMPERATURE = {"openai/gpt-6.1-sol", "anthropic/claude-sonnet-5"}  # temperature not in supported_parameters
PROTOCOLS = ["P1", "P2", "P3", "P4"]
REPS = [0, 1, 2]
BUDGET = 9.0
URL = "https://openrouter.ai/api/v1/chat/completions"


def prompt_hash(messages):
    return hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest()[:16]


def plan():
    cases = [json.loads(l) for l in CASES.open(encoding="utf-8")]
    jobs = {}
    for c in cases:
        for p in PROTOCOLS:
            msgs = pc.build_messages(c, p)
            ph = prompt_hash(msgs)
            for m in MODELS:
                for r in REPS:
                    jobs.setdefault((m, p, r, ph), msgs)
    return jobs


def key():
    import re
    return re.search(r"sk-or-[A-Za-z0-9_-]+", KEYFILE.read_text()).group(0)


def call(k, model, messages, rep, with_reasoning_off=True):
    body = {"model": model, "messages": messages, "max_tokens": 6000,
            "response_format": {"type": "json_object"}, "seed": 1731 + rep,
            "usage": {"include": True}}
    if model not in NO_TEMPERATURE:
        body["temperature"] = 0
    if with_reasoning_off:
        body["reasoning"] = {"enabled": False}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json",
                                          "X-Title": "CBA Study 3"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return body, json.loads(r.read().decode())


def do_job(k, job, msgs):
    model, proto, rep, ph = job
    rec = {"model": model, "protocol": proto, "rep": rep, "prompt_hash": ph,
           "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "attempts": []}
    reasoning_off = True
    for attempt in range(3):
        try:
            body, resp = call(k, model, msgs, rep, reasoning_off)
            ch = (resp.get("choices") or [{}])[0]
            rec.update(ok=True, reasoning_off_sent=reasoning_off,
                       request={kk: vv for kk, vv in body.items() if kk != "messages"},
                       returned_model=resp.get("model"), provider=resp.get("provider"),
                       content=(ch.get("message") or {}).get("content"),
                       finish_reason=ch.get("finish_reason"), usage=resp.get("usage"),
                       error=resp.get("error"))
            return rec
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            rec["attempts"].append({"http": e.code, "body": msg})
            if e.code == 400 and reasoning_off and "reason" in msg.lower():
                reasoning_off = False          # provider rejects disabling; record and use default
                continue
            if e.code in (402, 403):
                rec.update(ok=False, fatal=True); return rec
        except Exception as e:  # transport
            rec["attempts"].append({"exception": repr(e)[:300]})
        time.sleep(2)
    rec.update(ok=False)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true"); ap.add_argument("--max-seconds", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--models", default="")
    a = ap.parse_args()
    jobs = plan()
    done, spent = set(), 0.0
    if RAW.exists():
        for l in RAW.open(encoding="utf-8"):
            r = json.loads(l)
            spent += float(((r.get("usage") or {}).get("cost")) or 0)
            if r.get("ok"):
                done.add((r["model"], r["protocol"], r["rep"], r["prompt_hash"]))
    todo = [j for j in jobs if j not in done and (not a.models or j[0] in a.models.split(","))]
    if a.limit: todo = todo[:a.limit]
    print(f"planned={len(jobs)} done={len(done)} todo={len(todo)} spent=${spent:.4f}", flush=True)
    if a.dry: return
    RAW.parent.mkdir(exist_ok=True)
    k, lock, t0, stop = key(), threading.Lock(), time.time(), threading.Event()
    n = 0
    with ThreadPoolExecutor(a.workers) as ex, RAW.open("a", encoding="utf-8") as out:
        futs = {}
        it = iter(todo)
        def submit_next():
            if stop.is_set(): return
            j = next(it, None)
            if j: futs[ex.submit(do_job, k, j, jobs[j])] = j
        for _ in range(a.workers): submit_next()
        while futs:
            for f in as_completed(list(futs)):
                futs.pop(f); r = f.result()
                with lock:
                    out.write(json.dumps(r, ensure_ascii=False) + "\n"); out.flush()
                    spent += float(((r.get("usage") or {}).get("cost")) or 0); n += 1
                if r.get("fatal") or spent >= BUDGET: stop.set(); print("STOP: budget/fatal", spent, r.get("attempts"), flush=True)
                if a.max_seconds and time.time() - t0 > a.max_seconds: stop.set()
                if n % 50 == 0: print(f"{n} calls, ${spent:.3f}, {time.time()-t0:.0f}s", flush=True)
                submit_next()
                break
    print(f"finished batch: {n} calls, total spent ${spent:.4f}", flush=True)


if __name__ == "__main__":
    main()
