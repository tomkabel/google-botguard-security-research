# The Economics of Architectural Ceilings in Client-Side Anti-Automation

## A Cost-to-Bypass Analysis of Google's Botguard Virtual Machine

---

**Author:** Abel, T. K.

**Repository:** https://github.com/tomkabel/google-botguard-security-research

**Keywords:** Client-side attestation, Botguard, JavaScript virtual machine, bearer token portability, environmental spoofing, cost-to-bypass economics, anti-tamper layering, stateful telemetry, non-linear scaling penalties

---

## Abstract

Client-side anti-automation systems impose economic costs on adversaries through two structurally distinct mechanisms: **per-execution infrastructure costs** (stateless VM defenses like Botguard) and **profile-aging inventory costs** (stateful telemetry engines like reCAPTCHA v3). The adversary controls the execution substrate and every environmental measurement collected within it: **this is a forgery problem, not a cryptanalysis problem.** No software-only defense escapes this architectural fact. This paper formalizes both cost structures using Google's Botguard JavaScript Virtual Machine as a case study for the stateless paradigm. We propose an **anti-tamper layering framework** that decomposes stateless execution-time defenses into four measurable layers (environmental introspection, self-modifying code, anti-logger traps, chronometric integrity) and derive a **per-token cost model** whose linear assumptions fail at industrial throughput due to **Non-Linear Scaling Penalties (NLSP)** — subnet-level reputation cascades, premium proxy cost escalation, and superlinear infrastructure overhead. We formalize the non-linearity through cost component functions of adversary volume $V$, modeling the reputation failure rate $r(V)$ as a logistic function and demonstrating that the marginal cost $MC(V)$ increases convexly as the adversary exhausts the supply of cheap commodity IPs. The paper's central contribution is the economic formalization of the structural ceiling inherent to software-only attestation. We extend the analysis to stateful telemetry, showing that profile-aging costs introduce a time-to-production constraint that complements, but does not replace, the per-execution costs of stateless defenses.

**Contributions:**
1. The anti-tamper layering framework (L1–L4) for evaluating stateless execution-time client-side defenses (Botguard, Cloudflare Turnstile)
2. A formal economic model of the per-token cost function $C(V)$ as an increasing convex function of adversary throughput, with explicit marginal cost derivation and identification of the three NLSP mechanisms that drive superlinearity
3. An economic model of stateful telemetry profile-aging costs ($C_{aging}$), demonstrating why the stateless and stateful paradigms impose fundamentally different cost functions
4. A three-regime formalization of the economic ceiling, identifying the adversary scale at which each cost component becomes the binding constraint

---

## 1. Introduction

### 1.1 Motivation

Google's Botguard system is among the most sophisticated software-only client-side anti-automation mechanisms deployed in production. It is a custom, register-based Virtual Machine written entirely in JavaScript that executes encrypted bytecode, implements self-modifying opcodes, and enforces chronometric anti-tamper defenses.

The principle that anti-automation operates by raising the adversary's compute and infrastructure costs until attacks become economically unviable is well-established in industry. Major anti-bot providers — Cloudflare, Human Security (formerly PerimeterX), Kasada, and DataDome — explicitly design their defenses around this economic model. This paper's contribution is not the discovery of this principle but its formalization into a structured, measurable framework.

### 1.2 Central Thesis

1. **Two distinct economic ceilings govern software-only client-side anti-automation.** Stateless defenses (Botguard, Turnstile) impose per-execution infrastructure costs. Stateful defenses (reCAPTCHA v3) impose profile-aging inventory costs. These ceilings are complementary but non-substitutable.
2. **The architectural ceiling is structural, not an implementation failure.** The bypass is a forgery problem — presenting environmental and temporal parameters consistent with legitimate execution — not a cryptanalysis problem.
3. **The anti-tamper layering framework (L1–L4) provides a formal vocabulary for measuring and comparing bypass costs.**

### 1.3 Research Contributions

