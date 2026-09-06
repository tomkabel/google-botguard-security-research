# SoK: Client-Side Anti-Automation Under VLM-Based Attack — From Probabilistic Forgery to Operator Synthesis

---

**Authors:** Abel, T. K.

**Repository:** <https://github.com/tomkabel/google-botguard-security-research>

**Keywords:** Client-side attestation, VLM-based automation, operator synthesis, browser fingerprinting, behavioral biometrics, Privacy Pass, Private Access Tokens, device-bound session credentials, anti-automation economics, systematization of knowledge

---

## Abstract

Client-side anti-automation has evolved through five architecturally distinct paradigms, culminating in a landscape where Vision-Language Models (VLMs) and agentic AI systems challenge the assumptions underlying probabilistic client-side defenses. This Systematization of Knowledge proceeds in two parts. Part I (2010–2024) systematizes the five paradigms — Point-in-Time VM Attestation, Stateful Behavioral Telemetry, Behavioral Biometrics & Sensor Telemetry, Platform/OS-level Anonymous Attestation, and Hardware-Anchored Determinism — as a retrospective post-mortem; recasts the L1–L4 defense-in-depth stack as a historical diagnostic lens showing why each layer fails under Operator Synthesis (the VLM attack vector); and documents the obfuscation-versus-symbolic-execution arms race that the VLM paradigm renders moot. Part II analyzes which architectural properties survive and which degrade, contributes an initial cost-accounting framework grounded in VLM inference pricing, proxy-supply elasticity, and state-orchestration overhead with explicit empirical caveats, and documents attestation-market centralization — Apple, Google, and Microsoft's control over Private Access Tokens, Privacy Pass, and Device Bound Session Credentials, a consolidation the 2026 PACT initiative extends to issuer-judgment governance. The paper closes with an analysis of architectural resilience tiers and a research agenda for VLM-resilient attestation primitives.

**Contributions:**

1. A two-part SoK structure that resolves the structural dissonance of prior work: Part I as a historical retrospective on probabilistic attestation (2010–2024), Part II as a forward-looking analysis under Operator Synthesis.
2. An L1–L4 defense-in-depth framework reframed as a *historical diagnostic tool* for understanding why probabilistic client-side defenses fail under VLM attack, rather than a prescriptive defensive architecture.
3. An initial cost-accounting framework for Operator Synthesis attacks, grounded in VLM inference pricing, proxy market supply elasticity, and state-orchestration overhead, with explicit acknowledgment of the empirical gaps that prevent precise quantification.
4. A concrete analysis of attestation market centralization — documenting the vendor oligopoly (Apple, Google, Microsoft) on root-of-trust infrastructure — building on prior trilemma formulations with empirically grounded observations about market consolidation.

---

## 1. Introduction

### 1.1 Why the Field Still Needs a Taxonomy — And Why It Must Be a Diagnostic One

Client-side anti-automation has, over fifteen years, produced a rich but terminologically fractured design space. Vendors describe structurally different mechanisms using overlapping vocabulary: "bot detection" may refer to a point-in-time VM executing encrypted bytecode (Google Botguard), a long-term behavioral scoring engine (reCAPTCHA v3), or a hardware-attestation protocol (Apple Private Access Tokens) [24, 44, 62]. "Fingerprinting" can denote passive environmental introspection, active behavioral telemetry, or cryptographic token issuance [6, 38]. This imprecision obstructs comparative analysis and impedes academic research.

Previous efforts to systematize this space have attempted to build unified taxonomies that simultaneously classify all existing defenses and prescribe future directions. This paper argues that such an approach faces a structural challenge because the 2024–2025 emergence of production-capable Vision-Language Models (GPT-4o, Claude Computer Use, Gemini 2.0) and agentic AI frameworks (WebVoyager, CUA, Operator) has introduced a qualitatively distinct attack vector — "Operator Synthesis" — that bypasses the core detection premise of probabilistic client-side defenses for the APB threat model, representing the most severe escalation within the Environmental Forgery paradigm rather than a clean categorical break.

The appropriate response is not to force a unified taxonomy that pretends all paradigms remain viable, nor to abandon systematization entirely. It is to produce a *two-part* systematization: a historical retrospective that documents what was built and why it fails (Part I), and a forward-looking analysis that identifies the surviving architectural properties and the research gaps they expose (Part II).

### 1.2 Contributions and the Two-Part Structure

This paper makes four contributions:

**C1 — A Two-Part SoK Structure (Sections 3 and 4).** We explicitly partition the analysis into a historical retrospective (Part I, Section 3) and a forward-looking analysis under the Operator Synthesis paradigm (Part II, Section 4). This resolves the structural dissonance that arises when a single taxonomy attempts to simultaneously classify active defenses and acknowledge their obsolescence.

**C2 — The L1–L4 Framework as a Historical Diagnostic Tool (Section 3.4).** We generalize the four-layer defense-in-depth framework originally observed in Google's Botguard VM [24] into a vendor-neutral model, and explicitly reframe it as a *historical diagnostic framework* — a lens for understanding *why* VM-based attestation faces structural pressure under Operator Synthesis — rather than as a prescriptive architecture. The temporal arms race analysis (Section 3.5) is presented as a historical case study of a dynamic that the VLM paradigm renders moot at the VM level.

**C3 — An Initial Cost-Accounting Framework for VLM-Driven Attacks (Section 5).** We provide cost estimates grounded in observable market data: VLM inference pricing curves, proxy market supply elasticity, state-orchestration overhead, and — newly identified in this work — temporal latency costs from VLM inference delay. The conjunctive cost framework is extended to account for the VLM attacker's state-isolation requirements. We explicitly acknowledge the empirical gaps that prevent precise quantification and set a research agenda for closing them.

**C4 — Attestation Market Centralization Analysis (Section 6).** Building on the prior "Centralization vs. Anonymity Trilemma" framing from W3C mailing list debates [42, 43], we provide a concrete analysis of the attestation market oligopoly. We document how Apple, Google, and Microsoft's control over PAT issuance, Privacy Pass infrastructure, DBSC key storage, and Passkey synchronization creates a structural dependency that transforms the "Anonymous Authentication Gap" into an economic and political centralization problem. We further analyze how the 2026 Private Access Control Tokens (PACT) initiative [80] extends this consolidation from device root-of-trust infrastructure to issuer judgment, introducing a software-anchor variant of anonymous attestation whose Sybil economics and governance remain unresolved (Section 6.4).

**Scope.** This SoK covers client-side anti-automation mechanisms deployed in web browsers. Purely server-side defenses (WAF, TLS fingerprinting, DDoS scrubbing, rate limiting) are excluded as they operate under different economic models. The historical retrospective (Part I) covers 2010–2024. The forward-looking analysis (Part II) covers the Operator Synthesis paradigm as it has emerged in 2024–2025 and as it applies to near-future (2026–2028) defense research. Section 6.5 is a deliberate, explicitly flagged exception to this exclusion: it extends the analysis to passive server-side traffic-artifact continuity specifically because Section 4.3 identifies network-layer behavioral metadata as the defender's only recourse once client-side attestation is cryptographically valid but attacker-controlled, and analyzing that recourse closes a gap this SoK itself opens rather than reopening the excluded server-side category wholesale.

**Scope limitation: the Advanced Persistent Bot threat model.** We distinguish three tiers of adversary capability. (1) **Commodity Bot:** basic scraper scripts, `curl`, standard headless browsers, Puppeteer deployed at low scale. (2) **Sophisticated Automation (Middle Tier):** Puppeteer/Playwright farms with residential proxy integration, anti-detect browser licenses, and aged-profile management. These adversaries achieve effective bypass of probabilistic defenses through engineering investment rather than VLM inference, and their cost structure is dominated by proxy subscriptions ($500–$5,000/month per operator) plus anti-detect browser licensing ($30–$300/month per operator, team plans up to $500/month). The probabilistic defenses of the 2010–2024 era face significant pressure from this middle tier alone — a fact that prior SoKs have understated and that this paper addresses in the degradation analyses of Section 4.2. (3) **Advanced Persistent Bot (APB):** highly-resourced adversaries utilizing VLMs, custom orchestration, and industrial-scale proxy infrastructure, whose cost structure is dominated by VLM inference rather than anti-detect browser licensing. The middle tier establishes a baseline of degradation: VLMs amplify this degradation rather than causing it de novo. Our analysis focuses on VLM adoption as the capability that most severely exacerbates the structural pressure on probabilistic defenses for the top tier of adversaries. Claims about defense "degradation" should be read through this lens: a defense may be substantially degraded for APBs (and, to a lesser extent, for the middle tier) while remaining economically viable against Commodity Bots.

### 1.3 Threat Model: A Three-Axis Framework with Axis C as the Primary Lens

We adopt a three-axis threat model, with Axis C elevated from a supplementary dimension to the central analytical lens:

- **Axis A — Authentication State:** Anonymous (no prior identity assertion) vs. Authenticated (identity established through a credential). Anchored on NIST SP 800-63-3 [65].

- **Axis B — Attack Objective:** Resource Exhaustion/Scraping vs. Account Takeover/Fraud. Anchored on OWASP Automated Threat Handbook [66].

- **Axis C — Attack Vector:** Environmental Forgery (subverting the browser runtime, DOM, and JavaScript APIs from within) vs. **Operator Synthesis** (driving a legitimate unmodified browser from the OS input layer via a VLM or agentic AI system). This is the primary axis of analysis for this SoK.

The quadrant mapping for Axes A and B is as follows:

| | **Anonymous** | **Authenticated** |
|---|---|---|
| **Scraping / Resource Exhaustion** | Quadrant I: Point-in-Time VM,<br>Behavioral Biometrics,<br>Compute-Bound Challenges (auxiliary).<br>[66] | Quadrant III:<br>Session-bound rate limiting,<br>quota enforcement. |
| **Account Takeover / Fraud** | Quadrant II: Stateful Telemetry<br>&nbsp;&nbsp;&nbsp;&nbsp;(login risk scoring),<br>Platform Anonymous Attestation (PATs).<br>[66] | Quadrant IV: Hardware-Anchored<br>&nbsp;&nbsp;&nbsp;&nbsp;Determinism (DBSC,<br>Passkeys, WebAuthn).<br>[65] |

Axis C cuts across all four quadrants. Under Environmental Forgery, the attacker instruments the browser runtime to forge sensor data to a defensive VM. Under Operator Synthesis, the attacker drives an unmodified stock browser via OS-level accessibility APIs or GUI automation. The distinction is not a minor implementation detail: the defender's historical assumption — that the attacker must subvert the browser — no longer holds for the most capable adversary class. However, as Sections 4.1 and 5.2 show, Operator Synthesis does not create a clean categorical break; it is the most severe escalation within the Environmental Forgery paradigm, and the same cat-and-mouse dynamics continue at new layers (container-evasion, kinematic-smoothing, chronometric profiling).

### 1.4 Operator Synthesis as the Central Framing Device

Vision-Language Models (VLMs) — GPT-4o, Claude Computer Use, Gemini 2.0, and the agentic frameworks built atop them (WebVoyager, CUA, Operator) — introduce a qualitatively distinct attack vector for the Advanced Persistent Bot (APB) threat model, representing the most severe escalation within the Environmental Forgery paradigm. A VLM operating in a virtual machine environment can "see" the rendered browser via screen capture and "act" through synthesized mouse and keyboard events. Critically:

1. **The browser is legitimate.** The VLM does not need to instrument the DOM, forge `navigator` properties, subvert WebGL rendering, or bypass chronometric traps. It drives an unmodified Chrome, Firefox, or Safari instance exactly as a human would.

2. **The motor control is an emergent property with a critical orchestration dependency.** VLMs are trained on web-scale human demonstrations of computer use. The coordinate outputs, action selections, and timing distributions they generate draw from the same distribution as human operators — they do not require a separately trained GAN for trajectory generation. However, a critical engineering gap exists between VLM output and OS-level input. Frontier VLMs output text, JSON bounding boxes, or structured action specifications; they do not natively generate raw OS-level hardware interrupts, mouse event streams, or keyboard scancodes. An orchestration layer — PyAutoGUI, Puppeteer, Apple accessibility APIs, or a custom agentic wrapper — must translate the VLM's coordinate selection into a concrete kinematic trajectory (e.g., a Bezier curve from the cursor's current position to the target coordinate). If this orchestration layer uses naive linear interpolation, constant-velocity profiles, or generic ease-in/ease-out curves, the resulting mouse kinematics remain statistically distinguishable from human movement, and behavioral biometrics (Type III) retain detection leverage *even when the VLM's cognitive task selection is correct*. The attacker must invest additional engineering effort — a kinematic-smoothing layer, gaze-informed trajectory planning, or hardware-backed input synthesis — to close this gap. Motor control is not a turnkey property of the VLM; it is a property that the attacker must instantiate through a non-trivial orchestration pipeline, and the quality of that instantiation directly determines whether L1b detection remains viable.

3. **The asymmetry is inverted.** In the traditional model, the defender executes code in an environment the attacker owns. Under Operator Synthesis, the attacker's browser environment is *legitimate* from the perspective of the JavaScript runtime. The defender's code executes in an environment that passes the principal integrity checks, because no DOM-level or runtime-level instrumentation has occurred. However, as Sections 4.1 and 5.1 discuss, industrial-scale VLM deployment introduces environmental artifacts at the OS and network layers that a sophisticated defender can still detect.

