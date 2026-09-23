"""Config (a): Playwright/CDP automation of the 5-step flow.

--select dom   : DOM-grounded selection — first element whose text is "Continue", clicked by
                 element reference (el.click() via CDP Runtime). Models a DOM-candidate agent.
--select role  : accessibility-tree selection (get_by_role), which skips the aria-hidden decoy.
Usage: python a_playwright.py [--runs N] [--select dom|role] [--headed]
"""
import argparse
from playwright.sync_api import sync_playwright
from common import BASE, FLOW_ANSWERS, Run


def one_run(browser, select):
    run = Run(f"a-{select}")
    page = browser.new_page()
    try:
        page.goto(f"{BASE}/flow/1?run={run.id}")
        run.act("goto")
        for i, ans in enumerate(FLOW_ANSWERS, 1):
            page.fill(f"#f{i}", ans)
            run.act("fill")
            if select == "dom":
                # first DOM match in document order is the real button; the decoy is later in the DOM,
                # so pick the *last* match to model an agent ranking by visual prominence / z-index.
                page.locator("button:has-text('Continue')").last.evaluate("el => el.click()")
            else:
                page.get_by_role("button", name="Continue").click()
            run.act("click")
            page.wait_for_load_state()
            if page.url.split("?")[0].endswith(f"/flow/{i}"):  # decoy click does not navigate
                with page.expect_navigation():
                    page.locator("#real-continue").evaluate("el => el.click()")
                run.act("click-retry")
        page.wait_for_selector("#done", timeout=5000)
        run.r["success"] = True
    except Exception as e:  # recorded, not hidden
        run.r["error"] = repr(e)
    finally:
        page.close()
    return run.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--select", choices=["dom", "role"], default="dom")
    ap.add_argument("--headed", action="store_true")
    a = ap.parse_args()
    with sync_playwright() as p:
        b = p.chromium.launch(headless=not a.headed)
        for _ in range(a.runs):
            r = one_run(b, a.select)
            print(r["run_id"], "success" if r["success"] else f"fail {r['error']}")
        b.close()


if __name__ == "__main__":
    main()
