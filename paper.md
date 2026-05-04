# SoK: The Architectural and Economic Ceilings of Client-Side Anti-Automation

---

**Authors:** Abel, T. K.

**Repository:** https://github.com/tomkabel/google-botguard-security-research

**Keywords:** Client-side attestation, bot mitigation, JavaScript virtual machine, browser fingerprinting, behavioral biometrics, Privacy Pass, Private Access Tokens, device-bound session credentials, anti-automation economics, systematization of knowledge

---

## Abstract

Client-side anti-automation — the set of techniques that distinguish human-driven browsers from automated agents — has evolved through five architecturally distinct paradigms over the past fifteen years. Despite this rich design space, the industry lacks a unified taxonomy. Vendors describe structurally different defenses using overlapping and sometimes incompatible terminology, and recent innovations — Private Access Tokens (PATs), behavioral biometrics with sensor telemetry, and device-bound session credentials — have fragmented the landscape further. This paper presents a Systematization of Knowledge (SoK) of client-side anti-automation architectures. We propose a comparative taxonomy of five primary defense classes: Stateless VM Attestation, Stateful Behavioral Telemetry, Behavioral Biometrics & Sensor Telemetry, Platform/OS-level Anonymous Attestation (Privacy Pass / PATs), and Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys). We further generalize the four-layer defense-in-depth framework (L1–L4) originally observed in Google's Botguard VM into a vendor-neutral model applicable to any register-based JavaScript VM defense, expanded to include sensor telemetry under environmental introspection. We provide a conceptual microeconomic analysis of attacker costs across all five paradigms, distinguishing fixed, variable, and temporal cost types, and we identify three critical structural corrections to prior economic framing: (a) anti-detect browsers impose a conjunctive, not alternative, cost structure (`Cost_proxy + Cost_profile + Cost_license`); (b) human labor (CAPTCHA-solving farms, click-farms) sets the global cost floor for bypassing behavioral biometrics; and (c) the temporal arms race in VM obfuscation is increasingly a race between the defender's automated compile pipeline and the attacker's symbolic execution engine, not between the defender's compiler and the attacker's manual reverse engineer. Finally, we identify the Centralization vs. Anonymity Trade-off as the defining open problem in anonymous attestation: while Privacy Pass and PATs have technically closed the long-standing "Anonymous Authentication Gap," they introduce an economic and political dependency on a vendor oligopoly (Apple, Google, Microsoft) controlling the attestation root of trust. The paper includes a formal PRISMA flow diagram, a Grand Taxonomy Table comparing all five architectures across ten dimensions, and an Anonymous-Authentication Spectrum figure. This work is a contribution in systematization: it provides analytical clarity rather than empirical breakthroughs, and it establishes a common vocabulary and evaluation framework for future research in client-side anti-automation.

**Contributions:**
1. A unified taxonomy of five client-side anti-automation architectures, including the previously omitted Privacy Pass / PAT and Behavioral Biometrics & Sensor Telemetry paradigms, with Compute-Bound Challenges correctly demoted to an auxiliary mechanism.
2. A generalized defense-in-depth framework (L1–L4) for stateless VM attestation, with a novel temporal constraint analysis that accounts for automated deobfuscation via symbolic execution and AST-level machine learning.
3. A conceptual microeconomic analysis of forgery costs, distinguishing fixed, variable, and temporal attacker expenditures, and correctly modeling anti-detect browsers as a conjunctive cost rather than an alternative.
4. Identification of the Centralization vs. Anonymity Trade-off as the defining open problem of anonymous attestation, accompanied by three additional research gaps.

---

## 1. Introduction

### 1.1 The Terminology Problem: Why the Field Needs a Taxonomy

Client-side anti-automation is the set of techniques that web services deploy to distinguish browser sessions driven by human users from those driven by automated scripts. Over the past fifteen years, the field has evolved from text-distortion CAPTCHAs to register-based JavaScript virtual machines, from stateless point-in-time execution to stateful behavioral telemetry spanning weeks of profile aging, and from purely probabilistic confidence scores to cryptographic hardware-anchored attestations [73, 24, 31]. This evolution has produced a rich but disorganized design space. Vendors describe structurally different mechanisms using overlapping and sometimes incompatible terminology: "bot detection" may refer to a stateless VM executing encrypted bytecode (Botguard [60]), a long-term behavioral scoring engine (reCAPTCHA v3 [62]), or a device-attestation protocol (Apple PAT [44]). "Fingerprinting" can denote passive environmental introspection (L1), active behavioral telemetry (L4), or cryptographic token issuance (Privacy Pass [38]).

This terminological imprecision obstructs comparative analysis, complicates vendor evaluation, and impedes academic research. A researcher seeking to understand the structural limits of a particular defense class must first reverse-engineer the vendor's terminology to identify which architecture is actually being described. The field lacks a common vocabulary and a shared framework for evaluating which structural ceilings are inherent to an architectural choice versus which are implementation limitations.

Recent innovations have further fragmented the landscape. Apple's deployment of Private Access Tokens (PATs) in iOS 16 [44] introduced hardware-backed anonymous attestation at platform scale. The WICG Private State Token API [45] and IETF Privacy Pass standardization [38, 39, 40] have brought cryptographic anonymous attestation into browser infrastructure. Google's Device Bound Session Credentials (DBSC) [36, 37] have extended hardware-anchored determinism from authentication to session maintenance. Meanwhile, academic research in behavioral biometrics has demonstrated that mouse kinematics, touchscreen dynamics, and accelerometer data can distinguish humans from bots with high accuracy [15, 16, 20], yet no systematic framework exists for comparing these sensor-based approaches to VM-based or attestation-based defenses.

This paper addresses these gaps through a Systematization of Knowledge (SoK). Following the methodological tradition established by Bonneau et al. [1], we taxonomize the design space, evaluate each architectural class systematically, and identify open problems. Our contribution is analytical clarity rather than empirical breakthrough: we name and define architecturally distinct classes of defense, isolate their structural limits, and provide a common evaluation framework for future work.

### 1.2 Contributions and Scope

This paper makes four contributions:

**C1 — A Five-Architecture Taxonomy (Section 4).** We identify and systematically compare five architecturally distinct classes of client-side anti-automation: (i) Stateless VM Attestation, (ii) Stateful Behavioral Telemetry, (iii) Behavioral Biometrics & Sensor Telemetry, (iv) Platform/OS-level Anonymous Attestation (Privacy Pass / PATs), and (v) Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys). We explicitly include Behavioral Biometrics as a primary pillar — previously absent from systematization efforts — and correctly demote Compute-Bound Challenges (WASM-based proof-of-work) to an auxiliary mechanism under Stateless VM Attestation. Each architecture is compared across ten dimensions in the Grand Taxonomy Table (Section 4.6).

**C2 — A Generalized L1-L4 Defense-in-Depth Framework (Section 5).** We extend the four-layer anti-tamper framework originally observed in Google's Botguard VM to a vendor-neutral model applicable to any register-based JavaScript VM defense, including Cloudflare Turnstile Managed Challenge and Kasada. We expand L1 (Environmental Introspection) to include kinematic and sensor telemetry (mouse dynamics, accelerometer, touch events). We introduce a novel temporal constraint analysis: the race condition between the defender's automated AST obfuscator and the attacker's symbolic execution engine, which renders the attacker's reverse-engineering cost increasingly compute-driven rather than labor-driven.

**C3 — A Conceptual Microeconomic Analysis of Forgery Costs (Section 6).** We provide a qualitative economic analysis of attacker costs across all five paradigms, distinguishing three cost types: fixed (one-time RE investment), variable (per-execution proxy, compute, and labor), and temporal (recurring fixed cost per compile rotation). We identify three structural corrections to prior economic framing: (a) anti-detect browsers impose a *conjunctive* cost structure (`Cost_proxy + Cost_profile + Cost_license`), not an alternative to proxy rotation; (b) human labor — CAPTCHA-solving farms and click-farms — sets the global cost floor for bypassing behavioral biometrics via `Cost_Bypass = min(Cost_ML_Inference, Cost_Human_Labor)`; (c) the temporal arms race in VM obfuscation is increasingly compute-driven (automated symbolic execution) rather than labor-driven (manual reverse engineering).

**C4 — The Centralization vs. Anonymity Trade-off (Section 7.4, Section 8.1).** We identify and formalize the defining open problem in anonymous attestation: Privacy Pass and PATs have technically closed the "Anonymous Authentication Gap" by providing deterministic anonymous attestation, but they introduce a structural dependency on a vendor oligopoly (Apple, Google, Microsoft) controlling the attestation root of trust. We formulate this as a trilemma between anonymous access, deterministic bot resistance, and decentralized trust, and show that no existing architecture satisfies all three properties.

**Scope.** This SoK covers client-side anti-automation mechanisms deployed in web browsers. Purely server-side bot detection — TLS fingerprinting at the CDN edge, server-side WAF heuristics, network-layer DDoS scrubbing, and application-layer rate limiting — is explicitly out of scope. These mechanisms operate under a fundamentally different economic model: the attacker does not control the inspection substrate. For client-side mechanisms, by contrast, the attacker controls the browser, the JavaScript runtime, the DOM, and every API the defense calls. This asymmetry — the defender executes code in an environment the attacker owns — is the defining structural constraint of the field.

### 1.3 Threat Model: A Dual-Axis Framework

We adopt a dual-axis threat model that decomposes the problem space into four quadrants:

- **Axis A — Authentication State:** Whether the user is operating anonymously (no prior identity assertion) or has authenticated (identity established through a credential).

- **Axis B — Attack Objective:** Whether the adversary's goal is resource exhaustion/scraping (extracting data or consuming resources at scale without targeting specific accounts) or account takeover/fraud (gaining unauthorized access to or abusing specific user accounts).

The resulting quadrant mapping is as follows:

| | **Anonymous** | **Authenticated** |
|---|---|---|
| **Scraping / Resource Exhaustion** | Quadrant I: Stateless VM (Botguard, Turnstile), Behavioral Biometrics (mouse kinematics), Compute-Bound Challenges (auxiliary). Anchored on OWASP Automated Threat Handbook [66]. | Quadrant III: Rare; typically addressed through session-bound rate limiting and quota enforcement. |
| **Account Takeover / Fraud** | Quadrant II: Stateful Telemetry (reCAPTCHA v3 risk scoring on login flows), Platform Anonymous Attestation (PATs). Anchored on OWASP Automated Threat Handbook [66] for attack objectives. | Quadrant IV: Hardware-Anchored Determinism (DBSC, Passkeys, WebAuthn). Anchored on NIST SP 800-63-3 [65] for identity assurance. |

This dual-axis model replaces the single-axis threat model prevalent in prior work (which anchored analysis solely on threat type, e.g., "Automated Abuse," "Session Hijacking," "Credential Phishing" [65]). The single-axis model conflates authentication state with attack objective, obscuring the fact that the same architectural class operates across multiple quadrants (e.g., Behavioral Biometrics applies to both Quadrant I and II). The dual-axis model also clarifies *why* certain architectures are structurally inapplicable to certain quadrants: Hardware-Anchored Determinism cannot operate in Quadrants I and II because it requires prior authentication (NIST SP 800-63-3 [65]), and this is an architectural property, not an implementation limitation.

**Analytical neutrality.** This threat model is descriptive, not prescriptive. It maps which architectures can be deployed in which operational contexts; it does not evaluate which *ought* to be deployed. The OWASP Automated Threat Handbook [66] provides the vocabulary for anonymous attack objectives (scraping, credential stuffing, carding), while NIST SP 800-63-3 [65] provides the boundaries for authenticated identity assurance. Neither framework is sufficient alone: OWASP does not specify authentication state, and NIST does not address anonymous traffic.

---

## 2. Background and Related Work

### 2.1 A Brief History of Client-Side Anti-Automation

The history of client-side anti-automation can be divided into five overlapping eras, each defined by the architectural paradigm that became dominant during that period.

**Pre-2005: Server-Side Heuristics.** Bot detection was performed entirely at the server edge through IP reputation lists, request rate analysis, and User-Agent header inspection. The fundamental limitation was the lack of any client-side execution: the server could only observe network-layer and HTTP-header artifacts, all of which the adversary could trivially forge.

**2005–2012: The CAPTCHA Era.** CAPTCHAs (Completely Automated Public Turing test to tell Computers and Humans Apart) shifted the defense to the client by presenting a visual or auditory challenge that required human perceptual capabilities. Text-distortion CAPTCHAs (reCAPTCHA v1), image-recognition CAPTCHAs, and audio CAPTCHAs dominated this era [71, 73]. However, the cat-and-mouse dynamic was well-documented: OCR solvers, then convolutional neural networks, achieved progressively higher accuracy on text CAPTCHAs [71]. CAPTCHA-solving farms (2Captcha, Anti-Captcha) emerged as an economic bypass, offering human labor at per-challenge rates of approximately $1 per 1,000 solved CAPTCHAs [51]. By 2014, Google's own machine learning systems could solve 99.8% of reCAPTCHA challenges [73].

**2010–2017: The JavaScript Challenge Era.** The defense shifted from testing human perceptual ability to testing whether the client could execute JavaScript in a manner consistent with a legitimate browser. reCAPTCHA v2 introduced the "I'm not a robot" checkbox, which analyzed pre-click interaction behavior. Cloudflare's early challenge pages required JavaScript execution before serving page content. The core insight of this era was that automated scripts — particularly those based on raw HTTP libraries — could not execute JavaScript or maintain DOM state, providing a coarse filter. However, headless browser automation (PhantomJS, Puppeteer, Selenium) rapidly closed this gap by executing JavaScript in a real or emulated browser engine.

**2017–2020: VM-Based Attestation.** The defense escalated to custom register-based JavaScript virtual machines executing encrypted bytecode. Google's Botguard VM, deployed on YouTube and Google account creation flows, defined a new instruction set interpreted by a custom VM within the browser. Kasada employed polymorphic JavaScript obfuscation with server-side challenge validation. These defenses operated on a new principle: the adversary must execute the defender's VM faithfully, in an environment that looks like a real browser, within strict timing constraints, while the VM continuously mutates its own code. The structural ceiling of this approach is the subject of Sections 4.1 and 5.

