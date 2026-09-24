# Measurement harness (REVISION_PLAN Phase 4)

The harness behind paper §5.7 "Measured Costs on a Self-Hosted Testbed" (Tables 5.4, 5.5). Raw logs are
in `logs/`, generated tables in `results/summary.md`, and the grounding probe in `results/grounding_probe.json`.

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
| `testbed/server.py` | stdlib HTTP server: 5-step form (`/flow/1..5`), Turnstile pass/fail (`/turnstile?mode=`), reCAPTCHA v2 test (`/recaptcha`), optional v3 (`/recaptcha3`). Logs load/click/honeypot/step/verify events to `logs/server.jsonl`. Experiment B variants at `/v/1..9/flow/1..5`; pointer kinematics via `POST /kin` to `logs/kinematics.jsonl`. |
| `attackers/a_playwright.py` | (a) Playwright/CDP. `--select dom` = DOM-grounded element-reference click. `--select role` = accessibility-tree selection. |
| `attackers/b_osinput.py` | (b) xdotool keyboard input on stock Chromium with a fresh profile. No CDP, no webdriver flag. |
| `attackers/c_vlm.py` | (c) VLM computer-use agent: an `Adapter` interface plus `AnthropicAdapter` (Claude computer use), executed via xdotool with screenshot-only grounding. |
| `attackers/d_hybrid.py` | (d) scripted (b) for known pages; the VLM is called only for unrecognised pages (e.g. a CAPTCHA). |
| `attackers/e_smooth.py` | Experiment A: mouse-driven xdotool on the base form. `--path teleport` = `b-mouse` (pointer jumps to each target). `--path minjerk` = `e-smooth` (minimum-jerk path, lateral bow, Gaussian jitter, Fitts'-law duration, pre-click dwell). |
| `attackers/t_a11y.py` | Experiment B baseline (t): text-only LLM on the Playwright ARIA snapshot (no image); one JSON action naming an element by role and name, executed with Playwright `get_by_role`. A CDP agent (webdriver set). |
| `attackers/a_dom_adapted.py` | Experiment B script repair: a-dom with its selector table adapted by hand per variant; `lines_changed(k)` diffs against the base script. |
| `kinematics.py` | Experiment A detectors: segmentation, mouse-dynamics features, Balabit loader, threshold rule, min-jerk bot generator, numpy logistic regression. |
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
- `MeliousAdapter` (`VLM_PROVIDER=melious`, `MELIOUS_MODEL=<id>`, `MELIOUS_API_KEY`) covers any vision model on
  the Melious OpenAI-compatible API.

## How to run

```sh
cd measurement
python3 analyze.py --selfcheck                  # expect: selfcheck ok
python3 testbed/server.py [--verify] &          # http://127.0.0.1:8799
cd attackers
python3 a_playwright.py --runs 30 --select dom
python3 a_playwright.py --runs 30 --select role
Xvfb :99 -screen 0 1280x800x24 -nolisten tcp &  # (b)-(d) refuse the live display
export DISPLAY=:99
python3 b_osinput.py   --runs 10
VLM_PROVIDER=melious MELIOUS_MODEL=<id> python3 c_vlm.py --runs 10
VLM_PROVIDER=melious MELIOUS_MODEL=<id> python3 d_hybrid.py --runs 10 --start '/turnstile?mode=pass'
cd .. && python3 grounding_probe.py --trials 5  # optional: pick models
python3 analyze.py [--json | --summary | --check-paper]
```

Prices for cost per success come from `../analysis/params.json`:
`"prices_usd_per_mtok"` / `"prices_eur_per_mtok"`, each `{"value": {"<model id>": {"input": x, "output": y}}}`. Put the verified,
dated list prices there. No prices are hard-coded, and an unpriced model shows `-`.

## Outputs

`logs/runs-<config>.jsonl` holds one line per run: run_id, model, start/end, per-action durations,
tokens, and error. `logs/server.jsonl` holds the server events. `analyze.py` prints one row per config:

`config  n  pass  honeypot  vendor  run_med_s  act_p50  act_p90  cost/succ`

- **pass**: the server saw `flow_done` for that run. This is authoritative over the attacker's own flag.
- **honeypot**: the share of runs with ≥1 decoy activation.
- **vendor**: the share of verified tokens that passed. `-` without `--verify`.
- **act_p50 / act_p90**: the per-action latency distribution in seconds, excluding browser launch.
- **cost/succ**: total LLM spend across all runs divided by the number of successes, so failed runs count.

## Results (23 September 2026, paper §5.7)

- 70 runs: a-dom, a-role, b-xdotool 10 each; c-vlm and d-hybrid 10 each for glm-5.3-flash and qwen3.8-27b.
  (b)–(d) ran on Xvfb displays at 1280×800. Total LLM spend €0.28. Gemma runs were dropped (not used).
- `analyze.py --summary` writes `results/summary.md` / `summary.json`; `--check-paper` (run by `make numbers`)
  asserts that every table row appears verbatim in `paper.md`.
- Pass = server-side `flow_done`. For d-hybrid the attacker's own flag means "scripted control resumed after
  the VLM step" and is reported separately (glm 9/10, qwen 0/10).
- Limitations: test keys give fixed vendor outcomes (no v3 test key exists); no human baseline without IRB;
  xdotool moves the pointer in straight jumps (no kinematics); one provider, one day, list prices in EUR.

## Experiments A and B (24 September 2026)

Both keep the base tables untouched. Experiment runs go to `logs/xsite/` and `logs/kin/` (`RUN_LOG_DIR`), which
`analyze.py` does not glob for Tables 5.4/5.5. `analyze.py --summary` appends both experiments to
`results/summary.md` and adds `experiment_a_kinematics` / `experiment_b_xsite` to `summary.json`.
The new table rows start with `| base`, `| v<k>`, `| All`, `| Balabit`, `| Synthetic`, `| (a)`–`| (e)`, so
`--check-paper` (which matches `| a-`, `| b-`, `| c-vlm`, `| d-hybrid`) is unaffected.

### How to run

```sh
cd measurement
git clone https://github.com/balabit/Mouse-Dynamics-Challenge data/Mouse-Dynamics-Challenge  # gitignored
python3 testbed/server.py &
Xvfb :99 -screen 0 1280x800x24 -nolisten tcp & export DISPLAY=:99
cd attackers
# A: pointer kinematics are logged by every testbed page to logs/kinematics.jsonl (POST /kin)
RUN_LOG_DIR=../logs/kin python3 e_smooth.py --path teleport --runs 10
RUN_LOG_DIR=../logs/kin python3 e_smooth.py --path minjerk  --runs 10
# B: the unmodified agents on the base form (control) and variants /v/1..9; FLOW_PREFIX sets the start URL
export RUN_LOG_DIR=../logs/xsite
for v in "" /v/1 /v/2 /v/3 /v/4 /v/5 /v/6 /v/7 /v/8 /v/9; do   # --runs 2 in round 1, +4 in round 2 (N = 6)
  FLOW_PREFIX=$v python3 a_playwright.py --runs 6 --select dom
  FLOW_PREFIX=$v python3 a_playwright.py --runs 6 --select role
  FLOW_PREFIX=$v python3 b_osinput.py --runs 6
  FLOW_PREFIX=$v VLM_PROVIDER=melious MELIOUS_MODEL=glm-5.3-flash VLM_GOAL=generic python3 c_vlm.py --runs 6
  FLOW_PREFIX=$v VLM_PROVIDER=melious MELIOUS_MODEL=glm-5.3-flash python3 t_a11y.py --runs 6   # headless, no Xvfb
done
# script repair: adapted a-dom, once per variant, to its own log dir
for k in 1 2 3 4 5 6 7 8 9; do RUN_LOG_DIR=../logs/repair FLOW_PREFIX=/v/$k python3 a_dom_adapted.py --runs 1; done
cd .. && python3 analyze.py --summary   # trains both detectors on Balabit (~90 s), scores the kinematics log
```

### Experiment A: kinematic detector (Type III / L1b)

- **Recording.** Every testbed page buffers `mousemove`, `mousedown`, `click` and `keydown` as
  `[type, performance.now() ms, clientX, clientY]` (key identity is not recorded). It flushes them with
  `sendBeacon('/kin')` on submit, on pagehide and every 1,500 events. The existing `/event` telemetry is unchanged.
- **Human reference.** Balabit Mouse Dynamics Challenge training sessions (10 users): Á. Fülöp, L. Kovács,
  T. Kurics, E. Windhager-Pokol (2016), *Balabit Mouse Dynamics Challenge data set*,
  https://github.com/balabit/Mouse-Dynamics-Challenge. No licence file; its README invites research use. Not
  committed (`measurement/data/` is gitignored).
- **Segmentation.** A movement is the continuous burst of moves before a left press. A gap over 1 s between
  moves starts a new burst; a release, drag or other button resets it. Human movements must travel ≥20 px.
  Agent movements are all scored, including single-event jumps.
- **Resampling.** Balabit has client timestamps at about 60 Hz from a remote-desktop session. Browser events arrive at
  the X input rate. Both are linearly interpolated onto one 50 Hz grid before any feature is computed, so
  "samples" measures duration on a common clock. Pixels are not rescaled; screen sizes differ.
- **Features.** Samples, duration, straightness (displacement / path length), velocity mean/std, acceleration
  std, mean absolute jerk, curvature (turning angle per px) and pause before the press.
- **Classifier.** scikit-learn is not installed, so a transparent rule is used: *bot iff samples < N or
  straightness > S*, grid-searched on 6 training users. Bot class = synthetic movements between the same
  human endpoints: half teleports, half constant-velocity straight lines at 60 Hz. The fit gives N = 1
  (inactive) and S = 0.9925. **Held-out accuracy is 93.2%** on 4 unseen users (n = 38,272), with humans
  flagged at 9.0% and synthetic bots at 95.4%.

| Movement source | Movements | Flagged as bot | Median samples (50 Hz) | Median straightness |
|---|---|---|---|---|
| Balabit human, held-out users | 19,136 | 9% | 61 | 0.827 |
| (a) Playwright CDP click (a-role) | 42 | 100% | 1 | 1.000 |
| (b) scripted xdotool, pointer jumps (10 runs) | 98 | 100% | 1 | 1.000 |
| (c) VLM agent, glm-5.3-flash (20 runs, Exp. B) | 154 | 100% | 1 | 1.000 |
| (c) VLM agent, kimi-k3 (6 runs, Exp. B) | 59 | 100% | 1 | 1.000 |
| (e) smoothed OS input, min-jerk (10 runs) | 100 | 0% | 24 | 0.956 |

The detector separates *how the pointer is driven*, not *who decides where to click*. The VLM executor
jumps the pointer exactly like scripted xdotool, and ~50 lines of textbook motor model (not tuned against this or
any vendor detector) take the flag rate to 0%. Two `b-mouse` movements were lost to a page-load race: the
window title appears before the telemetry script attaches. The (c) movements come from the Experiment B runs.

### Experiment B: cross-site generalisation (what the VLM adds)

Nine unseen variants at `/v/<k>/flow/1..5`, all with the same five answers and the honeypot decoy over the real button:
v1 reworded labels; v2 German labels/title with "Weiter"; v3 randomised ids/names; v4 optional decoy field
placed first; v5 two fields per page (last/first name, email + repeat), reordered; v6 icon button "→" placed
above the field; v7 city dropdown; v8 confirmation checkbox; v9 all of v2–v4 and v6–v8 combined. The server logs
`step_submit {variant, step, ok}` and `flow_done {variant}`. **Pass = flow_done and every step answered
correctly.** On the base-form control the server does not validate answers, so pass = flow_done there.
The agents ran unmodified; only their start URL changed. `c-vlm` got a generic goal (`VLM_GOAL=generic`)
listing the five values and nothing about the page.

| Agent | Base (control) | Variants v1–v9 | Passed variants | VLM calls/run (median range) | Cost per success |
|---|---|---|---|---|---|
| a-dom (DOM selectors) | 2/2 | 4/18 | v1, v4 | – | – |
| a-role (accessibility role) | 2/2 | 4/18 | v1, v4 | – | – |
| b-xdotool (keyboard script) | 2/2 | 6/18 | v1, v3, v6 | – | – |
| c-vlm / glm-5.3-flash | 2/2 | 17/18 | all (v6 1/2) | 11–20 | €0.0028 |
| c-vlm / kimi-k3 (subset, 1 run each) | – | 6/6 | v2, v5–v9 | 13–20 | €0.1348 |

N = 2 runs per (agent, variant), 24 September 2026. The full per-variant grid, including run times, is in `results/summary.md`.
The failed glm run on v6 reached the end page with wrong answers on steps 4–5. a-dom hit the honeypot in 12 runs;
no other agent hit it. Experiment B LLM spend was €0.8603. One further glm run on v9 failed on three HTTP 429 rate-limit
responses before `MeliousAdapter` gained back-off. It is kept in `logs/xsite/excluded-infra.jsonl` (€0.0029) and is
not counted. A one-call kimi-k3 probe cost €0.0061. **Total LLM spend on 24 September: €0.87.**

### Round 2 (24 September 2026): power, text-only baseline, repair effort, learned classifier

Reviewers asked for more than N = 2, for something that separates vision from language reasoning, and for a
kinematic detector stronger than one straightness threshold. Earlier runs are kept; runs were added.

**Experiment B at N = 6.** Four more runs per (agent, variant) for a-dom, a-role, b-xdotool and c-vlm/glm-5.3-flash
(160 runs), plus the new text-only agent (t) at N = 6 on the base form and each variant (60 runs, one of them the
smoke-test run on v9, same code). kimi-k3 is unchanged (1 run on 6 variants). Intervals are Wilson 95% on the pooled
v1–v9 runs (`analyze.wilson`); cost per success = v1–v9 spend / v1–v9 successes.

| Agent | Base form | Variants v1–v9 | 95% CI (Wilson) | Cost per success |
|---|---|---|---|---|
| a-dom | 6/6 | 12/54 | 13%–35% | – |
| a-role | 6/6 | 12/54 | 13%–35% | – |
| b-xdotool | 6/6 | 18/54 | 22%–47% | – |
| c-vlm / glm-5.3-flash | 6/6 | 50/54 | 82%–97% | €0.0029 |
| c-vlm / kimi-k3 | – | 6/6 | 61%–100% | €0.1348 |
| t-a11y / glm-5.3-flash | 6/6 | 54/54 | 93%–100% | €0.0005 |

- The scripted agents stayed deterministic: every cell is 0/6 or 6/6, with the same variants passing as at N = 2.
- glm-5.3-flash failed 4 of 6 runs on v6 (icon button above the field), all by submitting wrong answers; every other
  variant was 6/6. a-dom hit the honeypot in 36 runs, no other agent did.
- **Text-only agent (t).** Each step sends `page.locator("body").aria_snapshot()` as text with the same generic
  goal as c-vlm, to glm-5.3-flash without an image; the model returns one JSON action (`fill`/`select`/`check`/`click`
  with role and accessible name), executed by Playwright. It passed every run (54/54 on variants), with a median of
  11 calls and 6–13 s per run, at about a sixth of the vision agent's cost per success. On these variants,
  language reasoning over the accessibility tree already generalises; vision is not needed. It is a CDP agent
  (`navigator.webdriver` set, CDP click events), so its detection profile is a-role's, not c-vlm's.

**Script repair (a-dom only).** `attackers/a_dom_adapted.py` holds the full a-dom script per variant (button selector
plus one line per field). Lines changed against the base script, and the adapted script run once per variant
(`logs/repair/`, pass judged by the server as above):

| Variant | v1 | v2 | v3 | v4 | v5 | v6 | v7 | v8 | v9 | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Lines changed | 0 | 1 | 5 | 0 | 3 | 1 | 1 | 1 | 6 | 18 |
| Adapted a-dom passes | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 9/9 |

This is a proxy for effort (edits, not minutes). The edits also presuppose that someone inspected each variant's
DOM; no time was measured. v3/v9 ids happen to be stable across loads on this testbed.

**Learned kinematic classifier (Experiment A).** scikit-learn could not be installed (`pip install --user` refused:
externally managed environment, PEP 668), so logistic regression is implemented in numpy (Newton/IRLS, L2 = 1 on
standardised features; `kinematics.fit_logreg`). Features: all nine of `kinematics.FEATURES` (log1p of the
heavy-tailed ones, log(1 − straightness)). Bot class: a minimum-jerk path between each human movement's endpoints,
with a Gaussian lateral bow (σ = 6% of distance), per-sample Gaussian jitter (σ drawn from 0.5–2 px) at 60 Hz, and the
paired human's duration and pre-click pause, so duration and pause carry no signal. Same user split as the rule
(6 training, 4 held-out users). Held-out **ROC AUC 0.9985**; at the threshold giving **90% TPR** on held-out min-jerk
bots, **0.22% of held-out human movements** are flagged (43/19,136). The largest weights are on curvature and mean
jerk, i.e. the classifier mainly detects the i.i.d. jitter.

| Movement source | Movements | Flagged (rule) | Flagged (classifier) |
|---|---|---|---|
| Balabit human, held-out users | 19,136 | 9% | 0% (0.22%) |
| Synthetic straight/teleport, held-out | 19,136 | 95% | 41% |
| Synthetic min-jerk, held-out | 19,136 | 1% | 90% |
| (a) Playwright CDP click (a-role) | 126 | 100% | 19% |
| (b) scripted xdotool, pointer jumps | 98 | 100% | 0% |
| (c) VLM agent, glm-5.3-flash | 455 | 100% | 0% |
| (c) VLM agent, kimi-k3 | 59 | 100% | 0% |
| (e) smoothed OS input, min-jerk | 100 | 0% | 35% |
| (t) text-only LLM, Playwright click | 312 | 100% | 0% |

- The two detectors are complementary: the rule catches pointer jumps, which the classifier never saw in training
  and does not flag; the classifier catches synthetic min-jerk paths, which the rule misses (1%).
- **(e) is from the same generator family** as the classifier's bot class (min-jerk + bow + Gaussian jitter), so it
  is an in-distribution test, not an unseen attacker. Even so only 35% are flagged: e-smooth uses Fitts'-law durations
  (median 0.46 s vs 1.22 s), σ = 1 px jitter and 100 Hz xdotool steps, so parameter changes inside one family already
  move it across the threshold. The (c)/(t) movement counts grew because Experiment B runs were added.

**Spend.** Round 2 LLM spend €0.1356 (c-vlm/glm €0.1041 for 40 runs, t-a11y €0.0316 for 60 runs), from logged token
counts at the `analysis/params.json` list prices. Experiment B spend over both rounds: €0.9960.

### Limitations

- **Round 2.** The text-only result holds for pages whose accessibility tree names every control; a site with
  unlabelled or canvas controls would separate (t) from (c), and our variants do not. Repair effort is lines, not
  time. The classifier's bot class is our own generator and it keys on jitter; a smoother generator (or one fitted to
  human data) would likely evade it, and no human data from the testbed exists to test false positives in the browser.
- **Balabit domain shift.** Remote-desktop capture at about 60 Hz from 10 office users on unknown screens, against
  browser events on a 1280×800 Xvfb. Resampling equalises the clock but not pointer acceleration, screen size or
  task. The bot class is synthetic and trivially straight, so 93.2% is an upper bound for this naive detector. The
  learned detector added in round 2 flags 35% of (e); no human data from the testbed exists to test its false
  positives in the browser (no IRB).
- **Synthetic variants.** Nine variants that we wrote ourselves, with five fields each, on localhost. They probe brittleness
  to presentation changes, not real-site diversity, and the scripted agents fail by construction when their
  selector or title assumption breaks. N = 6 per cell since round 2 (kimi-k3: 1, on 6 variants).
- **Single provider, one day.** Both VLMs came through Melious at EUR list prices; kimi-k3 at €2.80/€14.00 per
  M tokens (melious.ai/hub/models/kimi-k3, accessed 2026-09-24).
