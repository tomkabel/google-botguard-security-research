# SoK: Where Input Enters — Client-Side Anti-Automation When AI Agents Drive Unmodified Browsers

---

**Authors:** Anonymous submission

**Keywords:** Client-side anti-automation, input injection, VLM agents, computer-use agents, browser fingerprinting, behavioral biometrics, Privacy Pass, Private Access Tokens, attestation centralization, systematization of knowledge

---

## Abstract

Client-side anti-automation assumes that a bot runs inside, or instruments, the browser it drives. We argue that the property that decides detection is where input enters: inside the browser runtime (Environmental Forgery) or at the operating system, into an unmodified browser (Operator Synthesis). OS-level input is old; vision-language-model (VLM) agents make it cheap on every site. We systematize five defense paradigms along this axis, give a caveated cost-accounting exercise, and test it on a self-hosted testbed. In-runtime and kinematic signals separated how input was injected, not whether a VLM chose it: a straightness rule flagged scripted and VLM pointer jumps alike and missed a textbook smoothed path. What the VLM added was generalisation: on nine unseen form variants it passed 17 of 18 runs where base-form scripts passed at most 6. Two small open-weights VLMs acted in 1–2 s per call, and the cheaper one finished a five-field flow for about the price of one human CAPTCHA solve. Hardware-anchored attestation is indifferent to input modality; it moves attacker cost to real devices and accounts and concentrates trust in a few vendors and issuers.

---

## 1. Introduction

### 1.1 Why the Field Needs a Diagnostic Taxonomy

Client-side anti-automation terminology is fractured. "Bot detection" may mean a point-in-time VM executing encrypted bytecode (Google Botguard), a long-term behavioral scoring engine (reCAPTCHA v3), or a hardware-attestation protocol (Apple Private Access Tokens) [1, 2]. "Fingerprinting" can denote passive environmental introspection, active behavioral telemetry, or cryptographic token issuance [3, 4]. This imprecision obstructs comparative analysis.

Since 2024, computer-use agents such as OpenAI's Operator [5] and research agents such as WebVoyager [6] drive an unmodified browser from outside it, using screenshots. We call this attack vector *Operator Synthesis*. It is not new in kind (xdotool-style OS input predates VLMs), but VLMs remove the per-site script, so where input enters becomes the organising lens. We first analyse what probabilistic client-side defenses were built to detect (Section 3), then ask which of their properties survive when the attacker never touches the browser runtime (Sections 4–6).

### 1.2 Contributions

**C1 — Injection Point as the Organising Axis, With Measured Costs (Sections 4–5).** We classify attacks by where input enters (Axis C) and show which defense signals survive each. We estimate attacker costs from observable market data and extend the conjunctive cost framework to the VLM attacker's state-isolation requirements. A self-hosted measurement (Section 5.7) refutes the latency assumption for fast small models, puts the cheaper model's whole-flow cost at the price of one human CAPTCHA solve, and shows what the VLM adds: on nine unseen form variants it passed 17/18 runs where base-form scripts passed at most 6/18, while a kinematic rule flagged both alike.

**C2 — Attestation Market Centralization Analysis (Section 6).** Building on the centralization tension in anonymous token issuance [7, 8], we analyse who holds the roots of trust (Apple, third-party issuers, Google, passkey synchronisers). This dependency turns the "Anonymous Authentication Gap" into an economic and governance centralization problem, which the 2026 PACT initiative [9] extends to issuer judgment (Section 6.4).

**C3 — An Analytical Model of Point-in-Time VM Attestation (Section 3.4).** We propose a four-layer model of generic point-in-time VM challenges, synthesised from the obfuscation literature [10] and public descriptions of Botguard-style VMs [11], its best-documented (mostly grey-literature) instance, as a diagnostic lens for *why* VM-based attestation loses cost-imposing force under Operator Synthesis.

### 1.3 Threat Model and Scope

**Scope.** We cover client-side anti-automation in web browsers. Server-side defenses (WAF, TLS fingerprinting, rate limiting) are out of scope except where client-side schemes depend on them (§4.3, §5.3). Part I covers 2010–2024; Part II covers Operator Synthesis from 2024.

**Adversary tiers and the APB.** (1) **Commodity Bot:** scraper scripts, `curl`, headless browsers, low-scale Puppeteer. (2) **Sophisticated Automation (Middle Tier):** Puppeteer/Playwright farms with residential proxies, anti-detect browsers, and aged profiles. This tier bypasses probabilistic defenses through engineering rather than VLM inference, at costs dominated by proxies and anti-detect licences (illustratively $500–$5,000 and $30–$300 per operator-month; our assumption). (3) **Advanced Persistent Bot (APB):** highly-resourced adversaries using VLMs, custom orchestration, and industrial-scale proxy infrastructure, whose costs are dominated by VLM inference. VLMs amplify the middle tier's degradation of probabilistic defenses rather than causing it (Section 4.2). "Degradation" means: degraded for APBs, less so for the middle tier, still viable against Commodity Bots.

**Three axes.** Axis C is the primary lens.

- **Axis A — Authentication State:** Anonymous vs. Authenticated [12].

- **Axis B — Attack Objective:** Resource Exhaustion/Scraping vs. Account Takeover/Fraud [13].

- **Axis C — Attack Vector, defined by where input is injected:** **Environmental Forgery** injects input and forges signals *inside* the browser runtime (DOM APIs, synthesized JavaScript events, CDP/WebDriver, patched builds). **Operator Synthesis** injects OS-level input into an *unmodified* browser, with a VLM or agent choosing actions from the rendered screen.

| | **Anonymous** | **Authenticated** |
|---|---|---|
| **Scraping / Resource Exhaustion** | Quadrant I: Point-in-Time VM, Behavioral Biometrics, Compute-Bound Challenges (auxiliary) [13] | Quadrant III: Session-bound rate limiting, quota enforcement |
| **Account Takeover / Fraud** | Quadrant II: Stateful Telemetry (login risk scoring), Platform Anonymous Attestation (PATs) [13] | Quadrant IV: Hardware-Anchored Determinism (DBSC, Passkeys, WebAuthn) [12] |

Table: Axis A/B quadrants (NIST SP 800-63-3 [12], OWASP [13]).

Axis C cuts across all four quadrants. OS-level input injection (xdotool, AutoHotkey, PyAutoGUI) long predates VLMs. The VLM adds perception and cross-site generalisation, so OS-level injection needs no per-site scripts and becomes cheap at scale. Detection moves to container artifacts, input kinematics, and inference cadence (Sections 4.1, 5.2).

### 1.4 Operator Synthesis as the Central Framing