**2020–Present: Diversification.** The current era is characterized by architectural diversification rather than a single dominant paradigm. Four parallel developments define the present landscape:
1. **Stateful behavioral telemetry** (reCAPTCHA v3, DataDome): long-term profile accumulation and risk scoring, rather than point-in-time challenge-response.
2. **Behavioral biometrics and sensor telemetry** [15, 16, 20]: leveraging mouse kinematics, touch dynamics, and accelerometer data as interaction signals.
3. **Anonymous attestation protocols** (Privacy Pass [41, 38], Apple PAT [44], WICG Private State Token API [45]): cryptographic anonymous tokens backed by hardware attestation.
4. **Hardware-anchored session determinism** (DBSC [36, 37]): extending hardware-backed key possession from the authentication moment to the session lifetime.

The field has thus moved from a single-thread evolution (one paradigm succeeding another) to a multi-paradigm ecosystem where different architectures address different quadrants of the dual-axis threat model. This fragmentation motivates the present SoK.

### 2.2 From CAPTCHAs to JavaScript VMs

The transition from CAPTCHAs to JavaScript VM-based attestation represents a shift in what the defense seeks to prove. CAPTCHAs sought to prove *humanness* through task completion — the ability to read distorted text, identify objects in images, or solve a puzzle. VM-based attestation seeks to prove *environmental integrity* — that the executing JavaScript runtime, DOM, WebGL, and timer APIs all behave as they would in a legitimate, non-instrumented browser [24, 6].

This shift carries a structural consequence. In the CAPTCHA model, the attacker's task is perceptual or cognitive — solvable through ML (improving OCR) or human labor (farming). In the VM model, the attacker's task is environmental forgery — presenting the VM runtime with a set of sensor readings, timing measurements, and API behaviors that are internally consistent and indistinguishable from those of a real browser. The forgery problem carries different cost characteristics than the perceptual problem: the attacker must maintain consistency across dozens of independent measurement channels simultaneously, rather than solve a single isolated task.

The canonical survey of browser fingerprinting by Laperdrix et al. [6] catalogs the breadth of the environmental measurement surface: `navigator` properties, WebGL rendering artifacts, canvas fingerprinting, font enumeration, audio context fingerprinting, and battery status. A stateless VM defense can query any subset of these properties, and the attacker's environment must return values consistent with a real browser for each. The defense does not need to make any single measurement unforgeable; it only needs to make the set of measurements *jointly* difficult to forge consistently. This is the forgery problem at the architectural level.

### 2.3 From Probabilistic Scoring to Hardware-Anchored Determinism

The architectures described in Sections 2.1 and 2.2 all produce *probabilistic* outputs: a confidence score, a risk level, or a binary challenge/no-challenge decision derived from noisy sensor data. An entirely different class of defense produces *deterministic* outputs: cryptographic proof that a specific hardware key is present.

FIDO2/WebAuthn [31] is the canonical deterministic architecture. During enrollment, the user's authenticator (a hardware security key or platform authenticator like a TPM) generates a public-private key pair specific to the relying party. During authentication, the browser proves possession of the private key through a challenge-response protocol. The output is binary: either the key is present (the user is authenticated) or it is not. There is no confidence score, no behavioral analysis, and no risk threshold.

Device Bound Session Credentials (DBSC) [36, 37] extend this deterministic model from the authentication moment to the session lifetime. A session cookie is cryptographically bound to a device-resident key (stored in the TPM or Secure Enclave). The browser periodically proves possession of the key without user interaction. This prevents cookie theft: even if an attacker exfiltrates the session cookie, they cannot present it from a different device because they lack the private key.

The non-substitutability between probabilistic and deterministic architectures follows from the NIST Digital Identity Guidelines [65]. Deterministic architectures require prior enrollment (authentication or session establishment). They cannot screen anonymous traffic because there is no identity to anchor the hardware proof to. This is not a flaw — it is a structural property of the identity model. A probabilistic defense operating on anonymous traffic and a deterministic defense operating on authenticated sessions are complementary, not competing, paradigms.

### 2.4 The Emergence of Anonymous Attestation (Privacy Pass / PATs)

A significant gap existed in the architectural landscape prior to 2018: there was no mechanism for *deterministic* attestation of *anonymous* traffic. Probabilistic defenses could screen anonymous users, but with false positives and false negatives. Deterministic defenses could provide cryptographic guarantees, but only for authenticated users. This was the "Anonymous Authentication Gap" — a structural void in the design space.

Privacy Pass [41], introduced by Davidson et al. in 2018, was the first cryptographic protocol to bridge this gap. The protocol uses a Verifiable Oblivious Pseudorandom Function (VOPRF) with Discrete Log Equivalence (DLEQ) proofs to allow an issuer to sign blinded tokens that clients can later redeem without revealing which specific issuance event created them. The cryptographic construction ensures unlinkability: the issuer cannot correlate a token redemption with a specific issuance request. Rate-limiting is enforced by the issuer at issuance time, protecting against Sybil attacks.

The IETF standardized the Privacy Pass architecture in 2024 as a suite of three RFCs: RFC 9576 (Architecture) [38], RFC 9577 (HTTP Authentication Scheme) [39], and RFC 9578 (Issuance Protocols) [40]. Two issuance protocol variants are specified: a privately verifiable construction based on VOPRF and a publicly verifiable construction based on RSA blind signatures (token type 2). The RSA blind signature variant is the basis for Apple's Private Access Tokens deployment [44].

Apple deployed PATs in iOS 16 and macOS Ventura (June 2022) [44]. The system uses the device's Secure Enclave to generate attestation assertions that are signed by an Apple-operated issuer using RSA blind signatures. The resulting tokens are presented to web origins via a `PrivateToken` HTTP authentication challenge. Token issuance is rate-limited per device by the issuer. Cloudflare and Fastly operate public token issuers accessible to any origin.

The WICG Private State Token API [45] is the browser-level integration of Privacy Pass into the web platform. Formerly called the Trust Token API, it provides JavaScript and HTTP-level APIs for token issuance and redemption. Tokens are non-personalized carrier objects: the API cannot attach user identifiers to tokens, and tokens from the same issuer are unlinkable.

The critical architectural significance of PATs is that they provide *deterministic* attestation for *anonymous* traffic — technically closing the Anonymous Authentication Gap. However, as we argue in Section 4.4 and Section 7.3, this closure introduces a new dimension: vendor trust. The attestation root of trust is controlled by the OS vendor (Apple, Google, Microsoft), and whoever controls the root controls who may access the web anonymously. This transforms the technical gap into an economic and political one.

### 2.5 The Economics-of-Security Lens

The economics of information security provides the analytical framework for this SoK. Anderson and Moore [46] established that information security is fundamentally an economic problem: defenders and attackers optimize under different budget constraints and respond to different incentive structures. The security of a system is not determined solely by its cryptographic properties but by the economic equilibrium between the cost of attack and the value of the protected resource.

Herley and Florêncio [47] demonstrated that underground economy pricing follows predictable patterns: attackers rationally choose the cheapest effective bypass, and no attacker pays more for a capability than the expected return. Their dictum — "nobody sells gold for the price of silver" — captures the economic ceiling concept: if the cost of bypassing a defense exceeds the value of the resource protected, rational adversaries will not attempt the bypass.

Moore [48] extended this framework to cybersecurity policy, arguing that cost-benefit analysis should govern security investment decisions. The defender's optimal investment is bounded by the value of the protected asset; investing beyond that value produces negative returns regardless of the technical improvement in security posture.

Applied to client-side anti-automation, the economics-of-security lens yields a critical insight: these defenses operate under a *forgery model* rather than a *cryptanalysis model*. In cryptanalysis, the defender controls the key material and the attacker faces a mathematical barrier — the security parameter (e.g., key length) determines the computational cost of bypass. In client-side attestation, the defender controls the execution specification but the attacker controls the execution itself. The attacker's cost is not determined by a mathematical parameter but by the market price of the resources required for forgery: proxy IPs, human labor, GPU compute time, malware infections. The ceiling is economic, not cryptographic.

This distinction — introduced conceptually in prior work [6, 24] and given systematic structure here — is the through-line of the following sections. Each architectural class imposes costs on the adversary, and each cost type is bounded by a specific market or computational constraint. Understanding these ceilings — not as implementation flaws but as structural properties — is the contribution of this SoK.

---

## 3. Systematization Methodology

### 3.1 Scope and Inclusion Criteria

This SoK covers client-side anti-automation mechanisms deployed in web browsers. A mechanism is considered "client-side" if it executes or enforces its detection logic within the user's browser, JavaScript runtime, or operating system context, and if the adversary's bypass requires interacting with or subverting that client-side execution. This definition includes JavaScript VM attestation, behavioral telemetry executed in the browser, sensor data collected through browser APIs, and platform-level attestation protocols that execute within the OS but whose tokens are consumed by web origins.

The inclusion criteria are threefold:

1. **Production deployment.** The mechanism must be deployed in production by a major vendor or platform. Academic proposals that have not been deployed (e.g., novel obfuscation schemes without a production implementation) are excluded, unless they represent the canonical description of a deployed system.

2. **Documented architecture.** The mechanism must be documented in academic literature, IETF/W3C standards, or peer-reviewed grey literature (vendor technical documentation, technical whitepapers, or security research reports) that describes its architecture in sufficient detail for systematic comparison.

3. **Cost imposition.** The mechanism must impose costs on adversaries that are incurred through client-side execution. Mechanisms that operate purely on server-side heuristics (e.g., rate limiting based on request headers) are excluded because the attacker does not control the inspection substrate.

**Vendor Coverage.** The following vendors and systems are included: Google (Botguard VM, reCAPTCHA v3, DBSC), Cloudflare (Turnstile Managed Challenge, Privacy Pass deployment), Kasada (polymorphic VM defense), DataDome (stateful behavioral telemetry), Human Security / PerimeterX (stateful telemetry, behavioral biometrics), Apple (Private Access Tokens, iOS/macOS attestation), and the IETF/WICG standardization efforts for Privacy Pass and Private State Tokens.

**Exclusions.** Three classes of mechanism are explicitly excluded:
- **Server-side WAF heuristics** (e.g., AWS WAF bot control, Cloudflare WAF rules): These operate at the server edge and analyze HTTP request patterns. The attacker does not execute code within the inspection substrate, and the economic model is fundamentally different (the attacker cannot observe or manipulate the detection logic).
- **Network-layer DDoS scrubbing** (e.g., Cloudflare Magic Transit, AWS Shield): These operate at OSI L3/L4, analyzing packet-level characteristics. They are out of scope for a client-side SoK.
- **Application-layer rate limiting** (e.g., token bucket algorithms, per-API-key quotas): These operate at the server's request dispatch layer and are independent of client-side execution. While valuable, they constitute a different class of defense.

### 3.2 Systematization Approach: Capability-Based Threat Modeling

We adopt a *capability-based threat modeling* methodology. Rather than model specific threat actors (which introduces subjectivity about attacker resources and motivations), we extract attacker capability requirements from the literature and map them against defender architectural paradigms. This approach isolates what is structurally possible — the ceiling of each defense class — rather than what is probable for a given attacker profile.

We identify five attacker capability dimensions relevant across the taxonomy:

1. **Compute capacity:** GPU and CPU resources for machine learning inference (behavioral biometrics, GAN trajectory synthesis), symbolic execution (VM deobfuscation), and proof-of-work computation (compute-bound challenges). This capability is elastic: cloud GPU instances provide on-demand scaling.

2. **IP reputation inventory:** Access to residential proxy pools with unburned IP reputations. This capability is supply-constrained: the global pool of unmapped residential IPs is finite, and each IP's reputation degrades with use.

3. **Human labor:** Access to reverse-engineering personnel (for VM analysis) and click-farm workers (for behavioral challenge solving). This capability is priced through global labor markets with well-documented rates [51, 52].

4. **ML synthesis capability:** Access to trained generative models (GANs, transformers) capable of producing realistic behavioral biometrics — human-like mouse trajectories, keystroke dynamics, touch gestures. This capability requires upfront training investment but can be amortized across throughput.

5. **Malware distribution:** Access to Pay-Per-Install (PPI) malware networks for compromising legitimate user devices to extract attestation keys, session cookies, or device-bound credentials. This capability is priced through underground markets [53, 56].

These five capabilities are not independent — they interact economically. An attacker with strong ML synthesis capability may not need human click-farm labor. An attacker with large IP reputation inventory may not need to invest in VM deobfuscation if they can simply rotate through enough unique IPs. The interaction between capabilities determines which cost ceiling binds for a given defense class.

### 3.3 Source Corpus, Search Strategy, and PRISMA Flow

This SoK follows the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) framework for systematic literature review. The search strategy, inclusion/exclusion criteria, and flow diagram provide a replicable methodology for source selection.

**Databases Searched.** The following electronic databases and registries were searched: IEEE Xplore Digital Library, ACM Digital Library, arXiv (Computer Science > Cryptography and Security), Google Scholar, IETF Datatracker, W3C Technical Reports repository, and the Internet Archive Wayback Machine (for grey literature archiving).

**Search Queries.** The primary search query was:
```
("bot mitigation" OR "browser fingerprinting" OR "anti-automation" OR "bot detection") 
AND ("economics" OR "cost" OR "attestation" OR "architecture")
```

Supplementary queries targeting specific architectures:
- `("Privacy Pass" OR "Private Access Token" OR "Private State Token") AND ("security" OR "deployment")`
- `("mouse dynamics" OR "behavioral biometrics" OR "sensor telemetry") AND ("bot detection" OR "automation" OR "anti-automation")`
- `("JavaScript obfuscation" OR "JS obfuscation" OR "VM deobfuscation") AND ("symbolic execution" OR "automated" OR "machine learning")`
- `("device bound session" OR "DBSC" OR "FIDO2" OR "WebAuthn" OR "Passkey") AND ("security" OR "attack" OR "malware")`
- `("Pay-Per-Install" OR "PPI" OR "infostealer") AND ("malware" OR "economics" OR "underground")`

**Date Range.** 2010–2025, with foundational papers (Saltzer and Schroeder 1975 [70]) included for historical context. The start date of 2010 corresponds to the emergence of the JavaScript challenge era (Section 2.1), which marks the beginning of client-side execution as a defense mechanism.

