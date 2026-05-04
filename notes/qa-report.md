# QA Report — SoK: Architectural and Economic Ceilings of Client-Side Anti-Automation

**Date:** 2026-05-03 | **File Audited:** `paper.md` | **Status:** PASS

---

## 6.1 Empirical Claim Audit

| Red-Flag Term | Occurrences | Verdict |
|---|---|---|
| "PoC" | 1 (line 706) | **CLEAN** — describes external PoCs as a limitation of current methodology, not our own PoC |
| "experiment" | 1 (line 706) | **CLEAN** — same context as PoC |
| "observed" | 3 (lines 15, 43, 409) | **CLEAN** — all describe L1-L4 as "originally observed in Botguard VM" — historically accurate |
| "measured" | 4 (lines 365, 516, 543, 610) | **CLEAN** — cites other researchers' measurements (Caballero, Motoyama) or analytical concepts |
| "empirical" | 11 | **CLEAN** — all in context of "not empirical" disclaimers, "empirical calibration data that this SoK does not claim," or in reference titles |
| "our data" | 0 | **CLEAN** — absent |
| "we collected" | 0 | **CLEAN** — absent |
| "we ran" | 0 | **CLEAN** — absent |
| "20 IPs" | 0 | **CLEAN** — absent |
| "500 tokens" | 0 | **CLEAN** — absent |
| "24h" | 0 | **CLEAN** — absent |
| "hours" (cost estimates) | 2 (lines 474, 502) | **CLEAN** — "off-peak hours" (descriptive) and "hours or minutes" (analytical generalization, not fake estimate) |
| Calculus terms (derivative, logistic, $MC(V)$, $C_{token}$, $C(V)$, $\frac$) | 0 | **CLEAN** — zero calculus equations in manuscript |
| "40-60", "20-30", "15-25", "30-50" (engineer-hour estimates) | 0 | **CLEAN** — all fake hour estimates removed |
| "$3\alpha$", "$10\alpha$", "$50\alpha$" (regime multipliers) | 0 | **CLEAN** — regime table with fake multipliers removed |

**Verdict:** ZERO empirical liability items found. All 11 "empirical" mentions are in disclaimers explicitly stating this SoK does NOT present empirical measurements. Zero calculus equations. Zero fake engineering-hour estimates. Zero PoC data references.

---

## 6.2 Neutrality and Tone Audit

| Red-Flag Pattern | Occurrences | Verdict |
|---|---|---|
| "doomed to be bypassed" | 0 | **CLEAN** |
| "structurally doomed" | 1 (line 610) | **CLEAN** — appears ONLY in context of REJECTING this framing: "does NOT imply that software-only defenses are 'structurally doomed'" |
| "nobody sells gold for the price of silver" | 2 (lines 122, 867) | **CLEAN** — academically correct citation of Herley & Florêncio [47] |
| "stop chasing cryptographic guarantees" | 0 | **CLEAN** |
| "vendors are confused" | 0 | **CLEAN** |
| "industry lies about" | 0 | **CLEAN** |
| "should" (prescriptive) | 5 | **CLEAN** — used in descriptive contexts: citing Moore [48]'s argument, explaining what a property "should" be for valid detection |
| "must" (prescriptive) | 26 | **CLEAN** — all in analytical context describing architectural requirements ("the attacker must..."), not prescriptive imperatives |
| "ought" | 3 | **CLEAN** — all 3 in analytical context |
| "need to" (prescriptive) | 4 (lines 100, 177, 559, 628) | **CLEAN** — analytical contexts: "does not need to make... unforgeable" (describing forgery problem), "may not need human labor" (attacker capability), "does not need to make impossible" (analytical), "does not need to break" (analytical) |

**Language replacement verification:**
- "Software-only defenses are structurally doomed" → Replaced with "Software-only defenses are economically bounded by the proxy supply market, the temporal arms race, and the ML synthesis arms race." ✓ (Section 6.6)
- "Stop chasing cryptographic guarantees" → Replaced with "Client-side attestation operates under a forgery model rather than a cryptanalysis model, which imposes economic rather than mathematical bounds." ✓ (Section 5.8)

**Overall Tone Assessment:** The paper reads as an analytically neutral systematization. Every sentence describes *what is* — the architectures that exist, the costs they impose, the ceilings they face. There is no vendor bashing, no prescriptive doom-saying, no "consulting report" tone. The paper maintains the detached analytical stance expected of an SoK.

---

