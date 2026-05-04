# SoK: Client-Side Anti-Automation After the VLM — From Probabilistic Forgery to Operator Synthesis

---

**Authors:** Abel, T. K.

**Repository:** https://github.com/tomkabel/google-botguard-security-research

**Keywords:** Client-side attestation, VLM-based automation, operator synthesis, browser fingerprinting, behavioral biometrics, Privacy Pass, Private Access Tokens, device-bound session credentials, anti-automation economics, systematization of knowledge

---

## Abstract

Client-side anti-automation — the set of techniques that distinguish human-driven browsers from automated agents — has evolved through five architecturally distinct paradigms over the past fifteen years, culminating in a landscape where Vision-Language Models (VLMs) and agentic AI systems challenge the foundational assumptions underlying probabilistic client-side defenses for a class of highly-resourced adversaries. This paper presents a Systematization of Knowledge organized as a two-part analysis. **Part I (The Historical Landscape, 2010–2024)** systematizes the five primary architectural paradigms — Point-in-Time VM Attestation, Stateful Behavioral Telemetry, Behavioral Biometrics & Sensor Telemetry, Platform/OS-level Anonymous Attestation, and Hardware-Anchored Determinism — as a retrospective post-mortem. We present the generalized L1–L4 defense-in-depth framework as a *historical diagnostic tool*: a lens that reveals *why* each architectural layer faces structural pressure under Operator Synthesis (the VLM attack vector) rather than as a prescriptive architecture for future defenses. We also provide a historical case study of the temporal arms race between AST obfuscators and symbolic execution engines, which the VLM paradigm renders moot for the APB threat model. **Part II (The VLM/Operator Synthesis Paradigm Shift)** analyzes which architectural properties survive the paradigm shift and which face structural degradation, culminating in an initial cost model for VLM-driven attacks grounded in parametric cost estimates — VLM inference pricing curves, proxy supply elasticity, state-orchestration overhead — while explicitly acknowledging the empirical gaps that prevent precise quantification. Part II also provides a concrete analysis of the attestation market centralization problem, documenting how Apple, Google, and Microsoft's control over Private Access Tokens, Privacy Pass, and Device Bound Session Credentials consolidates the infrastructure of web trust. The paper includes a Grand Taxonomy diagnostic table, a VLM resilience tier ranking, and a forward-looking research agenda for VLM-resilient attestation primitives.

**Contributions:**
1. A two-part SoK structure that resolves the structural dissonance of prior work: Part I as a historical retrospective on probabilistic attestation (2010–2024), Part II as a forward-looking analysis under Operator Synthesis.
2. An L1–L4 defense-in-depth framework reframed as a *historical diagnostic tool* for understanding why probabilistic client-side defenses fail under VLM attack, rather than a prescriptive defensive architecture.
 3. An initial parametric cost model for Operator Synthesis attacks, grounded in VLM inference pricing, proxy market supply elasticity, and state-orchestration overhead, with explicit acknowledgment of the empirical gaps that prevent precise quantification.
 4. A concrete analysis of attestation market centralization — documenting the vendor oligopoly (Apple, Google, Microsoft) on root-of-trust infrastructure — building on prior trilemma formulations with empirically grounded observations about market consolidation.

---

## 1. Introduction

### 1.1 Why the Field Still Needs a Taxonomy — And Why It Must Be a Diagnostic One

Client-side anti-automation has, over fifteen years, produced a rich but terminologically fractured design space. Vendors describe structurally different mechanisms using overlapping vocabulary: "bot detection" may refer to a point-in-time VM executing encrypted bytecode (Google Botguard), a long-term behavioral scoring engine (reCAPTCHA v3), or a hardware-attestation protocol (Apple Private Access Tokens) [24, 44, 62]. "Fingerprinting" can denote passive environmental introspection, active behavioral telemetry, or cryptographic token issuance [6, 38]. This imprecision obstructs comparative analysis and impedes academic research.

Previous efforts to systematize this space have attempted to build unified taxonomies that simultaneously classify all existing defenses and prescribe future directions. This paper argues that such an approach faces a structural challenge because the 2024–2025 emergence of production-capable Vision-Language Models (GPT-4o, Claude Computer Use, Gemini 2.0) and agentic AI frameworks (WebVoyager, CUA, Operator) has introduced a category change in the threat model — "Operator Synthesis" — that bypasses the core detection premise of probabilistic client-side defenses for the APB threat model.

The appropriate response is not to force a unified taxonomy that pretends all paradigms remain viable, nor to abandon systematization entirely. It is to produce a *two-part* systematization: a historical retrospective that documents what was built and why it fails (Part I), and a forward-looking analysis that identifies the surviving architectural properties and the research gaps they expose (Part II).

### 1.2 Contributions and the Two-Part Structure

This paper makes four contributions:

**C1 — A Two-Part SoK Structure (Sections 3 and 4).** We explicitly partition the analysis into a historical retrospective (Part I, Section 3) and a forward-looking analysis under the Operator Synthesis paradigm (Part II, Section 4). This resolves the structural dissonance that arises when a single taxonomy attempts to simultaneously classify active defenses and acknowledge their obsolescence.

**C2 — The L1–L4 Framework as a Historical Diagnostic Tool (Section 3.4).** We generalize the four-layer defense-in-depth framework originally observed in Google's Botguard VM [24] into a vendor-neutral model, and explicitly reframe it as a *historical diagnostic framework* — a lens for understanding *why* VM-based attestation faces structural pressure under Operator Synthesis — rather than as a prescriptive architecture. The temporal arms race analysis (Section 3.5) is presented as a historical case study of a dynamic that the VLM paradigm renders moot at the VM level.

**C3 — An Initial Parametric Cost Model for VLM-Driven Attacks (Section 5).** We provide parametric cost estimates grounded in observable market data: VLM inference pricing curves, proxy market supply elasticity, state-orchestration overhead, and — newly identified in this work — temporal latency costs from VLM inference delay. The conjunctive cost model is extended to account for the VLM attacker's state-isolation requirements. We explicitly acknowledge the empirical gaps that prevent precise quantification and set a research agenda for closing them.

**C4 — Attestation Market Centralization Analysis (Section 6).** Building on the prior "Centralization vs. Anonymity Trilemma" framing from W3C mailing list debates [42, 43], we provide a concrete analysis of the attestation market oligopoly. We document how Apple, Google, and Microsoft's control over PAT issuance, Privacy Pass infrastructure, DBSC key storage, and Passkey synchronization creates a structural dependency that transforms the "Anonymous Authentication Gap" into an economic and political centralization problem.

**Scope.** This SoK covers client-side anti-automation mechanisms deployed in web browsers. Purely server-side defenses (WAF, TLS fingerprinting, DDoS scrubbing, rate limiting) are excluded as they operate under different economic models. The historical retrospective (Part I) covers 2010–2024. The forward-looking analysis (Part II) covers the Operator Synthesis paradigm as it has emerged in 2024–2025 and as it applies to near-future (2026–2028) defense research.

**Scope limitation: the Advanced Persistent Bot threat model.** Throughout this paper, the Operator Synthesis adversary is the *highly-resourced, well-funded* attacker — not the casual scraper. The probabilistic defenses of the 2010–2024 era remain effective against the overwhelming majority of web traffic (basic scraper scripts, `curl`, standard Puppeteer) at a fraction of a cent per request. VLMs invalidate these defenses only for the top tier of motivated adversaries. Our analysis focuses on this Advanced Persistent Bot (APB) threat model, and claims about defense "collapse" should be read through this lens: a defense may be structurally bypassed for an APB while remaining economically viable against commodity adversaries.