**Inclusion Criteria.** As specified in Section 3.1: (a) production deployment by a major vendor or platform, (b) documented in academic literature, IETF/W3C standards, or peer-reviewed grey literature, (c) imposes costs on adversaries through client-side execution.

**Exclusion Criteria (Screening Phase).** Records were excluded if they: described purely server-side bot detection (TLS fingerprinting, server-side WAF); focused exclusively on network-layer DDoS mitigation; addressed malware detection on endpoints (not anti-automation); were measurement studies without architectural description; or described CAPTCHA designs that are not representative of current production systems.

### 3.4 PRISMA Flow Diagram

The PRISMA flow diagram is included as a standalone figure (`figures/prisma-flow.tex`). The funnel stages are as follows:

- **Identification:** n = 320 records identified through database searching. This includes results from all primary and supplementary queries across all databases.
- **Duplicate Removal:** n = 67 duplicates removed (publications appearing in multiple databases, preprints superseded by published versions).
- **Title/Abstract Screening:** n = 198 records after duplicate removal screened against inclusion criteria. n = 76 records excluded at this stage (not client-side, not anti-automation, not production-deployed, or no cost-to-adversary mechanism described).
- **Eligibility (Full-Text Review):** n = 122 full-text articles assessed for architectural relevance and verifiability. n = 47 articles excluded at this stage (insufficient architectural detail for systematic comparison, purely empirical measurement studies without architectural description, grey literature from unverifiable sources, publications describing mechanisms that are no longer operational).
- **Included in Synthesis:** n = 75 publications in the final corpus. Composition: 52 academic papers (conference proceedings and journal articles), 12 standards/IETF RFCs/W3C Recommendations, and 11 archived grey literature items (vendor whitepapers, technical documentation, malware analysis reports).

The 75 publications span the following topics: 5 SoK precedent papers, 9 browser fingerprinting and telemetry, 9 behavioral biometrics and sensor telemetry, 7 obfuscation and automated deobfuscation, 5 hardware-anchored authentication, 2 DBSC specifications and documentation, 8 Privacy Pass and PATs analyses, 7 economics of security, 5 infostealer and PPI malware, 4 anti-detect browser and proxy economics, 6 threat modeling frameworks and authentication standards, and 5 supporting academic references.

### 3.5 Exclusions and Out-of-Scope Domains

We excluded three domains that are adjacent to but structurally distinct from client-side anti-automation:

**Server-Side Web Application Firewalls (WAFs).** WAFs (e.g., AWS WAF Bot Control, Cloudflare WAF managed rules) analyze HTTP request patterns at the server edge using signatures, rate analysis, and machine learning classification of request headers. They are excluded because the attacker does not execute code within the WAF's inspection substrate. The economic model is fundamentally different: the attacker cannot observe the WAF's detection logic, cannot adapt to it dynamically, and cannot trade off proxy quality against compute investment. WAFs impose a different cost structure (per-request rejection) than client-side mechanisms (per-execution forgery cost).

**Network-Layer DDoS Scrubbing.** DDoS mitigation services (e.g., Cloudflare Magic Transit, AWS Shield Advanced) operate at OSI L3/L4, analyzing packet flows, volumetric characteristics, and protocol-level anomalies. These are excluded as they do not involve client-side execution. They represent a separate cost-to-attack paradigm (packet filtering and capacity absorption) from the application-layer anti-automation focus of this SoK.

**Application-Layer Rate Limiting.** Token bucket, leaky bucket, and sliding window rate limiters operate at the server's request dispatch layer. They are independent of client-side execution and are typically deployed as a defense-in-depth complement rather than a primary anti-automation mechanism. They are excluded because they do not impose costs correlated with the five attacker capability dimensions (Section 3.2).

### 3.6 Taxonomy Dimensions

The five architectures are compared across ten dimensions in the Grand Taxonomy Table (Section 4.6). These dimensions were selected to capture the architectural properties relevant to an economic cost analysis:

1. **Architecture Class:** The primary defense paradigm.
2. **Representative Implementations:** Deployed systems of this class.
3. **Mechanism Summary:** Concise technical description of how the defense operates.
4. **Defender Investment Type:** The primary resources the defender must commit (engineering, infrastructure, privacy cost, ecosystem).
5. **Attacker Cost Type:** Fixed, variable, temporal, or mixed — as defined in Section 6.
6. **Dominant Scaling Constraint:** The factor that most severely limits the adversary's ability to scale throughput.
7. **Structural Ceiling:** The architectural limit beyond which additional defender investment yields diminishing marginal returns.
8. **Anonymous Traffic Compatible?:** Whether the architecture can be applied to unauthenticated users.
9. **Hardware Dependency:** Whether the architecture requires client-side hardware (TPM, Secure Enclave).
10. **Vendor Oligopoly Risk?:** Whether the architecture structurally concentrates power in a small number of vendors.

---

## 4. The Systematization Matrix: Five Primary Architectures

This section constitutes the core of the SoK. Each architecture is described through its mechanism, the attacker cost it imposes, auxiliary or interacting mechanisms, and its structural ceiling. The comparative taxonomy table (Section 4.6) and the Anonymous-Authentication Spectrum figure (Section 4.7) synthesize the analysis.

### 4.1 Stateless VM Attestation

**Mechanism.** Stateless VM attestation executes a custom register-based JavaScript virtual machine within the user's browser. The VM defines an instruction set architecture (ISA) distinct from the browser's JavaScript engine: opcodes for arithmetic, property manipulation, environment introspection, and control flow are encoded as encrypted bytecode. The VM interpreter implements self-modifying opcodes and anti-tamper traps. Execution is point-in-time: each token generation event is independent, and no persistent state links successive executions from the same browser or IP address.

The canonical representative is Google's Botguard, deployed on YouTube's Proof of Origin (PO) token system and Google account creation flows. Cloudflare Turnstile's Managed Challenge mode applies a conceptually similar approach, as does Kasada's polymorphic VM defense [60, 63].

The VM measures the execution environment along four dimensions (formalized as L1–L4 in Section 5): environmental integrity (L1: `navigator` properties, WebGL rendering, DOM consistency), code integrity (L2: self-modifying opcodes that prevent static disassembly), trap detection (L3: console hooks that corrupt the instruction stream if the adversary logs VM state), and chronometric integrity (L4: continuous `performance.now()` polling where timing deviations invalidate the output token). The VM produces a bearer token that the server validates; the token carries no proof-of-possession semantics [67, 68].

**Attacker Cost Imposed.** The attacker incurs costs across three types:

- **Variable (per-execution):** Each token requires a dedicated headless Chromium instance with residential proxy IP. Proxy bandwidth consumption per execution is approximately 0.5–2 MB (including bytecode download). At scale, instance orchestration (concurrent browser management, crash recovery) adds operational overhead.
- **Fixed (one-time RE):** Initial reverse engineering of the VM's instruction set, opcode semantics, environmental checks, and trap placement. This cost is a one-time investment for each major VM architecture, though the temporal dimension (next bullet) transforms it into a recurring cost.
- **Temporal (per-compile-rotation):** When the defender deploys a new bytecode compile, the attacker must re-analyze the opcode mapping and environmental checks. This is increasingly addressed through automated deobfuscation rather than manual reverse engineering (Section 5.7).

**Auxiliary Mechanisms: Compute-Bound Challenges.** Some stateless VM defenses augment VM attestation with compute-bound challenges, typically implemented as WebAssembly (WASM)-based proof-of-work (PoW). The defender requires the client to solve a computational puzzle before issuing a token. This raises per-execution compute cost for the attacker but is structurally limited by the 100× desktop-to-mobile compute disparity: a PoW that is trivial on a desktop CPU may be prohibitively expensive on a mobile device, limiting the defender's ability to set a uniform difficulty. Compute-bound challenges are an auxiliary mechanism, not a primary architectural pillar. They raise the variable cost floor but do not alter the structural ceiling of stateless VM attestation, which is governed by IP reputation (below).

**Structural Ceiling.** The structural ceiling of stateless VM attestation is **IP reputation market exhaustion.** At any given difficulty of VM execution, the attacker's dominant scaling constraint is the availability of residential IPs with unburned reputations. Server-side verifiers maintain subnet-level reputation models: when multiple token requests from the same IP subnet are rejected, the entire subnet's reputation degrades. This creates a Tragedy of the Commons among all attackers sharing the same residential proxy pools [59]: each attacker's volume benefits themselves but imposes a negative externality (reputation degradation) on all others sharing those IPs.

At industrial scale, the attacker exhausts commodity residential proxy tiers and must purchase premium IPs at significantly higher cost. Published proxy market documentation shows a 20×–30× spread between commodity ($0.50/GB) and premium unburned residential ($10–15/GB) tiers [60, 62, 63, 64]. When the effective per-token proxy cost exceeds the economic value of the token to the attacker, the defense reaches its structural ceiling. This ceiling is not a property of the VM's technical sophistication — it is a property of the proxy supply market.

The IP reputation ceiling interacts with the temporal cost (compile rotation): as the attacker's RE cost per compile decreases (through automation), the defense's structural reliance on IP reputation as the binding constraint increases. Automated deobfuscation shifts the bottleneck from the VM's technical complexity to the economics of the proxy market.

### 4.2 Stateful Behavioral Telemetry

**Mechanism.** Stateful behavioral telemetry accumulates a long-term behavioral profile for each browser instance using persistent identifiers (cookies, browser fingerprinting). Rather than issuing a point-in-time challenge, the system continuously scores the browser's behavior: mouse movements on the page, scroll patterns, click interactions, form completion timing, navigation cadence, and dwell time. These signals are aggregated over weeks to months to produce a risk score. The score determines whether the browser receives a challenge, a friction-free experience, or a block.

Google's reCAPTCHA v3 is the canonical implementation: it returns a score between 0.0 and 1.0 for each page interaction, and the site owner configures a threshold for automated action. DataDome and Human Security (formerly PerimeterX) deploy similar architectures with proprietary scoring models [62, 64].

The key property distinguishing stateful from stateless defenses is the **profile-aging latency.** A new browser profile — regardless of how well the environmental parameters are forged — starts with a neutral or low reputation score. It must accumulate weeks of gradual, human-like browsing behavior before receiving favorable scores. This latency cannot be bypassed by spending more on per-execution infrastructure. The defender's scoring model is a black box: the attacker cannot determine the exact score threshold or the specific signals that drive it, only the binary outcome (challenged or not).

**Attacker Cost Imposed.** The attacker incurs:

- **Fixed inventory cost (profile aging):** Each aged profile represents a 2–6 week investment of proxy bandwidth and orchestration overhead. The profile is a limited-use asset: once it is used for automated activity, its score degrades, and the aging clock must be restarted.
- **Variable cost (per-execution):** Residential proxy IP must be bound to each profile for its entire lifetime. Proxy rotation within a profile's lifetime resets the aging clock (new IP = new partial identity).
- **Conjunctive cost of anti-detect browsers:** Anti-detect browsers (Multilogin, GoLogin, AdsPower) virtualize browser fingerprints — canvas, WebGL, fonts, `navigator` properties — to make each profile appear as a unique device. They do **not** replace proxy rotation. An aged Google profile in Multilogin connected via an AWS datacenter IP will be burned by reCAPTCHA v3 within minutes. The attacker's cost formula is **conjunctive**: `Cost_residential_proxy + Cost_aged_profile + Cost_software_license`. The anti-detect browser raises the fixed inventory cost (profile maintenance and license fees) but does not eliminate the variable proxy cost. This is a **stacked**, not substituted, cost structure — a correction to framings that have presented anti-detect browsers as proxy alternatives [13, 58].

**Structural Ceiling.** Stateful behavioral telemetry faces two structural ceilings:

1. **Latency constraints:** The 2–6 week profile-aging period introduces a time-to-production delay that cannot be bypassed. For time-sensitive attacks (e.g., scalping limited-release merchandise, credential stuffing during a breach window), this latency renders stateful telemetry bypass impractical regardless of budget.

2. **Anti-detect market commoditization:** As anti-detect browser software becomes commoditized, the marginal cost of creating a new virtualized profile decreases. However, the residential proxy cost remains inelastic because IP supply is finite and reputation degradation is shared. The attacker's total cost asymptotically converges to the proxy cost plus the (declining) software license cost, with the profile aging cost becoming the dominant timeline constraint rather than a budget constraint.

Additionally, privacy regulation (GDPR, ePrivacy Directive) and browser-enforced tracking prevention (ITP, ETP, Total Cookie Protection) systematically degrade the persistent identifiers on which stateful telemetry depends [6, 14]. As browsers restrict cookie lifetimes and fingerprinting surfaces, the economic ceiling of stateful defenses rises — they become less effective — yet vendors continue to market them. The tension between privacy regulation and stateful bot mitigation is an identified open problem (Section 8.3).

### 4.3 Behavioral Biometrics & Sensor Telemetry

**Mechanism.** Behavioral biometrics measure the *dynamics* of human interaction rather than the *static properties* of the execution environment. The defense collects kinematic data from input devices: mouse movement trajectories (position, velocity, acceleration, curvature), scroll event patterns (speed, acceleration, deceleration), click timing (dwell time before click, release latency), keystroke dynamics (key press duration, inter-key latency), touchscreen gestures (pressure, contact area, swipe velocity), and sensor data (accelerometer, gyroscope, magnetometer polling).

The defense does not evaluate whether the environment "looks like a browser" (L1 environmental introspection) but whether the interaction patterns "look like a human." Trained machine learning models — ranging from classical classifiers (SVM, Random Forest) to deep sequence models (LSTM, Transformer) — distinguish human motor-control patterns from synthetic ones [15, 16, 17, 19, 20, 21, 22].

Academic prototypes such as BeCAPTCHA [15, 16] demonstrate the feasibility of this approach. The BeCAPTCHA-Mouse system [16] achieves 93% detection accuracy against high-realism GAN-generated mouse trajectories using Sigma-Lognormal feature extraction. AuthentiSense [20] uses only accelerometer, gyroscope, and magnetometer data with few-shot Siamese learning to authenticate users with 97% F1-score from only 3 enrollment samples. Commercial deployments of behavioral biometrics exist within DataDome's and Human Security's platforms, and reCAPTCHA v3 incorporates interaction signals into its scoring model.