Computer-use VLMs (OpenAI's CUA [5], Claude and Gemini models, WebVoyager [6]) make Operator Synthesis practical for the APB, with three properties.

1. **The browser is legitimate.** The VLM does not instrument the DOM, forge `navigator` properties, or subvert WebGL. The unmodified browser passes the runtime's principal integrity checks.

2. **Motor control depends on orchestration.** VLMs output text, bounding boxes, or structured actions, not OS-level input events. An orchestration layer (PyAutoGUI, xdotool, OS accessibility APIs) turns each target coordinate into a trajectory; injecting via Puppeteer/CDP instead falls back into Environmental Forgery. Linear interpolation or generic easing remains distinguishable from human movement, so behavioral biometrics (Type III) retain leverage *even when the VLM's task selection is correct*. This layer decides whether L1b detection remains viable (Section 3.4).

3. **Detection moves to the deployment layer.** Industrial-scale VLM deployment leaves detectable OS- and network-layer artifacts (Sections 4.1, 5.1).

We define **input synthesis** as the translation of a VLM's output into OS-level input events. Synthesized OS-level input is indistinguishable from physical input at the JavaScript layer and is observable only through deployment-layer signals (Sections 4.1, 5.2). Legitimate agents (WebVoyager [6], Mind2Web [14]) run the same perceive–select–synthesize loop; the adversarial variant differs only in its deployment stack. We use "Operator Synthesis" and "VLM-based attack" interchangeably.

---

## 2. Background and Related Work

### 2.1 A Brief History of Client-Side Anti-Automation

Server-side heuristics gave way to text, image and audio CAPTCHAs [15, 16]. By 2014 a deep network solved the hardest reCAPTCHA text challenges with 99.8% accuracy [17]. JavaScript challenges and reCAPTCHA v2's checkbox (December 2014) [18] followed, then JavaScript VMs executing obfuscated bytecode (Google Botguard, later Kasada) [11, 19]. Since 2020 the field has diversified into behavioral telemetry, biometrics and sensor telemetry [20–22], anonymous attestation (Privacy Pass, PATs, PACT) [1, 4, 9, 23], and hardware-anchored sessions (DBSC) [24, 25]. From 2025, VLMs solve generalized CAPTCHAs [26, 27].

### 2.2 From CAPTCHAs to JavaScript VMs

VM-based attestation shifts the proof from *humanness* to *environmental integrity*: the runtime, DOM, WebGL and timer APIs must behave as in a legitimate browser [3, 11]. Laperdrix et al. [3] catalog this surface; later work measured it at scale [28–30] and spoofed single dimensions [31]. The weakness is a failure of *complete mediation* [32]: the check runs in an environment the attacker controls.

### 2.3 From Probabilistic Scoring to Hardware-Anchored Determinism

Probabilistic defenses produce confidence scores from noisy sensor data [33]. Deterministic defenses (FIDO2/WebAuthn, DBSC) prove hardware key possession [12, 34] but require prior enrollment and cannot screen anonymous traffic [12]. Privacy Pass [35] and Apple PATs [1] bridge this "Anonymous Authentication Gap" cryptographically [4, 36, 37], at the cost of vendor centralization (§6). PACT [9] attests personhood or account standing through *issuer judgment* rather than hardware [38, 39].

### 2.4 The Economics-of-Security Lens

Anderson and Moore framed security as an economic problem [40], extended to policy [41] and cybercrime costs [42]. Herley and Florêncio [43] argued that credential markets are lemon markets whose advertised prices overstate attacker returns; we apply this caution to the prices in §5. Client-side defenses operate under a *forgery model*: attacker cost is set by market prices (proxies, human labor, GPU compute, malware infections), not by a security parameter. Bulk fraudulent-account merchants price CAPTCHA and verification costs into their product [44].

### 2.5 Related Work

*Bot detection.* Honeysite and deployment studies characterise bot fingerprints [45, 46]. Commercial anti-bot services stop basic scripted bots on most sites but are bypassed on up to 82% of them by automating less common real browsers [47]; fingerprint-based crawler blocking misses bots that alter a few attributes [48]. Picasso attests device class via canvas rendering [11]. These works mostly target Environmental Forgery; none measures what an attacker that leaves the browser untouched still pays.

*CAPTCHA breaking.* reCAPTCHA's image challenges and checkbox risk analysis fell [49], and Searles et al. [50] compare human and bot performance at scale.

*Computer-use agents.* Benchmarks [14, 51–53] track agents acting on real web and desktop environments. Attacks on these agents [54, 55] are potential defender tools against Operator Synthesis.

*Authenticating good bots.* IETF Web Bot Auth lets well-behaved agents opt in to cryptographic identification [56, 57].

*Comparative evaluation.* Our tiered evaluation follows Bonneau et al.'s benefit matrix [58].

| Work | Coverage | Threat model | Evaluation | Claims challenged |
|------|----------|--------------|------------|-------------------|
| Laperdrix et al. [3] | Browser fingerprinting: attributes, uses, defences | Tracker/fingerprinter versus user privacy; bot detection is one application | Literature survey | None directly; we treat fingerprint-based detection as one layer (L1a) that Operator Synthesis sidesteps |
| Guerar et al. [16] | 20 years of CAPTCHA designs and attacks | ML solvers and human farms against CAPTCHA challenges | Literature survey and taxonomy | That CAPTCHA hardness sets the bar: we argue the challenge is no longer the binding cost |
| Rokicki et al. [59] | JavaScript timers and timing attacks in browsers | Microarchitectural and side-channel attacks from web content | SoK with experimental timer analysis | None; we build on it for L4 chronometric checks |
| Searles et al. [50] | Modern CAPTCHAs in live deployment | Human users and automated solvers | User study (1,400 participants, 14,000 CAPTCHAs solved) and bot comparison | We extend its bot-versus-human finding from solvers to full-browser VLM agents |
| Bonneau et al. [58] | Password-replacement schemes | Authentication attacks | Benefit matrix: 35 schemes rated on 25 usability, deployability and security benefits | Not challenged; we reuse its comparative-matrix method |
| This SoK | Client-side anti-automation Types I–V, 2010–2026 | APB with Operator Synthesis (Axis C) as the primary lens | Mechanism matrix, tier assignment, structured cost accounting | The design assumption of Types I–III (§3.2) that automation runs inside or instruments the browser |

Table: Comparison with the closest surveys and SoKs.

---

## 3. PART I: Probabilistic Client-Side Attestation (2010–2024)

### 3.1 Literature Search

The original search is not PRISMA-replicable, and one team member classified the §3.2–§3.4 corpus. The logged rerun below was double-screened by two LLMs; no human screened it.

**Sources.** IEEE Xplore, ACM Digital Library, arXiv, Google Scholar, IETF Datatracker, W3C Technical Reports. The original pass (before May 2026, when the earliest committed draft already describes it) kept no log, so on 23 September 2026 we re-ran the main query on the two sources with a scriptable API: arXiv (74 hits) and Semantic Scholar (443 hits). DBLP's bot challenge blocked scripted clients. This gives 517 records and 444 unique titles, logged in `docs/corpus.csv` with their script (`analysis/literature_search.py`). Two LLM screeners from different vendors (glm-5.3-flash, mistral-small-4; temperature 0, blind to each other) screened all 444 titles and abstracts (110 on title alone) against the criteria below: Cohen's κ = 0.79, raw agreement 0.90. A third reader (Claude) adjudicated the 46 disagreements; one title-only exclusion of a cited paper was corrected on full text. 195 records were included, 7 of them already cited ([26, 27, 49, 60–63]). Both models then coded the includes into our taxonomy (κ = 0.76; 14 adjudicated): 162 CAPTCHA designs or solvers, 8 Type II, 8 Type III, 3 Type I, 3 Type IV, 2 Type V, 7 economics, and 2 web-agent capability studies. None needed a new class, but the main query mostly retrieves CAPTCHA work; the Type I–V literature came from supplementary queries and snowballing. The 188 new includes are coded at Type level from abstracts only (`docs/corpus.csv`, `analysis/screen_corpus.py`).

**Query.** `("bot mitigation" OR "bot detection" OR "anti-automation" OR "browser fingerprinting" OR CAPTCHA) AND (attestation OR cost OR economics OR architecture OR "CAPTCHA solving" OR "vision-language model" OR VLM OR "web agent" OR "computer-use agent" OR "GUI agent")`. Supplementary queries covered PATs, Privacy Pass, DBSC, behavioural biometrics, deobfuscation, and proxy and pay-per-install economics, then backward and forward snowballing.

**Inclusion and exclusion.** An item enters the *coded corpus* (classified into Types I–V and L1–L4) if it documents a client-side mechanism that imposes cost on automated clients, in peer-reviewed work, an IETF/W3C document, or grey literature corroborated by a second independent source. Production deployment is normally required; undeployed proposals (PACT [9, 38]) are included and marked as proposals because they define Type IV's direction. We exclude unevaluated theoretical proposals, server-side-only defences (WAFs, TLS fingerprinting), and marketing without mechanism detail.

**Coded corpus versus background.** Other references are background: economics framing, historical works, protocol RFCs, and agent/VLM papers characterising the Part II attacker. The original pass and snowballing were not logged, so we give no PRISMA-style numbers beyond the rerun counts above.

**Post-hoc additions and grey literature.** Snowballing and announcements added recent work (agentic web navigation, SDK-based residential proxies, PACT, 2025–2026 VLM CAPTCHA-solving measurements) and a selection bias toward work the authors knew. Single-vendor claims are flagged.

### 3.2 Five Architectural Types by Mechanism

We classify by primary mechanism: Execution (probing the runtime), Telemetry (passive behavioral/sensor data), or Cryptographic Binding (hardware-anchored proof). Production systems fuse them (§3.3).

| System | Execution | Telemetry | Cryptographic Binding | Primary Mechanism |
|--------|-----------|-----------|----------------------|-------------------|
| Google Botguard | ✓ [11] | ✓ —† | | Execution (collects L1b sensor telemetry) |
| Turnstile | ✓ [19] | ✓ [19] | | Execution |
| reCAPTCHA v3 | ✓ —† | ✓ —† | | Telemetry (with Execution auxiliary) |
| DataDome | | ✓ [64] | | Telemetry |
| Arkose Labs | ✓ —† | ✓ —† | | Telemetry |
| Apple PATs | | | ✓ [1] | Cryptographic Binding |
| Privacy Pass | | | ✓ [4, 35] | Cryptographic Binding (redemption only; the 2018 deployment used a solved CAPTCHA as the issuance attester [35]) |
| DBSC | | | ✓ [24, 25] | Cryptographic Binding |
| Passkeys/WebAuthn | | | ✓ [34] | Cryptographic Binding |

Table: Mechanism matrix. "—†" = no public mechanism-level source; empty = undocumented, not absent (authors' assessment).

**Type I: Point-in-Time VM Attestation.** A custom JavaScript VM probes the environment (L1–L4, §3.4) and yields a short-lived opaque token the server verifies with the vendor. Cost: per-execution proxy bandwidth, fixed RE, and RE per compile rotation. The ceiling is IP reputation market exhaustion under both paradigms (§3.4). Examples: Google Botguard, Cloudflare Turnstile Managed Challenge, Kasada [65].

**Type II: Stateful Behavioral Telemetry.** Persistent-identifier profiles score interaction cadence over weeks to months. Cost: proxy, aged profile and anti-detect license [66, 67]; the ceiling is profile-aging latency. Operator Synthesis removes only the need to forge behaviour *within* an aged profile. Examples: reCAPTCHA v3, DataDome, Human Security (PerimeterX).

**Type III: Behavioral Biometrics & Sensor Telemetry.** Measures mouse kinematics, click timing, touch pressure and accelerometer data [20, 68–72]. Cost under Environmental Forgery: `min(Cost_ML_Inference, Cost_Human_Labor)`, with CAPTCHA-solving farms at ∼$1/1K challenges [60] setting the floor. VLMs output coordinates, not trajectories (§1.4), so naive interpolation leaves L1b leverage (Tier 2, §4.2).

**Type IV: Platform/OS-Level Anonymous Attestation (Privacy Pass / PATs / PACT).** Anonymous tokens from a platform or third-party issuer. With a hardware anchor (Secure Enclave/TPM, per-device rate limits [8]), key extraction is prohibitive but proxying through PPI-compromised devices is viable [73, 74]. With a contextual anchor such as account standing (PACT [9, 38]), the Sybil problem moves from device scarcity to credential scarcity (§4.2–4.3). The hardware variant is Tier 1 because cost moves to real enrolled devices, not because it resists VLMs. Examples: Apple PATs, Cloudflare/Fastly Privacy Pass issuance, PACT (proposed).

**Type V: Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys).** DBSC binds a session cookie to a non-exportable device key [24, 25] and counters cookie theft, not automation. Cost: real enrolled devices or accounts, e.g. PPI-compromised hosts at $30–$200/month per botnet subscription [74]. Inapplicable to anonymous traffic [12]. Examples: Google DBSC, W3C WebAuthn, Passkeys.

### 3.3 Hybrid Production Systems

Turnstile's VM delivers telemetry to a behavioral scoring engine (Types I and II) [19], DataDome fuses Type II profiles with Type III biometrics [64], and Arkose Labs escalates to visual challenges when Type II/III scoring is inconclusive. We classify each by its *binding structural ceiling*, the constraint that limits adversary throughput; for Turnstile, IP reputation (Execution).

### 3.4 The L1–L4 Diagnostic Framework

L1–L4 is this paper's analytical model, synthesised from public sources (Path B): Google publishes no Botguard specification, and we did not reverse-engineer it. Our sources are Google's Picasso protocol [11]; Sivakorn et al.'s black-box study of reCAPTCHA [63]; grey-literature (GL) write-ups of the Botguard VM [75–78], which are single-author, unreviewed, version-specific and partly contradictory; and the fingerprinting, timer and obfuscation literature [3, 10, 59, 79]. It models point-in-time VM attestation, not one vendor's implementation.

- **L1a (Static Environmental Introspection).** Documented: reCAPTCHA renders a fixed canvas composition and compares the result against the declared User-Agent, escalating to a harder challenge on mismatch [63]; Picasso generalises this into server-seeded device-class challenges [11]. The Search-interstitial VM contains no plaintext fingerprint property names [76], so coverage varies by deployment. We hypothesize that containerised deployment at scale leaks anomalies (missing fonts, inconsistent WebGL), moving cost to container evasion (§4.1).
- **L1b (Dynamic Sensor Telemetry).** Documented: the VM reads real input events [76]. Kinematic scoring is claimed [77], but Sivakorn et al. found mouse timing and movement did not affect the risk score [63]; we treat it as inferred [20, 71]. We hypothesize that naive interpolation of VLM coordinates leaves detectable artifacts (§1.4).
- **L2 (Code Obfuscation, Polymorphism).** Documented: a custom bytecode VM with encrypted registers and runtime-loaded self-modifying opcodes [75], per-load keystream-encrypted bytecode [76], and a script URL and token-cipher constant that change each rotation [77]. BgUtils runs the VM as a black box [78], and a VLM never inspects bytecode: T_RE ≈ 0 at the VM level; application-level workflow RE remains (§5.5).
- **L3 (Execution Traps).** Documented: an "anti-logger" that patches getters so `console.log` or logpoints perturb VM state [75], and a `Function.prototype.toString` anti-hook probe [76]. Under OpSyn nothing is hooked, so the traps never fire. We hypothesize a perceptual *cognitive honeypot*: a decoy with non-zero `getBoundingClientRect()` size and `opacity: 0.01` in a `pointer-events: none` overlay that DOM-grounded agents such as SeeAct [80] may select, as in hidden-element attacks [54, 55]. It is narrow: screenshot-only agents (e.g. CogAgent [81]) never see it, `aria-hidden` hides it from accessibility-tree agents, and DOM-versus-screenshot cross-checks defeat it.
- **L4 (Chronometric Integrity).** Documented: the VM compares `performance.now()` and `Date.now()` to detect breakpoints and folds the result into the seed selecting the next bytecode byte, silently diverting execution under debugging [75]; `performance.now` also appears in the interstitial's signal set [76]. A second-scale extension of L4 (Section 5.2) needs slow inference: at 5–15 s per action an agent flow accumulates latency a human does not, but two small VLMs measured 0.77–1.45 s median per call (Section 5.7). What remains is regularity, not magnitude, and we claim no fixed ratio.

| Layer | Claimed mechanism | Public source(s) | Claim strength |
|-------|-------------------|------------------|----------------|
| L1a | Canvas render vs. declared UA consistency | Sivakorn et al. BH Asia 2016 [63]; Picasso [11] | Documented (reCAPTCHA, 2016) |
| L1a | Broad `navigator`/WebGL fingerprinting in the VM | [3] (general); contradicted for Search interstitial by GL [76] | Inferred; deployment-dependent |
| L1a | Container anomalies under OpSyn | — | Hypothesized |
| L1b | Real input-event collection | GL [76] | Documented (GL) |
| L1b | Mouse-kinematic scoring | GL claim [77]; null result [63]; [20, 71] (general) | Inferred; contested |
| L1b | Interpolation artifacts in VLM orchestration | — | Hypothesized |
| L2 | Custom bytecode VM, encrypted registers, self-modifying opcodes | GL [75, 76] | Documented (GL) |
| L2 | Script/cipher rotation | GL [77] | Documented (GL, one version) |
| L2 | VM executable as black box | GL [78] | Documented (GL) |
| L3 | Anti-logger, `toString` anti-hook probe | GL [75, 76] | Documented (GL) |
| L3 | Cognitive honeypot vs. DOM-grounded agents | [54, 55, 80] (agent attacks) | Hypothesized |
| L4 | Timing-based anti-debug feeding the VM seed | GL [75] | Documented (GL) |
| L4 | Second-scale inference-latency signal | Section 5.2 | Hypothesized; refuted for small VLMs (§5.7) |

Table: Evidence grading for L1–L4. Documented = observed for a Google product; inferred = general or contested sources; hypothesized = ours, unvalidated. GL = grey literature.

| Layer | Cost Type (EF) | Cost Under OpSyn | Nature of Shift |
|-------|----------------|---------------|-----------------|
| L1a | Variable (compute for forgery) | Shifted to container-evasion engineering | Not zero; moved from browser forgery to deployment-environment mimicry |
| L1b | Variable (ML inference or labor) | Shifted to kinematic-smoothing orchestration | Not zero; moved from trajectory generation to orchestration-layer quality assurance |
| L2 | Temporal (RE per compile rotation) | Near-zero at VM level; shifted to app-level workflow RE | VM bytecode black-boxed; DOM-level prompt engineering remains |
| L3 | Mixed (trap identification + overhead) | Shifted to perceptual-DOM alignment | Not zero; moved from DevTools-trap evasion to perceptual-DOM alignment engineering (Section 4.2) |
| L4 | Variable (timer synchronization) | Shifted to latency-evasion at inference timescale | Microsecond instrumentation gap closed; second-scale gap only for slow models (§5.7) |

Table: Cost-type shift per L1–L4 layer. EF = Environmental Forgery; OpSyn = Operator Synthesis.

### 3.5 The Temporal Arms Race

Point-in-time VMs rely on a race between the defender's rotation lifetime `T_Life` and the attacker's per-build reverse-engineering time `T_RE`. For Botguard, grey literature reports a hand-built token generator valid for only one bytecode sample [75, 77]; the rotation interval is not public. Automated deobfuscation [10, 82–84] and learned code models [85, 86] lowered `T_RE`, and hardening such as Loki [79] responded; that `T_RE` was approaching `T_Life` is our inference, not a measurement. Under Operator Synthesis the VM runs as a black box [78], so software-only obfuscation imposes no VM-level cost (L2 above).

---

## 4. PART II: The VLM/Operator Synthesis Attack Vector

*Part II (Sections 4–6) analyzes Operator Synthesis under the APB threat model and sets a research agenda for VLM-resilient anti-automation.*

### 4.1 Axis C as the New Baseline: What Operator Synthesis Changes

At scale, deployment constraints partially re-open detection surfaces.

| Assumption | Environmental Forgery | Operator Synthesis (Idealized) | Operator Synthesis (At Scale) |
|---|---|---|---|
| Browser state | Instrumented / modified | Stock, legitimate | Stock browser, but orchestration surfaces exposed |
| DOM integrity | Compromised | Intact | Intact |
| Sensor data | Forged | Ground truth | Ground truth for browser APIs; containerization leaks at OS/network layers |
| Execution timing | Affected by instrumentation | Native | Native at JS runtime level; VLM inference latency adds second-scale delays |
| Input modality | Programmatic API calls | OS-level GUI synthesis | OS-level GUI synthesis through an orchestration layer (PyAutoGUI, accessibility APIs) |
| Motor control | Separate GAN/trajectory generator | Emergent from VLM training | Emergent VLM selection, instantiated through orchestration layer that may introduce detectable kinematic artifacts |

Table: Idealized Operator Synthesis assumptions versus industrial-scale constraints.

**The containerization gap.** A stock Chrome browser in a Linux container, the cheapest way to run VLM operators at scale, still leaks fonts inconsistent with the declared OS, WebGL artifacts inconsistent with the expected GPU driver stack [87], and characteristic AudioContext output. L1a environmental introspection therefore retains leverage against containers. Driving real consumer devices closes the gap at the price of hardware acquisition and lower density per operator. The gap is a cost lever, not a detection guarantee.

OS-level input synthesis predates VLMs (xdotool, PyAutoGUI). The VLM adds perception and cross-site generalisation without per-site scripting. Operator Synthesis removes the instrumentation forgery cost paid by anti-detect-browser adversaries (§1.3), but not the IP-reputation cost (§5.3).

**The hybrid attacker.** A rational operator scripts deterministic steps and invokes the VLM only for perception, still injecting OS-level input into an unmodified browser. This keeps the Axis C properties at lower inference cost. Section 5 cost figures assuming per-action VLM inference are upper bounds for this attacker.

### 4.2 Architecture-by-Architecture Effects of Operator Synthesis

We place each type in one of three tiers by how much pre-VLM defense cost survives Operator Synthesis. Tier 1 mechanisms are indifferent to input modality, so cost moves entirely to acquiring real enrolled devices or accounts. Tier 2 keeps a residual client-observable surface. Tier 3 replaces the original constraint with a substitute cost the attacker can buy. Tiers do not measure total defense strength (Section 4.3).

**Type I (Point-in-Time VM Attestation) → Tier 2.** The forgery costs of L1–L4 largely cease. IP reputation remains the dominant constraint, and container artifacts (Section 4.1) impose a residual cost whose net effect is open (Section 5.3). The VM becomes a delivery mechanism rather than a defense.

**Type II (Stateful Behavioral Telemetry) → Tier 3.** A VLM does not create profile aging. It can operate purchased aged profiles, accounts or real long-lived devices without the instrumentation that previously betrayed them, so aging becomes a market price rather than a wait. Isolating aged state across thousands of parallel VLM instances is an orchestration cost that substitutes for the anti-detect browser license.

**Type III (Behavioral Biometrics & Sensor Telemetry) → Tier 2.** The VLM does not produce the trajectory between coordinates; an orchestration layer does (Section 1.4). L1b retains leverage only against poor orchestration: our straightness rule flagged every pointer jump but no textbook minimum-jerk path (§5.7), so closing the gap costs little against naive detectors; learned detectors are untested.

**Type IV (Anonymous Attestation / PATs) → Tier 1, hardware-anchored variant only.** The attestation binds to an enrolled device and account, not to input modality. A VLM operating a real attested device (e.g., an iPhone in a device farm driven through screen capture and OS-level input) obtains valid tokens. Tier 1 is therefore not VLM resilience. Cost moves to device and account acquisition, and per-device throughput is bounded by attester rate limits [8]. Key extraction is a separate, costlier chain [74]. Software-anchored variants do not qualify: PACT [9] binds attestation to issuer judgment of account standing, so the unit of scarcity becomes the credentialed account (Sections 4.3, 6.4). PACT treats the browser as a trusted user-agent [38], and its draft threat model lets attackers "control a number of Clients" [88], e.g. a copied or compromised profile.

**Type V (Hardware-Anchored Determinism / DBSC, passkeys) → Tier 1.** Proof of possession of a hardware-bound key is independent of input modality, so a VLM driving the enrolled device passes. DBSC counters cookie theft, not automation. Passkeys authenticate an account holder, not a human operator.

| Tier | Definition | Types | Mechanism |
|------|------------|-------|-----------------------|
| 1 | Input-modality-independent; cost moves to real enrolled devices/accounts | Type IV (PATs, hardware-anchored) [1, 8], Type V (DBSC/Passkeys) [24, 34] | A VLM driving a real enrolled device passes (binding is to the key, not the input modality [1, 24, 34]). Attacker cost = device/account acquisition (device farms) —†; throughput bounded by attester rate limits [8]. Key extraction is a separate chain (Section 4.3) [73, 74]. |
| 2 | Degraded — cost-shifted but not eliminated | Type I (VM Attestation), Type III (Behavioral Biometrics) | Detection premise substantially weakened at the cognitive level [26, 27, 62]; residual costs from container-evasion artifacts (Type I) —† or kinematic-orchestration quality (Type III) [21, 68, 69] remain |
| 3 | Substituted — original constraint met by a purchasable substitute | Type II (Stateful Telemetry) | Aging still required but bought (aged profiles, accounts, real devices) rather than waited out [44, 67]; state-orchestration infrastructure cost —† replaces the anti-detect browser license [66, 67] |

Table: Tier assignment under Operator Synthesis. Bracketed numbers source each cell claim; "—†" marks the authors' assessment. The tier placements are the authors' synthesis.

![Where the attacker's marginal cost lands, by defense type (rows) and attacker class (columns). The figure summarises §3.2 and §4.2 and is the authors' assessment, not a measurement; "device farm" drives real enrolled devices (§4.3, §5.6). Generated by `analysis/figure_cost_shift.py`.](figures/cost_shift.pdf){width=100%}

### 4.3 What Survives: Tier 1 Architectures and Their Limits

**PATs (Type IV): the real-device ceiling.** The cheapest bypass needs no compromise. The attacker drives real enrolled devices in a device farm, or relays challenges to genuine devices. Cost per token is acquisition amortised over the tokens each device obtains under the attester's per-device rate limits [8]. For the costlier device-compromise route, pay-per-install (PPI) services sold installs at $7–$180 per 1,000 (2011 Windows prices) [73]. No comparable public prices exist for PAT-capable Apple devices (§5.6).

SDK-based residential proxy networks (Bright Data, the former Hola network) are not a PAT bypass. They relay traffic through consenting users' devices [89] and supply IP reputation (§5.3), not attestation.

Farmed or relayed attestations are valid and indistinguishable at the attestation layer. The defender's recourse is server-side metadata: ASN reputation, IP-to-account cardinality, velocity limits and cross-session patterns.

**The software-anchor ceiling: token farming.** PACT-style anchors replace the device-compromise ceiling with an account-acquisition ceiling (§6.4). Bulk registration, credential stuffing and cheap subscriptions feed token farming, as designers expect [90]. The cryptographic layer prevents only certain linkability [4], not polluted tokens, so verifier-side rate limiting remains necessary for any anchor [91].

**DBSC/Passkeys (Type V): the session ceiling.** Malware or a VLM operating the key-holding device inherits the bound session. Tarrach et al. [92] found message-integrity gaps reachable by browser extensions. Kuchhal et al. [93] found only 4.4% of authenticators carry Level 2+ malware resistance certification. The limit is the key-storage environment, not the protocol.

**The universal ceiling.** Device and account markets, the malware supply chain [74], OS mitigations and user security posture, not protocol design, set the cost of controlling a real enrolled device.

### 4.4 Why PATs Are Not a Silver Bullet

PATs plus DBSC do not solve anti-automation, for three reasons.

**1. PATs require platform coordination.** RFC 9576 [4] separates the *attester* and *issuer* roles so that, absent collusion, the party that learns the client's identity does not learn which origin requested the token. For deployed PATs, Apple is the only attester and Cloudflare and Fastly are issuers, so this privacy property comes with a deployment dependency: origins cannot obtain attestation for clients whose platform vendor runs no attester, and we found no deployed PAT attester for Android or Windows.

**2. PATs shift the trust problem.** The defender must trust the attester's device and account checks and the issuer's policy over probabilistic detection. That is an economic and political judgment, not a technical guarantee. The attester is a single vendor whose incentives may diverge from the origin's.

**3. PATs create a two-tier accessibility surface.** PAT-only anti-automation effectively requires an Apple device (iOS 16+/macOS Ventura+). Android and most desktop users fall back to other challenges, which shifts friction onto users without Apple devices.

**The software-anchor response.** PACT [9] opens issuance: "Any entity or organization may provide credentials" [91]. This addresses reason 1 only by multiplying security-critical parties. It worsens reason 2: each Moderator picks its Anchors, with no accreditation or audit regime (§6.4) [88, 94]. Reason 3 stays open: its designers ask how "anyone in the world can get a useable anchor" [94].

---

## 5. A Structured Cost-Accounting Exercise for VLM-Driven Attacks (Part II)

*Our equations are accounting identities (quantity × price), not predictive models; they apply the forgery-model framing of §2.4.*

*Terminology.* "LLM tokens" are billed by an inference API. "Clearance tokens" are issued by a defensive VM or challenge on success (e.g. a Botguard response or challenge-clearance cookie).

**Table 5.1 — Cost parameters.** *Verified* = checked against the cited price page on 2026-09-23; *assumption* = illustrative.

| Parameter | Value used | Status |
|---|---|---|
| Frontier VLM input price `p_in` | $1.25–$5.00 per M LLM tokens | verified: $1.25 (GPT-5 [95], Gemini 2.5 CU [96]), $3.00 (Sonnet 4.6 [97]); upper end assumption |
| Frontier VLM output price `p_out` | $5.00–$20.00 per M LLM tokens | verified: $10 (GPT-5, Gemini 2.5 CU), $15 (Sonnet 4.6); range ends assumption |
| LLM tokens per action | ∼1,000 in / ∼500 out | assumption; measured 1,269–1,586 in / 24–142 out per call (§5.7) |
| Actions per clearance token `n` | 5–10 | assumption; pure VLM needed 11–18 calls (§5.7) |
| Per-attempt success `P` | 0.4–0.7 | assumption, informed by [6, 14, 26] |
| Residential proxy, commodity | ∼$2.50–$8/GB | verified: list $5–$8/GB, $2.50 under a 3-month promotion [98] |
| Residential proxy, premium / dedicated | ∼$10–$50/GB | assumption |
| VLM latency per perception–action step | 5–15 s | assumption (consistent with [99]); small VLMs measured 0.77–1.45 s median per call (§5.7) |
| Scripted-step latency | 0.5 s | assumption; xdotool measured 0.47 s median (§5.7) |

### 5.1 VLM Inference Cost Under Operator Synthesis

For any attack that must perceive rendered content, VLM inference adds to the Environmental Forgery cost stack (§5.3) rather than replacing it. The per-task inference cost is:

```text
C_inference = Σ_{i=1..n} (t_in,i × p_in + t_out,i × p_out)
```

with `t_in,i` / `t_out,i` the LLM tokens at step `i` and prices from Table 5.1.

**Per-attempt cost.** At Table 5.1 values one action costs $0.00125–$0.005 + $0.0025–$0.01 = **$0.00375–$0.015**, and 10 actions cost $0.0375–$0.15. These are frontier-price scenarios. Measured small-VLM calls used more input (1,269–1,586) but far less output (24–142 LLM tokens) than assumed (§5.7); re-sending prior screenshots would make cost roughly quadratic in `n`.

**Hybrid attackers** call the VLM only on the fraction `f` of steps needing perception or recovery and script the rest:

```text
C_inference,hybrid ≈ f × C_inference + (1 − f) × n × c_script
```

where `c_script` ≈ 0. At `f` = 0.2 the per-attempt cost falls five-fold, so the pure-VLM figures are an upper bound.

**Sensitivity.** Table 5.2 sweeps `f` and `P(success)` for a 10-step flow at Sonnet 4.6 prices [97], a frontier-model scenario; the small models of §5.7 cost 7×–320× less per success. "Accumulated" context re-sends every prior screenshot; "none" prunes history. Latency assumes 10 s per VLM step and 0.5 s per scripted step (`analysis/cost_model.py`).

| `f` | Context | Cost/attempt | Cost/success, P=0.4 | Cost/success, P=0.7 | Cost/success, P=0.9 | Latency/attempt |
|---|---|---|---|---|---|---|
| 0.1 | none | $0.010 | $0.026 | $0.015 | $0.012 | 14 s |
| 0.1 | accumulated | $0.010 | $0.026 | $0.015 | $0.012 | 14 s |
| 0.3 | none | $0.032 | $0.079 | $0.045 | $0.035 | 34 s |
| 0.3 | accumulated | $0.041 | $0.101 | $0.058 | $0.045 | 34 s |
| 0.5 | none | $0.052 | $0.131 | $0.075 | $0.058 | 52 s |
| 0.5 | accumulated | $0.083 | $0.206 | $0.118 | $0.092 | 52 s |
| 1.0 | none | $0.105 | $0.262 | $0.150 | $0.117 | 100 s |
| 1.0 | accumulated | $0.240 | $0.600 | $0.343 | $0.267 | 100 s |

Table: Table 5.2 — Hybrid-attacker sensitivity (illustrative; parameters in Table 5.1).

`f` moves cost per success (≈$0.01 to $0.60) more than `P(success)` does: `f` = 0.1 at `P` = 0.4 is cheaper than pure VLM at `P` = 0.9. Context accumulation matters only at `f` ≥ 0.5. At `f` ≤ 0.3 an attempt takes 14–34 s, inside the human range for a multi-step form; at the measured 1–2 s per call every row would be.

**Failure rates.** With independent per-attempt success `P(success)`, the expected cost per clearance token is:

```text
C_effective = C / P(success),   where C = C_inference + C_replan
```

`C_replan` counts only the extra re-planning LLM tokens, since `1/P(success)` already counts the retry. The multiplier is 1.67× at `P(success)` = 0.6 [6, 14, 26] and 2.5× at 0.4. With `C` = $0.05, `P(success)` = 0.4 gives $0.05/0.4 = $0.125 per clearance token and 0.7 gives $0.05/0.7 ≈ $0.071, a change of ≈ 43%. Defenses that raise perceptual ambiguity (dynamic layouts, canvas rendering, adversarial-noise overlays) should therefore raise `C_effective`.

### 5.2 The Latency Cost

Table 5.1 assumes 5–15 s per perception–action cycle, or 25–150 seconds per attempt over 5–10 actions. We found no public per-step figure for commercial computer-use models; OSWorld-Human attributes 75–94% of agent latency to planning and reflection calls [99].

1. **Chronometric heuristics (L4).** Without instrumentation, L4 sees only per-action latency, and VLM session duration overlaps the human range (passive VM challenges take equal time for both). At the measured 1–2 s per action (§5.7), VLM latency differs from human latency only in regularity. As a hard rule, timing flags slow, distracted, and assistive-technology users, and attackers can add random delays.

2. **Session timeout risk.** Challenge windows typically last 1–5 minutes, and a 10-step flow at 15 s per step takes 150 s, but measured small-VLM flows took 26–44 s (§5.7). Timeouts therefore bind only on slow, reasoning-heavy models.

Timeouts enter through `P(success)`, not a separate term:

```text
C_temporal = (C_inference + C_replan + C_bandwidth_per_attempt) / P(success)
```

where `P(success)` includes `(1 − P(timeout))` as a factor.

### 5.3 The Proxy Supply Market

Operator Synthesis still needs residential IPs from a tiered supply [89]. Commodity shared IPs cost ∼$2.50–$8/GB [98], and their reputation is a commons [61]. Sticky sessions cover a 25–150 s flow. Reputation pushes demand upward: a slow session exposes each exit IP longer, and a burned IP costs a whole multi-step attempt.

**Conjunctive cost model.** Driving a stock browser drops the anti-detect license of prior models (`Cost_proxy + Cost_aged_profile + Cost_software_license`) but adds state orchestration:

```text
Cost_bypass_OS = Cost_residential_proxy + Cost_session_isolation + Cost_VLM_inference
```

`Cost_session_isolation` covers per-session browser containers, storage persistence, and profile rotation. Net savings are plausibly positive, but no public pricing permits a direct comparison (§7.1).

### 5.4 Human Labor as a Cost Reference

Under Environmental Forgery, CAPTCHA farms [60] and click-farm labor [100] set the global cost floor. Human labor and VLM inference are substitutes, so the attacker pays `min(C_VLM, C_human)`. Solving services charge roughly $0.50–$2.00 per 1,000 solves [60], i.e. $0.0005–$0.002 each, below one VLM action at frontier prices (§5.1). Yet the cheaper measured model completed a whole five-field flow for €0.0010–€0.0019 per success (§5.7), the price of one human solve at these (2010) rates; the other model cost 7–27× more. Labor is therefore no longer a floor below VLM inference for simple flows, though a fair comparison needs current solver prices for equal-scope flows. VLM list prices fell repeatedly in 2023–2026 (GPT-5 launched at half GPT-4o's input price [95]). The VLM changes scaling, not substitutability: labor scales with headcount, VLM throughput with API quota.

### 5.5 The Temporal Arms Race: T_RE ≈ 0 at the VM Level

Under Environmental Forgery, compile rotation and attacker RE form a race (§3.5):

```text
T_RE < T_Life → defense is structurally bypassed
T_RE > T_Life → defense imposes recurring cost
```

Under Operator Synthesis, `T_RE ≈ 0` for the VM bytecode, which the attacker never reverse-engineers. A per-target workflow cost remains (goal, success criterion, error recovery, DOM work for the scripted fraction `1 − f`); it is small relative to VM RE but scales with the number of workflows. VM obfuscation and compile rotation therefore do not constrain this attacker. Randomised selectors raise only scripted cost; visual and sequential variation lowers the VLM's `P(success)` or raises `f`.

### 5.6 Tier 1 Under a Device Farm: Cost per Clearance Token

Tier 1 (Types IV and V, §4.2) is indifferent to input modality, so the attacker must acquire real enrolled devices, bounded by attester rate limits (§4.3). For PATs:

```text
C_token = (D / L + O) / (R × 30)
```

where `D` is the device price, `L` the amortisation period in months, `O` farm operations (mobile proxy or SIM, power, management) per device-month, and `R` the clearance tokens per device per origin per day (a per-origin limit needs the rate-limited issuance extension [8]; under a per-issuer limit `R` is shared across origins). Account cost would add to `D`.

**Parameters.** `D` = $100–$300 spans Swappa asking prices for used PAT-capable iPhones (iPhone XR from $103; SE 2nd gen $105, iPhone 11 $188, iPhone 13 $286 on average, July–August 2026 [101]); `L` = 12–24 months is an assumption. `O` = $9.30–$48.80 comes from an anti-detect vendor's 10-device phone-farm breakdown [102] (vendor-reported, Android-oriented, unverified). Owned-device cost is therefore $13.47–$73.80 per device-month. A rented AWS EC2 `mac2.metal` host lists at $0.65/hour with a 24-hour minimum [103], i.e. $468 per month; whether PAT issuance works on it is unverified. Apple does not publish `R`, and the issuance design [8] leaves it to the issuer, so we sweep it.

| Rate limit (tokens/device/origin/day) | Owned used iPhone, low | Owned used iPhone, high | Rented cloud Mac |
|---|---|---|---|
| 1 | $0.449 | $2.46 | $15.60 |
| 10 | $0.045 | $0.246 | $1.56 |
| 100 | $0.0045 | $0.025 | $0.156 |
| 1000 | $0.0004 | $0.0025 | $0.016 |

Table: Table 5.3 — Tier 1 (PAT) cost per clearance token vs. per-device rate limit (`analysis/cost_model.py`).

At `R` = 1 a farmed token costs $0.45–$2.46, above most Table 5.2 costs per success and far above the measured small-VLM costs (§5.7). At `R` ≥ 100 it drops below one cent, comparable to CAPTCHA-farm labor (§5.4). A strict limit also caps legitimate high-frequency users.

**Alternative acquisition paths.** Pay-per-install cost $7–$180 per 1,000 installs, i.e. $0.007–$0.18 per install [73], at 2011 Windows prices; PAT-capable Apple installs are likely far dearer. Where the issuer admits on account standing (PACT-style anchors, §6.4), bulk fraudulent accounts sold for $10–$200 per 1,000, i.e. $0.01–$0.20 per account [44] (Twitter, 2012–13). In every path the ceiling is a market price divided by an issuer-controlled rate limit.

### 5.7 Measured Costs on a Self-Hosted Testbed

We ran our self-hosted harness (artifact `measurement/`) against a localhost testbed of five pages, each with one text field, a "Continue" button, and a transparent decoy over it. The decoy is the L3 cognitive honeypot (§3.4): selection by element reference (JavaScript or CDP `click()`) fires it, while a click at screen coordinates reaches the real button. Configurations: (a) Playwright over CDP, selecting by DOM reference (`a-dom`) or accessibility role (`a-role`); (b) scripted xdotool input into stock Chromium without CDP; (c) a pure VLM agent that sees a 1280×800 screenshot and acts through xdotool; (d) a hybrid that uses the VLM only on unrecognised pages, starting with a Turnstile interstitial (always-pass test key), and hands back to (b) once the form appears. Models came from Melious [104] at EUR list prices. A grounding probe (click the real "Continue" in 25 screenshots) scored `glm-5.3-flash`, `qwen3.8-27b`, and `kimi-k2.7-code` 25/25 each, at 0.71 s, 1.72 s, and 3.09 s median; we ran the two fastest, and the larger kimi-k3 on part of the unseen-form test. Each stateless call sends one screenshot, the goal, and the last 12 actions, at temperature 0. Each configuration and model ran 10 times on 23 September 2026 (€0.2779 total LLM spend).

| Config | Model | Pass | Honeypot hit | `navigator.webdriver` | Action p50 / p90 (s) | Run p50 (s) |
|---|---|---|---|---|---|---|
| a-dom | – | 10/10 | 10/10 | 10/10 | 0.07 / 0.11 | 1.3 |
| a-role | – | 10/10 | 0/10 | 10/10 | 0.11 / 0.14 | 1.4 |
| b-xdotool | – | 10/10 | 0/10 | 0/10 | 0.47 / 1.89 | 7.0 |
| c-vlm | glm-5.3-flash | 10/10 | 0/10 | 0/10 | 1.40 / 1.89 | 26.3 |
| c-vlm | qwen3.8-27b | 10/10 | 0/10 | 0/10 | 1.57 / 2.54 | 44.1 |
| d-hybrid | glm-5.3-flash | 10/10 | 0/10 | 0/10 | 0.49 / 2.01 | 15.0 |
| d-hybrid | qwen3.8-27b | 9/10 | 0/10 | 0/10 | 1.83 / 3.09 | 42.7 |

Table: Table 5.4 — Detection signals and timing (N = 10 each). Pass = server-side completion; `navigator.webdriver` = runs whose page script reported the flag; action latency excludes browser launch.

| Config | Model | VLM calls/run | VLM call p50 / p90 (s) | LLM tokens in / out per call | Cost per success |
|---|---|---|---|---|---|
| c-vlm | glm-5.3-flash | 11 | 0.77 / 1.34 | 1,586 / 24 | €0.0019 |
| c-vlm | qwen3.8-27b | 18 | 1.45 / 2.09 | 1,336 / 95 | €0.0136 |
| d-hybrid | glm-5.3-flash | 3.5 | 1.01 / 1.82 | 1,549 / 115 | €0.0010 |
| d-hybrid | qwen3.8-27b | 13 | 1.66 / 3.70 | 1,269 / 142 | €0.0125 |

Table: Table 5.5 — VLM cost (median calls per run; cost per success = spend ÷ successes, list prices [104]).

**Detection signals follow the injection point.** The honeypot fired in 10/10 DOM-reference runs and 0/10 accessibility-role runs, because the decoy is hidden from the accessibility tree. None of the 50 OS-input runs fired it or set `navigator.webdriver`, which all 20 Playwright runs set. Both signals separate CDP automation from OS-level input and say nothing about whether a VLM is driving (Axis C, §4.1). By construction, the honeypot result confirms only the L3 mechanism, not a failure of any deployed system.

**Latency.** Median VLM call latency was 0.77–1.45 s, far below the assumed 5–15 s. The faster model's per-action latency was regular (p50 1.40 s, p90 1.89 s; §5.2) but at 1–2 s it is in the range of human per-field times; we have no human data for this flow. Pure-agent runs took 26.3–44.1 s (median) against 7.0 s scripted, inside the 1–5 minute challenge windows of §5.2. The 5–15 s assumption, and the L4 and timeout arguments built on it, therefore do not hold for fast small models. Frontier models that reason at length remain unmeasured.

**Tokens and cost.** Input was 1,269–1,586 LLM tokens per call (assumed ∼1,000). Output was 24–142 (assumed ∼500), because the prompt asks for one JSON action. The pure agent needed 11–18 calls (median; assumed 5–10) because it clicks, types, and submits separately. Cost per success was €0.0019–€0.0136, 7× to 320× below the pure-VLM row of Table 5.2 ($0.117–$0.600) at any EUR/USD rate between 1.0 and 1.2. Per-token prices and the stateless prompt explain the gap, not fewer steps.

**Hybrid hand-back is model-dependent.** With `glm-5.3-flash` the hybrid cut VLM calls from 11 to 3.5 per run, cost per success from €0.0019 to €0.0010, and run time from 26.3 s to 15.0 s, resuming scripted control in 9/10 runs. `qwen3.8-27b` never handed back (0/10): it ignored the instruction to stop at the first form page, so its hybrid row is a pure-VLM run plus an interstitial. One of its runs stalled on the first form page. The low-`f` region of Table 5.2 thus assumes a hand-off the attacker must engineer and verify per model.

**What the VLM adds: unseen forms.** Nine unseen variants keep the answers and the honeypot but change labels (incl. German), ids, fields, button placement, or input widgets, singly and combined. They test whether perception replaces per-site scripting. Agents scripted for the base form passed 4–6 of 18 variant runs, failing wherever a selector, role name, or key sequence stopped matching. The unchanged VLM agent passed 17/18 with glm-5.3-flash (one run submitted wrong answers) and 6/6 with the larger kimi-k3 (Table 5.6). Scripted failures are by construction, which is the point: each new site costs a scripter engineering time and a VLM only inference.

| Agent | Base form | Variants v1–v9 | Cost per success |
|---|---|---|---|
| Scripted, DOM selectors (a-dom) | 2/2 | 4/18 | – |
| Scripted, accessibility role (a-role) | 2/2 | 4/18 | – |
| Scripted, xdotool keyboard (b) | 2/2 | 6/18 | – |
| VLM agent, glm-5.3-flash (c) | 2/2 | 17/18 | €0.0028 |
| VLM agent, kimi-k3 (c) | – | 6/6 | €0.1348 |

Table: Table 5.6 — Passes on the base form and nine unseen variants (N = 2 per cell; kimi-k3 one run on six variants). Pass = flow completed with every answer correct.

**What detects it: kinematics, not the VLM.** We logged pointer events on every page and fitted a transparent rule (bot if path straightness > 0.9925) on public human mouse data [105] against synthetic straight or teleport moves. The rule reached 93.2% held-out accuracy and flagged 9% of human moves. It flagged every pointer movement of the scripted and VLM agents, which jump the pointer through xdotool, and none of a textbook minimum-jerk path (Table 5.7). Type III scoring therefore detects how the pointer is driven, not whether a VLM chose the target, and a generic smoothing step defeats this naive rule. Stronger kinematic models remain untested.

| Movement source | Movements | Flagged as bot |
|---|---|---|
| Balabit humans, held-out users | 19,136 | 9% |
| Synthetic straight or teleport moves | 19,136 | 95% |
| Playwright CDP click (a-role) | 42 | 100% |
| Scripted xdotool pointer jumps (b) | 98 | 100% |
| VLM agent, glm-5.3-flash (c) | 154 | 100% |
| VLM agent, kimi-k3 (c) | 59 | 100% |
| Smoothed min-jerk OS input (e) | 100 | 0% |

Table: Table 5.7 — Point-to-click movements flagged by the straightness rule.

**Limits.** The flows are synthetic forms on localhost, with small N, three open-weights models from one provider, and list prices; Experiments A and B cost €0.87. Vendor test keys always pass, so no vendor detection was measured. The human mouse data are remote-desktop traces resampled to 50 Hz, not browser traces from our testbed, and the variants are our own. There is no human baseline (no ethics approval for a user study), so we claim no human–VLM latency separation. Raw logs, the grounding probe, and `measurement/analyze.py` are in the artifact; its `--check-paper` mode checks every row of Tables 5.4–5.7 against the logs.

---

## 6. Industry Trajectory and Attestation Centralization (Part II)

Industry work over 2024–2026 advanced along three tracks: DBSC, passkeys, and anonymous attestation (Privacy Pass, Apple PATs, proposed PACT). DBSC and passkeys address authenticated-session threats, not anonymous automation. Anonymous attestation bears on the Anonymous Authentication Gap but relies on a small set of attesters and issuers. We argue that this reliance turns the gap into an Attestation Market Centralization problem (§6.3), which PACT extends rather than resolves (§6.4).

### 6.1 DBSC and the Session-Hijacking Threat Model

DBSC [24, 25, 106] is a Google/Chrome-led protocol that binds session cookies to a non-exportable key held in a TPM (or equivalent secure hardware). No vendor attestation server is involved. Non-exportability protects the key only after registration: malware present during session registration may be able to extract it, although Chrome rates such attacks as considerably harder and more detectable [106]. DBSC targets session hijacking (NIST 800-63 Authenticated/ATO quadrant [12]). It is an anti-cookie-theft mechanism, not an anti-automation mechanism, and says nothing about whether a fresh anonymous session is driven by a human or a VLM.

For the infostealer economy [73, 74, 107, 108], DBSC changes what stolen material is worth. Exfiltrated cookies expire quickly once replayed off-device, so the attacker must keep malware resident and use the key on the infected machine. The economic ceiling moves from the price of a stolen cookie log to the price of persistent on-device access (botnet rental and residency). That ceiling is higher and scales with compromised devices, not stolen logs.

### 6.2 Passkeys and the Credential-Phishing Threat Model

Passkeys (FIDO2/WebAuthn [34]) bind credentials to the relying party's origin, which defeats credential phishing for the passkey itself. Deployments that keep phishable fallback factors remain exposed to real-time phishing by downgrade [109]. Most consumer deployments use the attestation conveyance "none", so the relying party learns that a credential exists, not what hardware holds it. Centralization sits in the synchronization fabric (Apple iCloud Keychain, Google Password Manager, Microsoft), not in a per-authentication root of trust. Only 4.4% of authenticators carry Level 2+ certification offering malware resistance [93]. Browser extensions can reach message-integrity gaps [92], and timing side channels in authenticator behavior [110] erode the assumption of unobservable key operations.

### 6.3 The Attestation Market Centralization Problem

Against Operator Synthesis, the defenses that still impose cost on anonymous traffic are hardware-anchored anonymous tokens, which depend on a few parties that vouch for devices. None of them distinguishes a human from a VLM driving a real device. They move the attacker's cost to acquiring real, enrolled devices and bound throughput by attester rate limits. The question is who controls that vouching.

**Where trust concentrates.** We use RFC 9576 roles [4]: the *Attester* vouches for the client, the *Issuer* signs the token, the *Origin* redeems it.

- **Apple PATs:** Apple is the Attester, using device attestation on iOS 16+ and macOS Ventura+ [1]. Third-party Issuers such as Cloudflare and Fastly sign RSA blind-signature tokens. Apple's attester "can also perform rate-limiting" [1] but publishes no per-device limits. Concentration is in the attester role.
- **Private State Tokens:** a Chrome API [23] in which *registered third-party issuers* (not Google) issue VOPRF-based tokens. Google's October 2025 Privacy Sandbox update retired most Sandbox APIs but stated that Private State Tokens will be maintained [111]. Concentration is in the browser vendor's issuer registration.
- **PACT** [9]: adds no hardware root; it concentrates the judgement of which parties may vouch that a person is present (§6.4).

**The centralization–anonymity–bot-resistance tension.** Constructions such as [7, 8] make issuance unlinkable and rate-limited but do not analyze market structure. Consider three goals: (i) redemptions unlinkable to identities, (ii) bounded per-client token supply, and (iii) no small set of trusted parties. A scheme meeting (i) and (ii) must rate-limit on something the issuer can count without identifying the user. In deployed systems, that is a device key attested by a platform vendor or an account held with a large first party. Goal (ii) therefore pulls toward attesters that already hold a large, Sybil-resistant population, and deployed systems have relaxed (iii). This is not an impossibility result: threshold issuance, zero-knowledge proofs of personhood, and decentralized issuer networks are feasible in principle. The open question is whether any can reach a Sybil-resistant population at platform-vendor scale, and what pricing power, exclusion risk, and lock-in follow if none can.

**The ad-tech context.** Browser vendors that run ad platforms shape both stateful identifiers and the attestation APIs that replace them. Chrome announced in 2024 and confirmed in 2025 that it will not deprecate third-party cookies [111], so pressure on Type II state comes mainly from Safari ITP, Firefox Total Cookie Protection, and regulation (§7.4).

### 6.4 PACT: Software Anchors and Issuer Judgment

On June 22, 2026, Cloudflare announced **Private Access Control Tokens (PACT)** with Mozilla, Google, Microsoft, and Shopify: a protocol, to be standardized, that lets "sites with strong knowledge of 'personhood'" issue anonymous tokens the browser presents to other sites [9]. PACT builds on Privacy Pass (RFC 9576 [4]), with W3C Anti-Fraud Community Group design work since December 2025 [112]. It is a proposal with no deployment timeline, specified in an individual, Informational IETF draft (MoLE) [39, 88].

**The software-anchor turn.** PACT breaks with the hardware anchor behind Type IV's Tier 1 classification (§4.2), where Apple PATs anchor the Attester's knowledge in device posture [1]. PACT accepts *software or contextual anchors*: "a subscription, an account in good standing, or a verified phone number" [39]. This relocates the Sybil problem: the attacker's unit of scarcity becomes a credentialed account. Bulk registration, credential stuffing, stolen session tokens, and cheap subscriptions are automatable inputs to token farming [88, 90]. The browser acts as trusted user-agent, mediating credential storage, issuer selection, challenge budgets, and token conversion [38]. Under Operator Synthesis it is not a trust anchor: an operator may control the profile, the device, or both. Redemption hides which Anchor endorsed the client [39, 88]. That is the privacy property, and its price is that a Moderator cannot tell a strong Anchor from a weak one, so a token is worth only its issuer's admission process.

**The issuer-judgment problem.** Each site nominates one Moderator, which picks the Anchors it trusts [39, 88]. Shared Moderators carry "a centralisation risk" [39]; [9] pitches "PACT on Cloudflare's network". Rudis argues that as adoption spreads, a missing token carries information, so tokens become mandatory without anyone deciding it; traffic with no issuer relationship (scanners, archival crawlers, RSS readers, Tor users) becomes suspect [113]. The designers intend a fallback to today's challenges [39]. The draft has no Anchor accreditation or audit; Anchor feedback is a "TODO" [88]. Access starts "at the strength of the weakest" Anchor [39], and until Anchor governance is specified PACT inherits that posture [88]. A token proves only that *some* trusted Anchor vouched, not that a personhood check occurred. Account-standing anchors favor lasting platform relationships, and "a paid subscription costs an attacker the same as a real user" [39]. PACT targets agentic traffic [9]; agents may use the user's Credential, and the user agent must tell them apart [88].

---

## 7. Open Problems and Future Research

### 7.1 Closing the Empirical Gap in VLM Attack Economics

VLM agents solve production CAPTCHAs [26], and VLM-aware benchmarks [62] and training pipelines [27] exist. Missing are industrial-scale measurements of throughput, session continuity across proxy pools, and proxy market elasticity.

Our §5.7 harness is a first step; next are real vendor keys registered for localhost where terms allow, kinematically realistic input, a consented human baseline, and frontier computer-use models.

### 7.2 VLM-Resilient Attestation Primitives

Tier 1 is modality-indifferent (§4.2) but carries the dependencies of §6.

- **Decentralized anonymous attestation:** zero-knowledge proofs of personhood, threshold or distributed-VOPRF issuer networks, and hardware-backed attestation without OS-vendor dependency. For PACT, Anchor-hiding, which grew out of aggregating-issuer and IssuerHide designs [38, 114], is now a draft goal [88], but openness rests on per-Moderator Anchor choice, not distributed issuance.
- **Physical-presence challenges:** liveness detection or ambient sensor fusion that a VLM in a virtual machine cannot satisfy. The countermeasure is incentivized proxying: SDK-based proxy networks (§4.3) pay the device owner in in-app rewards to satisfy the challenge. This adds latency and reward cost, so such challenges need threat modeling against human relay.
- **Cross-modal consistency:** checking that camera, microphone, touchscreen, and accelerometer data fit one physical environment, which a VLM in a VM cannot easily fake.

### 7.3 Standardized Benchmarking ("Bot-Bench")

Evaluations under Operator Synthesis rely on grey-hat reverse engineering or small PoCs that compile rotation invalidates; a vendor-neutral harness with known human/VLM ground truth is needed. BehavePassDB [115] is a partial template but ignores VLM interaction patterns. MCA-Bench [62] is VLM-aware but covers only CAPTCHAs.

Such a benchmark must also measure false positives. L4 latency profiles, kinematics, and typing cadence differ for users of screen readers, switch access, voice control, eye-tracking, and other assistive technologies, and for older or motor-impaired users. Tighter thresholds against VLM-driven input shift cost onto these users as challenge escalation or lock-out. That cost is rarely reported and should be a first-class metric.

### 7.4 The Security–Privacy Trade-off in Stateful Mitigation

Type II needs persistent client state, which privacy law and browser tracking prevention constrain. Appendix D analyses the EU legal framework (ePrivacy Art. 5(3), GDPR Art. 6(1)(f), DMA Art. 6(7)) and separates legal limits from browser-imposed technical limits.

---

## 8. Conclusion

Under the APB threat model, three insights follow.

1. **Detection follows where input enters, not who chooses it.** On our testbed, in-runtime and kinematic signals separated CDP automation from OS-level input, and scripted from smoothed pointer paths, but never VLM from script; what the VLM added was passing unseen forms without per-site scripts (§5.7). Against top-tier attackers, probabilistic defenses therefore lose their premise and cost shifts to orchestration (§3.4, §4.2).
2. **Hardware anchors move cost; they do not end the contest.** Tier 1 is indifferent to input modality. Its ceiling is the price of real enrolled devices or accounts divided by an issuer-controlled rate limit (§5.6).
3. **The open problem is who controls web trust.** Attestation narrows the Anonymous Authentication Gap by concentrating trust in a few attesters and issuers (§6.3–§6.4); decentralized alternatives remain open.

---

## References

**[1]** Apple Inc. "Replace CAPTCHAs with Private Access Tokens." *WWDC22 Session*, June 8, 2022. URL: https://developer.apple.com/videos/play/wwdc2022/10077/.

**[2]** Human Security, Inc. (formerly PerimeterX). "The Economics of Bot Mitigation." *Industry Whitepaper*, 2022.

**[3]** P. Laperdrix, N. Bielova, B. Baudry, and G. Avoine. "Browser Fingerprinting: A Survey." *ACM Trans. Web*, Vol. 14, No. 2, Article 8, pp. 1–33, 2020. DOI: 10.1145/3386040.

**[4]** A. Davidson, J. Iyengar, and C. A. Wood. "The Privacy Pass Architecture." *RFC 9576*, IETF, June 2024. DOI: 10.17487/RFC9576.

**[5]** OpenAI. "Computer-Using Agent." OpenAI blog, January 23, 2025. URL: https://openai.com/index/computer-using-agent/.

**[6]** H. He, W. Yao, K. Ma, W. Yu, Y. Dai, H. Zhang, D. Cai, and D. S. Weld. "WebVoyager: Building an End-to-End Web Agent with Multimodal Models." In *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2024.

**[7]** B. Kreuter, T. Lepoint, M. Orrù, and M. Raykova. "Anonymous Tokens with Private Metadata Bit." In *Advances in Cryptology — CRYPTO 2020*, pp. 308–336. Springer, 2020. DOI: 10.1007/978-3-030-56784-2_11.

**[8]** H. Chu, K. Do, S. Faller, and L. Hanzlik. "On the Security of Rate-limited Privacy Pass." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2023. ePrint: 2023/1805.

**[9]** Cloudflare, Inc. "Cloudflare Collaborates With Leading Browsers to Develop a Privacy-First Protocol for the Global Internet." Press release, June 22, 2026. URL: https://www.cloudflare.com/press/press-releases/2026/cloudflare-collaborates-with-leading-browsers-to-develop-a-privacy-first-protocol-for-the-global-internet/.

**[10]** S. Schrittwieser, S. Katzenbeisser, J. Kinder, G. Merzdovnik, and E. Weippl. "Protecting Software through Obfuscation: Can It Keep Pace with Progress in Code Analysis?" *ACM Comput. Surv.*, Vol. 49, No. 1, Article 4, pp. 1–37, 2016. DOI: 10.1145/2886012.

**[11]** E. Bursztein, A. Malyshev, T. Pietraszek, and K. Thomas. "Picasso: Lightweight Device Class Fingerprinting for Web Clients." In *Proc. 6th Workshop on Security and Privacy in Smartphones and Mobile Devices (SPSM '16)*, pp. 93–102. ACM, 2016. DOI: 10.1145/2994459.2994467.

**[12]** P. A. Grassi et al. "Digital Identity Guidelines." *NIST Special Publication 800-63-3*, 2017.

**[13]** OWASP Foundation. "Automated Threat Handbook." *OWASP Project*, 2018–2024. URL: https://owasp.org/www-project-automated-threats-to-web-applications/.

**[14]** X. Deng, Y. Gu, B. Zheng, S. Chen, S. Stevens, B. Wang, H. Sun, and Y. Su. "Mind2Web: Towards a Generalist Agent for the Web." In *Proc. Conference on Neural Information Processing Systems (NeurIPS)*, 2023.

**[15]** E. Bursztein, M. Martin, and J. C. Mitchell. "Text-based CAPTCHA Strengths and Weaknesses." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 125–138, 2011. DOI: 10.1145/2046707.2046724.

**[16]** M. Guerar, L. Verderame, M. Migliardi, F. Palmieri, and A. Merlo. "Gotta CAPTCHA 'Em All: A Survey of 20 Years of the Human-or-Computer Dilemma." *ACM Comput. Surv.*, Vol. 54, No. 9, Article 192, pp. 1–33, 2021. DOI: 10.1145/3477142.

**[17]** I. J. Goodfellow, Y. Bulatov, J. Ibarz, S. Arnoud, and V. Shet. "Multi-digit Number Recognition from Street View Imagery using Deep Convolutional Neural Networks." In *Proc. International Conference on Learning Representations (ICLR)*, 2014. arXiv:1312.6082.

**[18]** V. Shet. "Are You a Robot? Introducing 'No CAPTCHA reCAPTCHA'." *Google Security Blog*, December 3, 2014. URL: https://security.googleblog.com/2014/12/are-you-robot-introducing-no-captcha.html.

**[19]** Cloudflare, Inc. "Bot Management Technical Documentation." *Cloudflare Docs*, 2023–2024.

**[20]** A. Acien, A. Morales, J. Fierrez, R. Vera-Rodriguez, and O. Delgado-Mohatar. "BeCAPTCHA: Behavioral Bot Detection using Touchscreen and Mobile Sensors benchmarked on HuMIdb." *Engineering Applications of Artificial Intelligence*, Vol. 98, 104058, 2021. DOI: 10.1016/j.engappai.2020.104058.

**[21]** A. Acien, A. Morales, J. Fierrez, and R. Vera-Rodriguez. "BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection." *Pattern Recognition*, Vol. 127, 108643, 2022. DOI: 10.1016/j.patcog.2022.108643.

**[22]** H. Fereidooni et al. "AuthentiSense: A Scalable Behavioral Biometrics Authentication Scheme using Few-Shot Learning for Mobile Platforms." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.23194.

**[23]** WICG. "Private State Token API." *WICG Community Group Draft*. URL: https://wicg.github.io/trust-token-api/.

**[24]** D. Rubery and K. Monsen, Eds. "Device Bound Session Credentials (DBSC)." *W3C Web Application Security Working Group / WICG*, 2024. URL: https://w3c.github.io/webappsec-dbsc/.

**[25]** Google Chrome Security Team. "Fighting Cookie Theft Using Device Bound Sessions." *Chromium Blog*, 2 April 2024. URL: https://blog.google/chromium/fighting-cookie-theft-using-device/.

**[26]** X. Teoh, Y. Lin, S. Li, R. Liu, A. Sollomoni, Y. Harel, and J. S. Dong. "Are CAPTCHAs Still Bot-hard? Generalized Visual CAPTCHA Solving with Agentic Vision Language Model." In *Proc. USENIX Security Symposium*, 2025. URL: https://www.usenix.org/conference/usenixsecurity25/presentation/teoh.

**[27]** Y. Chen, H. Zhai, C. Wang, R. Yang, L. Zhang, G. Wang, et al. "CAPTCHA Solving for Native GUI Agents: Automated Reasoning-Action Data Generation and Self-Corrective Training." arXiv:2603.23559, 2026. URL: https://arxiv.org/abs/2603.23559.

**[28]** A. Gómez-Boix, P. Laperdrix, and B. Baudry. "Hiding in the Crowd: An Analysis of the Effectiveness of Browser Fingerprinting at Large Scale." In *Proc. The Web Conference (WWW)*, pp. 309–318, 2018. DOI: 10.1145/3178876.3186097.

**[29]** S. Wu, P. Sun, Y. Zhao, and Y. Cao. "Him of Many Faces: Characterizing Billion-scale Adversarial and Benign Browser Fingerprints on Commercial Websites." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.24394.

**[30]** N. Andriamilanto, T. Allard, G. Le Guelvouit, and A. Garel. "A Large-scale Empirical Analysis of Browser Fingerprints Properties for Web Authentication." *ACM Trans. Web*, Vol. 16, No. 1, Article 1, pp. 1–62, 2022. DOI: 10.1145/3478026.

**[31]** Z. Liu, P. Shrestha, and N. Saxena. "Gummy Browsers: Targeted Browser Spoofing against State-of-the-Art Fingerprinting Techniques." In *Proc. International Conference on Applied Cryptography and Network Security (ACNS)*, June 2022. arXiv: 2110.10129.

**[32]** J. H. Saltzer and M. D. Schroeder. "The Protection of Information in Computer Systems." *Proc. IEEE*, Vol. 63, No. 9, pp. 1278–1308, 1975.

**[33]** X. Lin, P. Ilia, S. Solanki, and J. Polakis. "Phish in Sheep's Clothing: Exploring the Authentication Pitfalls of Browser Fingerprinting." In *Proc. USENIX Security Symposium*, 2022.

**[34]** J. Hodges, J.C. Jones, M.B. Jones, A. Kumar, and E. Lundberg, Eds. "Web Authentication: An API for Accessing Public Key Credentials, Level 2." *W3C Recommendation*, 8 April 2021. URL: https://www.w3.org/TR/2021/REC-webauthn-2-20210408/.

**[35]** A. Davidson, I. Goldberg, N. Sullivan, G. Tankersley, and F. Valsorda. "Privacy Pass: Bypassing Internet Challenges Anonymously." *Proc. on Privacy Enhancing Technologies (PoPETs)*, Vol. 2018, No. 3, pp. 164–180, 2018. DOI: 10.1515/popets-2018-0026.

**[36]** T. Pauly, S. Valdez, and C. A. Wood. "The Privacy Pass HTTP Authentication Scheme." *RFC 9577*, IETF, June 2024. DOI: 10.17487/RFC9577.

**[37]** S. Celi, A. Davidson, S. Valdez, and C. A. Wood. "Privacy Pass Issuance Protocols." *RFC 9578*, IETF, June 2024. DOI: 10.17487/RFC9578.

**[38]** antifraudcg/pact. "Design Proposal for PACT via ACTs with Aggregating Issuers." GitHub Issue #6, March 30, 2026. URL: https://github.com/antifraudcg/pact/issues/6

**[39]** D. Jackson. "PACT: Anonymous Credentials for the Web." *Mozilla Hacks*, June 23, 2026. URL: https://hacks.mozilla.org/2026/06/pact-anonymous-credentials-for-the-web/. Accessed September 24, 2026.

**[40]** R. Anderson and T. Moore. "The Economics of Information Security." *Science*, Vol. 314, No. 5799, pp. 610–613, 2006. DOI: 10.1126/science.1130992.

**[41]** T. Moore. "The Economics of Cybersecurity: Principles and Policy Options." *Int. J. Crit. Infrastruct. Prot.*, Vol. 3, No. 3, pp. 103–117, 2010. DOI: 10.1016/j.ijcip.2010.10.002.

**[42]** R. Anderson et al. "Measuring the Cost of Cybercrime." In R. Böhme (Ed.), *The Economics of Information Security and Privacy*, pp. 265–300. Springer, 2013. DOI: 10.1007/978-3-642-39498-0_12.

**[43]** C. Herley and D. Florêncio. "Nobody Sells Gold for the Price of Silver: Dishonesty, Uncertainty and the Underground Economy." In *Proc. Workshop on the Economics of Information Security (WEIS)*, June 2009. Published in T. Moore, D. Pym, and C. Ioannidis (Eds.), *Economics of Information Security and Privacy*, pp. 33–53. Springer, 2010. DOI: 10.1007/978-1-4419-6967-5_3.

**[44]** K. Thomas, D. McCoy, C. Grier, A. Kolcz, and V. Paxson. "Trafficking Fraudulent Accounts: The Role of the Underground Market in Twitter Spam and Abuse." In *Proc. USENIX Security Symposium*, 2013.

**[45]** X. Li, B. A. Azad, A. Rahmati, and N. Nikiforakis. "Good Bot, Bad Bot: Characterizing Automated Browsing Activity." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00079.

**[46]** H. Jonker, B. Krumnow, and G. Vlot. "Fingerprint Surface-Based Detection of Web Bot Detectors." In *Proc. ESORICS*, LNCS Vol. 11736, 2019. DOI: 10.1007/978-3-030-29962-0_28.

**[47]** B. A. Azad, O. Starov, P. Laperdrix, and N. Nikiforakis. "Web Runner 2049: Evaluating Third-Party Anti-bot Services." In *Proc. DIMVA*, LNCS Vol. 12223, 2020. DOI: 10.1007/978-3-030-52683-2_7.

**[48]** A. Vastel, W. Rudametkin, R. Rouvoy, and X. Blanc. "FP-Crawlers: Studying the Resilience of Browser Fingerprinting to Block Crawlers." In *Proc. NDSS Workshop on Measurements, Attacks, and Defenses for the Web (MADWeb)*, 2020. DOI: 10.14722/madweb.2020.23010.

**[49]** S. Sivakorn, I. Polakis, and A. D. Keromytis. "I Am Robot: (Deep) Learning to Break Semantic Image CAPTCHAs." In *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, 2016. DOI: 10.1109/EuroSP.2016.37.

**[50]** A. Searles, Y. Nakatsuka, E. Ozturk, A. Paverd, G. Tsudik, and A. Enkoji. "An Empirical Study & Evaluation of Modern CAPTCHAs." In *Proc. USENIX Security Symposium*, pp. 3081–3097, 2023. URL: https://www.usenix.org/conference/usenixsecurity23/presentation/searles.

**[51]** S. Zhou et al. "WebArena: A Realistic Web Environment for Building Autonomous Agents." In *Proc. International Conference on Learning Representations (ICLR)*, 2024. arXiv:2307.13854.

**[52]** J. Y. Koh et al. "VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks." In *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2024. arXiv:2401.13649.

**[53]** T. Xie et al. "OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments." In *Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track*, 2024. arXiv:2404.07972.

**[54]** Y. Zhang, T. Yu, and D. Yang. "Attacking Vision-Language Computer Agents via Pop-ups." In *Proc. 63rd Annual Meeting of the ACL (Long Papers)*, pp. 8387–8401, 2025. URL: https://aclanthology.org/2025.acl-long.411/.

**[55]** Z. Liao, L. Mo, C. Xu, M. Kang, J. Zhang, C. Xiao, Y. Tian, B. Li, and H. Sun. "EIA: Environmental Injection Attack on Generalist Web Agents for Privacy Leakage." In *Proc. International Conference on Learning Representations (ICLR)*, 2025. arXiv:2409.11295.

**[56]** A. Backman, J. Richer, and M. Sporny. "HTTP Message Signatures." *RFC 9421*, IETF, February 2024. DOI: 10.17487/RFC9421.

**[57]** IETF Web Bot Auth (webbotauth) Working Group. Charter and working documents. URL: https://datatracker.ietf.org/wg/webbotauth/about/.

**[58]** J. Bonneau, C. Herley, P. C. van Oorschot, and F. Stajano. "The Quest to Replace Passwords: A Framework for Comparative Evaluation of Web Authentication Schemes." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, pp. 553–567, 2012. DOI: 10.1109/SP.2012.44.

**[59]** T. Rokicki, C. Maurice, and P. Laperdrix. "SoK: In Search of Lost Time: A Review of JavaScript Timers in Browsers." In *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, 2021. DOI: 10.1109/EuroSP51992.2021.00039.

**[60]** M. Motoyama, K. Levchenko, C. Kanich, D. McCoy, G. M. Voelker, and S. Savage. "Re: CAPTCHAs—Understanding CAPTCHA-Solving Services in an Economic Context." In *Proc. USENIX Security Symposium*, 2010.

**[61]** K. Thomas et al. "Framing Dependencies Introduced by Underground Commoditization." In *Proc. Workshop on the Economics of Information Security (WEIS)*, 2015.

**[62]** Z. Wu, Y. Xue, Y. Feng, X. Wang, and Y. Song. "MCA-Bench: A Multimodal Benchmark for Evaluating CAPTCHA Robustness Against VLM-based Attacks." arXiv:2506.05982, 2025. URL: https://arxiv.org/abs/2506.05982.

**[63]** S. Sivakorn, I. Polakis, and A. D. Keromytis. "I'm Not a Human: Breaking the Google reCAPTCHA." Black Hat Asia, 2016. White paper: https://www.blackhat.com/docs/asia-16/materials/asia-16-Sivakorn-Im-Not-a-Human-Breaking-the-Google-reCAPTCHA-wp.pdf

**[64]** DataDome SAS. "Bot Detection and Mitigation Technical Overview." *Industry Documentation*, 2023.

**[65]** Kasada Pty Ltd. "Polymorphic Security Technical Documentation." *Industry Documentation*, 2023.

**[66]** B. A. Azad, O. Starov, P. Laperdrix, and N. Nikiforakis. "Taming the Shape Shifter: Detecting Anti-fingerprinting Browsers." In *Proc. DIMVA*, 2020.

**[67]** R. van Wegberg, B. Klievink, M. van Eeten, et al. "Plug and Prey? Measuring the Commoditization of Cybercrime via Online Anonymous Markets." In *Proc. USENIX Security Symposium*, pp. 1009–1026, 2018.

**[68]** H. Niu, J. Chen, Z. Zhang, and Z. Cai. "Mouse Dynamics Based Bot Detection Using Sequence Learning." In *Biometric Recognition (CCBR)*, LNCS Vol. 12878, pp. 49–56. Springer, 2021. DOI: 10.1007/978-3-030-86608-2_6.

**[69]** H. Niu, C. Cheng, and Z. Cai. "Learning Human Behavior for Bot Detection: A Perspective on Mouse Movement (MouseAgent)." In *Proc. China Automation Congress (CAC)*, pp. 6575–6580. IEEE, 2023. DOI: 10.1109/CAC59555.2023.10451138.

**[70]** C. Iliou, T. Kostoulas, T. Tsikrika, V. Katos, S. Vrochidis, and I. Kompatsiaris. "Detection of Advanced Web Bots by Combining Web Logs with Mouse Behavioural Biometrics." *Digital Threats: Research and Practice*, Vol. 2, No. 3, Article 24, pp. 1–26. ACM, 2021. DOI: 10.1145/3447815.

**[71]** S. Sadeghpour and N. Vlajic. "ReMouse Dataset: On the Efficacy of Measuring the Similarity of Human-Generated Trajectories for the Detection of Session-Replay Bots." *Journal of Cybersecurity and Privacy*, Vol. 3, No. 1, pp. 95–117. MDPI, 2023. DOI: 10.3390/jcp3010007.

**[72]** D. DeAlcala et al. "BeCAPTCHA-Type: Biometric Keystroke Data Generation for Improved Bot Detection." In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, pp. 1051–1060. IEEE, 2023. DOI: 10.1109/CVPRW59228.2023.00112.

**[73]** J. Caballero, C. Grier, C. Kreibich, and V. Paxson. "Measuring Pay-per-Install: The Commoditization of Malware Distribution." In *Proc. USENIX Security Symposium*, 2011.

**[74]** S. Pastrana, A. Hutchings, D. R. Thomas, and J. Tapiador. "Malware Finances and Operations: A Data-Driven Study of the Value Chain for Infections and Compromised Access." *arXiv:2306.15726*, 2023.

**[75]** dsekz. "botguard-reverse: Botguard full reverse." GitHub repository (write-up README), last commit 15 Sep 2025. https://github.com/dsekz/botguard-reverse  [grey literature]

**[76]** S. Shabat. "BotGuard-RE: Reverse engineering Google's BotGuard interstitial." GitHub repository, accessed 2026-09-23. https://github.com/shlomishabat/BotGuard-RE  [grey literature]

**[77]** Resoneo. "Google BotGuard Analysis / Analyse du système anti-bot de Google." Blog post, 2025 (accessed 2026-09-23). https://think.resoneo.com/botguard-google/  [grey literature, vendor/SEO blog]

**[78]** LuanRT. "BgUtils: Utility to generate PoTokens and run BotGuard attestation challenges." GitHub repository, accessed 2026-09-23. https://github.com/LuanRT/BgUtils  [grey literature]

**[79]** M. Schloegel et al. "Loki: Hardening Code Obfuscation Against Automated Attacks." In *Proc. USENIX Security Symposium*, pp. 3055–3073, 2022.

**[80]** L. Zheng, Z. Wang, D. Fu, Y. Zhang, Y. Lu, B. Dai, D. Song, K. He, and Y. Li. "SeeAct: GPT-4V(ision) is a Generalist Web Agent, if Grounded." In *Proc. International Conference on Machine Learning (ICML)*, 2024.

**[81]** W. Hong, W. Wang, Q. Lv, J. Xu, W. Yu, J. Ji, Y. Wang, Z. Wang, Y. Dong, M. Ding, and J. Tang. "CogAgent: A Visual Language Model for GUI Agents." In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 14281–14290, 2024. DOI: 10.1109/CVPR52733.2024.01354.

**[82]** K. Coogan, G. Lu, and S. Debray. "Deobfuscation of Virtualization-Obfuscated Software: A Semantics-Based Approach." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 275–284, 2011. DOI: 10.1145/2046707.2046739.

**[83]** P. Saxena, D. Akhawe, S. Hanna, F. Mao, S. McCamant, and D. Song. "A Symbolic Execution Framework for JavaScript." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, pp. 513–528, 2010.

**[84]** T. Blazytko, M. Contag, C. Aschermann, and T. Holz. "Syntia: Synthesizing the Semantics of Obfuscated Code." In *Proc. USENIX Security Symposium*, pp. 643–659, 2017.

**[85]** V. Raychev, M. Vechev, and A. Krause. "Predicting Program Properties from 'Big Code'." In *Proc. ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL)*, pp. 111–124, 2015. DOI: 10.1145/2676726.2677009.

**[86]** B. Rozière, M. Lachaux, L. Chanussot, and G. Lample. "DOBF: A Deobfuscation Pre-Training Objective for Programming Languages." In *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. 34, 2021. arXiv: 2102.07492.

**[87]** T. Laor et al. "DRAWNAPART: A Device Identification Technique based on Remote GPU Fingerprinting." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2022. DOI: 10.14722/ndss.2022.24093.

**[88]** S. Schlesinger, D. Jackson, and T. Meunier. "Moderation of unLinkable Endorsements (MoLE) Architecture." *Internet-Draft draft-jms-mole-architecture-00* (individual, Informational; work in progress), IETF, July 6, 2026. URL: https://datatracker.ietf.org/doc/draft-jms-mole-architecture/. Accessed September 24, 2026.

**[89]** X. Mi, X. Feng, X. Liao, B. Liu, X. Wang, F. Qian, Z. Li, S. Alrwais, L. Sun, and Y. Liu. "Resident Evil: Understanding Residential IP Proxy as a Dark Service." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2019. DOI: 10.1109/SP.2019.00011.

**[90]** antifraudcg/pact. "Malicious Bot use of tokens, browser use." GitHub Issue #11, June 25, 2026. URL: https://github.com/antifraudcg/pact/issues/11. Accessed September 24, 2026.

**[91]** D. Jackson, S. Schlesinger, and E. Trouton. "Private Access Control Tokens" (PACT problem statement). W3C Anti-Fraud Community Group, antifraudcg/proposals GitHub Issue #22, December 2, 2025. URL: https://github.com/antifraudcg/proposals/issues/22. Accessed September 24, 2026.

**[92]** T. Tarrach et al. "A Security and Usability Analysis of Local Attacks Against FIDO2." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2024.

**[93]** D. Kuchhal, M. Saad, A. Oest, and F. Li. "Evaluating the Security Posture of Real-World FIDO2 Deployments." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 2381–2395, 2023. DOI: 10.1145/3576915.3623063.

**[94]** antifraudcg/pact. "Fragmentation vs. Centralization of Anchors." GitHub Issue #12, June 25, 2026. URL: https://github.com/antifraudcg/pact/issues/12. Accessed September 24, 2026.

**[95]** OpenAI. "GPT-5" (model page: $1.25 input / $10.00 output per 1M tokens). *OpenAI API Documentation*. URL: https://developers.openai.com/api/docs/models/gpt-5. Accessed September 23, 2026. Archived: https://web.archive.org/web/20260921120808/https://developers.openai.com/api/docs/models/gpt-5.

**[96]** Google. "Gemini Developer API Pricing." URL: https://ai.google.dev/gemini-api/docs/pricing. Accessed September 23, 2026. Archived: https://web.archive.org/web/20260924054733/https://ai.google.dev/gemini-api/docs/pricing.

**[97]** Anthropic. "Pricing." *Claude Platform Docs*. URL: https://platform.claude.com/docs/en/about-claude/pricing. Accessed September 23, 2026. Archived: https://web.archive.org/web/20260923181040/https://platform.claude.com/docs/en/about-claude/pricing.

**[98]** Bright Data. "Residential Proxies Pricing." Archived September 24, 2026: https://web.archive.org/web/20260924054801/https://brightdata.com/pricing/proxy-network/residential-proxies (live page unreachable from our network).

**[99]** R. Abhyankar, Q. Qi, and Y. Zhang. "OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents." arXiv:2506.16042, 2025. URL: https://arxiv.org/abs/2506.16042.

**[100]** M. Motoyama, D. McCoy, K. Levchenko, S. Savage, and G. M. Voelker. "Dirty Jobs: The Role of Freelance Labor in Web Service Abuse." In *Proc. USENIX Security Symposium*, 2011.

**[101]** Swappa. "Used iPhone Prices" (iPhone XR, updated July 8, 2026; price index, updated August 12, 2026; asking prices of active listings). Archived: https://web.archive.org/web/20260708190037/https://swappa.com/prices/apple-iphone-xr and https://web.archive.org/web/20260812144427/https://swappa.com/prices.

**[102]** Multilogin. "Phone Farm Cost vs Cloud Phone Pricing." Vendor blog. https://multilogin.com/blog/phone-farm-cost-vs-cloud-phone-pricing/ (accessed 2026-09-23). Used for: 10-device farm monthly ops $93–$488 (proxy/SIM $5–$30/device/month).

**[103]** Amazon Web Services. "Amazon EC2 Mac Instances." https://aws.amazon.com/ec2/instance-types/mac/ (24-hour minimum allocation); price $0.65/h for mac2.metal via https://instances.vantage.sh/aws/ec2/mac2.metal (accessed 2026-09-23).

**[104]** Melious. "Model hub" (per-model pages for glm-5.3-flash, qwen3.8-27b, kimi-k2.7-code, kimi-k3, and mistral-small-4-119b-instruct with EUR list prices per million tokens). Accessed September 23, 2026. URL: https://melious.ai/hub/models.

**[105]** Á. Fülöp, L. Kovács, T. Kurics, and E. Windhager-Pokol. "Balabit Mouse Dynamics Challenge Data Set." 2016. URL: https://github.com/balabit/Mouse-Dynamics-Challenge.

**[106]** Google Chrome Security Team. "Device Bound Session Credentials (DBSC)." *Chrome for Developers*, 2024. URL: https://developers.chrome.com/docs/web-platform/device-bound-session-credentials.

**[107]** A. Côté Cyr. "Life on a Crooked RedLine: Analyzing the Infamous Infostealer's Backend." *ESET Research / WeLiveSecurity*, November 8, 2024. URL: https://www.welivesecurity.com/en/eset-research/life-crooked-redline-analyzing-infamous-infostealers-backend/.

**[108]** Microsoft Threat Intelligence. "Lumma Stealer: Breaking Down the Delivery Techniques and Capabilities of a Prolific Infostealer." *Microsoft Security Blog*, May 21, 2025. URL: https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/.

**[109]** E. Ulqinaku, H. Assal, A. Abdou, S. Chiasson, and S. Capkun. "Is Real-time Phishing Eliminated with FIDO? Social Engineering Downgrade Attacks against FIDO Protocols." In *Proc. USENIX Security Symposium*, 2021.

**[110]** M. Kepkowski, L. Hanzlik, I. D. Wood, and M. A. Kaafar. "How Not to Handle Keys: Timing Attacks on FIDO Authenticator Privacy." In *Proc. Privacy Enhancing Technologies Symposium (PETS)*, Vol. 2022, No. 4, pp. 705–726, 2022. DOI: 10.56553/popets-2022-0129.

**[111]** A. Chavez. "Update on Plans for Privacy Sandbox Technologies." *Google Privacy Sandbox Blog*, October 17, 2025. URL: https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies.

**[112]** W3C Anti-Fraud Community Group. "antifraudcg/pact" (PACT design repository). GitHub, 2025–2026. URL: https://github.com/antifraudcg/pact.

**[113]** B. Rudis. "PACT: The Open Web Doesn't Need Another Trust Oligopoly." *ai.rud.is*, June 23, 2026. URL: https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/

**[114]** antifraudcg/pact. "Sketching an Architecture That Uses Issuer Blinding." GitHub Issue #1, December 18, 2025. URL: https://github.com/antifraudcg/pact/issues/1

**[115]** G. Stragapede, R. Vera-Rodriguez, R. Tolosana, and A. Morales. "BehavePassDB: Public Database for Mobile Behavioral Biometrics and Benchmark Evaluation." *Pattern Recognition*, 2022. DOI: 10.1016/j.patcog.2022.109089.

**[116]** Directive 2002/58/EC of the European Parliament and of the Council of 12 July 2002 (Directive on privacy and electronic communications), Art. 5(3), as amended by Directive 2009/136/EC. OJ L 201, 31.7.2002, p. 37.

**[117]** European Data Protection Board. "Guidelines 2/2023 on Technical Scope of Art. 5(3) of ePrivacy Directive." Version 2.0, adopted October 7, 2024. URL: https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-22023-technical-scope-art-53-eprivacy-directive_en.

**[118]** Regulation (EU) 2016/679 (General Data Protection Regulation), Art. 6(1)(f) and Recital 49. OJ L 119, 4.5.2016, p. 1.

**[119]** Regulation (EU) 2022/1925 (Digital Markets Act), Art. 6(7). OJ L 265, 12.10.2022, p. 1.

---

## Appendix A: Ethics Considerations

This paper is a systematization based on public sources and analytical reasoning. We performed no live attacks against production services, did not attempt to bypass any deployed anti-automation system, and performed no reverse engineering of Botguard for this paper; the L1–L4 model is our own synthesis from published descriptions and the obfuscation literature. The cost-accounting exercise (§5) is dual-use: a defender can use it to identify where cost is imposed, and an attacker could use it to prioritise effort. We judge the marginal uplift to be low, because every parameter is drawn from public pricing and published research and the analysis contains no target-specific bypass technique. The released harness drives generic form-filling agents only against its own testbed: a guard refuses non-local targets, and the only vendor widget it loads uses a documented test key. Named companies and products are discussed only on the basis of their public documentation, announcements, and peer-reviewed or publicly reported analyses. The measurements in §5.7 ran only against our own testbed bound to localhost, with vendor test keys; the only external service involved was a commercial LLM API used under its ordinary terms, which also received the public titles and abstracts screened in §3.1. No human subjects took part; the human mouse traces are a public research dataset whose authors invite research use, and we do not redistribute them.

## Appendix B: Open Science

We release an anonymized artifact (link given in the submission form; `make artifact` exports it without git history) with: `analysis/params.json` (every §5 parameter with its source and verified/assumption status); `analysis/cost_model.py`, which regenerates every §5 number and asserts that each appears verbatim in the paper; `analysis/figure_cost_shift.py` (the systematization figure); the §3.1 search and screening scripts with all LLM screener outputs and adjudications (`analysis/literature_search.py`, `analysis/screen_corpus.py`, `docs/corpus.csv`, `docs/screening.md`); and the self-hosted measurement harness (`measurement/`) with the raw run and pointer logs, grounding probe, kinematic rule, and analysis script behind Tables 5.4–5.7 (§5.7). The Balabit mouse data [105] are not redistributed; the artifact fetches them from their public repository.

## Appendix C: Use of AI Tools

Generative AI played three roles in this work.

*Object of study (§5.7).* VLM agents are the attacker we measure. We used hosted open-weights models (glm-5.3-flash, MIT license; qwen3.8-27b, Apache-2.0; kimi-k3, custom license, for a larger-model check) through one provider [104]. glm-5.3-flash and qwen3.8-27b were the two fastest of three models that passed a 25-trial grounding probe, because small models are what a cost-minimising attacker would run; kimi-k3 checked whether a larger model changes the unseen-form result. Query volume was bounded by design: N = 10 runs per configuration in Tables 5.4–5.5 and N = 2 per variant in Table 5.6, one screenshot per call, a stateless prompt, and €1.15 of total spend over both measurement rounds. Inference ran on the provider's hardware, which is not disclosed. Hosted models can change without notice, so we release prompts, raw logs, and per-call token counts.

*Methodology (§3.1).* Two LLM screeners (glm-5.3-flash; mistral-small-4, Apache-2.0) screened and coded the literature rerun, and a third model (Claude) adjudicated their disagreements. This took about 1,300 short text calls and €0.12. The criteria, prompts, raw outputs and adjudications are in the artifact. LLM screening can miss relevance that only full text shows, as happened in one corrected case.

*Manuscript and artifact preparation.* An AI coding assistant (Claude) was used to draft and edit text, write the analysis and measurement code, check sources against primary pages, and run mock reviews. The authors inspected all outputs for accuracy and originality, and every number in §5 is regenerated by scripts from logged data.

## Appendix D: Legal Framework for Stateful Mitigation (EU)

Type II needs persistent client state to accumulate profile age, and that state is what privacy law and browser features constrain.

**Legal framework (EU).** *Article 5(3) of the ePrivacy Directive* [116] requires consent for storing or accessing information on terminal equipment, unless *strictly necessary* for a service the user requested. *EDPB Guidelines 2/2023* [117] extend it to script-based collection of device information, bringing fingerprinting and telemetry into scope. Processing personal data also needs a *GDPR* [118] lawful basis, naturally *Art. 6(1)(f)* (legitimate interests) read with *Recital 49*, which names network and information security as a legitimate interest. These obligations bind operators and bot-mitigation vendors. They do not bind browser tracking prevention (Safari ITP, Firefox ETP), which is a product decision.

**Two separate pressures.** Stateful mitigation faces (1) *legal* limits, which leave room for security processing, and (2) *technical* limits imposed unilaterally by browsers, which partition or expire state regardless of purpose and erode profile age even where processing is lawful. The second weakens Type II most, mainly on Safari and Firefox, since Chrome kept third-party cookies (§6.3).

**Competition law.** Where browser and OS vendors both restrict independent state and supply the replacing attestation APIs (§6.3), the *Digital Markets Act* [119] applies. Art. 6(7) obliges the designated gatekeepers Alphabet and Apple to offer free-of-charge, effective interoperability with features accessed or controlled via the operating system, subject to strictly necessary integrity measures. That may extend to OS-level attestation APIs; browser-level APIs and issuer registration may fall outside it. Its application to anti-abuse attestation is open.
