# Paper TODO

## Status: FOURTH REVISION COMPLETE (Addressing Second-Round Senior Expert PC Member Critique — All 10 Points)

All critique points from the second-round senior expert PC member review have been addressed:

### ✅ Critique 1: Perfect Native Motor Control Fallacy (Section 1.4, 4.2)
- Section 1.4 bullet 2: Replaced "The motor control is native" with detailed discussion of the orchestration layer gap — VLMs output text/JSON coordinates, not raw OS input; orchestration layer (PyAutoGUI, accessibility APIs) must translate to kinematic trajectories; naive interpolation produces detectable artifacts
- Section 4.2 Type III: Reframed as "Degraded to Tier 2/3 (Cognitive selection bypassed; kinematic instantiation gap remains)"
- Explicitly states that behavioral biometrics retain leverage against poorly-implemented orchestration
- Acknowledges that sophisticated attackers can invest in kinematic-smoothing layers, but this adds engineering cost

### ✅ Critique 2: Pristine Environment Delusion (Section 4.1)
- Added "At Scale" column to the Assumptions table documenting containerization artifacts
- Added "The containerization gap" subsection: documents missing system fonts, WebGL mismatches, AudioContext profiles, TCP/IP stack fingerprints
- Acknowledges that L1a detection is NOT fully collapsed under industrial-scale deployment

### ✅ Critique 3: Economic Framework Hypocrisy (Section 5)
- Section title renamed: "A Rigorous Economic Framework" → "An Initial Cost Model for VLM-Driven Attacks"
- Removed all "pseudo-mathematical" language
- Removed dismissive references to prior work; replaced with respectful acknowledgment
- Added explicit acknowledgment of empirical gaps
- Changed Contribution C3 from "corrected economic framework" to "initial parametric cost model"

### ✅ Critique 4: Tone & Absolute Language (Abstract, Introduction, throughout)
- Abstract: "fundamentally invalidate" → "challenge"; "collapses" → "faces structural pressure"; "renders moot" → "renders moot for the APB threat model"; "corrected economic framework" → "initial cost model"; "replaces the stale... Trilemma" → "provides a concrete analysis"
- Added explicit APB (Advanced Persistent Bot) scope limitation in Section 1.2
- Section 1.1: "structurally obsolete" → "bypasses the core detection premise... for the APB threat model"
- Conclusion: toned down from "structurally failed" to "faces structural degradation"; added nuance about continued efficacy against commodity adversaries
- Part I framing: toned down from "structurally bypassed" to "face structural degradation for the APB threat model"
- Part II opening: added scope qualifier
- Removed "structurally obsolete" language throughout

### ✅ Critique 5: PRISMA Tantrum (Section 3.1)
- Replaced "creates an unwarranted appearance of methodological rigor that experienced reviewers correctly identify as methodology washing" with neutral language
- PRISMA figure: removed "PRISMA was deliberately not employed" commentary; replaced with factual methodological note

### ✅ Critique 6: Type II Stateful Telemetry Nuance (Section 4.2)
- Reframed as "Degraded to Tier 2/3 (Profile-aging constraint lifted; state-orchestration cost substituted)"
- Added discussion of stateless VLM cookie orchestration burden — maintaining, isolating, rotating aged profiles across thousands of parallel instances without cross-contamination
- Identifies state-orchestration complexity and infrastructure cost as partial substitute for anti-detect browser license

### ✅ Critique 7: Latency Cost Omitted (Section 5, new subsection 5.2)
- Added "The Latency Cost: Temporal Overhead as a Non-Trivial Attack Surface" subsection
- Documents 5–15s per VLM inference cycle, creating 25–150s per-token wall-clock time
- Identifies chronometric heuristic (L4 extension to operator timing) and session timeout risk
- Added `C_temporal = C_inference + C_bandwidth_per_session + C_timeout_loss` formula
- Notes the 50× gap between human reaction time (~100ms) and VLM inference time (~5s minimum)

### ✅ Critique 8: T_RE = 0 Qualified (Section 5.5)
- Section title: "Why T_RE ≈ 0 Is the New Normal (With a Critical Caveat)"
- Added "Critical caveat: T_RE is not zero for the target application" — attacker must RE DOM structure, navigation flow, interaction logic to write VLM prompts
- SPAs with dynamic DOM mutation impose higher application-level RE cost
- Documents how application-level workflow diversity can impose meaningful RE costs