- **Anti-Tamper Layering Framework (Section 3):** Decomposition of stateless execution-time defenses into four discrete layers with measurable bypass costs.
- **Per-Token Cost Model and NLSP Analysis (Section 3.6):** A formal cost function of adversary volume $V$ with logistic failure rate $r_{failure}(V)$, stepwise proxy pricing $p(V)$, and marginal cost analysis showing convexity driven by three NLSP mechanisms.
- **Stateful Telemetry Economic Model (Section 3.5.1):** Formalization of the profile-aging cost ($C_{aging}$) showing fundamentally different cost functions between paradigms.
- **Economic Formalization of the Architectural Ceiling (Section 3.7):** A three-regime model identifying where each cost component becomes the binding constraint, with the ceiling expressed as the solution to $C_{token}(V) = R_{token}$.

### 1.4 Axiomatic Foundation: Threat Model Boundaries

The analysis is organized around three architecturally distinct threat models (well-established in IAM literature, NIST SP 800-63) that serve as the axiomatic lens through which the novel economic analysis is conducted:

| Threat Model | Defense Class | Hardware Required? | Authentication Required? |
|---|---|---|---|
| **Automated Abuse** | Probabilistic anti-automation (Botguard, reCAPTCHA) | No | No |
| **Session Hijacking** | Hardware-anchored session binding (DBSC) | Yes | Yes (session established) |
| **Credential Phishing** | Hardware-enrolled authentication (Passkeys, WebAuthn) | Yes | Yes (enrollment required) |

### 1.5 Scope and Limitations

This analysis integrates reverse-engineering intelligence (Botguard VM architecture, YouTube PO token system, automated token-harvesting pipeline). These are operational artifacts, not formal publications; they are listed in the Replication Package appendix. A small-scale PoC experiment (20 IPs, 500 tokens, 24h) was conducted as a feasibility check and is reported in Appendix C.

---

## 2. Background and Related Work

### 2.1 Probabilistic Bot Mitigation vs. Deterministic Identity Authentication

Deterministic identity authentication (FIDO2/WebAuthn) proves possession of a cryptographic key housed in a hardware authenticator. Security is binary and requires prior enrollment (NIST SP 800-63).

Probabilistic bot mitigation (Botguard) produces a scalar confidence score about whether the execution environment resembles a legitimate browser. It operates on anonymous traffic and cannot require hardware possession.

This distinction is well-understood in both academic literature (Bonneau et al. 2015, Bursztein et al. 2012) and industry practice (Cloudflare 2023, Human Security 2022).

### 2.2 JavaScript Obfuscation and VM-Based Defenses

Botguard's register-based VM defines an entirely new instruction set executed by a custom interpreter — a technique adapted from native-code protectors (VMProtect, Themida) to the browser context. Opcodes include arithmetic (328/USHR, 381/ADD), property manipulation (65/SETPROP, 467/GETPROP), environment introspection (220/IN), and halting operations (289/HALT).

### 2.3 Bearer Token Semantics and Botguard

The `bgRequest` and Proof of Origin (PO) tokens generated by the Botguard VM function as bearer tokens (RFC 6750, RFC 7519). The server validates internal integrity but cannot cryptographically bind the token to a specific presenter in the absence of proof-of-possession mechanisms (RFC 8471, RFC 9449).

### 2.4 Related Adversarial Techniques

The token-harvesting pipeline belongs to the class of reverse-proxy phishing attacks (Callegati et al. 2009, EvilGinx). Industry analyses of proxy economics document the pricing stratification (commodity pools at $0.50/GB vs. premium unburned IPs at $10–15/GB) that drives the non-linear cost model.

---

## 3. The Anti-Tamper Layering Framework

### 3.1 Framework Definition

1. **Layer identification:** Decompose the defense into distinct anti-tamper mechanisms.
2. **Cost measurement per layer:** Engineering hours (initial + maintenance), infrastructure cost per bypass, failure rate.
3. **Total cost computation:** Sum of layer costs, weighted by dependency.
4. **Economic viability assessment:** Compare total cost-to-bypass against the value of the protected resource.

### 3.2 Botguard's Four Defensive Layers

**L1 — Environmental Introspection.** Detects headless browser automation via `navigator.webdriver`, WebGL rendering artifacts, and DOM prototype chain integrity. Standard headless Chrome leaks 15–20 detectable properties.

**L2 — Self-Modifying Code.** Register 274 constructs the opcode array at runtime. `LOADSTRING` and `LOADOP` (EVAL) inject new instructions dynamically, preventing static disassembly.

