# SoK: The Architectural and Economic Ceilings of Client-Side Anti-Automation

---

**Authors:** Abel, T. K.

**Repository:** https://github.com/tomkabel/google-botguard-security-research

**Status:** Systematization of Knowledge (SoK) manuscript — analytical, no empirical data.

---

## Abstract

Client-side anti-automation — the set of techniques that distinguish human-driven browsers from automated agents — has evolved through five architecturally distinct paradigms over the past fifteen years. Despite this rich design space, the industry lacks a unified taxonomy, and recent innovations (Private Access Tokens, behavioral biometrics with sensor telemetry, device-bound session credentials) have fragmented the landscape further. This paper presents a Systematization of Knowledge (SoK) that proposes a comparative taxonomy of five primary defense classes — Stateless VM Attestation, Stateful Behavioral Telemetry, Behavioral Biometrics & Sensor Telemetry, Platform/OS-level Anonymous Attestation (Privacy Pass / PATs), and Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys) — compared across ten dimensions. We generalize the L1–L4 defense-in-depth framework beyond its Botguard-specific origins, introduce a novel temporal constraint analysis (Defender AST Obfuscator vs. Attacker Symbolic Execution Engine), and provide a conceptual microeconomic analysis identifying three structural corrections: (a) anti-detect browsers impose a conjunctive, not alternative, cost structure; (b) human labor sets the global cost floor for behavioral biometrics; and (c) the temporal arms race is increasingly compute-driven. We identify the Centralization vs. Anonymity Trade-off as the defining open problem in anonymous attestation. The paper includes a PRISMA flow diagram, a Grand Taxonomy Table, an Anonymous-Authentication Spectrum figure, and a 75-reference bibliography. This work is a contribution in systematization: it provides analytical clarity rather than empirical breakthroughs.

---

## Manuscript

The complete manuscript is available at **[paper.md](paper.md)**.

## Repository Structure

| Path | Description |
|---|---|
| `paper.md` | Full SoK manuscript (9 sections, 75 references) |
| `notes/content-audit.md` | Phase 1: Classification of prior README content |
| `notes/bibliography.md` | Phase 2: Curated 75-reference bibliography by topic |
| `notes/outline.md` | Phase 3: Detailed section-level outline |
| `notes/qa-report.md` | Phase 6: Empirical claim audit, neutrality audit, SoK checklist |
| `figures/prisma-flow.tex` | PRISMA flow diagram (LaTeX/TikZ) |
| `figures/taxonomy-table.tex` | Grand Taxonomy Table — 5 architectures × 10 dimensions (LaTeX) |
| `figures/auth-spectrum.tex` | Anonymous-Authentication Spectrum figure (LaTeX/TikZ) |

---

## Changelog

### v2.0 — SoK Pivot (May 2026)

**Complete rewrite from predictive/empirical draft to analytical Systematization of Knowledge:**

- **Removed:** All calculus (derivatives, logistic curves, $MC(V)$, $C_{token}(V)$), the 20-IP/500-token PoC, fake engineering-hour estimates (40-60h, etc.), all references to "our PoC" or "observed" failure rates, Appendix C (experimental data), Appendix A (statistical power analysis), three-regime table with numeric multipliers ($3\alpha$, $10\alpha$, $50\alpha$).
- **Added:** Five-architecture taxonomy including Behavioral Biometrics & Sensor Telemetry and Privacy Pass / PATs as primary pillars; generalized L1–L4 framework with sensor telemetry under L1; dual-axis threat model (Authentication State × Attack Objective) anchored on OWASP OAT + NIST 800-63; temporal constraint analysis (symbolic execution vs. compile rotation); human labor cost floor analysis (CAPTCHA farms); Infostealer/PPI malware economy as bypass for hardware-anchored determinism; Centralization vs. Anonymity Trilemma; PRISMA flow diagram with 75-reference bibliography; three standalone LaTeX/TikZ figures.
- **Tone:** Shifted from prescriptive/consulting to analytically neutral SoK.
- **References:** Expanded from ~20 to 75 (30+ from 2021–2025), spanning top-4 security venues, IETF/W3C standards, and peer-reviewed grey literature.

### v1.0 — Initial Draft (2024)

Original predictive/empirical paper with Botguard economic model, L1-L4 layers, and 20-IP PoC. Superseded by v2.0 SoK.

---

## Keywords

Client-side attestation, bot mitigation, JavaScript virtual machine, browser fingerprinting, behavioral biometrics, Privacy Pass, Private Access Tokens, device-bound session credentials, anti-automation economics, systematization of knowledge

---

*This repository hosts an academic Systematization of Knowledge (SoK) paper. The work is purely analytical and comparative. It contains no empirical measurements of live production systems, no reverse-engineered proprietary code, and no novel attacks or defenses.*
