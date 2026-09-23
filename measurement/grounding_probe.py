"""Grounding probe: can each Melious VLM find the real "Continue" button from a screenshot alone?

Screenshots /flow/1..5 of the local testbed (Playwright, 1280x800), asks each model for click
coordinates, scores a hit if the point lies inside the real button's bounding box.
  python grounding_probe.py [--trials 5] [--models a,b]   -> results/grounding_probe.json
Needs the testbed running and MELIOUS_API_KEY.
"""
import argparse, json, os, statistics, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "attackers"))
from common import BASE  # local-only guard
from c_vlm import MeliousAdapter, parse_action

MODELS = ["glm-5.3-flash", "kimi-k2.7-code", "gemma-4-26b-a4b", "qwen3.8-27b"]
PROMPT = ('This is a {w}x{h} pixel browser screenshot. Where would you click to press the "Continue" button? '
          'Reply with exactly one JSON object and nothing else: {{"action":"click","x":<int>,"y":<int>}}')


def pages():
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 800})
        for n in range(1, 6):
            pg.goto(f"{BASE}/flow/{n}?run=grounding-probe")
            bb = pg.locator("#real-continue").bounding_box()
            out.append({"page": f"/flow/{n}", "png": pg.screenshot(), "box": bb})
        b.close()
    return out


def hit(xy, bb):
    return bb["x"] <= xy[0] <= bb["x"] + bb["width"] and bb["y"] <= xy[1] <= bb["y"] + bb["height"]


def probe(model, shots, trials):
    ad, rows = MeliousAdapter(model), []
    for s in shots:
        for t in range(trials):
            try:
                text, i, o, dt = ad.ask(s["png"], PROMPT.format(w=1280, h=800))
                a = parse_action(text)
                xy = a[0]["coordinate"] if a and a[0].get("coordinate") else None
                rows.append({"page": s["page"], "trial": t, "xy": xy, "hit": bool(xy and hit(xy, s["box"])),
                             "hit_norm1000": bool(xy and hit([xy[0] * 1.28, xy[1] * 0.8], s["box"])),
                             "latency_s": round(dt, 3), "input_tokens": i, "output_tokens": o,
                             "reply": None if xy else text[:120]})
            except Exception as e:
                rows.append({"page": s["page"], "trial": t, "hit": False, "error": repr(e)[:200]})
    ok = [r for r in rows if "latency_s" in r]
    return {"model": model, "n": len(rows), "hits": sum(r["hit"] for r in rows),
            "hit_rate": sum(r["hit"] for r in rows) / len(rows),
            "hit_rate_norm1000": sum(r.get("hit_norm1000", False) for r in rows) / len(rows),
            "latency_s_median": statistics.median(r["latency_s"] for r in ok) if ok else None,
            "input_tokens_mean": statistics.mean(r["input_tokens"] for r in ok) if ok else None,
            "output_tokens_mean": statistics.mean(r["output_tokens"] for r in ok) if ok else None,
            "errors": len(rows) - len(ok), "trials": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=5)
    ap.add_argument("--models", default=",".join(MODELS))
    a = ap.parse_args()
    assert hit([100, 210], {"x": 40, "y": 200, "width": 160, "height": 40}) and not hit([10, 210], {"x": 40, "y": 200, "width": 160, "height": 40})
    shots = pages()
    with ThreadPoolExecutor(4) as ex:  # one thread per model; trials within a model are sequential
        res = list(ex.map(lambda m: probe(m, shots, a.trials), a.models.split(",")))
    out = {"date": time.strftime("%Y-%m-%d"), "provider": "melious.ai", "viewport": [1280, 800],
           "pages": [{"page": s["page"], "box": s["box"]} for s in shots], "results": res}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "grounding_probe.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), indent=1)
    for r in sorted(res, key=lambda r: (-r["hit_rate"], r["latency_s_median"] or 1e9)):
        print(f"{r['model']:<18} hit {r['hits']}/{r['n']} (norm1000 {r['hit_rate_norm1000']:.2f})  p50 {r['latency_s_median']}s  "
              f"tok in/out {r['input_tokens_mean']}/{r['output_tokens_mean']}  err {r['errors']}")


if __name__ == "__main__":
    main()