**L3 — Anti-Logger Trap.** Console methods are bound to trap functions via `t.prototype` stack manipulation. Logging any variable corrupts the instruction stream.

**L4 — Chronometric Defense.** The VM continuously polls `performance.now()` and `Date.now()`. The time delta mutates a seed value (`K.U`) that determines the bytecode decryption key. Deviations of ~50–200ms trigger invalid token generation.

### 3.3 Operational Cost Estimates

**Adversary Capability Model.** The following estimates assume an adversary with Senior Security Engineer proficiency — an individual fluent in V8 internals, headless Chrome instrumentation (Puppeteer/CDP), and JavaScript VM analysis. This skill profile corresponds to a professional reverse engineer working in either an advanced-persistent-threat (APT) team or a specialized automation-as-a-service operation. Hour estimates are heuristically calibrated from the author's own Botguard reverse-engineering cycle (Appendix B) and industry-typical sprint cadences for comparable browser-automation tooling development.

| Layer | Initial Engineering | Monthly Maintenance | Subversion Approach |
|---|---|---|---|
| L1: Environmental | 40–60 hours | 10–20 hours | Override navigator.webdriver, mask UA, spoof WebGL |
| L2: Self-Modifying Code | 20–30 hours | 0 hours | Dynamic tracing w/o triggering L3 |
| L3: Anti-Logger Trap | 15–25 hours | 5–10 hours | Restore console after VM init |
| L4: Chronometric | 30–50 hours | 15–25 hours | Override performance.now()/Date.now() |

These estimates are not empirical measurements but engineering heuristics; they serve as order-of-magnitude baselines for the economic model rather than precise predictions. An APT team with zero-day infrastructure may halve these figures; a solo operator without prior VM-analysis experience may double them.

### 3.5 Framework Scope and Boundaries

The L1–L4 framework models **stateless, execution-time defenses**. Cloudflare Turnstile maps cleanly (single L1 layer). Stateful telemetry engines operate on a different principle.

#### Stateful Telemetry Engines: A Complementary Paradigm

In a stateless defense (Botguard), the adversary's cost is incurred per token. In a stateful defense (reCAPTCHA v3), each browser profile accumulates a behavioral history that introduces a **profile-aging cost**:

C_stateful = C_aging + C_token

Where C_aging represents:
- **Time cost:** 2–6 weeks of gradual, human-like browsing before favorable risk scoring
- **Inventory cost:** Each aged profile is a limited-use asset; scaling multiplies costs linearly
- **Maintenance cost:** Automated activity patterns reset the aging clock

**Comparison.** Stateless models minimize C_token with immediate production; stateful models face a delay-to-production constraint that cannot be bypassed by spending more on per-token infrastructure. These are two distinct economic ceilings.

### 3.6 Per-Token Cost Model: Formal Economic Analysis

The adversary's objective is to maximize token throughput $V$ (tokens/day) subject to a budget constraint. The cost per token is not a scalar constant but an increasing function of $V$, governed by three supply constraints that tighten at scale.

#### 3.6.1 Cost Components as Functions of Volume

We express each cost component as a function of daily token output $V$:

$C_{token}(V) = \big(C_{browser}(V) + C_{IP}(V) + C_{stealth}(V)\big) \times \dfrac{1}{1 - r_{failure}(V)}$

Where each term is defined as follows:

**Browser Infrastructure Cost: $C_{browser}(V)$**

Execution of the Botguard VM requires a headless Chromium instance per concurrent token request. Infrastructure cost scales with the number of concurrent instances $n_{instances} = V / k_{throughput}$, where $k_{throughput}$ is the token-per-instance-per-day throughput (approximately 800–1,200 tokens/instance/day in our PoC; varies with VM compile complexity). For small $V$, overhead is linear. For large $V$, multi-datacenter orchestration, instance health monitoring, VM compile rotation, and session pool management introduce superlinear growth:

$C_{browser}(V) = c_0 \cdot \dfrac{V}{k_{throughput}} + c_1 \cdot \left(\dfrac{V}{k_{throughput}}\right)^2$

The quadratic term $c_1$ captures coordination overhead: at ~1,200 concurrent instances (the approximate requirement for $V = 1\text{M}$ tokens/day), the operational burden of instance lifecycle management, crash recovery, and compile-variant scheduling grows faster than linearly.

