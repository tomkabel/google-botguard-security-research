# Content Audit: README.md → SoK Classification

## KEEP (SoK-Ready Material)

| Section | Lines | Content | Fate |
|---------|-------|---------|------|
| Abstract (partial) | 17, para 1 sentences 1-2 | "forgery problem, not a cryptanalysis problem" thesis | Incorporate into Section 1.1 and 6.5 |
| 1.4 Threat Model | 48-57 | Three threat models table (Automated Abuse, Session Hijacking, Credential Phishing) with NIST SP 800-63 anchor | REPURPOSE into dual-axis framework (Section 1.3) — current table is single-axis (only threat model), needs expansion to add Auth State dimension |
| 2.1 Probabilistic vs Deterministic | 66-72 | Bot mitigation vs. identity authentication distinction | Rewrite into Background Section 2.1-2.2 |
| 2.3 Bearer Token Semantics | 78-80 | RFC 6750, RFC 7519 — bgRequest and PO tokens as bearer tokens; cannot cryptographically bind | Keep in Background or Section 4.1 |
| 3.2 L1-L4 Layers (conceptual) | 98-105 | Four defensive layers of Botguard VM | Extract as raw conceptual framework; generalize beyond Botguard in Section 5 |
| 3.5 Stateful Telemetry concept | 120-135 | C_stateful = C_aging + C_token; distinction between paradigms | Keep core insight; rewrite as Section 4.2 framework |
| 4.1 IP Reputation Burn | 244-245 | "Tragedy of the commons" — IP reputation as exhaustible shared resource | Rewrite for Section 6.3 |
| 5.0 DBSC/Passkeys analysis | 287-289 | Hardware-anchored auth non-substitutable for anonymous traffic | Keep; expand with infostealer/PPI economy in Section 4.5 and 7.1/7.2 |
| References (academic) | 322-328 | Saltzer, Schrittwieser, Callegati, Guerar, Bursztein, Bonneau, Ulqinaku, Laperdrix | Keep; expand with Phase 2 research |
| References (standards) | 331-337 | FIDO2, NIST 800-63-3, RFCs 8471/6750/7519/9449 | Keep; add RFC 9576/9577, WICG Private State Token |
| References (economic) | 353-357 | Varian, Moore, Anderson & Moore, Herley & Florêncio | Keep; add Motiee et al. on CAPTCHA farm economics |
| Forgery Problem Framing | 269-276 | "The adversary controls the execution substrate... This is why software-only attestation is architecturally bounded." | Extract core thesis; deploy throughout Sections 4, 5, 6 |

## REWRITE (Analytical Pivot Required)

| Section | Lines | Current Form | Required Transformation |
|---------|-------|-------------|------------------------|
| 1.1 Motivation | 31-33 | Botguard-specific | Generalize: "Bot mitigation vendors deploy VM-based attestation... Botguard is the most sophisticated example" |
| 1.2 Central Thesis | 37-39 | Framed as Botguard-specific contributions | Reframe as SoK contributions: taxonomy, generalized L1-L4, microeconomic analysis |
| 1.3 Research Contributions | 41-46 | Presents as novel empirical model (C(V), MC(V), NLSP) | Replace with: (1) taxonomy of 5 architectures, (2) generalized L1-L4 + temporal constraint, (3) microeconomic analysis, (4) centralization vs anonymity problem |
| 2.0 Background | 64-84 | Botguard-centric, brief | Expand to full SoK background: historical arc, all 5 paradigms, literature review |
| 3.1 Framework Definition | 90-95 | Botguard-specific layering definition | Generalize to vendor-neutral framework applicable to Turnstile, Kasada, etc. |
| 3.2 L1-L4 (detailed) | 98-105 | Botguard-specific opcodes | Rewrite as generalized L1-L4 with sensor telemetry under L1 |
| 3.5 Stateful Telemetry | 120-135 | Brief comparison | Expand into full Section 4.2 with conjunctive cost model |
| 3.6 Per-Token Cost Model | 137-215 | Full calculus: C(V), r(V) logistic, MC(V) derivative | DELETE all calculus. Replace with conceptual prose: "The attacker's per-token cost increases non-linearly at scale due to..." |
| 3.7 Three Regimes | 216-232 | Pseudoscientific table with numeric multipliers | DELETE. Replace with conceptual regime analysis without fake numbers |
| 4.0 Operational Constraints | 236-276 | "Operational Constraints" with equations | Extract qualitative insights; delete latency equation |
| 4.2 PO Token Multiplication | 250-264 | C_effective = C_token × N_videos | Rewrite as qualitative observation: "Per-request binding scales cost with target breadth" |
| 5.0 Industry Trajectory | 280-289 | 4 bullet points + DBSC/Passkeys section | Expand to full Section 7 covering all 5 paradigms + emerging standards |
| 6.0 Conclusions | 294-307 | "Key Findings," "For Defenders" prescriptive language | Rewrite as analytical conclusion: taxonomy summary, open problems, no prescriptions |
| Economic language | Throughout | "the adversary," "the attacker" used prescriptively | Maintain as descriptive: "an adversary," "attackers" |
| Threat model | 48-57 | Single-axis (threat model only) | Expand to dual-axis (Auth State × Attack Objective) |

