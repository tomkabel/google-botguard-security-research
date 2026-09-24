"""Aggregate testbed + attacker logs into per-config metrics (feeds paper §5.6).

  python analyze.py [--logs logs] [--params ../analysis/params.json] [--json]
  python analyze.py --selfcheck

Prices: params.json "prices_usd_per_mtok" and/or "prices_eur_per_mtok", each
{"value": {"<model id>": {"input": x, "output": y}}}. No prices are hard-coded; a model id missing
from params.json gives cost = None. Runs are grouped per (config, model); cost is reported in the
model's price currency. `--summary` writes results/summary.md + results/summary.json, and appends
Experiment B (logs/xsite/, cross-site variants) and Experiment A (logs/kinematics.jsonl scored by the
kinematics.py detector trained on Balabit in data/) when their inputs exist.
"""
import argparse, glob, json, math, os, statistics, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # kinematics.py


def read_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def read_runs(d):
    """Base runs live in logs/runs-*.jsonl; experiment runs in logs/xsite/ and logs/kin/ (not globbed here)."""
    return [r for p in sorted(glob.glob(os.path.join(d, "runs-*.jsonl"))) for r in read_jsonl(p)]


def pct(xs, q):
    if not xs:
        return None
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))]


def wilson(k, n, z=1.96):
    """Wilson score 95% interval for k successes in n runs."""
    if not n:
        return None
    p, d = k / n, 1 + z * z / n
    c, h = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


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


def agent_key(r):
    return r["config"] + (f" / {r['model']}" if r.get("model") else "")


def xsite(runs, events, prices):
    """Experiment B: {agent: {variant: stats}}. Success = server flow_done and every step's answer correct
    (base-form events carry no `ok`, so the control counts flow_done only). Variant 0 = base form."""
    by_run = defaultdict(list)
    for e in events:
        by_run[e.get("run")].append(e)
    cells = defaultdict(list)
    for r in runs:
        cells[(agent_key(r), r.get("variant", 0))].append(r)
    out = defaultdict(dict)
    for (agent, v), rs in sorted(cells.items()):
        ok, hp, calls, dur, steps, spend = 0, 0, [], [], [], 0.0
        for r in rs:
            ev = by_run.get(r["run_id"], [])
            sub = [e for e in ev if e["kind"] == "step_submit"]
            ok += any(e["kind"] == "flow_done" for e in ev) and {e["step"] for e in sub if e.get("ok", True)} >= {1, 2, 3, 4, 5}
            hp += any(e["kind"] == "honeypot" for e in ev)
            steps.append(max((e["step"] for e in sub), default=0))
            calls.append(sum("latency_s" in x for x in r.get("llm_calls", [])))
            dur.append(r["end"] - r["start"])
            p = prices.get(r.get("model") or "")
            if p:
                spend += (r["input_tokens"] * p["input"] + r["output_tokens"] * p["output"]) / 1e6
        out[agent][v] = {"runs": len(rs), "successes": ok, "honeypot_runs": hp, "furthest_step_median": statistics.median(steps),
                         "vlm_calls_median": statistics.median(calls), "run_s_median": statistics.median(dur), "spend": spend}
    return dict(out)


def xsite_md(x, desc):
    agents = sorted(x)
    vlm = {a for a in agents if any(c["vlm_calls_median"] for c in x[a].values())}
    lines = ["| Variant | " + " | ".join(agents) + " |", "|---" * (len(agents) + 1) + "|"]
    for v in sorted({v for a in agents for v in x[a]}):
        cells = []
        for a in agents:
            c = x[a].get(v)
            cells.append("–" if c is None else f"{c['successes']}/{c['runs']}" + (
                f" · {c['vlm_calls_median']:g} calls · {c['run_s_median']:.0f} s" if a in vlm else ""))
        lines.append(f"| {'base form (control)' if v == 0 else f'v{v} {desc.get(v, "")}'} | " + " | ".join(cells) + " |")
    tot = []
    for a in agents:
        cs = [c for v, c in x[a].items() if v]
        s, n, sp = sum(c["successes"] for c in cs), sum(c["runs"] for c in cs), sum(c["spend"] for c in cs)
        tot.append(f"{s}/{n}" + (f" · €{sp / s:.4f}/success" if a in vlm and s else ""))
    lines.append("| All variants (v1–v9) | " + " | ".join(tot) + " |")
    hp = {a: sum(c["honeypot_runs"] for c in x[a].values()) for a in agents}
    spend = sum(c["spend"] for a in agents for c in x[a].values())
    notes = [f"- Honeypot hits (runs): " + ", ".join(f"{a} {n}" for a, n in hp.items()) + ".",
             f"- Experiment B LLM spend: €{spend:.4f}."]
    return "\n".join(lines) + "\n\n" + "\n".join(notes) + "\n"


