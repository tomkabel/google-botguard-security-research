# Editorial Decision Package

**Manuscript:** SoK: Client-Side Anti-Automation After the VLM — From Probabilistic Forgery to Operator Synthesis
**Authors:** Abel, T. K.
**Review Date:** 2026-05-20
**Editor-in-Chief:** IEEE S&P Program Chair (Systems Security)

---

## Consolidated Review Matrix

| Dimension | EIC | R1 (Methodology) | R2 (Domain) | R3 (Perspective) | DA (Devil's Advocate) |
|-----------|-----|-------------------|-------------|-------------------|----------------------|
| **Overall Recommendation** | Major Revision | Minor Revision | Accept (minor rev) | Major Revision | CRITICAL flags |
| **Originality** | Moderate | Good | Strong | Strong | Questions core framing |
| **Methodology** | Adequate | Strong (with gaps) | N/A (domain focus) | Good (economic gaps) | Questions APB binary |
| **Technical Accuracy** | Good | N/A | Strong (3 corrections) | N/A | Challenges Tier 1 |
| **Significance** | High (contingent) | High | High | High | Undermines central thesis |
| **Writing Quality** | Good | Good | Good | Good | Good |

---

## Consensus Items (All 5 Reviewers Agree)

1. **The two-part SoK structure is methodologically appropriate.** All five reviewers endorse the decision to partition into a historical retrospective (Part I) and forward-looking analysis (Part II) as the correct response to the VLM paradigm shift.

2. **The L1–L4 cost-shift analysis is the paper's strongest contribution.** The recognition that costs under Operator Synthesis "shift rather than vanish" — to container-evasion, kinematic-orchestration, perceptual-DOM alignment, and second-scale latency profiling — is unanimously the paper's best analytical artifact.

3. **The SDK-proxy bypass of PATs/DBSC (§4.3) is a genuinely novel insight.** All five reviewers note that the observation that Bright Data-style SDK proxying routes through consenting devices with valid attestation keys fundamentally lowers the bypass ceiling for Tier 1 architectures.

4. **The paper requires empirical anchoring.** Consensus that the cost-accounting framework (Section 5) needs either concrete measurements or an explicit reframing as a qualitative cost checklist.

5. **The latency gap analysis (§5.2) is a significant new detection surface idea.** All reviewers recognize the novelty of shifting chronometric analysis from microsecond instrumentation detection to second-scale operator profiling.

---

## Disagreements and Divergent Opinions

### 1. Part I Length and Derivative Status
- **EIC:** Part I is too derivative of prior work [6, 24] and does not earn its ~90-line length.
- **R2 (Domain):** Part I is appropriate — provides the necessary foundation for the cost-shift analysis.
- **Resolution (EIC/R2 split):** Part I should be condensed but not eliminated. The domain framing is necessary for non-specialist readers (SoK audience). Compromise: retain the architectural classification (§3.2) and the L1–L4 framework (§3.4), condense the background history (§3.5) into a summary paragraph.

### 2. reCAPTCHA v3 Classification
- **R2 (Domain):** reCAPTCHA v3 should be classified as Type II/Type I hybrid, not pure Type II.
- **All other reviewers:** Noted but did not independently evaluate.
- **Resolution:** Adopt R2's correction for the vendor-mechanism matrix.

### 3. Economic Framework: Description vs. Model
- **EIC:** The cost-accounting framework is arithmetic, not economic — it tallies costs without deriving equilibria or decision-relevant quantities.
- **R1 (Methodology):** The framework is appropriately scoped as an "initial" contribution; the honesty about empirical gaps is a strength.
- **R3 (Perspective):** The framework needs equilibrium modeling, cost-floor bounding, and a hybrid attacker model.
- **Resolution (consensus with EIC/R3 lean):** The framework should be retitled "Structured Cost-Accounting Exercise" or similar. Add cost-floor estimates, equilibrium analysis, and a hybrid attacker subsection.

### 4. "Paradigm Shift" vs. "Incremental Escalation"
- **DA (CRITICAL):** The central framing overstates the break — VLM attacks are detectable through the same environmental channels; this is a more sophisticated forgery, not a category change.
- **EIC:** Agrees — the "paradigm shift" rhetoric should be dialed back.
- **R2:** Accepts "Operator Synthesis" as a category change because the browser runtime itself is legitimate.
- **Resolution:** Retain "Operator Synthesis" as a distinct attack vector (the paper's strongest conceptual contribution) but temper "paradigm shift" language. Replace with "Operator Synthesis as a new attack paradigm within the APB threat model."

---

## Devil's Advocate CRITICAL Issues — Special Flags

The following CRITICAL issues identified by the Devil's Advocate **must** be addressed before publication per IRON RULE #4:

### DA-CRITICAL-1: The "Category Change" Framing Overstates the Break
The DA argues: the paper describes a paradigm shift but its own evidence shows the same cat-and-mouse game continuing at new layers — container-evasion, kinematic-smoothing, second-scale latency profiling are all *forms of environmental forgery at different layers*. The VLM is a more sophisticated forger, not a fundamentally different threat.

**Required revision:** Either (a) provide stronger evidence that Operator Synthesis constitutes a categorical break (e.g., empirical measurements showing L1–L4 bypass rates >95% for VLM-driven sessions vs. <5% for commodity automation), or (b) reframe the paper around the more defensible claim — that Operator Synthesis represents the *most severe escalation* within the Environmental Forgery paradigm, requiring a re-evaluation of defense economics and architectural priorities.

### DA-CRITICAL-2: The APB/Commodity Bot Binary Excludes the Middle Tier
The DA argues: the paper acknowledges a middle tier (Puppeteer + anti-detect farms that operate below VLM cost thresholds) but then ignores it in all substantive analysis. Many of the paper's claims about "VLM degradation" apply equally to sophisticated Puppeteer/Playwright farms with anti-detect fingerprints that already defeat probabilistic defenses without VLMs.

**Required revision:** (a) Incorporate the middle tier into the threat model as a distinct adversary class with its own cost surface, or (b) explicitly justify why the binary is analytically necessary despite its acknowledged incompleteness, and (c) revisit the degradation analysis to ensure claims attributed to "VLM/Operator Synthesis" are not equally applicable to non-VLM automation at comparable spend.

### DA-CRITICAL-3: Tier 1 PAT Classification is Contradicted by the Paper's Own Analysis
The DA argues: if SDK-based proxy networks (Bright Data) can generate valid PAT attestations through consenting devices at effectively zero marginal cost per attested device (once the SDK is deployed), PATs are not "structurally resilient" (Tier 1). The paper's own §4.3 analysis contradicts its §4.2 tier assignment.

**Required revision:** Reconcile the contradiction. Either (a) downgrade PATs to Tier 2 with the SDK-proxy bypass articulated as the degradation mechanism, or (b) explicitly define "structural resilience" as resilience against *Operator Synthesis specifically* (not against the separate device-compromise attack chain), and restructure the resilience criteria accordingly.

---

## Editorial Decision Letter

**Decision: Major Revision** (Not Accept due to DA-CRITICAL constraints. Not Reject — the paper has genuine contributions and the structural issues are addressable.)

Dear Authors,

Thank you for submitting your SoK manuscript on client-side anti-automation under VLM-based attack. The paper has been reviewed by four peer reviewers and a Devil's Advocate. All five reviewers recognize the timeliness and potential significance of this work, particularly the L1–L4 cost-shift diagnostic framework (C2), the SDK-proxy bypass analysis (§4.3), and the latency cost identification (§5.2).

However, the review panel has identified three structural issues that prevent acceptance in the current form:

**1. The "Operator Synthesis" framing needs recalibration.** The Devil's Advocate's CRITICAL-1 finding — that your own evidence shows VLM-based attacks are detectable through the same environmental channels (container-artifacts, kinematic traces, chronometric profiles) — undermines the "category change" claim. We recommend reframing the paper as documenting the *most severe escalation* within the Environmental Forgery paradigm rather than a categorical break. This does not diminish the contribution; it makes it more defensible.

**2. The APB/Commodity Bot binary needs resolution.** CRITICAL-2 correctly identifies that a significant middle tier of sophisticated Puppeteer/Playwright farms achieves similar effects without VLM cost. Your degradation analysis must either incorporate this tier explicitly or justify why the binary simplification is analytically necessary and does not inflate the VLM's apparent impact.

**3. The resilience tier assignment for PATs is internally inconsistent.** CRITICAL-3 identifies that your own SDK-proxy bypass analysis (§4.3) contradicts the Tier 1 assignment for PATs (§4.2). Either downgrade PATs or clarify the resilience criteria.

Beyond these CRITICAL issues, the EIC and Perspective Reviewer identified additional major concerns that must be addressed:

- Condense Part I or justify its length relative to prior work.
- Provide empirical grounding for the cost-accounting framework, or rename it to reflect its qualitative nature.
- Address the server-side defense inconsistency (Section 4.3 vs. scope).
- Add cost-floor estimates and supply elasticity equilibrium analysis to the economic section.
- Develop the ad-tech macroeconomic observation into a structured analysis.
- Correct the reCAPTCHA v3 classification (R2 finding).
- Correct the 25–50× latency gap to a defensible 5–10× (R2 finding).

We look forward to receiving a revised manuscript addressing these concerns.

Sincerely,
Editor-in-Chief

---

## Revision Roadmap (Prioritized)

### Critical (Must Address Before Resubmission)

| Priority | Issue | Source | Section | Action |
|----------|-------|--------|---------|--------|
| **C1** | DA-CRITICAL-1: Framing overstatement | DA, EIC | Title, §1, §4 | Reframe "paradigm shift" → "most severe escalation." Retain "Operator Synthesis" as distinct attack vector. |
| **C2** | DA-CRITICAL-2: APB binary excludes middle tier | DA, R3 | §1.2, §4.2, §5 | Incorporate or justify the middle-tier exclusion; revise degradation claims to isolate VLM-specific effects. |
| **C3** | DA-CRITICAL-3: PAT Tier 1 inconsistent with §4.3 | DA | §4.2, §4.3 | Reconcile: either downgrade PATs to Tier 2 or restructure resilience criteria. |
| **C4** | Empirical anchoring for cost framework | EIC, R1, R3 | §5 | Add at least one empirical measurement or rename to "structured cost checklist." |
| **C5** | Part I length vs. derivative status | EIC | §3 | Condense §3.5 (temporal arms race) to summary; retain §3.2 and §3.4. |

### Major

| Priority | Issue | Source | Section | Action |
|----------|-------|--------|---------|--------|
| M1 | Server-side defense inconsistency | EIC | §1.2 vs. §4.3 | Either include server-side defenses in scope or modify the §4.3 claim. |
| M2 | reCAPTCHA v3 misclassification | R2 | §3.2 | Reclassify as Type II with Type I auxiliary. |
| M3 | 25–50× latency gap exaggeration | R2 | §5.2 | Correct to 5–10×; use total challenge completion time baseline (~3s), not reaction time (~200ms). |
| M4 | Ad-tech observation underdeveloped | R3 | §6.3, §7.4 | Expand from one-sentence observation to structured 1–2 paragraph analysis. |
| M5 | Cost framework: deflation lacks cost floor | R3 | §5.1 | Add physical cost-floor bounding (energy+hardware amortization). |
| M6 | Cost framework: static supply elasticity | R3 | §5.3 | Add equilibrium argument: VLM demand for premium proxies raises equilibrium prices. |
| M7 | Section 3.2 absolutism contradicts §4.2 | R2 | §3.2, §4.2 | Reconcile: §3.2 Type I/III claims of "cease to impose costs"/"collapses entirely" must align with §4.2's nuanced Tier 2/3 analysis. |
| M8 | Missing exclusion criteria in search methodology | R1 | §3.1 | Add exclusion criteria; note how many items retrieved vs. included. |

### Minor

| Priority | Issue | Source | Section | Action |
|----------|-------|--------|---------|--------|
| N1 | Google Scholar non-reproducible | R1 | §3.1 | Remove from enumerated databases or document as supplementary discovery. |
| N2 | No deduplication methodology | R1 | §3.1 | Add deduplication flow. |
| N3 | No forward snowballing documented | R1 | §3.1 | Add forward citation tracking note. |
| N4 | Grey literature quality assessment missing | R1 | §3.1 | Add assessment framework statement. |
| N5 | SDK/Secure Enclave access mechanism | R2 | §4.3 | Acknowledge iOS API consent requirements; preserve economic insight. |
| N6 | China/Russia platform dimension | R3 | §6.3 | Add one-sentence scope limitation. |
| N7 | GDPR vs. ITP/ETP conflation | R3 | §7.4 | Distinguish regulatory mandates from browser-vendor voluntary actions. |
| N8 | Missing hybrid attacker model | R3 | §5.4 | Add subsection on VLM + scripted automation + human click-farm hybrid. |
| N9 | Missing trilemma chain connection | R3 | §6.3, §7.4 | Connect privacy → Type II degradation → PAT adoption → platform linkability into explicit chain. |
| N10 | L1–L4 framework single-system derivation | R1 | §3.4 | Add comparative table mapping multiple implementations to L1–L4. |
| N11 | No historical trace for L1–L4 diagnostic claim | R1 | §3.4 | Add brief mapping to documented bypass milestones. |
| N12 | State-orchestration cost unquantified | R3 | §5.3 | Add approximate order-of-magnitude estimate. |
| N13 | No sensitivity analysis | R1, R3 | §5 | Add short parameter-variation robustness check. |
| N14 | Retry independence assumption | R1 | §5.2 | Acknowledge heavy-tailed failure distributions. |
| N15 | Defender cost model absent | R1 | §4, §5 | Add brief discussion of defender-side costs (FP rate, deployment cost). |
| N16 | Multi-modal latency distribution analysis | R2 | §5.2 | Acknowledge shape-of-distribution vs. mean-difference framing. |
| N17 | Missing agentic framework citations [80,81,82] | EIC, R2 | Throughout | Add WebVoyager, WebArena, CUA, Mind2Web citations. |
| N18 | No regulatory prescription | R3 | §7.4 | Add brief forward-looking policy recommendation. |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Recommendation | **Major Revision** |
| CRITICAL issues (DA) | 3 (all must be resolved) |
| MAJOR issues | 8 |
| MINOR issues | 18 |
| Total actionable items | 29 |
| Reviewers in agreement on core contribution | 5/5 (L1–L4 cost-shift analysis) |
| Reviewers recommending Accept after revisions | 4/5 (conditional) |
| Anti-patterns detected | 0 (no fabrication, no rubber-stamping, no sycophancy) |