### 1.3 Threat Model: A Three-Axis Framework with Axis C as the Primary Lens

We adopt a three-axis threat model, with Axis C elevated from a supplementary dimension to the central analytical lens:

- **Axis A — Authentication State:** Anonymous (no prior identity assertion) vs. Authenticated (identity established through a credential). Anchored on NIST SP 800-63-3 [65].

- **Axis B — Attack Objective:** Resource Exhaustion/Scraping vs. Account Takeover/Fraud. Anchored on OWASP Automated Threat Handbook [66].

- **Axis C — Attack Vector:** Environmental Forgery (subverting the browser runtime, DOM, and JavaScript APIs from within) vs. **Operator Synthesis** (driving a legitimate unmodified browser from the OS input layer via a VLM or agentic AI system). This is the primary axis of analysis for this SoK.

The quadrant mapping for Axes A and B is as follows:

$$
\begin{array}{l|l|l}
 & \textbf{Anonymous} & \textbf{Authenticated} \\ \hline
\textbf{Scraping / Resource Exhaustion} & 
\begin{tabular}{l}
Quadrant I: Point-in-Time VM, \\
Behavioral Biometrics, \\
Compute-Bound Challenges (auxiliary). \\
\text{[66]}
\end{tabular} & 
\begin{tabular}{l}
Quadrant III: \\
Session-bound rate limiting, \\
quota enforcement.
\end{tabular} \\ \hline
\textbf{Account Takeover / Fraud} & 
\begin{tabular}{l}
Quadrant II: Stateful Telemetry \\
\quad (login risk scoring), \\
Platform Anonymous Attestation (PATs). \\
\text{[66]}
\end{tabular} & 
\begin{tabular}{l}
Quadrant IV: Hardware-Anchored \\
\quad Determinism (DBSC, \\
Passkeys, WebAuthn). \\
\text{[65]}
\end{tabular}
\end{array}
$$

Axis C cuts across all four quadrants. Under Environmental Forgery, the attacker instruments the browser runtime to forge sensor data to a defensive VM. Under Operator Synthesis, the attacker drives an unmodified stock browser via OS-level accessibility APIs or GUI automation. The distinction is not a minor implementation detail but a category change: the defender's historical assumption — that the attacker must subvert the browser — no longer holds for the most capable adversary class.

### 1.4 The VLM Paradigm Shift as the Central Framing Device

Vision-Language Models (VLMs) — GPT-4o, Claude Computer Use, Gemini 2.0, and the agentic frameworks built atop them (WebVoyager, CUA, Operator) — introduce a substantively new attack paradigm for the Advanced Persistent Bot (APB) threat model. A VLM operating in a virtual machine environment can "see" the rendered browser via screen capture and "act" through synthesized mouse and keyboard events. Critically:

1. **The browser is legitimate.** The VLM does not need to instrument the DOM, forge `navigator` properties, subvert WebGL rendering, or bypass chronometric traps. It drives an unmodified Chrome, Firefox, or Safari instance exactly as a human would.

2. **The motor control is an emergent property with a critical orchestration dependency.** VLMs are trained on web-scale human demonstrations of computer use. The coordinate outputs, action selections, and timing distributions they generate draw from the same distribution as human operators — they do not require a separately trained GAN for trajectory generation. However, a critical engineering gap exists between VLM output and OS-level input. Frontier VLMs output text, JSON bounding boxes, or structured action specifications; they do not natively generate raw OS-level hardware interrupts, mouse event streams, or keyboard scancodes. An orchestration layer — PyAutoGUI, Puppeteer, Apple accessibility APIs, or a custom agentic wrapper — must translate the VLM's coordinate selection into a concrete kinematic trajectory (e.g., a Bezier curve from the cursor's current position to the target coordinate). If this orchestration layer uses naive linear interpolation, constant-velocity profiles, or generic ease-in/ease-out curves, the resulting mouse kinematics remain statistically distinguishable from human movement, and behavioral biometrics (Type III) retain detection leverage *even when the VLM's cognitive task selection is correct*. The attacker must invest additional engineering effort — a kinematic-smoothing layer, gaze-informed trajectory planning, or hardware-backed input synthesis — to close this gap. Motor control is not a turnkey property of the VLM; it is a property that the attacker must instantiate through a non-trivial orchestration pipeline, and the quality of that instantiation directly determines whether L1b detection remains viable.

3. **The asymmetry is inverted.** In the traditional model, the defender executes code in an environment the attacker owns. Under Operator Synthesis, the attacker's browser environment is *legitimate* from the perspective of the JavaScript runtime. The defender's code executes in an environment that passes the principal integrity checks, because no DOM-level or runtime-level instrumentation has occurred. However, as Sections 4.1 and 5.1 discuss, industrial-scale VLM deployment introduces environmental artifacts at the OS and network layers that a sophisticated defender can still detect.

This paper treats the VLM paradigm shift as the central framing device, not a future concern or a supplementary analysis section. Every architecture evaluated in Part I is assessed through the lens of Operator Synthesis. The resilience tiers established in Section 4 apply consistently across all evaluated paradigms.

---

## 2. Background and Related Work

### 2.1 A Brief History of Client-Side Anti-Automation

The history of client-side anti-automation can be divided into five overlapping eras:

**Pre-2005: Server-Side Heuristics.** Bot detection through IP reputation, request rate analysis, and User-Agent header inspection. No client-side execution.

**2005–2012: The CAPTCHA Era.** Text-distortion, image-recognition, and audio CAPTCHAs tested human perceptual ability [71, 73]. OCR and CNN-based solvers progressively eroded CAPTCHA effectiveness. CAPTCHA-solving farms emerged as economic bypass mechanisms (∼$1 per 1,000 solved CAPTCHAs) [51]. By 2014, Google's systems solved 99.8% of reCAPTCHA challenges [73]. Visual CAPTCHAs remain in production as fallback escalation paths (Arkose Labs, hCaptcha), but ceased to be the standalone frontier of defense.

**2010–2017: The JavaScript Challenge Era.** reCAPTCHA v2's "I'm not a robot" checkbox and Cloudflare's JS challenge pages shifted the defense to testing JavaScript execution capability. Headless browser automation (PhantomJS, Puppeteer, Selenium) rapidly closed this gap.

**2017–2020: VM-Based Attestation.** Custom register-based JavaScript VMs (Google Botguard, Kasada) executing encrypted bytecode defined the next escalation. The adversary must execute the defender's VM faithfully in an environment that looks like a real browser, within strict timing constraints, while the VM continuously mutates its own code [24, 60].

**2020–Present: Diversification and the VLM Paradigm Shift.** Four parallel developments define the present landscape: (a) stateful behavioral telemetry (reCAPTCHA v3, DataDome); (b) behavioral biometrics and sensor telemetry [15, 16, 20]; (c) anonymous attestation protocols (Privacy Pass, PATs) [38, 44, 45]; (d) hardware-anchored session determinism (DBSC) [36, 37]. The 2024 emergence of production VLMs introduced Operator Synthesis as a fifth development that retroactively reclassifies (a) and (b) as structurally bypassed for the APB threat model — a critical scope qualifier that prior discussion has sometimes omitted.

### 2.2 From CAPTCHAs to JavaScript VMs

