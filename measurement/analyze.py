"""Aggregate testbed + attacker logs into per-config metrics (feeds paper §5.6).

  python analyze.py [--logs logs] [--params ../analysis/params.json] [--json]
  python analyze.py --selfcheck

Prices: params.json {"prices_usd_per_mtok": {"value": {"<model id>": {"input": x, "output": y}}}}.
No prices are hard-coded; a model id missing from params.json gives $ = None.
"""
import argparse, glob, json, os, statistics
from collections import defaultdict


def read_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def pct(xs, q):
    if not xs:
        return None
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))]


def analyze(runs, events, prices):
    by_run = defaultdict(list)
    for e in events:
        by_run[e.get("run")].append(e)
    cfg = defaultdict(list)
    for r in runs:
        cfg[r["config"]].append(r)
    out = {}
    for c, rs in sorted(cfg.items()):
        ok, hp, dur, act, tin, tout, cost, verif = 0, 0, [], [], 0, 0, 0.0, []
        priced = True
        for r in rs:
            ev = by_run.get(r["run_id"], [])
            # server-side flow_done is authoritative; attacker's own flag only if no server log exists
            success = any(e["kind"] == "flow_done" for e in ev) if ev else bool(r.get("success"))
            ok += success
            hp += any(e["kind"] == "honeypot" for e in ev)
            verif += [e["verified"] for e in ev if e["kind"] == "verify" and e.get("verified") is not None]
            dur.append(r["end"] - r["start"])
            act += [a["dur_s"] for a in r["actions"] if a["kind"] != "launch"]
            tin += r.get("input_tokens", 0)
            tout += r.get("output_tokens", 0)
            p = prices.get(r.get("model") or "")
            if r.get("input_tokens") or r.get("output_tokens"):
                if p:
                    cost += (r["input_tokens"] * p["input"] + r["output_tokens"] * p["output"]) / 1e6
                else:
                    priced = False
        n = len(rs)
        out[c] = {
            "runs": n, "successes": ok, "pass_rate": ok / n,
            "honeypot_rate": hp / n,
            "vendor_verify_pass_rate": (sum(verif) / len(verif)) if verif else None,
            "run_s": {"median": statistics.median(dur), "p90": pct(dur, 0.9)},
            "action_s": {"p10": pct(act, 0.1), "median": pct(act, 0.5), "p90": pct(act, 0.9), "n": len(act)},
            "tokens_per_success": {"input": tin / ok, "output": tout / ok} if ok else None,
            "usd_per_success": (cost / ok if ok and priced else None) if (tin or tout) else 0.0,
        }
    return out


DEFAULT_PARAMS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "params.json")


def load_prices(path=DEFAULT_PARAMS):
    if not os.path.exists(path):
        raise SystemExit(f"params file not found: {path}")
    prices = json.load(open(path)).get("prices_usd_per_mtok", {})
    return prices.get("value", prices)  # analysis/params.json wraps every entry as {"value": ...}


def selfcheck():
    t = 1000.0
    runs = [
        {"run_id": "a1", "config": "a-dom", "model": None, "start": t, "end": t + 2, "success": True,
         "actions": [{"kind": "goto", "dur_s": 0.5}, {"kind": "click", "dur_s": 0.1}], "input_tokens": 0, "output_tokens": 0},
        {"run_id": "a2", "config": "a-dom", "model": None, "start": t, "end": t + 4, "success": True,
         "actions": [{"kind": "click", "dur_s": 0.3}], "input_tokens": 0, "output_tokens": 0},
        {"run_id": "c1", "config": "c-vlm", "model": "m", "start": t, "end": t + 60, "success": True,
         "actions": [{"kind": "launch", "dur_s": 3}, {"kind": "llm", "dur_s": 8}], "input_tokens": 1_000_000, "output_tokens": 100_000},
        {"run_id": "c2", "config": "c-vlm", "model": "m", "start": t, "end": t + 90, "success": False,
         "actions": [{"kind": "llm", "dur_s": 12}], "input_tokens": 1_000_000, "output_tokens": 100_000},
    ]
    events = [{"run": "a1", "kind": "honeypot"}, {"run": "a1", "kind": "flow_done"},
              {"run": "a2", "kind": "load"},  # attacker claimed success, server disagrees
              {"run": "c1", "kind": "flow_done"}, {"run": "c1", "kind": "verify", "verified": True},
              {"run": "c2", "kind": "verify", "verified": False}]
    m = analyze(runs, events, {"m": {"input": 2.0, "output": 10.0}})
    a, c = m["a-dom"], m["c-vlm"]
    assert a["runs"] == 2 and a["successes"] == 1 and a["pass_rate"] == 0.5, a
    assert a["honeypot_rate"] == 0.5 and a["usd_per_success"] == 0.0
    assert a["action_s"]["median"] == 0.3 and a["run_s"]["median"] == 3
    assert c["successes"] == 1 and c["honeypot_rate"] == 0
    assert c["action_s"]["n"] == 2  # launch excluded
    assert c["vendor_verify_pass_rate"] == 0.5
    # 2 runs * (1M*$2 + 0.1M*$10)/1M = $6 spend over 1 success
    assert abs(c["usd_per_success"] - 6.0) < 1e-9, c
    assert c["tokens_per_success"] == {"input": 2_000_000, "output": 200_000}
    assert analyze(runs[2:3], events, {})["c-vlm"]["usd_per_success"] is None  # unpriced model
    assert load_prices()["claude-sonnet-4-6"] == {"input": 3.0, "output": 15.0}  # real params.json is found and parsed
    print("selfcheck ok")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", default=os.path.join(here, "logs"))
    ap.add_argument("--params", default=DEFAULT_PARAMS)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selfcheck", action="store_true")
    a = ap.parse_args()
    if a.selfcheck:
        return selfcheck()
    runs = [r for p in sorted(glob.glob(os.path.join(a.logs, "runs-*.jsonl"))) for r in read_jsonl(p)]
    srv = os.path.join(a.logs, "server.jsonl")
    events = read_jsonl(srv) if os.path.exists(srv) else []
    prices = load_prices(a.params)
    m = analyze(runs, events, prices)
    if a.json:
        return print(json.dumps(m, indent=2))
    print(f"{'config':<12}{'n':>4}{'pass':>7}{'honeypot':>10}{'vendor':>8}{'run_med_s':>11}{'act_p50':>9}{'act_p90':>9}{'$/success':>11}")
    f = lambda v, s="{:.2f}": "-" if v is None else s.format(v)
    for c, x in m.items():
        print(f"{c:<12}{x['runs']:>4}{f(x['pass_rate']):>7}{f(x['honeypot_rate']):>10}{f(x['vendor_verify_pass_rate']):>8}"
              f"{f(x['run_s']['median']):>11}{f(x['action_s']['median'], '{:.3f}'):>9}{f(x['action_s']['p90'], '{:.3f}'):>9}"
              f"{f(x['usd_per_success'], '{:.4f}'):>11}")


if __name__ == "__main__":
    main()
