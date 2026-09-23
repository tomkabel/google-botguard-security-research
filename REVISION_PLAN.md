# Revision Plan — SoK: Client-Side Anti-Automation Under VLM-Based Attack

Consolidates every finding from the five mock review boards (IEEE S&P, USENIX Sec '27, ACM CCS '27,
IEEE EuroS&P, PoPETs '27; all **Reject**, 1.5–2/5) and tracks it to a final fix.

Status legend: **DONE** = fixed in `c7288da` (text-only pass) · **VERIFY** = fixed but rests on
unchecked facts · **OPEN** = not yet addressed · **AUTHOR** = needs author input/decision.

Baseline after `c7288da`: ~18.8k words, 109 refs, no figures, markdown only.

---

## 0. Critique inventory (what the boards said → where it stands)

| # | Finding (boards raising it) | Status |
|---|---|---|
| F1 | L1–L4 attributed to [24], which never mentions Botguard (all 5) | DONE (recast as own model) — needs Phase 2 evidence |
| F2 | Tier 1 "resilient" is a category error; device farms ignored (all 5) | DONE (reframed) — needs Phase 3 cost analysis |
| F3 | Protocol errors: PAT attester/issuer, DBSC owner/export, PST, SDK proxies, iOS consent, unlinkability (all 5) | DONE / VERIFY |
| F4 | §5 formula & arithmetic errors, unsourced prices (all 5) | DONE; prices partly VERIFY |
| F5 | Self-contradictions: Axis C, profile aging, "arms race moot" (all 5) | DONE |
| F6 | Leftover revision-response text, phantom cross-refs (all 5) | DONE |
| F7 | Citation misuse ([67],[68],[71],[42],[73–75],[49], secondary 99.8%) (all 5) | DONE |
| F8 | §3.1 methodology not systematic; corpus = reference list (all 5) | Partly DONE (honest wording) — OPEN: real protocol + coding sheet |
| F9 | Missing related work (≥3 boards) | DONE (§2.5) — VERIFY summaries |
| F10 | PACT built on news/blogs (all 5) | DONE (primary sources) |
| F11 | Anonymity, ethics, Open Science, AI-use disclosure (USENIX, S&P, Euro) | DONE except AI-use = AUTHOR |
| F12 | No measurement at all; VLM vs scripted OS-input confound (all 5; S&P fatal) | **OPEN** — Phase 4 |
| F13 | Page limit: likely 15–20+ pages (USENIX, S&P) | **OPEN** — Phase 6 |
| F14 | No systematization figure; tables lack per-cell citations; no comparison vs prior surveys (S&P, Euro) | **OPEN** — Phase 5 |
| F15 | Cognitive honeypot untested (S&P, USENIX, CCS) | Redesigned — OPEN: test in Phase 4 |
| F16 | Privacy not central (PoPETs) — only if targeting PETS | AUTHOR (venue choice) |
| F17 | Hybrid attacker model (S&P) | DONE (qualitative) — OPEN: sensitivity table |
| F18 | Repetition / hedging / prose density (all 5) | Partly DONE — OPEN in Phase 6 |
| F19 | Ethics of Botguard RE if L1–L4 came from own analysis (S&P, PETS) | AUTHOR |

---

## Phase 1 — Decisions and verification debt (≈2 days, blocks everything)

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

## Phase 2 — Ground the L1–L4 model (F1, F19) (≈1 week)

- **Path A (own RE):** add §3.4.1 "Analysis method": Botguard script versions/dates collected, tooling,
  what was observed per layer, what was inferred; ToS/legal basis; disclosure to Google (date);
  release sanitized notes as artifact. Update Ethics section accordingly.
- **Path B (synthesis):** add a per-layer evidence table: layer → public source(s) (Picasso, public
  deobfuscation write-ups, vendor docs) → claim strength (documented / inferred / hypothesized).
  Remove any layer detail that has no public source.
- **Done when:** no L1–L4 sentence lacks either a citation or an explicit "we hypothesize".

## Phase 3 — Strengthen the analytical core (F2, F4, F17) (≈1 week)

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

## Phase 4 — Minimal ethical measurement (F12, F15) (≈2–3 weeks) — biggest verdict lever

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

## Phase 5 — Systematization quality (F8, F14, F16) (≈1 week)

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

## Phase 6 — Length, prose, format (F13, F18) (≈3–4 days)

1. Target ≈11–12k words body for a 13-page two-column limit (current ≈18.8k → cut ~35%).
   Cuts: repeated scope/APB caveats (keep one in §1.3), duplicate tier definitions, §5.1 hardware list,
   restated container/kinematics caveats, background already in related work.
2. One claim per sentence; remove "critically/structurally/fundamentally".
3. Convert to the venue LaTeX template (IEEEtran / usenix); BibTeX from the reference list;
   measure pages; update `Makefile` to build the template PDF.
4. Anonymity sweep: repo name, commit metadata in artifacts, self-citations in third person, anonymized artifact URL.

## Phase 7 — Pre-submission gate (≈2 days)

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
