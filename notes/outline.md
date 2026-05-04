# Outline — SoK: The Architectural and Economic Ceilings of Client-Side Anti-Automation

---

## 1. Introduction

### 1.1 The Terminology Problem: Why the Field Needs a Taxonomy
- The bot mitigation industry lacks a unified vocabulary; vendors describe the same architectures using incompatible terminology.
- "Bot detection" conflates five architecturally distinct mechanisms under one term. This imprecision obstructs comparative analysis, academic research, and defender evaluation.
- Recent innovations — Private Access Tokens, behavioral biometrics, and device-bound session credentials — have fragmented the landscape further.
- An SoK is warranted to (a) name and define architecturally distinct classes of defense, (b) isolate their structural limits, and (c) provide a common evaluation framework for future work.
- **Citations:** [4, 6, 73]

### 1.2 Contributions & Scope
- **C1 — Five-Architecture Taxonomy:** Stateless VM Attestation, Stateful Behavioral Telemetry, Behavioral Biometrics & Sensor Telemetry, Platform Anonymous Attestation (PATs), and Hardware-Anchored Determinism. Compute-Bound Challenges correctly demoted to auxiliary mechanism under Stateless VM.
- **C2 — Generalized L1-L4 Defense-in-Depth Framework:** Generalized from Botguard to any register-based JS VM, expanded L1 to include sensor telemetry, and introduced the temporal constraint (Defender AST Obfuscator vs. Attacker Symbolic Execution Engine).
- **C3 — Conceptual Microeconomic Analysis:** Fixed, variable, and temporal attacker cost types; conjunctive cost of anti-detect browsers (`Cost_proxy + Cost_profile + Cost_license`); human labor as global cost floor for behavioral biometrics.
- **C4 — Centralization vs. Anonymity Trade-off:** Identification of the defining open problem in anonymous attestation.

### 1.3 Threat Model: A Dual-Axis Framework
- **Axis A — Authentication State:** Anonymous vs. Authenticated.
- **Axis B — Attack Objective:** Resource Exhaustion/Scraping vs. Account Takeover/Fraud.
- **Quadrant I (Anonymous + Scraping):** Stateless VM, Behavioral Biometrics, Compute-Bound Challenges. OWASP OAT [66] anchor.
- **Quadrant II (Anonymous + ATO):** Stateful Telemetry (risk scoring on login flows), Platform Anonymous Attestation (PATs). OWASP OAT [66] anchor.
- **Quadrant III (Authenticated + Scraping):** Rare; session-bound rate limiting. NIST SP 800-63-3 [65] anchor.
- **Quadrant IV (Authenticated + ATO):** Hardware-Anchored Determinism (DBSC, Passkeys). NIST SP 800-63-3 [65] anchor.
- **Table:** 2×2 quadrant matrix with representative defenses.

---

## 2. Background & Related Work

### 2.1 A Brief History of Client-Side Anti-Automation
- Pre-2005: Server-side rate limiting, IP blacklisting. No client-side execution.
- 2005–2012: CAPTCHA era (text, image, audio). Cat-and-mouse dynamic with OCR and ML solvers. [71, 73]
- 2010–2017: JavaScript challenge era (reCAPTCHA v2, early Turnstile). JavaScript execution as a proxy for browser legitimacy.
- 2017–2020: VM-based attestation (Botguard, Kasada). Custom register-based VMs executing encrypted bytecode. [24]

### 2.2 From CAPTCHAs to JavaScript VMs
- CAPTCHA limitations: accessibility, user friction, ML solvers achieving superhuman accuracy.
- JS VMs: shift from proving humanness through task completion to proving humanness through execution environment integrity.
- The fundamental insight: the defender controls the execution specification; the attacker controls the execution substrate. This asymmetry defines the field. [6, 24]

### 2.3 From Probabilistic Scoring to Hardware-Anchored Determinism
- Probabilistic scoring: Botguard produces confidence scores; reCAPTCHA v3 returns 0.0–1.0 risk scores. Both operate on anonymous traffic.
- Hardware-anchored determinism: FIDO2/WebAuthn [31] proves cryptographic possession. DBSC [36, 37] binds cookies to TPM/Secure Enclave keys. Both require prior enrollment/authentication (NIST 800-63 [65]).
- The non-substitutability: hardware-anchored mechanisms cannot screen anonymous traffic. This is not a flaw; it is a structural property of the IAM model. [65]

