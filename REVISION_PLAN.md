# Revision Plan — SoK: Client-Side Anti-Automation Under VLM-Based Attack

Consolidates every finding from the five mock review boards (IEEE S&P, USENIX Sec '27, ACM CCS '27,
IEEE EuroS&P, PoPETs '27; all **Reject**, 1.5–2/5) and tracks it to a final fix.

Status legend: **DONE** = fixed in the working tree · **VERIFY** = fixed but rests on
unchecked facts · **OPEN** = not yet addressed · **AUTHOR** = needs author input/decision.

Baseline after `c7288da`: ~18.8k words, 109 refs, no figures. Current (2026-09-23, uncommitted):
~20.5k words, 117 refs, 1 figure, `analysis/` + `measurement/` artifacts. Decisions taken:
venue = IEEE S&P 2027 SoK (`docs/venue.md`); L1–L4 = Path B (public-source synthesis, no own RE).

## TODO(author) — everything that needs a human

Collected from `paper.md` and the repo (`grep -rn "TODO(author)"`), plus open AUTHOR items:

1. `paper.md` §5 Table 5.1, proxy row: Bright Data price page [97] unreachable (DNS-blocked);
   re-verify "from $5.88/GB" from another network and archive it. Same in `analysis/params.json`
   (`proxy_commodity`, marked UNVERIFIED) and `docs/fact-check.md`.
2. `paper.md` §5.6 + `analysis/params.json` `tier1_device_price`: cite a dated used-market price
   snapshot for a PAT-capable iPhone ($100–$300 is an assumption).
3. `docs/fact-check.md`: check Azad et al. [51] one-line summary against the DIMVA 2020 abstract.
4. `paper.md` "Use of AI Tools": placeholder text, fill per IEEE S&P 2027 policy.
5. Confirm the original literature-search date ("August 2026", §3.1).
6. Measurement (Phase 4): run the harness (`measurement/README.md`), incl. a second VLM (open
   model) adapter; any human pilot needs an IRB/ethics determination first.
7. Archive/screenshot URLs for the four price pages [94–97] (fact-check "Blocked").
8. Length: cut ~20.5k → ~11–12k words and move to the IEEEtran template (Phase 6).

---

## 0. Critique inventory (what the boards said → where it stands)

| # | Finding (boards raising it) | Status |
|---|---|---|
| F1 | L1–L4 attributed to [24], which never mentions Botguard (all 5) | DONE — Path B evidence table in §3.4 (documented/inferred/hypothesized per layer) |
| F2 | Tier 1 "resilient" is a category error; device farms ignored (all 5) | DONE — reframed + §5.6 device-farm cost per clearance token |
| F3 | Protocol errors: PAT attester/issuer, DBSC owner/export, PST, SDK proxies, iOS consent, unlinkability (all 5) | DONE (DBSC registration-time key capture caveat added, §6.1) |
| F4 | §5 formula & arithmetic errors, unsourced prices (all 5) | DONE (script-generated) — Bright Data price = AUTHOR |
| F5 | Self-contradictions: Axis C, profile aging, "arms race moot" (all 5) | DONE |
| F6 | Leftover revision-response text, phantom cross-refs (all 5) | DONE |
| F7 | Citation misuse ([67],[68],[71],[42],[73–75],[49], secondary 99.8%) (all 5) | DONE (PPI price now matches Caballero et al.) |
| F8 | §3.1 methodology not systematic; corpus = reference list (all 5) | DONE (dated rerun, `docs/corpus.csv`, coded vs background) — OPEN: second screener / κ |
| F9 | Missing related work (≥3 boards) | DONE (§2.5; Searles/Bonneau figures verified) — Azad summary = AUTHOR |
| F10 | PACT built on news/blogs (all 5) | DONE (primary sources) |
| F11 | Anonymity, ethics, Open Science, AI-use disclosure (USENIX, S&P, Euro) | DONE (Open Science lists artifacts) except AI-use = AUTHOR |
| F12 | No measurement at all; VLM vs scripted OS-input confound (all 5; S&P fatal) | DONE (small): §5.7 Tables 5.4/5.5 — 90 runs, configs (a)–(d), three Melious VLMs incl. open-weights Gemma, N=10/cell; confound isolated ((b) vs (c)). Scale-up, real vendor keys, human baseline OPEN |
| F13 | Page limit: likely 15–20+ pages (USENIX, S&P) | **OPEN** — Phase 6 (~20.5k words) |
| F14 | No systematization figure; tables lack per-cell citations; no comparison vs prior surveys (S&P, Euro) | DONE (Fig. cost_shift, per-cell cites, §2.5 table) |
| F15 | Cognitive honeypot untested (S&P, USENIX, CCS) | DONE: a-dom 10/10 hits, a-role 0/10, OS-input 0/70 (§5.7); holds by construction, stated |
| F16 | Privacy not central (PoPETs) — only if targeting PETS | N/A (venue = IEEE S&P) |
| F17 | Hybrid attacker model (S&P) | DONE (Table 5.2 sensitivity) |
| F18 | Repetition / hedging / prose density (all 5) | Partly DONE — OPEN in Phase 6 |
| F19 | Ethics of Botguard RE if L1–L4 came from own analysis (S&P, PETS) | DONE (Path B; Ethics section states no RE) |

---

## Phase 1 — Decisions and verification debt — mostly DONE

Status: 1 DONE (IEEE S&P) · 2 DONE (Path B) · 3 AUTHOR · 4 AUTHOR · 5 DONE (`docs/venue.md`) ·
6 DONE except Bright Data, Azad, archive URLs (AUTHOR; see `docs/fact-check.md`).

1. **AUTHOR: choose the primary venue.** Recommendation: IEEE S&P or EuroS&P SoK track (security
   framing already fits). PoPETs only if you commit to Phase 5b privacy reframing. Record choice here.
2. **AUTHOR: L1–L4 provenance.** State whether it derives from your own Botguard analysis.
   - If yes → Phase 2 path A (disclosed method + ethics). If no → path B (synthesis only).
3. **AUTHOR: fill "Use of AI Tools" placeholder** per chosen venue's policy wording.
4. **AUTHOR: confirm literature-search date** (currently "August 2026", inferred).
5. **Fetch the official 2027 CFP** for the chosen venue; record page limit, anonymity, appendix,
   ethics, AI-use, artifact rules, deadlines in `docs/venue.md`. Replace all "unverified" assumptions.
6. **Close VERIFY items** (subagent, primary sources only):
   - OSWorld arXiv ID; RFC 9421 authors/date; §2.5 one-line summaries of each related paper vs. abstracts.
   - The four API price pages (GPT-5, Gemini 2.5 CU, Claude Sonnet 4.6, Bright Data) — screenshot/archive URL.
   - Protocol claims in §4.3/§4.4 written without web lookup (agent C): PAT rate limits, Android Keystore app binding.
   - Restore local Firecrawl (`asus:3002`) — agents fell back to WebSearch.
   - **Done when:** every factual sentence in §2–§6 maps to a checked source; list kept in `docs/fact-check.md`.

## Phase 2 — Ground the L1–L4 model (F1, F19) — DONE (Path B)

- **Path A (own RE):** add §3.4.1 "Analysis method": Botguard script versions/dates collected, tooling,
  what was observed per layer, what was inferred; ToS/legal basis; disclosure to Google (date);
  release sanitized notes as artifact. Update Ethics section accordingly.
- **Path B (synthesis):** add a per-layer evidence table: layer → public source(s) (Picasso, public
  deobfuscation write-ups, vendor docs) → claim strength (documented / inferred / hypothesized).
  Remove any layer detail that has no public source.
- **Done when:** no L1–L4 sentence lacks either a citation or an explicit "we hypothesize".

## Phase 3 — Strengthen the analytical core (F2, F4, F17) — DONE

Status: 1 DONE (§5.6; device price = AUTHOR) · 2 DONE (Table 5.2) · 3 DONE · 4 DONE (`make numbers`).

1. **Tier 1 device-acquisition cost model** (new §5.x): cost per valid clearance token =
   (device price amortized + farm ops) / (tokens per device per rate-limit window). Parameters from
   public device-farm / phone-farm pricing; sensitivity over rate-limit values. Compare with PPI-malware
   and account-acquisition (PACT) paths.
2. **Hybrid-attacker sensitivity table:** cost/latency per success as f(fraction of steps needing VLM,
   P(success), context length). Show where timing/cost signals stop discriminating.
3. **Tier definitions table:** one table, explicit ordering criterion, each cell cited.
4. **Re-derive every §5 number with a script** (`analysis/cost_model.py`, with assert-based self-check)
   so text and tables are generated from one parameter file. Ships as the Open Science artifact.
- **Done when:** script reproduces every number in §5; Tier 1 has a quantified cost, not an adjective.

## Phase 4 — Minimal ethical measurement (F12, F15) — DONE at small scale (2026-09-23)

Status: 1 DONE (Turnstile + reCAPTCHA v2 test keys; no v3 test key exists) · 2 DONE for (a)–(d); Melious adapter,
3 VLMs (glm-5.3-flash, qwen3.8-27b, open-weights gemma-4-26b-a4b) · 3 DONE: §5.7, `measurement/results/summary.md`,
`make numbers` asserts tables vs logs; vendor score not measured (test keys) · 4 AUTHOR (IRB) · 5 harness released, ToS noted in README ·
6 DONE: §5.7 added; Table 5.1 status column and params.json carry measured values; §3.4 L4, §5.2, §7.1,
abstract, C2, Ethics, Open Science updated. Finding: 5–15 s/step assumption too slow for small VLMs; hybrid hand-back
worked only for glm (9/10), qwen/gemma 0/10.

Scope strictly to **self-hosted / test-sitekey** targets. No production Google/Botguard endpoints.

1. **Testbed:** own pages with reCAPTCHA v3 test key, Cloudflare Turnstile test key, a multi-step form,
   and the redesigned cognitive-honeypot decoy.
2. **Three attacker configs (isolates the VLM contribution, answers S&P's fatal confound):**
   (a) Playwright/CDP automation · (b) scripted OS-level input (xdotool/PyAutoGUI) on stock Chrome ·
   (c) VLM computer-use agent (≥2 models, one open) + OS-level input · (d) hybrid (b)+(c).
3. **Measure:** vendor score/pass rate, per-action latency distribution, LLM tokens & $ per success,
   honeypot trigger rate (DOM-grounded vs screenshot-only agent).
4. **Human baseline:** use published timings (Searles et al.); small human pilot only with IRB/ethics approval.
5. **Ethics/Artifacts:** IRB determination (or exemption note), vendor ToS check for test keys,
   release harness + raw logs.
6. **Integrate:** new §5.6 "Measured costs"; replace illustrative rows in Table 5.1; update §4.1 claims
   on container artifacts/kinematics with what the data shows (including negative results).
- **Done when:** C3 cost claims and the latency/honeypot claims each cite a measured table.
- **If skipped:** retitle claims as hypotheses and move measurement to §7.1 as an explicit open problem;
  expect reviewers to still call it a position paper.

## Phase 5 — Systematization quality (F8, F14, F16) — DONE except second screener

Status: 1 DONE (single screener; κ OPEN) · 2 DONE · 3 DONE · 4 DONE · 5b N/A.

1. **§3.1 real protocol:** rerun the dated query; keep a screening log (`docs/corpus.csv`: id, source,
   stage, include/exclude reason, coded dimensions). Separate coded corpus from background refs in text.
   Ideally a second screener on a 20% sample with Cohen's κ.
2. **Per-cell citations** in the mechanism matrix and tier table.
3. **Comparison table vs prior surveys/SoKs** (the SoKs/surveys cited in the paper, Searles '23, Bonneau '12): coverage, threat model,
   evaluation, claims challenged.
4. **One systematization figure:** defense type × attacker class → where cost moves (replaces repeated
   caveat text and at least one table).
5b. **(PoPETs only)** make privacy the research question: linkability/metadata exposure per mechanism,
   attester/issuer knowledge table, fingerprinting data collected per type; retitle §7.4 accordingly.

## Phase 6 — Length, prose, format (F13, F18) — OPEN

1. Target ≈11–12k words body for a 13-page two-column limit (current ≈18.8k → cut ~35%).
   Cuts: repeated scope/APB caveats (keep one in §1.3), duplicate tier definitions, §5.1 hardware list,
   restated container/kinematics caveats, background already in related work.
2. One claim per sentence; remove "critically/structurally/fundamentally".
3. Convert to the venue LaTeX template (IEEEtran / usenix); BibTeX from the reference list;
   measure pages; update `Makefile` to build the template PDF.
4. Anonymity sweep: repo name, commit metadata in artifacts, self-citations in third person, anonymized artifact URL.

## Phase 7 — Pre-submission gate — OPEN (reference check + `make numbers` pass today)

1. Re-run all five `sok-review-*` agents on the final PDF/markdown; every remaining "fatal/high" item
   must be fixed or explicitly argued in the paper.
2. Automated checks: reference script (every cite ↔ entry, no placeholders), `cost_model.py` self-check,
   link check on all URLs, spell-check.
3. Final read by a human outside the project (catches jargon the agents normalize).
4. Tag `submission-<venue>-2027`, push.

---

## Order and critical path

Phase 1 → (2 ∥ 3) → 4 → 5 → 6 → 7. Phase 4 is optional but it is the only step reviewers said
would move the verdict from Reject; all other phases make the paper *correct*, Phase 4 makes it *novel*.
Without Phase 4, target a workshop or a later cycle rather than risking an early reject.
