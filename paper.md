# SoK: Client-Side Anti-Automation Under VLM-Based Attack — From Probabilistic Forgery to Operator Synthesis

---

**Authors:** Anonymous submission

**Keywords:** Client-side attestation, VLM-based automation, operator synthesis, browser fingerprinting, behavioral biometrics, Privacy Pass, Private Access Tokens, device-bound session credentials, anti-automation economics, systematization of knowledge

---

## Abstract

Client-side anti-automation assumes that a bot must subvert the browser it runs in. Vision-Language Model (VLM) computer-use agents break that assumption: they perceive the rendered page and inject OS-level input into an unmodified browser, an attack vector we call Operator Synthesis. We systematize five defense paradigms — point-in-time VM attestation, stateful behavioral telemetry, behavioral biometrics, platform anonymous attestation, and hardware-anchored session binding — and propose an L1–L4 analytical model of Botguard-style VMs to explain why their cost-imposing layers lose force when the attacker no longer touches the runtime. We then give a structured, explicitly caveated cost-accounting exercise based on VLM inference pricing, proxy supply, and state orchestration. Hardware-anchored schemes are not VLM-resilient; they are indifferent to input modality and move attacker cost to acquiring real enrolled devices and accounts. Finally, we document how attestation dependence concentrates trust in a few platform vendors and issuers, and outline open problems.

**Contributions:**

1. An L1–L4 analytical model of client-side VM attestation, synthesised from public descriptions of Botguard-style VMs and the obfuscation literature, used to diagnose why probabilistic defenses degrade under Operator Synthesis.
2. A structured cost-accounting exercise for Operator Synthesis attacks, grounded in VLM inference pricing, proxy market supply, and state-orchestration overhead, with its empirical gaps stated.
3. An analysis of attestation market centralization: which platform vendors and issuers hold the roots of trust for Private Access Tokens, Privacy Pass, Device Bound Session Credentials, and passkeys.

---

## 1. Introduction

### 1.1 Why the Field Still Needs a Taxonomy — And Why It Must Be a Diagnostic One

Client-side anti-automation has, over fifteen years, produced a rich but terminologically fractured design space. Vendors describe structurally different mechanisms using overlapping vocabulary: "bot detection" may refer to a point-in-time VM executing encrypted bytecode (Google Botguard), a long-term behavioral scoring engine (reCAPTCHA v3), or a hardware-attestation protocol (Apple Private Access Tokens) [1, 2]; Google's own published work on client challenges addresses the narrower task of device-class fingerprinting [3]. "Fingerprinting" can denote passive environmental introspection, active behavioral telemetry, or cryptographic token issuance [4, 5]. This imprecision obstructs comparative analysis.

Since 2024, computer-use agents have made a further distinction unavoidable. OpenAI's Operator is powered by its Computer-Using Agent (CUA) model, which combines GPT-4o's vision with reinforcement-learned GUI control [6]; Anthropic exposes a "computer use" capability for Claude models; and research agents such as WebVoyager [7] operate real browsers from screenshots. These systems drive an unmodified browser from outside it. We call this attack vector *Operator Synthesis* and use it as the organising lens: we first analyse what probabilistic client-side defenses were built to detect (Section 3), then ask which of their properties survive when the attacker never touches the browser runtime (Sections 4–6).

### 1.2 Contributions

This paper makes three contributions:

**C1 — An L1–L4 Analytical Model of VM Attestation (Section 3.4).** No primary technical description of Botguard's internals is public. We therefore propose our own four-layer model, synthesised from public descriptions of Botguard-style VMs [3] and from the obfuscation literature [8], and use it as a diagnostic lens for *why* VM-based attestation loses cost-imposing force under Operator Synthesis, not as a prescriptive architecture.

**C2 — A Cost-Accounting Exercise for VLM-Driven Attacks (Section 5).** We estimate attacker costs from observable market data: VLM inference pricing, proxy market supply, state-orchestration overhead, and the latency cost of per-action inference. We extend the conjunctive cost framework to the VLM attacker's state-isolation requirements and state the empirical gaps that prevent precise quantification.

**C3 — Attestation Market Centralization Analysis (Section 6).** Building on the centralization tension identified in anonymous token issuance [9, 10], we analyse which parties hold the roots of trust: Apple as PAT attester, third-party issuers such as Cloudflare and Fastly, Google as the driver of DBSC, and platform vendors as passkey synchronisers. We describe how this dependency turns the "Anonymous Authentication Gap" into an economic and governance centralization problem. We further analyze how the 2026 Private Access Control Tokens (PACT) initiative [11] extends this consolidation from device root-of-trust infrastructure to issuer judgment, introducing a software-anchor variant of anonymous attestation whose Sybil economics and governance remain unresolved (Section 6.4).

**Scope.** This SoK covers client-side anti-automation mechanisms deployed in web browsers. Purely server-side defenses (WAF, TLS fingerprinting, DDoS scrubbing, rate limiting) are excluded as they operate under different economic models. The historical retrospective (Part I) covers 2010–2024. The forward-looking analysis (Part II) covers the Operator Synthesis paradigm as it has emerged in 2024–2025 and as it applies to near-future (2026–2028) defense research.

**Scope limitation: the Advanced Persistent Bot threat model.** We distinguish three tiers of adversary capability. (1) **Commodity Bot:** basic scraper scripts, `curl`, standard headless browsers, Puppeteer deployed at low scale. (2) **Sophisticated Automation (Middle Tier):** Puppeteer/Playwright farms with residential proxy integration, anti-detect browser licenses, and aged-profile management. These adversaries achieve effective bypass of probabilistic defenses through engineering investment rather than VLM inference, and their cost structure is dominated by proxy subscriptions ($500–$5,000/month per operator) plus anti-detect browser licensing ($30–$300/month per operator, team plans up to $500/month). The probabilistic defenses of the 2010–2024 era face significant pressure from this middle tier alone (Section 4.2). (3) **Advanced Persistent Bot (APB):** highly-resourced adversaries utilizing VLMs, custom orchestration, and industrial-scale proxy infrastructure, whose cost structure is dominated by VLM inference rather than anti-detect browser licensing. The middle tier establishes a baseline of degradation: VLMs amplify this degradation rather than causing it de novo. Our analysis focuses on VLM adoption as the capability that most intensifies the structural pressure on probabilistic defenses for the top tier of adversaries. Claims about defense "degradation" should be read through this lens: a defense may be substantially degraded for APBs (and, to a lesser extent, for the middle tier) while remaining economically viable against Commodity Bots.

### 1.3 Threat Model: A Three-Axis Framework with Axis C as the Primary Lens

We adopt a three-axis threat model, with Axis C elevated from a supplementary dimension to the central analytical lens:

- **Axis A — Authentication State:** Anonymous (no prior identity assertion) vs. Authenticated (identity established through a credential). Anchored on NIST SP 800-63-3 [12].

- **Axis B — Attack Objective:** Resource Exhaustion/Scraping vs. Account Takeover/Fraud. Anchored on OWASP Automated Threat Handbook [13].

- **Axis C — Attack Vector, defined by where input is injected:** **Environmental Forgery** injects input and forges signals *inside* the browser runtime (DOM APIs, synthesized JavaScript events, CDP/WebDriver instrumentation, patched builds). **Operator Synthesis** injects OS-level input events into an *unmodified* browser, with a VLM or agentic system choosing the actions from the rendered screen. This is the primary axis of analysis for this SoK.

The quadrant mapping for Axes A and B is as follows:

| | **Anonymous** | **Authenticated** |
|---|---|---|
| **Scraping / Resource Exhaustion** | Quadrant I: Point-in-Time VM, Behavioral Biometrics, Compute-Bound Challenges (auxiliary) [13] | Quadrant III: Session-bound rate limiting, quota enforcement |
| **Account Takeover / Fraud** | Quadrant II: Stateful Telemetry (login risk scoring), Platform Anonymous Attestation (PATs) [13] | Quadrant IV: Hardware-Anchored Determinism (DBSC, Passkeys, WebAuthn) [12] |

Table: The Axis A/B threat-model quadrant matrix in NIST 800-63 terminology [12, 13].

Axis C cuts across all four quadrants. Under Environmental Forgery, the attacker instruments the browser runtime to forge sensor data to a defensive VM. Under Operator Synthesis, the attacker drives an unmodified stock browser via OS-level accessibility APIs or GUI automation. The distinction is not a minor implementation detail: the defender's historical assumption — that the attacker must subvert the browser — no longer holds for the most capable adversary class. OS-level input injection itself is not new — xdotool, AutoHotkey, and PyAutoGUI long predate VLMs. What the VLM adds is perception and cross-site generalisation: the attacker no longer needs per-site scripts or selectors, so OS-level injection becomes cheap to apply at scale. Detection then moves to other layers (container artifacts, input kinematics, inference cadence; Sections 4.1 and 5.2).

### 1.4 Operator Synthesis as the Central Framing Device

Computer-use VLMs — OpenAI's CUA (the model behind Operator) [6], Claude models with the computer-use capability, Gemini models, and research agents such as WebVoyager [7] — give the Advanced Persistent Bot (APB) a practical way to realise Operator Synthesis. A VLM operating in a virtual machine environment can "see" the rendered browser via screen capture and "act" through synthesized mouse and keyboard events. Critically:

1. **The browser is legitimate.** The VLM does not need to instrument the DOM, forge `navigator` properties, subvert WebGL rendering, or bypass chronometric traps. It drives an unmodified Chrome, Firefox, or Safari instance exactly as a human would.

2. **The motor control is an emergent property with a critical orchestration dependency.** VLMs are trained on web-scale human demonstrations of computer use. The coordinate outputs, action selections, and timing distributions they generate draw from the same distribution as human operators — they do not require a separately trained GAN for trajectory generation. However, a critical engineering gap exists between VLM output and OS-level input. Frontier VLMs output text, JSON bounding boxes, or structured action specifications; they do not natively generate raw OS-level hardware interrupts, mouse event streams, or keyboard scancodes. An orchestration layer — PyAutoGUI, xdotool, OS accessibility APIs, or a custom agentic wrapper (an orchestrator that injects via Puppeteer/CDP instead falls back into Environmental Forgery) — must translate the VLM's coordinate selection into a concrete kinematic trajectory (e.g., a Bezier curve from the cursor's current position to the target coordinate). If this orchestration layer uses naive linear interpolation, constant-velocity profiles, or generic ease-in/ease-out curves, the resulting mouse kinematics remain statistically distinguishable from human movement, and behavioral biometrics (Type III) retain detection leverage *even when the VLM's cognitive task selection is correct*. The attacker must invest additional engineering effort — a kinematic-smoothing layer, gaze-informed trajectory planning, or hardware-backed input synthesis — to close this gap. Motor control is not a turnkey property of the VLM; it is a property that the attacker must instantiate through a non-trivial orchestration pipeline, and the quality of that instantiation directly determines whether L1b detection remains viable (L1–L4 defined in Section 3.4).

3. **The asymmetry is inverted.** In the traditional model, the defender executes code in an environment the attacker owns. Under Operator Synthesis, the attacker's browser environment is *legitimate* from the perspective of the JavaScript runtime. The defender's code executes in an environment that passes the principal integrity checks, because no DOM-level or runtime-level instrumentation has occurred. However, as Sections 4.1 and 5.1 discuss, industrial-scale VLM deployment introduces environmental artifacts at the OS and network layers that a sophisticated defender can still detect.

Formally, we define **input synthesis** as the translation of a VLM's perceptual and action-selection output into OS-level input events (mouse, keyboard, touch), as distinct from the programmatic input injection — DOM API calls, synthesized JavaScript events — that characterizes Environmental Forgery. The distinction matters because programmatic input is observable from inside the browser runtime, whereas synthesized OS-level input is not: it is indistinguishable from physical input at the JavaScript layer, and only becomes observable through deployment-layer signals (Sections 4.1, 5.2).

**A working scenario.** The abstraction is easier to ground with a concrete (if hypothetical) instance. Consider an APB operator running a ticket-harvesting operation against a Botguard-protected checkout flow. The operator provisions a small cluster of containers, each running an unmodified stock Chrome browser whose traffic egresses through a residential proxy. An orchestration service wraps a frontier computer-use VLM: it captures each container's rendered screen, prompts the model to locate the VM challenge's visual target, and translates the returned coordinates into synthetic mouse events through an OS-level input API. The VLM never inspects the defensive VM's bytecode, and the browser's JavaScript runtime observes no instrumentation — from the defender's vantage, the session is a genuine user on a genuine device. What the defender retains is not a DOM- or runtime-layer signal but a deployment-layer one: container-specific environment leaks (missing fonts, GPU-stack mismatches; Section 4.1), the second-scale cadence of VLM inference between actions (Section 5.2), and the burn-down of the proxy pool's shared reputation (Section 5.3). The same perceive–select–synthesize loop is visible in legitimate computer-use agents (WebVoyager [7], Mind2Web [14]); the adversarial variant differs in its deployment stack, not in the input-synthesis mechanism.

This paper treats Operator Synthesis as the central framing device, not a future concern or a supplementary analysis section. Every architecture evaluated in Part I is assessed through the lens of Operator Synthesis. The resilience tiers established in Section 4 apply consistently across all evaluated paradigms. We use "Operator Synthesis" and "VLM-based attack" interchangeably throughout.

---

## 2. Background and Related Work

### 2.1 A Brief History of Client-Side Anti-Automation

The history of client-side anti-automation can be divided into five overlapping eras:

**Pre-2005: Server-Side Heuristics.** Bot detection through IP reputation, request rate analysis, and User-Agent header inspection. No client-side execution.

**2005–2012: The CAPTCHA Era.** Text-distortion, image-recognition, and audio CAPTCHAs tested human perceptual ability [15, 16]. OCR and CNN-based solvers progressively eroded CAPTCHA effectiveness. CAPTCHA-solving farms emerged as economic bypass mechanisms (∼$1 per 1,000 solved CAPTCHAs) [17]. By 2014, a deep network trained for Street View house numbers solved the hardest category of reCAPTCHA text challenges with 99.8% accuracy [18; see also 16]. Semantic image CAPTCHAs fell to off-the-shelf image annotation shortly after [19], and a 2023 large-scale user study found modern CAPTCHAs slow for humans while automated solvers reported in the literature match or exceed human accuracy [20]. Visual CAPTCHAs remain in production as fallback escalation paths (Arkose Labs, hCaptcha), but ceased to be the standalone frontier of defense.