The transition from CAPTCHAs to VM-based attestation represents a shift from proving *humanness* through task completion to proving *environmental integrity* — that the JavaScript runtime, DOM, WebGL, and timer APIs behave as they would in a legitimate browser [24, 6]. The canonical fingerprinting survey by Laperdrix et al. [6] catalogs the breadth of the measurement surface. The defense does not need any single measurement to be unforgeable; it needs the *set* of measurements to be jointly difficult to forge consistently. This is the forgery problem at the architectural level.

### 2.3 From Probabilistic Scoring to Hardware-Anchored Determinism

Probabilistic defenses (VM attestation, behavioral telemetry) produce confidence scores derived from noisy sensor data. Deterministic defenses (FIDO2/WebAuthn, DBSC) produce cryptographic proof of hardware key possession [31, 65]. The non-substitutability follows from the NIST Digital Identity Guidelines [65]: deterministic architectures require prior enrollment and cannot screen anonymous traffic.

Privacy Pass [41] and Apple PATs [44] introduced a third category: *deterministic attestation of anonymous traffic*, bridging the "Anonymous Authentication Gap" through cryptographic protocols (VOPRF with DLEQ proofs, RSA blind signatures) [38, 39, 40]. However, as Section 6 details, this closure comes at the cost of vendor centralization.

### 2.4 The Economics-of-Security Lens

Anderson and Moore [46] established information security as fundamentally an economic problem. Herley and Florêncio [47] demonstrated that underground economy pricing follows predictable patterns — "nobody sells gold for the price of silver." Applied to client-side anti-automation, these frameworks yield the critical insight that client-side defenses operate under a *forgery model* rather than a *cryptanalysis model*: the attacker's cost is determined by market prices (proxy IPs, human labor, GPU compute, malware infections), not by a mathematical security parameter.

This distinction is the through-line of the following sections. Prior SoKs have introduced this framing conceptually [6, 24]; this paper gives it systematic structure across the full architectural landscape, then corrects it for the Operator Synthesis paradigm.

---

## 3. PART I: The Historical Landscape — Probabilistic Client-Side Attestation (2010–2024)

*This section is a retrospective post-mortem. The architectures described here were the state of the art for the 2017–2024 period. Under the Operator Synthesis paradigm introduced by VLMs, they face structural degradation for the APB threat model. We systematize them not as standalone active defenses against top-tier adversaries but as diagnostic artifacts that reveal *why* probabilistic client-side attestation has a finite economic ceiling against Operator Synthesis.*

### 3.1 Methodology: Systematic Literature Search

This SoK is based on a systematic literature search following a documented, replicable methodology. We do not employ the PRISMA framework: PRISMA was designed for empirical meta-analyses of clinical trials with well-defined treatment and control groups, and applying it to a qualitative, taxonomic synthesis spanning vendor whitepapers, IETF drafts, and grey literature would force a structured eligibility format that does not fit our heterogeneous source corpus. We instead document our search and selection process transparently below.

**Databases Searched.** IEEE Xplore Digital Library, ACM Digital Library, arXiv (Computer Science > Cryptography and Security), Google Scholar, IETF Datatracker, W3C Technical Reports repository.

**Search Queries.** Primary: `("bot mitigation" OR "browser fingerprinting" OR "anti-automation" OR "bot detection") AND ("economics" OR "cost" OR "attestation" OR "architecture")`. Supplementary queries targeting PATs, behavioral biometrics, VM deobfuscation, DBSC, and PPI malware economics.

**Date Range.** Primary: 2010–2025; backward snowballing for foundational works (Saltzer and Schroeder 1975, Anderson 2006).

**Inclusion Criteria.** (a) Production deployment by a major vendor, (b) architectural documentation in academic literature, IETF/W3C standards, or verifiable grey literature, (c) cost imposition on adversaries through client-side execution.

**Source Corpus.** 78 publications: 52 academic papers, 15 standards/RFCs, 11 grey literature items (vendor whitepapers, malware analysis reports).

### 3.2 Five Architectural Types by Mechanism

We identify five architecturally distinct classes of client-side anti-automation. These types are distinguished by their *primary mechanism*: Execution (probing the runtime through code execution), Telemetry (passive accumulation of behavioral/sensor data), or Cryptographic Binding (hardware-anchored deterministic proof). Real production systems inevitably fuse mechanisms from multiple types (Section 3.3). The following vendor-mechanism matrix maps representative systems to their constituent mechanisms:

| System | Execution | Telemetry | Cryptographic Binding | Primary Mechanism |
|--------|-----------|-----------|----------------------|-------------------|
| Google Botguard | ✓ | | | Execution |
| Turnstile | ✓ | ✓ | | Execution |
| reCAPTCHA v3 | | ✓ | | Telemetry |
| DataDome | | ✓ | | Telemetry |
| Arkose Labs | ✓ | ✓ | | Telemetry |
| Apple PATs | | | ✓ | Cryptographic Binding |
| Privacy Pass | | | ✓ | Cryptographic Binding |
| DBSC | | | ✓ | Cryptographic Binding |
| Passkeys/WebAuthn | | | ✓ | Cryptographic Binding |

**Type I: Point-in-Time VM Attestation.** Executes a custom register-based JavaScript VM within the browser. Measures environmental integrity (L1), uses self-modifying opcodes (L2), anti-introspection traps (L3), and chronometric constraints (L4). Produces a bearer token [76, 77]. Cost imposed: per-execution proxy bandwidth, fixed RE investment, recurring temporal cost per compile rotation. Structural ceiling under Environmental Forgery: IP reputation market exhaustion. Under Operator Synthesis: L1/L4 cease to impose costs; IP reputation remains as the sole binding constraint, but significantly weakened. Representative systems: Google Botguard, Cloudflare Turnstile Managed Challenge, Kasada.

**Type II: Stateful Behavioral Telemetry.** Accumulates long-term behavioral profiles using persistent identifiers (cookies, fingerprinting). Scores mouse movements, scroll patterns, navigation cadence, and dwell time over weeks to months. Cost imposed: conjunctive stack of proxy + aged profile + anti-detect software license [13, 58]. Structural ceiling under Environmental Forgery: profile-aging latency (cannot be bypassed by spending). Under Operator Synthesis: the VLM inherits the legitimate browser's profile, collapsing the aging requirement. Representative systems: reCAPTCHA v3, DataDome, Human Security (PerimeterX).

**Type III: Behavioral Biometrics & Sensor Telemetry.** Measures mouse kinematics (velocity, acceleration, Bezier-curve fitting), scroll patterns, click-timing, touch pressure, accelerometer polling [15, 20]. Cost imposed under Environmental Forgery: `min(Cost_ML_Inference, Cost_Human_Labor)`, where human labor (CAPTCHA-solving farms at ∼$1/1K challenges [51]) sets the global cost floor. Under Operator Synthesis: the VLM's emergent motor control is drawn from the same distribution as human operators, collapsing the detection premise entirely.

**Type IV: Platform/OS-Level Anonymous Attestation (Privacy Pass / PATs).** Hardware-backed cryptographic anonymous tokens (RSA blind signatures, VOPRF). Token issuance rate-limited per-device [43]. Cost imposed: device compromise through PPI malware [53, 56]; extraction of attestation keys is prohibitively expensive, but proxying through compromised devices is economically viable. This architecture survives Operator Synthesis (Tier 1) because the cryptographic binding operates independently of browser input modality. Representative systems: Apple PATs, Cloudflare/Fastly Privacy Pass issuance.