**IP Proxy Cost: $C_{IP}(V)$**

Residential proxy markets exhibit tiered pricing that creates a stepwise cost function [2.4]. At low volume ($V < 10\text{K}$ tokens/day), the adversary can operate within a single pricing tier using commodity residential pools at the base rate $p_{base}$ (e.g., $\sim$$0.50$/GB as of 2023). As volume increases:

$C_{IP}(V) = p(V) \cdot b_{data} \cdot V$

Where $b_{data}$ is bandwidth consumed per token execution (~0.5–2 MB including Botguard bytecode download) and $p(V)$ is the effective price per GB:

$p(V) = \begin{cases} p_{base} & V \leq V_{tier1} \\ p_{mid} & V_{tier1} < V \leq V_{tier2} \\ p_{premium} & V > V_{tier2} \end{cases}$

Published proxy market pricing shows a $20\times$–$30\times$ spread between commodity and premium residential tiers [Industry]. As subnet exhaustion forces the adversary upward through these tiers, the effective IP cost per token jumps discontinuously.

**Stealth Maintenance Cost: $C_{stealth}(V)$**

Stealth cost captures the engineering effort required to adapt subversion techniques as the Botguard VM compile rotates. Google deploys new bytecode compiles on an irregular schedule. Each compile rotation requires re-analysis of opcode changes and environmental checks:

$C_{stealth}(V) = c_s \cdot \dfrac{V}{T_{compile\_life}}$

Where $T_{compile\_life}$ is the average lifetime of a Botguard compile before rotation, and $c_s$ is the engineering cost per adaptation cycle. This component is linear in $V$ but variable in time, introducing stochastic cost spikes.

#### 3.6.2 The Reputation Failure Rate as a Logistic Function

The failure rate $r_{failure}$ is the proportion of token-generation attempts that the server-side verifier rejects. At PoC scale, this is well-modeled as constant. At industrial scale, subnet-level reputation burns drive it upward as a function of volume:

$r_{failure}(V) = r_0 + \dfrac{r_{max} - r_0}{1 + e^{-k(V - V_{0.5})}}$

Where:
- $r_0$ is the baseline failure rate at low volume (observed ~0.15–0.30 in our PoC, Appendix C)
- $r_{max}$ is the asymptotic maximum failure rate approached as reputation burn saturates all available subnets
- $V_{0.5}$ is the volume at which the failure rate reaches its midpoint (the "reputation saturation threshold")
- $k$ is the steepness parameter reflecting how aggressively the server-side reputation system cascades burns

At low-to-medium volume ($V \ll V_{0.5}$), $r_{failure}(V) \approx r_0$ and the model is linear. At high volume ($V \gg V_{0.5}$), $r_{failure}(V) \to r_{max}$, which may approach values above 0.90 [2.4].

The term $\frac{1}{1 - r_{failure}(V)}$ acts as a **multiplier** on all other cost components. As $r_{failure} \to 1$, this multiplier diverges, representing the point where no finite infrastructure budget can sustain throughput — the structural economic ceiling.

#### 3.6.3 Marginal Cost Analysis

The marginal cost per additional token is the derivative of total cost with respect to volume:

$MC(V) = \dfrac{d}{dV}C_{token}(V)$

$MC(V) = \dfrac{1}{1 - r_{failure}(V)} \cdot \left[\dfrac{dC_{browser}}{dV} + \dfrac{dC_{IP}}{dV} + \dfrac{dC_{stealth}}{dV}\right] + \dfrac{C_{browser}(V) + C_{IP}(V) + C_{stealth}(V)}{(1 - r_{failure}(V))^2} \cdot \dfrac{dr_{failure}}{dV}$

The second term, containing $\frac{dr_{failure}}{dV}$, is the **NLSP amplification term**. It captures the compound effect: as $r_{failure}$ rises with volume, not only does each token cost more, but the *rate at which costs increase per additional token* (the marginal cost) also accelerates. This is the mathematical expression of why linear cost models systematically underestimate costs at scale.

Three specific mechanisms drive the convexity of $MC(V)$:
1. **Subnet-level reputation burn** — modeled through $r_{failure}(V)$ as a logistic function approaching $r_{max}$
2. **Premium proxy cost escalation** — modeled through the step function $p(V)$ as the adversary exhausts commodity pricing tiers
3. **Superlinear infrastructure overhead** — modeled through the quadratic term in $C_{browser}(V)$, capturing multi-instance coordination costs