### 2.4 The Emergence of Anonymous Attestation (Privacy Pass / PATs)
- Privacy Pass [41]: 1-RTT anonymous token issuance using VOPRF + DLEQ proofs.
- IETF standardization [38, 39, 40]: Architecture, HTTP scheme, and issuance protocols.
- Apple PAT deployment (iOS 16+, 2022) [44]: Hardware-backed attestation via Secure Enclave, issuing anonymized tokens via RSA blind signatures.
- WICG Private State Token API [45]: Browser-level anonymous attestation integration.
- The critical shift: PATs technically bridge the "Anonymous Authentication Gap" — providing deterministic attestation without identity disclosure. However, they introduce vendor centralization as a structural property. [42, 43]

### 2.5 The Economics-of-Security Lens
- Anderson & Moore (2006) [46]: Information security is fundamentally an economic problem; defenders and attackers optimize under different budget constraints.
- Herley & Florêncio (2009) [47]: Underground economy pricing theory; "nobody sells gold for the price of silver."
- Moore (2010) [48]: Cybersecurity cost-benefit frameworks.
- Application: Client-side anti-automation is best understood as an economic arms race, not a cryptographic one. The appropriate analytical framework is microeconomic cost analysis, not security proof theory.

---

## 3. Systematization Methodology

### 3.1 Scope and Inclusion Criteria
- **Scope:** Client-side anti-automation mechanisms deployed in web browsers. The attacker controls the execution environment (browser/OS).
- **Inclusion Criteria:** Technologies must be (a) deployed in production by a major vendor or platform, (b) documented in academic literature, IETF/W3C standards, or peer-reviewed grey literature, and (c) impose costs on adversaries through client-side execution.
- **Exclusions:** Purely server-side bot detection (TLS fingerprinting at CDN edge, server-side WAF heuristics, network-layer DDoS scrubbing, application-layer rate limiting). These operate under a different economic model — the attacker does not control the inspection substrate.
- **Vendor Coverage:** Google (Botguard, reCAPTCHA v3, DBSC), Cloudflare (Turnstile, Privacy Pass deployment), Kasada (VM-based defense), DataDome (stateful telemetry), Apple (PATs), WICG/IETF (standards).

### 3.2 Systematization Approach: Capability-Based Threat Modeling
- **Methodology:** Adopt capability-based threat modeling. Extract attacker requirements from the literature (compute capacity, IP reputation inventory, human labor for RE, ML synthesis capability) and map them against defender architectural paradigms.
- **Attacker Capability Dimensions:**
  1. Compute capacity (GPU/CPU for ML inference, symbolic execution, VM execution)
  2. IP reputation inventory (residential proxy pool size and quality)
  3. Human labor (RE engineering, click-farm operations)
  4. ML synthesis capability (GAN/transformer models for behavioral mimicry)
  5. Malware distribution (PPI network access for device compromise)
- **Why capabilities, not intentions:** This paper maps structural ceilings, not attacker motivations. Capability-based modeling isolates what is architecturally possible regardless of threat actor sophistication.

### 3.3 Source Corpus, Search Strategy, and PRISMA Flow
- **Databases Searched:** IEEE Xplore, ACM Digital Library, arXiv, Google Scholar, IETF Datatracker, W3C TR.
- **Search Queries:** `("bot mitigation" OR "browser fingerprinting" OR "anti-automation" OR "bot detection") AND ("economics" OR "cost" OR "attestation" OR "architecture")`; supplementary queries: `("Privacy Pass" OR "Private Access Token") AND ("security" OR "deployment")`; `("mouse dynamics" OR "behavioral biometrics" OR "sensor telemetry") AND ("bot detection" OR "automation")`; `("JavaScript obfuscation" OR "VM deobfuscation") AND ("symbolic execution" OR "automated")`.
- **Date Range:** 2010–2025, with foundational papers (Saltzer 1975) included for historical context.
- **Source Corpus:** Academic publications from top-4 security conferences (IEEE S&P, USENIX Security, CCS, NDSS), IETF/W3C standards, and peer-reviewed grey literature (vendor technical whitepapers, industry reports, malware analysis reports). Reviewed 75+ publications.