This paper treats Operator Synthesis as the central framing device, not a future concern or a supplementary analysis section. Every architecture evaluated in Part I is assessed through the lens of Operator Synthesis. The resilience tiers established in Section 4 apply consistently across all evaluated paradigms. We use "Operator Synthesis" and "VLM-based attack" interchangeably throughout, acknowledging that the attack vector does not constitute a clean categorical break from prior Environmental Forgery paradigms but represents its most severe escalation for the APB threat model.

---

## 2. Background and Related Work

### 2.1 A Brief History of Client-Side Anti-Automation

The history of client-side anti-automation can be divided into five overlapping eras:

**Pre-2005: Server-Side Heuristics.** Bot detection through IP reputation, request rate analysis, and User-Agent header inspection. No client-side execution.

**2005–2012: The CAPTCHA Era.** Text-distortion, image-recognition, and audio CAPTCHAs tested human perceptual ability [68, 70]. OCR and CNN-based solvers progressively eroded CAPTCHA effectiveness. CAPTCHA-solving farms emerged as economic bypass mechanisms (∼$1 per 1,000 solved CAPTCHAs) [51]. By 2014, Google's systems solved 99.8% of reCAPTCHA challenges [70]. Visual CAPTCHAs remain in production as fallback escalation paths (Arkose Labs, hCaptcha), but ceased to be the standalone frontier of defense.

**2010–2017: The JavaScript Challenge Era.** reCAPTCHA v2's "I'm not a robot" checkbox and Cloudflare's JS challenge pages shifted the defense to testing JavaScript execution capability. Headless browser automation (PhantomJS, Puppeteer, Selenium) rapidly closed this gap.

**2017–2020: VM-Based Attestation.** Custom register-based JavaScript VMs (Google Botguard, Kasada) executing encrypted bytecode defined the next escalation. The adversary must execute the defender's VM faithfully in an environment that looks like a real browser, within strict timing constraints, while the VM continuously mutates its own code [24, 60].

**2020–Present: Diversification and the VLM Paradigm Shift.** Four parallel developments define the present landscape: (a) stateful behavioral telemetry (reCAPTCHA v3, DataDome); (b) behavioral biometrics and sensor telemetry [15, 16, 20]; (c) anonymous attestation protocols (Privacy Pass, PATs, and — from 2026 — Private Access Control Tokens) [38, 44, 45, 80]; (d) hardware-anchored session determinism (DBSC) [36, 37]. The 2024 emergence of production VLMs introduced Operator Synthesis as a fifth development that retroactively reclassifies (a) and (b) as structurally bypassed for the APB threat model — a critical scope qualifier that prior discussion has sometimes omitted.

### 2.2 From CAPTCHAs to JavaScript VMs

The transition from CAPTCHAs to VM-based attestation represents a shift from proving *humanness* through task completion to proving *environmental integrity* — that the JavaScript runtime, DOM, WebGL, and timer APIs behave as they would in a legitimate browser [24, 6]. The canonical fingerprinting survey by Laperdrix et al. [6] catalogs the breadth of the measurement surface. The defense does not need any single measurement to be unforgeable; it needs the *set* of measurements to be jointly difficult to forge consistently. This is the forgery problem at the architectural level.

### 2.3 From Probabilistic Scoring to Hardware-Anchored Determinism

Probabilistic defenses (VM attestation, behavioral telemetry) produce confidence scores derived from noisy sensor data. Deterministic defenses (FIDO2/WebAuthn, DBSC) produce cryptographic proof of hardware key possession [31, 65]. The non-substitutability follows from the NIST Digital Identity Guidelines [65]: deterministic architectures require prior enrollment and cannot screen anonymous traffic.

Privacy Pass [41] and Apple PATs [44] introduced a third category: *deterministic attestation of anonymous traffic*, bridging the "Anonymous Authentication Gap" through cryptographic protocols (VOPRF with DLEQ proofs, RSA blind signatures) [38, 39, 40]. However, as Section 6 details, this closure comes at the cost of vendor centralization. The 2026 Private Access Control Tokens (PACT) initiative [80] complicates this category in a direction central to this SoK: it demonstrates that the category is not inherently hardware-anchored. PACT, announced by Cloudflare with Mozilla, Google, Microsoft, and Shopify, extends Privacy Pass to attest personhood or account standing through *issuer judgment* — active subscriptions, account standing, or issuer vouching — rather than device hardware [81, 84]. As Sections 4.2 and 6.4 show, the anchor choice determines both the architecture's resilience tier under Operator Synthesis and its centralization profile.

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

**Date Range.** Primary: 2010–2025; backward snowballing for foundational works (Saltzer and Schroeder 1975, Anderson 2006). Forward snowballing (citation tracking) on key references ensured coverage of recent work building on the canonical corpus.

**Inclusion Criteria.** (a) Production deployment by a major vendor, (b) architectural documentation in academic literature, IETF/W3C standards, or verifiable grey literature, (c) cost imposition on adversaries through client-side execution.

**Exclusion Criteria.** (1) Purely theoretical proposals without production deployment or verifiable prototype evaluation. (2) Server-side-only defenses operating without client-side execution (WAFs, TLS fingerprinting without browser-level interrogation). (3) Commercial marketing materials lacking architectural documentation. (4) Duplicate entries cut during deduplication across the six databases.

**Deduplication and Screening.** Initial search across six databases yielded approximately 230 unique items. Title and abstract screening against inclusion/exclusion criteria reduced the corpus to 95 publications. Full-text architectural assessment eliminated 17 publications that lacked sufficient mechanism-level documentation for taxonomic classification, leaving the final corpus of 78 publications, subsequently expanded to 85 references through additions for agentic web-navigation frameworks, SDK-proxy network research, and the Private Access Control Tokens (PACT) initiative.

**Grey Literature Quality Assessment.** Grey literature items (vendor whitepapers, malware analysis reports) were included only when architectural claims were independently verifiable through (a) cross-referencing with academic publications describing the same mechanism, (b) consistency across multiple independent grey-literature sources, or (c) the mechanism being publicly documented in IETF/W3C standards and the grey-literature source providing supplementary architectural detail.

**Source Corpus.** 85 references: 57 academic papers, 10 standards and RFCs, and 18 grey-literature items (vendor whitepapers, threat-intelligence reports, preprints, and blog posts). Section 6.5's server-side companion discussion draws on a supplementary set of 14 references [86]–[99] — TLS/TCP/HTTP passive-fingerprinting tooling and standards, plus two self-citations to the author's own published essays — added *outside* this systematic search process specifically to support the flagged scope exception described in Section 1.2; they were not subject to the deduplication and screening process above, and Section 6.5 states this explicitly. Including this supplement, the full reference list totals 99: 58 academic papers, 15 standards and RFCs, and 26 grey-literature items.

### 3.2 Five Architectural Types by Mechanism

We identify five architecturally distinct classes of client-side anti-automation. These types are distinguished by their *primary mechanism*: Execution (probing the runtime through code execution), Telemetry (passive accumulation of behavioral/sensor data), or Cryptographic Binding (hardware-anchored deterministic proof). Real production systems inevitably fuse mechanisms from multiple types (Section 3.3). The following vendor-mechanism matrix maps representative systems to their constituent mechanisms:

| System | Execution | Telemetry | Cryptographic Binding | Primary Mechanism |
|--------|-----------|-----------|----------------------|-------------------|
| Google Botguard | ✓ | | | Execution |
| Turnstile | ✓ | ✓ | | Execution |
| reCAPTCHA v3 | ✓ | ✓ | | Telemetry (with Execution auxiliary) |
| DataDome | | ✓ | | Telemetry |
| Arkose Labs | ✓ | ✓ | | Telemetry |
| Apple PATs | | | ✓ | Cryptographic Binding |
| Privacy Pass | | | ✓ | Cryptographic Binding |
| DBSC | | | ✓ | Cryptographic Binding |
| Passkeys/WebAuthn | | | ✓ | Cryptographic Binding |

**Type I: Point-in-Time VM Attestation.** Executes a custom register-based JavaScript VM within the browser. Measures environmental integrity (L1), uses self-modifying opcodes (L2), anti-introspection traps (L3), and chronometric constraints (L4). Produces a bearer token [73, 74]. Cost imposed: per-execution proxy bandwidth, fixed RE investment, recurring temporal cost per compile rotation. Structural ceiling under Environmental Forgery: IP reputation market exhaustion. Under Operator Synthesis: L1 and L4 detection premises shift rather than collapse — L1a shifts to container-evasion artifacts, L1b shifts to kinematic-orchestration quality, L4 shifts from microsecond instrumentation detection to second-scale latency profiling (Section 5.2). L2/L3 become black-boxed at the VM level. IP reputation remains the sole binding economic constraint, but significantly weakened. Representative systems: Google Botguard, Cloudflare Turnstile Managed Challenge, Kasada.

**Type II: Stateful Behavioral Telemetry.** Accumulates long-term behavioral profiles using persistent identifiers (cookies, fingerprinting). Scores mouse movements, scroll patterns, navigation cadence, and dwell time over weeks to months. Cost imposed: conjunctive stack of proxy + aged profile + anti-detect software license [13, 58]. Structural ceiling under Environmental Forgery: profile-aging latency (cannot be bypassed by spending). Under Operator Synthesis: the VLM inherits the legitimate browser's profile, collapsing the aging requirement. Representative systems: reCAPTCHA v3, DataDome, Human Security (PerimeterX).

**Type III: Behavioral Biometrics & Sensor Telemetry.** Measures mouse kinematics (velocity, acceleration, Bezier-curve fitting), scroll patterns, click-timing, touch pressure, accelerometer polling [15, 20]. Cost imposed under Environmental Forgery: `min(Cost_ML_Inference, Cost_Human_Labor)`, where human labor (CAPTCHA-solving farms at ∼$1/1K challenges [51]) sets the global cost floor. Under Operator Synthesis: the VLM's emergent cognitive selection of visual targets bypasses the behavioral model's prediction of interaction targets. However, as Section 1.4 details, VLMs output coordinate selections, not kinematic trajectories — a separate orchestration layer must translate coordinates into mouse movement. If that orchestration uses naive linear interpolation or constant-velocity profiles, the resulting kinematics remain statistically distinguishable from human movement, and behavioral biometrics (L1b) retain detection leverage (Tier 2/3 in Section 4.2).

**Type IV: Platform/OS-Level Anonymous Attestation (Privacy Pass / PATs / PACT).** Cryptographic anonymous tokens (RSA blind signatures, VOPRF) issued by a platform or third-party issuer. The anchor may be hardware-backed — device attestation via Secure Enclave/TPM, token issuance rate-limited per-device [43] — or software/contextual, as in the 2026 PACT proposal, where the anchor is issuer judgment of account standing, subscription status, or first-party relationship [80, 81]. Cost imposed (hardware anchor): device compromise through PPI malware [53, 56]; extraction of attestation keys is prohibitively expensive, but proxying through compromised devices is economically viable. Cost imposed (contextual anchor): account acquisition and synthesis (bulk registration, credential stuffing, aged-account purchases, cheap subscriptions), relocating the Sybil problem from device scarcity to credential scarcity (Sections 4.2–4.3). The hardware-anchored variant survives Operator Synthesis (Tier 1) because the cryptographic binding operates independently of browser input modality; the contextual variant does not inherit this property. Representative systems: Apple PATs, Cloudflare/Fastly Privacy Pass issuance, PACT (proposed).

**Type V: Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys).** Cryptographic proof of hardware key possession. DBSC extends this from authentication to session lifetime [36, 37]. Cost imposed: device compromise through PPI malware at $30–$200/month per botnet subscription [56]. Structurally inapplicable to anonymous traffic [65]. Also survives Operator Synthesis (Tier 1). Representative systems: Google DBSC, W3C WebAuthn, Passkeys (Apple, Google, Microsoft).

### 3.3 The Hybrid Reality: Production Systems Fuse Mechanisms

A taxonomy that cannot cleanly classify the three most prominent production systems — Cloudflare Turnstile, DataDome, and Arkose Labs — without immediately resorting to "hybrid" exceptions has limited diagnostic value unless the hybrid nature is acknowledged from the outset.

Cloudflare Turnstile uses a JavaScript VM challenge as the *delivery mechanism* for stateful telemetry collection. The VM does not merely measure the environment; it establishes a persistent session that feeds a behavioral scoring engine. Turnstile is simultaneously Type I (point-in-time VM attestation) and Type II (stateful behavioral telemetry), with the VM serving as the instrumentation layer for the telemetry [60].

DataDome similarly fuses Type II (stateful profile accumulation) with Type III (mouse kinematics and behavioral biometrics), using one to bootstrap the other when profile data is insufficient [64].

Arkose Labs deploys visual-interactive challenges (Type I auxiliary) as a fallback escalation when its probabilistic scoring (Type II/III fusion) is inconclusive.

These are not edge cases or implementation flaws. They are evidence that the industry converged on hybrid architectures because each pure architectural type has a well-understood structural weakness that a complementary type can partially mitigate. The taxonomy's value is not in achieving clean classification of every system, but in providing the *analytical vocabulary* to identify which mechanisms a hybrid system combines and which attack vectors remain exposed.

In this SoK, we classify each system by the mechanism that most closely describes its *binding structural ceiling*: the constraint that limits the adversary's throughput regardless of hybridization. For Turnstile, the binding constraint remains IP reputation (Execution mechanism), even though behavioral telemetry (Telemetry mechanism) provides supplementary signal.

