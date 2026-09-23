"""Reproduces every number in paper.md Section 5 from params.json (stdlib only).

Run: python3 analysis/cost_model.py   (or `make numbers`)
Self-check: asserts that each printed number/table appears verbatim in paper.md Section 5.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = {k: v["value"] for k, v in json.loads((ROOT / "analysis/params.json").read_text()).items() if not k.startswith("_")}
M = 1e6


def action_cost(p_in, p_out, t_in=P["t_in"], t_out=P["t_out"]):
    return t_in * p_in / M + t_out * p_out / M


def attempt_cost(m, ctx, p_in=P["p_in_point"], p_out=P["p_out_point"]):
    """m VLM steps; with ctx the k-th step re-sends k screenshots of history (linear growth)."""
    return sum((k if ctx else 1) * P["t_in"] * p_in / M + P["t_out"] * p_out / M for k in range(1, m + 1))


def usd(x):
    return f"${x:.4f}" if x < 0.01 else f"${x:.3f}" if x < 1 else f"${x:.2f}"


def hybrid_table():
    n = P["sweep_n"]
    vlm_lat = sum(P["vlm_step_latency"]) / 2
    ps = P["sweep_p_success"]
    head = "| `f` | Context | Cost/attempt | " + " | ".join(f"Cost/success, P={p}" for p in ps) + " | Latency/attempt |"
    rows = [head, "|" + "---|" * (4 + len(ps))]
    for f in P["sweep_f"]:
        m = round(f * n)
        lat = m * vlm_lat + (n - m) * P["script_step_latency"]
        for ctx in (False, True):
            c = attempt_cost(m, ctx)
            rows.append(f"| {f} | {'accumulated' if ctx else 'none'} | {usd(c)} | "
                        + " | ".join(usd(c / p) for p in ps) + f" | {lat:.0f} s |")
    return "\n".join(rows)


def tier1_table():
    dlo, dhi = P["tier1_device_price"]
    llo, lhi = P["tier1_device_life"]
    olo, ohi = P["tier1_ops_per_device_month"]
    mon_lo, mon_hi = dlo / lhi + olo, dhi / llo + ohi
    mac_mon = P["tier1_cloud_mac_hourly"] * 24 * 30
    rows = ["| Rate limit (tokens/device/origin/day) | Owned used iPhone, low | Owned used iPhone, high | Rented cloud Mac |",
            "|---|---|---|---|"]
    for r in P["tier1_rate_limit_sweep"]:
        t = r * 30
        rows.append(f"| {r} | {usd(mon_lo / t)} | {usd(mon_hi / t)} | {usd(mac_mon / t)} |")
    return mon_lo, mon_hi, mac_mon, "\n".join(rows)


def main():
    out = {}
    (a_lo, a_hi) = action_cost(P["p_in"][0], P["p_out"][0]), action_cost(P["p_in"][1], P["p_out"][1])
    out["action"] = f"${a_lo:.5f}–${a_hi:.3f}"
    n_hi = P["n_actions"][1]
    out["attempt"] = f"${a_lo * n_hi:.4f}–${a_hi * n_hi:.2f}"
    out["hybrid_fold"] = f"falls {1 / P['f_example']:.0f}".replace("5", "five") + "-fold"
    out["mult_06"] = f"{1 / P['p_success_example']:.2f}×"
    out["mult_04"] = f"{1 / P['p_success'][0]:.1f}×"
    c = P["c_attempt_example"]
    lo, hi = c / P["p_success"][0], c / P["p_success"][1]
    out["per_success"] = f"= ${lo:.3f} per clearance token"
    out["per_success_07"] = f"≈ ${hi:.3f}"
    out["delta_pct"] = f"≈ {round((lo - round(hi, 3)) / lo * 100)}%"
    ls = P["vlm_step_latency"]
    out["latency"] = f"{ls[0] * P['n_actions'][0]}–{ls[1] * P['n_actions'][1]} seconds per attempt"
    cf = P["captcha_farm"]
    out["captcha"] = f"${cf[0] / 1000:.4f}–${cf[1] / 1000:.3f} each"
    mon_lo, mon_hi, mac_mon, t1 = tier1_table()
    out["t1_month"] = f"${mon_lo:.2f}–${mon_hi:.2f} per device-month"
    out["t1_mac"] = f"${mac_mon:.0f} per month"
    pp = P["ppi_price"]
    out["ppi"] = f"${pp[0] / 1000:.3f}–${pp[1] / 1000:.2f} per install"
    ap = P["account_price"]
    out["acct"] = f"${ap[0] / 1000:.2f}–${ap[1] / 1000:.2f} per account"
    out["hybrid_table"] = hybrid_table()
    out["tier1_table"] = t1

    for k, v in out.items():
        print(f"[{k}]\n{v}\n" if "\n" in v else f"{k:15s} {v}")

    paper = (ROOT / "paper.md").read_text()
    sec5 = paper[paper.index("## 5. "):paper.index("## 6. ")]
    missing = [k for k, v in out.items() if v not in sec5]
    assert not missing, f"paper.md §5 out of sync with script for: {missing}"
    print("self-check OK: every number above appears verbatim in paper.md §5")


if __name__ == "__main__":
    main()