def agent_totals(cells):
    """Per agent: base-form cell, v1-v9 successes/runs, Wilson CI, cost per success (v1-v9 spend / successes)."""
    base, var = cells.get(0, cells.get("0")), [c for v, c in cells.items() if str(v) != "0"]
    s, n, sp = sum(c["successes"] for c in var), sum(c["runs"] for c in var), sum(c["spend"] for c in var)
    return {"base": base, "successes": s, "runs": n, "ci95": wilson(s, n), "cost_per_success": sp / s if sp and s else None}


def ci_str(ci):
    return f"{ci[0]:.0%}–{ci[1]:.0%}" if ci else "–"


def xsite_agents_md(x):
    lines = ["| Agent | Base form | Variants v1–v9 | 95% CI (Wilson) | Cost per success |", "|---|---|---|---|---|"]
    for a in sorted(x):
        t = agent_totals(x[a])
        b = f"{t['base']['successes']}/{t['base']['runs']}" if t["base"] else "–"
        cost = f"€{t['cost_per_success']:.4f}" if t["cost_per_success"] else "–"
        lines.append(f"| {a} | {b} | {t['successes']}/{t['runs']} | {ci_str(t['ci95'])} | {cost} |")
    return "\n".join(lines) + "\n"


def repair(runs, events, prices):
    """a-dom with hand-adapted selectors (logs/repair): lines changed per variant and server-side passes."""
    lines = {r.get("variant", 0): r["lines_changed"] for r in runs}
    cells = xsite(runs, events, prices).get("a-dom-adapted", {})
    return {"lines_changed": {v: lines[v] for v in sorted(lines)}, "cells": cells}


def repair_md(rp):
    vs = sorted(rp["lines_changed"])
    lc, cells = rp["lines_changed"], rp["cells"]
    return "\n".join([
        "| Variant | " + " | ".join(f"v{v}" for v in vs) + " | Total |", "|---" * (len(vs) + 2) + "|",
        "| Lines changed (vs base a-dom script) | " + " | ".join(str(lc[v]) for v in vs) + f" | {sum(lc.values())} |",
        "| Adapted a-dom passes (server) | " + " | ".join(f"{cells[v]['successes']}/{cells[v]['runs']}" for v in vs)
        + f" | {sum(c['successes'] for c in cells.values())}/{sum(c['runs'] for c in cells.values())} |"]) + "\n"


KIN_LABELS = {"a-role": "(a) Playwright CDP click (a-role)", "a-dom": "(a) Playwright el.click() (a-dom)",
              "b-mouse": "(b) scripted xdotool, pointer jumps", "e-smooth": "(e) smoothed OS input, min-jerk",
              "t-a11y / glm-5.3-flash": "(t) text-only LLM on accessibility tree, Playwright click"}