### 3.4 PRISMA Flow Diagram → See `figures/prisma-flow.tex`
- **Identification:** n = 320 records from database searches.
- **Screening:** n = 198 after duplicate removal and title/abstract screening against inclusion criteria.
- **Eligibility:** n = 122 full-text articles assessed for architectural relevance and verifiability.
- **Included:** n = 75 publications in final synthesis (12 standards, 52 academic papers, 11 grey literature).
- **PRISMA-compliant justification for counts provided in prose.**

### 3.5 Exclusions and Out-of-Scope Domains
- Server-side WAF heuristics (different economic model; attacker does not control inspection substrate).
- Network-layer DDoS scrubbing (operates at OSI L3/L4; not client-side).
- Application-layer rate limiting (operates at server edge; independent of client execution).
- Cryptographic authentication protocols per se (FIDO2 is included only as it relates to the hardware-anchored paradigm within the taxonomy).

### 3.6 Taxonomy Dimensions
- Ten comparison dimensions (defined for Section 4.6 table):
  1. Architecture Class
  2. Representative Implementations
  3. Mechanism Summary
  4. Defender Investment Type
  5. Attacker Cost Type (Fixed / Variable / Mixed / Temporal)
  6. Dominant Scaling Constraint
  7. Structural Ceiling
  8. Anonymous Traffic Compatible?
  9. Hardware Dependency
  10. Vendor Oligopoly Risk?

---

## 4. The Systematization Matrix: Five Primary Architectures

### 4.1 Stateless VM Attestation
- **Mechanism:** Custom register-based JavaScript VM executes encrypted bytecode; measures environmental integrity (L1), uses self-modifying code (L2), traps introspection (L3), enforces chronometric constraints (L4). Point-in-time execution; no persistent profile.
- **Representative Implementations:** Google Botguard, Cloudflare Turnstile Managed Challenge, Kasada Polymorphic VM.
- **Attacker Cost Imposed:** Per-execution proxy + compute cost; fixed RE engineering cost (with automation driving toward temporal); variable stealth maintenance cost per compile rotation.
- **Auxiliary Mechanisms (4.1.1): Compute-Bound Challenges:** WASM-based PoW that raises per-execution compute cost. Structurally limited by 100× desktop-to-mobile compute disparity; cannot stand alone as a primary pillar. Demoted to auxiliary status.
- **Structural Ceiling:** IP reputation market exhaustion (Tragedy of the Commons). At industrial scale, subnet-level reputation burns make all IPs on a proxy pool non-viable, independent of VM bypass sophistication. [6, 59]
- **Citations:** [6, 24, 26, 27, 30, 59, 60, 63]

### 4.2 Stateful Behavioral Telemetry
- **Mechanism:** Long-term browser profile accumulation; behavioral history scored over weeks-to-months; risk thresholds determine challenge escalation. Persistent identifiers (cookies, fingerprinting) aggregate signals.
- **Representative Implementations:** Google reCAPTCHA v3, DataDome, Human Security (PerimeterX).
- **Attacker Cost Imposed:** Profile-aging inventory cost (2–6 weeks of human-like browsing before favorable scoring); plus per-execution cost.
- **The Conjunctive Cost of Anti-Detect Browsers:** Anti-detect browsers (Multilogin, GoLogin, AdsPower) virtualize profiles but do not replace proxies. The attacker must bind a high-quality residential proxy to each profile — an aged Google profile connected via datacenter IP will be burned instantly. Cost = `Cost_residential_proxy + Cost_aged_profile + Cost_software_license`. This is conjunctive (stacked), not alternative. [13, 58]
- **Structural Ceiling:** Latency constraints (time-to-production delay cannot be bypassed by spending); anti-detect market commoditization drives down profile cost but proxy cost remains inelastic.
- **Citations:** [6, 10, 11, 14, 62, 64]