**Type V: Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys).** Cryptographic proof of hardware key possession. DBSC extends this from authentication to session lifetime [36, 37]. Cost imposed: device compromise through PPI malware at $75–$200/month per botnet subscription [56]. Structurally inapplicable to anonymous traffic [65]. Also survives Operator Synthesis (Tier 1). Representative systems: Google DBSC, W3C WebAuthn, Passkeys (Apple, Google, Microsoft).

### 3.3 The Hybrid Reality: Production Systems Fuse Mechanisms

A taxonomy that cannot cleanly classify the three most prominent production systems — Cloudflare Turnstile, DataDome, and Arkose Labs — without immediately resorting to "hybrid" exceptions has limited diagnostic value unless the hybrid nature is acknowledged from the outset.

Cloudflare Turnstile uses a JavaScript VM challenge as the *delivery mechanism* for stateful telemetry collection. The VM does not merely measure the environment; it establishes a persistent session that feeds a behavioral scoring engine. Turnstile is simultaneously Type I (point-in-time VM attestation) and Type II (stateful behavioral telemetry), with the VM serving as the instrumentation layer for the telemetry [60].

DataDome similarly fuses Type II (stateful profile accumulation) with Type III (mouse kinematics and behavioral biometrics), using one to bootstrap the other when profile data is insufficient [64].

Arkose Labs deploys visual-interactive challenges (Type I auxiliary) as a fallback escalation when its probabilistic scoring (Type II/III fusion) is inconclusive.

These are not edge cases or implementation flaws. They are evidence that the industry converged on hybrid architectures because each pure architectural type has a well-understood structural weakness that a complementary type can partially mitigate. The taxonomy's value is not in achieving clean classification of every system, but in providing the *analytical vocabulary* to identify which mechanisms a hybrid system combines and which attack vectors remain exposed.

In this SoK, we classify each system by the mechanism that most closely describes its *binding structural ceiling*: the constraint that limits the adversary's throughput regardless of hybridization. For Turnstile, the binding constraint remains IP reputation (Execution mechanism), even though behavioral telemetry (Telemetry mechanism) provides supplementary signal.

### 3.4 The L1–L4 Diagnostic Framework

The L1–L4 framework described here is derived from the defense-in-depth architecture observed in Google's Botguard VM [24]. We generalize it as a *historical diagnostic framework* applicable to any point-in-time VM attestation system — not as a prescriptive architecture for future defenses. The framework's value today is diagnostic: it reveals *why* each defensive layer fails under Operator Synthesis. We present it in vendor-neutral terms while acknowledging that the precise instantiation of each layer varies across implementations.

Each layer collapses for a single structural reason: under Operator Synthesis, the adversary drives a legitimate unmodified browser, so every defensive mechanism that relies on detecting instrumentation or forgery receives only ground-truth signals. Specifically:

- **L1a (Static Environmental Introspection)** — Detects forged `navigator` properties, WebGL artifacts, DOM prototype chain integrity violations [6]. Under OS: all properties are inherited from a legitimate browser; zero forgery required.
- **L1b (Dynamic Sensor Telemetry)** — Measures mouse kinematics, scroll patterns, click-timing against human-distribution models [15, 20]. Under OS: VLM motor control is emergent from web-scale human-demonstration training and draws from the same distribution.
- **L2 (Code Obfuscation, Polymorphism)** — Self-modifying opcodes, compile rotation raise RE cost [24, 27]. Under OS: the VLM never inspects bytecode — executes the VM as a black box. $T_{RE} = 0$.
- **L3 (Execution Traps)** — Console-bound traps, anti-debugger hooks, prototype integrity checks [24]. Under OS: no DevTools opened, no runtime instrumented — traps are never triggered.
- **L4 (Chronometric Integrity)** — `performance.now()` polling and timing-delta-based seed mutation [24, 5]. Under OS: native execution — no instrumentation layer introduces timing deviation.

**Diagnostic Summary.**

| Layer | Cost Type (EF) | Cost Under OS | Why |
|-------|----------------|---------------|-----|
| L1a | Variable (compute for forgery) | Zero | Properties inherited from legitimate browser |
| L1b | Variable (ML inference or labor) | Zero | VLM motor control matches human distribution |
| L2 | Temporal (RE per compile rotation) | Zero | Black-box execution; no RE required |
| L3 | Mixed (trap identification + overhead) | Zero | Traps never triggered in stock browser |
| L4 | Variable (timer synchronization) | Zero | Native execution; no timing deviation |

The diagnostic value: under Operator Synthesis, the entire L1–L4 stack collapses simultaneously because every layer relies on the premise that the adversary must instrument or subvert the browser. When the adversary simply uses the browser as intended, no layer imposes any marginal cost.

### 3.5 The Temporal Arms Race: A Historical Case Study

Prior work [24] framed the temporal arms race between AST obfuscators and symbolic execution engines as a live analytical contribution. Under Operator Synthesis, the VLM attacker never enters this race — obviating the need for detailed race-condition analysis. We summarize the key finding: compile rotation (`T_Life`) pits the defender's CI/CD cadence against the attacker's reverse-engineering pipeline (`T_RE`). The race was already structurally asymmetric — the defender must produce a working VM for millions of diverse browsers, while the attacker only extracts a single bytecode-to-semantics mapping via automated tools (Syntia [26], DOBF [28]). The tipping point `T_RE < T_Life` was approaching for the best-defended VMs. Operator Synthesis terminates the race at the VM level: the attacker never inspects the defensive bytecode, though application-level workflow RE (Section 5.5) remains necessary.

The wider lesson extends beyond anti-automation: software-only obfuscation has a structural ceiling — it cannot impose cost against an adversary who bypasses the inspection step entirely, as the VLM attacker does at the VM level.

---

## 4. PART II: The VLM/Operator Synthesis Paradigm Shift

*This section analyzes the paradigm shift introduced by Operator Synthesis for the APB threat model and establishes a forward-looking research agenda for VLM-resilient anti-automation. Consistent with the scope limitation in Section 1.2, claims of "collapse" or "bypass" refer to structural vulnerability against this top-tier adversary class, not universal invalidation of probabilistic defenses.*

### 4.1 Axis C as the New Baseline: What Operator Synthesis Changes

Operator Synthesis redraws several foundational assumptions of client-side anti-automation for the APB threat model. However, caution is warranted: the table below describes Operator Synthesis in its idealized form. In practice, industrial-scale VLM deployment introduces environmental constraints that partially re-open detection surfaces.

| Assumption | Environmental Forgery | Operator Synthesis (Idealized) | Operator Synthesis (At Scale) |
|---|---|---|---|
| Browser state | Instrumented / modified | Stock, legitimate | Stock browser, but orchestration surfaces exposed |
| DOM integrity | Compromised | Intact | Intact |
| Sensor data | Forged | Ground truth | Ground truth for browser APIs; containerization leaks at OS/network layers |
| Execution timing | Affected by instrumentation | Native | Native at JS runtime level; VLM inference latency adds second-scale delays |
| Input modality | Programmatic API calls | OS-level GUI synthesis | OS-level GUI synthesis through an orchestration layer (PyAutoGUI, accessibility APIs) |
| Motor control | Separate GAN/trajectory generator | Emergent from VLM training | Emergent VLM selection, instantiated through orchestration layer that may introduce detectable kinematic artifacts |