def kin_scores(model, kin_lines, runs):
    """Apply the trained rule and the logistic classifier to browser movements, grouped per agent (config / model)."""
    import kinematics as K
    agent = {r["run_id"]: agent_key(r) for r in runs}
    groups = defaultdict(list)
    for run, segs in K.browser_segments(kin_lines).items():
        if run in agent and segs:  # keyboard-only / el.click() agents produce no pointer movement
            groups[agent[run]] += [K.features(s) for s in segs]
    label = lambda a: KIN_LABELS.get(a) or (f"(c) VLM agent, {a.partition(' / ')[2]}" if a.startswith("c-vlm") else a)
    rule, clf = model["rule"], model["classifier"]
    out = {"Balabit human, held-out users": K.summarize(model["_test_human"], rule, clf),
           "Synthetic straight/teleport, held-out": K.summarize(model["_test_bot"], rule, clf),
           "Synthetic min-jerk, held-out": K.summarize(model["_test_mj"], rule, clf)}
    for a in sorted(groups, key=label):
        out[label(a)] = K.summarize(groups[a], rule, clf)
    return out


def kin_md(model, scores):
    f = lambda v, s: "–" if v is None else s.format(v)
    lines = ["| Movement source | Movements | Flagged as bot (rule) | Flagged (classifier) | Median samples (50 Hz) "
             "| Median straightness | Median duration (s) |", "|---|---|---|---|---|---|---|"]
    for k, s in scores.items():
        share = s["flagged_bot"] / s["movements"] if s["movements"] else None
        cshare = s["flagged_clf"] / s["movements"] if s["movements"] else None
        lines.append(f"| {k} | {s['movements']} | {s['flagged_bot']} ({f(share, '{:.0%}')}) | {s['flagged_clf']} ({f(cshare, '{:.0%}')}) "
                     f"| {f(s['median_samples'], '{:g}')} "
                     f"| {f(s['median_straightness'], '{:.3f}')} | {f(s['median_duration_s'], '{:.2f}')} |")
    r = model["rule"]
    cond = (f"samples < {r['N']} or " if r["N"] > 1 else "") + f"straightness > {r['S']}"
    lines += ["", f"- Rule (grid search over samples < N or straightness > S): bot iff {cond}; fitted on Balabit users "
              f"{', '.join(model['train_users'])} (n = {model['n_train']}), held-out accuracy {model['test_accuracy']:.1%} on users "
              f"{', '.join(model['test_users'])} (n = {model['n_test']}; humans flagged {model['test_human_flagged']:.1%}, "
              f"synthetic bots flagged {model['test_bot_flagged']:.1%}).",
              f"- Classifier: logistic regression (numpy Newton/IRLS, L2) on {', '.join(model['classifier']['features'])}; "
              f"bot class = min-jerk paths with bow and jitter, paired human duration and pause (same generator family as "
              f"e-smooth, so the (e) row is in-distribution). Held-out ROC AUC {model['classifier']['auc']:.4f}; at the "
              f"threshold for {model['classifier']['test_bot_tpr']:.0%} TPR on held-out min-jerk bots, held-out humans "
              f"flagged {model['classifier']['test_human_fpr']:.2%} (n = {model['classifier']['n_test']})."]
    return "\n".join(lines) + "\n"


PAPER_AGENT = {"a-dom": "Scripted, DOM selectors (a-dom)", "a-role": "Scripted, accessibility role (a-role)",
               "b-xdotool": "Scripted, xdotool keyboard (b)"}
PAPER_T = "Text-only LLM on accessibility tree, {} (t)"
PAPER_KIN = {"Balabit human, held-out users": "Balabit humans, held-out users",
             "Synthetic straight/teleport, held-out": "Synthetic straight or teleport moves",
             "(a) Playwright CDP click (a-role)": "Playwright CDP click (a-role)",
             "(b) scripted xdotool, pointer jumps": "Scripted xdotool pointer jumps (b)",
             "(e) smoothed OS input, min-jerk": "Smoothed min-jerk OS input (e)",
             "Synthetic min-jerk, held-out": "Synthetic min-jerk moves (classifier bot class)",
             "(t) text-only LLM on accessibility tree, Playwright click": "Text-only LLM, Playwright click (t)"}