### 4.3 Behavioral Biometrics & Sensor Telemetry
- **Mechanism:** Measures the dynamics of human interaction — mouse kinematics (velocity, acceleration, Bezier-curve fitting), scroll patterns, click-timing, touch-event pressure, accelerometer polling. The defender measures *how* the user interacts, not just *what* environment they use.
- **Representative Implementations:** BeCAPTCHA research prototypes [15, 16], commercial behavioral biometrics in DataDome/Human Security, reCAPTCHA v3 interaction signals.
- **Attacker Cost Imposed:** Defined as minimization function: `Cost_Bypass = min(Cost_ML_Inference, Cost_Human_Labor)`.
  - **ML Synthesis Path:** GAN-based trajectory generators [16, 18] must produce believable human-like Bezier curves and timing jitters at scale. Computational overhead scales with throughput.
  - **Human Labor Path:** Routing the challenge to CAPTCHA-solving farms (2Captcha, Anti-Captcha) or click-farms where workers manually wiggle the mouse and click for a per-token labor fee. Documented underground economy [51, 52].
  - **Economic Implication:** Human labor sets the absolute global price ceiling for bypassing behavioral biometrics. If ML synthesis costs more than human labor, the attacker defaults to the labor market.
- **Structural Ceiling:** The defender's ability to raise interaction complexity above the cost threshold where human labor becomes economically unsustainable at industrial throughput. This is a labor-market arbitrage, not a technological arms race.
- **Citations:** [15, 16, 17, 18, 19, 20, 21, 22, 51, 52]

### 4.4 Platform/OS-level Anonymous Attestation (Privacy Pass / PATs)
- **Mechanism:** Hardware-backed attestation (via OS/device enclave like Apple Secure Enclave) generates cryptographic tokens (RSA blind signatures or VOPRF-based) without revealing user identity. Tokens are redeemed at web origins for anonymous, deterministic "humanness" verification. Token issuance is rate-limited per-device.
- **Representative Implementations:** Apple Private Access Tokens (iOS 16+, macOS Ventura) [44], Cloudflare/Fastly Privacy Pass deployment, WICG Private State Token API [45].
- **Attacker Cost Imposed:** Device compromise required — attacker must either (a) extract attestation keys from the hardware enclave (prohibitively expensive) or (b) compromise legitimate user devices via PPI malware networks to obtain signed attestations [53, 54, 55]. Cannot be farmed at scale without physical device access.
- **Structural Ceiling:** Vendor centralization — Apple, Google, Microsoft control the attestation root of trust. Whoever controls the root controls who may access the web anonymously. This is not a cryptographic weakness but a structural economic property. Additionally, token issuance is rate-limited per-device, capping throughput even for compromised devices.
- **Citations:** [38, 39, 40, 41, 42, 43, 44, 45]

### 4.5 Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys, WebAuthn)
- **Mechanism:** Cryptographic proof-of-possession of a private key housed in hardware (TPM, Secure Enclave). DBSC [36] periodically proves session cookie possession without re-authentication. FIDO2/WebAuthn [31] proves credential possession during authentication. Both are deterministic — either the key is present or it is not.
- **Representative Implementations:** Google DBSC (Chrome), FIDO2/WebAuthn (all major browsers), Passkeys (Apple, Google, Microsoft).
- **Attacker Cost Imposed:** The attacker does not forge the TPM attestation. Instead, they bypass via device compromise through PPI malware networks. The attacker buys malware installs (RedLine [54], Lumma [55] at $75–$200/mo [56]) at per-infection rates, exports session cookies, or proxies through the compromised device. The economic bypass cost is the black-market price of a malware infection, not the mathematical hardness of the attestation protocol.
- **Structural Ceiling:** Three-fold: (a) user adoption friction, (b) identity binding (inapplicable to anonymous traffic), and (c) the black-market equilibrium price of a successful malware infection on the target demographic's machine [56]. This third ceiling is the most economically significant — if PPI infection cost < resource value protected, the ceiling is breached.
- **Citations:** [31, 32, 33, 34, 35, 36, 37, 53, 54, 55, 56, 57]