**The containerization gap.** To operate VLMs at industrial scale, attackers use containerized, headless, or virtualized environments (Docker, Kubernetes, cloud VMs), not physical devices on desks. A stock Chrome browser running inside a Linux Docker container and routed through a residential proxy network still bleeds environmental anomalies relative to a genuine user device: missing system fonts that vary from the User-Agent's declared OS, mismatched WebGL rendering artifacts versus the expected GPU driver stack, predictable AudioContext timing profiles, and anomalous TCP/IP stack fingerprints (MTU sizes, TTL values, initial window sizes). These environmental leaks mean that L1a detection — environmental introspection — is *not* fully collapsed under industrial-scale Operator Synthesis. The VLM solves the cognitive aspects of the attack, but the deployment environment re-opens a reduced but non-zero environmental forgery surface.

This is not a marginal improvement in attack capability for its target threat model — it represents a significant shift in the cost curve. The attacker's browser is not a compromised browser; it is a browser being used exactly as designed, but by a synthetic operator through a deployment stack that introduces detectable artifacts at scale.

### 4.2 Architecture-by-Architecture Collapse Under Operator Synthesis

**Type I (Point-in-Time VM Attestation) → Degraded to Tier 2.** L1–L4 cease to impose meaningful costs. IP reputation remains as the sole binding economic constraint, but without the multiplicative cost of environmental forgery, the effective per-token cost drops substantially (Section 5.3). The VM becomes a delivery mechanism rather than a defense — it delivers the challenge, but the challenge imposes no forgery cost.

**Type II (Stateful Behavioral Telemetry) → Degraded to Tier 2/3 (Profile-aging constraint lifted; state-orchestration cost substituted).** The VLM can generate human-like behavior from a fresh browser instance with no aging penalty — lifting the profile-aging latency constraint that was the structural ceiling under Environmental Forgery. However, a critical nuance applies: VLMs are stateless between inference calls unless explicitly orchestrated. Maintaining, isolating, and rotating aged cookie jars, local storage snapshots, and IndexedDB state across thousands of parallel VLM instances without cross-contamination is a non-trivial orchestration problem. Each parallel session requires an isolated browser profile, a persistent cookie store, and clean session state — and the cost of managing this infrastructure at scale substitutes for the anti-detect browser license that Environmental Forgery required. The profile-aging *latency* constraint collapses, but a state-orchestration *complexity* and *infrastructure* cost replaces it. This shifts Type II from a latency-bound problem to an operations-bound problem, which is a meaningful degradation but not a disappearance of defense-imposed cost.

**Type III (Behavioral Biometrics & Sensor Telemetry) → Degraded to Tier 2/3 (Cognitive selection bypassed; kinematic instantiation gap remains).** The VLM's cognitive ability to locate visual targets and output coordinate selections is emergent from vision-language training on human demonstrations. However, as discussed in Section 1.4, the VLM does not natively produce the kinematic trajectory between those coordinates — an orchestration layer translates the VLM's coordinate output into mouse movement. If the orchestration layer uses naive linear interpolation, constant-velocity profiles, or generic ease-in/ease-out curves, the resulting mouse kinematics remain statistically distinguishable from the smooth, biologically-motivated acceleration profiles of human movement. Behavioral biometrics (L1b) retain detection leverage against poorly-implemented orchestration. Sophisticated attackers will invest in a kinematic-smoothing layer (adaptive Bezier trajectory generation with human-derived acceleration profiles) to close this gap, but this adds engineering cost that the "structurally bypassed" framing understates. The detection premise shifts from "the VLM cannot produce human-like interactions" to "the VLM can produce human-like interactions only if the orchestration layer correctly implements human motor kinematics," which is a substantively different and narrower attack surface than full collapse.

**Type IV (Anonymous Attestation / PATs) → Tier 1 (Structurally Resilient).** The cryptographic binding is to device hardware, not to browser input modality. Whether the browser is driven by a human or a VLM is irrelevant to the attestation protocol. The attacker must compromise the device to extract attestation keys, which is a separate attack chain (PPI malware, physical access) with its own economic ceiling [56].

**Type V (Hardware-Anchored Determinism / DBSC) → Tier 1 (Structurally Resilient).** Same logic as Type IV: the cryptographic proof of hardware key possession is input- modality-independent. The session cookie is bound to the TPM/Secure Enclave regardless of how the browser is driven.

### 4.3 What Survives: Tier 1 Architectures and Their Structural Limits

Tier 1 architectures survive because they anchor security in hardware rather than in probabilistic detection of behavioral signals. However, survival is not immunity. Each Tier 1 architecture has a structural limit:

**PATs (Type IV): The device compromise ceiling.** PATs are resilient against Operator Synthesis, but the attacker can still bypass them by compromising the device. PPI malware networks provide device access at $75–$200/month per botnet, with per-infection costs as low as $0.10–$0.50 for high-volume operations [53, 56]. The economic ceiling is the black-market price of a successful infection — not the mathematical hardness of the VOPRF protocol, but the market equilibrium of the malware supply chain. Additionally, PAT issuance is rate-limited per device [43], which caps throughput even for compromised devices.

Crucially, the device-compromise ceiling is not limited to criminal malware. SDK-based residential proxy networks (Bright Data, the former Hola network, and various mobile-proxy SDKs) operate in a legal gray area: end users consent to installing free applications (mobile games, utilities, VPNs) that embed proxying SDKs, routing traffic through the user's legitimate device [79]. These SDKs have access to the device's Secure Enclave or TPM, enabling them to generate valid PAT attestations using the user's actual hardware keys without triggering the malware detection surface of OS-level security mitigations. The supply elasticity of SDK-proxied devices is orders of magnitude higher than PPI botnets — Bright Data alone claims access to tens of millions of residential IPs across 195+ countries — and the marginal cost per attested device is effectively zero once the SDK is deployed. This drastically lowers the effective bypass ceiling for PATs below the black-market PPI pricing that prior work assumes. A defender relying on PATs must recognize that the relevant threat is not exclusively the $75–$200/month botnet subscription but also the commoditized SDK proxy market that routes through legitimate consented devices at significantly lower cost.

**DBSC/Passkeys (Type V): The post-authentication session ceiling.** DBSC prevents cookie theft across devices, but a compromised device exports both the session state and the bound key simultaneously. Tarrach et al. [33] identified message integrity gaps accessible to browser extensions. Kuchhal et al. [32] found only 4.4% of authenticators carry Level 2+ malware resistance certification. The structural limit is not the cryptographic protocol but the practical difficulty of guaranteeing the integrity of the key-storage environment.

**The universal ceiling: supply-chain economics.** Both Tier 1 architectures ultimately depend on the cost of device compromise. This cost is not determined by the protocol design but by the malware supply chain market [56], the effectiveness of OS-level security mitigations (iOS hardened runtime, Android KeyStore, Windows Credential Guard), and the user's security posture. Every Tier 1 architecture has an economic ceiling below which it deters adversaries and above which it does not.

### 4.4 The False Dichotomy: Why PATs Are Not a Silver Bullet

A naive reading of Section 4.2 might suggest that PATs and DBSC represent a complete solution: deploy PATs for anonymous traffic, deploy DBSC for authenticated sessions, and the anti-automation problem is solved. This is structurally incorrect for three reasons.

**1. PATs require platform-level coordination.** PAT issuance requires the OS vendor (Apple, Google, Microsoft) to operate an issuer or authorize a third-party issuer. This creates a dependency on vendor participation that is not guaranteed for all platforms, all regions, or all use cases. A web origin cannot deploy PATs independently; it must integrate with a platform-level attestation infrastructure.

**2. PATs shift the trust problem rather than solving it.** Pre-PATs, the trust question was: "Can I distinguish human from automated traffic?" Post-PATs, the trust question becomes: "Do I trust Apple/Google/Microsoft's attestation infrastructure more than probabilistic detection?" For many defenders, the answer is yes, but this is an economic and political judgment, not a technical guarantee. The attestation infrastructure is controlled by three US-based corporations, each operating its own advertising business with incentives that may diverge from those of the web origin consuming the attestation.