**2010–2017: The JavaScript Challenge Era.** JavaScript challenge pages (e.g., Cloudflare's) and reCAPTCHA v2's "I'm not a robot" checkbox, introduced in December 2014 [21], shifted the defense to testing JavaScript execution capability and client-side risk signals. Headless browser automation (PhantomJS, Selenium, later Puppeteer) steadily closed this gap.

**c. 2013–2020: VM-Based Attestation.** Custom JavaScript VMs executing obfuscated bytecode (Google Botguard, publicly analysed by independent researchers from around 2013; later Kasada and others) defined the next escalation. In our model (Section 3.4), the adversary must execute the defender's VM faithfully in an environment that looks like a real browser, within timing constraints, while the served program changes over time [3, 22].

**2020–Present: Diversification and the VLM Paradigm Shift.** Four parallel developments define the present landscape: (a) stateful behavioral telemetry (reCAPTCHA v3, DataDome); (b) behavioral biometrics and sensor telemetry [23–25]; (c) anonymous attestation protocols (Privacy Pass, PATs, and from 2026 Private Access Control Tokens) [1, 5, 11, 26]; (d) hardware-anchored session determinism (DBSC) [27, 28]. The 2024 emergence of production VLMs introduced Operator Synthesis as a fifth development that substantially weakens (a) and (b) against the APB threat model. From 2025, empirical demonstrations of generalized VLM-based CAPTCHA solving [29, 30] closed the loop on the CAPTCHA era's residual fallback paths, turning the visual challenge from a perceptual test into a tractable inference task.

### 2.2 From CAPTCHAs to JavaScript VMs

The transition from CAPTCHAs to VM-based attestation represents a shift from proving *humanness* through task completion to proving *environmental integrity* — that the JavaScript runtime, DOM, WebGL, and timer APIs behave as they would in a legitimate browser [3, 4]. The canonical fingerprinting survey by Laperdrix et al. [4] catalogs the breadth of the measurement surface; subsequent studies quantified fingerprinting at scale [31–33], showed that fingerprinting behavior is itself detectable [34], and demonstrated targeted spoofing of individual measurement dimensions [35]. Related systematizations in adjacent subfields follow the same method [36]. The defense does not need any single measurement to be unforgeable; it needs the *set* of measurements to be jointly difficult to forge consistently. The structural weakness is a failure of *complete mediation* in Saltzer and Schroeder's sense [37]: the check runs inside an environment the attacker controls, so it cannot mediate every access.

### 2.3 From Probabilistic Scoring to Hardware-Anchored Determinism

Probabilistic defenses (VM attestation, behavioral telemetry) produce confidence scores derived from noisy sensor data whose deployment as authentication signals carries documented pitfalls [38]. Deterministic defenses (FIDO2/WebAuthn, DBSC) produce cryptographic proof of hardware key possession [12, 39]. The non-substitutability follows from the NIST Digital Identity Guidelines [12]: deterministic architectures require prior enrollment and cannot screen anonymous traffic.

Privacy Pass [40] and Apple PATs [1] introduced a third category: *deterministic attestation of anonymous traffic*, bridging the "Anonymous Authentication Gap" through cryptographic protocols (VOPRF with DLEQ proofs, RSA blind signatures) [5, 41, 42]. However, as Section 6 details, this closure comes at the cost of vendor centralization. The 2026 Private Access Control Tokens (PACT) initiative [11] complicates this category in a direction central to this SoK: it demonstrates that the category is not inherently hardware-anchored. PACT, announced by Cloudflare with Mozilla, Google, Microsoft, and Shopify, extends Privacy Pass to attest personhood or account standing through *issuer judgment* — active subscriptions, account standing, or issuer vouching — rather than device hardware [43, 44]. As Sections 4.2 and 6.4 show, the anchor choice determines both the architecture's resilience tier under Operator Synthesis and its centralization profile.

### 2.4 The Economics-of-Security Lens

Anderson and Moore [45] established information security as fundamentally an economic problem, a line subsequently extended to cybersecurity policy [46] and to the macro-level measurement of cybercrime costs [47]. Herley and Florêncio [48] argued that underground markets for stolen credentials are lemon markets: because buyers cannot verify quality, "nobody sells gold for the price of silver," and advertised prices overstate attacker returns — a caution we apply to the market prices used in Section 5. Applied to client-side anti-automation, these frameworks yield the critical insight that client-side defenses operate under a *forgery model* rather than a *cryptanalysis model*: the attacker's cost is determined by market prices (proxy IPs, human labor, GPU compute, malware infections), not by a cryptographic security parameter.

This distinction is the through-line of the following sections. Account-abuse markets make the same point empirically: Thomas et al. measured merchants selling fraudulent Twitter accounts in bulk, with CAPTCHA and verification costs priced into the product [49].

### 2.5 Related Work

*Bot detection in the wild.* Li et al. deployed honeysites to characterise automated browsing and characterised their fingerprints and behaviour at scale [50]. Azad et al. evaluated commercial anti-bot services and showed they block simple bots but miss those that adapt their fingerprints [51]. Jonker et al. characterised the fingerprint surface of web-bot frameworks and measured bot-detection deployment across the top million sites [52]; Vastel et al. showed that fingerprint-based crawler blocking can be evaded by altering a few attributes [53]. Bursztein et al.'s Picasso describes a Google protocol that uses canvas rendering to attest device class [3]. These works target Environmental Forgery; none considers an attacker that leaves the browser untouched.

*CAPTCHA breaking.* Beyond text CAPTCHAs [15, 18], Sivakorn et al. broke reCAPTCHA's image challenges and exploited its checkbox risk analysis [19]; Searles et al. measured human and bot performance on modern CAPTCHAs at scale [20]; and agentic VLMs now solve generalised visual CAPTCHAs [29, 30].

*Computer-use agents.* Benchmarks such as WebArena [54], VisualWebArena [55], Mind2Web [14], and OSWorld [56] track the rapid improvement of agents that act on real web and desktop environments. A parallel line attacks the agents themselves, via adversarial pop-ups [57] or injected page content [58]; such attacks are potential defender tools against Operator Synthesis.

*Authenticating good bots.* The IETF Web Bot Auth working group is standardising cryptographic authentication of automated clients, building on HTTP Message Signatures [59, 60]. This inverts the problem: rather than detecting bad bots, well-behaved agents opt in to identification.

*Comparative evaluation.* Our tiered evaluation is in the spirit of the benefit-matrix comparison in Bonneau et al.'s framework for password-replacement schemes [61].

| Work | Coverage | Threat model | Evaluation | Claims challenged |
|------|----------|--------------|------------|-------------------|
| Laperdrix et al. [4] | Browser fingerprinting: attributes, uses, defences | Tracker/fingerprinter versus user privacy; bot detection is one application | Literature survey | None directly; we treat fingerprint-based detection as one layer (L1a) that Operator Synthesis sidesteps |
| Guerar et al. [16] | 20 years of CAPTCHA designs and attacks | ML solvers and human farms against CAPTCHA challenges | Literature survey and taxonomy | That CAPTCHA hardness sets the bar: we argue the challenge is no longer the binding cost |
| Rokicki et al. [62] | JavaScript timers and timing attacks in browsers | Microarchitectural and side-channel attacks from web content | SoK with experimental timer analysis | None; we build on it for L4 chronometric checks |
| Searles et al. [20] | Modern CAPTCHAs in live deployment | Human users and automated solvers | User study (1,400 participants, 14,000 CAPTCHAs solved) and bot comparison | We extend its bot-versus-human finding from solvers to full-browser VLM agents |
| Bonneau et al. [61] | Password-replacement schemes | Authentication attacks | Benefit matrix: 35 schemes rated on 25 usability, deployability and security benefits | Not challenged; we reuse its comparative-matrix method |
| This SoK | Client-side anti-automation Types I–V, 2010–2026 | APB with Operator Synthesis (Axis C) as the primary lens | Mechanism matrix, tier assignment, structured cost accounting | That client-side detection raises attacker cost regardless of input modality |

Table: Comparison with the closest surveys and SoKs cited in this paper.

---

## 3. PART I: The Historical Landscape — Probabilistic Client-Side Attestation (2010–2024)

*This section is a retrospective post-mortem. The architectures described here were the state of the art for the 2017–2024 period. Under the Operator Synthesis paradigm introduced by VLMs, they face structural degradation for the APB threat model. We systematize them not as standalone active defenses against top-tier adversaries but as diagnostic artifacts that reveal *why* probabilistic client-side attestation has a finite economic ceiling against Operator Synthesis.*

### 3.1 Methodology: Systematic Literature Search

This SoK rests on a structured, but not fully systematic, literature search. We report it so that a reader can judge its coverage; we do not claim PRISMA-level replicability. All searching, screening and coding was done by a single author, with no second screener and no inter-rater agreement measure. Classification decisions in §3.2–§3.4 are therefore one analyst's judgement and should be read as such.

**Sources searched.** IEEE Xplore, ACM Digital Library, arXiv (cs.CR, cs.CL, cs.CV), Google Scholar, IETF Datatracker, W3C Technical Reports. The original search pass (August 2026) kept no log. We therefore re-ran the main query on 23 September 2026 against the two sources with a scriptable API: arXiv (title/abstract fields, 74 hits) and Semantic Scholar (bulk search, 443 hits). DBLP was also attempted but was unreachable to scripted clients (its bot challenge blocked the request). The two result sets give 517 records and 444 unique titles after title-level de-duplication. All of them are logged in `docs/corpus.csv` together with the script that produced them (`analysis/literature_search.py`). Only 7 of these 444 records match a work already in our reference list ([17, 19, 29, 30, 63, 64, 76]). The other 437 are logged as *not screened*: we record them and do not claim a screening decision for them. So the rerun shows that most of the coded corpus came from the supplementary queries and from snowballing, not from the main query. Screening the rerun set is still open work.

**Query.** `("bot mitigation" OR "bot detection" OR "anti-automation" OR "browser fingerprinting" OR CAPTCHA) AND (attestation OR cost OR economics OR architecture OR "CAPTCHA solving" OR "vision-language model" OR VLM OR "web agent" OR "computer-use agent" OR "GUI agent")`. Supplementary targeted queries covered Private Access Tokens, Privacy Pass, DBSC, behavioural biometrics, VM/code deobfuscation, and residential-proxy and pay-per-install economics. Backward and forward snowballing from the included items added foundational and recent work.

**Inclusion criteria.** An item enters the *coded corpus* (the set classified into Types I–V and the L1–L4 model) if it (a) describes a client-side mechanism that imposes cost on automated clients, and (b) documents that mechanism at a level sufficient to classify it, in peer-reviewed work, an IETF/W3C document, or grey literature whose architectural claims are corroborated by a second independent source. Production deployment is normally required. **Explicit exception:** standards-track proposals without deployment (PACT [11, 43]) are included because they define the direction of Type IV; they are marked as proposals wherever they appear.

**Exclusion criteria.** (1) Theoretical proposals with neither deployment nor prototype evaluation, other than the exception above. (2) Server-side-only defences (WAFs, TLS fingerprinting without browser-level interrogation). (3) Marketing material without mechanism-level detail.

**Coded corpus versus background references.** The reference list mixes two roles. The coded corpus consists of the systems and papers classified in the §3.2 mechanism matrix and §3.2–§3.5. The remaining references are background: economics-of-security framing, historical works (e.g. Saltzer and Schroeder), protocol RFCs cited for definitions, and agent/VLM papers used to characterise the attacker in Part II. The only per-stage counts we report are those of the logged rerun above (identified: 517; unique: 444; matched to cited work: 6; not screened: 438). We did not log per-stage counts for the original pass or for the snowballing, so we do not report PRISMA-style numbers for the full corpus.

**Post-hoc additions.** After the main screening, items were added outside the query process: agentic web-navigation frameworks, SDK-based residential-proxy research, the PACT proposal, and 2025–2026 measurements of VLM-based CAPTCHA solving. These were found by snowballing and by following recent announcements, not by a rerun of the query. This adds recency but also selection bias toward work the author already knew about.

**Grey literature.** Vendor whitepapers and threat-intelligence reports were used only when an architectural claim was corroborated by an academic paper, a standards document, or a second independent grey-literature source. Where a claim rests on a single vendor source, the text says so.

### 3.2 Five Architectural Types by Mechanism

We identify five architecturally distinct classes of client-side anti-automation. These types are distinguished by their *primary mechanism*: Execution (probing the runtime through code execution), Telemetry (passive accumulation of behavioral/sensor data), or Cryptographic Binding (hardware-anchored deterministic proof). Real production systems inevitably fuse mechanisms from multiple types (Section 3.3). The following vendor-mechanism matrix maps representative systems to their constituent mechanisms:

| System | Execution | Telemetry | Cryptographic Binding | Primary Mechanism |
|--------|-----------|-----------|----------------------|-------------------|
| Google Botguard | ✓ [3] | ✓ —† | | Execution (collects L1b sensor telemetry) |
| Turnstile | ✓ [22] | ✓ [22] | | Execution |
| reCAPTCHA v3 | ✓ —† | ✓ —† | | Telemetry (with Execution auxiliary) |
| DataDome | | ✓ [65] | | Telemetry |
| Arkose Labs | ✓ —† | ✓ —† | | Telemetry |
| Apple PATs | | | ✓ [1] | Cryptographic Binding |
| Privacy Pass | | | ✓ [5, 40] | Cryptographic Binding (redemption only; the 2018 deployment used a solved CAPTCHA as the issuance attester [40]) |
| DBSC | | | ✓ [27, 28] | Cryptographic Binding |
| Passkeys/WebAuthn | | | ✓ [39] | Cryptographic Binding |

Table: Production-system mechanism matrix — execution, telemetry, cryptographic binding, and primary mechanism per system. Each ✓ carries the source that documents it; "—†" marks a cell with no public mechanism-level source (authors' assessment). An empty cell means the mechanism is not documented in the cited sources; it does not prove the mechanism is absent (authors' assessment).

**Type I: Point-in-Time VM Attestation.** Executes a custom register-based JavaScript VM within the browser. Measures environmental integrity (L1), uses self-modifying opcodes (L2), anti-introspection traps (L3), and chronometric constraints (L4). Produces a short-lived opaque bearer token that the protected server verifies with the vendor. Cost imposed: per-execution proxy bandwidth, fixed RE investment, recurring temporal cost per compile rotation. Structural ceiling under Environmental Forgery: IP reputation market exhaustion. Under Operator Synthesis: L1 and L4 detection premises shift rather than collapse — L1a shifts to container-evasion artifacts, L1b shifts to kinematic-orchestration quality, L4 shifts from microsecond instrumentation detection to second-scale latency profiling (Section 5.2). L2/L3 become black-boxed at the VM level. IP reputation remains the primary binding economic constraint, but residual detection surfaces — containerization artifacts and orchestration-layer kinematics — continue to impose non-trivial costs, albeit at a reduced level compared with Environmental Forgery. Representative systems: Google Botguard, Cloudflare Turnstile Managed Challenge, Kasada [66].

**Type II: Stateful Behavioral Telemetry.** Accumulates long-term behavioral profiles using persistent identifiers (cookies, fingerprinting). Scores mouse movements, scroll patterns, navigation cadence, and dwell time over weeks to months. Cost imposed: conjunctive stack of proxy + aged profile + anti-detect software license [67, 68]. Structural ceiling under Environmental Forgery: profile-aging latency, which is paid in time rather than money. Under Operator Synthesis the aging requirement does not go away: a VLM driving a fresh browser has no history, so the attacker still needs aged profiles or real, long-used devices, bought or grown. What Operator Synthesis removes is the need to forge behaviour *within* an aged profile, not the need for the profile. Representative systems: reCAPTCHA v3, DataDome, Human Security (PerimeterX).

**Type III: Behavioral Biometrics & Sensor Telemetry.** Measures mouse kinematics (velocity, acceleration, Bezier-curve fitting), scroll patterns, click-timing, touch pressure, accelerometer polling [23, 69–73]; the same sensor channels are used for mobile behavioural authentication [25], a related but distinct problem. Cost imposed under Environmental Forgery: `min(Cost_ML_Inference, Cost_Human_Labor)`, where human labor (CAPTCHA-solving farms at ∼$1/1K challenges [17]) sets the global cost floor. Under Operator Synthesis: the VLM's emergent cognitive selection of visual targets bypasses the behavioral model's prediction of interaction targets. However, as Section 1.4 details, VLMs output coordinate selections, not kinematic trajectories — a separate orchestration layer must translate coordinates into mouse movement. If that orchestration uses naive linear interpolation or constant-velocity profiles, the resulting kinematics remain statistically distinguishable from human movement, and behavioral biometrics (L1b) retain detection leverage (Tier 2 in Section 4.2).

**Type IV: Platform/OS-Level Anonymous Attestation (Privacy Pass / PATs / PACT).** Cryptographic anonymous tokens (RSA blind signatures, VOPRF) issued by a platform or third-party issuer. The anchor may be hardware-backed — device attestation via Secure Enclave/TPM, token issuance rate-limited per-device [10] — or software/contextual, as in the 2026 PACT proposal, where the anchor is issuer judgment of account standing, subscription status, or first-party relationship [11, 43]. Cost imposed (hardware anchor): device compromise through PPI malware [74, 75]; extraction of attestation keys is prohibitively expensive, but proxying through compromised devices is economically viable. Cost imposed (contextual anchor): account acquisition and synthesis (bulk registration, credential stuffing, aged-account purchases, cheap subscriptions), relocating the Sybil problem from device scarcity to credential scarcity (Sections 4.2–4.3). The hardware-anchored variant is Tier 1 not because it resists VLMs — it is indifferent to input modality, and a VLM driving a real attested device passes — but because the attacker's cost moves to acquiring real enrolled devices, with throughput bounded by attester rate limits; the contextual variant moves cost to accounts instead. Representative systems: Apple PATs, Cloudflare/Fastly Privacy Pass issuance, PACT (proposed).

**Type V: Hardware-Anchored Determinism (DBSC, FIDO2/Passkeys).** Cryptographic proof of hardware key possession. DBSC binds a session cookie to a non-exportable device key so that stolen cookies cannot be replayed elsewhere [27, 28]; it is an anti-cookie-theft mechanism, not an anti-automation one. Cost imposed: access to real enrolled devices or accounts — including device/phone farms or PPI-compromised hosts at $30–$200/month per botnet subscription [75]. Structurally inapplicable to anonymous traffic [12]. Tier 1 in the same limited sense as Type IV: a VLM operating a real device passes; the constraint is device and account supply. Representative systems: Google DBSC, W3C WebAuthn, Passkeys (Apple, Google, Microsoft).

### 3.3 The Hybrid Reality: Production Systems Fuse Mechanisms

A taxonomy that cannot cleanly classify the three most prominent production systems — Cloudflare Turnstile, DataDome, and Arkose Labs — without immediately resorting to "hybrid" exceptions has limited diagnostic value unless the hybrid nature is acknowledged from the outset.

Cloudflare Turnstile uses a JavaScript VM challenge as the *delivery mechanism* for stateful telemetry collection. The VM does not merely measure the environment; it establishes a persistent session that feeds a behavioral scoring engine. Turnstile is simultaneously Type I (point-in-time VM attestation) and Type II (stateful behavioral telemetry), with the VM serving as the instrumentation layer for the telemetry [22].

DataDome similarly fuses Type II (stateful profile accumulation) with Type III (mouse kinematics and behavioral biometrics), using one to bootstrap the other when profile data is insufficient [65].

Arkose Labs deploys visual-interactive challenges (Type I auxiliary) as a fallback escalation when its probabilistic scoring (Type II/III fusion) is inconclusive.

These are not edge cases or implementation flaws. They are evidence that the industry converged on hybrid architectures because each pure architectural type has a well-understood structural weakness that a complementary type can partially mitigate. The taxonomy's value is not in achieving clean classification of every system, but in providing the *analytical vocabulary* to identify which mechanisms a hybrid system combines and which attack vectors remain exposed.

In this SoK, we classify each system by the mechanism that most closely describes its *binding structural ceiling*: the constraint that limits the adversary's throughput regardless of hybridization. For Turnstile, the binding constraint remains IP reputation (Execution mechanism), even though behavioral telemetry (Telemetry mechanism) provides supplementary signal.

### 3.4 The L1–L4 Diagnostic Framework

L1–L4 is this paper's analytical model, synthesised from public sources (Path B): Google publishes no specification of Botguard, and we did not reverse-engineer it ourselves. Our sources are Google's Picasso protocol, whose server-seeded canvas challenges resist replay [3]; the Sivakorn et al. black-box study of reCAPTCHA's checkbox risk analysis [76]; grey-literature reverse-engineering write-ups of the Botguard VM [77–80]; and the fingerprinting, timer and obfuscation literature [4, 8, 62, 81]. The grey-literature sources are single-author, unreviewed and tied to particular script versions and deployments (reCAPTCHA, the Search interstitial, YouTube), and they partly disagree; the evidence table below grades each claim accordingly. L1–L4 is a *diagnostic model* for point-in-time VM attestation, not a description of one vendor's current implementation. Its purpose is to show how each layer's cost burden shifts under Operator Synthesis.

Under Environmental Forgery, each layer imposes cost because the attacker must instrument or subvert the browser to forge sensor data. Under Operator Synthesis, the adversary drives an unmodified browser, so the *instrumentation-detection* premise of each layer collapses. We hypothesize that the cost does not vanish but *shifts* to new surfaces — the orchestration layer between VLM output and OS input, the deployment stack, and inference latency:

- **L1a (Static Environmental Introspection)** — Consistency checks on the declared environment. Documented: reCAPTCHA renders a fixed canvas composition and compares the result against the declared User-Agent, falling back to a harder challenge on UA or engine mismatch [76]; Picasso generalises this into server-seeded device-class challenges [3]. The Search-interstitial VM, by contrast, contains no plaintext fingerprint property names [78], so coverage varies by deployment. Under OpSyn, properties come from a legitimate browser. We hypothesize that industrial-scale deployment in containers leaks anomalies (missing fonts, WebGL output inconsistent with the declared OS), moving cost to container-evasion engineering (Section 4.1).
- **L1b (Dynamic Sensor Telemetry)** — Input-event and kinematic signals. That the VM reads real input events is documented [78]; that it scores mouse kinematics against human models is claimed [79] but contradicted by Sivakorn et al., who found that mouse timing and movement patterns did not affect the risk score [76]. We therefore treat kinematic scoring as inferred from the general literature [23, 72], not documented for Botguard. We hypothesize that because VLMs emit coordinates, not trajectories, naive orchestration-layer interpolation leaves detectable artifacts (Section 1.4).
- **L2 (Code Obfuscation, Polymorphism)** — Documented: a custom bytecode VM with encrypted registers, self-modifying opcodes loaded at runtime [77], a per-load keystream-encrypted bytecode [78], and a script URL and token-cipher constant that change with each rotation [79]. Under OpSyn the VLM never inspects bytecode; BgUtils likewise runs the VM as a black box in a real runtime [80]. T_RE ≈ 0 at the VM level; application-level workflow RE remains (Section 5.5).
- **L3 (Execution Traps)** — Documented: an "anti-logger" that patches getters so `console.log` or logpoints perturb VM state [77], and a `Function.prototype.toString` anti-hook probe [78]. Under OpSyn no DevTools are opened and no runtime is hooked, so the traps never fire. We hypothesize that L3's premise can move to the perceptual layer: a *cognitive honeypot* — a decoy with non-zero `getBoundingClientRect()` size, rendered near-invisible (`opacity: 0.01`) inside a `pointer-events: none` overlay — that DOM-grounded agents such as SeeAct in element-choice mode [82] may select by element reference, mirroring known pop-up and hidden-element attacks on agents [57, 58]. This is untested and narrow: screenshot-only agents (CogAgent [83], OpenAI's CUA, Anthropic's Computer Use) never see the decoy; `aria-hidden` and tab-order removal, required so assistive-technology users are not flagged, also hide it from accessibility-tree agents; and cross-checking DOM targets against screenshot crops defeats it.
- **L4 (Chronometric Integrity)** — Documented: the VM compares `performance.now()` and `Date.now()` to detect breakpoints and folds the result into the seed that selects the next bytecode byte, silently diverting execution when debugging is detected [77]; `performance.now` also appears in the interstitial's signal set [78]. Timer semantics follow [62]. Under OpSyn native execution introduces no microsecond deviation. We hypothesize that L4 extends to the second scale (Section 5.2): at an assumed 5–15 s of inference per action (Table 5.1), a multi-step agent flow accumulates latency a human does not. Baselines must be like for like — single-CAPTCHA human times (2–5 s) do not transfer — and we claim no fixed ratio; the candidate signal is per-action latency against human baselines for the same flow.

**Evidence per layer.** *Documented* = directly observed in a cited source for a Google product; *inferred* = supported by general literature or contested sources, not observed for Botguard; *hypothesized* = our proposal, unvalidated. Grey literature (GL) is unreviewed and version-specific.

| Layer | Claimed mechanism | Public source(s) | Claim strength |
|-------|-------------------|------------------|----------------|
| L1a | Canvas render vs. declared UA consistency | Sivakorn et al. BH Asia 2016 [76]; Picasso [3] | Documented (reCAPTCHA, 2016) |
| L1a | Broad `navigator`/WebGL fingerprinting in the VM | [4] (general); contradicted for Search interstitial by GL [78] | Inferred; deployment-dependent |
| L1a | Container anomalies under OpSyn | — | Hypothesized |
| L1b | Real input-event collection | GL [78] | Documented (GL) |
| L1b | Mouse-kinematic scoring | GL claim [79]; null result [76]; [23, 72] (general) | Inferred; contested |
| L1b | Interpolation artifacts in VLM orchestration | — | Hypothesized |
| L2 | Custom bytecode VM, encrypted registers, self-modifying opcodes | GL [77, 78] | Documented (GL) |
| L2 | Script/cipher rotation | GL [79] | Documented (GL, one version) |
| L2 | VM executable as black box | GL [80] | Documented (GL) |
| L3 | Anti-logger, `toString` anti-hook probe | GL [77, 78] | Documented (GL) |
| L3 | Cognitive honeypot vs. DOM-grounded agents | [57, 58, 82] (agent attacks) | Hypothesized |
| L4 | Timing-based anti-debug feeding the VM seed | GL [77] | Documented (GL) |
| L4 | Second-scale inference-latency signal | Section 5.2 | Hypothesized |

Table: Evidence grading for the L1–L4 model. GL = grey literature.

**Diagnostic Summary.**

| Layer | Cost Type (EF) | Cost Under OpSyn | Nature of Shift |
|-------|----------------|---------------|-----------------|
| L1a | Variable (compute for forgery) | Shifted to container-evasion engineering | Not zero; moved from browser forgery to deployment-environment mimicry |
| L1b | Variable (ML inference or labor) | Shifted to kinematic-smoothing orchestration | Not zero; moved from trajectory generation to orchestration-layer quality assurance |
| L2 | Temporal (RE per compile rotation) | Near-zero at VM level; shifted to app-level workflow RE | VM bytecode black-boxed; DOM-level prompt engineering remains |
| L3 | Mixed (trap identification + overhead) | Shifted to perceptual-DOM alignment | Not zero; moved from DevTools-trap evasion to perceptual-DOM alignment engineering (Section 4.2) |
| L4 | Variable (timer synchronization) | Shifted to latency-evasion at inference timescale | Microsecond instrumentation gap closed; second-scale inference gap opened |

Table: Cost-type shift per L1–L4 layer under Operator Synthesis. EF = Environmental Forgery; OpSyn = Operator Synthesis.

The diagnostic value of the L1–L4 framework under Operator Synthesis is not that the stack collapses to zero cost — it is that the *nature* of the cost imposed on the attacker shifts from browser-instrumentation forgery to systems-integration engineering. Defenses rooted in L1a, L1b, and L4 do not vanish; they transform into detection surfaces at the orchestration and deployment layers, which remain exploitable by a sophisticated defender.

### 3.5 The Temporal Arms Race: A Historical Case Study

Point-in-time VMs rely on a temporal race: the defender rotates the compiled VM on a lifetime `T_Life` (for Botguard, grey-literature analyses report per-rotation changes to the script URL and token-cipher constant, and a hand-built token generator valid only for one bytecode sample [77, 79]), and the attacker must reverse-engineer each build within `T_RE`. We have no public data on the actual rotation interval. The general tension between obfuscation and automated analysis is surveyed in [8]. Later automated tools lowered `T_RE` for virtualisation-style obfuscation: semantics-based deobfuscation of virtualised code [84], symbolic execution for JavaScript [85], and program synthesis of obfuscated handler semantics (Syntia [86]); hardening such as Loki [81] responded. Learned models of code point in the same direction — property prediction over obfuscated JavaScript [87] and deobfuscation as a code-model pre-training objective (DOBF [88]) — though neither was built as a VM-attestation attack tool. We treat the claim that `T_RE` was approaching `T_Life` for well-defended VMs as our inference from this trend, not a measured result. Under Operator Synthesis the race ends at the VM level: the attacker never inspects the defensive bytecode and runs the VM as a black box, as open-source PoToken tooling already does for YouTube's Botguard [80]. The lesson is that software-only obfuscation cannot impose cost on an adversary who skips the inspection step. Application-level workflow RE (Section 5.5) keeps a separate, cheaper temporal constraint at the DOM layer.

---

## 4. PART II: The VLM/Operator Synthesis Attack Vector

*Part II (Sections 4–6) analyzes the Operator Synthesis attack vector for the APB threat model and establishes a forward-looking research agenda for VLM-resilient anti-automation. Consistent with the scope limitation in Section 1.2, claims of "degradation" or "bypass" refer to structural vulnerability against this top-tier adversary class, not universal invalidation of probabilistic defenses. The middle tier of sophisticated non-VLM automation (Puppeteer/Playwright farms) independently imposes pressure on probabilistic defenses without VLM inference; our analysis treats VLM adoption as the capability that most intensifies this pressure.*

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

Table: Idealized Operator Synthesis assumptions versus industrial-scale constraints.

**The containerization gap.** The cheapest way to run VLM operators at scale is in containerized or virtualized environments (Docker, Kubernetes, cloud VMs). A stock Chrome browser inside a Linux container, routed through a residential proxy, still leaks client-observable anomalies relative to a genuine user device: system fonts inconsistent with the User-Agent's declared OS, WebGL rendering artifacts inconsistent with the expected GPU driver stack [89], and characteristic AudioContext output. L1a environmental introspection therefore retains leverage against containerized deployments. (Network-layer anomalies such as TCP/IP stack fingerprints — MTU, TTL, initial window size — also leak, but network fingerprinting is outside this paper's client-side scope; we treat it only as a server-side complement.) The gap is not universal: an attacker who instead drives real consumer devices — device farms of physical phones or desktops, or rented real-device clouds — presents genuine fonts, GPUs and sensors, and closes it at the price of hardware acquisition and lower density per operator. The containerization gap is thus a cost lever, not a detection guarantee.