### 4.6 Comparative Taxonomy (Grand Table) → See `figures/taxonomy-table.tex`
- 10-column table comparing all five architectures across taxonomy dimensions.
- **Table structure:**
  | Architecture | Implementations | Mechanism | Defender Investment | Attacker Cost Type | Scaling Constraint | Structural Ceiling | Anonymous? | HW Dependency | Oligopoly Risk |
  |---|---|---|---|---|---|---|---|---|---|

### 4.7 The Anonymous-Authentication Spectrum (Figure) → See `figures/auth-spectrum.tex`
- Visual spectrum from Fully Anonymous + Probabilistic (left) → Identified + Hardware-Enrolled Authentication (right).
- Resolves the old "Anonymous Authentication Gap" misconception: PATs occupy the center, bridging the gap but introducing vendor trust as a new dimension.

---

## 5. Generalized Defense-in-Depth: The L1-L4 Stack for Stateless VMs

### 5.1 Elevating Botguard-Specific Layers to a General Framework
- The L1-L4 framework was originally described in the context of Botguard. This section generalizes it to any register-based JS VM defense, including Cloudflare Turnstile Managed Challenge and Kasada.
- The framework decomposes stateless execution-time defenses into four discrete, measurable layers. Each layer imposes a distinct cost type on the adversary.

### 5.2 L1: Environmental Introspection & Sensor Telemetry
- **Static:** `navigator.webdriver` detection, WebGL rendering artifacts, DOM prototype chain integrity, User-Agent consistency. Detectable properties: 15–20 in standard headless Chrome.
- **Dynamic (EXPANDED):** Mouse kinematics, scroll events, click-timing, accelerometer polling, touch-event pressure. The defender measures both *environment* and *behavior* at L1.
- **Cost Imposed:** Variable compute cost. Generating realistic human-like Bezier curves and timing jitters at scale requires ML models (GANs trained on human movements). However, true cost bounded by `min(Cost_ML_Inference, Cost_Human_Labor)` — the global human labor market. [15, 16, 18, 51, 52]
- **Cost Type:** Mixed (Variable compute OR Variable labor).

### 5.3 L2: Obfuscation & Polymorphism
- **Mechanism:** Self-modifying code, runtime opcode construction (e.g., register 274 in Botguard), LOADSTRING/LOADOP dynamic instruction injection, periodic compile rotation.
- **Cost Imposed:** Temporal cost — the attacker's RE cost is a recurring fixed cost (step function) bounded by ratio of Time-to-Defeat (T_RE) to Compile Lifespan (T_Life).
- **Critical Insight:** T_RE is increasingly compute-driven, not human-driven. State-of-the-art attackers use automated deobfuscation, symbolic execution (KLEE, Triton) [25, 26], and AST-level ML transformers [28, 29] to automatically map new opcodes. The temporal race: **defender's AST obfuscator vs. attacker's symbolic execution engine**.
- **Cost Type:** Temporal (recurring fixed cost, increasing with automation).

### 5.4 L3: Execution Traps
- **Mechanism:** Console methods bound to trap functions; logging any variable corrupts the instruction stream; anti-debugger hooks; prototype chain integrity checks.
- **Cost Imposed:** Mixed — initial automated RE to identify trap logic (fixed/temporal), but maintaining trap awareness at scale requires per-execution orchestration overhead (variable).
- **Cost Type:** Mixed (Fixed/Temporal + Variable).

### 5.5 L4: Chronometric Integrity
- **Mechanism:** Continuous polling of `performance.now()` and `Date.now()`; time delta mutates a seed value that determines bytecode decryption key. Deviations of ~50–200ms trigger invalid token generation. Server-side timestamp freshness enforcement prevents batch generation.
- **Cost Imposed:** Per-execution synchronization overhead (variable). Timer spoofing must maintain consistency across multiple clock sources simultaneously.
- **Cost Type:** Variable.