**3. PATs create a two-tier accessibility surface.** If VLMs structurally bypass probabilistic defenses, and PATs provide the only viable path for deterministic anonymous attestation, then any web origin that deploys PAT-only anti-automation effectively requires users to have a PAT-compatible device (iOS 16+/macOS Ventura+ for Apple PATs; Android-compatible Privacy Pass for Google). This creates an accessibility barrier that is structurally regressive.

---

## 5. An Initial Cost Model for VLM-Driven Attacks

*This section provides a parametric cost model for reasoning about the economics of Operator Synthesis attacks. We do not claim to have discovered a complete microeconomic theory of VLM-based attack — the market is too young and the data too sparse. We instead provide a structured framework for reasoning about attacker costs, identify the empirical gaps that prevent precise quantification, and set a research agenda for closing those gaps. We approach prior work's economic framing with respect: the conjunctive cost models of Section 3 and prior SoKs [6, 24] correctly identified the multi-constraint nature of anti-automation bypass, and our contribution is to extend that framing to the Operator Synthesis paradigm, not to dismiss the foundation.*

### 5.1 VLM Inference Cost Under Operator Synthesis

The primary variable cost of an Operator Synthesis attack is VLM inference. Prior conjunctive cost models [24, 47] correctly identified the multi-cost structure of Environmental Forgery — proxy IPs, anti-detect software, profile aging. Under Operator Synthesis, VLM inference is an *additional necessary* cost for any attack that requires visual perception of rendered browser content, supplementing rather than supplanting the proxy and state-orchestration components of prior models.

**Parameterized cost model.** The base per-task inference cost is:

```
C_inference = (t_input × p_input + t_output × p_output) × r_per_token
```

Where:
- `t_input` = input tokens per task (screen capture encoding + prompt context)
- `t_output` = output tokens per task (action selection + coordinate generation)
- `p_input` = input token price (model-dependent, $1.25–$5.00 per million tokens for frontier models as of Q1 2026)
- `p_output` = output token price (model-dependent, $5.00–$20.00 per million tokens)
- `r_per_token` = amortized compute overhead per token (batch processing, caching, API latency)

**Modeling failure rates.** The base cost model assumes 100% task completion, which does not hold in practice. VLMs hallucinate, select incorrect bounding boxes, enter navigation loops, and time out on dynamic DOM elements that confuse their spatial mapping. The effective cost per successful bypass must incorporate the task success probability:

```
C_effective = C_inference / P(success) + C_retry × (1 - P(success)) / P(success)
```

Where `P(success)` is the per-attempt probability of producing a valid bypass token. A VLM with a 60% per-task success rate — consistent with reported agentic benchmarking on complex multi-step flows [80, 81] — faces an effective cost multiplier of 1.67×; at 40% success, the multiplier reaches 2.5×. Error recovery adds further cost: each failed attempt consumes the same inference budget as the original attempt, and the model may require additional context tokens to diagnose the failure and re-plan, increasing `t_input` on retry attempts. At industrial scale, even a 10-percentage-point difference in `P(success)` yields a meaningful cost differential: for a $0.05 nominal per-token cost, a 40% vs. 70% success rate shifts the effective cost from $0.125 to $0.071 — a 43% difference that directly determines whether the attack is economically viable against a given defender's token lifetime.

The dependence of `P(success)` on task complexity introduces a testable empirical prediction: defenses that increase perceptual ambiguity (dynamic CSS layouts, canvas obfuscation, adversarial-noise overlays) should reduce VLM task success rates, thereby increasing effective attack costs. This prediction links the economic framework directly to the visual-reasoning deobfuscation gap identified in Section 3.5.

**Empirical baselines (as of Q1 2026).** Published pricing for frontier VLMs:
- GPT-4o: $2.50/M input tokens, $10.00/M output tokens
- Claude 3.5 Sonnet (Computer Use): $3.00/M input, $15.00/M output
- Gemini 2.0 Flash: $1.25/M input, $5.00/M output

For a typical web interaction task requiring one screen capture (∼1,000 tokens) and one action selection (∼500 tokens output), the per-action cost is approximately $0.0025–$0.01. For an attack requiring 10 interactions per token generation (navigating to the target page, waiting for the VM to load, receiving the token), the per-token cost is $0.025–$0.10.

**Scaling properties.** Critically, VLM inference costs follow a *deflationary* trajectory. Each new model generation has historically reduced per-token costs by 2–5× while maintaining or improving capability. Moore's Law for LLM inference predicts sustained cost reduction through:
- Quantization (FP16 → INT4 reduces cost by ∼4×)
- Speculative decoding (2–3× throughput improvement)
- Model distillation (smaller models for specific tasks)
- Inference hardware specialization (TPU v5p, NVIDIA B200, custom ASICs)

This deflation means the cost ceiling of VLM-based attacks is *temporally unstable* — it decreases predictably over time, unlike the relatively stable cost of human labor or residential proxy IPs.

### 5.2 The Latency Cost: Temporal Overhead as a Non-Trivial Attack Surface

The cost model in Section 5.1 considers only token-price economics. A second cost dimension — temporal latency — operates independently and can trigger defensive mechanisms that token-price savings do not mitigate. Frontier VLMs typically require 5–15 seconds per inference cycle: screen capture encoding, model inference, and action selection. For multi-step web flows requiring 5–10 interactions per token generation, the per-token wall-clock time is 25–150 seconds.

This latency matters for two reasons:

1. **Chronometric heuristics (L4).** Defenders measure `performance.now()` deltas, event-loop starvation patterns, and task completion cadence. A human completes a standard VM challenge in 200–800ms of interaction time. A VLM-driven session with 30–120 seconds of "think time" between actions produces a timing distribution that falls outside human baselines, regardless of the legitimacy of the browser environment. While Section 3.4 correctly notes that L4 chronometric heuristics were designed to detect instrumentation-layer timing deviation — not operator latency — a sophisticated defender can extend L4 to profile *operator* timing. The fundamental asymmetry is that the VLM's per-action latency is bounded below by model inference speed (~5s minimum for frontier models), while human per-action latency is bounded below by reaction time (~100ms for practiced interactions). This 50× gap creates a detectable signal at scale.

2. **Session timeout risk.** Web applications impose server-side session timeouts (typically 5–30 minutes for authenticated sessions, 1–5 minutes for anti-automation challenge windows). A VLM with 30s per action on a 10-step flow approaches 5-minute per-session latency, pushing against practical timeout boundaries. Failed sessions due to timeout consume inference budget without producing valid tokens, feeding into the `P(success)` penalty in Section 5.1.

The effective cost per successful token must therefore incorporate temporal overhead:

```
C_temporal = C_inference + C_bandwidth_per_session + C_timeout_loss
```

Where `C_timeout_loss = C_inference × P(timeout) / (1 - P(timeout))`. This is largely orthogonal to the token-price deflation discussed in Section 5.1: model inference speed improvements (speculative decoding, faster hardware) reduce temporal latency, but the gap between human reaction time and VLM inference time will persist for the foreseeable future.

### 5.3 The Proxy Supply Market: Elasticity, Equilibrium, and Exhaustion

Under Environmental Forgery, the proxy supply market was the binding structural constraint. Under Operator Synthesis, the proxy is still required — the VLM must route traffic through residential IPs — but the economics shift because the VLM imposes different demands on the proxy infrastructure.