### 3.4 The L1–L4 Diagnostic Framework

The L1–L4 framework described here is derived from the defense-in-depth architecture observed in Google's Botguard VM [24]. We generalize it as a *historical diagnostic framework* applicable to any point-in-time VM attestation system — not as a prescriptive architecture for future defenses. The framework's value today is diagnostic: it reveals *how* each defensive layer's cost burden shifts under Operator Synthesis, and which layers retain detection leverage that the initial VLM literature has overlooked. We present it in vendor-neutral terms while acknowledging that the precise instantiation of each layer varies across implementations.

Under Environmental Forgery, each layer imposes a cost because the attacker must instrument or subvert the browser to forge sensor data. Under Operator Synthesis, the adversary drives a legitimate unmodified browser at the JavaScript runtime level, so the *instrumentation-detection* premise of each layer collapses. However — and this is the critical nuance that Sections 4 and 5 develop in detail — the costs do not simply vanish to zero. They *shift* to new attack surfaces: the orchestration layer between VLM output and OS input, the containerization stack required for industrial-scale deployment, and the temporal latency of VLM inference itself. Each layer's cost under Operator Synthesis is therefore non-zero but *qualitatively different* from its cost under Environmental Forgery. Specifically:

- **L1a (Static Environmental Introspection)** — Detects forged `navigator` properties, WebGL artifacts, DOM prototype chain integrity violations [6]. Under OS at the browser level: properties are inherited from a legitimate browser. However, industrial-scale VLM deployment requires containerized environments (Docker, K8s) that bleed environmental anomalies — missing system fonts, WebGL rendering mismatches versus the User-Agent's declared OS, anomalous TCP/IP stack fingerprints. The attacker must invest in container-evasion engineering (Section 4.1).
- **L1b (Dynamic Sensor Telemetry)** — Measures mouse kinematics, scroll patterns, click-timing against human-distribution models [15, 20]. Under OS at the cognitive level: VLM motor planning is emergent from web-scale human-demonstration training. However, VLMs output coordinate selections, not kinematic trajectories. An orchestration layer must translate coordinates into mouse movement, and naive interpolation produces detectable kinematic artifacts. The attacker must invest in kinematic-smoothing orchestration (Section 1.4).
- **L2 (Code Obfuscation, Polymorphism)** — Self-modifying opcodes, compile rotation raise RE cost [24, 27]. Under OS: the VLM never inspects bytecode — executes the VM as a black box. T_RE ≈ 0 at the VM level. However, application-level DOM and workflow reverse-engineering is still required (Section 5.5).
- **L3 (Execution Traps)** — Console-bound traps, anti-debugger hooks, prototype integrity checks [24]. Under OS at the JS/DevTools level: no DevTools opened, no runtime instrumented — traps are never triggered. However, under Operator Synthesis, L3's detection premise shifts to the **Cognitive/Perceptual Layer**: the gap between what the rendered DOM exposes to agentic frameworks and what the human visual system perceives. Frameworks that traverse the DOM tree for action selection (SeeAct's text-based affordance enumeration [79], CogAgent's CogTool grounding) treat all rendered elements as interactable, including elements the human eye never registers. A defender can exploit this by deploying *Cognitive Honeypots*: a full-viewport transparent `<div>` (`position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.001)`) containing a decoy element at valid page coordinates. The decoy reports non-zero `getBoundingClientRect()` dimensions and passes DOM presence checks, but is visually imperceptible to a human. A VLM orchestrator using DOM-based element enumeration may select the decoy, triggering the defensive action (session blacklisting, telemetry flagging). This trap succeeds specifically against DOM-enumerating agentic frameworks (Tier 2/3 degradation per Section 4.2); pixel-level VLMs (GPT-4o CUA, Claude Computer Use) are immune since they operate on screenshots only, requiring a multi-surface attack for full coverage. The attacker must invest in visual-grounding validation — cross-referencing DOM targets against screenshot crops before selecting — to avoid honeypot activation. The cost shifts from anti-trap-evasion at the bytecode layer to perceptual-DOM alignment engineering at the orchestration layer.
- **L4 (Chronometric Integrity)** — `performance.now()` polling and timing-delta-based seed mutation [24, 5]. Under OS at the microsecond instrumentation level: native execution introduces no timing deviation. However, Section 5.2 identifies that L4's detection premise can be *extended*: the macroscopic latency of VLM inference (5–15 seconds per action) versus human total challenge completion time (2–5 seconds) creates a 5–10× timing gap that a sophisticated defender can exploit.

**Revised Diagnostic Summary.**

| Layer | Cost Type (EF) | Cost Under OS | Nature of Shift |
|-------|----------------|---------------|-----------------|
| L1a | Variable (compute for forgery) | Shifted to container-evasion engineering | Not zero; moved from browser forgery to deployment-environment mimicry |
| L1b | Variable (ML inference or labor) | Shifted to kinematic-smoothing orchestration | Not zero; moved from trajectory generation to orchestration-layer quality assurance |
| L2 | Temporal (RE per compile rotation) | Near-zero at VM level; shifted to app-level workflow RE | VM bytecode black-boxed; DOM-level prompt engineering remains |
| L3 | Mixed (trap identification + overhead) | Shifted to perceptual-DOM alignment | Not zero; moved from DevTools-trap evasion to perceptual-DOM alignment engineering (Section 4.2) |
| L4 | Variable (timer synchronization) | Shifted to latency-evasion at inference timescale | Microsecond instrumentation gap closed; second-scale inference gap opened |

The diagnostic value of the L1–L4 framework under Operator Synthesis is not that the stack collapses to zero cost — it is that the *nature* of the cost imposed on the attacker shifts from browser-instrumentation forgery to systems-integration engineering. Defenses rooted in L1a, L1b, and L4 do not vanish; they transform into detection surfaces at the orchestration and deployment layers, which remain exploitable by a sophisticated defender.

### 3.5 The Temporal Arms Race: A Historical Case Study

The temporal arms race between AST obfuscators and symbolic execution engines — documented in prior work [24] — pitted compile rotation (`T_Life`) against the attacker's reverse-engineering pipeline (`T_RE`) measured via automated tools (Syntia [26], DOBF [28]). The tipping point `T_RE < T_Life` was approaching for the best-defended VMs. Under Operator Synthesis, this race terminates at the VM level: the attacker never inspects the defensive bytecode, black-boxing the obfuscation layer entirely. The wider lesson: software-only obfuscation has a structural ceiling — it cannot impose cost against an adversary who bypasses the inspection step. However, application-level workflow RE (Section 5.5) restores a distinct, cheaper temporal constraint at the DOM layer.

---

## 4. PART II: The VLM/Operator Synthesis Attack Vector

*This section analyzes the Operator Synthesis attack vector for the APB threat model and establishes a forward-looking research agenda for VLM-resilient anti-automation. Consistent with the scope limitation in Section 1.2, claims of "degradation" or "bypass" refer to structural vulnerability against this top-tier adversary class, not universal invalidation of probabilistic defenses. The middle tier of sophisticated non-VLM automation (Puppeteer/Playwright farms) independently imposes pressure on probabilistic defenses without VLM inference; our analysis treats VLM adoption as the capability that most severely exacerbates this pressure.*

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

This is not a marginal improvement in attack capability for its target threat model — it represents a significant escalation in the cost curve. The attacker's browser is not a compromised browser; it is a browser being used exactly as designed, but by a synthetic operator through a deployment stack that introduces detectable artifacts at scale. The middle tier of sophisticated non-VLM automation (Section 1.2) already imposes substantial pressure on probabilistic defenses through conventional anti-detect browsers; Operator Synthesis amplifies this pressure by removing the environmental-forgery cost component that was the binding constraint on middle-tier adversaries.

### 4.2 Architecture-by-Architecture Collapse Under Operator Synthesis

**Type I (Point-in-Time VM Attestation) → Degraded to Tier 2.** L1–L4 cease to impose meaningful costs. IP reputation remains as the sole binding economic constraint, but without the multiplicative cost of environmental forgery, the effective per-token cost drops substantially (Section 5.3). The VM becomes a delivery mechanism rather than a defense — it delivers the challenge, but the challenge imposes no forgery cost.

**Type II (Stateful Behavioral Telemetry) → Degraded to Tier 2/3 (Profile-aging constraint lifted; state-orchestration cost substituted).** The VLM can generate human-like behavior from a fresh browser instance with no aging penalty — lifting the profile-aging latency constraint that was the structural ceiling under Environmental Forgery. However, a critical nuance applies: VLMs are stateless between inference calls unless explicitly orchestrated. Maintaining, isolating, and rotating aged cookie jars, local storage snapshots, and IndexedDB state across thousands of parallel VLM instances without cross-contamination is a non-trivial orchestration problem. Each parallel session requires an isolated browser profile, a persistent cookie store, and clean session state — and the cost of managing this infrastructure at scale substitutes for the anti-detect browser license that Environmental Forgery required. The profile-aging *latency* constraint collapses, but a state-orchestration *complexity* and *infrastructure* cost replaces it. This shifts Type II from a latency-bound problem to an operations-bound problem, which is a meaningful degradation but not a disappearance of defense-imposed cost.

**Type III (Behavioral Biometrics & Sensor Telemetry) → Degraded to Tier 2/3 (Cognitive selection bypassed; kinematic instantiation gap remains).** The VLM's cognitive ability to locate visual targets and output coordinate selections is emergent from vision-language training on human demonstrations. However, as discussed in Section 1.4, the VLM does not natively produce the kinematic trajectory between those coordinates — an orchestration layer translates the VLM's coordinate output into mouse movement. If the orchestration layer uses naive linear interpolation, constant-velocity profiles, or generic ease-in/ease-out curves, the resulting mouse kinematics remain statistically distinguishable from the smooth, biologically-motivated acceleration profiles of human movement. Behavioral biometrics (L1b) retain detection leverage against poorly-implemented orchestration. Sophisticated attackers will invest in a kinematic-smoothing layer (adaptive Bezier trajectory generation with human-derived acceleration profiles) to close this gap, but this adds engineering cost that the "structurally bypassed" framing understates. The detection premise shifts from "the VLM cannot produce human-like interactions" to "the VLM can produce human-like interactions only if the orchestration layer correctly implements human motor kinematics," which is a substantively different and narrower attack surface than full collapse.

**Type IV (Anonymous Attestation / PATs) → Tier 1 (Structurally Resilient) — for the hardware-anchored variant.** The cryptographic binding is to device hardware, not to browser input modality. Whether the browser is driven by a human or a VLM is irrelevant to the attestation protocol. The attacker must compromise the device to extract attestation keys, which is a separate attack chain (PPI malware, physical access) with its own economic ceiling [56]. This classification does not extend to software-anchored variants of the category. The 2026 PACT proposal [80] binds attestation to issuer judgment of account standing rather than to device hardware: the unit of scarcity becomes the credentialed account, and account acquisition — bulk registration, credential stuffing, aged-account purchases, subsidized subscriptions — is automatable at costs the APB threat model can absorb (Section 4.3). PACT's design also assigns the browser the role of trusted user-agent mediating credential storage, issuer selection, and challenge budgets [81] — an assumption that fails precisely under Operator Synthesis, where the browser profile, the device, or both are under attacker control, and where a copied or compromised profile can exercise the same issuance APIs as a legitimate user [81, 83].

**Type V (Hardware-Anchored Determinism / DBSC) → Tier 1 (Structurally Resilient).** Same logic as Type IV: the cryptographic proof of hardware key possession is input- modality-independent. The session cookie is bound to the TPM/Secure Enclave regardless of how the browser is driven.

**VLM Resilience Tier Ranking (Operator Synthesis Resistance Only).**

The tiers below measure resilience specifically against Operator Synthesis — that is, whether the detection mechanism is input-modality-dependent. They do not measure total defense strength: Type IV and Type V face additional attack chains (device compromise, SDK proxying) that are independent of Operator Synthesis and whose economics are analyzed separately in Section 4.3.

| Tier | Definition | Types | Degradation Mechanism |
|------|------------|-------|-----------------------|
| 1 | Structurally resilient *against Operator Synthesis* | Type IV (PATs, hardware-anchored), Type V (DBSC/Passkeys) | Cryptographic binding independent of input modality; VLM cannot forge attestation keys. Device compromise and SDK-proxying are orthogonal attack chains (Section 4.3). |
| 2 | Degraded — cost-shifted | Type I (VM Attestation), Type III (Behavioral Biometrics) | Detection premise substantially weakened at cognitive level; residual costs from container-evasion (Type I) or kinematic orchestration (Type III) remain |
| 2/3 | Degraded — cost-shifted with operational substitution | Type II (Stateful Telemetry) | Profile-aging latency constraint lifted; state-orchestration complexity and infrastructure cost partially substitutes |

The Tier 1 classification of Type IV applies to the hardware-anchored variant (Apple PATs). Software-anchored Type IV variants such as PACT [80] do not qualify: their binding is issuer judgment rather than cryptographic hardware possession, and their Sybil economics degrade to account acquisition (Section 4.2, Type IV; Section 4.3).

### 4.3 What Survives: Tier 1 Architectures and Their Structural Limits

Tier 1 architectures survive because they anchor security in hardware rather than in probabilistic detection of behavioral signals. However, survival is not immunity. Each Tier 1 architecture has a structural limit:

