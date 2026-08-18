# SoK: Client-Side Anti-Automation Under VLM-Based Attack — From Probabilistic Forgery to Operator Synthesis

**Author:** Abel, T. K.

**Repository:** https://github.com/tomkabel/google-botguard-security-research

**Status:** Systematization of Knowledge (SoK) manuscript — analytical, no empirical measurements.

---

## Abstract

Client-side anti-automation has evolved through five architecturally distinct paradigms, culminating in a landscape where Vision-Language Models (VLMs) and agentic AI systems challenge the foundational assumptions behind probabilistic client-side defenses. This Systematization of Knowledge (SoK) is organized in two parts. **Part I (2010–2024)** systematizes the five architectural paradigms — Point-in-Time VM Attestation, Stateful Behavioral Telemetry, Behavioral Biometrics & Sensor Telemetry, Platform/OS-level Anonymous Attestation, and Hardware-Anchored Determinism — and reframes the L1–L4 defense-in-depth stack as a *historical diagnostic* lens rather than a prescriptive architecture, alongside a case study of the obfuscation-versus-symbolic-execution temporal arms race. **Part II** analyzes which architectural properties survive the VLM "Operator Synthesis" attack vector and which structurally degrade, an initial cost-accounting framework grounded in observable data (VLM inference pricing, proxy supply elasticity, state-orchestration overhead) with explicit empirical caveats, and an analysis of attestation-market centralization around the Apple/Google/Microsoft root-of-trust oligopoly. The paper contributes a taxonomy, a diagnostic framework, a cost model with acknowledged empirical gaps, and identifies the centralization problem as the defining open question — analytical clarity rather than empirical breakthroughs.

---

## Manuscript

The complete, self-contained manuscript — including its inline 85-reference bibliography — is in **`paper.md`** (8 sections across two parts).

## Build

```sh
make          # produces paper.pdf via pandoc + lualatex
make clean    # removes paper.pdf
```

## Repository Layout

| Path | Description |
|---|---|
| `paper.md` | Full self-contained manuscript (8 sections, inline 85-reference bibliography) |
| `README.md` | This file |
| `Makefile` | Builds `paper.pdf` from `paper.md` (pandoc, lualatex) |
| `AGENTS.md` | Working conventions for AI agents operating on this repo |

---

## Keywords

Client-side attestation, VLM-based automation, operator synthesis, browser fingerprinting, behavioral biometrics, Privacy Pass, Private Access Tokens, device-bound session credentials, anti-automation economics, systematization of knowledge

---

## Changelog

### v3.0 — Self-Contained Consolidation (2026)

- Inlined the bibliography (85 references, deduplicated and renumbered) into `paper.md`; removed the external `notes/bibliography.md`.
- Removed stale planning/review artifacts (outline, QA report, content audit) and orphaned figures that no longer matched the manuscript.
- Removed machine-local agent-tooling cruft and compiled binaries from version control; collapsed agent context to `AGENTS.md`.

### v2.0 — SoK Pivot (May 2026)

Rewrite from the v1.0 predictive/empirical draft into an analytical two-part SoK: removed fabricated calculus and engineering-hour estimates; expanded the reference base.

### v1.0 — Initial Draft (2024)

Original predictive/empirical draft. Superseded.

---

*This repository hosts an academic Systematization of Knowledge (SoK) paper. The work is purely analytical and comparative. It contains no empirical measurements of live production systems, no reverse-engineered proprietary code, and no novel attacks or defenses.*