def paper_extra_md(js):
    """Compact rows of paper Tables 5.6 (Experiment B, plus a-dom repair effort) and 5.7 (Experiment A), from
    results/summary.json. Labels avoid the `| a-` / `| b-` / `| c-vlm` / `| d-hybrid` prefixes of the stale check."""
    rows = []
    for a, cells in js.get("experiment_b_xsite", {}).get("cells", {}).items():
        t = agent_totals(cells)
        cfg, _, model = a.partition(" / ")
        label = PAPER_AGENT.get(a) or (PAPER_T.format(model) if cfg == "t-a11y" else f"VLM agent, {model} (c)")
        b = f"{t['base']['successes']}/{t['base']['runs']}" if t["base"] else "–"
        cost = f"€{t['cost_per_success']:.4f}" if t["cost_per_success"] else "–"
        rows.append(f"| {label} | {b} | {t['successes']}/{t['runs']} | {ci_str(t['ci95'])} | {cost} |")
    rp = js.get("experiment_b_repair")
    if rp:
        lc = rp["lines_changed"]
        # prose phrase in §5.7, checked verbatim like the table rows
        rows.append(f"{sum(lc.values())} changed lines over {len(lc)} variants "
                    f"({min(lc.values())}–{max(lc.values())} per variant)")
    for k, v in js.get("experiment_a_kinematics", {}).get("scores", {}).items():
        label = PAPER_KIN.get(k) or f"VLM agent, {k.rpartition(', ')[2]} (c)"
        rows.append(f"| {label} | {v['movements']:,} | {v['flagged_bot'] / v['movements']:.0%} "
                    f"| {v['flagged_clf'] / v['movements']:.0%} |")
    return rows