**PATs (Type IV): The device compromise ceiling.** PATs are resilient against Operator Synthesis, but the attacker can still bypass them by compromising the device. PPI malware networks provide device access at $30–$200/month per botnet (with dark-web market prices documented up to $4,800/month for premium botnets), with per-infection costs as low as $0.10–$0.50 for high-volume operations [53, 56]. The economic ceiling is the black-market price of a successful infection — not the mathematical hardness of the VOPRF protocol, but the market equilibrium of the malware supply chain. Additionally, PAT issuance is rate-limited per device [43], which caps throughput even for compromised devices.

Crucially, the device-compromise ceiling is not limited to criminal malware. SDK-based residential proxy networks (Bright Data, the former Hola network, and various mobile-proxy SDKs) operate in a legal gray area: end users consent to installing free applications (mobile games, utilities, VPNs) that embed proxying SDKs, routing traffic through the user's legitimate device [76]. On Android, such SDKs with user-granted permissions can interact with the Keystore and potentially generate valid attestations; on iOS, PAT attestation routes through DeviceCheck/AppAttest APIs which require per-session user consent and are not transparently accessible to third-party SDKs — the SDK must prompt the user through a consent flow or exploit application-level permissions, making the bypass more constrained than on Android but still economically viable at scale. The supply elasticity of SDK-proxied devices is orders of magnitude higher than PPI botnets — Bright Data alone claims access to tens of millions of residential IPs across 195+ countries — and the marginal cost per attested device is effectively zero once the SDK is deployed. This drastically lowers the effective bypass ceiling for PATs below the black-market PPI pricing that prior work assumes. A defender relying on PATs must recognize that the relevant threat is not exclusively the $30–$200/month botnet subscription but also the commoditized SDK proxy market that routes through legitimate consented devices at significantly lower cost.

When PAT attestations arrive from SDK-proxied devices — which present perfectly valid cryptographic proof from uncompromised hardware — the defender cannot distinguish them from legitimate traffic at the attestation layer. The defender's only recourse is to fall back to *network-layer behavioral metadata*: ASN reputation scoring, IP-to-Account cardinality analysis, velocity and rate-limiting heuristics, and cross-session pattern matching. These server-side signals, long demoted as legacy defenses in the hardware-attestation literature, re-emerge as the critical complement to cryptographically valid but attacker-controlled attestations. This observation ties the hardware-attestation critique directly to the necessity of maintaining server-side stateful analysis even — and especially — when client-side cryptographic attestation has been successfully weaponized.

**The software-anchor ceiling: token farming.** PACT-style contextual anchors replace the device-compromise ceiling with an account-acquisition ceiling (Sections 4.2, 6.4). If the issuer's admission signal is an active subscription, account standing, or a first-party relationship, the attacker's unit of scarcity becomes a credentialed account: bulk registration, credential stuffing, stolen session tokens, and cheap subscriptions are all automatable inputs to a token-farming pipeline upstream of the attestation protocol [83]. The cryptographic layer does not prevent polluted tokens from entering circulation — it only prevents certain kinds of linkability [85] — so verifier-side rate limiting of redemption remains necessary regardless of anchor type [83, 85]. The defender's position parallels the SDK-proxy analysis above: attestations issued against farmed accounts are cryptographically indistinguishable from legitimate attestations at the protocol layer, and the recourse is again network-layer behavioral metadata. The anchor choice therefore determines which black-market price constitutes the ceiling — device infection or account acquisition — and both are market prices, not security parameters.

**DBSC/Passkeys (Type V): The post-authentication session ceiling.** DBSC prevents cookie theft across devices, but a compromised device exports both the session state and the bound key simultaneously. Tarrach et al. [33] identified message integrity gaps accessible to browser extensions. Kuchhal et al. [32] found only 4.4% of authenticators carry Level 2+ malware resistance certification. The structural limit is not the cryptographic protocol but the practical difficulty of guaranteeing the integrity of the key-storage environment.

**The universal ceiling: supply-chain economics.** Both Tier 1 architectures ultimately depend on the cost of device compromise. This cost is not determined by the protocol design but by the malware supply chain market [56], the effectiveness of OS-level security mitigations (iOS hardened runtime, Android KeyStore, Windows Credential Guard), and the user's security posture. Every Tier 1 architecture has an economic ceiling below which it deters adversaries and above which it does not.

### 4.4 The False Dichotomy: Why PATs Are Not a Silver Bullet

A naive reading of Section 4.2 might suggest that PATs and DBSC represent a complete solution: deploy PATs for anonymous traffic, deploy DBSC for authenticated sessions, and the anti-automation problem is solved. This is structurally incorrect for three reasons.

**1. PATs require platform-level coordination.** PAT issuance requires the OS vendor (Apple, Google, Microsoft) to operate an issuer or authorize a third-party issuer. This creates a dependency on vendor participation that is not guaranteed for all platforms, all regions, or all use cases. A web origin cannot deploy PATs independently; it must integrate with a platform-level attestation infrastructure.

**2. PATs shift the trust problem rather than solving it.** Pre-PATs, the trust question was: "Can I distinguish human from automated traffic?" Post-PATs, the trust question becomes: "Do I trust Apple/Google/Microsoft's attestation infrastructure more than probabilistic detection?" For many defenders, the answer is yes, but this is an economic and political judgment, not a technical guarantee. The attestation infrastructure is controlled by three US-based corporations, each operating its own advertising business with incentives that may diverge from those of the web origin consuming the attestation.

**3. PATs create a two-tier accessibility surface.** If VLMs structurally bypass probabilistic defenses, and PATs provide the only viable path for deterministic anonymous attestation, then any web origin that deploys PAT-only anti-automation effectively requires users to have a PAT-compatible device (iOS 16+/macOS Ventura+ for Apple PATs; Android-compatible Privacy Pass for Google). This creates an accessibility barrier that is structurally regressive.

**The software-anchor response and its limits.** The PACT initiative [80] is best read as the industry's own acknowledgment of these three limitations — in particular the platform-coordination dependency of reason 1 — but it does not resolve them. PACT broadens the issuer set beyond OS vendors to any party that "knows something about the user" — identity providers, subscription services, e-commerce platforms [80, 81] — which addresses reason 1 only by multiplying the parties whose judgment becomes security-critical. Reason 2 intensifies in a different form: the trust question becomes "Do I trust Cloudflare's or any accredited issuer's admission process more than probabilistic detection?" and, as Section 6.4 details, no accreditation, revocation, or audit regime for issuers has been specified [80, 83]. Reason 3 likewise intensifies: if issuers anchor on financial or account-standing signals, the accessibility barrier is no longer device ownership but *consumer status* — unbanked, low-income, and anonymity-seeking users may have no usable issuer relationship at all [84]. The CAPTCHA that PACT replaces could at least be solved without proving consumer status; a subscription-anchored token cannot.

---

## 5. A Structured Cost-Accounting Exercise for VLM-Driven Attacks

*This section provides a structured cost-accounting exercise for reasoning about the economics of Operator Synthesis attacks. We do not claim to have discovered a predictive economic model of VLM-based attack — the market is too young and the data too sparse, and our exercise tallies costs without deriving supply/demand equilibria or utility functions that could predict attacker behavior. We instead provide a structured cost-accounting exercise for reasoning about attacker costs, identify the empirical gaps that prevent precise quantification, and set a research agenda for closing those gaps. Where we offer equations, they are accounting identities (quantity × price) not economic models — they organize cost categories but do not predict outcomes. We approach prior work's economic framing with respect: the conjunctive cost models of Section 3 and prior SoKs [6, 24] correctly identified the multi-constraint nature of anti-automation bypass, and our contribution is to extend that framing to the Operator Synthesis paradigm, not to dismiss the foundation.*

### 5.1 VLM Inference Cost Under Operator Synthesis

The primary variable cost of an Operator Synthesis attack is VLM inference. Prior conjunctive cost models [24, 47] correctly identified the multi-cost structure of Environmental Forgery — proxy IPs, anti-detect software, profile aging. Under Operator Synthesis, VLM inference is an *additional necessary* cost for any attack that requires visual perception of rendered browser content, supplementing rather than supplanting the proxy and state-orchestration components of prior models.

**Base cost-accounting equation.** The per-task inference cost is:

```text
C_inference = (t_input × p_input + t_output × p_output) × r_per_token
```

Where:

- `t_input` = input tokens per task (screen capture encoding + prompt context)
- `t_output` = output tokens per task (action selection + coordinate generation)
- `p_input` = input token price (model-dependent, $1.25–$5.00 per million tokens for frontier models as of Q1 2026)
- `p_output` = output token price (model-dependent, $5.00–$20.00 per million tokens)
- `r_per_token` = amortized compute overhead per token (batch processing, caching, API latency)

**Modeling failure rates.** The base cost model assumes 100% task completion, which does not hold in practice. VLMs hallucinate, select incorrect bounding boxes, enter navigation loops, and time out on dynamic DOM elements that confuse their spatial mapping. The effective cost per successful bypass must incorporate the task success probability:

```text
C_effective = C_inference / P(success) + C_retry × (1 - P(success)) / P(success)
```

Where `P(success)` is the per-attempt probability of producing a valid bypass token. A VLM with a 60% per-task success rate — consistent with reported agentic benchmarking on complex multi-step flows [77, 78] — faces an effective cost multiplier of 1.67×; at 40% success, the multiplier reaches 2.5×. Error recovery adds further cost: each failed attempt consumes the same inference budget as the original attempt, and the model may require additional context tokens to diagnose the failure and re-plan, increasing `t_input` on retry attempts. At industrial scale, even a 10-percentage-point difference in `P(success)` yields a meaningful cost differential: for a $0.05 nominal per-token cost, a 40% vs. 70% success rate shifts the effective cost from $0.125 to $0.071 — a 43% difference that directly determines whether the attack is economically viable against a given defender's token lifetime.

The dependence of `P(success)` on task complexity introduces a testable empirical prediction: defenses that increase perceptual ambiguity (dynamic CSS layouts, canvas obfuscation, adversarial-noise overlays) should reduce VLM task success rates, thereby increasing effective attack costs. This prediction links the economic framework directly to the visual-reasoning deobfuscation gap identified in Section 3.5.

**Empirical baselines (as of Q1 2026).** Published pricing for frontier VLMs:

- GPT-4o (May 2024, legacy): $2.50/M input tokens, $10.00/M output tokens. Current frontier models (GPT-5.4, GPT-5.5) are priced higher with expanded capabilities.
- Claude Sonnet 4.6: $3.00/M input, $15.00/M output. Computer use is available as a tool feature on this model.
- Gemini 2.0 Flash: $0.10/M input, $0.40/M output (general-purpose model; image generation deprecated). For computer-use-capable models, Gemini 2.5 Computer Use Preview is priced at $1.25/M input, $10.00/M output.

For a typical web interaction task requiring one screen capture (∼1,000 tokens) and one action selection (∼500 tokens output), the per-action cost is approximately $0.0025–$0.01. For an attack requiring 10 interactions per token generation (navigating to the target page, waiting for the VM to load, receiving the token), the per-token cost is $0.025–$0.10.

**Scaling properties.** Critically, VLM inference costs follow a *deflationary* trajectory. Each new model generation has historically reduced per-token costs by 2–5× while maintaining or improving capability. Moore's Law for LLM inference predicts sustained cost reduction through:

- Quantization (FP16 → INT4 reduces cost by ∼4×)
- Speculative decoding (2–3× throughput improvement)
- Model distillation (smaller models for specific tasks)
- Inference hardware specialization (TPU v5p, NVIDIA B200, custom ASICs)

This deflation means the cost ceiling of VLM-based attacks is *temporally unstable* — it decreases predictably over time, unlike the relatively stable cost of human labor or residential proxy IPs.

### 5.2 The Latency Cost: Temporal Overhead as a Non-Trivial Attack Surface

The cost exercise in Section 5.1 considers only token-price economics. A second cost dimension — temporal latency — operates independently and can trigger defensive mechanisms that token-price savings do not mitigate. Frontier VLMs typically require 5–15 seconds per inference cycle: screen capture encoding, model inference, and action selection. For multi-step web flows requiring 5–10 interactions per token generation, the per-token wall-clock time is 25–150 seconds.

This latency matters for two reasons:

1. **Chronometric heuristics (L4).** The L4 layer was originally designed to detect microsecond-scale timing deviations introduced by JavaScript instrumentation layers. Under Operator Synthesis, the instrumentation gap closes — no DevTools or debugger introduces timing noise. However, L4's detection premise is not obsolete; its *target shifts*. VLM inference introduces a *macroscopic* timing deviation: a human completes a standard VM challenge in 2–5 seconds of total interaction time (page load + cognitive processing + interaction), while a VLM-driven session requires 25–120 seconds of "think time" between actions (5–15s per inference cycle × 5–10 interactions per token generation). This is not a subtle instrumentation artifact — it is a 5–10× latency gap (or larger for complex multi-step flows) detectable by chronometric heuristics. The VLM's per-action latency is bounded below by model inference speed (~5s minimum for frontier models), while human per-action latency spans a broader, noisier distribution bounded below by reaction time (~100ms for simple interactions, 1–3s for complex decisions). L4 therefore survives under Operator Synthesis: it no longer detects *how* the browser is driven, but it detects *how fast* the operator can perceive and react. This is a qualitatively different and potentially more robust detection surface than the microsecond-precision timing analysis it replaced. The attacker can partially close this gap through model distillation and local deployment (reducing inference latency to 1–3s for domain-specific models), but the shape of the human latency distribution — specifically, its higher variance and the presence of occasional sub-second interactions — remains distinguishable from the more tightly bounded VLM inference distribution.