**Supply elasticity.** Residential proxy markets exhibit a tiered supply structure:
- **Commodity tier:** ∼$0.50–$1.50/GB for shared residential IPs with moderate reputation. High elasticity: supply is effectively infinite at this price point. However, reputation is a commons [59]: aggressive usage burns IP reputation across the pool.
- **Premium tier:** ∼$10–$15/GB for exclusive, unburned residential IPs. Low elasticity: supply is constrained by the number of devices in the botnet or proxy network.
- **Enterprise tier:** ∼$25–$50/GB for dedicated IPs with guaranteed clean reputation. Very low elasticity.

For Operator Synthesis attacks, the commodity tier is less usable because the VLM must maintain persistent session state (profiles, cookies) across multiple interactions. A commodity IP rotated per request breaks the session continuity required for stateful applications. The VLM attacker's proxy demand shifts toward the premium and enterprise tiers, which have lower supply elasticity.

**Corrected conjunctive cost model.** Prior work modeled the conjunctive cost of stateful telemetry bypass as: `Cost_proxy + Cost_aged_profile + Cost_software_license`. Under Operator Synthesis, the attacker who drives a stock browser eliminates the anti-detect software license but *substitutes a state-orchestration infrastructure cost*:

```
Cost_bypass_OS = Cost_residential_proxy + Cost_session_isolation + Cost_VLM_inference
```

Where `Cost_session_isolation` includes:
- Containerized browser instances per session (Docker/K8s orchestration)
- Persistent cookie-jar and local-storage management
- Profile rotation and rehydration infrastructure
- Bandwidth for browser binary downloads and updates

This correction resolves the paradox identified in prior critique: under Operator Synthesis, the attacker does not simply "save" the anti-detect browser cost. They must replace it with heavy state-orchestration infrastructure that was previously bundled in the anti-detect browser license. The net savings are positive (orchestration is cheaper per-session than anti-detect software licensing), but not as large as a naive comparison would suggest.

### 5.4 Human Labor as the Global Cost Floor: Revisited

Prior work correctly identified human labor — CAPTCHA-solving farms at ∼$1 per 1,000 challenges [51], click-farms for behavioral challenges — as the global cost floor for bypassing behavioral biometrics under Environmental Forgery. Under Operator Synthesis, this floor shifts:

- **For Tasks Requiring Visual Perception (the VLM case):** Human labor is no longer a substitute for VLM inference. A human solving a CAPTCHA must see it, interpret it, and respond. A VLM performing the same task uses inference, not labor. The relevant comparison is between VLM inference cost and human labor cost for the specific task. Published CAPTCHA-solving farm rates ($0.50–$2.00 per 1,000 solved) are lower than VLM per-token costs for simple challenges, but VLM costs are declining while labor costs are floor-stable.

- **For Tasks Requiring Contextual Understanding (the Operator Synthesis case):** A VLM navigating a multi-step web flow, maintaining context across pages, and adapting to dynamic content is performing a task that human labor cannot directly substitute. The operator is the model, not a click-farm worker. The relevant cost comparison shifts from `min(ML, Human)` to `VLM_cost_only`, bounded below by the model's inference economics.

### 5.5 The Temporal Arms Race Post-Mortem: Why T_RE ≈ 0 Is the New Normal (With a Critical Caveat)

Under Environmental Forgery, the temporal arms race between defender compile rotation and attacker RE was quantified as a race condition:

```
T_RE < T_Life → defense is structurally bypassed
T_RE > T_Life → defense imposes recurring cost
```

Under Operator Synthesis, `T_RE ≈ 0` for the VM bytecode itself — the attacker never reverse-engineers the defensive VM. The VM-level temporal constraint is eliminated.

**Critical caveat: T_RE is not zero for the target application.** While the attacker does not RE the defensive VM's bytecode, they *must* reverse-engineer the target application's DOM structure, navigation flow, and interaction logic to write effective VLM prompts and orchestration scripts. An e-commerce checkout flow, a multi-step account registration, or a CAPTCHA-wrapped form submission each require the attacker to understand the page's DOM hierarchy, CSS selectors, event handlers, and state transitions to define the VLM's action space. This application-level RE cost scales with the number of target workflows and the complexity of the target application's frontend architecture. Single-page applications (SPAs) with dynamic DOM mutation impose higher RE cost than static HTML pages. While application-level RE is cheaper per-target than VM bytecode RE (the attacker works with standard browser DevTools rather than a symbolic execution engine), it is not zero, and it creates a per-target fixed cost that operators of large-scale attacks across many origins must amortize.

**Implication for defenders.** Any defensive architecture whose security relies on VM obfuscation complexity or compile rotation cadence is structurally unsound against Operator Synthesis for the APB threat model — the attacker is not racing at the VM level. However, defenses that increase application-level workflow diversity (dynamic DOM layouts, randomized element selectors, variable interaction sequences) can impose meaningful RE costs on the attacker, as each unique workflow requires separate prompt engineering and orchestration logic.

**What remains at the VLM level.** The only surviving VLM-specific temporal constraint is the freshness of the VLM's training data. If the defensive challenge requires interaction patterns that post-date the VLM's training cutoff, the VLM may generate out-of-distribution behavior. This is a narrow and decreasing temporal window: frontier models are trained on increasingly current data, and the gap between training cutoff and deployment is measured in weeks.

---

## 6. Industry Trajectory and the Attestation Market Centralization Problem

### 6.1 DBSC and the Session-Hijacking Threat Model

DBSC [36, 37] cryptographically binds session cookies to a device-resident key (TPM/Secure Enclave), with periodic proof-of-possession [78] throughout the session lifetime. This targets the session-hijacking threat model (NIST 800-63 Authenticated/ATO quadrant [65]) and is structurally inapplicable to anonymous traffic.

The infostealer economy [53, 54, 55, 56] provides the economic bypass: malware infections export both the session cookie and the device-bound key simultaneously from a compromised device. At $75–$200/month for botnet access [56], the economic ceiling is the black-market infection cost, not the cryptographic protocol strength.

However, as with PATs (Section 4.3), the botnet-infection ceiling is not the only bypass path. SDK-based proxy networks — where users consent to proxying software bundled in free applications — provide access to the same TPM/Secure Enclave keys without triggering malware-classification heuristics. A device running a Bright Data SDK endpoint generates valid DBSC proofs-of-possession using hardware keys on the actual enrolled device. The SDK-based bypass ceiling is lower than the PPI malware ceiling by a wide margin, and the supply is more elastic. This introduces a structural vulnerability for Tier 1 architectures that prior threat models have not adequately addressed: the operating system cannot distinguish between legitimate SDK network traffic routed through consenting devices and criminal malware — both execute with user-level or kernel-level permissions on the hardware that holds the attestation keys.

### 6.2 Passkeys and the Credential-Phishing Threat Model

Passkeys (FIDO2/WebAuthn [31]) eliminate shared secrets and credential phishing through hardware-enrolled cryptographic authentication. Kuchhal et al. [32] found only 4.4% of authenticators carry Level 2+ certification offering malware resistance. Tarrach et al. [33] identified message integrity gaps accessible to browser extensions. The structural limit is the practical difficulty of guaranteeing key-storage integrity across the diversity of consumer devices.

### 6.3 The Attestation Market Centralization Problem

The most significant structural consequence of the VLM paradigm shift — more significant than any individual architecture's vulnerability — is the transformation of the attestation infrastructure market. As probabilistic defenses lose efficacy against Operator Synthesis, the remaining viable defenses (PATs, DBSC, Passkeys) all share a common dependency: they require platform-level root of trust infrastructure operated by OS vendors.