#### 3.6.4 Scalability Constraint Formalism

The adversary faces a maximum feasible volume $V_{max}$ determined by the convergence of these cost components. $V_{max}$ is the solution to:

$\dfrac{C_{token}(V_{max})}{R_{token}} = 1$

Where $R_{token}$ is the economic value per token to the adversary (e.g., ad impression revenue, search position lift). When $C_{token}(V) > R_{token}$, the attack is net-negative and unsustainable. The shape of $C_{token}(V)$ — convex and increasing — ensures a finite $V_{max}$ exists. This is the **formal definition of the architectural economic ceiling**.

### 3.7 The Economic Ceiling: Three Regimes

The cost function $C_{token}(V)$ exhibits three qualitatively distinct regimes, each characterized by which NLSP component dominates the marginal cost:

| Regime | Volume ($V$) | Dominant Cost Component | Effective Cost Multiplier |
|---|---|---|---|
| **PoC scale** | $V < 10^4$ tokens/day | $C_{IP}$ (linear) | Baseline ($\alpha = 1$) |
| **Low-to-medium industrial** | $10^4 < V < 10^5$ tokens/day | $C_{IP}$ (tier transition) + $r_{failure}$ (early logistic rise) | $3\alpha$ to $10\alpha$ |
| **High industrial** | $V > 10^6$ tokens/day | $r_{failure}$ (asymptotic approach to $r_{max}$) + $C_{browser}$ (quadratic term dominance) | $10\alpha$ to $50\alpha$ |

At PoC scale, the cost multiplier is close to the baseline: the adversary operates within a single proxy pricing tier ($p(V) = p_{base}$) and subnet reputation burns are minimal ($r_{failure}(V) \approx r_0$).

At low-to-medium industrial scale ($10^4$–$10^5$ tokens/day), the adversary begins exhausting commodity proxy tier supply ($p(V)$ transitions toward $p_{mid}$), and early reputation effects push $r_{failure}(V)$ above its baseline. The effective per-token cost rises to $3\times$–$10\times$ the PoC baseline.

At high industrial scale ($V > 10^6$ tokens/day), the premium proxy tier becomes unavoidable ($p(V) \to p_{premium}$), coordination overhead in $C_{browser}(V)$ amplifies, and $r_{failure}(V)$ converges toward $r_{max}$ — driving the failure multiplier $\frac{1}{1 - r_{failure}(V)}$ toward infinity. The effective per-token cost reaches $10\times$ to $50\times$ the PoC baseline. At this point, $C_{token}(V)$ exceeds any plausible per-token economic value $R_{token}$, and the defense reaches its **structural economic ceiling**.

The ceiling shape is sublinear in defense investment (adding obfuscation layers raises engineering costs linearly but does not alter the convexity of $C_{token}(V)$) and superlinear in adversary throughput (the NLSP mechanisms compound). This asymmetry — linear investment produces superlinear cost escalation for the adversary — is the economic property that distinguishes software-only anti-automation from cryptographic defenses.

---

## 4. Operational Constraints and Multipliers

The per-token cost model of Section 3.6 captures the cost per unit of adversary output. Three additional operational constraints modulate the relationship between cost and throughput, acting as discrete cost multipliers that compound the NLSP effects at scale.

### 4.1 Token-Harvesting Economics

Automated token generation faces three interacting operational constraints:

**IP Reputation Burn Dominance.** The server-side verifier's subnet reputation model is the dominant operational constraint. Unlike bandwidth or compute, reputation is an exhaustible shared resource: a single high-volume operator on a subnet degrades quality for all other operators sharing that same IP range. The resulting "tragedy of the commons" dynamic means that $r_{failure}(V)$ in the formal model (Section 3.6.2) rises not only with the adversary's own volume but with aggregate volume across all competing adversaries on the same residential proxy pools. This makes the effective failure rate a function of broader proxy-market equilibrium, not merely individual throughput.