2. **Session timeout risk.** Web applications impose server-side session timeouts (typically 5–30 minutes for authenticated sessions, 1–5 minutes for anti-automation challenge windows). A VLM with 30s per action on a 10-step flow approaches 5-minute per-session latency, pushing against practical timeout boundaries. Failed sessions due to timeout consume inference budget without producing valid tokens, feeding into the `P(success)` penalty in Section 5.1.

The effective cost per successful token must therefore incorporate temporal overhead:

```text
C_temporal = C_inference + C_bandwidth_per_session + C_timeout_loss
```

Where `C_timeout_loss = C_inference × P(timeout) / (1 - P(timeout))`, representing the expected inference cost from a geometric series of retries prior to success. This temporal overhead is largely orthogonal to the token-price deflation discussed in Section 5.1: model inference speed improvements (speculative decoding, faster hardware) reduce temporal latency, but the gap between human reaction time and VLM inference time will persist for the foreseeable future.

### 5.3 The Proxy Supply Market: Elasticity, Equilibrium, and Exhaustion

Under Environmental Forgery, the proxy supply market was the binding structural constraint. Under Operator Synthesis, the proxy is still required — the VLM must route traffic through residential IPs — but the economics shift because the VLM imposes different demands on the proxy infrastructure.

**Supply elasticity.** Residential proxy markets exhibit a tiered supply structure:

- **Commodity tier:** ∼$1–$6/GB for shared residential IPs with moderate reputation. High elasticity: supply is effectively infinite at this price point. However, reputation is a commons [59]: aggressive usage burns IP reputation across the pool.
- **Premium tier:** ∼$10–$15/GB for exclusive, unburned residential IPs. Low elasticity: supply is constrained by the number of devices in the botnet or proxy network.
- **Enterprise tier:** ∼$25–$50/GB for dedicated IPs with guaranteed clean reputation. Very low elasticity.

For Operator Synthesis attacks, the commodity tier is less usable because the VLM must maintain persistent session state (profiles, cookies) across multiple interactions. A commodity IP rotated per request breaks the session continuity required for stateful applications. The VLM attacker's proxy demand shifts toward the premium and enterprise tiers, which have lower supply elasticity.

**Corrected conjunctive cost model.** Prior work modeled the conjunctive cost of stateful telemetry bypass as: `Cost_proxy + Cost_aged_profile + Cost_software_license`. Under Operator Synthesis, the attacker who drives a stock browser eliminates the anti-detect software license but *substitutes a state-orchestration infrastructure cost*:

```text
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

```text
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

DBSC [36, 37] cryptographically binds session cookies to a device-resident key (TPM/Secure Enclave), with periodic proof-of-possession [75] throughout the session lifetime. This targets the session-hijacking threat model (NIST 800-63 Authenticated/ATO quadrant [65]) and is structurally inapplicable to anonymous traffic.

The infostealer economy [53, 54, 55, 56] provides the economic bypass: malware infections export both the session cookie and the device-bound key simultaneously from a compromised device. At $30–$200/month for botnet access (with dark-web market prices documented up to $4,800/month for premium botnets), the economic ceiling is the black-market infection cost, not the cryptographic protocol strength.

However, as with PATs (Section 4.3), the botnet-infection ceiling is not the only bypass path. SDK-based proxy networks — where users consent to proxying software bundled in free applications — provide access to the same TPM/Secure Enclave keys without triggering malware-classification heuristics. A device running a Bright Data SDK endpoint generates valid DBSC proofs-of-possession using hardware keys on the actual enrolled device. The SDK-based bypass ceiling is lower than the PPI malware ceiling by a wide margin, and the supply is more elastic. This introduces a structural vulnerability for Tier 1 architectures that prior threat models have not adequately addressed: the operating system cannot distinguish between legitimate SDK network traffic routed through consenting devices and criminal malware — both execute with user-level or kernel-level permissions on the hardware that holds the attestation keys.

### 6.2 Passkeys and the Credential-Phishing Threat Model

Passkeys (FIDO2/WebAuthn [31]) eliminate shared secrets and credential phishing through hardware-enrolled cryptographic authentication. Kuchhal et al. [32] found only 4.4% of authenticators carry Level 2+ certification offering malware resistance. Tarrach et al. [33] identified message integrity gaps accessible to browser extensions. The structural limit is the practical difficulty of guaranteeing key-storage integrity across the diversity of consumer devices.

### 6.3 The Attestation Market Centralization Problem

The most significant structural consequence of the VLM paradigm shift — more significant than any individual architecture's vulnerability — is the transformation of the attestation infrastructure market. As probabilistic defenses lose efficacy against Operator Synthesis, the remaining viable defenses (PATs, DBSC, Passkeys) all share a common dependency: they require platform-level root of trust infrastructure operated by OS vendors.

**The consolidation dynamic.** Three companies — Apple, Google, Microsoft — control the device attestation layer for the web today; the 2026 PACT initiative [80] extends the dynamic from device roots of trust to issuer judgment (Section 6.4):

- **Apple PATs:** RSA blind signatures issued by Apple's servers, backed by Secure Enclave attestation on iOS 16+ and macOS Ventura+ [44]. Token issuance is rate-limited per device. Apple controls which origins receive tokens and at what rate.
- **Google Privacy Pass:** VOPRF-based issuance integrated into Chrome via the Private State Token API [45]. Google operates an issuer. Google controls which origins participate and under what terms.
- **Microsoft Device Bound Session Credentials:** TPM-backed session binding in Windows and Edge [36]. Microsoft controls the key storage and attestation infrastructure.
- **Cloudflare PACT:** a cross-browser anonymous-attestation initiative announced in 2026 with Mozilla, Google, Microsoft, and Shopify [80]. PACT does not add a new hardware root of trust; it consolidates a different asset — the *right to judge who is a person*. Cloudflare, already positioned behind a substantial share of global web infrastructure, is a natural central participant in issuance [83], and origins are expected to configure a small set of aggregating issuers whose admission policies become security-critical [81].

**Reframing the trilemma.** Prior work [42, 43] usefully framed this as a "Centralization vs. Anonymity Trilemma" — identifying a theoretical trade-off between anonymous access, deterministic bot resistance, and decentralized trust. This framing correctly identified the structural tension. We extend it by observing that the trilemma is not merely a theoretical construct but an empirically observable market outcome: all three OS vendors have converged on centralized attestation infrastructure as the practical resolution of the trilemma, and the resulting market consolidation is its own structural concern distinct from the abstract trade-off. The centralization problem is therefore not a refutation of the trilemma framing but an empirical corollary: given the trilemma, the market has resolved it through platform vendor consolidation, and this resolution carries consequences — pricing power, exclusion risk, and vendor lock-in — that the theoretical trilemma framing alone does not capture. The question is not whether decentralized anonymous attestation is theoretically possible (it is — zero-knowledge proofs of personhood, decentralized issuer networks, and threshold attestation protocols are all feasible in principle). The question is whether any decentralized alternative can achieve the *economic scaling* to compete with platform-integrated attestation.

**The ad-tech macroeconomic context.** The deprecation of third-party cookies by browser vendors — who simultaneously operate the largest digital advertising platforms — creates a dual economic effect: it degrades independent stateful bot mitigation (Type II) while consolidating attestation power into platform-native APIs (Privacy Sandbox, PATs, SKAdNetwork). This intersection of ad-tech market consolidation and bot mitigation economics requires critical scrutiny beyond the technical protocol analysis.

### 6.4 PACT: The Software-Anchor Turn and the Issuer-Judgment Problem

On June 22, 2026, Cloudflare announced **Private Access Control Tokens (PACT)**, a cross-industry initiative joined by Mozilla Firefox, Google Chrome, Microsoft Edge, and Shopify, to replace CAPTCHAs and behavioral surveillance with anonymous cryptographic attestation — a response to a web in which bots now account for roughly 58% of HTTP requests [80]. PACT extends the Privacy Pass architecture (RFC 9576) with blind signatures: an origin that has already established that a visitor is legitimate issues an anonymous token, and the browser carries it to the next site as proof that a human is in the loop, with no CAPTCHA, no forced login, and no fingerprinting. Precision about status is required: as of mid-2026, PACT is a proposal, not a product. There is no deployment timeline, no IETF draft published under the PACT name, and no finalized issuance-governance specification; what exists is a press statement and early design discussion in the `antifraudcg/pact` repository [81, 83]. The most consequential decision — who gets to issue tokens, and on what basis — remains open. Notably, Apple, co-creator of the original Private Access Tokens with Cloudflare in 2022, did not join the announcement [80, 83].

The architectural significance of PACT for this SoK is its break with the hardware anchor that motivates Type IV's Tier 1 classification (Section 4.2). In Privacy Pass terminology, an **Attester** is a party that knows something about the user, and the **Issuer** signs the blinded token [80]. Apple PATs anchor that knowledge in device posture — approved device, approved hardware, approved operating environment, verified without installed software [44]. PACT instead accepts *software or contextual anchors*: active subscriptions, account standing, first-party relationships, or issuer vouching [81, 84]. This does not remove the Sybil problem; it relocates it. The attacker's unit of scarcity ceases to be a compromised device and becomes a credentialed account — and bulk account registration, credential stuffing, stolen session tokens, and cheap subscriptions are all automatable inputs to a token-farming pipeline that operates upstream of the attestation protocol. As one analysis puts it, token farming creates a new abuse layer upstream; the fix, hardware attestation, slides back into exactly what Web Environment Integrity was rejected for [83].

The proposal assigns the browser the role of trusted user-agent: it mediates credential storage, issuer selection, challenge budgets, and token conversion [81]. Under the Operator Synthesis threat model, this boundary is not a trust anchor. A bot operator may control the browser profile, the device, or both, and a copied or compromised profile can exercise the same issuance APIs as a legitimate user. The cryptographic unlinkability of blind signatures does not repair this: it only ensures that a token can be redeemed without revealing which issuer produced it or which user obtained it. The token's value depends entirely on the quality of the issuer's admission process, and the announced attack surface reflects this — unauthorized endorsement acquisition, token replay, token theft, credential export, anchor impersonation, malicious anchor behavior, Sybil amplification, metadata leakage, and downgrade attacks [84].

PACT's centralization profile differs from hardware attestation's. The concentration is not in device roots of trust but in issuer judgment: origins are expected to configure up to two aggregating issuers and a credit cost per request [81], which makes the origin's issuer choice a gatekeeping decision, and Cloudflare — already the termination point for a substantial share of web traffic — a natural central participant [83]. The structural dynamic that critics identified in Google's Web Environment Integrity proposal recurs: a small number of platforms decide which clients are treated as legitimate [83]. The ratchet effect amplifies it. PACT tokens begin as optional friction-reducers, but as adoption spreads, the *absence* of a token carries information: token-bearing traffic passes cleanly, untokened traffic is challenged more aggressively, risk thresholds are recalibrated, and no single actor decides to make tokens mandatory [83]. The result is a systematically suspect class of legitimate traffic with no issuer relationship — internet measurement systems, security research scanners, archival crawlers, RSS readers, Tor users, and alternative browsers [83]. Compounding this, PACT as announced lacks the governance mechanisms that would control issuer quality: no issuer accreditation model, no public issuer directory, no revocation lists, no audit requirements, and — as the nearest rate-control mechanism — only the IETF's rate-limited issuance draft [83]. Absent these, the ecosystem faces the classic adverse-selection problem: low-quality issuers undercut high-quality ones, and a blind-signature token proves only that *some* issuer signed it, not that a meaningful personhood check occurred.

Three further trade-offs warrant note. First, metadata: blind signatures protect linkability at the verifying origin, but the initial issuer still observes which account requested a token and when [80]; the aggregating-issuer and IssuerHide (zero-knowledge issuer-blinding) architectures discussed in the PACT repository would mitigate this [81, 82], but they remain design options, not properties of PACT as announced. Second, exclusion: if issuers anchor on financial or account-standing signals, the system distinguishes consumers with persistent platform relationships from everyone else — inverting the intended anti-abuse effect, since sophisticated bot operators can afford accounts while legitimate low-income or anonymity-seeking users cannot [84]. Third, sovereignty: a state that becomes a mandatory issuer could observe issuance events, deny tokens to disfavored traffic, and require acceptance of state-issued credentials within its jurisdiction; data-localization regimes could balkanize the web at the protocol layer [84]. Finally, PACT is explicitly motivated by agentic AI traffic [80, 84], yet its token semantics for the human → AI agent → website model — whether each agent receives its own token, whether shared tokens invite replay and theft, and whether delegated issuance exists — are unresolved. PACT answers "is a real person behind this session" without answering "which actor is authorized to spend that personhood" [83]. The cryptographic layer is the least controversial part of the proposal; the governance layer is absent. Until issuer accreditation, revocation, auditing, aggregation defaults, and an explicit open-web fallback are specified, PACT is not a trust protocol so much as a trust-proxy protocol: it inherits the security posture of whatever issuer an origin happens to configure [83].

### 6.5 The Excluded Chapter: Passive Server-Side Traffic-Artifact Continuity