## DELETE (Empirical Liability / Pseudoscience)

| Section | Lines | Description | Reason |
|---------|-------|-------------|--------|
| 3.3 Operational Cost Estimates | 107-118 | "40-60 hours," "20-30 hours," "15-25 hours," "30-50 hours" engineering estimates | Fake numbers. Author admits "not empirical measurements but engineering heuristics." Delete entirely. |
| 3.6.1 Browser Infrastructure Cost equation | 152-155 | C_browser(V) with c_0, k_throughput, quadratic c_1 | Fake calculus with fabricated constants |
| 3.6.1 IP Proxy Cost equation | 159-167 | p(V) step function with $0.50/GB, 20x-30x spread | Fake numeric estimates; keep conceptual insight only |
| 3.6.1 Stealth Maintenance Cost equation | 171-174 | C_stealth(V) with c_s, T_compile_life | Fake calculus; keep qualitative insight |
| 3.6.2 Reputation Failure Rate eq | 179-191 | r(V) logistic with r_0 "observed ~0.15-0.30" | DELETE fake observation; keep qualitative insight about logistic shape |
| 3.6.3 Marginal Cost analysis | 193-206 | Full derivative of MC(V) with NLSP amplification term | Pure fabrication |
| 3.6.4 Scalability Constraint | 208-214 | V_max equation, R_token derivation | Delete entire formalization |
| 3.7 Three Regimes Table | 220-224 | $3\alpha$, $10\alpha$, $50\alpha$ multipliers | Fabricated numbers; delete table |
| 4.1 Latency equation | 247 | Instance provisioning with μ, σ, z | Delete equation; keep qualitative observation |
| 4.2 PO Token equations | 256, 262 | C_effective, C_per_video formulas | Delete; keep qualitative insight |
| All "PoC" references | 60, 61, 183, 315 | "20 IPs, 500 tokens, 24h" | Delete all empirical claims |
| Appendix A | 313 | Statistical Power Analysis | Delete entirely |
| Appendix B | 314 | Replication Package | Replace with neutral methodological note |
| Appendix C | 315 | Preliminary PoC Data | Delete entirely |
| Abstract sentences 3-4 | 17 | "We formalize... NLSP... logistic function... marginal cost..." | Delete all formalization claims |
| Contributions 2-4 | 21-23 | "Formal economic model," "C_aging," "three-regime formalization" | Replace with SoK contributions |
| "Industry" placeholder | 167, 321 | `[Industry]` citation | Delete placeholder; replace with real citations |
| Future Work (empirical) | 307 | "1,000+ residential IPs, 90+ day measurement" | Delete empirical future work |
| 3.5.1 C_stateful equation | 128 | C_stateful = C_aging + C_token | Delete equation; keep distinction in prose |
| "Adversary Capability Model" | 109 | "Senior Security Engineer proficiency... APT team" framing | Delete; replace with reference to capability-based threat modeling in Section 3.2 |

## Summary

- **KEEP items:** 11 sections with salvageable intellectual assets
- **REWRITE items:** 16 sections needing analytical pivot
- **DELETE items:** 24 distinct calculus/empirical/fabricated elements
- **Total README.md sections classified:** All 361 lines covered