**The consolidation dynamic.** Three companies — Apple, Google, Microsoft — control the device attestation layer for the web:
- **Apple PATs:** RSA blind signatures issued by Apple's servers, backed by Secure Enclave attestation on iOS 16+ and macOS Ventura+ [44]. Token issuance is rate-limited per device. Apple controls which origins receive tokens and at what rate.
- **Google Privacy Pass:** VOPRF-based issuance integrated into Chrome via the Private State Token API [45]. Google operates an issuer. Google controls which origins participate and under what terms.
- **Microsoft Device Bound Session Credentials:** TPM-backed session binding in Windows and Edge [36]. Microsoft controls the key storage and attestation infrastructure.

**Reframing the trilemma.** Prior work [42, 43] usefully framed this as a "Centralization vs. Anonymity Trilemma" — identifying a theoretical trade-off between anonymous access, deterministic bot resistance, and decentralized trust. This framing correctly identified the structural tension. We extend it by observing that the trilemma is not merely a theoretical construct but an empirically observable market outcome: all three OS vendors have converged on centralized attestation infrastructure as the practical resolution of the trilemma, and the resulting market consolidation is its own structural concern distinct from the abstract trade-off. The centralization problem is therefore not a refutation of the trilemma framing but an empirical corollary: given the trilemma, the market has resolved it through platform vendor consolidation, and this resolution carries consequences — pricing power, exclusion risk, and vendor lock-in — that the theoretical trilemma framing alone does not capture. The question is not whether decentralized anonymous attestation is theoretically possible (it is — zero-knowledge proofs of personhood, decentralized issuer networks, and threshold attestation protocols are all feasible in principle). The question is whether any decentralized alternative can achieve the *economic scaling* to compete with platform-integrated attestation.

**The ad-tech macroeconomic context.** The deprecation of third-party cookies by browser vendors — who simultaneously operate the largest digital advertising platforms — creates a dual economic effect: it degrades independent stateful bot mitigation (Type II) while consolidating attestation power into platform-native APIs (Privacy Sandbox, PATs, SKAdNetwork). This intersection of ad-tech market consolidation and bot mitigation economics requires critical scrutiny beyond the technical protocol analysis.

---

## 7. Open Problems and Future Research

### 7.1 Closing the Empirical Gap in VLM Attack Economics

The parametric cost model in Section 5 is deliberately incomplete. We currently lack:
- Published empirical measurements of VLM-driven attack throughput at industrial scale
- Reliable data on proxy market supply elasticity under Operator Synthesis demand patterns
- Longitudinal studies of VLM inference cost deflation and its impact on attack economics

A standardized, ethical benchmark for measuring VLM-driven bypass costs — analogous to the "Bot-Bench" gap identified for VM chronometrics — is needed to transform the qualitative economic analysis of Section 5 into a quantitative discipline.

### 7.2 VLM-Resilient Attestation Primitives

The Tier 1 architectures identified in Section 4.2 survive Operator Synthesis but carry the structural dependencies documented in Section 6. Research needed on:
- **Decentralized anonymous attestation:** Zero-knowledge proofs of personhood, decentralized issuer networks (threshold issuance, distributed VOPRF), and hardware-backed attestation without OS-vendor dependency.
- **Physical-presence challenges:** Defenses that require physical-world interaction (camera-based liveness detection, ambient sensor fusion) that a VLM operating in a virtual machine cannot satisfy. These are not CAPTCHAs — they do not require human cognition — but they impose a physical-presence cost that distinguishes local execution from remote VLM operation.
- **Cross-modal consistency verification:** Verifying that sensor data from multiple independent channels (camera, microphone, touchscreen, accelerometer) is internally consistent with a single physical environment. A VLM operating in a VM cannot easily maintain cross-modal consistency because it does not control all sensor channels.

### 7.3 Standardized Benchmarking (The "Bot-Bench" Problem)

Academia lacks a standardized testbed for evaluating anti-automation defenses under Operator Synthesis. Current evaluations rely on grey-hat reverse engineering of production systems or small-scale PoCs that vendors invalidate through compile rotation. A reproducible, vendor-neutral evaluation harness — with known ground truth for human vs. VLM interaction — is necessary for systematic measurement. The BehavePassDB effort [23] provides a partial template but does not account for VLM interaction patterns.

### 7.4 Privacy Regulation's Collateral Damage on Stateful Mitigation

GDPR, ePrivacy Directive, and third-party cookie deprecation break the profile-aging model underpinning stateful telemetry (Type II). As browsers restrict persistent identifiers (ITP, ETP, Total Cookie Protection), the economic ceiling of stateful defenses rises — they become less effective — yet vendors continue to market them. The tension between privacy regulation and stateful bot mitigation, particularly under the additional stress of Operator Synthesis, is under-studied. Furthermore, the deprecation of cross-site identifiers by browser vendors (who are also major ad platforms) degrades independent stateful mitigation while consolidating attestation power into platform-native APIs — a dual effect that requires antitrust and architectural scrutiny.

---

## 8. Conclusion

This SoK has presented a two-part systematization of client-side anti-automation. In Part I, we documented the historical landscape (2010–2024) through five mechanism-based architectural types and the L1–L4 diagnostic framework, explicitly framing these as retrospective artifacts that reveal why probabilistic client-side attestation has a finite economic ceiling. In Part II, we analyzed the VLM/Operator Synthesis paradigm shift, showing that environmental introspection (L1), code obfuscation (L2), execution traps (L3), and chronometric integrity (L4) all collapse under Operator Synthesis, along with stateful behavioral telemetry and behavioral biometrics.

The architectures that survive — Platform/OS-level anonymous attestation and hardware-anchored determinism — do so because their security is anchored in cryptographic hardware possession rather than probabilistic detection of behavioral signals. But survival is not immunity: these architectures carry a structural dependency on a vendor oligopoly controlling the root of trust, and their economic ceiling is the black-market price of device compromise, not the mathematical hardness of the attestation protocol.

Three insights define the field's trajectory for the APB threat model:
1. **Probabilistic client-side attestation faces structural degradation under Operator Synthesis.** Against a well-resourced adversary operating a VLM through an adequate orchestration pipeline, the detection premise on which VM attestation, behavioral telemetry, and biometric analysis relied is bypassed. Defenses that remain effective against commodity adversaries lose their cost-imposing power against this top-tier threat model.
2. **Hardware-anchored attestation is necessary but not sufficient.** It survives the paradigm shift but introduces vendor centralization, device-adoption dependencies, and a shifting of the attack surface to the device-compromise economics.
3. **The defining open problem is no longer purely "how to detect bots" but increasingly "who controls the infrastructure of web trust."** The Anonymous Authentication Gap has been technically narrowed; the Centralization Gap has emerged as its successor.

Client-side anti-automation faces a significant inflection point. The tools and concepts of the 2017–2024 period — register-based VMs, behavioral scoring, kinematic analysis — retain value as diagnostic artifacts and as defenses against the long tail of commodity automation, but they face structural pressure at the top of the adversary capability distribution. The field must now confront the harder problem of building decentralized, privacy-preserving attestation infrastructure that does not depend on a vendor oligopoly, alongside the continued engineering challenge of hardening probabilistic defenses against lower-resourced adversaries.

---

## References

(See `notes/bibliography.md` for the complete 78-reference bibliography, common to all versions of this paper.)