def selfcheck():
    import kinematics
    kinematics.selfcheck()
    runs = [{"run_id": r, "config": "c-vlm", "model": "m", "variant": v, "start": 0, "end": 30, "input_tokens": 1_000_000,
             "output_tokens": 0, "llm_calls": [{"latency_s": 1}, {"error": "x"}, {"latency_s": 1}]} for r, v in
            (("x1", 3), ("x2", 3), ("x3", 0))] + [{"run_id": "x4", "config": "b-xdotool", "variant": 3, "start": 0, "end": 5}]
    ok5 = lambda run: [{"run": run, "kind": "step_submit", "variant": 3, "step": s, "ok": True} for s in range(1, 6)]
    events = (ok5("x1") + [{"run": "x1", "kind": "flow_done"}]
              + ok5("x2")[:4] + [{"run": "x2", "kind": "step_submit", "step": 5, "ok": False}, {"run": "x2", "kind": "flow_done"}]
              + [{"run": "x3", "kind": "step_submit", "step": s} for s in range(1, 6)] + [{"run": "x3", "kind": "flow_done"}]
              + [{"run": "x4", "kind": "step_submit", "step": 1, "ok": True}, {"run": "x4", "kind": "honeypot"}])
    x = xsite(runs, events, {"m": {"input": 1.0, "output": 0.0}})
    v3, v0, b3 = x["c-vlm / m"][3], x["c-vlm / m"][0], x["b-xdotool"][3]
    assert v3["runs"] == 2 and v3["successes"] == 1 and v3["vlm_calls_median"] == 2 and v3["spend"] == 2.0, v3  # wrong answer = fail
    assert v0["successes"] == 1 and b3["successes"] == 0 and b3["furthest_step_median"] == 1 and b3["honeypot_runs"] == 1
    md = xsite_md(x, {3: "random ids"})
    assert "| v3 random ids | 0/1 | 1/2 · 2 calls · 30 s |" in md and "| All variants (v1–v9) | 0/1 | 1/2 · €2.0000/success |" in md, md
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
    ex = {"experiment_b_xsite": {"cells": {"c-vlm / m": {"0": {"successes": 1, "runs": 1, "spend": 0.1},
                                                         "3": {"successes": 1, "runs": 2, "spend": 0.5}}}},
          "experiment_b_repair": {"lines_changed": {"1": 0, "3": 5}},
          "experiment_a_kinematics": {"scores": {"(c) VLM agent, m": {"movements": 1234, "flagged_bot": 1234, "flagged_clf": 617}}}}
    assert paper_extra_md(ex) == ["| VLM agent, m (c) | 1/1 | 1/2 | 9%–91% | €0.5000 |", "5 changed lines over 2 variants (0–5 per variant)",
                                  "| VLM agent, m (c) | 1,234 | 100% | 50% |"], paper_extra_md(ex)
    lo, hi = wilson(17, 18)
    assert abs(lo - 0.742) < 0.001 and abs(hi - 0.990) < 0.001, (lo, hi)
    assert wilson(0, 0) is None and wilson(0, 5)[0] == 0.0 and wilson(5, 5)[1] == 1.0
    assert xsite_agents_md(x).splitlines()[2] == "| b-xdotool | – | 0/1 | 0%–79% | – |", xsite_agents_md(x)
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
    runs = read_runs(a.logs)
    srv = os.path.join(a.logs, "server.jsonl")
    events = read_jsonl(srv) if os.path.exists(srv) else []
    prices = load_prices(a.params)
    m = analyze(runs, events, prices)
    if a.check_paper:
        paper = open(os.path.join(here, "..", "paper.md")).read()
        rows = [l for l in summary_md(m).splitlines() if l.startswith("| ")]
        sj = os.path.join(here, "results", "summary.json")
        rows += paper_extra_md(json.load(open(sj))) if os.path.exists(sj) else []  # Tables 5.6/5.7 (A needs Balabit to recompute)
        missing = [l for l in rows if l not in paper]
        # reverse direction: a measured-looking row in the paper that the logs no longer produce
        stale = [l for l in paper.splitlines() if l.startswith(("| a-", "| b-", "| c-vlm", "| d-hybrid")) and l not in rows]
        assert not missing and not stale, f"paper.md §5.7 out of sync with logs: missing={missing} stale={stale}"
        return print("paper check OK: every measured row appears verbatim in paper.md")
    if a.summary:
        res = os.path.join(here, "results")
        os.makedirs(res, exist_ok=True)
        md, js = summary_md(m), dict(m)
        xruns = read_runs(os.path.join(a.logs, "xsite"))
        if xruns:  # Experiment B
            sys.path.insert(0, os.path.join(here, "testbed"))
            from server import VARIANTS
            x = xsite(xruns, events, prices)
            js["experiment_b_xsite"] = {"variants": {k: v["desc"] for k, v in VARIANTS.items()}, "cells": x}
            md += "\n## Experiment B: cross-site generalisation (pass = server flow_done with all answers correct)\n\n"
            md += xsite_md(x, {k: v["desc"] for k, v in VARIANTS.items()})
            md += "\n### Per agent (v1–v9 pooled; 95% Wilson interval; cost per success = v1–v9 spend / v1–v9 successes)\n\n"
            md += xsite_agents_md(x)
        rruns = read_runs(os.path.join(a.logs, "repair"))
        if rruns:  # Experiment B script repair: a-dom with per-variant adapted selectors
            rp = repair(rruns, events, prices)
            js["experiment_b_repair"] = rp
            md += "\n### Script repair: a-dom selectors adapted per variant (lines changed, not minutes)\n\n" + repair_md(rp)
        kin = os.path.join(a.logs, "kinematics.jsonl")
        balabit = os.path.join(here, "data", "Mouse-Dynamics-Challenge")
        if os.path.exists(kin) and os.path.isdir(balabit):  # Experiment A
            import kinematics
            model = kinematics.train(balabit)
            scores = kin_scores(model, read_jsonl(kin), xruns + read_runs(os.path.join(a.logs, "kin")))
            js["experiment_a_kinematics"] = {"classifier": {k: v for k, v in model.items() if not k.startswith("_")},
                                             "scores": scores}
            md += "\n## Experiment A: kinematic detector on point-to-click movements\n\n" + kin_md(model, scores)
        elif os.path.exists(kin):
            print(f"skipping Experiment A: clone the Balabit dataset into {balabit}", file=sys.stderr)
        json.dump(js, open(os.path.join(res, "summary.json"), "w"), indent=1)
        open(os.path.join(res, "summary.md"), "w").write(md)
        return print(md)
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