The attacker's browser is not a compromised browser; it is a browser used exactly as designed, by a synthetic operator. OS-level input synthesis itself is not new — tools such as xdotool and PyAutoGUI predate VLMs. What the VLM adds is perception (reading arbitrary rendered pages and challenges) and cross-site generalisation without per-site scripting. The middle tier of non-VLM automation (Section 1.2) already pressures probabilistic defenses through anti-detect browsers; Operator Synthesis removes the browser-instrumentation forgery cost that those adversaries pay. It does not remove the IP-reputation cost, which we treat throughout as the dominant *remaining* constraint once forgery cost is gone (Section 5.3).

**The hybrid attacker.** A VLM on every step is not the cost-minimising configuration. A rational operator scripts the deterministic parts of a flow (navigation, form filling, known selectors) and invokes the VLM only for perception — an unfamiliar challenge, a changed layout, a visual puzzle — with all input still injected at the OS level into an unmodified browser. This hybrid keeps the Axis C properties of Operator Synthesis while cutting inference calls, and therefore cost and latency, by the fraction of steps that are scriptable. Cost figures in Section 5 that assume per-action VLM inference should be read as upper bounds for this attacker.

### 4.2 Architecture-by-Architecture Effects of Operator Synthesis

We place each architectural type in one of three tiers, ordered by how much of the defense's pre-VLM cost survives Operator Synthesis: Tier 1 > Tier 2 > Tier 3. Tier 1: the mechanism does not depend on input modality at all, so its cost is unchanged and moves entirely to acquiring real enrolled devices or accounts. Tier 2: the detection premise is weakened but a residual client-observable surface survives. Tier 3: the defense's original constraint no longer applies to the attacker as such and is replaced by a substitute cost the attacker can buy.

**Type I (Point-in-Time VM Attestation) → Tier 2.** The browser-instrumentation forgery costs that L1–L4 impose under Environmental Forgery largely cease. IP reputation remains the dominant economic constraint; residual detection surfaces — containerization artifacts (Section 4.1) and orchestration-layer kinematics (Section 1.4) — continue to impose non-trivial costs on attackers, albeit at a reduced level compared with Environmental Forgery. Without the multiplicative cost of environmental forgery, the effective per-token cost plausibly drops, though the net saving remains an open empirical question (Section 5.3). The VM becomes a delivery mechanism rather than a defense — it delivers the challenge, but the challenge imposes no environmental forgery cost beyond the residual surfaces above.

**Type II (Stateful Behavioral Telemetry) → Tier 3 (aging cost bought rather than waited out; state-orchestration cost added).** Profile aging is a function of time and history; a VLM does not create it, and a fresh browser driven by a VLM is still a fresh profile. Operator Synthesis therefore does not remove the aging requirement. What changes is how the attacker meets it: a VLM can operate purchased aged profiles, aged accounts, or real long-lived devices without the browser instrumentation that previously betrayed them, so the aging constraint becomes a market price rather than a latency the attacker must wait out. VLMs are also stateless between inference calls unless explicitly orchestrated. Maintaining, isolating, and rotating aged cookie jars, local storage snapshots, and IndexedDB state across thousands of parallel VLM instances without cross-contamination is a non-trivial orchestration problem. Each parallel session requires an isolated browser profile, a persistent cookie store, and clean session state — and the cost of managing this infrastructure at scale substitutes for the anti-detect browser license that Environmental Forgery required. Type II thus shifts from a latency-bound problem to a procurement- and operations-bound problem: aged state is bought, and keeping it isolated is an infrastructure cost. Defense-imposed cost persists, but in purchasable form.

**Type III (Behavioral Biometrics & Sensor Telemetry) → Tier 2 (Cognitive selection bypassed; kinematic instantiation gap remains).** The VLM's cognitive ability to locate visual targets and output coordinate selections is emergent from vision-language training on human demonstrations. However, as discussed in Section 1.4, the VLM does not natively produce the kinematic trajectory between those coordinates — an orchestration layer translates the VLM's coordinate output into mouse movement. If the orchestration layer uses naive linear interpolation, constant-velocity profiles, or generic ease-in/ease-out curves, the resulting mouse kinematics remain statistically distinguishable from the smooth, biologically-motivated acceleration profiles of human movement. Behavioral biometrics (L1b) retain detection leverage against poorly-implemented orchestration. Sophisticated attackers will invest in a kinematic-smoothing layer (adaptive Bezier trajectory generation with human-derived acceleration profiles) to close this gap, which adds engineering cost. The detection premise shifts from "the VLM cannot produce human-like interactions" to "the VLM can produce human-like interactions only if the orchestration layer correctly implements human motor kinematics" — a narrower residual surface, not zero.

