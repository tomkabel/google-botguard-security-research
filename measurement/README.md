# Measurement harness (REVISION_PLAN Phase 4)

A harness for the paper's planned §5.6 "Measured costs". It is built and smoke-tested. **No
measurement data has been collected yet.** Nothing in this directory may be cited as a result
until the runs described below have actually been done.

## Ethics scope (binding)

- **Self-hosted only.** The testbed binds to `127.0.0.1`. `attackers/common.py` refuses any
  `TESTBED_URL` that is not local. No agent is ever pointed at a third-party or production site,
  and never at a Google/Botguard production endpoint.
- **Vendor test keys only.**
  - Cloudflare Turnstile: the documented test keys (site key `1x…AA` always passes, `2x…AB`
    always fails; the matching secrets are `1x…AA` / `2x…AA`). Source:
    developers.cloudflare.com/turnstile/troubleshooting/testing/, checked 2026-09-23.
  - reCAPTCHA: Google documents test keys **for v2 only** (developers.google.com/recaptcha/docs/faq).
    **No v3 test key exists.** So `/recaptcha` uses the v2 test key. `/recaptcha3` stays disabled
    unless you register your own v3 key restricted to `localhost` and set
    `RECAPTCHA_V3_SITEKEY` / `RECAPTCHA_V3_SECRET`. Before doing that, check the reCAPTCHA terms
    for automated-traffic testing. Test keys give fixed outcomes, so they measure the *harness and
    the flow*, not vendor detection. Any real vendor-score claim needs a self-registered
    localhost key and a ToS check, recorded here.
  - The vendor widget JS is loaded from the vendor CDN, as the test-key docs intend. The server
    calls `siteverify` only when started with `--verify`, and then only with test secrets.
- **LLM APIs.** Config (c)/(d) calls a model provider's API with screenshots of the local testbed.
  That is ordinary API use. No key is committed; the model id comes from `ANTHROPIC_MODEL`.
- **Human pilot.** None has been run. Any human-baseline pilot needs an IRB/ethics determination
  (approval or a documented exemption) *before* recruiting. Until then, use published human timings
  (e.g. Searles et al.) and label them as such.
- Release: the harness plus raw `logs/*.jsonl` go out as an artifact. The logs contain no personal
  data because the form answers are fixed dummies.

## Layout

| Path | What |
|---|---|
| `testbed/server.py` | stdlib HTTP server: 5-step form (`/flow/1..5`), Turnstile pass/fail (`/turnstile?mode=`), reCAPTCHA v2 test (`/recaptcha`), optional v3 (`/recaptcha3`). Logs load/click/honeypot/step/verify events to `logs/server.jsonl`. |
| `attackers/a_playwright.py` | (a) Playwright/CDP. `--select dom` = DOM-grounded element-reference click. `--select role` = accessibility-tree selection. |
| `attackers/b_osinput.py` | (b) xdotool keyboard input on stock Chromium with a fresh profile. No CDP, no webdriver flag. |
| `attackers/c_vlm.py` | (c) VLM computer-use agent: an `Adapter` interface plus `AnthropicAdapter` (Claude computer use), executed via xdotool with screenshot-only grounding. |
| `attackers/d_hybrid.py` | (d) scripted (b) for known pages; the VLM is called only for unrecognised pages (e.g. a CAPTCHA). |
| `analyze.py` | Aggregates the logs into per-config metrics. `--selfcheck` runs asserts on a synthetic fixture. |

**Cognitive honeypot.** Implemented as §3.4 (L3) specifies. The decoy "Continue" button has a
non-zero bounding rect (160×40), `opacity:0.01`, and sits inside a full-viewport overlay with
`pointer-events:none`. It carries `aria-hidden="true"` and `tabindex=-1`. It sits exactly over the
real button, so a coordinate click reaches the real one. Its handler fires only when something
selects it by element reference (JS/CDP `el.click()`).

## Requirements

Status on the dev box (2026-09-23): `playwright` (Python) and its Chromium are installed.
`xdotool`, `chromium` and ImageMagick `import` are installed, on an X11 session. `anthropic` SDK 0.100 is installed.
**`pyautogui` is not installed** and is not needed because (b)–(d) use xdotool.