**The boundary, stated honestly.** Section 1.2 excludes "purely server-side defenses (WAF, TLS fingerprinting, DDoS scrubbing, rate limiting)" from this SoK's scope because they operate under a different economic model than client-side execution, telemetry, or cryptographic binding — a reasonable exclusion for a taxonomy of *client-side* anti-automation, and one that kept the L1–L4 diagnostic framework (Section 3.4) from being diluted by a heterogeneous, separately-literatured category. But Section 4.3 does not stay on the client-side side of that boundary: it concludes that once a client-side attestation is cryptographically valid yet attacker-controlled — an SDK-proxied device presenting a genuine PAT, a farmed account presenting a genuine PACT token — "the defender's only recourse is to fall back to network-layer behavioral metadata: ASN reputation scoring, IP-to-Account cardinality analysis, velocity and rate-limiting heuristics, and cross-session pattern matching." The paper builds the entire case for that recourse and then declines to analyze it. This subsection is the natural sequel that Section 4.3 itself demands, not a re-opening of the excluded category wholesale: it examines one specific, passively-observed slice of server-side signal — the one Sections 4.1 and 5.2 already gesture at without naming as such — rather than WAF rules, DDoS scrubbing, or rate limiting generally. As Section 3.1 states, the references supporting this subsection were gathered outside this SoK's systematic search methodology; what follows is this paper's own analytical extension, not an additional literature review, and it should be weighted accordingly.

**Defining the surface.** We define *passive server-side traffic-artifact continuity* as a session- or request-level continuity signal derived from properties of the network connection that the browser's JavaScript runtime does not control and cannot self-report. Concretely: the TLS ClientHello cipher-suite, extension, and elliptic-curve ordering (the JA3 fingerprint [86]) and its JA4+ successors, which extend the same idea jointly across TLS, HTTP, and TCP behavior (JA4, JA4H, JA4T [87, 88]); the framing and settings-negotiation behavior of the HTTP/2 (RFC 9113 [96]) and HTTP/3 (RFC 9114 [97]) connection, including the version-independent stream-prioritization signals both protocols share via RFC 9218's Extensible Prioritization Scheme [99]; and the transport-layer fields visible to any terminating server without application-layer cooperation, which split by transport rather than forming one universal set — path MTU is not an IP-header field but is inferred from the packet sizes and fragmentation behavior a server observes in arriving traffic, while a sender's initial IPv4 TTL or IPv6 Hop Limit is inferred from the already-decremented value the header field actually carries on arrival; both inferences hold regardless of whether the connection rides TCP or QUIC/UDP, while initial TCP window size is specific to HTTP/1.1 and HTTP/2 sessions carried over TCP and has no counterpart on a native HTTP/3 connection, which runs over QUIC (RFC 9000 [98]) and UDP rather than TCP. Section 4.1 already names the TCP-carried subset of these fields as the containerization gap's leaks. None of this is new cryptography or a new protocol. Passive TLS and TCP/IP fingerprinting is a decade-old technique with an academic literature of its own [89] and mature tooling (p0f predates this SoK's entire Part I timeline [90]), and JA3/JA4-class signals are already production-deployed at CDN scale for bot detection [91, 92]. What is new to this SoK is connecting the technique explicitly to the paper's own findings: the fields Section 4.1 names as artifacts of the *attacker's* containerized deployment are, from the server's vantage point, exactly the inputs to the network-layer behavioral metadata Section 4.3 names as the defender's last recourse.

**Why this survives Operator Synthesis.** The survival logic is the same shape as Type IV/V's in Section 4.2 — modality independence — obtained here without a hardware root of trust or platform-vendor coordination. In the vocabulary of Section 1.3's Axis C, this signal is orthogonal to the axis: Operator Synthesis changes *how* a browser is driven (OS-level input synthesis versus programmatic DOM manipulation), not *what its network stack emits* when it opens a TLS connection. The TCP/IP stack and TLS library are negotiated below the JavaScript runtime and below the orchestration layer Section 1.4 describes; a VLM-driven session, a human session, and a headless-script session sharing the same browser binary on the same OS emit the same handshake. This is precisely the property Section 4.1's containerization-gap discussion and Section 5.2's macroscopic-latency discussion already rely on without naming it: both are server-observable without any client cooperation, which is what makes them survive a threat model built around subverting the client.

**Honest limits: not an authenticator, and not unforgeable.** This is a continuity or risk score, not an authenticator, and this subsection does not propose it as one. NIST SP 800-63B draws a definitional line between an authenticator — something a subscriber proves possession and control of — and contextual signals used to inform a risk-based decision [93]; passive traffic-artifact continuity sits on the risk-signal side of that line, consumed the way a DBSC proof-of-possession failure or a PAT rate-limit breach is already consumed in Section 4.3 — to gate a step-up challenge, never to assert an identity by itself. It is also, like every mechanism catalogued in this SoK, evadable. TLS-fingerprint spoofing to mimic a stock browser is a documented, production-observed attacker technique, not a hypothetical one [91], and tooling to reproduce a target browser's TLS/H2/TCP fingerprint on demand — the fingerprintproxy-class approach the broader research program around this SoK treats as its own falsifier — is genuinely effective against any single one of these signals in isolation. Consistent with this SoK's economics-of-security framing (Section 2.4), the value is conjunctive and probabilistic, not categorical: cross-layer coherence between the TLS fingerprint, the HTTP/2-or-3 behavior, and the TCP/IP fields Section 4.1 already treats as jointly expensive to fake, combined with calibrated scoring rather than a hard pass/fail gate. An attacker who has already paid Section 5.3's premium or enterprise proxy-tier prices to obtain session continuity for a Type II bypass has not thereby purchased TLS/TCP-stack coherence with that proxy's declared identity — the two costs are different line items, and a defender scoring across both may close a gap that a single-signal defense leaves open — by how much is exactly the score-delta measurement this subsection's cost-accounting discussion below, and its accompanying footnote, flag as unmeasured. Spoofing one layer is comparatively cheap; spoofing all layers consistently, across a large session population, while simultaneously maintaining the state-orchestration cost structure of Sections 4.2 and 5.3, is a different and more expensive problem.[^continuity-score]

**Extending the cost-accounting framework (bridging to Section 5).** Section 5's cost-accounting exercise — VLM inference pricing (5.1), macroscopic latency (5.2), proxy-supply elasticity (5.3) — is directly reusable here with one substitution. Where Section 5.1's `C_effective` computes an attacker's cost per successful bypass token as a function of the per-attempt success probability `P(success)`, the cost-to-evade a server-side continuity score takes the same accounting-identity shape:

```text
Cost_evasion = Cost_proxy_tier + Cost_fingerprint_spoof_tooling + Cost_state_orchestration
```

`Cost_evasion`, defined this way, is a per-attempt figure — the budget an attacker spends to present one session's worth of spoofed transport-layer artifacts — not a per-successful-evasion figure. `Cost_proxy_tier` and `Cost_state_orchestration` are recurring, session-scoped costs (subscription and per-session compute, respectively); `Cost_fingerprint_spoof_tooling` is a fixed development cost amortized across the sessions the tooling serves before the target scoring implementation changes and the tooling needs updating. To make this comparable to Section 5.1's `C_effective` — which is explicitly a cost *per successful bypass* — the same division by success probability applies:

```text
C_evasion_effective = Cost_evasion / P(score below step-up threshold | spoofed layer set)
```

This paper does not have a value for `P(score below step-up threshold | spoofed layer set)`, and does not claim to. The missing empirical input is exactly the kind of gap Section 7.1 already names for the VLM-side cost model: a standardized, adversarial measurement of the score delta a given evasion budget purchases, run against a real scoring implementation and a real fingerprint-spoofing harness rather than assumed. Naming this gap sets up the relevant experiment without claiming its result.

**The centralization counterpoint.** Section 6.3's critique of PAT/Privacy Pass/DBSC centralization, and Section 6.4's critique of PACT's issuer-judgment consolidation, both identify a market structure in which a small number of platform vendors or accredited issuers become security-critical gatekeepers. A first-party, server-observed continuity score is a structural counterpoint worth stating plainly: it requires no OS-vendor coordination, no cross-origin issuer economy, and no accreditation regime. Any origin that terminates its own TLS can compute it from connections it already receives. This is not a substitute for Section 6's cryptographic attestation — it answers a different question (session continuity, not personhood or device integrity) — but it is the one candidate in this SoK's entire architecture landscape whose deployment does not require Apple, Google, Microsoft, or an accredited PACT issuer to participate, which matters given Section 4.4's three-part critique of platform dependency. The honest reverse limitation should be stated with equal weight: because it requires no coordination, it also earns no interoperability. Every origin computes its own score, on its own traffic, with no shared cross-origin standard for what "continuous" means — the opposite failure mode from PACT's over-centralization, not a resolution of the trilemma in Section 6.3.

The same structural claim this subsection makes — that an attestation not bound to the context it is meant to secure degrades into a portable signal rather than proof — recurs across the author's other published work: a general treatment of client-side trust decay [94], and a specific case study of a session-continuity failure in a national eID cross-device signing flow [95]. Both are cited here as applied case studies of the same argument in adjacent domains, not as additional peer-reviewed sources, and are marked as self-citations for that reason.

[^continuity-score]: One production instantiation of this class of scoring — ingesting TLS/H2/H3/TCP artifacts at the terminating edge to compute a continuity score — is the author's own system, disclosed here as such rather than as a claim of independent validation. It is referenced only as an existence proof that the architecture described above is buildable at the edge, not as evidence of its detection accuracy, which remains unmeasured in any publicly reviewable way and is explicitly out of scope for this SoK.

---

## 7. Open Problems and Future Research

### 7.1 Closing the Empirical Gap in VLM Attack Economics

The cost-accounting framework in Section 5 is deliberately incomplete. We currently lack:

- Published empirical measurements of VLM-driven attack throughput at industrial scale
- Reliable data on proxy market supply elasticity under Operator Synthesis demand patterns
- Longitudinal studies of VLM inference cost deflation and its impact on attack economics

A standardized, ethical benchmark for measuring VLM-driven bypass costs — analogous to the "Bot-Bench" gap identified for VM chronometrics — is needed to transform the qualitative economic analysis of Section 5 into a quantitative discipline.

### 7.2 VLM-Resilient Attestation Primitives

The Tier 1 architectures identified in Section 4.2 survive Operator Synthesis but carry the structural dependencies documented in Section 6. Research needed on:

- **Decentralized anonymous attestation:** Zero-knowledge proofs of personhood, decentralized issuer networks (threshold issuance, distributed VOPRF), and hardware-backed attestation without OS-vendor dependency. The PACT design discussion illustrates both the feasibility and the governance gap: aggregating-issuer and IssuerHide architectures [81, 82] would mitigate initial-issuer metadata exposure, but as of the 2026 announcement they remain design options rather than defaults, and no decentralized issuer network has been specified [80, 83].
- **Physical-presence challenges:** Defenses that require physical-world interaction (camera-based liveness detection, ambient sensor fusion) that a VLM operating in a virtual machine cannot satisfy. These are not CAPTCHAs — they do not require human cognition — but they impose a physical-presence cost that distinguishes local execution from remote VLM operation. Defenders must account for a critical countermeasure: incentivized proxying, where SDK-based proxy networks—leveraging the attestation bypass dynamics analyzed in Section 4.3—prompt the legitimate device owner to satisfy the physical challenge in exchange for in-app rewards, bridging the physical gap. This does not reduce the bypass cost to zero — it introduces latency (user must be available), incentive costs (per-action reward), and coordination complexity — but it establishes that physical-presence challenges require deployment-time threat modeling against SDK-mediated human relay, not just autonomous VLM operation.
- **Cross-modal consistency verification:** Verifying that sensor data from multiple independent channels (camera, microphone, touchscreen, accelerometer) is internally consistent with a single physical environment. A VLM operating in a VM cannot easily maintain cross-modal consistency because it does not control all sensor channels.

### 7.3 Standardized Benchmarking (The "Bot-Bench" Problem)

Academia lacks a standardized testbed for evaluating anti-automation defenses under Operator Synthesis. Current evaluations rely on grey-hat reverse engineering of production systems or small-scale PoCs that vendors invalidate through compile rotation. A reproducible, vendor-neutral evaluation harness — with known ground truth for human vs. VLM interaction — is necessary for systematic measurement. The BehavePassDB effort [23] provides a partial template but does not account for VLM interaction patterns.

### 7.4 Privacy Regulation's Collateral Damage on Stateful Mitigation

GDPR, ePrivacy Directive, and third-party cookie deprecation break the profile-aging model underpinning stateful telemetry (Type II). As browsers restrict persistent identifiers (ITP, ETP, Total Cookie Protection), the economic ceiling of stateful defenses rises — they become less effective — yet vendors continue to market them. The tension between privacy regulation and stateful bot mitigation, particularly under the additional stress of Operator Synthesis, is under-studied.

The structural irony is acute: **browser-implemented tracking prevention mechanisms (ITP, ETP, Total Cookie Protection) and related regulatory mandates structurally enforce the amnesia that VLMs mathematically exploit.** Profile-aging was the one Type II defense that Operator Synthesis could not trivially bypass — it required time, not just inference compute, to accumulate. By restricting persistent cross-session identifiers, these browser-enforced restrictions — which in some cases go beyond GDPR's legal requirements, implementing stricter anti-tracking defaults than the regulation mandates — eliminate the profile-aging constraint that was Type II's last structural ceiling against the APB threat model. The irony operates at two levels: (1) browser vendors unilaterally implementing stronger tracking prevention than regulation requires, and (2) GDPR's legitimate-interest and proportionality provisions — which could permit bot-detection telemetry with user notice and opt-out — being effectively overridden by blanket browser-level restrictions. Privacy and security are not inherently opposed, but in this specific case, the timeline of browser-enforced tracking prevention (ITP/ETP deployment) intersects with the VLM capability timeline (2024–2025) to produce an outcome that neither policy nor platform design alone would have created.

Furthermore, the deprecation of cross-site identifiers by browser vendors (who are also major ad platforms) degrades independent stateful mitigation while consolidating attestation power into platform-native APIs — a dual effect that requires antitrust and architectural scrutiny.

---

## 8. Conclusion

This SoK has presented a two-part systematization of client-side anti-automation. In Part I, we documented the historical landscape (2010–2024) through five mechanism-based architectural types and the L1–L4 diagnostic framework, explicitly framing these as retrospective artifacts that reveal why probabilistic client-side attestation has a finite economic ceiling. In Part II, we analyzed the Operator Synthesis attack vector for the APB threat model, showing that the cost burden of each layer shifts from browser-instrumentation forgery to systems-integration engineering: L1a shifts to container-evasion, L1b shifts to kinematic-smoothing orchestration, L2 shifts to application-level workflow RE, L4 shifts from microsecond instrumentation detection to second-scale latency profiling.

The architectures that survive — Platform/OS-level anonymous attestation and hardware-anchored determinism — do so because their security is anchored in cryptographic hardware possession rather than probabilistic detection of behavioral signals. But survival is not immunity: these architectures carry a structural dependency on a vendor oligopoly controlling the root of trust, and their economic ceiling is the black-market price of device compromise, not the mathematical hardness of the attestation protocol.

Three insights define the field's trajectory for the APB threat model:

1. **Probabilistic client-side attestation faces severe structural pressure under Operator Synthesis.** Against a well-resourced adversary operating a VLM through an adequate orchestration pipeline, the detection premise on which VM attestation, behavioral telemetry, and biometric analysis relied is substantially degraded. Defenses that remain effective against commodity adversaries lose their cost-imposing power against this top-tier threat model. However, Operator Synthesis does not eliminate probabilistic detection entirely — the cost burden shifts rather than vanishes, as the L1–L4 diagnostic analysis demonstrates.
2. **Hardware-anchored attestation is necessary but not sufficient.** It survives the paradigm shift but introduces vendor centralization, device-adoption dependencies, and a shifting of the attack surface to the device-compromise economics.
3. **The defining open problem is no longer purely "how to detect bots" but increasingly "who controls the infrastructure of web trust."** The Anonymous Authentication Gap has been technically narrowed; the Centralization Gap has emerged as its successor — and the 2026 PACT initiative shows the gap is now contested along a second axis, as the industry experiments with replacing hardware roots of trust with issuer judgment (Section 6.4).

Client-side anti-automation faces a significant inflection point. The tools and concepts of the 2017–2024 period — register-based VMs, behavioral scoring, kinematic analysis — retain value as diagnostic artifacts and as defenses against the long tail of commodity automation, but their cost-imposing power is substantially reduced for adversaries operating at the top of the capability distribution. The field must now confront the harder problem of building decentralized, privacy-preserving attestation infrastructure that does not depend on a vendor oligopoly, alongside the continued engineering challenge of hardening probabilistic defenses against lower-resourced adversaries.

---

## References

**[1]** J. Bonneau, A. Miller, J. Clark, A. Narayanan, J. A. Kroll, and E. W. Felten. "SoK: Research Perspectives and Challenges for Bitcoin and Cryptocurrencies." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2015. DOI: 10.1109/SP.2015.14.

**[2]** K. Thomas et al. "SoK: Hate, Harassment, and the Changing Landscape of Online Abuse." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00028.

**[3]** Y. Wu, W. K. Edwards, and S. Das. "SoK: Social Cybersecurity." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2022. DOI: 10.1109/SP46214.2022.9833757.

**[4]** N. Mathews, J. K. Holland, S. E. Oh, M. S. Rahman, N. Hopper, and M. Wright. "SoK: A Critical Evaluation of Efficient Website Fingerprinting Defenses." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2023. DOI: 10.1109/SP46215.2023.10179289.

**[5]** T. Rokicki, C. Maurice, and P. Laperdrix. "SoK: In Search of Lost Time: A Review of JavaScript Timers in Browsers." In *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, 2021. DOI: 10.1109/EuroSP51992.2021.00039.

**[6]** P. Laperdrix, N. Bielova, B. Baudry, and G. Avoine. "Browser Fingerprinting: A Survey." *ACM Trans. Web*, Vol. 14, No. 2, Article 8, pp. 1–33, 2020. DOI: 10.1145/3386040.

**[7]** U. Iqbal, S. Englehardt, and Z. Shafiq. "Fingerprinting the Fingerprinters: Learning to Detect Browser Fingerprinting Behaviors." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00019.

**[8]** A. Gómez-Boix, P. Laperdrix, and B. Baudry. "Hiding in the Crowd: An Analysis of the Effectiveness of Browser Fingerprinting at Large Scale." In *Proc. The Web Conference (WWW)*, pp. 309–318, 2018. DOI: 10.1145/3178876.3186097.

**[9]** T. Laor et al. "DRAWNAPART: A Device Identification Technique based on Remote GPU Fingerprinting." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2022. DOI: 10.14722/ndss.2022.24093.

**[10]** S. Wu, P. Sun, Y. Zhao, and Y. Cao. "Him of Many Faces: Characterizing Billion-scale Adversarial and Benign Browser Fingerprints on Commercial Websites." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.24049.

**[11]** X. Lin, P. Ilia, S. Solanki, and J. Polakis. "Phish in Sheep's Clothing: Exploring the Authentication Pitfalls of Browser Fingerprinting." In *Proc. USENIX Security Symposium*, 2022.

**[12]** Z. Liu, P. Shrestha, and N. Saxena. "Gummy Browsers: Targeted Browser Spoofing against State-of-the-Art Fingerprinting Techniques." In *Proc. International Conference on Applied Cryptography and Network Security (ACNS)*, June 2022. arXiv: 2110.10129.

**[13]** B. A. Azad, O. Starov, P. Laperdrix, and N. Nikiforakis. "Taming the Shape Shifter: Detecting Anti-fingerprinting Browsers." In *Proc. DIMVA*, 2020.

**[14]** N. Andriamilanto, T. Allard, G. Le Guelvouit, and A. Garel. "A Large-scale Empirical Analysis of Browser Fingerprints Properties for Web Authentication." *ACM Trans. Web*, Vol. 16, No. 1, Article 1, pp. 1–62, 2022. DOI: 10.1145/3478026.

**[15]** A. Acien, A. Morales, J. Fierrez, R. Vera-Rodriguez, and O. Delgado-Mohatar. "BeCAPTCHA: Behavioral Bot Detection using Touchscreen and Mobile Sensors benchmarked on HuMIdb." *Engineering Applications of Artificial Intelligence*, Vol. 98, 104058, 2021. DOI: 10.1016/j.engappai.2020.104058.

**[16]** A. Acien, A. Morales, J. Fierrez, and R. Vera-Rodriguez. "BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection." *Pattern Recognition*, Vol. 127, 108643, 2022. DOI: 10.1016/j.patcog.2022.108643.

**[17]** H. Niu, J. Chen, Z. Zhang, and Z. Cai. "Mouse Dynamics Based Bot Detection Using Sequence Learning." In *Biometric Recognition (CCBR)*, LNCS Vol. 12878, pp. 49–56. Springer, 2021. DOI: 10.1007/978-3-030-86608-2_6.

**[18]** H. Niu, C. Cheng, and Z. Cai. "Learning Human Behavior for Bot Detection: A Perspective on Mouse Movement (MouseAgent)." In *Proc. China Automation Congress (CAC)*, pp. 6575–6580. IEEE, 2023. DOI: 10.1109/CAC59555.2023.10451138.

**[19]** C. Iliou, T. Kostoulas, T. Tsikrika, V. Katos, S. Vrochidis, and I. Kompatsiaris. "Detection of Advanced Web Bots by Combining Web Logs with Mouse Behavioural Biometrics." *Digital Threats: Research and Practice*, Vol. 2, No. 3, Article 24, pp. 1–26. ACM, 2021. DOI: 10.1145/3447815.

**[20]** H. Fereidooni et al. "AuthentiSense: A Scalable Behavioral Biometrics Authentication Scheme using Few-Shot Learning for Mobile Platforms." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.24044.

**[21]** S. Sadeghpour and N. Vlajic. "ReMouse Dataset: On the Efficacy of Measuring the Similarity of Human-Generated Trajectories for the Detection of Session-Replay Bots." *Journal of Cybersecurity and Privacy*, Vol. 3, No. 1, pp. 95–117. MDPI, 2023. DOI: 10.3390/jcp3010007.

**[22]** D. DeAlcala et al. "BeCAPTCHA-Type: Biometric Keystroke Data Generation for Improved Bot Detection." In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, pp. 1051–1060. IEEE, 2023. DOI: 10.1109/CVPRW59228.2023.00112.

**[23]** G. Stragapede, R. Vera-Rodriguez, R. Tolosana, and A. Morales. "BehavePassDB: Public Database for Mobile Behavioral Biometrics and Benchmark Evaluation." *Pattern Recognition*, 2022. DOI: 10.1016/j.patcog.2022.109010.

**[24]** S. Schrittwieser, S. Katzenbeisser, J. Kinder, G. Merzdovnik, and E. Weippl. "Protecting Software through Obfuscation: Can It Keep Pace with Progress in Code Analysis?" *ACM Comput. Surv.*, Vol. 49, No. 1, Article 4, pp. 1–37, 2016. DOI: 10.1145/2886012.

**[25]** P. Saxena, D. Akhawe, S. Hanna, F. Mao, S. McCamant, and D. Song. "A Symbolic Execution Framework for JavaScript." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, pp. 513–528, 2010.

**[26]** T. Blazytko, M. Contag, C. Aschermann, and T. Holz. "Syntia: Synthesizing the Semantics of Obfuscated Code." In *Proc. USENIX Security Symposium*, pp. 643–659, 2017.

**[27]** M. Schloegel et al. "Loki: Hardening Code Obfuscation Against Automated Attacks." In *Proc. USENIX Security Symposium*, pp. 3055–3073, 2022.

**[28]** B. Rozière, M. Lachaux, L. Chanussot, and G. Lample. "DOBF: A Deobfuscation Pre-Training Objective for Programming Languages." In *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. 34, 2021. arXiv: 2102.07492.

**[29]** V. Raychev, M. Vechev, and A. Krause. "Predicting Program Properties from 'Big Code'." In *Proc. ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL)*, pp. 111–124, 2015. DOI: 10.1145/2676726.2677009.