### 5.6 Qualitative Cost Analysis: Fixed vs. Variable vs. Temporal
| Layer | Cost Type | Dominant Driver | Scalability Profile |
|-------|-----------|-----------------|---------------------|
| L1 (Environmental) | Mixed (Variable) | ML inference or human labor per token | Scales with throughput |
| L2 (Obfuscation) | Temporal | RE automation pipeline speed vs. compile rotation cadence | Step function at each rotation event |
| L3 (Traps) | Mixed | Automated RE for trap identification + per-execution awareness | Scales weakly with throughput |
| L4 (Chronometrics) | Variable | Per-execution timer orchestration and synchronization | Scales with throughput |

### 5.7 The Temporal Constraint: Defender AST Obfuscator vs. Attacker Symbolic Execution
- Compile rotation does not create an infinite barrier. It creates a race condition between the defender's CI/CD compile-deployment cadence and the attacker's automated RE pipeline.
- **The Defender Side:** Compile rotation is automated (CI/CD pipeline); the marginal cost of pushing a new compile is negligible. Compile complexity is bounded by JavaScript runtime constraints.
- **The Attacker Side:** Automated deobfuscation via symbolic execution, differential analysis across compile versions [26], and AST-level neural models that predict opcode mappings [28, 29] compresses T_RE below manual RE timelines.
- **The Tipping Point:** The structural ceiling is reached when the attacker automates the un-mapping of the VM faster than the defender's pipeline can push new compiles. At that point, T_RE < T_Life consistently, and the defense provides only transient value.
- **Citations:** [24, 25, 26, 27, 28, 29, 30]

### 5.8 Why the Stack is Bounded (The Forgery Principle)
- The adversary controls the execution substrate. Every measurement the VM takes is of data the adversary can observe and intercept. An anti-tamper layer raises the cost of interception but cannot change the structural fact that the defended software executes in an environment the adversary owns.
- This is why software-only attestation is architecturally bounded: **this is a forgery problem, not a cryptanalysis problem.** No amount of VM complexity changes the paradigm from the latter to the former.
- The defender can raise forgery costs to unprofitable levels — and does — but the ceiling is economic, not cryptographic.

---

## 6. The Microeconomic Constraints of Forgery

### 6.1 The Temporal Arms Race: Automated Deobfuscation and the Collapse of T_RE
- Compile rotation does not create an infinite barrier. It creates a race condition between the defender's CI/CD pipeline and the attacker's RE pipeline.
- **Critical insight:** Advanced attackers have shifted from manual RE to automated deobfuscation — symbolic execution [25, 26], differential analysis across compile versions, and AST-level neural models [28, 29] that predict opcode mappings.
- The structural ceiling is reached when the attacker automates the un-mapping of the VM faster than the defender's pipeline can push new compiles. The defender's maintenance cost is automation-driven and low; the attacker's RE cost is increasingly compute-driven rather than labor-driven.
- **Citations:** [24, 25, 26, 27, 28, 29, 30]

### 6.2 Human Labor as the Global Cost Floor
- **NEW SECTION.** For any client-side challenge requiring human-like interaction — behavioral biometrics, CAPTCHAs, sensor telemetry — the attacker's bypass cost is floored by the global market for human labor.
- CAPTCHA-solving farms (2Captcha, Anti-Captcha) and low-wage click-farms set a hard price ceiling that ML synthesis cannot undercut without massive upfront training investment [51, 52].
- The defender's goal is to raise per-token interaction complexity to the point where human labor becomes economically unsustainable at industrial throughput. This is not a technological arms race; it is a **labor-market arbitrage**.
- Empirical documentation: Motoyama et al. (2010) [51] measured CAPTCHA-solving at ~$1 per 1,000 solved CAPTCHAs; rates have declined since.
- **Citations:** [51, 52]

### 6.3 The Variable Cost Weaponization (Proxy Depletion)
- Forcing attackers to consume real-world proxy bandwidth (residential IPs) is a sound software defense because proxy depletion creates a non-linear scaling penalty.
- Residential proxy supply is finite. As the attacker scales throughput, they exhaust cheap commodity IPs and must either pay premium rates or accept higher failure rates. This is a supply-constrained variable cost that cannot be amortized.
- Published proxy market documentation shows commodity pools at ~$0.50/GB vs. premium unburned residential IPs at $10–15/GB — a 20×–30× spread [60, 62, 63, 64].
- **Citations:** [60, 62, 63, 64]