### ✅ Critique 9: Trilemma Section Nuance (Section 6.3)
- Section renamed from "Why This Is Not a Trilemma" to "Reframing the Trilemma"
- Changed Contribution C4 from "replaces the prior trilemma" to "building on the prior trilemma framing"
- Acknowledges prior work [42, 43] as "usefully framed" and "correctly identified the structural tension"
- Positions the market consolidation analysis as an empirical corollary, not a refutation

### ✅ Critique 10: Over-indexing on Botguard (Section 3.4)
- Added explicit acknowledgment: "derived from the defense-in-depth architecture observed in Google's Botguard VM"
- Generalized language: "We present it in vendor-neutral terms while acknowledging that the precise instantiation of each layer varies across implementations"

### ✅ Scope Limitation Added
- Added explicit APB threat model scope section after the existing scope section
- Documents that probabilistic defenses remain effective against 95%+ of traffic
- All claims of "collapse" scoped through this lens

### ✅ Critique 10: Section 3.4 Table Contradiction (Zero Cost vs. Non-Zero Analysis)
- Replaced the entire L1-L4 table: all "Zero" cost entries changed to "Shifted to..." descriptions
- L1a: "Zero" → "Shifted to container-evasion engineering"
- L1b: "Zero" → "Shifted to kinematic-smoothing orchestration"
- L2: "Zero" → "Near-zero at VM level; shifted to app-level workflow RE"
- L3: "Zero" → "Near-zero"
- L4: "Zero" → "Shifted to latency-evasion at inference timescale"
- Bullet point descriptions updated to reflect non-zero shift framing
- Opening paragraph reframed: "the costs do not simply vanish to zero — they shift"
- Closing paragraph reframed: "the nature of the cost shifts from browser-instrumentation forgery to systems-integration engineering"

### ✅ Critique 11: L4 Mental Gymnastics (Section 5.2)
- Replaced defensive "While Section 3.4 correctly notes that L4 was designed to detect instrumentation-layer timing deviation" with owning the evolution
- New framing: "L4's detection premise is not obsolete; its target shifts"
- Explicitly states: "L4 therefore survives the paradigm shift"
- Identifies 25–50× latency gap as a potentially more robust detection surface than microsecond timing
- Acknowledges the attacker cannot close this gap through better orchestration

### ✅ Critique 12: Terminology — Cost-Accounting Framework (Section 5)
- "Parametric cost model" → "attacker cost-accounting framework" throughout
- Section 5 intro: added explicit disclaimer that the framework tallies costs without deriving supply/demand equilibria or utility functions
- Contribution C3: "Initial Parametric Cost Model" → "Initial Cost-Accounting Framework"
- Contribution list: "parametric cost model" → "cost-accounting framework"
- Abstract: "parametric cost estimates" → "observable cost data"
- Section 7.1: "parametric cost model" → "cost-accounting framework"

### ✅ Critique 13: C_timeout_loss Clarification (Section 5.2)
- Added "representing the expected inference cost from a geometric series of retries prior to success"

### ✅ Critique 14: SDK-Proxy Insight — Push Harder (Section 4.3)
- Added three-sentence paragraph on network-layer behavioral metadata as defender's only recourse against valid-but-attacker-controlled PAT attestations
- Explicitly ties hardware-attestation critique back to necessity of server-side stateful analysis
- Positions ASN reputation, IP-to-Account cardinality, velocity checks as critical complement

### ✅ Critique 15: APB Usage in Conclusion
- Conclusion opening paragraph: added "for the APB threat model" and replaced "all collapse" with per-layer cost-shift language
- L4 specifically called out as shifting from microsecond detection to second-scale latency profiling

### ✅ Critique 16: Privacy Regulation (Section 7.4)
- Added: "Privacy regulation structurally mandates the amnesia that VLMs mathematically exploit"
- Added analysis of how regulatory timeline and VLM capability timeline intersect to produce mutually reinforcing degradation of Type II defenses

## Remaining Work Before Submission

- [ ] Add reference [67] (RFC 6750, Bearer Token), [68] (RFC 7519, JWT), [69] (RFC 9449, DPoP)
- [ ] Add reference [79] (SDK proxy network whitepapers) and [80, 81] (VLM agentic benchmarking)
- [ ] Complete all LaTeX formatting (inline tables in Section 1.3)
- [ ] Archive all grey literature URLs via Wayback Machine
- [ ] Add the forward-looking research subsections to the bibliography references
- [ ] Review for consistency of VLM resilience tier language across all sections
- [ ] Compile LaTeX and verify figure rendering
- [ ] Final proofread for typographical errors