## 6.3 SoK Criteria Checklist

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Provides a **taxonomy** | ✅ PASS | 5 architectures + L1-L4 stack; Grand Taxonomy Table (Section 4.6) |
| 2 | **Compares** existing work rather than proposing new defense | ✅ PASS | Comparative analysis across all sections |
| 3 | **Clarifies terminology** across vendors | ✅ PASS | Explicit definitions of stateless vs. stateful vs. behavioral biometrics vs. anonymous attestation vs. hardware-anchored |
| 4 | Identifies **open problems** | ✅ PASS | Section 8 with 4 substantive research gaps |
| 5 | **Comprehensive** across ecosystem | ✅ PASS | Google, Cloudflare, Kasada, DataDome, Apple, IETF, WICG |
| 6 | **Free of unverifiable empirical claims** | ✅ PASS | Confirmed by 6.1 audit |
| 7 | **Analytically neutral** tone | ✅ PASS | Confirmed by 6.2 audit |
| 8 | **Methodology section** explaining systematization | ✅ PASS | Full Section 3 with PRISMA framework |
| 9 | **Dual-axis threat model** (Auth State × Attack Objective) | ✅ PASS | Section 1.3 with quadrant table |
| 10 | Anti-detect browsers framed as **conjunctive cost** | ✅ PASS | Sections 4.2, 6.5: `Cost_proxy + Cost_profile + Cost_license` |
| 11 | **Automated deobfuscation** in temporal arms race | ✅ PASS | Sections 5.7, 6.1: symbolic execution, differential analysis, neural models |
| 12 | **PRISMA Flow Diagram** as formal figure | ✅ PASS | `figures/prisma-flow.tex`; Section 3.4 |
| 13 | **Human labor** as global cost floor for behavioral biometrics | ✅ PASS | Sections 4.3, 5.2, 6.2: `min(Cost_ML_Inference, Cost_Human_Labor)` |
| 14 | **Infostealer / PPI malware economy** as bypass for HW-anchored | ✅ PASS | Sections 4.5, 7.1, 7.2: RedLine, Lumma, PPI pricing data |
| 15 | Grey-literature citations via **Wayback Machine** | ⚠️ PENDING | Noted in Methodology (Section 3.4) and Methodological Note (Appendix A). Archiving must be completed before submission but is noted as required. |
| 16 | Complex tables/figures drafted in **LaTeX/TikZ** | ✅ PASS | `figures/prisma-flow.tex`, `figures/taxonomy-table.tex`, `figures/auth-spectrum.tex` |

**Checklist Score:** 15/16 PASS, 1 PENDING (Wayback Machine archiving — procedural, not content).

---

## Reference Audit

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Total references | 50+ | 75 | ✅ PASS |
| 2021–2025 references | 15+ | 30+ | ✅ PASS |
| References from top-4 venues | Significant | Yes (IEEE S&P, USENIX, CCS, NDSS represented) | ✅ PASS |
| Fake/placeholder citations | 0 | 0 | ✅ PASS |
| "Industry" placeholder | 0 | 0 | ✅ PASS — removed from old README |

---

## Structural Integrity

| Check | Status |
|-------|--------|
| Section 1-9 structure matches outline | ✅ PASS |
| Abstract matches SoK standards | ✅ PASS |
| Contributions 1-4 match plan | ✅ PASS |
| Dual-axis threat model (not single-axis) | ✅ PASS |
| Five architectures (not four or six) | ✅ PASS |
| Compute-Bound Challenges properly demoted | ✅ PASS (Section 4.1, "Auxiliary Mechanisms") |
| L1 expanded with sensor telemetry | ✅ PASS (Section 5.2) |
| Temporal constraint framed as compute-vs-compute race | ✅ PASS (Sections 5.7, 6.1) |
| No fake hour estimates | ✅ PASS |
| Forgery Principle arc maintained throughout | ✅ PASS |
| Centralization vs. Anonymity Trade-off as lead open problem | ✅ PASS (Sections 7.4, 8.1) |
| PRISMA with exact counts and flow figure | ✅ PASS (Section 3.4) |

---

## Final Verdict

**PASS.** The manuscript meets all SoK quality criteria. Zero empirical liabilities, zero calculus, zero fake estimates. Tone is analytically neutral. Structure follows the plan exactly. Reference count (75) exceeds target (50+). All complex figures are LaTeX/TikZ-native. The only pending item is Wayback Machine archiving of grey-literature URLs (procedural, not content).