**Latency-Induced Infrastructure Amplification.** Each VM execution consumes 2–5 seconds of Chromium instance time (compile-dependent). Server-side timeouts at 5–10 seconds create a hard per-token latency window. At scale, latency variance inflates the required concurrent Chromium instance count beyond the theoretical minimum: to sustain $V$ tokens/day with mean execution time $\mu$ and variance $\sigma^2$, the adversary must provision $n \geq \frac{V \cdot (\mu + z \cdot \sigma)}{T_{day}}$ instances to absorb the tail, where $z$ is the safety factor for timeout avoidance. This variance multiplier feeds directly into the quadratic term of $C_{browser}(V)$.

**Token Freshness and Batch Elimination.** Botguard tokens embed server-side timestamps that enforce freshness windows (typically 30–120 seconds for bgRequest tokens; variable for PO tokens). This eliminates batch-generation strategies: the adversary cannot produce a stockpile of tokens during off-peak hours and consume them later. Token generation must be **online and time-synchronized**, forcing the infrastructure cost $C_{browser}(V)$ to be sustained continuously rather than amortized over bursts.

### 4.2 Per-Request Cost Multiplication: YouTube Proof of Origin (PO) Tokens

YouTube's PO token system introduces a distinct cost multiplier that compounds the per-token model. Each PO token is bound to a specific Video ID (`v` parameter), transforming token generation from a resource that scales with the adversary's own infrastructure alone into one that scales with **target content volume**.

In the YouTube context, the adversary's effective cost function becomes:

$C_{effective} = C_{token} \times N_{videos}$

Where $N_{videos}$ is the number of distinct videos targeted. This is a **per-request multiplication** effect: even if the per-token cost $C_{token}$ is held constant, the adversary's total cost scales linearly with the breadth of content targeted. For adversaries targeting YouTube at industrial scale — e.g., view-count manipulation across tens of thousands of videos — this multiplier alone can render the attack economically non-viable independently of NLSP effects.

When combined with NLSP at high throughput, the effective cost per video is:

$C_{per\_video}(V, N) = C_{token}(V) \cdot N$

Where $C_{token}(V)$ is already superlinear in $V$. The joint effect — superlinear per-token cost multiplied by linear content breadth — creates a **bilinear cost surface** that systematically constrains both depth (volume per target) and breadth (number of targets) of automation.

### 4.3 Formalizing the Architectural Ceiling

The adversary controls the execution substrate. The JavaScript environment, the DOM, the timer APIs — every "measurement" the VM takes of its environment is a measurement of data the adversary can observe and intercept. An anti-tamper layer can raise the cost of interception, but it cannot change the structural fact that the defended software executes in an environment the adversary owns.

This is why software-only attestation is architecturally bounded. The defender can increase engineering complexity (additional VM opcodes, deeper chronometric checks, more aggressive compile rotation), but each increment raises the adversary's cost **linearly** ($C_{stealth}(V)$ as a function of compile rotation frequency) while the defense's own complexity cost also grows linearly. The structural ceiling — where $C_{token}(V) = R_{token}$ — remains an economic phenomenon, not a cryptographic one.

The distinction between a **forgery problem** and a **cryptanalysis problem** captures this essential asymmetry:
- In cryptanalysis, the defender controls the key material; the attacker faces a mathematical barrier.
- In client-side attestation forgery, the defender controls the execution specification; the attacker controls the execution itself.

No amount of VM-complexity layering changes the paradigm from the latter to the former. As stated in the Abstract: **this is a forgery problem, not a cryptanalysis problem.** The economics of anti-automation — the raising of forgery costs to unprofitable levels — is the only viable defense within this structural constraint.

---

## 5. Generalization and Industry Trajectory

- Complexity does not equal security
- Temporal integrity requires a hardware anchor
- Bearer token portability is an architectural property
- Attestation must be remote-verifiable

### DBSC and Passkeys

DBSC and Passkeys address session hijacking and credential phishing respectively. Both are inapplicable to anonymous traffic screening — this follows directly from IAM principles (NIST SP 800-63). The economic contribution is the **formalization** of why these mechanisms are non-substitutable for the automated-abuse threat model.

---

## 6. Conclusions

### Two Economic Ceilings, One Structural Principle

Client-side anti-automation imposes cost through two structurally distinct mechanisms: per-execution infrastructure cost (stateless) and profile-aging inventory cost (stateful). Both are bounded by the adversary's cost structure, not the defender's engineering.

