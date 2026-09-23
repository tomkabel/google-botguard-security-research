"""Aggregate testbed + attacker logs into per-config metrics (feeds paper §5.6).

  python analyze.py [--logs logs] [--params ../analysis/params.json] [--json]
  python analyze.py --selfcheck

Prices: params.json "prices_usd_per_mtok" and/or "prices_eur_per_mtok", each
{"value": {"<model id>": {"input": x, "output": y}}}. No prices are hard-coded; a model id missing
from params.json gives cost = None. Runs are grouped per (config, model); cost is reported in the
model's price currency. `--summary` writes results/summary.md + results/summary.json.
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
        cfg[r["config"] + (f" / {r['model']}" if r.get("model") else "")].append(r)
    out = {}
    for c, rs in sorted(cfg.items()):
        ok, hp, wd, own, dur, act, tin, tout, cost, verif, llm, ncall = 0, 0, 0, 0, [], [], 0, 0, 0.0, [], [], []
        priced = True
        for r in rs:
            ev = by_run.get(r["run_id"], [])
            # server-side flow_done is authoritative; attacker's own flag only if no server log exists
            success = any(e["kind"] == "flow_done" for e in ev) if ev else bool(r.get("success"))
            ok += success
            hp += any(e["kind"] == "honeypot" for e in ev)
            wd += any(e.get("webdriver") for e in ev)  # page script reports navigator.webdriver on load
            own += bool(r.get("success"))  # attacker's own flag; for d-hybrid = scripted control resumed
            verif += [e["verified"] for e in ev if e["kind"] == "verify" and e.get("verified") is not None]
            dur.append(r["end"] - r["start"])
            act += [a["dur_s"] for a in r["actions"] if a["kind"] != "launch"]
            llm += [x["latency_s"] for x in r.get("llm_calls", []) if "latency_s" in x]
            ncall.append(sum("latency_s" in x for x in r.get("llm_calls", [])))
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
            "honeypot_rate": hp / n, "honeypot_runs": hp, "webdriver_runs": wd, "attacker_flag_runs": own,
            "vendor_verify_pass_rate": (sum(verif) / len(verif)) if verif else None,
            "run_s": {"median": statistics.median(dur), "p90": pct(dur, 0.9)},
            "action_s": {"p10": pct(act, 0.1), "median": pct(act, 0.5), "p90": pct(act, 0.9), "n": len(act)},
            "tokens_per_success": {"input": tin / ok, "output": tout / ok} if ok else None,
            "llm_call_s": {"median": pct(llm, 0.5), "p90": pct(llm, 0.9), "n": len(llm)},
            "llm_calls_per_run": statistics.median(ncall),
            "tokens_per_call": {"input": tin / len(llm), "output": tout / len(llm)} if llm else None,
            "spend": cost,
            "currency": (prices.get(rs[0].get("model") or "") or {}).get("currency", "USD"),
            "cost_per_success": (cost / ok if ok and priced else None) if (tin or tout) else 0.0,
        }
    return out


DEFAULT_PARAMS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "params.json")


def load_prices(path=DEFAULT_PARAMS):
    if not os.path.exists(path):
        raise SystemExit(f"params file not found: {path}")
    P, out = json.load(open(path)), {}
    for key, cur in (("prices_usd_per_mtok", "USD"), ("prices_eur_per_mtok", "EUR")):
        d = P.get(key, {})
        for m, p in d.get("value", d).items():  # analysis/params.json wraps every entry as {"value": ...}
            out[m] = dict(p, currency=cur)
    return out


def summary_md(m):
    """Two markdown tables (behaviour; VLM cost) plus totals. Rows are pasted verbatim into paper §5.7."""
    f = lambda v, s="{:.2f}": "–" if v is None else s.format(v)
    beh = ["| Config | Model | Pass | Honeypot hit | `navigator.webdriver` | Action p50 / p90 (s) | Run p50 (s) |",
           "|---|---|---|---|---|---|---|"]
    vlm = ["| Config | Model | VLM calls/run | VLM call p50 / p90 (s) | LLM tokens in / out per call | Cost per success |",
           "|---|---|---|---|---|---|"]
    notes, spend = [], defaultdict(float)
    for c, x in m.items():
        cfg, _, model = c.partition(" / ")
        n = x["runs"]
        beh.append(f"| {cfg} | {model or '–'} | {x['successes']}/{n} | {x['honeypot_runs']}/{n} | {x['webdriver_runs']}/{n} "
                   f"| {f(x['action_s']['median'])} / {f(x['action_s']['p90'])} | {f(x['run_s']['median'], '{:.1f}')} |")
        if not x["llm_call_s"]["n"]:
            continue
        t, cost = x["tokens_per_call"], x["cost_per_success"]
        cur = "€" if x["currency"] == "EUR" else "$"
        spend[cur] += x["spend"]
        vlm.append(f"| {cfg} | {model} | {x['llm_calls_per_run']:g} | {f(x['llm_call_s']['median'])} / {f(x['llm_call_s']['p90'])} "
                   f"| {t['input']:,.0f} / {t['output']:,.0f} | {'–' if cost is None else f'{cur}{cost:.4f}'} |")
        if cfg == "d-hybrid":
            notes.append(f"- d-hybrid / {model}: scripted control resumed after the VLM step in {x['attacker_flag_runs']}/{n} runs.")
    notes += [f"- Total LLM spend: {cur}{v:.4f}." for cur, v in sorted(spend.items())]
    return "\n".join(beh) + "\n\n" + "\n".join(vlm) + "\n\n" + "\n".join(notes) + "\n"


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
    a, c = m["a-dom"], m["c-vlm / m"]
    assert a["runs"] == 2 and a["successes"] == 1 and a["pass_rate"] == 0.5, a
    assert a["honeypot_rate"] == 0.5 and a["cost_per_success"] == 0.0
    assert a["action_s"]["median"] == 0.3 and a["run_s"]["median"] == 3
    assert c["successes"] == 1 and c["honeypot_rate"] == 0
    assert c["action_s"]["n"] == 2  # launch excluded
    assert c["vendor_verify_pass_rate"] == 0.5
    # 2 runs * (1M*$2 + 0.1M*$10)/1M = $6 spend over 1 success
    assert abs(c["cost_per_success"] - 6.0) < 1e-9, c
    assert c["tokens_per_success"] == {"input": 2_000_000, "output": 200_000}
    assert analyze(runs[2:3], events, {})["c-vlm / m"]["cost_per_success"] is None  # unpriced model
    assert load_prices()["claude-sonnet-4-6"] == {"input": 3.0, "output": 15.0, "currency": "USD"}  # real params.json
    assert load_prices()["glm-5.3-flash"]["currency"] == "EUR"
    md = summary_md(m)
    assert "| c-vlm | m | 1/2 | 0/2 | 0/2 |" in md and "| a-dom | – | 1/2 | 1/2 |" in md, md
    assert md.count("| c-vlm |") == 1  # fixture logs no llm_calls, so no VLM-cost row
    assert c["webdriver_runs"] == 0 and c["attacker_flag_runs"] == 1
    print("selfcheck ok")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", default=os.path.join(here, "logs"))
    ap.add_argument("--params", default=DEFAULT_PARAMS)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selfcheck", action="store_true")
    ap.add_argument("--summary", action="store_true", help="write results/summary.md and summary.json")
    ap.add_argument("--check-paper", action="store_true", help="assert every summary table row appears in paper.md")
    a = ap.parse_args()
    if a.selfcheck:
        return selfcheck()
    runs = [r for p in sorted(glob.glob(os.path.join(a.logs, "runs-*.jsonl"))) for r in read_jsonl(p)]
    srv = os.path.join(a.logs, "server.jsonl")
    events = read_jsonl(srv) if os.path.exists(srv) else []
    prices = load_prices(a.params)
    m = analyze(runs, events, prices)
    if a.check_paper:
        paper = open(os.path.join(here, "..", "paper.md")).read()
        rows = [l for l in summary_md(m).splitlines() if l.startswith("| ")]
        missing = [l for l in rows if l not in paper]
        # reverse direction: a measured-looking row in the paper that the logs no longer produce
        stale = [l for l in paper.splitlines() if l.startswith(("| a-", "| b-", "| c-vlm", "| d-hybrid")) and l not in rows]
        assert not missing and not stale, f"paper.md §5.7 out of sync with logs: missing={missing} stale={stale}"
        return print("paper check OK: every measured row appears verbatim in paper.md")
    if a.summary:
        res = os.path.join(here, "results")
        os.makedirs(res, exist_ok=True)
        json.dump(m, open(os.path.join(res, "summary.json"), "w"), indent=1)
        open(os.path.join(res, "summary.md"), "w").write(summary_md(m))
        return print(summary_md(m))
    if a.json:
        return print(json.dumps(m, indent=2))
    print(f"{'config':<32}{'n':>4}{'pass':>7}{'honeypot':>10}{'vendor':>8}{'run_med_s':>11}{'act_p50':>9}{'act_p90':>9}{'cost/succ':>11}")
    f = lambda v, s="{:.2f}": "-" if v is None else s.format(v)
    for c, x in m.items():
        print(f"{c:<32}{x['runs']:>4}{f(x['pass_rate']):>7}{f(x['honeypot_rate']):>10}{f(x['vendor_verify_pass_rate']):>8}"
              f"{f(x['run_s']['median']):>11}{f(x['action_s']['median'], '{:.3f}'):>9}{f(x['action_s']['p90'], '{:.3f}'):>9}"
              f"{f(x['cost_per_success'], '{:.4f}'):>11}")


if __name__ == "__main__":
    main()
