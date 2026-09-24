"""Experiment B, script repair: a-dom with its selectors adapted by hand to each variant (repair-effort proxy).

SCRIPTS[k] is the full a-dom script for variant k (0 = base form, identical to a_playwright.py --select dom): one
button selector plus one (step, Playwright op, selector, value) line per field. Repair effort = lines changed
against SCRIPTS[0] (difflib opcodes; a replaced block counts max(old, new) lines). This counts edits, not minutes.
Field ids for v3/v9 were read off the variant pages (they are stable across loads on this testbed; a site that
re-randomises ids per load would need label-based selectors, same line count). The click logic is unchanged from
a-dom (last match by element reference, retry on #real-continue), so the honeypot still fires.
Usage: RUN_LOG_DIR=../logs/repair FLOW_PREFIX=/v/3 python a_dom_adapted.py --runs 1
"""
import argparse, difflib
from playwright.sync_api import sync_playwright
from common import BASE, FLOW, PREFIX, Run

C, W, ARROW = "button:has-text('Continue')", "button:has-text('Weiter')", "button:has-text('→')"
N, E, CITY, Z, Y = "Test User", "test@example.invalid", "Tartu", "50090", "YES"
BASE_SCRIPT = [("button", C), (1, "fill", "#f1", N), (2, "fill", "#f2", E), (3, "fill", "#f3", CITY),
               (4, "fill", "#f4", Z), (5, "fill", "#f5", Y)]
SCRIPTS = {
    0: BASE_SCRIPT,
    1: BASE_SCRIPT,  # reworded labels: ids unchanged
    2: [("button", W)] + BASE_SCRIPT[1:],
    3: [("button", C), (1, "fill", "#x0cb1df4025", N), (2, "fill", "#xd49a0f798a", E), (3, "fill", "#x6194026154", CITY),
        (4, "fill", "#xb945c0c99c", Z), (5, "fill", "#xb1ed9f74f2", Y)],
    4: BASE_SCRIPT,  # optional field first, main field keeps #f<n>
    5: [("button", C), (1, "fill", "#f1", "User"), (1, "fill", "#f1first", "Test"), (2, "fill", "#f2", E),
        (2, "fill", "#f2email2", E), (3, "fill", "#f3", CITY), (4, "fill", "#f4", Z), (5, "fill", "#f5", Y)],
    6: [("button", ARROW)] + BASE_SCRIPT[1:],
    7: BASE_SCRIPT[:3] + [(3, "select_option", "#f3", CITY)] + BASE_SCRIPT[4:],
    8: BASE_SCRIPT[:5] + [(5, "check", "#f5", None)],
    9: [("button", W), (1, "fill", "#xc3f377034b", N), (2, "fill", "#xac6f1e99ad", E),
        (3, "select_option", "#xc181eff080", CITY), (4, "fill", "#x8289c44c77", Z), (5, "check", "#x4fff54ee24", None)],
}


def lines_changed(k):
    ops = difflib.SequenceMatcher(None, SCRIPTS[0], SCRIPTS[k], autojunk=False).get_opcodes()
    return sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in ops if tag != "equal")


def one_run(browser, k):
    script = SCRIPTS[k]
    button = script[0][1]
    run = Run("a-dom-adapted")
    run.r["lines_changed"] = lines_changed(k)
    page = browser.new_page()
    try:
        page.goto(f"{BASE}{FLOW}/1?run={run.id}")
        run.act("goto")
        for i in range(1, 6):
            for _, op, sel, val in (l for l in script[1:] if l[0] == i):
                getattr(page, op)(sel, *([val] if val else []))
                run.act(op)
            page.locator(button).last.evaluate("el => el.click()")  # as a-dom: last match, by element reference
            run.act("click")
            page.wait_for_load_state()
            if page.url.split("?")[0].endswith(f"/flow/{i}"):  # decoy click does not navigate
                with page.expect_navigation():
                    page.locator("#real-continue").evaluate("el => el.click()")
                run.act("click-retry")
        page.wait_for_selector("#done", timeout=5000)
        run.r["success"] = True
    except Exception as e:
        run.r["error"] = repr(e)
    finally:
        page.close()
    return run.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1)
    a = ap.parse_args()
    k = int(PREFIX.split("/")[2]) if PREFIX else 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for _ in range(a.runs):
            r = one_run(b, k)
            print(r["run_id"], f"v{k}", r["lines_changed"], "success" if r["success"] else f"fail {r['error']}")
        b.close()


if __name__ == "__main__":
    import sys
    if "--selfcheck" in sys.argv:
        assert [lines_changed(k) for k in range(10)] == [0, 0, 1, 5, 0, 3, 1, 1, 1, 6], [lines_changed(k) for k in range(10)]
        raise SystemExit(print("selfcheck ok"))
    main()