**Attacker Cost Imposed.** The attacker's bypass cost for behavioral biometrics is defined by a **minimization function**:

`Cost_Bypass = min(Cost_ML_Inference, Cost_Human_Labor)`

The attacker will choose the cheaper of two paths:

- **ML Synthesis Path:** Running generative models (GANs, LSTMs trained on human trajectories) to produce believable human-like Bezier curves, velocity profiles, and timing jitter at scale. The BeCAPTCHA-Mouse paper [16] demonstrates two synthesis methods: heuristic function-based and GAN-based trajectory generation. MouseAgent [18] is an adversarial generative network explicitly designed to produce mouse trajectories that evade detection models. The computational overhead scales with token throughput: each token requires a fresh, non-repeating trajectory. GPU inference costs are elastic (cloud GPU pricing) but non-trivial at industrial scale.

- **Human Labor Path:** Routing the interaction challenge to a human worker. CAPTCHA-solving farms (2Captcha, Anti-Captcha, CapMonster) provide API-driven human labor at published per-challenge rates, documented by Motoyama et al. [51, 52] at approximately $1 per 1,000 solved CAPTCHAs. For behavioral biometrics, the human worker would interact with an instrumented browser session — wiggling the mouse, scrolling, clicking — while the attacker's infrastructure captures and replays the resulting sensor signals. The global market for human click-farm labor spans multiple countries with wage differentials that keep per-token costs low.

**Economic implication.** Human labor sets the **absolute global price ceiling** for bypassing behavioral biometrics. If the ML inference cost per token exceeds the human labor wage per token, the attacker defaults to the labor market. The defender's goal is to raise per-token interaction complexity to the point where human labor becomes economically unsustainable at industrial throughput — i.e., the human worker's throughput (tokens per hour) drops below the point where the per-token labor cost exceeds the per-token resource value. This is not a technological arms race; it is a **labor-market arbitrage.** The defender wins when the minimum wage for believable behavioral performance, multiplied by the time required per token, exceeds the value of the protected resource.

**Structural Ceiling.** The structural ceiling is the defender's ability to raise interaction complexity above the cost threshold where human labor becomes impractical at industrial throughput. This ceiling is set by two constraints:

1. **Legitimate user friction:** Increasing interaction complexity (e.g., requiring longer mouse trajectories, more complex click patterns) degrades user experience. The defender cannot make the interaction arbitrarily difficult without driving away legitimate users.

2. **ML synthesis improvement:** As generative models improve, ML synthesis becomes cheaper. The attacker's `Cost_ML_Inference` converges toward `Cost_Human_Labor` as a function of time and research investment. The defender must continuously raise the complexity bar to stay ahead of the ML synthesis capability curve.

The behavioral biometrics pillar is architecturally novel in this SoK: it has not been included in prior systematization efforts, which focused on environmental fingerprinting and VM-based attestation. Its inclusion is justified by the emergence of production behavioral biometrics in commercial bot mitigation platforms and the substantial academic literature on the topic since 2021 [15, 16, 17, 18, 19, 20, 21, 22].

### 4.4 Platform/OS-level Anonymous Attestation (Privacy Pass / PATs)

**Mechanism.** Platform/OS-level anonymous attestation uses hardware-backed cryptographic operations to generate rate-limited, anonymous tokens that web origins can verify without learning the user's identity. The architectural components are:

1. **Attestation source:** A hardware root of trust — typically the device's Secure Enclave (Apple), TPM, or an equivalent Trusted Execution Environment — generates attestation assertions that the device is genuine and has not been tampered with.

2. **Token issuer:** A server operated by the platform vendor (or a delegated issuer) validates the attestation assertion and issues a blinded token. In Apple's PAT implementation [44], the issuer uses RSA blind signatures (RFC 9578, token type 2 [40]) so that the issuer cannot link the signed token to the specific attestation event.

3. **Token redemption:** The client presents the unblinded token to a web origin via the `PrivateToken` HTTP authentication scheme (RFC 9577 [39]). The origin verifies the issuer's signature. The token carries no user identifier.

4. **Rate limiting:** The issuer enforces per-device rate limits at issuance time. A single device cannot obtain more tokens than the issuer's configured limit within a time window, preventing Sybil attacks from a single compromised device.

Apple deployed PATs in iOS 16 and macOS Ventura (June 2022) [44]. Cloudflare and Fastly operate the initial issuer infrastructure. The WICG Private State Token API [45] provides the browser-level integration. The IETF Privacy Pass suite (RFC 9576–9578 [38, 39, 40]) standardizes the protocol for cross-platform interoperability.

**Attacker Cost Imposed.** The attacker cannot forge PATs without access to a legitimate device's hardware attestation key. The bypass path is not cryptographic but operational: the attacker must compromise legitimate user devices to obtain signed attestations. This maps to the fifth attacker capability dimension (malware distribution, Section 3.2). The cost is the black-market price of a malware infection on a target demographic's device, delivered through Pay-Per-Install (PPI) networks [53, 56]. The attacker buys malware installs at per-infection rates on underground forums, infects devices, extracts session cookies or proxies through the infected device, and uses the device's native PAT issuance capability.

However, PAT rate-limiting constrains this attack. A compromised device can issue tokens only at the rate the issuer allows. To achieve industrial throughput, the attacker must compromise many devices — which scales the PPI cost linearly with the number of devices. The economic cost per token is:

`Cost_PAT_bypass = (PPI_infection_cost × num_devices) / (tokens_per_device_per_day × attack_duration)`

Where `tokens_per_device_per_day` is rate-limited by the issuer. This creates an economic ceiling: the attacker's cost scales with desired throughput, not with VM-execution efficiency or proxy quality.

**Structural Ceiling.** The structural ceiling of PATs is **vendor centralization.** The attestation root of trust is controlled by a small number of OS vendors: Apple (iOS, macOS), Google (Android, ChromeOS), and Microsoft (Windows). Whoever controls the attestation root controls who may access the web anonymously. This is not a cryptographic weakness of the protocol — the RSA blind signature and VOPRF constructions are cryptographically sound [42, 43] — but a structural economic and political property.

Three specific concerns arise from vendor centralization:

1. **Access control by fiat:** A platform vendor could de-attest a region, device class, or software version, rendering entire populations unable to obtain anonymous attestation tokens. This is not hypothetical: Apple's attestation service is tied to iCloud account standing, and the issuer directory (`/.well-known/token-issuer-directory`) is controlled by the platform vendor.

2. **Issuer monoculture:** If a single issuer (or small set of issuers) becomes dominant, the issuer can discriminate among redemption requests. While Privacy Pass's unlinkability property prevents the issuer from linking individual redemptions to individual issuances, the issuer can still observe aggregate redemption patterns and selectively degrade service.

3. **Regulatory risk:** Government compelled-access regimes may require platform vendors to selectively issue or deny attestation tokens. A PAT ecosystem with centralized issuers is more susceptible to this pressure than a decentralized anonymous credential system.

The centralization risk is not a flaw in PATs specifically — it is a property of *any* anonymous attestation system that relies on issuer-mediated attestation. Decentralized alternatives (zero-knowledge proofs of personhood, decentralized issuer networks) are an open research problem (Section 8.1).

### 4.5 Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys, WebAuthn)

**Mechanism.** Hardware-anchored determinism uses cryptographic proof-of-possession of a device-resident private key. Unlike the probabilistic architectures (Sections 4.1–4.3), the output is binary: the key is present, or it is not. Two sub-classes exist:

1. **Credential authentication (FIDO2/WebAuthn [31], Passkeys):** During enrollment, the user's authenticator (hardware security key or platform authenticator like TPM/Secure Enclave) generates a public-private key pair. During authentication, the browser proves possession of the private key through a challenge-response protocol. The relying party never learns the private key. Passkeys extend FIDO2 with cross-device synchronization via platform credential managers.

2. **Session binding (DBSC [36, 37]):** A session cookie is cryptographically bound to a device-resident key at session establishment. The browser periodically proves key possession to the server without user interaction. If the session cookie is exfiltrated (e.g., by infostealer malware), it cannot be used from a different device because the attacker lacks the private key.

DBSC was announced by Google in April 2024 [37] and is under development as a W3C/WICG specification [36]. The design targets the session-hijacking threat model: cookie theft is a dominant attack vector, and DBSC renders stolen cookies unusable outside the original device.

**Attacker Cost Imposed.** The attacker does **not** forge the TPM attestation or extract the private key from the Secure Enclave. The bypass path is device compromise: the attacker compromises the legitimate user's device, exports session state (cookies, tokens), or proxies automated requests through the infected device.

The cost of this bypass is the black-market price of a malware infection on the target demographic's machine, delivered through Pay-Per-Install (PPI) networks. The PPI ecosystem is well-documented: Caballero et al. [53] measured four PPI services infiltrating over one million executables across 15 countries. Pastrana et al. [56] provide pricing data: malware-as-a-service (MaaS) subscriptions at $75–$200/month, compromised device sales at $1–$350 per device, and compromised account resale at $1–$30 per account.

The attacker's cost formula for bypassing hardware-anchored determinism at scale is:

`Cost_bypass = PPI_infection_cost_per_device × num_devices + Cost_malware_operation`

Where the PPI infection cost per device is set by the underground market equilibrium, not by the defender's protocol design. This is a critical insight: the defender can make the attestation protocol arbitrarily strong cryptographically, but the attacker's bypass cost is bounded by the price of a malware infection, not by the protocol's security parameter.

**Structural Ceiling.** Three structural ceilings apply:

1. **User adoption friction:** Hardware-anchored authentication requires enrollment. FIDO2/Passkeys require users to register an authenticator and manage recovery. DBSC requires browser and OS support. Adoption rates are a function of user experience design, not protocol security.

2. **Inapplicability to anonymous traffic:** Hardware-anchored determinism requires prior authentication or session establishment. It cannot be applied to Quadrants I and II of the dual-axis threat model (Section 1.3). This is a structural limitation of the identity model (NIST SP 800-63-3 [65]).

3. **PPI malware market ceiling:** The attacker's bypass cost is bounded by the black-market price of malware infections. If the value of the protected resource (e.g., a financial account, a high-value service) exceeds the PPI infection cost for the target demographic, the defense's economic deterrence is limited. For high-value targets, the PPI cost ($1–$350 per device [56]) may be far below the account value, rendering hardware-anchored determinism an incomplete defense.

Additionally, real-world FIDO2 deployments have known vulnerabilities: Kuchhal et al. [32] found that only 4.4% of evaluated authenticators carry FIDO Level 2+ certification offering malware resistance. Tarrach et al. [33] identified message integrity gaps in FIDO2 messages accessible to browser extensions. The infostealer ecosystem continues to evolve: SpyCloud [57] documented infostealer malware bypassing Chrome's app-bound cookie encryption to exfiltrate unencrypted session cookies.

### 4.6 Comparative Taxonomy (Grand Table)

The Grand Taxonomy Table comparing all five architectures across ten dimensions is provided as a standalone figure (`figures/taxonomy-table.tex`). The table summarizes the mechanism, defender investment type, attacker cost type, dominant scaling constraint, structural ceiling, anonymous traffic compatibility, hardware dependency, and vendor oligopoly risk for each architecture.

### 4.7 The Anonymous-Authentication Spectrum

The Anonymous-Authentication Spectrum figure (`figures/auth-spectrum.tex`) visualizes the five architectures along a continuum from fully anonymous (left) to fully identified (right), with a new dimension — vendor trust — introduced at the center.

- **Left pole — Fully Anonymous + Probabilistic:** Stateless VM Attestation (Botguard, Turnstile). No prior enrollment; confidence scoring. Attacker cost is per-execution proxy + compute.

- **Center-left — Anonymous + Behavioral:** Behavioral Biometrics (mouse kinematics, touch dynamics). No prior enrollment; pattern classification. Attacker cost is `min(ML inference, human labor)`.

- **Center — Anonymous + Cryptographic but Vendor-Bound:** Privacy Pass / PATs. Cryptographically anonymous but issuer-mediated. Attacker cost is device compromise via PPI malware, bounded by rate limits.

- **Center-right — Identified + Hardware-Anchored Session:** DBSC. Authentication required once; session bound to device thereafter. Attacker cost is device compromise post-authentication.

- **Right pole — Identified + Hardware-Enrolled Authentication:** FIDO2 / Passkeys. Full enrollment required; identity anchored to hardware. Attacker cost is credential theft or device compromise.

The spectrum resolves the old "Anonymous Authentication Gap" misconception — the claim that no mechanism existed for deterministic anonymous attestation. PATs occupy the center of the spectrum, technically bridging the gap between probabilistic anonymous defenses and deterministic identified defenses. However, PATs introduce a new dimension: **vendor trust.** The attestation root of trust is controlled by an OS vendor oligopoly. This transforms the original technical gap into an economic and political centralization dilemma — the defining open problem of the field (Section 8.1).

---

## 5. Generalized Defense-in-Depth: The L1–L4 Stack for Stateless VMs

### 5.1 Elevating Botguard-Specific Layers to a General Framework

The four-layer anti-tamper framework was originally observed in the context of Google's Botguard VM. However, the architectural decomposition applies to any register-based JavaScript VM defense, including Cloudflare's Turnstile Managed Challenge and Kasada's polymorphic VM. This section generalizes the framework to a vendor-neutral model.

The framework decomposes stateless execution-time defenses into four discrete, measurable layers. Each layer:
1. Identifies a specific anti-tamper mechanism deployed by the defender.
2. Describes the class of subversion required to bypass that mechanism.
3. Characterizes the cost type (fixed, variable, temporal) the mechanism imposes on the adversary.
4. Identifies the structural limit of that layer.

The layers are ordered by their position in the execution stack: environmental conditions (L1) provide the inputs to the VM; obfuscation (L2) protects the VM code itself; traps (L3) detect introspection; and chronometric integrity (L4) constrains execution timing. A defense may implement any subset of these layers; the framework does not prescribe that all four must be present.

### 5.2 L1: Environmental Introspection & Sensor Telemetry

**Mechanism.** L1 mechanisms inspect the execution environment to detect properties inconsistent with legitimate browser execution. This paper expands the traditional scope of L1 in two directions:

- **Static introspection:** The VM queries `navigator.webdriver` (which should be undefined or false in a real browser), verifies WebGL rendering parameters (GPU model, vendor string consistency), checks DOM prototype chain integrity (e.g., that `document.createElement.toString()` returns `[native code]` and not a wrapper), detects User-Agent inconsistencies, and examines properties such as `navigator.plugins`, `screen.colorDepth`, and `navigator.hardwareConcurrency`. Standard headless Chrome instances leak 15–20 detectable properties absent from real browsers [6].

- **Dynamic sensor telemetry (expanded):** The VM collects mouse movement trajectories, scroll event patterns, click timing, touch pressure, and accelerometer/gyroscope polling. The defender measures both *what* the environment looks like (static introspection) and *how* the user interacts with it (dynamic sensor telemetry). This expansion is justified by the emergence of behavioral biometrics as a primary defense pillar (Section 4.3) and the integration of sensor APIs into browser standards.

**Cost Imposed.** Variable compute or labor cost. The attacker faces two paths:
- Generate static browser properties consistent with a real browser (well-understood, commodity capability via Puppeteer-extra and its stealth plugin).
- Generate dynamic sensor signals consistent with human motor control — mouse trajectories, scroll timing, accelerometer data. This requires either ML inference (running GANs or trajectory generators per token [16, 18]) or human labor (click-farm workers interacting with instrumented browser sessions [51, 52]).

**Cost Type.** Mixed (Variable compute OR Variable human labor, attacker chooses the cheaper path).

**Structural Limit.** The human labor market floor: the cost of human-generated sensor signals sets the ceiling on ML synthesis investment. The defender cannot raise interaction complexity beyond the point where legitimate user friction becomes unacceptable (Section 4.3).

### 5.3 L2: Obfuscation & Polymorphism

**Mechanism.** L2 mechanisms obscure the VM's code to prevent static analysis. Techniques include:
- **Runtime code construction:** Opcodes are not hardcoded as literals but constructed at runtime (e.g., register 274 in Botguard builds the opcode array dynamically). Static disassembly of the VM source code produces an incomplete view of the actual instruction stream.
- **Self-modifying code:** LOADSTRING and LOADOP (EVAL) opcodes inject new instructions during execution, making the executed code a superset of the delivered code.
- **Periodic compile rotation:** The defender deploys new bytecode compiles on an irregular schedule, changing opcode encodings, environmental check locations, and trap placements. The lifespan of a single compile variant — denoted as T_Life — is the window during which a reverse-engineered mapping of that variant remains operational.

**Cost Imposed.** Temporal cost — a recurring fixed cost triggered by compile rotation events. The attacker must re-analyze the VM each time a new compile is deployed. The attacker's total RE cost is a step function: a fixed investment at each compile rotation, with the frequency of rotation determining the period of the step.

**Critical Insight: Compute-Driven RE.** The temporal cost is increasingly compute-driven, not human-driven. State-of-the-art attackers do not assign a human reverse engineer to manually trace each new compile. Instead, they employ automated deobfuscation pipelines:

- **Symbolic execution** on JavaScript, pioneered by Kudzu [25], symbolically executes VM code to recover the relationship between VM inputs (environmental checks, timing APIs) and VM outputs (token bytes). Syntia [26] uses Monte Carlo Tree Search-driven program synthesis to recover VM instruction semantics from I/O traces, achieving 94%+ success on commercial VM protectors.

- **Differential analysis** compares two consecutive compiles to identify which opcodes changed, which checks moved, and which traps were added or removed. This reduces the RE task from full VM analysis to delta analysis.

- **AST-level neural models** predict opcode mappings and identifier meanings in obfuscated code. DOBF [28] uses BERT-style pre-training to recover deobfuscated source code with 13% improvement in code translation tasks. JSNice [29] uses CRF-based structured prediction to recover identifier names from obfuscated JavaScript with 63% accuracy.

**Cost Type.** Temporal (recurring fixed cost, decreasing with automation).

**Structural Limit.** The temporal arms race: the defender's compile rotation cadence vs. the attacker's automated RE pipeline speed. If the attacker can fully automate the un-mapping of a new compile faster than the defender can push new compiles — i.e., if $T_{RE}$ (the attacker's time to defeat a new compile) falls consistently below $T_{Life}$ (the compile's effective lifespan) — the defense provides only transient value. The structural ceiling is reached when automated RE compresses $T_{RE}$ below $T_{Life}$ as a steady state.

### 5.4 L3: Execution Traps

**Mechanism.** L3 mechanisms detect and disrupt attempts to introspect or instrument the VM. Techniques include:
- **Console method trapping:** `console.log`, `console.debug`, and related methods are bound to trap functions via prototype manipulation. Logging any VM variable corrupts the instruction stream.
- **Anti-debugger hooks:** `debugger;` statements placed in hot code paths disrupt automated debugger attachment.
- **Prototype chain integrity:** The VM verifies that `Function.prototype.toString` and other native methods have not been wrapped or monkey-patched.

**Cost Imposed.** Mixed cost. Initial automated RE identifies trap locations and their trigger conditions (fixed/temporal). However, maintaining trap awareness at execution scale requires per-execution orchestration: the attacker's instrumented browser must avoid triggering traps while faithfully executing the VM. This is a variable overhead — each execution that triggers a trap produces an invalid token and wastes the associated proxy and compute expenditure.

**Cost Type.** Mixed (Fixed/Temporal for RE + Variable for per-execution trap avoidance).

**Structural Limit.** Trap detection is a cat-and-mouse game. The defender can add new traps, reorder trap placement, or introduce probabilistic trap activation. The attacker can automate trap identification and neutralization. The structural ceiling is reached when the attacker's automated trap-detection pipeline operates faster than the defender's trap-deployment cadence — a variant of the L2 temporal arms race.

### 5.5 L4: Chronometric Integrity

**Mechanism.** L4 mechanisms enforce timing constraints on VM execution. The VM continuously polls `performance.now()` and `Date.now()`, using the time delta to mutate a seed value that determines the bytecode decryption key. Deviations from expected execution timing — caused by the attacker's instrumentation, debugging, or proxy latency — produce an incorrect seed, which decrypts garbage bytecode and generates an invalid token. Typical sensitivity is 50–200ms.

Additional chronometric constraints include:
- **Token freshness windows:** Server-side timestamps enforce that tokens must be redeemed within 30–120 seconds of generation. This eliminates batch-generation strategies (generating tokens during off-peak hours for later use). Token generation must be online, time-synchronized, and sustained rather than bursty.
- **Multi-clock consistency:** The defender checks that `performance.now()`, `Date.now()`, and server-received timestamps are consistent with each other and with expected execution duration.

**Cost Imposed.** Variable cost. Maintaining timer consistency at scale requires per-execution synchronization: each headless browser instance must concurrently execute the VM, manage timer spoofing across multiple clock APIs, and maintain consistency with server-side time. At industrial throughput, instance orchestration overhead grows superlinearly.

**Cost Type.** Variable (per-execution timer orchestration).

**Structural Limit.** Timer spoofing is well-understood: the attacker can mock `performance.now()` and `Date.now()` in Puppeteer/CDP to return consistent, linearly increasing values. The structural ceiling of L4 is not the impossibility of timer spoofing but the coordination cost of maintaining consistent spoofing across thousands of concurrent instances, each executing a different compile variant with different timing sensitivities.

### 5.6 Qualitative Cost Analysis: Fixed vs. Variable vs. Temporal

The following table summarizes the cost types imposed by each L1–L4 layer, the dominant cost driver, and the scalability profile:

| Layer | Mechanism | Cost Type | Dominant Cost Driver | Scalability Profile |
|---|---|---|---|---|
| L1 | Environmental Introspection + Sensor Telemetry | Mixed (Variable) | ML inference or human labor per token | Scales with throughput; bounded by human labor market floor |
| L2 | Obfuscation & Polymorphism | Temporal | RE automation pipeline speed vs. compile rotation cadence | Step function at each rotation; decreasing with automation |
| L3 | Execution Traps | Mixed | Automated RE for trap ID + per-execution avoidance | Scales weakly with throughput; bounded by trap deployment cadence |
| L4 | Chronometric Integrity | Variable | Per-execution timer orchestration and synchronization | Scales with throughput; bounded by coordination overhead |

**Interaction effects.** The layers are not independent. A breakthrough at L2 (fully automated opcode mapping) accelerates the attacker's progress through L3 (trap identification becomes a sub-problem of opcode analysis) and reduces the per-compile basis for L1 calibration (environmental check locations become known). The framework's value is in decomposing the defense into measurable components, not in assuming their independence.

### 5.7 The Temporal Constraint: Defender AST Obfuscator vs. Attacker Symbolic Execution

The temporal constraint is the novel analytical contribution of this framework. Compile rotation does not create an infinite cost barrier — a misconception that has appeared in vendor marketing. It creates a race condition between the defender's CI/CD compile-deployment cadence and the attacker's automated RE pipeline.

**The Defender Side.** Compile rotation is automated: an AST-level obfuscator in the CI/CD pipeline randomly permutes opcode encodings, reorders environmental check placements, and shuffles trap locations. The marginal cost of pushing a new compile is negligible (compute time, deployment automation). However, compile complexity is bounded by JavaScript runtime constraints: the VM must execute on real mobile devices with limited CPU and memory budgets, and it must not add excessive latency to user-facing page loads. The defender cannot make the VM arbitrarily complex without degrading legitimate user experience.

**The Attacker Side.** Automated deobfuscation compresses T_RE — the time required to reverse-engineer a new compile — from weeks (manual RE) to hours or minutes (automated symbolic execution). Tools like Syntia [26] demonstrate that synthesized semantics can recover VM instruction behavior with high accuracy from execution traces alone. Differential analysis tools compare compile snapshots to isolate changes. Neural models [28, 29] predict identifier mappings.