**Type IV (Anonymous Attestation / PATs) → Tier 1 — for the hardware-anchored variant.** The attestation binds to an enrolled device and account, not to input modality. This cuts both ways: whether the device is driven by a human or a VLM is irrelevant to the protocol, so a VLM operating a real attested device (for example, an iPhone or Mac in a device farm, driven through screen capture and OS-level input) obtains valid tokens. Tier 1 is therefore not VLM resilience. It means the attacker's cost moves to acquiring real enrolled devices and accounts, and throughput per device is bounded by the attester's issuance rate limits [10]. Extracting keys from a device is a separate, costlier chain (PPI malware, physical access) [75]. This classification does not extend to software-anchored variants of the category. The 2026 PACT proposal [11] binds attestation to issuer judgment of account standing rather than to device hardware: the unit of scarcity becomes the credentialed account, and account acquisition — bulk registration, credential stuffing, aged-account purchases, subsidized subscriptions — is automatable at costs the APB threat model can absorb (Section 4.3). PACT's design also assigns the browser the role of trusted user-agent mediating credential storage, issuer selection, and challenge budgets [43] — an assumption that fails precisely under Operator Synthesis, where the browser profile, the device, or both are under attacker control, and where a copied or compromised profile can exercise the same issuance APIs as a legitimate user [43, 90].

**Type V (Hardware-Anchored Determinism / DBSC, passkeys) → Tier 1.** Same logic as Type IV: proof of possession of a hardware-bound key is independent of input modality, so a VLM driving the browser on the enrolled device passes. Note that DBSC is an anti-cookie-theft mechanism — it stops a stolen session cookie from being replayed on another machine — not an anti-automation mechanism; it imposes no cost on automation running on the device that holds the key. Passkeys likewise authenticate an account holder, not a human operator.

**Tier ordering (Operator Synthesis only).**

The tiers measure how much defense-imposed cost survives Operator Synthesis specifically, i.e. whether the mechanism depends on input modality. They do not measure total defense strength: Types IV and V face separate attack chains (device and account acquisition, device compromise) analyzed in Section 4.3. Each type occupies exactly one tier.

| Tier | Definition | Types | Mechanism |
|------|------------|-------|-----------------------|
| 1 | Input-modality-independent; cost moves to real enrolled devices/accounts | Type IV (PATs, hardware-anchored) [1, 10], Type V (DBSC/Passkeys) [27, 39] | A VLM driving a real enrolled device passes (binding is to the key, not the input modality [1, 27, 39]). Attacker cost = device/account acquisition (device farms) —†; throughput bounded by attester rate limits [10]. Key extraction is a separate chain (Section 4.3) [74, 75]. |
| 2 | Degraded — cost-shifted but not eliminated | Type I (VM Attestation), Type III (Behavioral Biometrics) | Detection premise substantially weakened at the cognitive level [29, 30, 64]; residual costs from container-evasion artifacts (Type I) —† or kinematic-orchestration quality (Type III) [24, 69, 70] remain |
| 3 | Substituted — original constraint met by a purchasable substitute | Type II (Stateful Telemetry) | Aging still required but bought (aged profiles, accounts, real devices) rather than waited out [49, 68]; state-orchestration infrastructure cost —† replaces the anti-detect browser license [67, 68] |

