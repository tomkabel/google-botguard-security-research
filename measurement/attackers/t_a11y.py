"""Config (t): text-only LLM agent on the accessibility tree (Experiment B baseline, no vision).

Each step sends the page's Playwright ARIA snapshot as TEXT (no image), the generic goal and the agent's own action
history to the model and gets ONE JSON action back that names an element by role and accessible name. Playwright
executes it (get_by_role). This is honestly a CDP agent: navigator.webdriver is set and its clicks are CDP mouse
events, so every CDP signal of Table 5.4 applies. It exists only to ask whether language reasoning over the
accessibility tree already generalises to unseen variants without vision.
Env: VLM_PROVIDER=melious (required), MELIOUS_MODEL, MELIOUS_API_KEY; FLOW_PREFIX, RUN_LOG_DIR as in common.py.
Usage: RUN_LOG_DIR=../logs/xsite FLOW_PREFIX=/v/3 VLM_PROVIDER=melious MELIOUS_MODEL=glm-5.3-flash python t_a11y.py --runs 6
"""
import argparse, json, os, re
from playwright.sync_api import sync_playwright
from common import BASE, FLOW, Run
from c_vlm import GENERIC_GOAL, MeliousAdapter

PROMPT = ("You control a web browser. The current page's accessibility tree (Playwright ARIA snapshot) is:\n{tree}\n\n"
          "Task: {goal}\nActions already taken (oldest first): {hist}\n"
          "Reply with exactly ONE JSON object and nothing else, one of:\n"
          '{{"action":"fill","role":"textbox","name":"<accessible name>","text":"<str>"}}  '
          '{{"action":"select","role":"combobox","name":"<accessible name>","option":"<option text>"}}  '
          '{{"action":"check","role":"checkbox","name":"<accessible name>"}}  '
          '{{"action":"click","role":"<role>","name":"<accessible name>"}}  {{"action":"done"}}\n'
          "role and name must match an element in the tree exactly.")
KINDS = {"fill": "text", "select": "option", "check": None, "click": None}


def parse(text):
    """Model reply -> action dict ({} = done, None = unparseable)."""
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    for m in re.finditer(r"\{[^{}]*\}", text):
        try:
            a = json.loads(m.group(0))
        except ValueError:
            continue
        kind = str(a.get("action", "")).lower()
        if kind == "done":
            return {}
        if kind in KINDS and isinstance(a.get("role"), str) and isinstance(a.get("name"), str) \
                and (KINDS[kind] is None or isinstance(a.get(KINDS[kind]), str)):
            return dict(a, action=kind)
    return None


def execute(page, a):
    loc = page.get_by_role(a["role"], name=a["name"], exact=True).first
    if a["action"] == "fill":
        loc.fill(a["text"])
    elif a["action"] == "select":
        loc.select_option(label=a["option"])
    elif a["action"] == "check":
        loc.check()
    else:
        loc.click()
        page.wait_for_load_state()


def one_run(browser, max_steps):
    llm = MeliousAdapter()
    run = Run("t-a11y", model=llm.model)
    run.r["llm_calls"] = llm.calls  # same list object: survives exceptions
    page = browser.new_page()
    page.set_default_timeout(5000)
    hist = []
    try:
        page.goto(f"{BASE}{FLOW}/1?run={run.id}")
        run.act("goto")
        for _ in range(max_steps):
            tree = page.locator("body").aria_snapshot()
            text, i, o, _ = llm.ask(None, PROMPT.format(tree=tree, goal=GENERIC_GOAL, hist=json.dumps(hist[-12:]) or "none"))
            run.tokens(i, o)
            run.act("llm")
            a = parse(text)
            if a == {}:
                break
            if a is None:
                hist.append({"invalid_reply": text[:80]})
                continue
            try:
                execute(page, a)
                hist.append(a)
            except Exception as e:  # element not found etc.: the model sees the failure next step
                hist.append(dict(a, error=type(e).__name__))
            run.act(a["action"])
        run.r["success"] = page.locator("#done").count() > 0  # hint only; analyze.py uses server flow_done
    except Exception as e:
        run.r["error"] = repr(e)
    finally:
        page.close()
    return run.save()


def main():
    assert os.environ.get("VLM_PROVIDER") == "melious", "t_a11y uses the Melious API only"
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--max-steps", type=int, default=30)
    a = ap.parse_args()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for _ in range(a.runs):
            r = one_run(b, a.max_steps)
            print(r["run_id"], "success" if r["success"] else f"fail {r['error']}", r["input_tokens"], r["output_tokens"])
        b.close()


def selfcheck():
    assert parse('```json\n{"action":"fill","role":"textbox","name":"City","text":"Tartu"}\n```')["text"] == "Tartu"
    assert parse('<think>{"action":"done"}</think>{"action":"CLICK","role":"button","name":"Weiter"}')["action"] == "click"
    assert parse('{"action":"done"}') == {} and parse('{"action":"fill","role":"textbox","name":"x"}') is None
    print("selfcheck ok")


if __name__ == "__main__":
    import sys
    if "--selfcheck" in sys.argv:
        raise SystemExit(selfcheck())
    main()