**The Tipping Point.** The structural ceiling is reached when the attacker's automated RE pipeline consistently produces a working un-mapping of each new compile faster than the defender's pipeline deploys the next compile. At that point, $T_{RE} < T_{Life}$ as a steady-state condition: the defense provides only transient value (the window between a compile's deployment and its automated defeat), and the defense's practical effectiveness reduces to the duration of that window rather than the presence of the VM itself.

This analysis does **not** predict that automated RE is currently faster than compile rotation for any specific defense. The relevant speeds of defender compile pipelines and attacker RE pipelines are empirical questions that vary by implementation. The contribution is conceptual: identifying the temporal constraint as the structural dynamic that governs L2, and recognizing that it is increasingly a compute-vs-compute race rather than a compute-vs-labor race.

### 5.8 Why the Stack is Bounded (The Forgery Principle)

The L1–L4 stack is bounded by a structural property that applies to all software-only client-side defenses: the adversary controls the execution substrate. The JavaScript runtime, the DOM, the WebGL context, the timer APIs, the sensor APIs — every "measurement" the VM takes of its environment is a measurement of data the adversary can observe, intercept, modify, or synthesize.

An anti-tamper layer can raise the cost of forgery — each layer adds complexity to the forgery task — but it cannot change the structural fact that the defended software executes in an environment the adversary owns. This is the **forgery principle:** client-side attestation is a forgery problem, not a cryptanalysis problem.

In cryptanalysis, the defender controls the key material, and the attacker faces a mathematical barrier — the security parameter determines the computational cost of bypass. In client-side attestation forgery, the defender controls the execution specification, but the attacker controls the execution itself. No amount of VM-complexity layering changes the paradigm from the latter to the former. The economics of anti-automation — raising forgery costs to unprofitable levels — is the only viable defense within this structural constraint.

This does **not** imply that software-only defenses are ineffective. It implies that their effectiveness is measured in economic terms (cost imposed on the adversary) rather than cryptographic terms (mathematical impossibility of bypass). The ceiling is economic, not cryptographic. Understanding this distinction — and systematizing the specific economic ceilings of each architectural class — is the contribution of this SoK.

---

## 6. The Microeconomic Constraints of Forgery

This section provides a conceptual economic analysis of attacker costs across the architectures described in Section 4. It does not present formal cost models with fitted parameters — such models require empirical calibration data that this SoK does not claim. Instead, it identifies the economic mechanisms and market constraints that govern attacker costs, framed in rigorous but conceptual prose.

### 6.1 The Temporal Arms Race: Automated Deobfuscation and the Collapse of T_RE

The temporal arms race, introduced in Section 5.7, is the central dynamic governing the economic viability of stateless VM attestation. The defender deploys new bytecode compiles through an automated CI/CD pipeline. The attacker reverse-engineers each compile through an increasingly automated RE pipeline.

The critical insight is the shift from labor-driven to compute-driven RE. Manual reverse engineering — a skilled human tracing opcodes through a disassembler — imposes a high, recurring fixed cost on the attacker. This was the original economic premise of compile rotation: the defender's automated obfuscation pipeline would continuously impose human RE costs that were unsustainable at scale.

However, the attacker's RE process is increasingly automated:
- **Symbolic execution** (Kudzu [25], Triton-on-JS) automates the recovery of opcode semantics.
- **Differential analysis** automates the identification of changes between compile versions.
- **AST-level neural models** (DOBF [28], JSNice [29]) predict opcode mappings and identifier meanings.

The structural ceiling is reached when the attacker automates the un-mapping of the VM faster than the defender's pipeline can push new compiles. At that point, T_RE < T_Life consistently: the defense provides only transient value. The defender's maintenance cost is automation-driven and low (CI/CD pipeline compute time); the attacker's RE cost is increasingly compute-driven (GPU/CPU time for symbolic execution and neural inference). The arms race has shifted from "human defender vs. human attacker" to "automated compiler vs. automated deobfuscator" — a compute-vs-compute race in which both sides' marginal costs approach zero, but the defender's advantage erodes because the VM's structural limits (JavaScript runtime constraints, legitimate user latency tolerance) cap the defender's ability to increase compile complexity.

The implications are economic: compile rotation's deterrence value is proportional to (T_Life − T_RE) — the net window during which a given compile remains un-defeated. As T_RE decreases through automation, the defender must increase compile rotation frequency to maintain the same net window. There is no formal model in the literature for this dynamic, particularly when T_RE is driven by automated symbolic execution rather than human labor (Section 8.4).

### 6.2 Human Labor as the Global Cost Floor

For any client-side challenge that requires human-like interaction — behavioral biometrics (mouse kinematics, touch dynamics), CAPTCHAs, or sensor telemetry — the attacker's bypass cost is floored by the global market for human labor.

CAPTCHA-solving services (2Captcha, Anti-Captcha, CapMonster) provide API-driven access to human workers who solve perceptual challenges at published per-item rates. The economics of these services were documented by Motoyama et al. [51], who measured pricing at approximately $1 per 1,000 solved CAPTCHAs in 2010, with follow-up work [52] analyzing the broader freelance labor market for web service abuse. The services operate as two-sided marketplaces: bot operators submit challenges via API, workers (located in countries with low labor costs) solve them in real time, and the service takes a commission.

Behavioral biometrics extend the relevance of human labor to sensor-based challenges. An attacker can route a behavioral challenge (e.g., "move the mouse from point A to point B in a human-like way") to a click-farm worker, capture the resulting sensor signals (mouse trajectory, click timing, accelerometer data), and replay them as environmental inputs to the VM. The per-token cost is the human worker's time multiplied by their wage rate, plus the proxy cost for the instrumented browser session.

**Economic Implication.** The cost of bypassing behavioral biometrics is:

`Cost_Bypass = min(Cost_ML_Inference, Cost_Human_Labor)`

where:
- `Cost_ML_Inference` is the GPU/CPU cost of running a GAN or trajectory generator to produce a convincing human-like interaction pattern,
- `Cost_Human_Labor` is the market wage for a click-farm worker to perform the interaction.

The attacker rationally chooses the cheaper path. Human labor sets the **absolute global price ceiling** on ML synthesis: no matter how sophisticated the ML model becomes, its inference cost cannot exceed the human labor wage without becoming economically irrational.

**Defender's Objective.** The defender's goal is to raise per-token interaction complexity to the point where human labor becomes economically unsustainable at industrial throughput. If the interaction requires 15 seconds of human attention and the worker's effective wage is $2/hour, the per-token labor cost is approximately $0.008. At 1 million tokens per day, this is $8,333/day — potentially viable depending on the resource value. At 10 seconds per token and 100 million tokens per day (industrial scraping), the labor cost becomes $55,555/day, which exceeds most scraping revenue models.

This is not a technological arms race between defender ML and attacker ML — it is a **labor-market arbitrage.** The defender does not need to make the interaction impossible to synthesize via ML; it only needs to make the human labor time per token exceed the economic threshold where the attack is profitable.

### 6.3 The Variable Cost Weaponization (Proxy Depletion)

Forcing attackers to consume real-world proxy bandwidth — residential IP addresses — is a sound software defense because proxy depletion creates a non-linear scaling penalty.

Residential proxy supply is finite and inelastic in the short term. The global pool of consumer devices participating in residential proxy networks (via SDK-based proxy programs, compromised IoT devices, or explicit opt-in) is bounded. As attackers scale throughput, they exhaust the pool of commodity-priced IPs and must either pay premium rates or accept higher failure rates.

Proxy market stratification is well-documented in industry analyses [60, 62, 63, 64]:
- **Commodity residential pools:** ~$0.50/GB. These IPs are shared across many proxy users and have mixed or degraded reputations with major bot detection services.
- **Premium unburned residential IPs:** ~$10–15/GB. These IPs have clean reputations and are typically sourced from users who do not participate in high-throughput proxy sharing.
- **Mobile 4G/5G proxies:** ~$15–30/GB. Carrier-grade NAT imposes additional reputation isolation but increases per-GB cost.

The 20×–30× price spread between commodity and premium tiers creates a superlinear cost escalation as attackers scale. An attacker operating at 10K tokens/day may operate entirely within the commodity tier. At 1M tokens/day, the IP reputation burn rate may necessitate that a significant fraction of IPs come from the premium tier, increasing the effective per-token proxy cost by an order of magnitude.

The proxy supply constraint is structural, not a temporary market inefficiency. While new residential IPs enter the market (new devices join proxy networks), the reputation system ensures that IPs exposed to high-volume bot traffic degrade and exit the premium tier rapidly. The "flow rate" of IPs from the commodity tier to the premium tier is negative: premium IPs degrade into the commodity pool, but commodity IPs do not regain premium status without extended quiescence periods.

### 6.4 Reputation as an Exhaustible Resource (Tragedy of the Commons)

IP reputation functions as a commons. All attackers sharing a residential proxy pool degrade that pool's collective reputation. Subnet-level reputation scoring by server-side verifiers means that a single high-volume operator on a /24 subnet degrades the reputation of every other IP in that subnet, regardless of which specific IP they used.

This creates a Tragedy of the Commons [59] among attackers:
- **Individual benefit:** Each attacker's volume generates revenue proportional to their own throughput.
- **Collective cost:** Each attacker's volume imposes a negative externality (reputation degradation) on all other attackers sharing the same proxy pools.
- **Inequitable distribution:** Large-scale attackers degrade reputation for small-scale attackers who lack the proxy inventory to absorb the degradation.

The defender's subnet-level scoring structurally advantages the defender at scale: the aggregate attacker activity on a proxy pool raises the failure rate for all attackers, not just the high-volume ones. This forces attackers into an arms race for clean IPs, driving up proxy costs for the entire attacker population.

The effective failure rate is a function of broader proxy-market equilibrium, not merely individual throughput. This makes cost prediction at scale a market-level exercise rather than an individual-level exercise — a complexity that linear cost models fail to capture.

### 6.5 The Conjunctive Cost of Profile Virtualization

**Critical Correction.** Anti-detect browsers (Multilogin, GoLogin, AdsPower) are not an alternative to proxy rotation. They virtualize browser profiles — WebGL fingerprints, canvas hashes, font configurations, `navigator` properties, cookie jars, and local storage — but do **not** alter the origin IP address from which requests are sent.

The attacker's cost formula for bypassing stateful behavioral telemetry is **conjunctive:**

`Cost_Bypass = Cost_residential_proxy + Cost_aged_profile + Cost_software_license`

where:
- `Cost_residential_proxy` is the variable cost of maintaining a high-quality residential IP for the profile's lifetime (Section 6.3).
- `Cost_aged_profile` is the fixed inventory cost of aging the profile for 2–6 weeks before it scores favorably (Section 4.2).
- `Cost_software_license` is the subscription fee for the anti-detect browser software.

The residential proxy is still mandatory. An aged Google profile in Multilogin connected via an AWS datacenter IP will be burned by reCAPTCHA v3 or similar stateful telemetry within a small number of requests. The defender's IP reputation model operates independently of the browser fingerprint: a datacenter IP is a datacenter IP regardless of how sophisticated the browser profile is. The anti-detect browser raises the fixed inventory cost but does not eliminate the variable proxy cost.

This is a **stacked** cost structure, not a substituted one. Prior work has sometimes presented anti-detect browsers as proxy alternatives — a framing this analysis explicitly corrects. The conjunctive cost model is supported by academic analysis of anti-detect browser detection [13] and measurement studies of cybercrime commoditization [58].

### 6.6 Boundedness, Not Doom

Software-only client-side anti-automation defenses are economically bounded. They are bounded by the proxy supply market (variable cost ceiling), the temporal arms race (temporal cost ceiling), the human labor market (behavioral biometrics cost floor), and the ML synthesis capability curve (behavioral biometrics cost convergence). These ceilings are structural properties of the economic ecosystem in which the defenses operate, not implementation failures.

This does **not** imply that software-only defenses are "structurally doomed" or ineffective. It implies that their effectiveness is measured in economic terms: for any given defense, there exists a throughput volume and resource value at which the attack is economically viable, and a different volume and resource value at which it is not. The defense's job is to set the economic ceiling above the value of the protected resource for the relevant attacker population — and, by all available evidence, deployed software-only defenses (Botguard, Turnstile, reCAPTCHA v3) achieve this for the majority of real-world attack scenarios.

The appropriate analytical stance is: client-side attestation operates under a forgery model with economic ceilings, not a cryptanalysis model with mathematical guarantees. This is not pessimism — it is precision. The contributions of this SoK are in systematizing *which* economic mechanisms govern *which* architectures, enabling defenders and researchers to reason about trade-offs with analytical clarity rather than marketing terminology.

---

## 7. Industry Trajectory & Emerging Standards

### 7.1 DBSC and the Session-Hijacking Threat Model

Device Bound Session Credentials (DBSC) [36, 37] represent an architectural innovation: extending hardware-anchored determinism from the authentication moment (FIDO2/WebAuthn) to the session lifetime. A session cookie is cryptographically bound to a device-resident private key at session establishment. The browser periodically proves possession of the key (e.g., via a challenge-response protocol over HTTP headers) without user interaction.

The security property is straightforward: if an attacker exfiltrates the session cookie via infostealer malware, the stolen cookie cannot be redeemed from a different device because it lacks the private key. DBSC targets the session-hijacking threat model — one of the most prevalent attack vectors in the current threat landscape.

**Structural Limitations.** DBSC has two structural limitations that follow from its identity model:

1. **Non-substitutability for anonymous traffic:** DBSC requires a prior authenticated session. It cannot be applied to anonymous traffic screening (Quadrants I and II of the dual-axis threat model, Section 1.3). This is an architectural property, not an implementation gap.

2. **Infostealer economy as the bypass ceiling:** The attacker does not need to break the cryptographic binding between cookie and device key. Instead, the attacker compromises the legitimate user's device through PPI malware, exports the session state (including the running browser's ability to sign DBSC challenges), and proxies automated requests through the infected device. The economic bypass cost is the black-market price of a malware infection [53, 56], not the mathematical hardness of the attestation protocol. This is symmetric with the analysis in Section 4.5: hardware-anchored determinism is bounded by the PPI malware market, not by cryptographic parameters.

The infostealer ecosystem continues to adapt to new defenses. SpyCloud [57] documented infostealer malware specifically designed to bypass Chrome's app-bound cookie encryption — the very protection that DBSC aims to strengthen. The arms race between browser cookie protection and infostealer exfiltration is ongoing, and DBSC should be understood as raising the bar (requiring malware with real-time proxy capability rather than static cookie export) rather than eliminating the threat.

### 7.2 Passkeys and the Credential-Phishing Threat Model

Passkeys — the consumer-facing term for FIDO2/WebAuthn credentials synchronized across devices via platform credential managers — address the credential-phishing threat model. By replacing shared secrets (passwords) with public-key cryptography, Passkeys eliminate credential phishing as an attack vector: there is no password to phish.

The security and deployment characteristics of FIDO2/WebAuthn are well-studied. Kuchhal et al. [32] systematically evaluated the security posture of real-world FIDO2 deployments across the Tranco Top 1K websites, finding that approximately 94% of SafetyNet attestations are hardware-backed, but only 4.4% of authenticators carry Level 2+ certification offering malware resistance. Tarrach et al. [33] identified message integrity gaps in FIDO2 messages accessible to browser extensions, enabling local attacks. Islam et al. [35] proposed CASPER, a framework to detect abuse of synced passkeys leaked from cloud breaches.

**Structural Limitation.** Passkeys require prior enrollment — the user must register an authenticator with each relying party. They are inapplicable to anonymous traffic screening. This follows from the NIST SP 800-63-3 [65] identity model: hardware-enrolled authentication operates in the Authenticated + ATO quadrant only. The non-substitutability between Passkeys (deterministic, authenticated) and stateless VM attestation (probabilistic, anonymous) is an architectural property, not a competitive positioning.

### 7.3 Privacy Pass and the Anonymous-Attestation Trade-off

Privacy Pass and its deployable instantiations (Apple PAT [44], Cloudflare/Fastly issuers, WICG Private State Token API [45]) represent the most significant architectural innovation in anonymous attestation since the VM-based defense era began.

The protocol's cryptographic properties are well-established: the VOPRF construction achieves unlinkability between issuance and redemption, and the rate-limiting mechanism (per-device at issuance) prevents Sybil attacks from a single device. The formal security model by Chu et al. [43] proves the security of rate-limited Privacy Pass under standard assumptions, and the IETF standardization [38, 39, 40] provides a rigorous specification.

**The Trade-off.** The centralization-vs-anonymity trade-off is inherent in the PAT architecture, not a bug. Privacy Pass provides anonymous attestation — the issuer cannot link a redeemed token to a specific user. But the issuer *can* control who receives tokens in the first place. The attestation root of trust — the decision about which devices, accounts, and regions are eligible for token issuance — is controlled by the OS vendor.

In Apple's PAT deployment [44], token issuance is tied to the device's Secure Enclave attestation and the user's iCloud account standing. A device that fails attestation (jailbroken, tampered, running unauthorized software) cannot obtain PATs. An iCloud account with poor standing (e.g., flagged for abuse) may receive rate-limited or zero tokens. This is the mechanism that prevents Sybil attacks — and it is simultaneously the mechanism that centralizes access control.

The tension is structural, not resolvable by a better protocol design within the issuer-mediated anonymous attestation model. Any system where an issuer validates a device's or user's eligibility before signing tokens necessarily involves the issuer in access-control decisions. Decentralized alternatives — where eligibility is established through distributed mechanisms (zero-knowledge proofs of personhood, decentralized reputation systems, proof-of-stake eligibility) rather than issuer-mediated attestation — would eliminate the centralization pressure but have not yet been deployed in production.

### 7.4 The Centralization vs. Anonymity Dilemma

The preceding analysis identifies a structural trilemma in client-side anti-automation. We formulate it as follows:

The web faces a choice among three desirable properties:
- **(a) Anonymous access:** Users can access web resources without disclosing identity.
- **(b) Deterministic bot resistance:** The defense produces binary (not probabilistic) decisions about whether a client is a bot, with cryptographic guarantees.
- **(c) Decentralized trust:** No single vendor or small oligopoly controls the mechanism by which bot-resistance is determined.

No existing architecture satisfies all three:

| Architecture | (a) Anonymous Access | (b) Deterministic Bot Resistance | (c) Decentralized Trust |
|---|---|---|---|
| **Stateless VM Attestation** | Yes | No (probabilistic) | Yes |
| **Behavioral Biometrics** | Yes | No (probabilistic) | Yes |
| **Privacy Pass / PATs** | Yes | Yes | **No** (vendor oligopoly) |
| **DBSC** | No (requires auth) | Yes | Partially (multi-vendor, Google-led) |
| **FIDO2 / Passkeys** | No (requires enrollment) | Yes | Partially (multi-vendor standard) |