Table: Architecture-by-architecture tier assignment under Operator Synthesis (tier semantics defined in the text). Bracketed numbers give the source for each cell claim. "—†" marks a claim with no direct public source (authors' assessment). The tier placements themselves are the authors' synthesis of these sources.

The Tier 1 classification of Type IV applies to the hardware-anchored variant (Apple PATs). Software-anchored Type IV variants such as PACT [11] do not qualify: their binding is issuer judgment rather than cryptographic hardware possession, and their Sybil economics degrade to account acquisition (Section 4.2, Type IV; Section 4.3).

![Where the attacker's marginal cost lands, by defense type (rows) and attacker class (columns). The figure summarises §3.2 and §4.2 and is the authors' assessment, not a measurement. Against Operator Synthesis and hybrid attackers, Type I cost falls to IP reputation, Type II cost stays in aged state, and Type III cost moves to kinematic orchestration. Types IV and V push every attacker class to device or account acquisition. "Scripted OS input" is pre-VLM OS-level automation (xdotool, PyAutoGUI; §4.1) of a genuine browser, so it pays the same IP, aged-state and kinematic costs as Operator Synthesis. "Device farm" drives real enrolled devices (§4.3, §5.6); its IP reputation and aged state come bundled with the device, so its cost lands on device acquisition except under Type III, where the farm's input still has to pass kinematic scoring. Generated by `analysis/figure_cost_shift.py`.](figures/cost_shift.pdf){width=100%}

### 4.3 What Survives: Tier 1 Architectures and Their Structural Limits

Tier 1 architectures keep their cost under Operator Synthesis because they anchor on possession of a real enrolled device or account rather than on probabilistic detection of behavioral signals. That cost is a market price, and each Tier 1 architecture has a structural limit:

**PATs (Type IV): The real-device ceiling.** The cheapest bypass requires no compromise at all: the attacker acquires real enrolled devices and accounts and drives them, by VLM or script, in a device farm. Cost per token is then device and account acquisition amortised over the tokens each device can obtain, which the attester's per-device rate limits [10] cap. A related real-device relay variant forwards challenges to a pool of genuine devices (owned, rented, or operated by paid humans) that obtain tokens on the attacker's behalf. The costlier alternative is device compromise. Pay-per-install (PPI) services sold installs at $7–$180 per 1,000, i.e. $0.007–$0.18 per infected host (2011 Windows prices, cheapest in Asia, dearest in the US/UK) [74]; comparable public prices for installs on PAT-capable Apple devices do not exist (Section 5.6). The economic ceiling is the black-market price of a successful infection — not the cryptographic hardness of the VOPRF protocol, but the market equilibrium of the malware supply chain. Per-device rate limits [10] cap throughput here too.

SDK-based residential proxy networks (Bright Data, the former Hola network, various mobile-proxy SDKs) are *not* a PAT bypass, though they are often conflated with one. Such SDKs relay network traffic through consenting users' devices [91]; they supply residential IP reputation, not attestation. A proxy SDK cannot mint PATs or DBSC proofs for a browser session originating elsewhere: PATs are issued to the device's own system networking stack for requests that device makes, Android Keystore keys are bound to the app that created them and unusable by other apps, DBSC keys are held by the browser and non-exportable, and Android has no PAT mechanism at all. Obtaining attestations through an SDK would require the host app's own code to request them and ship the results out — an application-level compromise, i.e. the device-compromise chain above, not a property of proxying. Residential proxies therefore bear on the IP-reputation constraint (Section 5.3), not on the Tier 1 ceiling.

Attestations from farmed or relayed real devices are cryptographically valid and indistinguishable from legitimate traffic at the attestation layer. The defender's recourse is server-side behavioral metadata: ASN reputation, IP-to-account cardinality, velocity limits, and cross-session pattern matching. These signals, often demoted as legacy in the hardware-attestation literature, remain the necessary complement to cryptographically valid but attacker-controlled attestations.

**The software-anchor ceiling: token farming.** PACT-style contextual anchors replace the device-compromise ceiling with an account-acquisition ceiling (Sections 4.2, 6.4). If the issuer's admission signal is an active subscription, account standing, or a first-party relationship, the attacker's unit of scarcity becomes a credentialed account: bulk registration, credential stuffing, stolen session tokens, and cheap subscriptions are all automatable inputs to a token-farming pipeline upstream of the attestation protocol [90]. The cryptographic layer does not prevent polluted tokens from entering circulation — it only prevents certain kinds of linkability [5] — so verifier-side rate limiting of redemption remains necessary regardless of anchor type [90]. The defender's position parallels the real-device analysis above: attestations issued against farmed accounts are cryptographically indistinguishable from legitimate attestations at the protocol layer, and the recourse is again network-layer behavioral metadata. The anchor choice therefore determines which black-market price constitutes the ceiling — device infection or account acquisition — and both are market prices, not security parameters.

**DBSC/Passkeys (Type V): The post-authentication session ceiling.** DBSC prevents a stolen cookie from being replayed on another device, but it does not constrain automation on the device holding the key: malware or a VLM operating that device inherits the bound session. Tarrach et al. [92] identified message integrity gaps accessible to browser extensions. Kuchhal et al. [93] found only 4.4% of authenticators carry Level 2+ malware resistance certification. The structural limit is not the cryptographic protocol but the practical difficulty of guaranteeing the integrity of the key-storage environment.

**The universal ceiling: supply-chain economics.** Both Tier 1 architectures ultimately depend on the cost of obtaining control of a real enrolled device — by purchase, rental, or compromise. This cost is not determined by the protocol design but by device and account markets, the malware supply chain [75], the effectiveness of OS-level security mitigations (iOS hardened runtime, Android KeyStore, Windows Credential Guard), and the user's security posture. Every Tier 1 architecture has an economic ceiling below which it deters adversaries and above which it does not.

### 4.4 The False Dichotomy: Why PATs Are Not a Silver Bullet

A naive reading of Section 4.2 might suggest that PATs and DBSC represent a complete solution: deploy PATs for anonymous traffic, deploy DBSC for authenticated sessions, and the anti-automation problem is solved. This is structurally incorrect for three reasons.

**1. PATs require platform-level coordination.** In the Privacy Pass architecture (RFC 9576) [5] the *attester* and the *issuer* are distinct roles. For deployed PATs, Apple is the attester (vouching for the device and account), and issuers are third parties such as Cloudflare and Fastly. No equivalent PAT attester is operated by Google or Microsoft. A web origin therefore cannot deploy PATs independently: it depends on an OS vendor acting as attester and on an issuer it trusts, a dependency not guaranteed across platforms, regions, or use cases.

**2. PATs shift the trust problem rather than solving it.** Pre-PATs, the trust question was: "Can I distinguish human from automated traffic?" Post-PATs, it becomes: "Do I trust the attester's device and account checks, and the issuer's policy, more than probabilistic detection?" For many defenders the answer is yes, but this is an economic and political judgment, not a technical guarantee — and today the attester role for PATs is held by a single platform vendor whose incentives may diverge from those of the web origin consuming the token.

**3. PATs create a two-tier accessibility surface.** If probabilistic defenses degrade under Operator Synthesis and hardware-anchored tokens become the preferred anonymous signal, a web origin that deploys PAT-only anti-automation effectively requires an Apple device (iOS 16+/macOS Ventura+). Android and most desktop users have no PAT path and must fall back to other challenges. This creates an accessibility barrier that is structurally regressive.

**The software-anchor response and its limits.** The PACT initiative [11] is best read as the industry's own acknowledgment of these three limitations — in particular the platform-coordination dependency of reason 1 — but it does not resolve them. PACT broadens the issuer set beyond OS vendors to any party that "knows something about the user" — identity providers, subscription services, e-commerce platforms [11, 43] — which addresses reason 1 only by multiplying the parties whose judgment becomes security-critical. Reason 2 intensifies in a different form: the trust question becomes "Do I trust Cloudflare's or any accredited issuer's admission process more than probabilistic detection?" and, as Section 6.4 details, no accreditation, revocation, or audit regime for issuers has been specified [11, 90]. Reason 3 likewise intensifies: if issuers anchor on financial or account-standing signals, the accessibility barrier is no longer device ownership but *consumer status* — unbanked, low-income, and anonymity-seeking users may have no usable issuer relationship at all [44]. The CAPTCHA that PACT replaces could at least be solved without proving consumer status; a subscription-anchored token cannot.

---

## 5. A Structured Cost-Accounting Exercise for VLM-Driven Attacks (Part II)

*This section provides a structured cost-accounting exercise for reasoning about the economics of Operator Synthesis attacks. The market is too young for a predictive economic model; our equations are accounting identities (quantity × price) that organize cost categories rather than models that predict outcomes. We identify the empirical gaps that prevent precise quantification and set a research agenda for closing them, extending the conjunctive cost framing of Section 3 and prior work [4] to the Operator Synthesis paradigm.*

*Terminology.* To avoid ambiguity, "LLM tokens" denotes units of model input/output billed by an inference API; "clearance tokens" denotes the artefact a defensive VM or challenge issues on success (e.g. a Botguard response or challenge-clearance cookie) that the attacker is trying to obtain.

**Table 5.1 — Cost parameters.** Rows marked *verified* were checked against the cited public price page (accessed 2026-09-23); rows marked *assumption* are illustrative values chosen to make the arithmetic concrete and should not be read as measured market prices.

| Parameter | Value used | Status |
|---|---|---|
| Frontier VLM input price `p_in` | $1.25–$5.00 per M LLM tokens | verified at lower/middle end: GPT-5 $1.25 [94], Gemini 2.5 Computer Use $1.25 [95], Claude Sonnet 4.6 $3.00 [96]; upper end assumption |
| Frontier VLM output price `p_out` | $5.00–$20.00 per M LLM tokens | verified points: $10 (GPT-5, Gemini 2.5 CU), $15 (Sonnet 4.6); range ends assumption |
| LLM tokens per action | ∼1,000 in / ∼500 out | assumption (lower bound; a single screenshot alone typically exceeds 1,000 input tokens) |
| Actions per clearance token `n` | 5–10 | assumption |
| Per-attempt success `P` | 0.4–0.7 | assumption, informed by [7, 14, 29] |
| Residential proxy, commodity | ∼$2.50–$6/GB | TODO(author): Bright Data page [97] unreachable from our network on 2026-09-23; earlier-recorded "from $5.88/GB" not re-verified |
| Residential proxy, premium / dedicated | ∼$10–$50/GB | assumption |
| VLM latency per perception–action step | 5–15 s | assumption (no public per-step figure; consistent with [98]) |
| Scripted-step latency | 0.5 s | assumption |

### 5.1 VLM Inference Cost Under Operator Synthesis

The primary variable cost of an Operator Synthesis attack is VLM inference. Prior conjunctive cost models [48] identified the multi-cost structure of Environmental Forgery — proxy IPs, anti-detect software, profile aging. Under Operator Synthesis, VLM inference is an *additional necessary* cost for any attack that requires visual perception of rendered browser content, supplementing rather than supplanting the proxy and state-orchestration components of prior models.

**Base cost-accounting equation.** The per-task inference cost is:

```text
C_inference = Σ_{i=1..n} (t_in,i × p_in + t_out,i × p_out)
```

Where `n` is the number of actions per attempt, `t_in,i` / `t_out,i` are the LLM tokens consumed at step `i` (screen capture encoding plus accumulated prompt context; action selection plus coordinates), and `p_in` / `p_out` are per-LLM-token prices (Table 5.1). Tokens × price is already a dollar amount; no further per-token factor applies.

**Per-action and per-attempt cost.** With 1,000 input LLM tokens at $1.25–$5.00/M and 500 output LLM tokens at $5.00–$20.00/M, one action costs $0.00125–$0.005 + $0.0025–$0.01 = **$0.00375–$0.015**. For `n` = 10 actions the naive per-attempt cost is $0.0375–$0.15. This is a lower bound for two reasons. First, a full-resolution screenshot usually encodes to more than 1,000 input LLM tokens. Second, an agent that keeps the history of previous screenshots and actions in context re-sends that history at every step, so `t_in,i` grows roughly linearly in `i` and the per-attempt cost grows superlinearly (roughly quadratically) in `n` unless the attacker prunes or summarises context. Prompt caching and batch tiers lower the effective price of the repeated prefix.

**Hybrid attackers.** A cost-minimising attacker does not call the VLM on every step. Deterministic, stable steps (navigation, known form fields) can be scripted; the VLM is invoked only on the fraction `f` of steps that require perception or recovery from unexpected state:

```text
C_inference,hybrid ≈ f × C_inference + (1 − f) × n × c_script
```

where `c_script` ≈ 0 relative to VLM calls. For `f` = 0.2, the per-attempt inference cost above falls five-fold. The pure-VLM figures in this section are therefore an upper bound on what a competent operator pays.

**Hybrid-attacker sensitivity.** Table 5.2 sweeps `f` and `P(success)` for a 10-step flow at a single verified price point (Sonnet 4.6, $3/$15 per M LLM tokens [96]) with the Table 5.1 token assumptions. "Accumulated" context means the k-th VLM step re-sends the k screenshots seen so far (linear growth of `t_in,i`); "none" means the attacker prunes history. Latency assumes 10 s per VLM step (midpoint of Section 5.2) and 0.5 s per scripted step (assumption). All values are generated by `analysis/cost_model.py` from `analysis/params.json` (Open Science).

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

Table: Table 5.2 — Hybrid-attacker sensitivity (illustrative; parameters in Table 5.1 and `analysis/params.json`).

Two regularities follow. Cost per success spans roughly 50× across the grid (≈$0.01 to $0.60), and `f` moves it more than `P(success)` does: a hybrid attacker at `f` = 0.1 with a weak model (`P` = 0.4) pays less than a pure-VLM attacker with a strong one (`P` = 0.9). Context accumulation matters only when many steps use the VLM (`f` ≥ 0.5). Latency tracks `f` alone: at `f` ≤ 0.3 an attempt takes 14–34 s, inside the human range for a multi-step form, so neither cost nor timing (Section 5.2) discriminates a low-`f` hybrid attacker from a human.

**Modeling failure rates.** VLMs hallucinate, select incorrect bounding boxes, enter navigation loops, and time out on dynamic DOM elements. If each attempt costs `C` and succeeds independently with probability `P(success)`, the expected number of attempts per success is `1/P(success)` and the expected cost per successful clearance token is:

```text
C_effective = C / P(success),   where C = C_inference + C_replan
```

`C_replan` denotes only the *extra* LLM tokens an attempt spends diagnosing a failed prior attempt and re-planning; it is not a second charge for the retry itself, which the `1/P(success)` factor already counts. At `P(success)` = 0.6 — consistent with reported agentic benchmarking on complex multi-step flows [7, 14] and measured VLM-CAPTCHA solving rates [29] — the multiplier is 1.67×; at 0.4 it is 2.5×. Worked example: with `C` = $0.05 per attempt, `P(success)` = 0.4 gives $0.05/0.4 = $0.125 per clearance token and `P(success)` = 0.7 gives $0.05/0.7 ≈ $0.071. A 30-percentage-point difference in success rate thus changes the cost per success by ≈ 43% (from $0.125 down to $0.071). Whether that matters depends on how long the resulting clearance token remains usable.

The dependence of `P(success)` on task complexity yields a testable prediction: defenses that increase perceptual ambiguity (dynamic layouts, canvas rendering, adversarial-noise overlays) should reduce VLM task success and raise `C_effective`.

**Scaling properties.** VLM inference prices have trended downward: between 2023 and 2026 vendors repeatedly cut per-LLM-token list prices for a given capability level (e.g. GPT-5 launched at half GPT-4o's input price [94]). Two qualifications apply. First, these are vendor-published list prices, not marginal inference costs; volume, batch, and cached-pricing tiers reduce effective prices further, while list prices understate the cost of serving under sustained adversarial load. Second, the deflation trajectory is an observed market trend, not a law: it is plausible but not guaranteed to continue at the same rate, and the economics of VLM-driven attacks inherit that uncertainty. The mechanisms that have driven the reductions to date include:

- Quantization (FP16 → INT4 reduces cost by ∼4×)
- Speculative decoding (2–3× throughput improvement)
- Model distillation (smaller models for specific tasks)
- Inference hardware specialization (TPU v5p, NVIDIA B200, custom ASICs)

This deflation means the cost ceiling of VLM-based attacks is *temporally unstable* — it has tended to fall over time, unlike the relatively stable cost of human labor or residential proxy IPs.

### 5.2 The Latency Cost: Temporal Overhead as a Non-Trivial Attack Surface

The cost exercise in Section 5.1 considers only token-price economics. A second cost dimension — temporal latency — operates independently and can trigger defensive mechanisms that price reductions do not mitigate. As a working assumption (Table 5.1), a frontier VLM takes 5–15 seconds per perception–action cycle (screen capture encoding, inference, action selection). We found no public per-step latency figure for commercial computer-use models; the closest measurement, OSWorld-Human, reports that state-of-the-art computer-use agents take tens of minutes on OSWorld tasks that humans finish in a few, with planning and reflection LLM calls accounting for 75–94% of end-to-end latency [98], which is consistent with multi-second steps but does not pin down our range. For flows of 5–10 actions per clearance token, wall-clock time is therefore 25–150 seconds per attempt.

This latency matters for two reasons:

1. **Chronometric heuristics (L4).** The L4 layer was originally designed to detect microsecond-scale timing deviations introduced by JavaScript instrumentation layers. Under Operator Synthesis, the instrumentation gap closes — no DevTools or debugger introduces timing noise. What remains is a *macroscopic* signal: the per-action latency distribution. The comparison must be made carefully. A passive VM challenge (e.g. a Botguard-style script that collects telemetry in the background) requires no human interaction at all, so there is no "human completion time" to compare against — the VM finishes in the same time for a human and a VLM-driven browser. Where a flow does require interaction, humans also take tens of seconds on multi-step forms, so the aggregate session duration of a VLM (25–150 s for 5–10 actions) overlaps the human range rather than exceeding it by a fixed factor. The distinguishing feature, if any, is distributional: VLM per-action latency is bounded below by inference time (seconds) and comparatively regular, while human per-action latency is noisier and includes sub-second interactions. Timing is therefore a weak signal. It can contribute to a risk score, but used as a hard rule it produces false positives on slow, distracted, or assistive-technology users (screen readers, switch access, voice control), and attackers can narrow the gap with smaller local models or by adding random delays.

2. **Session timeout risk.** Web applications impose server-side session timeouts (typically 5–30 minutes for authenticated sessions, 1–5 minutes for anti-automation challenge windows). At the upper end of the 5–15 s range, a 10-step flow takes 150 s, which approaches short challenge windows. Sessions that time out consume inference budget without producing a clearance token.

Timeouts are one of the failure modes already counted in `P(success)`; they must not be added a second time. The per-success cost including bandwidth is therefore:

```text
C_temporal = (C_inference + C_replan + C_bandwidth_per_attempt) / P(success)
```

where `P(success)` already includes `(1 − P(timeout))` as a factor. Faster inference (speculative decoding, specialised hardware, smaller local models) lowers `P(timeout)` and narrows the latency distribution gap at the same time.

### 5.3 The Proxy Supply Market: Elasticity, Equilibrium, and Exhaustion

Under Environmental Forgery, the proxy supply market was the binding structural constraint. Under Operator Synthesis, the proxy is still required — the VLM must route traffic through residential IPs — but the economics shift because the VLM imposes different demands on the proxy infrastructure.

**Supply elasticity.** Residential proxy markets exhibit a tiered supply structure [91]. We use "elasticity" qualitatively; we do not estimate it. Only the commodity band below is checked against a public price page (Table 5.1); the others are illustrative:

- **Commodity tier:** ∼$2.50–$6/GB for shared residential IPs [97]. Supply is large at this price, but reputation is a commons [63]: aggressive usage burns IP reputation across the pool.
- **Premium tier (assumption):** ∼$10–$15/GB for exclusive or less-used residential IPs; supply is bounded by the number of enrolled devices.
- **Dedicated tier (assumption):** ∼$25–$50/GB for dedicated IPs with cleaner reputation.

Session continuity does not by itself force the attacker off the commodity tier: commodity residential providers routinely sell "sticky" sessions that pin one exit IP for minutes to hours, which covers a 25–150 s VLM flow. What pushes demand upward is reputation, not stickiness: a VLM session is slow and stateful, so each exit IP is exposed to the target for longer, and a burned shared IP costs the attacker a whole multi-step attempt rather than a single request.

**Conjunctive cost model under Operator Synthesis.** Prior work modeled the conjunctive cost of stateful telemetry bypass as: `Cost_proxy + Cost_aged_profile + Cost_software_license`. Under Operator Synthesis, the attacker who drives a stock browser eliminates the anti-detect software license but *substitutes a state-orchestration infrastructure cost*:

```text
Cost_bypass_OS = Cost_residential_proxy + Cost_session_isolation + Cost_VLM_inference
```

Where `Cost_session_isolation` includes:

- Containerized browser instances per session (Docker/K8s orchestration)
- Persistent cookie-jar and local-storage management
- Profile rotation and rehydration infrastructure
- Bandwidth for browser binary downloads and updates

Under Operator Synthesis the attacker therefore does not simply "save" the anti-detect browser cost; they replace it with heavy state-orchestration infrastructure that was previously bundled in the anti-detect browser license. The net savings are plausibly positive — orchestration infrastructure is cheaper per-session than anti-detect software licensing — but this remains a qualitative claim: no public pricing data currently permits a direct per-session comparison of the two cost stacks, and the relative magnitudes should be treated as an open empirical question (Section 7.1) rather than a settled result.

### 5.4 Human Labor as the Global Cost Floor: Revisited

Prior work correctly identified human labor — CAPTCHA-solving farms at ∼$1 per 1,000 challenges [17], click-farms and freelance labor markets for behavioral challenges [99] — as the global cost floor for bypassing behavioral biometrics under Environmental Forgery. Under Operator Synthesis, this floor shifts:

- **Single perception tasks (CAPTCHAs).** Human labor and VLM inference are substitutes; the attacker pays `min(C_VLM, C_human)`. CAPTCHA-solving services charge roughly $0.50–$2.00 per 1,000 solves [17], i.e. $0.0005–$0.002 each — below the $0.00375–$0.015 per VLM action in Section 5.1 — but VLM prices are falling while labor prices are comparatively stable.

- **Multi-step flows (the Operator Synthesis case).** Human labor is also a substitute here: [99] documents paid human workers carrying out multi-step abuse such as account creation and fraudulent engagement. The comparison therefore stays `min(C_VLM, C_human)`, where `C_human` is a per-task wage for the whole flow rather than a per-CAPTCHA price. What the VLM changes is not substitutability but scaling: labor throughput grows with headcount and recruitment, while VLM throughput grows with API quota and parallel sessions.

### 5.5 The Temporal Arms Race Under Operator Synthesis: T_RE ≈ 0 at the VM Level

Under Environmental Forgery, the temporal arms race between defender compile rotation and attacker RE takes the form of a race condition (Section 3.5):

```text
T_RE < T_Life → defense is structurally bypassed
T_RE > T_Life → defense imposes recurring cost
```

Under Operator Synthesis, `T_RE ≈ 0` for the VM bytecode itself — the attacker never reverse-engineers the defensive VM. The VM-level temporal constraint is eliminated.

**Caveat: per-target workflow cost is not zero.** The attacker does not RE the VM, but must still specify the task: which pages to visit, what goal to state, what counts as success, and how to recover from errors. A pixel-level VLM acts on screen coordinates and does not need the page's DOM hierarchy or CSS selectors; the per-target cost is therefore prompt and success-criterion engineering plus testing, not frontend reverse engineering. Hybrid attackers (Section 5.1) do inspect the DOM for the scripted fraction `1 − f` of steps, and pay the corresponding per-target cost there. This fixed cost is small relative to VM bytecode RE, but it scales with the number of distinct target workflows and must be amortised across many sessions.

**Implication for defenders.** Security that rests on VM obfuscation complexity or compile rotation cadence does not constrain an Operator Synthesis attacker, who is not racing at the VM level. Randomised element selectors raise costs only for the scripted (DOM-driven) part of a hybrid attack; against the VLM-driven part, what matters is visual and sequential variation (changing layouts, variable interaction sequences) that lowers `P(success)` or raises `f`.

**What remains at the VLM level.** The remaining VLM-specific temporal constraint is training-data freshness: a challenge whose interaction pattern post-dates the model's training cutoff may elicit out-of-distribution behaviour. The gap between training cutoff and public deployment of frontier models is typically several months, so this window is real but narrow, and in-context examples in the prompt can often bridge it without retraining.

### 5.6 Tier 1 Under a Device Farm: Cost per Clearance Token

Section 4.2 (tier table) places hardware-anchored Type IV (PATs) and Type V in Tier 1 because they are indifferent to input modality; their attacker cost is acquiring real enrolled devices, bounded by attester rate limits (Section 4.3). This subsection turns that sentence into an accounting identity for the PAT case:

```text
C_token = (D / L + O) / (R × 30)
```

where `D` is the device price, `L` the amortisation period in months, `O` farm operations per device-month (mobile proxy or SIM, power, management), and `R` the clearance tokens one device can obtain per origin per day under the attester's and issuer's rate limits. Account cost (one Apple Account per device) is omitted and would add to `D`.

**Parameters.** `D` = $100–$300 for a used PAT-capable iPhone and `L` = 12–24 months are assumptions (TODO(author): cite a dated used-market price snapshot). `O` = $9.30–$48.80 is derived from an anti-detect vendor's published phone-farm cost breakdown (monthly total for a 10-device farm ÷ 10) [100]; it is vendor-reported, Android-oriented, and not independently verified. The owned-device monthly cost is therefore $13.47–$73.80 per device-month. As a rented alternative, an AWS EC2 `mac2.metal` host lists at $0.65/hour with a 24-hour minimum allocation [101], i.e. $468 per month; whether PAT issuance works on EC2 Mac hosts is unverified. `R` is the key unknown: Apple does not publish its attester or issuer limits, and the rate-limited issuance design [10] leaves the per-origin limit to the issuer. We therefore sweep it.

| Rate limit (tokens/device/origin/day) | Owned used iPhone, low | Owned used iPhone, high | Rented cloud Mac |
|---|---|---|---|
| 1 | $0.449 | $2.46 | $15.60 |
| 10 | $0.045 | $0.246 | $1.56 |
| 100 | $0.0045 | $0.025 | $0.156 |
| 1000 | $0.0004 | $0.0025 | $0.016 |

Table: Table 5.3 — Tier 1 (PAT) cost per clearance token vs. per-device rate limit (generated by `analysis/cost_model.py`).

**Reading the table.** Tier 1's cost is a function of `R`, which the defender (issuer) controls. At `R` = 1 per origin per day, a farmed token costs $0.45–$2.46 — above every VLM cost per success in Table 5.2. At `R` ≥ 100 it drops below one cent, cheaper than VLM inference and comparable to CAPTCHA-farm labor (Section 5.4). The VLM cost stacks on top only if the farm needs perception; a scripted farm pays none. Tier 1 is thus not "resilient" in the abstract: it is exactly as expensive as the issuer's rate limit makes it, and a strict limit also caps legitimate high-frequency users.

**Alternative acquisition paths.** *Device compromise (PPI).* Caballero et al. measured pay-per-install prices of $7–$180 per 1,000 installs, i.e. $0.007–$0.18 per install [74]; these are 2011 Windows prices, and no public price exists for installs on PAT-capable Apple devices, which is likely far higher. A compromised device is subject to the same `R`, so per-token cost is the install price amortised over the tokens obtained before remediation. *Account acquisition (PACT-style software anchors).* Where the issuer admits on account standing rather than hardware (Section 6.4), the unit of scarcity is an account; Thomas et al. observed bulk fraudulent-account prices of $10–$200 per 1,000, i.e. $0.01–$0.20 per account [49] (Twitter, 2012–13; not directly transferable to accounts with payment or subscription history). In all three paths the ceiling is a market price divided by an issuer-controlled rate limit.

---

## 6. Industry Trajectory and the Attestation Market Centralization Problem (Part II)

Industry deployment over 2024–2026 has advanced along three tracks — hardware-anchored session determinism (DBSC), credential-phishing-resistant authentication (passkeys), and anonymous attestation (Privacy Pass, Apple PATs, and the 2026 PACT initiative). DBSC and passkeys address authenticated-session threats (cookie theft, credential phishing) rather than anonymous automation; anonymous attestation is the track that bears on the Anonymous Authentication Gap, and it does so by relying on a small set of attesters and issuers. The thesis of this section is that this reliance converts the gap into an Attestation Market Centralization problem (§6.3), which the PACT software-anchor proposal extends rather than resolves (§6.4).

### 6.1 DBSC and the Session-Hijacking Threat Model

DBSC [27, 28, 102] is a Google/Chrome-led protocol that binds session cookies to a device-resident key held in a TPM (or equivalent secure hardware); the browser periodically proves possession of that key to refresh short-lived cookies. The key is generated as non-exportable and no vendor attestation server is involved: the relying site simply registers the public key. Non-exportability protects the key only after registration: Chrome's developer documentation cautions that malware already present on the device during session registration may be able to extract the private key, enabling hijacking comparable to ordinary cookie theft, although it rates such attacks (like TPM-driver modification) as considerably harder and more detectable [102]. (DPoP [103] is a related proof-of-possession mechanism for OAuth tokens, not the DBSC protocol.) DBSC targets the session-hijacking threat model (NIST 800-63 Authenticated/ATO quadrant [12]): it is an anti-cookie-theft mechanism, not an anti-automation mechanism, and it says nothing about whether a fresh anonymous session is driven by a human or a VLM.

Its effect on the infostealer economy [74, 75, 104, 105] is to change what stolen material is worth. Because the private key cannot be exported, exfiltrated cookies expire quickly once replayed off-device; the attacker must instead keep malware resident and *use* the key on the infected machine, routing session traffic through it. The economic ceiling therefore moves from the price of a stolen cookie log to the price of persistent on-device access, i.e. botnet rental and residency. It is still set by device-compromise economics rather than by cryptographic strength, but it is higher than the pre-DBSC ceiling and scales with the number of compromised devices, not the number of stolen logs.

A residential-proxy SDK running on a consenting user's device does not change this picture: it relays traffic but cannot produce DBSC proofs for sessions that originate elsewhere, because the key is bound to the browser profile on that device. Only code that drives the enrolled browser itself — malware, or an operator controlling a device farm — can exercise the key.

### 6.2 Passkeys and the Credential-Phishing Threat Model

Passkeys (FIDO2/WebAuthn [39]) eliminate shared secrets and bind credentials to the relying party's origin — the latest step in the documented evolution of password-based authentication [106]. Origin binding defeats credential phishing for the passkey itself, but deployments that keep weaker fallback factors remain exposed: Ulqinaku et al. [107] show that real-time phishing is *not* eliminated when FIDO is offered alongside phishable second factors that an attacker can downgrade to. Passkeys also carry little device information to relying parties: most consumer deployments use the attestation conveyance "none", so the relying party learns that a credential exists, not what hardware holds it. Where centralization appears, it is in the synchronization fabric (Apple iCloud Keychain, Google Password Manager, Microsoft) that stores and replicates credentials, not in a per-authentication root of trust. Kuchhal et al. [93] found only 4.4% of authenticators carry Level 2+ certification offering malware resistance. Tarrach et al. [92] identified message integrity gaps accessible to browser extensions, and timing side channels in authenticator behavior [108] further erode the assumption of unobservable key operations. The structural limit is the practical difficulty of guaranteeing key-storage integrity across the diversity of consumer devices and cloud-synchronized passkey stores [109].

### 6.3 The Attestation Market Centralization Problem

As probabilistic defenses lose cost-imposing power against Operator Synthesis, the defenses that retain it for anonymous traffic — hardware-anchored anonymous tokens — depend on a small number of parties that vouch for devices. None of them distinguishes a human from a VLM driving a real device; they move the attacker's cost to acquiring real, enrolled devices, and bound throughput by attester rate limits. Who controls that vouching is therefore the structural question.

**Where trust concentrates.** Using RFC 9576 roles [5] (the *Attester* vouches for the client; the *Issuer* signs the token; the *Origin* redeems it):

- **Apple PATs:** Apple is the Attester, using device attestation on iOS 16+ and macOS Ventura+ [1]; issuance is performed by third-party Issuers such as Cloudflare and Fastly, which sign RSA blind-signature tokens. Apple's attester performs device attestation and "can also perform rate-limiting" [1], though Apple publishes no per-device limits; there is no per-session user consent step, and Android has no PAT equivalent. Concentration here is in the attester role.
- **Private State Tokens:** a Chrome API [26] in which *registered third-party issuers* (not Google) issue VOPRF-based tokens that origins redeem. Google's October 2025 Privacy Sandbox update retired most Sandbox APIs but stated that Private State Tokens will be maintained [110]. Concentration here is in the browser vendor's issuer-registration process rather than in a hardware root.
- **DBSC:** a Google/Chrome-led protocol with non-exportable keys and no vendor attestation server (§6.1). It is not an anonymous-attestation scheme; its only centralizing dependency is on the TPM and OS key-storage stack, and we therefore do not count it in the attestation-market argument.
- **PACT:** a cross-browser proposal announced in June 2026 by Cloudflare with Mozilla, Google, Microsoft, and Shopify [11]. It adds no hardware root of trust; it concentrates a different asset — the judgement of which parties may vouch that a person is present (§6.4).

**The centralization–anonymity–bot-resistance tension (informal argument).** Anonymous-token constructions such as Kreuter et al.'s private-metadata-bit tokens [9] and the analysis of rate-limited Privacy Pass [10] show how issuance can be made unlinkable and rate-limited; they are constructions and security analyses, not analyses of market structure. Our argument builds on them informally. Consider three goals: (i) redemptions unlinkable to identities, (ii) bounded per-client token supply (bot resistance), and (iii) no small set of trusted parties. A scheme meeting (i) and (ii) must rate-limit on *something* that the issuer can count without identifying the user — in deployed systems, a device key attested by a platform vendor or an account held with a large first party. Requirement (ii) therefore pulls toward attesters that already hold a large, Sybil-resistant population, which is the definition of a concentrated market. Relaxing decentralization (iii) is thus the path of least resistance, and it is the path deployed systems have taken. This is not an impossibility result: threshold issuance, zero-knowledge proofs of personhood, and decentralized issuer networks are feasible in principle. The open question is whether any of them can obtain a Sybil-resistant population at the scale platform vendors already have, and what pricing power, exclusion risk, and lock-in follow if none can.

**The ad-tech context.** Browser vendors that also operate advertising platforms shape both the availability of stateful identifiers and the attestation APIs that replace them. Chrome announced in 2024 and confirmed in 2025 that it will not deprecate third-party cookies, retaining user choice instead [110], so the pressure on Type II state comes mainly from Safari ITP, Firefox Total Cookie Protection, and regulation (§7.4). The intersection of ad-tech market position and bot-mitigation infrastructure nonetheless warrants scrutiny beyond protocol analysis.

### 6.4 PACT: The Software-Anchor Turn and the Issuer Judgment Problem

*This subsection is a case study of an emerging proposal, not of a deployed system.* On June 22, 2026, Cloudflare announced **Private Access Control Tokens (PACT)**, an initiative with Mozilla Firefox, Google Chrome, Microsoft Edge, and Shopify, committing to develop and submit for standardization a privacy-preserving protocol that lets "sites with strong knowledge of 'personhood'" issue anonymous tokens which the browser presents to other sites to show that a human is in the loop [11]. PACT builds on the Privacy Pass architecture (RFC 9576 [5]). The technical design predates the announcement: the `antifraudcg/pact` repository in the W3C Anti-Fraud Community Group was created in December 2025, and its design issues (aggregating issuers [43]; issuer blinding [111]) date from December 2025 [112]; the June 2026 press release made the effort public and added the browser commitments. As of this writing PACT is a proposal: there is no deployment timeline, no IETF draft published under the PACT name, and no finalized issuance-governance specification. The most consequential decision — who may issue tokens, and on what basis — remains open. Apple, which co-developed Private Access Tokens with Cloudflare in 2022, is not listed among the participants [11].

The architectural significance of PACT for this SoK is its break with the hardware anchor that motivates Type IV's Tier 1 classification (Section 4.2). In RFC 9576 terminology [5], the **Attester** is a party that knows something about the client, and the **Issuer** signs the blinded token. Apple PATs anchor that knowledge in device posture — approved device, approved hardware, approved operating environment, verified without installed software [1]. PACT instead accepts *software or contextual anchors*: active subscriptions, account standing, first-party relationships, or issuer vouching [43, 44]. This does not remove the Sybil problem; it relocates it. The attacker's unit of scarcity ceases to be a compromised device and becomes a credentialed account — and bulk account registration, credential stuffing, stolen session tokens, and cheap subscriptions are all automatable inputs to a token-farming pipeline that operates upstream of the attestation protocol. As one analysis puts it, token farming creates a new abuse layer upstream; the fix, hardware attestation, slides back into exactly what Web Environment Integrity was rejected for [90].

The proposal assigns the browser the role of trusted user-agent: it mediates credential storage, issuer selection, challenge budgets, and token conversion [43]. Under the Operator Synthesis threat model, this boundary is not a trust anchor. A bot operator may control the browser profile, the device, or both, and a copied or compromised profile can exercise the same issuance APIs as a legitimate user. The cryptographic unlinkability of blind signatures does not repair this: it ensures that a redeemed token cannot be linked to the issuance event or the user who obtained it, but the token still reveals which issuer key signed it — hiding the issuer is precisely what the IssuerHide sketch [111] proposes as an extension. The token's value depends entirely on the quality of the issuer's admission process, and the announced attack surface reflects this — unauthorized endorsement acquisition, token replay, token theft, credential export, anchor impersonation, malicious anchor behavior, Sybil amplification, metadata leakage, and downgrade attacks [44].

PACT's centralization profile differs from hardware attestation's. The concentration is not in device roots of trust but in issuer judgment: origins are expected to configure up to two aggregating issuers and a credit cost per request [43], which makes the origin's issuer choice a gatekeeping decision, and Cloudflare — already the termination point for a substantial share of web traffic — a natural central participant [90]. The structural dynamic that critics identified in Google's Web Environment Integrity proposal recurs: a small number of platforms decide which clients are treated as legitimate [90]. The ratchet effect amplifies it. PACT tokens begin as optional friction-reducers, but as adoption spreads, the *absence* of a token carries information: token-bearing traffic passes cleanly, untokened traffic is challenged more aggressively, risk thresholds are recalibrated, and no single actor decides to make tokens mandatory [90]. The result is a systematically suspect class of legitimate traffic with no issuer relationship — internet measurement systems, security research scanners, archival crawlers, RSS readers, Tor users, and alternative browsers [90]. Compounding this, PACT as announced lacks the governance mechanisms that would control issuer quality: no issuer accreditation model, no public issuer directory, no revocation lists, no audit requirements, and — as the nearest rate-control mechanism — only the IETF's rate-limited issuance draft [90]. Absent these, the ecosystem faces the classic adverse-selection problem: low-quality issuers undercut high-quality ones, and a blind-signature token proves only that *some* issuer signed it, not that a meaningful personhood check occurred.

Three further trade-offs warrant note. First, metadata: blind signatures protect linkability at the verifying origin, but the initial issuer still observes which account requested a token and when [43]; the aggregating-issuer and IssuerHide (zero-knowledge issuer-blinding) architectures discussed in the PACT repository would mitigate this [43, 111], but they remain design options, not properties of PACT as announced. Second, exclusion: if issuers anchor on financial or account-standing signals, the system distinguishes consumers with persistent platform relationships from everyone else — inverting the intended anti-abuse effect, since sophisticated bot operators can afford accounts while legitimate low-income or anonymity-seeking users cannot [44]. Third, sovereignty: a state that becomes a mandatory issuer could observe issuance events, deny tokens to disfavored traffic, and require acceptance of state-issued credentials within its jurisdiction; data-localization regimes could balkanize the web at the protocol layer [44]. Finally, PACT is explicitly motivated by agentic AI traffic [11], yet its token semantics for the human → AI agent → website model — whether each agent receives its own token, whether shared tokens invite replay and theft, and whether delegated issuance exists — are unresolved. PACT answers "is a real person behind this session" without answering "which actor is authorized to spend that personhood" [90]. The cryptographic layer is the least controversial part of the proposal; the governance layer is absent. Until issuer accreditation, revocation, auditing, aggregation defaults, and an explicit open-web fallback are specified, PACT is not a trust protocol so much as a trust-proxy protocol: it inherits the security posture of whatever issuer an origin happens to configure [90].

---

## 7. Open Problems and Future Research

This section identifies four open problems, ordered by research leverage: closing the empirical gap in VLM attack economics (Section 7.1), designing VLM-resilient attestation primitives (Section 7.2), standardizing evaluation under Operator Synthesis (Section 7.3), and accounting for how privacy regulation constrains stateful mitigation (Section 7.4).

### 7.1 Closing the Empirical Gap in VLM Attack Economics

The cost-accounting framework in Section 5 is deliberately incomplete. We currently lack:

- Published empirical measurements of VLM-driven attack throughput at industrial scale
- Reliable data on proxy market supply elasticity under Operator Synthesis demand patterns
- Longitudinal studies of VLM inference cost deflation and its impact on attack economics

Initial empirical measurements have begun to appear: generalized VLM agents now solve production CAPTCHAs with reported success rates that make large-scale operation economically plausible [29], CAPTCHA-class benchmarks against VLM attacks are being standardized [64], and reasoning-action training pipelines for GUI-agent CAPTCHA solving are being industrialized [30]. What remains missing is measurement at industrial scale — attack throughput under sustained load, session-continuity behavior across proxy pools, and proxy market elasticity under Operator Synthesis demand. A standardized, ethical benchmark for measuring VLM-driven bypass costs (§7.3) is needed to transform the qualitative economic analysis of Section 5 into a quantitative discipline.

As a first step we release a self-hosted measurement harness in the artifact (`measurement/`). It consists of a testbed bound to localhost (a five-step form flow carrying a cognitive-honeypot decoy, Turnstile and reCAPTCHA v2 widgets using the vendors' documented test keys, and server-side event logging), plus four attacker configurations: DOM/CDP automation, scripted OS-level input, a pure VLM computer-use agent, and a hybrid. An analysis script turns the logs into pass rate, per-action latency, and dollar cost per success, pricing tokens from `analysis/params.json`. Agents are only ever pointed at this local testbed, never at third-party or production sites; test keys give fixed outcomes, so the harness measures agent cost and latency, not vendor detection. We have not yet run it at a scale worth reporting, so this paper contains no measured numbers from it; every figure in Section 5 remains the illustrative accounting of Table 5.1.

### 7.2 VLM-Resilient Attestation Primitives

The Tier 1 architectures identified in Section 4.2 survive Operator Synthesis but carry the structural dependencies documented in Section 6. Research needed on:

- **Decentralized anonymous attestation:** Zero-knowledge proofs of personhood, decentralized issuer networks (threshold issuance, distributed VOPRF), and hardware-backed attestation without OS-vendor dependency. The PACT design discussion illustrates both the feasibility and the governance gap: aggregating-issuer and IssuerHide architectures [43, 111] would mitigate initial-issuer metadata exposure, but as of the 2026 announcement they remain design options rather than defaults, and no decentralized issuer network has been specified [11, 90].
- **Physical-presence challenges:** Defenses that require physical-world interaction (camera-based liveness detection, ambient sensor fusion) that a VLM operating in a virtual machine cannot satisfy. These are not CAPTCHAs — they do not require human cognition — but they impose a physical-presence cost that distinguishes local execution from remote VLM operation. Defenders must account for a critical countermeasure: incentivized proxying, where SDK-based proxy networks—leveraging the attestation bypass dynamics analyzed in Section 4.3—prompt the legitimate device owner to satisfy the physical challenge in exchange for in-app rewards, bridging the physical gap. This does not reduce the bypass cost to zero — it introduces latency (user must be available), incentive costs (per-action reward), and coordination complexity — but it establishes that physical-presence challenges require deployment-time threat modeling against SDK-mediated human relay, not just autonomous VLM operation.
- **Cross-modal consistency verification:** Verifying that sensor data from multiple independent channels (camera, microphone, touchscreen, accelerometer) is internally consistent with a single physical environment. A VLM operating in a VM cannot easily maintain cross-modal consistency because it does not control all sensor channels.

### 7.3 Standardized Benchmarking (The "Bot-Bench" Problem)

Academia lacks a standardized testbed for evaluating anti-automation defenses under Operator Synthesis. Current evaluations rely on grey-hat reverse engineering of production systems or small-scale PoCs that vendors invalidate through compile rotation. A reproducible, vendor-neutral evaluation harness — with known ground truth for human vs. VLM interaction — is necessary for systematic measurement. The BehavePassDB effort [113] provides a partial template but does not account for VLM interaction patterns; MCA-Bench [64] is a first step toward VLM-aware CAPTCHA benchmarking but covers only the CAPTCHA class, not VM attestation, behavioral telemetry, or attestation protocols.

Such a benchmark must also measure false positives on legitimate users, not only attacker success. Timing and behavioural signals (L4 latency profiles, kinematics, typing cadence) are exactly the signals that differ for users of screen readers, switch access, voice control, eye-tracking, or other assistive technologies, and for older or motor-impaired users. A defense that raises its threshold against VLM-driven input shifts cost onto these users as challenge escalation or lock-out; that cost is rarely reported and should be a first-class metric in any evaluation.

### 7.4 The Security–Privacy Trade-off in Stateful Mitigation

Stateful telemetry (Type II) relies on persistent client state to accumulate profile age. Profile age is a function of time and history; a VLM does not create it, and Operator Synthesis does not remove the requirement — an attacker must still buy aged profiles or operate real, long-lived devices. The same persistent state that makes profile aging work is, however, what privacy law and browser privacy features deliberately constrain. This is a genuine security–privacy trade-off, not a defect in either side, and its legal shape is under-studied.

**Legal framework (EU).** Two instruments apply to different actors. *Article 5(3) of the ePrivacy Directive* [114] requires consent for storing or accessing information on a user's terminal equipment, with an exemption where this is *strictly necessary* for a service explicitly requested by the user. The EDPB's *Guidelines 2/2023 on the Technical Scope of Art. 5(3)* [115] make clear that the provision covers not only cookies but also script-based collection of device information, which brings client-side fingerprinting and telemetry collection within scope. Whether bot detection qualifies as strictly necessary is a case-by-case question: security measures tied to a service the user requested (e.g. protecting a login or checkout) have a stronger claim than cross-site profiles built over time. Where personal data is then processed, the *GDPR* [116] requires a lawful basis; *Art. 6(1)(f)* (legitimate interests), read with *Recital 49*, which names network and information security — including preventing unauthorised access and "denial of service" attacks — as a legitimate interest, is the natural basis, subject to a balancing test and data minimisation. These obligations bind website operators and bot-mitigation vendors acting as controllers or processors. They do not bind browsers' tracking-prevention features: Safari ITP, Firefox ETP/Total Cookie Protection, and similar mechanisms are product decisions by browser vendors, not legal compliance mechanisms, and they are neither required nor constrained by GDPR.

**Two separate pressures.** It follows that stateful mitigation faces two distinct pressures that should not be conflated: (1) *legal* limits on what an operator may store and process, which leave room for security processing under the strictly-necessary exemption and legitimate interests; and (2) *technical* limits imposed unilaterally by browsers, which partition or expire state regardless of purpose and so reduce the profile-age signal even where its processing would be lawful. The second pressure is the one that most directly weakens Type II, and it applies unevenly: Chrome has kept third-party cookies (§6.3), so the effect is concentrated on Safari and Firefox users.

**Competition law as the centralization hook.** Where browser and OS vendors both restrict independent state and supply the attestation APIs that replace it (§6.3), the *Digital Markets Act* [117] is the relevant instrument. Alphabet (Chrome, Android) and Apple (Safari, iOS) are designated gatekeepers, and the DMA's interoperability obligation for hardware and software features accessed or controlled via the operating system (Art. 6(7), subject to a strictly-necessary integrity exception) provides a legal basis for asking whether attestation APIs and issuer-registration processes are offered to third parties on fair, reasonable, and non-discriminatory terms. How these obligations apply to anti-abuse attestation is an open research and policy question.

---

## 8. Conclusion

This SoK has presented a two-part systematization of client-side anti-automation. In Part I, we documented the historical landscape (2010–2024) through five mechanism-based architectural types and the L1–L4 diagnostic framework, explicitly framing these as retrospective artifacts that reveal why probabilistic client-side attestation has a finite economic ceiling. In Part II, we analyzed the Operator Synthesis attack vector for the APB threat model, showing that the cost burden of each layer shifts from browser-instrumentation forgery to systems-integration engineering: L1a shifts to container-evasion, L1b shifts to kinematic-smoothing orchestration, L2 shifts to application-level workflow RE, L4 shifts from microsecond instrumentation detection to second-scale latency profiling.

The Tier 1 architectures — platform-level anonymous attestation and hardware-anchored credentials — are not resilient to VLMs as such: they are indifferent to input modality, and a VLM driving a real attested device passes them. What they change is where the attacker's cost lies. Instead of forging an environment, the attacker must acquire real enrolled devices or accounts (device and phone farms, compromised machines), and throughput is bounded by attester rate limits. Their economic ceiling is the price of device acquisition or compromise, not the hardness of the protocol, and they depend on a small set of attesters and issuers.

Three insights define the field's trajectory for the APB threat model:

1. **Probabilistic client-side attestation faces severe structural pressure under Operator Synthesis.** Against a well-resourced adversary operating a VLM through an adequate orchestration pipeline, the detection premise on which VM attestation, behavioral telemetry, and biometric analysis relied is substantially degraded. Defenses that remain effective against commodity adversaries lose their cost-imposing power against this top-tier threat model. However, Operator Synthesis does not eliminate probabilistic detection entirely — the cost burden shifts rather than vanishes, as the L1–L4 diagnostic analysis demonstrates.
2. **Hardware-anchored attestation moves cost; it does not end the contest.** It shifts the attack surface to device-acquisition and device-compromise economics, bounded by rate limits, and introduces attester/issuer concentration and device-adoption dependencies.
3. **An increasingly important open problem is "who controls the infrastructure of web trust."** Anonymous attestation narrows the Anonymous Authentication Gap at the cost of concentration in attesters and issuers; the 2026 PACT proposal shows the question is contested along a second axis, as the industry experiments with replacing hardware anchors with issuer judgment (Section 6.4).

Client-side anti-automation faces a significant inflection point. The tools and concepts of the 2017–2024 period — register-based VMs, behavioral scoring, kinematic analysis — retain value as diagnostic artifacts and as defenses against the long tail of commodity automation, but their cost-imposing power is substantially reduced for adversaries operating at the top of the capability distribution. The field must now confront the harder problem of building decentralized, privacy-preserving attestation infrastructure that does not depend on a vendor oligopoly, alongside the continued engineering challenge of hardening probabilistic defenses against lower-resourced adversaries.

---

## Ethics Considerations

This paper is a systematization based on public sources and analytical reasoning. We performed no live attacks against production services, did not attempt to bypass any deployed anti-automation system, and performed no reverse engineering of Botguard for this paper; the L1–L4 model is our own synthesis from published descriptions and the obfuscation literature. The cost-accounting exercise (§5) is dual-use: a defender can use it to identify where cost is imposed, and an attacker could use it to prioritise effort. We judge the marginal uplift to be low, because every parameter is drawn from public pricing and published research and the analysis contains no bypass technique, tooling, or target-specific detail. Named companies and products are discussed only on the basis of their public documentation, announcements, and peer-reviewed or publicly reported analyses.

## Open Science

We release an artifact with: `analysis/params.json` (every §5 parameter with its source and verified/assumption status); `analysis/cost_model.py`, which regenerates every §5 number and asserts that each appears verbatim in the paper; `analysis/figure_cost_shift.py` (the systematization figure); the §3.1 search script and screening sheet (`analysis/literature_search.py`, `docs/corpus.csv`); and the self-hosted measurement harness (`measurement/`, §7.1), which has produced no results reported here.

## Use of AI Tools

[Author to complete per venue policy: AI-assisted drafting/editing was used for ...]

---

## References

**[1]** Apple Inc. "Replace CAPTCHAs with Private Access Tokens." *WWDC22 Session*, June 8, 2022. URL: https://developer.apple.com/videos/play/wwdc2022/10077/.

**[2]** Human Security, Inc. (formerly PerimeterX). "The Economics of Bot Mitigation." *Industry Whitepaper*, 2022.

**[3]** E. Bursztein, A. Malyshev, T. Pietraszek, and K. Thomas. "Picasso: Lightweight Device Class Fingerprinting for Web Clients." In *Proc. 6th Workshop on Security and Privacy in Smartphones and Mobile Devices (SPSM '16)*, pp. 93–102. ACM, 2016. DOI: 10.1145/2994459.2994467.

**[4]** P. Laperdrix, N. Bielova, B. Baudry, and G. Avoine. "Browser Fingerprinting: A Survey." *ACM Trans. Web*, Vol. 14, No. 2, Article 8, pp. 1–33, 2020. DOI: 10.1145/3386040.

**[5]** A. Davidson, J. Iyengar, and C. A. Wood. "The Privacy Pass Architecture." *RFC 9576*, IETF, June 2024. DOI: 10.17487/RFC9576.

**[6]** OpenAI. "Computer-Using Agent." OpenAI blog, January 23, 2025. URL: https://openai.com/index/computer-using-agent/.

**[7]** H. He, W. Yao, K. Ma, W. Yu, Y. Dai, H. Zhang, D. Cai, and D. S. Weld. "WebVoyager: Building an End-to-End Web Agent with Multimodal Models." In *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2024.

**[8]** S. Schrittwieser, S. Katzenbeisser, J. Kinder, G. Merzdovnik, and E. Weippl. "Protecting Software through Obfuscation: Can It Keep Pace with Progress in Code Analysis?" *ACM Comput. Surv.*, Vol. 49, No. 1, Article 4, pp. 1–37, 2016. DOI: 10.1145/2886012.

**[9]** B. Kreuter, T. Lepoint, M. Orrù, and M. Raykova. "Anonymous Tokens with Private Metadata Bit." In *Advances in Cryptology — CRYPTO 2020*, pp. 308–336. Springer, 2020. DOI: 10.1007/978-3-030-56784-2_11.

**[10]** H. Chu, K. Do, S. Faller, and L. Hanzlik. "On the Security of Rate-limited Privacy Pass." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2023. ePrint: 2023/1805.

**[11]** Cloudflare, Inc. "Cloudflare Collaborates With Leading Browsers to Develop a Privacy-First Protocol for the Global Internet." Press release, June 22, 2026. URL: https://www.cloudflare.com/press/press-releases/2026/cloudflare-collaborates-with-leading-browsers-to-develop-a-privacy-first-protocol-for-the-global-internet/.

**[12]** P. A. Grassi et al. "Digital Identity Guidelines." *NIST Special Publication 800-63-3*, 2017.

**[13]** OWASP Foundation. "Automated Threat Handbook." *OWASP Project*, 2018–2024. URL: https://owasp.org/www-project-automated-threats-to-web-applications/.

**[14]** X. Deng, Y. Gu, B. Zheng, S. Chen, S. Stevens, B. Wang, H. Sun, and Y. Su. "Mind2Web: Towards a Generalist Agent for the Web." In *Proc. Conference on Neural Information Processing Systems (NeurIPS)*, 2023.

**[15]** E. Bursztein, M. Martin, and J. C. Mitchell. "Text-based CAPTCHA Strengths and Weaknesses." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 125–138, 2011. DOI: 10.1145/2046707.2046724.

**[16]** M. Guerar, L. Verderame, M. Migliardi, F. Palmieri, and A. Merlo. "Gotta CAPTCHA 'Em All: A Survey of 20 Years of the Human-or-Computer Dilemma." *ACM Comput. Surv.*, Vol. 54, No. 9, Article 192, pp. 1–33, 2021. DOI: 10.1145/3477142.

**[17]** M. Motoyama, K. Levchenko, C. Kanich, D. McCoy, G. M. Voelker, and S. Savage. "Re: CAPTCHAs—Understanding CAPTCHA-Solving Services in an Economic Context." In *Proc. USENIX Security Symposium*, 2010.

**[18]** I. J. Goodfellow, Y. Bulatov, J. Ibarz, S. Arnoud, and V. Shet. "Multi-digit Number Recognition from Street View Imagery using Deep Convolutional Neural Networks." In *Proc. International Conference on Learning Representations (ICLR)*, 2014. arXiv:1312.6082.

**[19]** S. Sivakorn, I. Polakis, and A. D. Keromytis. "I Am Robot: (Deep) Learning to Break Semantic Image CAPTCHAs." In *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, 2016. DOI: 10.1109/EuroSP.2016.37.

**[20]** A. Searles, Y. Nakatsuka, E. Ozturk, A. Paverd, G. Tsudik, and A. Enkoji. "An Empirical Study & Evaluation of Modern CAPTCHAs." In *Proc. USENIX Security Symposium*, pp. 3081–3097, 2023. URL: https://www.usenix.org/conference/usenixsecurity23/presentation/searles.

**[21]** V. Shet. "Are You a Robot? Introducing 'No CAPTCHA reCAPTCHA'." *Google Security Blog*, December 3, 2014. URL: https://security.googleblog.com/2014/12/are-you-robot-introducing-no-captcha.html.

**[22]** Cloudflare, Inc. "Bot Management Technical Documentation." *Cloudflare Docs*, 2023–2024.

**[23]** A. Acien, A. Morales, J. Fierrez, R. Vera-Rodriguez, and O. Delgado-Mohatar. "BeCAPTCHA: Behavioral Bot Detection using Touchscreen and Mobile Sensors benchmarked on HuMIdb." *Engineering Applications of Artificial Intelligence*, Vol. 98, 104058, 2021. DOI: 10.1016/j.engappai.2020.104058.

**[24]** A. Acien, A. Morales, J. Fierrez, and R. Vera-Rodriguez. "BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection." *Pattern Recognition*, Vol. 127, 108643, 2022. DOI: 10.1016/j.patcog.2022.108643.

**[25]** H. Fereidooni et al. "AuthentiSense: A Scalable Behavioral Biometrics Authentication Scheme using Few-Shot Learning for Mobile Platforms." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.23194.

**[26]** WICG. "Private State Token API." *WICG Community Group Draft*. URL: https://wicg.github.io/trust-token-api/.

**[27]** D. Rubery and K. Monsen, Eds. "Device Bound Session Credentials (DBSC)." *W3C Web Application Security Working Group / WICG*, 2024. URL: https://w3c.github.io/webappsec-dbsc/.

**[28]** Google Chrome Security Team. "Fighting Cookie Theft Using Device Bound Sessions." *Chromium Blog*, 2 April 2024. URL: https://blog.google/chromium/fighting-cookie-theft-using-device/.

**[29]** X. Teoh, Y. Lin, S. Li, R. Liu, A. Sollomoni, Y. Harel, and J. S. Dong. "Are CAPTCHAs Still Bot-hard? Generalized Visual CAPTCHA Solving with Agentic Vision Language Model." In *Proc. USENIX Security Symposium*, 2025. URL: https://www.usenix.org/conference/usenixsecurity25/presentation/teoh.

**[30]** Y. Chen, H. Zhai, C. Wang, R. Yang, L. Zhang, G. Wang, et al. "CAPTCHA Solving for Native GUI Agents: Automated Reasoning-Action Data Generation and Self-Corrective Training." arXiv:2603.23559, 2026. URL: https://arxiv.org/abs/2603.23559.

**[31]** A. Gómez-Boix, P. Laperdrix, and B. Baudry. "Hiding in the Crowd: An Analysis of the Effectiveness of Browser Fingerprinting at Large Scale." In *Proc. The Web Conference (WWW)*, pp. 309–318, 2018. DOI: 10.1145/3178876.3186097.

**[32]** S. Wu, P. Sun, Y. Zhao, and Y. Cao. "Him of Many Faces: Characterizing Billion-scale Adversarial and Benign Browser Fingerprints on Commercial Websites." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.24394.

**[33]** N. Andriamilanto, T. Allard, G. Le Guelvouit, and A. Garel. "A Large-scale Empirical Analysis of Browser Fingerprints Properties for Web Authentication." *ACM Trans. Web*, Vol. 16, No. 1, Article 1, pp. 1–62, 2022. DOI: 10.1145/3478026.

**[34]** U. Iqbal, S. Englehardt, and Z. Shafiq. "Fingerprinting the Fingerprinters: Learning to Detect Browser Fingerprinting Behaviors." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00017.

**[35]** Z. Liu, P. Shrestha, and N. Saxena. "Gummy Browsers: Targeted Browser Spoofing against State-of-the-Art Fingerprinting Techniques." In *Proc. International Conference on Applied Cryptography and Network Security (ACNS)*, June 2022. arXiv: 2110.10129.

**[36]** N. Mathews, J. K. Holland, S. E. Oh, M. S. Rahman, N. Hopper, and M. Wright. "SoK: A Critical Evaluation of Efficient Website Fingerprinting Defenses." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2023. DOI: 10.1109/SP46215.2023.10179289.

**[37]** J. H. Saltzer and M. D. Schroeder. "The Protection of Information in Computer Systems." *Proc. IEEE*, Vol. 63, No. 9, pp. 1278–1308, 1975.

**[38]** X. Lin, P. Ilia, S. Solanki, and J. Polakis. "Phish in Sheep's Clothing: Exploring the Authentication Pitfalls of Browser Fingerprinting." In *Proc. USENIX Security Symposium*, 2022.

**[39]** J. Hodges, J.C. Jones, M.B. Jones, A. Kumar, and E. Lundberg, Eds. "Web Authentication: An API for Accessing Public Key Credentials, Level 2." *W3C Recommendation*, 8 April 2021. URL: https://www.w3.org/TR/2021/REC-webauthn-2-20210408/.

**[40]** A. Davidson, I. Goldberg, N. Sullivan, G. Tankersley, and F. Valsorda. "Privacy Pass: Bypassing Internet Challenges Anonymously." *Proc. on Privacy Enhancing Technologies (PoPETs)*, Vol. 2018, No. 3, pp. 164–180, 2018. DOI: 10.1515/popets-2018-0026.

**[41]** T. Pauly, S. Valdez, and C. A. Wood. "The Privacy Pass HTTP Authentication Scheme." *RFC 9577*, IETF, June 2024. DOI: 10.17487/RFC9577.

**[42]** S. Celi, A. Davidson, S. Valdez, and C. A. Wood. "Privacy Pass Issuance Protocols." *RFC 9578*, IETF, June 2024. DOI: 10.17487/RFC9578.

**[43]** antifraudcg/pact. "Design Proposal for PACT via ACTs with Aggregating Issuers." GitHub Issue #6, December 18, 2025. URL: https://github.com/antifraudcg/pact/issues/6

**[44]** K. Gupta. "PACT — Private Access Control Tokens: A Privacy-Preserving Trust Architecture for Humans and AI Agents on the Web." *krishnag.ceo*, June 2026. URL: https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/

**[45]** R. Anderson and T. Moore. "The Economics of Information Security." *Science*, Vol. 314, No. 5799, pp. 610–613, 2006. DOI: 10.1126/science.1130992.

**[46]** T. Moore. "The Economics of Cybersecurity: Principles and Policy Options." *Int. J. Crit. Infrastruct. Prot.*, Vol. 3, No. 3, pp. 103–117, 2010. DOI: 10.1016/j.ijcip.2010.10.002.

**[47]** R. Anderson et al. "Measuring the Cost of Cybercrime." In R. Böhme (Ed.), *The Economics of Information Security and Privacy*, pp. 265–300. Springer, 2013. DOI: 10.1007/978-3-642-39498-0_12.

**[48]** C. Herley and D. Florêncio. "Nobody Sells Gold for the Price of Silver: Dishonesty, Uncertainty and the Underground Economy." In *Proc. Workshop on the Economics of Information Security (WEIS)*, June 2009. Published in T. Moore, D. Pym, and C. Ioannidis (Eds.), *Economics of Information Security and Privacy*, pp. 33–53. Springer, 2010. DOI: 10.1007/978-1-4419-6967-5_3.

**[49]** K. Thomas, D. McCoy, C. Grier, A. Kolcz, and V. Paxson. "Trafficking Fraudulent Accounts: The Role of the Underground Market in Twitter Spam and Abuse." In *Proc. USENIX Security Symposium*, 2013.

**[50]** X. Li, B. A. Azad, A. Rahmati, and N. Nikiforakis. "Good Bot, Bad Bot: Characterizing Automated Browsing Activity." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00079.

**[51]** B. A. Azad, O. Starov, P. Laperdrix, and N. Nikiforakis. "Web Runner 2049: Evaluating Third-Party Anti-bot Services." In *Proc. DIMVA*, LNCS Vol. 12223, 2020. DOI: 10.1007/978-3-030-52683-2_7.

**[52]** H. Jonker, B. Krumnow, and G. Vlot. "Fingerprint Surface-Based Detection of Web Bot Detectors." In *Proc. ESORICS*, LNCS Vol. 11736, 2019. DOI: 10.1007/978-3-030-29962-0_28.

**[53]** A. Vastel, W. Rudametkin, R. Rouvoy, and X. Blanc. "FP-Crawlers: Studying the Resilience of Browser Fingerprinting to Block Crawlers." In *Proc. NDSS Workshop on Measurements, Attacks, and Defenses for the Web (MADWeb)*, 2020. DOI: 10.14722/madweb.2020.23010.

**[54]** S. Zhou et al. "WebArena: A Realistic Web Environment for Building Autonomous Agents." In *Proc. International Conference on Learning Representations (ICLR)*, 2024. arXiv:2307.13854.

**[55]** J. Y. Koh et al. "VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks." In *Proc. Annual Meeting of the Association for Computational Linguistics (ACL)*, 2024. arXiv:2401.13649.

**[56]** T. Xie et al. "OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments." In *Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track*, 2024. arXiv:2404.07972.

**[57]** Y. Zhang, T. Yu, and D. Yang. "Attacking Vision-Language Computer Agents via Pop-ups." In *Proc. 63rd Annual Meeting of the ACL (Long Papers)*, pp. 8387–8401, 2025. URL: https://aclanthology.org/2025.acl-long.411/.

**[58]** Z. Liao, L. Mo, C. Xu, M. Kang, J. Zhang, C. Xiao, Y. Tian, B. Li, and H. Sun. "EIA: Environmental Injection Attack on Generalist Web Agents for Privacy Leakage." In *Proc. International Conference on Learning Representations (ICLR)*, 2025. arXiv:2409.11295.

**[59]** A. Backman, J. Richer, and M. Sporny. "HTTP Message Signatures." *RFC 9421*, IETF, February 2024. DOI: 10.17487/RFC9421.

**[60]** IETF Web Bot Auth (webbotauth) Working Group. Charter and working documents. URL: https://datatracker.ietf.org/wg/webbotauth/about/.

**[61]** J. Bonneau, C. Herley, P. C. van Oorschot, and F. Stajano. "The Quest to Replace Passwords: A Framework for Comparative Evaluation of Web Authentication Schemes." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, pp. 553–567, 2012. DOI: 10.1109/SP.2012.44.

**[62]** T. Rokicki, C. Maurice, and P. Laperdrix. "SoK: In Search of Lost Time: A Review of JavaScript Timers in Browsers." In *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, 2021. DOI: 10.1109/EuroSP51992.2021.00039.

**[63]** K. Thomas et al. "Framing Dependencies Introduced by Underground Commoditization." In *Proc. Workshop on the Economics of Information Security (WEIS)*, 2015.

**[64]** Z. Wu, Y. Xue, Y. Feng, X. Wang, and Y. Song. "MCA-Bench: A Multimodal Benchmark for Evaluating CAPTCHA Robustness Against VLM-based Attacks." arXiv:2506.05982, 2025. URL: https://arxiv.org/abs/2506.05982.

**[65]** DataDome SAS. "Bot Detection and Mitigation Technical Overview." *Industry Documentation*, 2023.

**[66]** Kasada Pty Ltd. "Polymorphic Security Technical Documentation." *Industry Documentation*, 2023.

**[67]** B. A. Azad, O. Starov, P. Laperdrix, and N. Nikiforakis. "Taming the Shape Shifter: Detecting Anti-fingerprinting Browsers." In *Proc. DIMVA*, 2020.

**[68]** R. van Wegberg, B. Klievink, M. van Eeten, et al. "Plug and Prey? Measuring the Commoditization of Cybercrime via Online Anonymous Markets." In *Proc. USENIX Security Symposium*, pp. 1009–1026, 2018.

**[69]** H. Niu, J. Chen, Z. Zhang, and Z. Cai. "Mouse Dynamics Based Bot Detection Using Sequence Learning." In *Biometric Recognition (CCBR)*, LNCS Vol. 12878, pp. 49–56. Springer, 2021. DOI: 10.1007/978-3-030-86608-2_6.

**[70]** H. Niu, C. Cheng, and Z. Cai. "Learning Human Behavior for Bot Detection: A Perspective on Mouse Movement (MouseAgent)." In *Proc. China Automation Congress (CAC)*, pp. 6575–6580. IEEE, 2023. DOI: 10.1109/CAC59555.2023.10451138.

**[71]** C. Iliou, T. Kostoulas, T. Tsikrika, V. Katos, S. Vrochidis, and I. Kompatsiaris. "Detection of Advanced Web Bots by Combining Web Logs with Mouse Behavioural Biometrics." *Digital Threats: Research and Practice*, Vol. 2, No. 3, Article 24, pp. 1–26. ACM, 2021. DOI: 10.1145/3447815.

**[72]** S. Sadeghpour and N. Vlajic. "ReMouse Dataset: On the Efficacy of Measuring the Similarity of Human-Generated Trajectories for the Detection of Session-Replay Bots." *Journal of Cybersecurity and Privacy*, Vol. 3, No. 1, pp. 95–117. MDPI, 2023. DOI: 10.3390/jcp3010007.

**[73]** D. DeAlcala et al. "BeCAPTCHA-Type: Biometric Keystroke Data Generation for Improved Bot Detection." In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, pp. 1051–1060. IEEE, 2023. DOI: 10.1109/CVPRW59228.2023.00112.

**[74]** J. Caballero, C. Grier, C. Kreibich, and V. Paxson. "Measuring Pay-per-Install: The Commoditization of Malware Distribution." In *Proc. USENIX Security Symposium*, 2011.

**[75]** S. Pastrana, A. Hutchings, D. R. Thomas, and J. Tapiador. "Malware Finances and Operations: A Data-Driven Study of the Value Chain for Infections and Compromised Access." *arXiv:2306.15726*, 2023.

**[76]** S. Sivakorn, I. Polakis, and A. D. Keromytis. "I'm Not a Human: Breaking the Google reCAPTCHA." Black Hat Asia, 2016. White paper: https://www.blackhat.com/docs/asia-16/materials/asia-16-Sivakorn-Im-Not-a-Human-Breaking-the-Google-reCAPTCHA-wp.pdf

**[77]** dsekz. "botguard-reverse: Botguard full reverse." GitHub repository (write-up README), last commit 15 Sep 2025. https://github.com/dsekz/botguard-reverse  [grey literature]

**[78]** S. Shabat. "BotGuard-RE: Reverse engineering Google's BotGuard interstitial." GitHub repository, accessed 2026-09-23. https://github.com/shlomishabat/BotGuard-RE  [grey literature]

**[79]** Resoneo. "Google BotGuard Analysis / Analyse du système anti-bot de Google." Blog post, 2025 (accessed 2026-09-23). https://think.resoneo.com/botguard-google/  [grey literature, vendor/SEO blog]

**[80]** LuanRT. "BgUtils: Utility to generate PoTokens and run BotGuard attestation challenges." GitHub repository, accessed 2026-09-23. https://github.com/LuanRT/BgUtils  [grey literature]

**[81]** M. Schloegel et al. "Loki: Hardening Code Obfuscation Against Automated Attacks." In *Proc. USENIX Security Symposium*, pp. 3055–3073, 2022.

**[82]** L. Zheng, Z. Wang, D. Fu, Y. Zhang, Y. Lu, B. Dai, D. Song, K. He, and Y. Li. "SeeAct: GPT-4V(ision) is a Generalist Web Agent, if Grounded." In *Proc. International Conference on Machine Learning (ICML)*, 2024.

**[83]** W. Hong, W. Wang, Q. Lv, J. Xu, W. Yu, J. Ji, Y. Wang, Z. Wang, Y. Dong, M. Ding, and J. Tang. "CogAgent: A Visual Language Model for GUI Agents." In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 14281–14290, 2024. DOI: 10.1109/CVPR52733.2024.01354.

**[84]** K. Coogan, G. Lu, and S. Debray. "Deobfuscation of Virtualization-Obfuscated Software: A Semantics-Based Approach." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 275–284, 2011. DOI: 10.1145/2046707.2046739.

**[85]** P. Saxena, D. Akhawe, S. Hanna, F. Mao, S. McCamant, and D. Song. "A Symbolic Execution Framework for JavaScript." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, pp. 513–528, 2010.

**[86]** T. Blazytko, M. Contag, C. Aschermann, and T. Holz. "Syntia: Synthesizing the Semantics of Obfuscated Code." In *Proc. USENIX Security Symposium*, pp. 643–659, 2017.

**[87]** V. Raychev, M. Vechev, and A. Krause. "Predicting Program Properties from 'Big Code'." In *Proc. ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL)*, pp. 111–124, 2015. DOI: 10.1145/2676726.2677009.

**[88]** B. Rozière, M. Lachaux, L. Chanussot, and G. Lample. "DOBF: A Deobfuscation Pre-Training Objective for Programming Languages." In *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. 34, 2021. arXiv: 2102.07492.

**[89]** T. Laor et al. "DRAWNAPART: A Device Identification Technique based on Remote GPU Fingerprinting." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2022. DOI: 10.14722/ndss.2022.24093.

**[90]** B. Rudis. "PACT: The Open Web Doesn't Need Another Trust Oligopoly." *ai.rud.is*, June 23, 2026. URL: https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/

**[91]** X. Mi, X. Feng, X. Liao, B. Liu, X. Wang, F. Qian, Z. Li, S. Alrwais, L. Sun, and Y. Liu. "Resident Evil: Understanding Residential IP Proxy as a Dark Service." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2019. DOI: 10.1109/SP.2019.00011.

**[92]** T. Tarrach et al. "A Security and Usability Analysis of Local Attacks Against FIDO2." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2024.

**[93]** D. Kuchhal, M. Saad, A. Oest, and F. Li. "Evaluating the Security Posture of Real-World FIDO2 Deployments." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 2381–2395, 2023. DOI: 10.1145/3576915.3623063.

**[94]** OpenAI. "GPT-5" (model page: $1.25 input / $10.00 output per 1M tokens). *OpenAI API Documentation*. URL: https://developers.openai.com/api/docs/models/gpt-5. Accessed September 23, 2026.

**[95]** Google. "Gemini Developer API Pricing." URL: https://ai.google.dev/gemini-api/docs/pricing. Accessed September 23, 2026.

**[96]** Anthropic. "Pricing." *Claude Platform Docs*. URL: https://platform.claude.com/docs/en/about-claude/pricing. Accessed September 23, 2026.

**[97]** Bright Data. "Residential Proxies Pricing." URL: https://brightdata.com/pricing/proxy-network/residential-proxies. Accessed September 23, 2026.

**[98]** R. Abhyankar, Q. Qi, and Y. Zhang. "OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents." arXiv:2506.16042, 2025. URL: https://arxiv.org/abs/2506.16042.

**[99]** M. Motoyama, D. McCoy, K. Levchenko, S. Savage, and G. M. Voelker. "Dirty Jobs: The Role of Freelance Labor in Web Service Abuse." In *Proc. USENIX Security Symposium*, 2011.

**[100]** Multilogin. "Phone Farm Cost vs Cloud Phone Pricing." Vendor blog. https://multilogin.com/blog/phone-farm-cost-vs-cloud-phone-pricing/ (accessed 2026-09-23). Used for: 10-device farm monthly ops $93–$488 (proxy/SIM $5–$30/device/month).

**[101]** Amazon Web Services. "Amazon EC2 Mac Instances." https://aws.amazon.com/ec2/instance-types/mac/ (24-hour minimum allocation); price $0.65/h for mac2.metal via https://instances.vantage.sh/aws/ec2/mac2.metal (accessed 2026-09-23).

**[102]** Google Chrome Security Team. "Device Bound Session Credentials (DBSC)." *Chrome for Developers*, 2024. URL: https://developers.chrome.com/docs/web-platform/device-bound-session-credentials.

**[103]** D. Fett, B. Campbell, J. Bradley, T. Lodderstedt, M. Jones, and D. Waite. "OAuth 2.0 Demonstrating Proof of Possession (DPoP)." *RFC 9449*, IETF, September 2023. DOI: 10.17487/RFC9449.

**[104]** A. Côté Cyr. "Life on a Crooked RedLine: Analyzing the Infamous Infostealer's Backend." *ESET Research / WeLiveSecurity*, November 8, 2024. URL: https://www.welivesecurity.com/en/eset-research/life-crooked-redline-analyzing-infamous-infostealers-backend/.

**[105]** Microsoft Threat Intelligence. "Lumma Stealer: Breaking Down the Delivery Techniques and Capabilities of a Prolific Infostealer." *Microsoft Security Blog*, May 21, 2025. URL: https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/.

**[106]** J. Bonneau, C. Herley, P. C. van Oorschot, and F. Stajano. "Passwords and the Evolution of Imperfect Authentication." *Commun. ACM*, Vol. 58, No. 7, pp. 78–87, 2015. DOI: 10.1145/2699390.

**[107]** E. Ulqinaku, H. Assal, A. Abdou, S. Chiasson, and S. Capkun. "Is Real-time Phishing Eliminated with FIDO? Social Engineering Downgrade Attacks against FIDO Protocols." In *Proc. USENIX Security Symposium*, 2021.

**[108]** M. Kepkowski, L. Hanzlik, I. D. Wood, and M. A. Kaafar. "How Not to Handle Keys: Timing Attacks on FIDO Authenticator Privacy." In *Proc. Privacy Enhancing Technologies Symposium (PETS)*, Vol. 2022, No. 4, pp. 705–726, 2022. DOI: 10.56553/popets-2022-0129.

**[109]** M. Islam, S. S. Arora, R. Chatterjee, and K. C. Wang. "Detecting Compromise of Passkey Storage on the Cloud." In *Proc. USENIX Security Symposium*, pp. 7743–7762, 2025.

**[110]** A. Chavez. "Update on Plans for Privacy Sandbox Technologies." *Google Privacy Sandbox Blog*, October 17, 2025. URL: https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies.

**[111]** antifraudcg/pact. "Sketching an Architecture That Uses Issuer Blinding." GitHub Issue #1, December 18, 2025. URL: https://github.com/antifraudcg/pact/issues/1

**[112]** W3C Anti-Fraud Community Group. "antifraudcg/pact" (PACT design repository). GitHub, 2025–2026. URL: https://github.com/antifraudcg/pact.

**[113]** G. Stragapede, R. Vera-Rodriguez, R. Tolosana, and A. Morales. "BehavePassDB: Public Database for Mobile Behavioral Biometrics and Benchmark Evaluation." *Pattern Recognition*, 2022. DOI: 10.1016/j.patcog.2022.109089.

**[114]** Directive 2002/58/EC of the European Parliament and of the Council of 12 July 2002 (Directive on privacy and electronic communications), Art. 5(3), as amended by Directive 2009/136/EC. OJ L 201, 31.7.2002, p. 37.

**[115]** European Data Protection Board. "Guidelines 2/2023 on Technical Scope of Art. 5(3) of ePrivacy Directive." Version 2.0, adopted October 7, 2024. URL: https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-22023-technical-scope-art-53-eprivacy-directive_en.

**[116]** Regulation (EU) 2016/679 (General Data Protection Regulation), Art. 6(1)(f) and Recital 49. OJ L 119, 4.5.2016, p. 1.

**[117]** Regulation (EU) 2022/1925 (Digital Markets Act), Art. 6(7). OJ L 265, 12.10.2022, p. 1.