- (a): `pip install playwright && playwright install chromium`
- (b)–(d): X11 session, `xdotool`, a Chrome/Chromium binary (`CHROME=google-chrome` to override)
- (c)–(d): ImageMagick `import`, `pip install anthropic`, `ANTHROPIC_MODEL`, and credentials
  (`ANTHROPIC_API_KEY` or an `ant auth login` profile).
  - `CU_TOOL=toolset` (default) uses `computer_toolset_20260801`, which is required on `claude-opus-5-5`.
  - `CU_TOOL=legacy` uses `computer_20251124` with beta `computer-use-2025-11-24`.
- Plan item 2(c) asks for ≥2 VLMs including one open model. Add a second `Adapter` (e.g. a locally
  served open VLM) with the same `step()` / `results()` contract. **Not implemented yet.**

## How to run

```sh
cd measurement
python3 analyze.py --selfcheck                  # expect: selfcheck ok
python3 testbed/server.py [--verify] &          # http://127.0.0.1:8799
cd attackers
python3 a_playwright.py --runs 30 --select dom
python3 a_playwright.py --runs 30 --select role
python3 b_osinput.py   --runs 30                # takes over the X display
ANTHROPIC_MODEL=<id> python3 c_vlm.py --runs 10
ANTHROPIC_MODEL=<id> python3 d_hybrid.py --runs 10 --start '/turnstile?mode=pass'
cd .. && python3 analyze.py [--json]
```

Prices for `$ / success` come from `../analysis/params.json`:
`{"prices_usd_per_mtok": {"<model id>": {"input": x, "output": y}}}`. Put the verified,
dated list prices there. No prices are hard-coded, and an unpriced model shows `-`.

## Outputs

`logs/runs-<config>.jsonl` holds one line per run: run_id, model, start/end, per-action durations,
tokens, and error. `logs/server.jsonl` holds the server events. `analyze.py` prints one row per config:

`config  n  pass  honeypot  vendor  run_med_s  act_p50  act_p90  $/success`

- **pass**: the server saw `flow_done` for that run. This is authoritative over the attacker's own flag.
- **honeypot**: the share of runs with ≥1 decoy activation.
- **vendor**: the share of verified tokens that passed. `-` without `--verify`.
- **act_p50 / act_p90**: the per-action latency distribution in seconds, excluding browser launch.
- **$/success**: total LLM spend across all runs divided by the number of successes, so failed runs count.

## Smoke test done at build time (not data)

- `analyze.py --selfcheck` passed.
- Local server plus config (a), 5 runs each. `--select dom` passed 5/5 with honeypot 5/5.
  `--select role` passed 5/5 with honeypot 0/5.
- A Playwright coordinate click on the real button went through the overlay to step 2 with
  0 honeypot events.
- `getBoundingClientRect()` of the decoy is 160×40. `get_by_role("button", name="Continue")`
  found 1 element (the decoy is hidden from the a11y tree).
- These runs only confirm the wiring. The logs were deleted.
- (b), (c) and (d) were compile/import-checked only; they were not executed. (b) takes over the
  display, and (c)/(d) need an API key and incur spend.

## What goes into paper §5.6

1. A table per config (a-dom, a-role, b, c per model, d): pass rate, honeypot trigger rate,
   median/p90 run time, per-action latency p50/p90, tokens and $ per success. Give n and dates.
2. Compare per-action latency against published human timings for a comparable flow. Do not
   compare against single-CAPTCHA solve times (see §3.4 L4).
3. The honeypot result, stated with its scope. It fires on DOM-reference selection (a-dom) and
   is by construction invisible to a11y-tree (a-role), keyboard (b) and screenshot-only (c)
   agents. Report negative results as such.
4. The hybrid (d) versus pure-VLM (c) cost ratio. This addresses the S&P confound: how much of
   the cost is the VLM itself and how much is OS-level input.
5. Limitations:
   - Test keys give fixed vendor outcomes.
   - There is no v3 test key.
   - Only one VLM is wired so far.
   - There is no human pilot without IRB.