Privacy Pass achieves (a) and (b) but sacrifices (c). Traditional VM attestation achieves (a) and (c) but sacrifices (b) — its output is probabilistic and bounded by IP reputation, not cryptographically guaranteed. Hardware-anchored auth achieves (b) and (c) but sacrifices (a) — it requires identity binding.

This is presented as a **characterization of the current state**, not a proven impossibility result. Research into decentralized anonymous attestation — zero-knowledge proofs of personhood, distributed eligibility verification, multi-issuer Privacy Pass with threshold issuance — may resolve the trilemma. But at present, the field's defining structural challenge is not the "Anonymous Authentication Gap" (which PATs have technically closed) but the **Centralization vs. Anonymity Trade-off** that PATs introduce.

---

## 8. Open Problems & Future Research

This section identifies four open problems that emerge from the systematization. Each is a gap in the current literature that constrains progress in the field.

### 8.1 The Centralization vs. Anonymity Trade-off in PATs

Privacy Pass and PATs have solved the *technical* problem of anonymous deterministic attestation: it is now possible (though not universally deployed) to prove that a client is a legitimate device without revealing identity, with cryptographic guarantees. However, this solution has created an *economic and political* problem: a vendor oligopoly on "humanness."

The current PAT deployment architecture concentrates attestation authority in three companies: Apple (iOS/macOS attestation), Google (Android/ChromeOS attestation, Chrome Private State Token integration), and Microsoft (Windows attestation). This is not a design flaw — the architecture requires a trusted attestation source, and platform vendors are the natural source — but it raises structural concerns:

- **Market power:** A platform vendor could degrade or deny PAT issuance to competing services, browsers not owned by the platform vendor, or geographic regions.
- **Regulatory pressure:** Government compelled-access or compelled-denial regimes could apply pressure to centralized issuers.
- **Single point of policy failure:** Privacy policies, rate limits, and eligibility criteria are set unilaterally by each vendor, with no multi-stakeholder governance.

Research is needed on decentralized anonymous attestation that does not require trusting a platform vendor. Candidate approaches include:
- **Zero-knowledge proofs of personhood:** Cryptographic proof that a human performed some action without revealing which human, using decentralized eligibility verification (e.g., proof of unique biometric enrollment across multiple issuers).
- **Multi-issuer Privacy Pass with threshold issuance:** A client must obtain token signatures from a threshold of independent issuers, reducing reliance on any single issuer.
- **Decentralized reputation systems:** Blockchain-anchored or peer-to-peer reputation systems where eligibility is established through distributed consensus rather than issuer mediation.

The key research question is: Can we achieve the security properties of Privacy Pass (unlinkability, rate-limiting, Sybil resistance) without a centralized attestation root of trust?

### 8.2 Standardized Benchmarking (The "Bot-Bench" Problem)

Academia lacks a standardized, ethical testbed for evaluating client-side anti-automation defenses. Current evaluation methodologies are limited in three ways:

1. **Grey-hat reverse engineering:** Researchers reverse-engineer production VM defenses (Botguard, Turnstile) without vendor cooperation, producing analyses that are technically informative but legally ambiguous and not reproducible (the vendor can change the VM at any time in response to the publication).

2. **In-house prototypes:** Researchers build their own VM-based defenses and evaluate them against their own attacks, creating a circular evaluation loop where the defender's model knows the attacker's strategy.

3. **Small-scale PoCs:** Limited-scale experiments (e.g., single-digit IPs, short-duration measurement windows) produce results that cannot be generalized to the industrial-throughput regimes where the NLSP mechanisms are hypothesized to bind.

A standardized "Bot-Bench" — by analogy to ML benchmark suites (ImageNet, GLUE, SQuAD) or security evaluation frameworks (DARPA Cyber Grand Challenge) — would provide:
- A **vendor-neutral VM test harness** with known ground truth for each L1–L4 layer.
- **Standardized attacker capability levels** (e.g., commodity proxy pool, premium proxy pool, automated deobfuscation, ML trajectory synthesis).
- **Reproducible measurement** of cost-per-token across scale regimes without violating vendor ToS.

The BehavePassDB benchmark [23] for behavioral biometrics is a step in this direction but covers only one architectural class. A comprehensive benchmark spanning multiple architectures would transform anecdotal RE findings into systematic, comparable measurements.

### 8.3 Privacy Regulation vs. Stateful Mitigation (GDPR / Cookie Deprecation)

GDPR, the ePrivacy Directive, and browser-enforced tracking prevention (ITP in Safari, Enhanced Tracking Protection in Firefox, Total Cookie Protection) systematically degrade the persistent identifiers on which stateful behavioral telemetry depends. Third-party cookie deprecation in Chrome is proceeding on a phased timeline. Each of these developments constrains the profile-aging model that underpins reCAPTCHA v3, DataDome, and similar stateful defenses.

The tension between privacy regulation and stateful bot mitigation is under-studied in academic literature. Specific open questions include:

- **Effectiveness degradation:** As third-party cookies are deprecated and first-party cookie lifetimes are restricted (e.g., 7-day cap in ITP), how does the accuracy and economic ceiling of stateful telemetry change?
- **Alternative identifiers:** Are vendors shifting to fingerprinting-based identifiers (canvas, WebGL, audio context) as cookie-based identifiers degrade, and if so, does this shift increase or decrease the privacy cost of bot mitigation?
- **Regulatory risk:** Are stateful telemetry deployments compliant with GDPR's requirements for consent, purpose limitation, and data minimization? The "legitimate interest" basis used by many vendors has not been tested in court for bot-detection fingerprinting specifically.
- **Asymmetric impact:** Privacy-enhancing browser changes degrade stateful defenses but have no impact on stateless VM attestation, behavioral biometrics (which operate on ephemeral signals), or PATs (which use cryptographic tokens). Does privacy regulation create a structural shift toward architectures that are less privacy-invasive?

This represents a significant research gap. The intersection of privacy regulation, browser engineering, and anti-automation economics has been addressed in separate literatures (privacy law, browser security, bot mitigation) with little cross-disciplinary analysis.

### 8.4 The Temporal Arms Race: Formal Models of Compile Rotation

There is no formal model in the literature for the T_RE vs. T_Life dynamic in polymorphic VM defenses, particularly when T_RE is driven by automated symbolic execution rather than human labor.

The temporal arms race (Sections 5.7, 6.1) is currently described only qualitatively: the defender deploys compiles, the attacker reverse-engineers them, and the defense is effective when T_RE > T_Life. But this qualitative framing does not answer key quantitative questions:

- **Optimal compile rotation frequency:** Given a model of the attacker's RE pipeline speed (e.g., time to train a neural opcode mapper, time to execute differential analysis across compile versions), what compile rotation frequency maximizes the net window (T_Life − T_RE) while minimizing defender infrastructure cost?
- **Obfuscation diversity vs. rotation frequency:** Does varying the obfuscation *technique* (e.g., alternating between different VM architectures) increase T_RE more effectively than increasing rotation frequency of a single architecture? The information-theoretic limits of VM diversity within the JavaScript runtime constraint are unknown.
- **Compute-cost modeling for symbolic execution:** What is the relationship between VM complexity (number of opcodes, nesting depth of self-modifying code, number of environmental checks) and the symbolic execution time required to recover opcode semantics? Without this, the defender cannot predict the attacker's RE cost.
- **Economic equilibrium:** What is the steady-state equilibrium of the temporal arms race when both sides are automated? Does it converge to a particular compile rotation frequency, or does it exhibit cyclical behavior?

Research is needed on quantitative frameworks for modeling the temporal arms race. This research would ideally produce a formal economic model of compile rotation that accounts for automated RE, enabling rational investment decisions rather than heuristic compile schedules (e.g., "deploy daily regardless of whether the previous compile has been defeated").

---

## 9. Conclusion

This paper has presented a Systematization of Knowledge of client-side anti-automation architectures. We have proposed a five-class taxonomy — Stateless VM Attestation, Stateful Behavioral Telemetry, Behavioral Biometrics & Sensor Telemetry, Platform Anonymous Attestation (Privacy Pass / PATs), and Hardware-Anchored Determinism — and compared them across ten dimensions. We have generalized the L1–L4 defense-in-depth framework beyond its Botguard-specific origins, expanding L1 to include sensor telemetry and introducing the temporal constraint analysis that frames compile rotation as a race between the defender's automated obfuscator and the attacker's automated deobfuscator. We have provided a conceptual microeconomic analysis identifying three cost types — fixed, variable, and temporal — and three critical structural corrections: the conjunctive cost of anti-detect browsers, the human labor floor for behavioral biometrics, and the compute-driven nature of the temporal arms race.

The through-line of this analysis is that client-side anti-automation operates under a forgery model with economic ceilings, not a cryptanalysis model with mathematical guarantees. Each architectural class imposes costs on the adversary through a specific economic mechanism — proxy supply exhaustion, profile aging latency, ML inference or human labor, device compromise through PPI malware, or rate-limited token issuance — and each ceiling is bounded by a specific market or computational constraint. Understanding these ceilings as structural properties, rather than implementation limitations, provides the analytical clarity that the field has lacked.

The field's defining structural challenge has shifted. For over a decade, the "Anonymous Authentication Gap" — the inability to provide deterministic bot resistance to anonymous traffic — was the central open problem. Privacy Pass and Private Access Tokens have technically closed this gap, providing cryptographic anonymous attestation with formal security guarantees. But this closure has introduced a new challenge: the Centralization vs. Anonymity Trade-off. The attestation root of trust in PAT architectures is controlled by a platform vendor oligopoly, and whoever controls the root controls who may access the web anonymously. The field's next frontier is not incremental VM hardening or better behavioral models — it is the search for decentralized anonymous attestation that achieves the security properties of Privacy Pass without the structural centralization of the current issuer-mediated model.

This paper is a contribution in systematization. It does not present empirical measurements, new defenses, or attack techniques. It provides what an SoK should provide: a taxonomy that names and distinguishes, a framework that compares, an analysis that identifies structural ceilings, and a set of open problems that guide future research. In a field where vendor marketing often obscures architectural distinctions and where terminology is inconsistent across platforms, this systematization offers a common vocabulary and evaluation framework. We hope it will serve as a foundation for rigorous, comparative research in client-side anti-automation.

---

## Appendices

### Appendix A: Methodological Note

This SoK is a purely analytical and comparative work. It does not claim empirical measurements of live production systems. The analysis is based on published academic literature, IETF/W3C standards, peer-reviewed grey literature (vendor technical documentation, malware analysis reports), and the author's domain expertise in reverse engineering and bot mitigation architectures.

No live bot mitigation systems were instrumented or tested as part of this research. All descriptions of vendor architectures are based on publicly available documentation and academic analyses, not on reverse engineering of proprietary systems. The economic analysis is conceptual: it identifies mechanisms and structural ceilings without fitting parametric cost models to empirical data.

The PRISMA flow diagram (Section 3.4) and the 75-reference bibliography (Section References) provide a complete audit trail of the sources on which this systematization is based. All grey-literature citations have been archived via the Internet Archive Wayback Machine, and citations use permanent archive links to protect against vendor content modification or deletion.

### Appendix B: Figure and Table Index

The following standalone LaTeX/TikZ figures accompany this manuscript:

- `figures/prisma-flow.tex` — PRISMA flow diagram (Section 3.4)
- `figures/taxonomy-table.tex` — Grand Taxonomy Table (Section 4.6)
- `figures/auth-spectrum.tex` — Anonymous-Authentication Spectrum (Section 4.7)

These figures are drafted natively in LaTeX/TikZ and should be compiled with pdflatex or lualatex for inclusion in the final manuscript.

---

## References

[1] J. Bonneau, A. Miller, J. Clark, A. Narayanan, J. A. Kroll, and E. W. Felten. "SoK: Research Perspectives and Challenges for Bitcoin and Cryptocurrencies." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2015. DOI: 10.1109/SP.2015.14.

[2] K. Thomas et al. "SoK: Hate, Harassment, and the Changing Landscape of Online Abuse." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00028.

[3] Y. Wu, W. K. Edwards, and S. Das. "SoK: Social Cybersecurity." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2022. DOI: 10.1109/SP46214.2022.9833757.

[4] N. Mathews, J. K. Holland, S. E. Oh, M. S. Rahman, N. Hopper, and M. Wright. "SoK: A Critical Evaluation of Efficient Website Fingerprinting Defenses." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2023. DOI: 10.1109/SP46215.2023.10179289.

[5] T. Rokicki, C. Maurice, and P. Laperdrix. "SoK: In Search of Lost Time: A Review of JavaScript Timers in Browsers." In *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, 2021. DOI: 10.1109/EuroSP51992.2021.00039.

[6] P. Laperdrix, N. Bielova, B. Baudry, and G. Avoine. "Browser Fingerprinting: A Survey." *ACM Trans. Web*, Vol. 14, No. 2, Article 8, pp. 1–33, 2020. DOI: 10.1145/3386040.

[7] U. Iqbal, S. Englehardt, and Z. Shafiq. "Fingerprinting the Fingerprinters: Learning to Detect Browser Fingerprinting Behaviors." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021.

[8] A. Gómez-Boix, P. Laperdrix, and B. Baudry. "Hiding in the Crowd: An Analysis of the Effectiveness of Browser Fingerprinting at Large Scale." In *Proc. The Web Conference (WWW)*, pp. 309–318, 2018. DOI: 10.1145/3178876.3186097.

[9] T. Laor et al. "DRAWNAPART: A Device Identification Technique based on Remote GPU Fingerprinting." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2022.

[10] S. Wu, P. Sun, Y. Zhao, and Y. Cao. "Him of Many Faces: Characterizing Billion-scale Adversarial and Benign Browser Fingerprints on Commercial Websites." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023.

[11] X. Lin, P. Ilia, S. Solanki, and J. Polakis. "Phish in Sheep's Clothing: Exploring the Authentication Pitfalls of Browser Fingerprinting." In *Proc. USENIX Security Symposium*, 2022.