### 6.4 Reputation as an Exhaustible Resource (Tragedy of the Commons)
- IP reputation is a commons. All attackers sharing a residential proxy pool degrade that pool's reputation collectively.
- The defender's subnet-level scoring creates a Tragedy of the Commons among attackers: each attacker's volume benefits themselves but imposes a negative externality (reputation degradation) on all other attackers sharing the same IP range. This structurally advantages the defender at scale.
- The effective failure rate is a function of broader proxy-market equilibrium, not merely individual throughput. This makes cost prediction at scale a market-level, not individual-level, exercise.
- **Citations:** [59, 60]

### 6.5 The Conjunctive Cost of Profile Virtualization
- **CRITICAL FIX.** Anti-detect browsers (Multilogin, GoLogin, AdsPower) are not an "alternative" to proxy rotation. They virtualize browser profiles (fingerprints, cookies, local storage, WebGL canvas) but do not alter the network origin IP.
- The attacker's cost formula for stateful telemetry bypass is **conjunctive**: `Cost_residential_proxy + Cost_aged_profile + Cost_software_license`.
- The residential proxy is still mandatory — an aged Google profile in Multilogin connected via an AWS datacenter IP will be burned by reCAPTCHA v3 instantly. The anti-detect browser raises the fixed inventory cost but does not eliminate the variable proxy cost.
- This is a **stacked**, not substituted, cost structure. Prior work has sometimes framed anti-detect browsers as proxy alternatives; this analysis corrects that framing.
- **Citations:** [13, 58]

### 6.6 Boundedness, Not Doom
- Software-only defenses are economically bounded by the proxy supply market, the temporal arms race, and the ML synthesis arms race.
- They are not "structurally doomed." The ceiling is economic, not cryptographic. Within their design envelopes, they provide effective deterrence against adversaries whose attack value is below the cost ceiling.
- The appropriate analytical stance is: software-only defenses operate under a forgery model with economic ceilings, not a cryptanalysis model with mathematical guarantees.

---

## 7. Industry Trajectory & Emerging Standards

### 7.1 DBSC and the Session-Hijacking Threat Model
- DBSC [36, 37]: TPM-backed cryptographic binding of session cookies to device. Periodic proof-of-possession without re-authentication.
- Targets the session-hijacking threat model (NIST 800-63 Authenticated/ATO quadrant [65]). Cannot be applied to anonymous traffic.
- **Infostealer Economy Analysis:** The structural ceiling of DBSC is not user friction. The thriving PPI malware market [53, 54, 55, 56] allows attackers to bypass DBSC by compromising the legitimate user's device and exporting session state. The economic bypass cost is the black-market price of a malware infection, not the mathematical hardness of the attestation protocol.
- **Citations:** [36, 37, 53, 54, 55, 56, 57]

### 7.2 Passkeys and the Credential-Phishing Threat Model
- Passkeys (FIDO2/WebAuthn [31]): hardware-enrolled cryptographic authentication. Eliminates credential phishing by removing shared secrets.
- Structural limitation: requires prior enrollment (NIST 800-63 [65]). Non-substitutable for anonymous traffic screening.
- Security posture: Kuchhal et al. (2023) [32] found that only 4.4% of authenticators carry Level 2+ certification offering malware resistance. Tarrach et al. (2024) [33] identified message integrity gaps accessible to browser extensions.
- The infostealer threat applies symmetrically to Passkeys: compromised devices can export session state post-authentication.
- **Citations:** [31, 32, 33, 34, 35]

### 7.3 Privacy Pass and the Anonymous-Attestation Trade-off
- PATs [38, 39, 40] provide deterministic anonymous attestation — technically closing the "Anonymous Authentication Gap."
- However, this comes at a structural cost: vendor centralization. Apple, Google, Microsoft control the attestation root of trust [44, 45]. This is not a weakness of the protocol per se but a structural economic property: whoever controls the attestation root of trust controls who may access the web anonymously.
- Rate-limited issuance [43] limits the compromised-device threat but also creates a throttling vector for legitimate users behind CGNAT or shared IPs.
- **Citations:** [38, 39, 40, 41, 42, 43, 44, 45]