**[30]** K. Coogan, G. Lu, and S. Debray. "Deobfuscation of Virtualization-Obfuscated Software: A Semantics-Based Approach." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 275–284, 2011. DOI: 10.1145/2046707.2046739.

**[31]** J. Hodges, J.C. Jones, M.B. Jones, A. Kumar, and E. Lundberg, Eds. "Web Authentication: An API for Accessing Public Key Credentials, Level 2." *W3C Recommendation*, 8 April 2021. URL: https://www.w3.org/TR/2021/REC-webauthn-2-20210408/.

**[32]** D. Kuchhal, M. Saad, A. Oest, and F. Li. "Evaluating the Security Posture of Real-World FIDO2 Deployments." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 2381–2395, 2023. DOI: 10.1145/3576915.3623063.

**[33]** T. Tarrach et al. "A Security and Usability Analysis of Local Attacks Against FIDO2." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2024.

**[34]** M. Kepkowski, L. Hanzlik, I. D. Wood, and M. A. Kaafar. "How Not to Handle Keys: Timing Attacks on FIDO Authenticator Privacy." In *Proc. Privacy Enhancing Technologies Symposium (PETS)*, Vol. 2022, No. 4, pp. 705–726, 2022. DOI: 10.56553/popets-2022-0129.

**[35]** M. Islam, S. S. Arora, R. Chatterjee, and K. C. Wang. "Detecting Compromise of Passkey Storage on the Cloud." In *Proc. USENIX Security Symposium*, pp. 7743–7762, 2025.

**[36]** D. Rubery and K. Monsen, Eds. "Device Bound Session Credentials (DBSC)." *W3C Web Application Security Working Group / WICG*, 2024. URL: https://w3c.github.io/webappsec-dbsc/.

**[37]** Google Chrome Security Team. "Fighting Cookie Theft Using Device Bound Sessions." *Chromium Blog*, 2 April 2024. URL: https://blog.google/chromium/fighting-cookie-theft-using-device/.

**[38]** A. Davidson, J. Iyengar, and C. A. Wood. "The Privacy Pass Architecture." *RFC 9576*, IETF, June 2024. DOI: 10.17487/RFC9576.

**[39]** T. Pauly, S. Valdez, and C. A. Wood. "The Privacy Pass HTTP Authentication Scheme." *RFC 9577*, IETF, June 2024. DOI: 10.17487/RFC9577.

**[40]** S. Celi, A. Davidson, S. Valdez, and C. A. Wood. "Privacy Pass Issuance Protocols." *RFC 9578*, IETF, June 2024. DOI: 10.17487/RFC9578.