**Key Findings:**
1. Botguard is operationally effective within its design envelope. NLSP raise cost at scale, but high-value targets remain viable.
2. The L1–L4 framework models stateless defenses. Stateful telemetry introduces a distinct, complementary cost structure.
3. Chronometric defenses (L4) are structurally subvertible but economically effective.
4. The economic ceiling is infrastructure-bound, not complexity-bound.

**For Defenders:** Invest in IP reputation analysis and rate limiting. Consider stateful + stateless as complementary. Software-only anti-automation provides economic deterrence, not cryptographic guarantees.

**Future Work:** 1,000+ residential IPs, 90+ day measurement window, multiple Botguard compiles, empirical measurement of stateful aging curves, stateless vs. stateful comparative measurement.

---

## Appendices

- **Appendix A: Statistical Power Analysis** — N=20 IPs is insufficient for statistical inference
- **Appendix B: Replication Package** — go-rod pipeline, Cypa's botguard-reverse, LuanRT's BgUtils
- **Appendix C: Preliminary PoC Data** — Full experimental results (20 IPs, 500 tokens, 24h)

---

## References

### Academic
- Saltzer, J. H. and Schroeder, M. D. (1975). The Protection of Information in Computer Systems.
- Schrittwieser, S. et al. (2016). Protecting Software through Obfuscation. ACM Comput. Surv.
- Callegati, F., Cerroni, W., and Ramilli, M. (2009). Man-in-the-Middle Attack to the HTTPS Protocol. IEEE S&P.
- Guerar, M. et al. (2021). Gotta CAPTCHA 'Em All. ACM Comput. Surv.
- Bursztein, E. et al. (2012). Text-based CAPTCHA Strengths and Weaknesses. ACM CCS.
- Bonneau, J. et al. (2015). Passwords and the Evolution of Imperfect Authentication. Commun. ACM.
- Ulqinaku, E. et al. (2021). Is Real-time Phishing Eliminated with FIDO? USENIX Security.
- Laperdrix, P. et al. (2020). Browser Fingerprinting: A Survey. ACM Trans. Web.

### Standards
- FIDO Alliance. (2021). WebAuthn Level 2. W3C.
- Grassi, P. A. et al. (2017). Digital Identity Guidelines. NIST SP 800-63-3.
- RFC 8471: Token Binding Protocol v1.0
- RFC 6750: OAuth 2.0 Bearer Token Usage
- RFC 7519: JSON Web Token
- RFC 9449: OAuth 2.0 DPoP

### Industry
- Cloudflare, Inc. (2023). Bot Management Technical Documentation.
- Human Security, Inc. (2022). The Economics of Bot Mitigation.
- Kasada Pty Ltd. (2023). Polymorphic Security Technical Documentation.
- DataDome SAS. (2023). Bot Detection and Mitigation Technical Overview.
- Google Chrome Security Team. (2024). Device Bound Session Credentials (DBSC).
- EvilGinx: Standalone MITM Attack Framework (Gretzky, 2017).
- Residential Proxy Market Pricing and Subnet Reputation Dynamics (2023).
- Bright Data (formerly Luminati). Residential Proxy Network Pricing Structure, 2023–2024.
- Oxylabs. Residential Proxy Tier Pricing and Pool Exhaustion Dynamics, 2023.
- Imperva (2023). Bad Bot Report: The Economics of Automated Traffic.
- Netacea (2022). The Bot Management Review: Cost Analysis of Automated Attacks.
- Distil Networks (2020). Bot Economics: A Cost-Benefit Analysis of Bot Attacks.

### Economic Methodology
- Varian, H. R. (2014). Intermediate Microeconomics: A Modern Approach (9th ed.). W. W. Norton. — Marginal cost analysis and production functions in industrial organization.
- Moore, T. (2010). The Economics of Cybersecurity: Principles and Policy Options. Int. J. Crit. Infrastruct. Prot. 3(3–4), 103–117.
- Anderson, R. and Moore, T. (2006). The Economics of Information Security. Science, 314(5799), 610–613.
- Herley, C. and Florêncio, D. (2010). Nobody Sells Gold for the Price of Silver: Dishonesty, Uncertainty and the Underground Economy. WEIS.

---

*This document is for educational and research purposes only.*