### 7.4 The Centralization vs. Anonymity Dilemma
- **The Trilemma:** The web faces a three-way trade-off: (a) anonymous access, (b) deterministic bot resistance, (c) decentralized trust.
  - **Privacy Pass / PATs:** Achieves (a) and (b), sacrifices (c).
  - **Traditional VMs (Botguard):** Achieves (a) and (c), sacrifices (b) at scale.
  - **Hardware-Anchored Auth (DBSC/Passkeys):** Achieves (b) and (c), sacrifices (a).
- **No existing architecture satisfies all three.** This is the defining structural challenge of the field.
- The trilemma is presented as a characterization of the current state, not a proven impossibility result. Research into decentralized anonymous attestation may resolve it.

---

## 8. Open Problems & Future Research

### 8.1 The Centralization vs. Anonymity Trade-off in PATs
- Privacy Pass and PATs have solved the *technical* problem of anonymous deterministic attestation but created an *economic and political* problem: a vendor oligopoly on "humanness."
- Research needed on decentralized anonymous attestation (e.g., zero-knowledge proofs of personhood, decentralized issuer networks) that does not require trusting Apple, Google, or Microsoft.
- Key constraints: rate-limiting without identity, Sybil-resistance without central enrollment, cryptographic unlinkability with abuse prevention.

### 8.2 Standardized Benchmarking (The "Bot-Bench" Problem)
- Academia lacks a "Bot-Bench" — a standardized, ethical testbed for evaluating VM chronometric defenses without violating vendor ToS.
- Current evaluations rely on grey-hat reverse engineering or small-scale PoCs that vendors invalidate through compile rotation.
- Needed: A reproducible, vendor-neutral VM test harness with known ground truth for evaluating L1-L4 layer effectiveness. This would transform anecdotal RE into systematic measurement.
- **Citations:** [23, 24]

### 8.3 Privacy Regulation vs. Stateful Mitigation (GDPR / Cookie Deprecation)
- GDPR, ePrivacy Directive, and third-party cookie deprecation break the long-term profile-aging model underpinning stateful telemetry (reCAPTCHA v3, DataDome).
- As browsers restrict persistent identifiers (ITP, ETP, Total Cookie Protection), the economic ceiling of stateful defenses actually *rises* (they become less effective), yet vendors continue to market them.
- The tension between privacy regulation and stateful bot mitigation is under-studied in academic literature. This represents a significant research gap.
- **Citations:** [6, 14]

### 8.4 The Temporal Arms Race: Formal Models of Compile Rotation
- There is no formal model in the literature for the T_RE vs. T_Life dynamic in polymorphic VM defenses, particularly when T_RE is driven by automated symbolic execution rather than human labor.
- Research needed on quantitative frameworks for measuring how quickly automated deobfuscation pipelines adapt to compile rotation, and what defender deployment cadences are economically optimal against compute-driven attackers.
- Key questions: What is the optimal compile rotation frequency given automated RE? Can compile obfuscation diversity (not just rotation) meaningfully increase T_RE? What are the information-theoretic limits of VM diversity in a JavaScript runtime?
- **Citations:** [24, 25, 26, 27, 28]

---

## 9. Conclusion
- Summary of the five-architecture taxonomy and L1-L4 framework.
- Reiteration that the paper provides analytical clarity rather than empirical breakthroughs.
- The field's defining challenge has shifted: PATs have technically closed the "Anonymous Authentication Gap," but the **Centralization vs. Anonymity Trade-off** now occupies that position.
- Client-side anti-automation operates under a forgery model with economic ceilings, not a cryptanalysis model with mathematical guarantees. This insight, though not new, is given systematic structure through the taxonomy and cost-type framework presented here.
- Call for future work on decentralized anonymous attestation, standardized benchmarking, and formal models of the temporal arms race.

---

## References
- See `notes/bibliography.md` for the complete 75-reference bibliography.