**[41]** A. Davidson, I. Goldberg, N. Sullivan, G. Tankersley, and F. Valsorda. "Privacy Pass: Bypassing Internet Challenges Anonymously." *Proc. on Privacy Enhancing Technologies (PoPETs)*, Vol. 2018, No. 3, pp. 164–180, 2018. DOI: 10.1515/popets-2018-0026.

**[42]** B. Kreuter, T. Lepoint, M. Orrù, and M. Raykova. "Anonymous Tokens with Private Metadata Bit." In *Advances in Cryptology — CRYPTO 2020*, pp. 308–336. Springer, 2020. DOI: 10.1007/978-3-030-56784-2_11.

**[43]** H. Chu, K. Do, S. Faller, and L. Hanzlik. "On the Security of Rate-limited Privacy Pass." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2023. ePrint: 2023/1805.

**[44]** Apple Inc. "Replace CAPTCHAs with Private Access Tokens." *WWDC22 Session*, June 8, 2022. URL: https://developer.apple.com/videos/play/wwdc2022/10077/.

**[45]** WICG. "Private State Token API." *WICG Community Group Draft*. URL: https://wicg.github.io/trust-token-api/.

**[46]** R. Anderson and T. Moore. "The Economics of Information Security." *Science*, Vol. 314, No. 5799, pp. 610–613, 2006. DOI: 10.1126/science.1130992.

**[47]** C. Herley and D. Florêncio. "Nobody Sells Gold for the Price of Silver: Dishonesty, Uncertainty and the Underground Economy." In *Proc. Workshop on the Economics of Information Security (WEIS)*, June 2009. Published in T. Moore, D. Pym, and C. Ioannidis (Eds.), *Economics of Information Security and Privacy*, pp. 33–53. Springer, 2010. DOI: 10.1007/978-1-4419-6967-5_3.

**[48]** T. Moore. "The Economics of Cybersecurity: Principles and Policy Options." *Int. J. Crit. Infrastruct. Prot.*, Vol. 3, No. 3, pp. 103–117, 2010. DOI: 10.1016/j.ijcip.2010.10.002.

**[49]** H. R. Varian. *Intermediate Microeconomics: A Modern Approach*, 9th ed. W. W. Norton & Company, 2014.

**[50]** R. Anderson et al. "Measuring the Cost of Cybercrime." In R. Böhme (Ed.), *The Economics of Information Security and Privacy*, pp. 265–300. Springer, 2013. DOI: 10.1007/978-3-642-39498-0_12.

**[51]** M. Motoyama, K. Levchenko, C. Kanich, D. McCoy, G. M. Voelker, and S. Savage. "Re: CAPTCHAs—Understanding CAPTCHA-Solving Services in an Economic Context." In *Proc. USENIX Security Symposium*, 2010.

**[52]** M. Motoyama, D. McCoy, K. Levchenko, S. Savage, and G. M. Voelker. "Dirty Jobs: The Role of Freelance Labor in Web Service Abuse." In *Proc. USENIX Security Symposium*, 2011.

**[53]** J. Caballero, C. Grier, C. Kreibich, and V. Paxson. "Measuring Pay-per-Install: The Commoditization of Malware Distribution." In *Proc. USENIX Security Symposium*, 2011.

**[54]** A. Côté Cyr. "Life on a Crooked RedLine: Analyzing the Infamous Infostealer's Backend." *ESET Research / WeLiveSecurity*, November 8, 2024. URL: https://www.welivesecurity.com/en/eset-research/life-crooked-redline-analyzing-infamous-infostealers-backend/.

**[55]** Microsoft Threat Intelligence. "Lumma Stealer: Breaking Down the Delivery Techniques and Capabilities of a Prolific Infostealer." *Microsoft Security Blog*, May 21, 2025. URL: https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/.

**[56]** S. Pastrana, A. Hutchings, D. R. Thomas, and J. Tapiador. "Malware Finances and Operations: A Data-Driven Study of the Value Chain for Infections and Compromised Access." *arXiv:2306.15726*, 2023.

**[57]** K. Drakonakis, S. Ioannidis, and J. Polakis. "The Cookie Hunter: Automated Black-box Auditing for Web Authentication and Authorization Flaws." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2020. DOI: 10.1145/3372297.3417869.

**[58]** R. van Wegberg, B. Klievink, M. van Eeten, et al. "Plug and Prey? Measuring the Commoditization of Cybercrime via Online Anonymous Markets." In *Proc. USENIX Security Symposium*, pp. 1009–1026, 2018.

**[59]** K. Thomas et al. "Framing Dependencies Introduced by Underground Commoditization." In *Proc. Workshop on the Economics of Information Security (WEIS)*, 2015.

**[60]** Cloudflare, Inc. "Bot Management Technical Documentation." *Cloudflare Docs*, 2023–2024.

**[61]** Google Chrome Security Team. "Device Bound Session Credentials (DBSC)." *Chrome for Developers*, 2024. URL: https://developers.chrome.com/docs/web-platform/device-bound-session-credentials.

**[62]** Human Security, Inc. (formerly PerimeterX). "The Economics of Bot Mitigation." *Industry Whitepaper*, 2022.

**[63]** Kasada Pty Ltd. "Polymorphic Security Technical Documentation." *Industry Documentation*, 2023.

**[64]** DataDome SAS. "Bot Detection and Mitigation Technical Overview." *Industry Documentation*, 2023.

**[65]** P. A. Grassi et al. "Digital Identity Guidelines." *NIST Special Publication 800-63-3*, 2017.

**[66]** OWASP Foundation. "Automated Threat Handbook." *OWASP Project*, 2018–2024. URL: https://owasp.org/www-project-automated-threats-to-web-applications/.

**[67]** J. H. Saltzer and M. D. Schroeder. "The Protection of Information in Computer Systems." *Proc. IEEE*, Vol. 63, No. 9, pp. 1278–1308, 1975.

**[68]** E. Bursztein, M. Martin, and J. C. Mitchell. "Text-based CAPTCHA Strengths and Weaknesses." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2012. DOI: 10.1145/2046707.2046724.

**[69]** J. Bonneau, C. Herley, P. C. van Oorschot, and F. Stajano. "Passwords and the Evolution of Imperfect Authentication." *Commun. ACM*, Vol. 58, No. 7, pp. 78–87, 2015. DOI: 10.1145/2699390.

**[70]** M. Guerar, L. Verderame, M. Migliardi, F. Palmieri, and A. Merlo. "Gotta CAPTCHA 'Em All: A Survey of 20 Years of the Human-or-Computer Dilemma." *ACM Comput. Surv.*, Vol. 54, No. 9, Article 192, pp. 1–33, 2021. DOI: 10.1145/3477142.

**[71]** E. Ulqinaku, H. Assal, A. A. Gkaniatsas, S. Schechter, and S. Capkun. "Is Real-time Phishing Eliminated with FIDO?" In *Proc. USENIX Security Symposium*, 2021.

**[72]** L. Allodi. "Economic Factors of Vulnerability Trade and Exploitation: Empirical Evidence from a Prominent Russian Cybercrime Market." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 1483–1499, 2017. DOI: 10.1145/3133956.3133960.

**[73]** M. Jones and D. Hardt. "The OAuth 2.0 Authorization Framework: Bearer Token Usage." *RFC 6750*, IETF, October 2012. DOI: 10.17487/RFC6750.

**[74]** M. Jones, J. Bradley, and N. Sakimura. "JSON Web Token (JWT)." *RFC 7519*, IETF, May 2015. DOI: 10.17487/RFC7519.

**[75]** D. Fett, B. Campbell, J. Bradley, T. Lodderstedt, M. Jones, and D. Waite. "OAuth 2.0 Demonstrating Proof of Possession (DPoP)." *RFC 9449*, IETF, September 2023. DOI: 10.17487/RFC9449.

**[76]** A. A. Noroozian, M. Ciere, M. van Eeten, and C. H. Ganan. "Residential Proxies: A Peek Behind the Curtain of the Proxies-as-a-Service Market." In *Proc. ACM Internet Measurement Conference (IMC)*, 2021. DOI: 10.1145/3487552.3487856.

**[77]** H. He, W. Yao, K. Ma, W. Yu, Y. Dai, H. Zhang, D. Cai, and D. S. Weld. "WebVoyager: Building an End-to-End Web Agent with Multimodal Models." In *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2024.

**[78]** X. Deng, Y. Gu, B. Zheng, S. Chen, S. Stevens, B. Wang, H. Sun, and Y. Su. "Mind2Web: Towards a Generalist Agent for the Web." In *Proc. Conference on Neural Information Processing Systems (NeurIPS)*, 2023.

**[79]** L. Zheng, Z. Wang, D. Fu, Y. Zhang, Y. Lu, B. Dai, D. Song, K. He, and Y. Li. "SeeAct: GPT-4V(ision) is a Generalist Web Agent, if Grounded." In *Proc. International Conference on Machine Learning (ICML)*, 2024.

**[80]** TechTimes. "Cloudflare, Chrome, and Firefox Plan to Replace CAPTCHAs With Cryptographic Tokens." June 23, 2026. URL: https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm

**[81]** antifraudcg/pact. "Design Proposal for PACT via ACTs with Aggregating Issuers." GitHub Issue #6, December 18, 2025. URL: https://github.com/antifraudcg/pact/issues/6

**[82]** antifraudcg/pact. "Sketching an Architecture That Uses Issuer Blinding." GitHub Issue #1, December 18, 2025. URL: https://github.com/antifraudcg/pact/issues/1

**[83]** B. Rudis. "PACT: The Open Web Doesn't Need Another Trust Oligopoly." *ai.rud.is*, June 23, 2026. URL: https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/

**[84]** K. Gupta. "PACT — Private Access Control Tokens: A Privacy-Preserving Trust Architecture for Humans and AI Agents on the Web." *krishnag.ceo*, June 2026. URL: https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/

**[85]** SourceFeed. "Cryptographic Trust Over Tracking: Inside the PACT Protocol." June 23, 2026. URL: https://sourcefeed.dev/a/cryptographic-trust-over-tracking-inside-the-pact-protocol

**[86]** J. Althouse, J. Atkinson, and J. Atkins. "TLS Fingerprinting with JA3 and JA3S." *Salesforce Engineering Blog*, January 15, 2019. URL: https://engineering.salesforce.com/tls-fingerprinting-with-ja3-and-ja3s-247362855967/

**[87]** FoxIO. "JA4+ Network Fingerprinting." *FoxIO Blog*, September 26, 2023. URL: https://blog.foxio.io/ja4+-network-fingerprinting

**[88]** FoxIO. "JA4T: TCP Fingerprinting." *FoxIO Blog*, April 23, 2024. URL: https://foxio.io/blog/ja4t-tcp-fingerprinting

**[89]** M. Husák, M. Čermák, T. Jirsík, and P. Čeleda. "HTTPS Traffic Analysis and Client Identification Using Passive SSL/TLS Fingerprinting." *EURASIP Journal on Information Security*, Vol. 2016, Article 6, 2016. DOI: 10.1186/s13635-016-0030-7.

**[90]** M. Zalewski. "p0f v3: Passive Fingerprinter." Tool documentation, *lcamtuf.coredump.cx*, 2014. URL: https://lcamtuf.coredump.cx/p0f3/

**[91]** Akamai Technologies. "Bots Tampering with TLS to Avoid Detection." *Akamai Security Blog*, May 15, 2019. URL: https://www.akamai.com/blog/security/bots-tampering-with-tls-to-avoid-detection

**[92]** Akamai Technologies. "Evading Link Scanning Security Services with Passive Fingerprinting." *Akamai Security Blog*, December 9, 2020. URL: https://www.akamai.com/blog/security/evading-link-scanning-security-services-with-passive-fingerprinting

**[93]** P. A. Grassi, J. L. Fenton, et al. "Digital Identity Guidelines: Authentication and Lifecycle Management." *NIST Special Publication 800-63B*, June 2017 (with subsequent updates). URL: https://csrc.nist.gov/pubs/sp/800/63/b/upd2/final

**[94]** T. K. Abel. "What Client-Side Trust Is Actually Worth." *tomabel.ee*, 2026. URL: https://tomabel.ee/disclosures/what-client-side-trust-is-actually-worth. Self-citation: the author's own published essay, cited as an applied case study, not a peer-reviewed source.

**[95]** T. K. Abel. "The Achilles' Heel of Estonia's e-State — Smart-ID / eID Research." *tomabel.ee*, 2026. URL: https://tomabel.ee/disclosures/smart-id-achilles-heel. Self-citation: the author's own published disclosure report, cited as an applied case study, not a peer-reviewed source.

**[96]** M. Thomson, Ed., and C. Benfield, Ed. "HTTP/2." *RFC 9113*, IETF, June 2022. DOI: 10.17487/RFC9113.

**[97]** M. Bishop, Ed. "HTTP/3." *RFC 9114*, IETF, June 2022. DOI: 10.17487/RFC9114.

**[98]** J. Iyengar, Ed., and M. Thomson, Ed. "QUIC: A UDP-Based Multiplexed and Secure Transport." *RFC 9000*, IETF, May 2021. DOI: 10.17487/RFC9000.

**[99]** K. Oku and L. Pardue. "Extensible Prioritization Scheme for HTTP." *RFC 9218*, IETF, June 2022. DOI: 10.17487/RFC9218.