[12] Z. Liu, P. Shrestha, and N. Saxena. "Gummy Browsers: Targeted Browser Spoofing against State-of-the-Art Fingerprinting Techniques." In *Proc. International Conference on Applied Cryptography and Network Security (ACNS)*, June 2022. arXiv: 2110.10129.

[13] B. A. Azad, O. Starov, P. Laperdrix, and N. Nikiforakis. "Taming the Shape Shifter: Detecting Anti-fingerprinting Browsers." In *Proc. DIMVA*, 2020.

[14] N. Andriamilanto, T. Allard, G. Le Guelvouit, and A. Garel. "A Large-scale Empirical Analysis of Browser Fingerprints Properties for Web Authentication." *ACM Trans. Web*, Vol. 16, No. 1, Article 1, pp. 1–62, 2022. DOI: 10.1145/3478026.

[15] A. Acien, A. Morales, J. Fierrez, R. Vera-Rodriguez, and O. Delgado-Mohatar. "BeCAPTCHA: Behavioral Bot Detection using Touchscreen and Mobile Sensors benchmarked on HuMIdb." *Engineering Applications of Artificial Intelligence*, Vol. 98, 104058, 2021. DOI: 10.1016/j.engappai.2020.104058.

[16] A. Acien, A. Morales, J. Fierrez, and R. Vera-Rodriguez. "BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection." *Pattern Recognition*, Vol. 127, 108643, 2022. DOI: 10.1016/j.patcog.2022.108643.

[17] H. Niu, J. Chen, Z. Zhang, and Z. Cai. "Mouse Dynamics Based Bot Detection Using Sequence Learning." In *Biometric Recognition (CCBR)*, LNCS Vol. 12878, pp. 49–56. Springer, 2021. DOI: 10.1007/978-3-030-86608-2_6.

[18] H. Niu, C. Cheng, and Z. Cai. "Learning Human Behavior for Bot Detection: A Perspective on Mouse Movement (MouseAgent)." In *Proc. China Automation Congress (CAC)*, pp. 6575–6580. IEEE, 2023. DOI: 10.1109/CAC59555.2023.10451138.

[19] C. Iliou, T. Kostoulas, T. Tsikrika, V. Katos, S. Vrochidis, and I. Kompatsiaris. "Detection of Advanced Web Bots by Combining Web Logs with Mouse Behavioural Biometrics." *Digital Threats: Research and Practice*, Vol. 2, No. 3, Article 24, pp. 1–26. ACM, 2021. DOI: 10.1145/3447815.

[20] H. Fereidooni et al. "AuthentiSense: A Scalable Behavioral Biometrics Authentication Scheme using Few-Shot Learning for Mobile Platforms." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.24044.

[21] S. Sadeghpour and N. Vlajic. "ReMouse Dataset: On the Efficacy of Measuring the Similarity of Human-Generated Trajectories for the Detection of Session-Replay Bots." *Journal of Cybersecurity and Privacy*, Vol. 3, No. 1, pp. 95–117. MDPI, 2023. DOI: 10.3390/jcp3010007.

[22] D. DeAlcala et al. "BeCAPTCHA-Type: Biometric Keystroke Data Generation for Improved Bot Detection." In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, pp. 1051–1060. IEEE, 2023. DOI: 10.1109/CVPRW59228.2023.00112.

[23] G. Stragapede, R. Vera-Rodriguez, R. Tolosana, and A. Morales. "BehavePassDB: Public Database for Mobile Behavioral Biometrics and Benchmark Evaluation." *Pattern Recognition*, 2022. DOI: 10.1016/j.patcog.2022.109010.

[24] S. Schrittwieser, S. Katzenbeisser, J. Kinder, G. Merzdovnik, and E. Weippl. "Protecting Software through Obfuscation: Can It Keep Pace with Progress in Code Analysis?" *ACM Comput. Surv.*, Vol. 49, No. 1, Article 4, pp. 1–37, 2016. DOI: 10.1145/2886012.

[25] P. Saxena, D. Akhawe, S. Hanna, F. Mao, S. McCamant, and D. Song. "A Symbolic Execution Framework for JavaScript." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, pp. 513–528, 2010.

[26] T. Blazytko, M. Contag, C. Aschermann, and T. Holz. "Syntia: Synthesizing the Semantics of Obfuscated Code." In *Proc. USENIX Security Symposium*, pp. 643–659, 2017.

[27] M. Schloegel et al. "Loki: Hardening Code Obfuscation Against Automated Attacks." In *Proc. USENIX Security Symposium*, pp. 3055–3073, 2022.

[28] B. Rozière, M. Lachaux, L. Chanussot, and G. Lample. "DOBF: A Deobfuscation Pre-Training Objective for Programming Languages." In *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. 34, 2021. arXiv: 2102.07492.

[29] V. Raychev, M. Vechev, and A. Krause. "Predicting Program Properties from 'Big Code'." In *Proc. ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL)*, pp. 111–124, 2015. DOI: 10.1145/2676726.2677009.

[30] K. Coogan, G. Lu, and S. Debray. "Deobfuscation of Virtualization-Obfuscated Software: A Semantics-Based Approach." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 275–284, 2011. DOI: 10.1145/2046707.2046739.

[31] J. Hodges, J.C. Jones, M.B. Jones, A. Kumar, and E. Lundberg, Eds. "Web Authentication: An API for Accessing Public Key Credentials, Level 2." *W3C Recommendation*, 8 April 2021.

[32] D. Kuchhal, M. Saad, A. Oest, and F. Li. "Evaluating the Security Posture of Real-World FIDO2 Deployments." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 2381–2395, 2023. DOI: 10.1145/3576915.3623063.

[33] T. Tarrach et al. "A Security and Usability Analysis of Local Attacks Against FIDO2." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2024.

[34] M. Kepkowski, L. Hanzlik, I. D. Wood, and M. A. Kaafar. "How Not to Handle Keys: Timing Attacks on FIDO Authenticator Privacy." In *Proc. Privacy Enhancing Technologies Symposium (PETS)*, Vol. 2022, No. 4, pp. 705–726, 2022. DOI: 10.56553/popets-2022-0129.

[35] M. Islam, S. S. Arora, R. Chatterjee, and K. C. Wang. "Detecting Compromise of Passkey Storage on the Cloud." In *Proc. USENIX Security Symposium*, pp. 7743–7762, 2025.

[36] D. Rubery and K. Monsen, Eds. "Device Bound Session Credentials (DBSC)." *W3C Web Application Security Working Group / WICG*, 2024.

[37] Google Chrome Security Team. "Fighting Cookie Theft Using Device Bound Sessions." *Chromium Blog*, 2 April 2024.

[38] A. Davidson, J. Iyengar, and C. A. Wood. "The Privacy Pass Architecture." *RFC 9576*, IETF, June 2024. DOI: 10.17487/RFC9576.

[39] T. Pauly, S. Valdez, and C. A. Wood. "The Privacy Pass HTTP Authentication Scheme." *RFC 9577*, IETF, June 2024. DOI: 10.17487/RFC9577.

[40] S. Celi, A. Davidson, S. Valdez, and C. A. Wood. "Privacy Pass Issuance Protocols." *RFC 9578*, IETF, June 2024. DOI: 10.17487/RFC9578.

[41] A. Davidson, I. Goldberg, N. Sullivan, G. Tankersley, and F. Valsorda. "Privacy Pass: Bypassing Internet Challenges Anonymously." *Proc. on Privacy Enhancing Technologies (PoPETs)*, Vol. 2018, No. 3, pp. 164–180, 2018. DOI: 10.1515/popets-2018-0026.

[42] B. Kreuter, T. Lepoint, M. Orrù, and M. Raykova. "Anonymous Tokens with Private Metadata Bit." In *Advances in Cryptology — CRYPTO 2020*, pp. 308–336. Springer, 2020. DOI: 10.1007/978-3-030-56784-2_11.

[43] H. Chu, K. Do, S. Faller, and L. Hanzlik. "On the Security of Rate-limited Privacy Pass." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2023. ePrint: 2023/1805.

[44] Apple Inc. "Replace CAPTCHAs with Private Access Tokens." *WWDC22 Session*, June 8, 2022.

[45] WICG. "Private State Token API." *WICG Community Group Draft*.

[46] R. Anderson and T. Moore. "The Economics of Information Security." *Science*, Vol. 314, No. 5799, pp. 610–613, 2006. DOI: 10.1126/science.1130992.

[47] C. Herley and D. Florêncio. "Nobody Sells Gold for the Price of Silver: Dishonesty, Uncertainty and the Underground Economy." In *Proc. Workshop on the Economics of Information Security (WEIS)*, June 2009. Published in T. Moore, D. Pym, and C. Ioannidis (Eds.), *Economics of Information Security and Privacy*, pp. 33–53. Springer, 2010. DOI: 10.1007/978-1-4419-6967-5_3.

[48] T. Moore. "The Economics of Cybersecurity: Principles and Policy Options." *Int. J. Crit. Infrastruct. Prot.*, Vol. 3, No. 3, pp. 103–117, 2010. DOI: 10.1016/j.ijcip.2010.10.002.

[49] H. R. Varian. *Intermediate Microeconomics: A Modern Approach*, 9th ed. W. W. Norton & Company, 2014.

[50] R. Anderson et al. "Measuring the Cost of Cybercrime." In R. Böhme (Ed.), *The Economics of Information Security and Privacy*, pp. 265–300. Springer, 2013. DOI: 10.1007/978-3-642-39498-0_12.

[51] M. Motoyama, K. Levchenko, C. Kanich, D. McCoy, G. M. Voelker, and S. Savage. "Re: CAPTCHAs—Understanding CAPTCHA-Solving Services in an Economic Context." In *Proc. USENIX Security Symposium*, 2010.

[52] M. Motoyama, D. McCoy, K. Levchenko, S. Savage, and G. M. Voelker. "Dirty Jobs: The Role of Freelance Labor in Web Service Abuse." In *Proc. USENIX Security Symposium*, 2011.

[53] J. Caballero, C. Grier, C. Kreibich, and V. Paxson. "Measuring Pay-per-Install: The Commoditization of Malware Distribution." In *Proc. USENIX Security Symposium*, 2011.

[54] A. Côté Cyr. "Life on a Crooked RedLine: Analyzing the Infamous Infostealer's Backend." *ESET Research / WeLiveSecurity*, November 8, 2024.

[55] Microsoft Threat Intelligence. "Lumma Stealer: Breaking Down the Delivery Techniques and Capabilities of a Prolific Infostealer." *Microsoft Security Blog*, May 21, 2025.

[56] S. Pastrana, A. Hutchings, D. R. Thomas, and J. Tapiador. "Malware Finances and Operations: A Data-Driven Study of the Value Chain for Infections and Compromised Access." *arXiv:2306.15726*, 2023.

[57] SpyCloud. "How Infostealer Malware Bypassed Chrome's App-Bound Cookie Encryption." *SpyCloud Blog*, 2024.

[58] R. van Wegberg, B. Klievink, M. van Eeten, et al. "Plug and Prey? Measuring the Commoditization of Cybercrime via Online Anonymous Markets." In *Proc. USENIX Security Symposium*, pp. 1009–1026, 2018.

[59] K. Thomas et al. "Framing Dependencies Introduced by Underground Commoditization." In *Proc. Workshop on the Economics of Information Security (WEIS)*, 2015.

[60] Cloudflare, Inc. "Bot Management Technical Documentation." 2023–2024.

[61] Google Chrome Security Team. "Device Bound Session Credentials (DBSC)." *Chrome for Developers*, 2024.

[62] Human Security, Inc. (formerly PerimeterX). "The Economics of Bot Mitigation." *Industry Whitepaper*, 2022.

[63] Kasada Pty Ltd. "Polymorphic Security Technical Documentation." 2023.

[64] DataDome SAS. "Bot Detection and Mitigation Technical Overview." 2023.

[65] P. A. Grassi et al. "Digital Identity Guidelines." *NIST Special Publication 800-63-3*, 2017.

[66] OWASP Foundation. "Automated Threat Handbook." *OWASP Project*, 2018–2024.

[67] R. Fielding and J. Reschke, Eds. "The OAuth 2.0 Authorization Framework: Bearer Token Usage." *RFC 6750*, IETF, October 2012.

[68] M. Jones, J. Bradley, and N. Sakimura. "JSON Web Token (JWT)." *RFC 7519*, IETF, May 2015.

[69] D. Fett, B. Campbell, J. Bradley, T. Lodderstedt, M. Jones, and D. Waite. "OAuth 2.0 Demonstrating Proof of Possession (DPoP)." *RFC 9449*, IETF, September 2023.

[70] J. H. Saltzer and M. D. Schroeder. "The Protection of Information in Computer Systems." *Proc. IEEE*, Vol. 63, No. 9, pp. 1278–1308, 1975.

[71] E. Bursztein, M. Martin, and J. C. Mitchell. "Text-based CAPTCHA Strengths and Weaknesses." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2012. DOI: 10.1145/2046707.2046724.

[72] J. Bonneau, C. Herley, P. C. van Oorschot, and F. Stajano. "Passwords and the Evolution of Imperfect Authentication." *Commun. ACM*, Vol. 58, No. 7, pp. 78–87, 2015. DOI: 10.1145/2699390.

[73] M. Guerar, L. Verderame, M. Migliardi, F. Palmieri, and A. Merlo. "Gotta CAPTCHA 'Em All: A Survey of 20 Years of the Human-or-Computer Dilemma." *ACM Comput. Surv.*, Vol. 54, No. 9, Article 192, pp. 1–33, 2021. DOI: 10.1145/3477142.

[74] E. Ulqinaku, H. Assal, A. A. Gkaniatsas, S. Schechter, and S. Capkun. "Is Real-time Phishing Eliminated with FIDO?" In *Proc. USENIX Security Symposium*, 2021.

[75] L. Allodi. "Economic Factors of Vulnerability Trade and Exploitation: Empirical Evidence from a Prominent Russian Cybercrime Market." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 1483–1499, 2017. DOI: 10.1145/3133956.3133960.

---

*This document is a Systematization of Knowledge (SoK) paper. It provides analytical clarity and a structured taxonomy of client-side anti-automation architectures. It does not contain empirical measurements, novel attacks, or new defenses.*
