# Kits Kärneriks: The Inherent Fragility of Client-Side Trust

## A Systematization of Knowledge on Browser-Based Attestation via the Botguard Virtual Machine and the Puppet Strategy

---

**Author:** Abel, T. K. (2021)

**Repository:** https://github.com/tomkabel/google-botguard-security-research

**Keywords:** Client-side attestation, Botguard, JavaScript VM, token portability, environmental spoofing, remote attestation, WebAuthn, Proof of Origin tokens

---

## Abstract

This Systematization of Knowledge (SoK) examines Google's Botguard JavaScript Virtual Machine as a canonical case study in the inherent fragility of client-side trust. Botguard—a register-based, self-modifying VM executing encrypted bytecode within the browser sandbox—represents a ceiling for software-only attestation mechanisms. This work integrates three research contributions: (1) the original "Puppet" bypass strategy, which demonstrates that client-generated security tokens can be extracted from a compliant browser environment and trafficked to a Man-in-the-Middle phishing context, decoupling token generation from token usage; (2) Cypa's reverse engineering of Botguard's VM architecture, opcode classification, chronometric anti-debug defenses, and encrypted memory reader function; and (3) LuanRT's analysis of YouTube's Proof of Origin (PO) Token system, documenting multi-layer challenge initialization, integrity token retrieval, and StreamProtectionStatus enforcement. The central thesis is that software-only client-side attestation is architecturally incapable of proving the absence of an adversary, because every computational step executes on adversary-controlled hardware. A Taxonomy of Attestation Rigor is constructed comparing hardware-backed (TEE/WebAuthn) and software-only (obfuscated VM) approaches across seven dimensions, establishing that "Sole Control" is technically unverifiable for the latter category. The findings generalize to all forms of remote attestation: without a hardware root of trust, the Relying Party cannot distinguish a legitimate user from a sufficiently advanced emulator.

---

## 1. Introduction

Modern web authentication rests on a paradox: the entity being verified is also the entity performing the verification. When a browser executes a security script, validates a runtime environment, and generates an attestation token, all of these operations occur on a machine over which the Relying Party has no administrative authority. The operator of that machine—whether a legitimate user or a threat actor—controls the operating system, the browser process, the network stack, and the memory space in which the security logic executes. This foundational asymmetry, termed here the **Client-Side Trust Paradox**, is the central subject of the present Systematization of Knowledge (SoK).

This work examines Google's **Botguard** system as a canonical case study of software-only client-side attestation. Botguard is not, as casual observers have characterized it, a fingerprinting script. It is a custom, register-based Virtual Machine written entirely in JavaScript that executes encrypted bytecode, implements self-modifying opcodes, and enforces chronometric anti-tamper defenses via continuous polling of `performance.now()` and `Date.now()` \cite{abel2021}. The VM emulates a modern CPU within the browser sandbox, maintaining register state, a rolling encryption key (Register 21), a position tracker (Z.W), and a time-mutating seed (Z.U) that collectively resist static and dynamic analysis \cite{abel2021,cypa}. This complexity has led to the common characterization of Botguard as a "hostile, obfuscated Virtual Machine running directly in the client's browser" \cite{abel2021}.

The research corpus integrated here comprises three distinct contributions: (1) the original **Puppet** bypass strategy—a proof-of-concept demonstrating that Botguard-generated tokens can be extracted from a compliant browser environment and trafficked to a Man-in-the-Middle (MITM) phishing context \cite{abel2021}; (2) the reverse engineering of Botguard's VM architecture and anti-tamper mechanisms by Cypa (@dsekz), including opcode classification and the memory reader function analysis \cite{cypa}; and (3) LuanRT's analysis of the Proof of Origin (PO) Token system used by YouTube, documenting the multi-layer challenge initialization, integrity token retrieval, and StreamProtectionStatus (sps) enforcement mechanism \cite{luanrt}.

The central argument advanced by this SoK is that the Botguard VM's extraordinary complexity—its self-modifying opcodes, rolling encryption keys, time-based seed mutation, and anti-logger traps—does not alter a fundamental architectural reality: **the Trust Anchor is the client environment**. When a threat actor controls that environment, all client-side defenses become environmental spoofing targets rather than security boundaries. The Puppet strategy is not a "bypass" in the conventional sense of breaking a cryptographic mechanism; it is an **architectural validation** of the trust-boundary limitation inherent in any software-only attestation scheme. The FIDO2 proxy failure case documented in this research—where a valid token generated in a "clean" browser authenticates a session initiated from a "dirty" one \cite{abel2021}—serves as a formal proof that a Relying Party cannot distinguish between a legitimate user and a sufficiently advanced emulator operating on an adversary-controlled machine.

The server-side validation model examined here reveals a critical asymmetry: validation checks the token's integrity but not its origin \cite{abel2021}. The token proves that *a* browser passed the checks; it does not prove *which* operator is holding the token. This token portability vulnerability is not an implementation bug in Botguard but an architectural property of any system where token generation occurs on an untrusted host.

This SoK makes the following contributions:

- **Taxonomy of Attestation Rigor (Section 3):** A structured comparison of hardware-backed (TEE-based) and software-only (obfuscated VM) attestation mechanisms, with explicit analysis of why "Sole Control" is technically unverifiable for the latter category. The taxonomy draws directly on the chronometric spoofing capabilities demonstrated by the anti-debug and anti-logger subversion documented in Register 21, Z.W, and Z.U analysis \cite{abel2021,cypa}.

- **Adversarial Modeling of Environmental Spoofing (Section 4):** A formal case study of the Puppet strategy as a Token Portability Vulnerability, demonstrating that token generation is fundamentally decoupled from token usage in modern web authentication \cite{abel2021}.

- **Threat Landscape Evolution Analysis (Section 5):** An examination of the industry shift from static single-token checks to session-bound and content-bound tokens, framing the Puppet strategy as the natural escalation from credential theft to dynamic environment spoofing \cite{abel2021,luanrt}.

- **Generalization to Remote Attestation Theory (Section 7):** An argument that the Botguard case study reveals an inherent ceiling for server-driven fraud detection—a ceiling that applies to any system that trusts client-generated attestation tokens.

The remainder of this paper is organized as follows. Section 2 surveys related work in remote attestation, token binding, and adversarial techniques. Section 3 presents the Taxonomy of Attestation Rigor. Section 4 formalizes the Puppet strategy as an adversarial model. Section 5 analyzes PO Tokens as an escalation of attestation complexity. Section 6 argues for an inherent ceiling in server-driven fraud detection. Section 7 generalizes findings to broader remote attestation and TEE contexts. Section 8 concludes.

---

## 2. Background and Related Work

### 2.1 Remote Attestation in Web Authentication

Remote attestation is the process by which a verifier (Relying Party) obtains trustworthy measurements of a prover's (client's) software state \cite{tee}. In the web authentication context, attestation serves to assure the server that the client environment is unmodified, that no adversary has instrumented the browser, and that the user is operating in a trusted execution context. Two paradigms dominate: hardware-backed attestation, where measurements are rooted in a Trusted Execution Environment such as a TPM or Secure Enclave (exemplified by FIDO2/WebAuthn \cite{fido2}); and software-only attestation, where integrity is self-reported by obfuscated client-side code (exemplified by Botguard). The FIDO2 standard's attestation model relies on a hardware authenticator that signs attestation statements with a private key that never leaves the secure enclave \cite{fido2}. The Token Binding Protocol (RFC 8471) further strengthens this model by cryptographically binding TLS connections to tokens, preventing token export and replay \cite{rfc8471}. These standards represent the hardware-backed pole of the attestation continuum. Botguard represents the opposing pole—a software-only scheme where the "attestation" is a self-generated token whose only validation is server-side integrity checking.

### 2.2 JavaScript Obfuscation and VM-Based Defenses

Software obfuscation has a well-documented history in malware protection \cite{obfuscation}. Control-flow flattening, opaque predicates, and string encryption are standard techniques. Botguard's register-based VM represents an escalation: rather than obfuscating the control flow of a JavaScript program, it defines an entirely new instruction set executed by a custom interpreter. This approach, previously documented in commercial protectors such as VMProtect and Themida for native code, has been adapted to the browser context. The VM uses a register-based approach (as opposed to stack-based) to more closely mimic x86 architecture \cite{abel2021}. The opcodes identified through reverse engineering include standard arithmetic (328/USHR, 381/ADD), property manipulation (65/SETPROP, 467/GETPROP), environment introspection (220/IN), and halting (289/HALT) \cite{abel2021,cypa}.

### 2.3 Token Portability as an Attack Surface

The concept of token portability—the ability to extract a security token from one context and reuse it in another—is the foundational vulnerability exploited by the Puppet strategy. Standard session management techniques attempt to prevent token portability through origin binding, channel binding, and time-bound expiration. However, these mechanisms are effective only when the binding is enforced at both generation and verification. In the Botguard model, token generation occurs on the client and verification on the server; there is no cryptographic mechanism by which the server can verify that the token was generated in the same session context in which it is presented.

### 2.4 Related Adversarial Techniques

The Puppet strategy belongs to a broader class of Man-in-the-Browser (MitB) attacks, where the adversary controls the browser environment to manipulate or extract sensitive data. Phishing kits that employ reverse proxies (e.g., EvilGinx, Modlishka) have demonstrated credential theft at scale. The Puppet strategy extends this lineage by automating the full attestation lifecycle: rather than proxying user interaction, it generates its own legitimate tokens through a fully emulated browser environment.

---

## 3. Taxonomy of Attestation Rigor

### 3.1 Defining the Attestation Continuum

The mechanisms by which a Relying Party authenticates a client environment span a continuum anchored by two poles: hardware-backed attestation (exemplified by WebAuthn with Trusted Execution Environments) and software-only obfuscation (exemplified by Botguard's JavaScript VM). The critical distinction lies in the **Root of Trust**: whether the attestation chain terminates in hardware that the adversary cannot modify, or in software executing on an adversary-controlled general-purpose CPU.

This section constructs a comparative taxonomy across seven dimensions, grounding each claim in the specific architectural evidence provided by the Botguard case study. The taxonomy serves two purposes: first, to demonstrate that the two approaches occupy fundamentally different positions on the trust continuum; and second, to prove that software-only methods cannot technically verify "Sole Control"—the property that no adversary is present in the authenticated session.

### 3.2 Comparative Framework

| Dimension | Hardware-Backed (TEE/WebAuthn) | Software-Only (Botguard) |
|---|---|---|
| **Root of Trust** | Hardware-fused private key in secure enclave; attestation certificate chains to manufacturer via FIDO MDS3 \cite{fido2}. | VM entry point located dynamically via substring extraction from bytecode; initialization function discovered at runtime. No persistent identity \cite{abel2021}. |
| **Attestation Channel** | Out-of-band attestation statement over CTAP (USB/NFC/BLE); cryptographically verifiable \cite{fido2}. | Token is the attestation itself; in-band HTTP request body. No architectural separation between attestation and application data \cite{abel2021}. |
| **Spoofing Resistance** | TEE measurements collected by hardware isolated from OS; spoofing requires physical key extraction. | Environmental parameters (`navigator.webdriver`, WebGL context, prototype chain) read by JavaScript and overridable by adversarial JavaScript. Stealth layer demonstrated to mask each parameter \cite{abel2021}. |
| **Token Binding** | Originating origin bound via Channel ID (RFC 8471) or attestation certificate \cite{rfc8471}. | Token encodes no persistent binding to user session. Tokens extracted from one context validate when injected into another \cite{abel2021}. |
| **Side-Channel Resistance** | Enclave isolates cryptographic operations from host OS and other processes. | Anti-logger trap vulnerable to console introspection; `t.prototype` stack manipulation shifts memory pointer upon logging \cite{abel2021}. |
| **Chronometric Integrity** | Hardware real-time counters; not spoofable without kernel compromise. | `performance.now()` + `Date.now()` comparison; debugger detection via time delta; Register 21 / Z.W / Z.U temporal dependencies \cite{abel2021}. |
| **Deployment Overhead** | Requires physical hardware (security key or TPM); server requires MDS integration. | Zero deployment overhead—entirely JavaScript-delivered. Primary motivation for adoption despite limitations. |

### 3.3 The "Sole Control" Problem

The taxonomy reveals a structural limitation: for software-only attestation, the property of "Sole Control"—the assurance that no adversary is influencing the authenticated session—is technically unverifiable. The evidence is most clearly demonstrated in the chronometric dimension.

Botguard's anti-debug mechanism attempts to detect adversarial presence by measuring time deltas. The VM polls `performance.now()` and `Date.now()` continuously, storing the result in a **Seed** (maintained in the VM context as `K.U`) \cite{abel2021}. If a debugger or breakpoint causes execution to pause, the elapsed time delta exceeds an expected threshold, and the seed mutates to a value that corrupts the decryption key for the next block of bytecode. The VM does not halt; it silently diverges into a garbage execution path, generating an invalid token. This is a sophisticated defense, but it is not a secure one.

The anti-logger mechanism, which binds trap functions to console methods through `t.prototype` stack manipulation \cite{abel2021}, reveals the same vulnerability from a different angle. By shifting the memory pointer through prototype modification, the VM attempts to detect instrumentation. However, this defense is itself subvertible: an adversary who controls the execution environment can override these traps, suppress the time delta signal, or feed the VM a consistent temporal reference.

The critical evidence lies in the memory reader function. The function `H` reads bytes from the bytecode array and encrypts them before return. Register 21 acts as a rolling key array; `Z.W` functions as a position tracker that increments linearly; `Z.U` is the seed that mutates based on time and execution history \cite{abel2021,cypa}. The call `H(true, L, 8)` reads 8 bits and, when the first argument is true, invokes an encryption routine using Register 21. A `SETPROP` opcode scrambles these keys, resetting the position and pulling a new seed from the reader. This circular dependency—the reader relies on the seed, the seed relies on the reader, and both rely on temporal integrity—is precisely where chronometric spoofing achieves its effect. An adversary who can present the VM with a fabricated time reference consistent with expected execution windows can maintain seed integrity and follow the valid execution path. The adversary need not understand the VM's opcodes or break its encryption; they need only simulate the temporal conditions under which the VM expects to operate.

This finding generalizes beyond Botguard. **Any software-only attestation mechanism that depends on temporal measurements to detect adversarial presence inherits the vulnerability that the adversary controls the clock.** Chronometric spoofing is not a bug in Botguard's implementation; it is a necessary consequence of operating without a hardware root of trust.

### 3.4 Implications for Relying Parties

The taxonomy forces a sobering conclusion for Relying Parties: server-side fraud detection that relies on client-generated attestation tokens faces a ceiling determined not by the sophistication of the client-side logic but by the architectural impossibility of verifying client integrity from the server. The token proves that *a* browser passed the checks; it does not prove *which* operator is holding the token, nor does it prove the absence of an adversary in the session. Server-side correlation signals (IP reputation, behavioral analytics, historical session patterns) can raise the operational cost of an attack but cannot close the architectural gap \cite{abel2021}.

The practical implication is a reorientation of defense strategy: instead of attempting to make client-side attestation adversary-proof—a goal that, as this taxonomy demonstrates, is structurally unachievable for software-only mechanisms—Relying Parties should invest in detection of temporal anomalies at the server side, accept the attestation ceiling, and deploy layered defenses that combine client-side signals with server-side pattern analysis.

---

## 4. Adversarial Modeling: The Puppet Strategy as a Trust-Boundary Demonstration

### 4.1 Architectural Overview of the Puppet

Given the complexity of the Botguard VM—self-modifying opcodes, rolling encryption keys, and time-based seed mutation—pure reverse engineering represents a high-cost, low-yield attrition strategy. The most efficient attack vector is not to break the cryptographic lock but to steal the key. The Puppet strategy achieves this by creating a compliant execution environment that satisfies all of Botguard's environmental and behavioral checks, then extracting the generated token for use in a separate, adversarial context.

The Puppet is constructed using **go-rod**, a Golang-based browser automation framework that provides fine-grained control over browser lifecycle, network interception, and JavaScript execution \cite{abel2021}. The architecture comprises four stages:

1. **Stealth Layer Construction.** Standard headless Chrome leaks its identity through detectable properties including `navigator.webdriver = true`, distinctive user-agent strings, and observable WebGL rendering artifacts. The Puppet applies stealth patches that mask the user agent, override prototype methods to remove automation indicators, and spoof WebGL rendering contexts to match those of a genuine browser instance \cite{abel2021}. These modifications operate at the renderer process level, making them transparent to JavaScript executing within the page.

2. **Token Generation.** The automated browser navigates to `accounts.google.com` and submits a target credential. Botguard initializes within the page context, executes its full VM lifecycle—including chronometric validation and environmental introspection—and mints the `bgRequest` token \cite{abel2021}. Because the Puppet presents a consistent, non-anomalous environment, the VM follows the valid execution path and produces a cryptographically correct token.

3. **Interception.** A client-side request hook captures the network request immediately after token generation but before it reaches Google's server. The token is extracted and the request is aborted, preventing the token from being "spent" on the legitimate domain \cite{abel2021}.

4. **Injection.** The extracted token is forwarded to a separate MITM proxy infrastructure. When a victim initiates a login session through the phishing proxy, the Puppet controller attaches the pre-generated token to the victim's request. Google's server validates the token against its integrity checks and authorizes the session, unable to distinguish the token's provenance \cite{abel2021}.

### 4.2 Formalizing the Token Portability Vulnerability

The Puppet strategy succeeds because of a fundamental architectural gap: **token generation is decoupled from token usage.** The server-side validation model checks the token's cryptographic integrity, not the context in which it was generated \cite{abel2021}. The token proves that *a* compliant instance of the VM produced it; it does not prove that the current user is the operator of that instance.

This decoupling can be formalized as follows. Let $G$ be the token generation function executed on the client, $V$ be the verification function executed on the server, and $C$ be the client environment (user agent, plugins, hardware properties, temporal state). The server accepts a token $\tau$ if $V(\tau) = \text{valid}$. The security property intended by the design is that $\tau$ is produced by a process $G(C, U)$ where $U$ is the legitimate user in possession of the session. However, the Puppet demonstrates that an adversary can compute $\tau' = G(C', \bot)$ where $C'$ is an emulated environment approximating $C$ and $\bot$ indicates the absence of a legitimate user, then present $\tau'$ to the server in a session controlled by the adversary. Since $V(\tau') = \text{valid}$, the server cannot distinguish $\tau'$ from $\tau$.

This is not a cryptographic break but an **architectural trust-boundary demonstration**. The vulnerability is inherent to any attestation system where:

- The generation of the attestation token occurs on an adversary-controlled host;
- The verification function has no mechanism to bind the token to the specific session context;
- The attestation secret (if any) is accessible during the generation process.

### 4.3 The FIDO2 Proxy Failure as Formal Proof

The Puppet strategy's implications extend beyond Botguard. Consider a FIDO2 WebAuthn authentication flow conducted through a reverse proxy. In the intended security model, the browser's origin is cryptographically bound to the authenticator's assertion via the `rpId` parameter. However, if an adversary operates a proxy that terminates the TLS connection at the phishing domain and establishes a new TLS connection to the legitimate Relying Party, the browser believes it is authenticating to the phishing domain. The authenticator's attestation is valid for the phishing `rpId`; the adversary then forwards this assertion to the legitimate server, which accepts it because the cryptographic signature is correct for the user's credential.

The Botguard case is structurally identical. The distinction is one of trust anchor: FIDO2 relies on a hardware authenticator that performs origin binding, while Botguard relies on a software VM that performs environmental validation. The Puppet strategy demonstrates that **software-based origin and environment validation are indistinguishable from emulation to a server-side verifier.** The formal proof is that the verifier cannot distinguish between the distributions of tokens produced by a legitimate user operating a genuine browser and an adversary operating a sufficiently advanced emulator, provided the emulator correctly mimics the environmental properties checked by the attestation logic.

### 4.4 Operational Observations

The Puppet strategy carries practical limitations. Each compiled instance of the Botguard VM uses different variable names and opcode mappings, meaning that any analysis that depends on specific identifier names must be repeated per compile \cite{abel2021}. However, because the strategy operates at the environmental level rather than the code level, recompilation does not affect the attack: the adversary does not need to understand the VM, only to present an environment that satisfies its checks. The operational cost of the attack is the effort required to maintain the stealth layer against evolving detection heuristics.

---

## 5. Multi-Layer Token Analysis: PO Tokens and the Escalation of Attestation

### 5.1 Challenge Initialization

YouTube's Proof of Origin (PO) Token system represents an evolutionary response to the token portability vulnerability. Before a PO Token can be generated, the client must obtain a Botguard challenge consisting of a VM script and its associated bytecode program. Three methods exist for this retrieval \cite{abel2021,luanrt}:

1. **Direct from Page Source:** The InnerTube challenge response is embedded in the initial page HTML.

2. **InnerTube API:** An API endpoint returns challenge data in readable format:
   ```typescript
   const challengeResponse = await innertube
     .getAttestationChallenge('ENGAGEMENT_TYPE_UNBOUND');
   const interpreterUrl = challengeResponse.bg_challenge.interpreter_url
     .private_do_not_access_or_else_trusted_resource_url_wrapped_value;
   ```

3. **Web Anti-Abuse Private API:** Google's internal `jnn-pa.googleapis.com` endpoint (`google.internal.waa.v1.Waa/Create`) provides challenge data, potentially obfuscated depending on the `requestKey` \cite{abel2021}.

### 5.2 Integrity Token Retrieval

The Botguard VM is loaded with the bytecode program, which returns several functions via a callback mechanism. The `asyncSnapshotFunction` is invoked to obtain the Botguard response:

```javascript
const webPoSignalOutput = [];
const botguardResponse = await snapshot({
  contentBinding: undefined,
  signedTimestamp: undefined,
  webPoSignalOutput: webPoSignalOutput,
  skipPrivacyBuffer: undefined
});
```

This response is exchanged for an integrity token via the `GenerateIT` endpoint \cite{abel2021,luanrt}:

```typescript
const integrityTokenResponse = await fetch(
  'https://jnn-pa.googleapis.com/$rpc/google.internal.waa.v1.Waa/GenerateIT',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json+protobuf',
      'x-goog-api-key': '[REDACTED]',
    },
    body: JSON.stringify([requestKey, botguardResponse])
  }
);
// Returns: [integrityToken, estimatedTtlSecs, mintRefreshThreshold, websafeFallbackToken]
```

### 5.3 Token Typology

YouTube's player employs three distinct PO Token types, each with different binding semantics and portability properties \cite{abel2021,luanrt}:

- **Cold Start Token:** A placeholder token using a simple XOR cipher, bound to Data Sync ID or Visitor ID. Used to initiate playback before a full session token is minted.

- **Session Bound Token:** Generated on first user interaction with the player. Binds to the account's Data Sync ID (authenticated users) or Visitor ID (anonymous users). Represents a step toward session-aware attestation.

- **Content Bound Token:** Generated per `/player` request. Bound to the specific Video ID via `serviceIntegrityDimensions.poToken`. Designed to be non-cacheable and tied to the current content request.

### 5.4 StreamProtectionStatus (sps)

The player evaluates a value called `sps` in each media segment response (UMP or SABR streaming protocols) to determine PO Token requirements \cite{abel2021}:

- **Status 1:** Valid PO Token present, user has YouTube Premium, or stream does not require tokens.
- **Status 2:** PO Token required; client may request up to 1--2 MB of data before playback interruption.
- **Status 3:** PO Token mandatory; no further data deliverable without a valid token.

The `sps` mechanism represents a pragmatic acknowledgment of the attestation ceiling: rather than preventing token portability entirely, it enforces graduated consequences when portability is detected, limiting the damage window.

### 5.5 Applicability of the Puppet Bypass

The environmental spoofing approach remains theoretically applicable to YouTube's PO Token system. The core vulnerability—token portability—persists. A compliant browser environment can generate valid PO Tokens that are then transferred to a different context. However, the multi-layer architecture introduces friction: three distinct token types with different binding semantics, server-side `sps` enforcement, and content-bound tokens tied to specific Video IDs \cite{abel2021}. These factors raise the operational cost of the attack but do not alter the fundamental architectural vulnerability: token generation still occurs on an adversary-controlled client.

---

## 6. The Inherent Ceiling of Server-Driven Fraud Detection

### 6.1 The Signal Asymmetry Problem

Server-side fraud detection systems correlate multiple signals—IP reputation, user-agent consistency, behavioral patterns, historical session data—to assess the likelihood of adversarial presence. The Puppet strategy exposes a fundamental asymmetry: the server has access only to signals that the client chooses to transmit. Environmental properties, temporal measurements, and behavioral biometrics are all collected and reported by code executing on the adversary-controlled host. An adversary who understands which signals influence the server's risk model can fabricate them.

### 6.2 Industry Responses and Their Limitations

The PO Token system's multi-layer architecture and `sps` enforcement represent the most sophisticated industry response to the token portability problem. Content-bound tokens reduce the replay window; session-bound tokens tie attestation to user identity; graduated enforcement limits data leakage \cite{abel2021}. However, these are mitigations, not solutions. They raise the adversary's operational cost but do not close the architectural gap. The adversary still controls the token generation environment; the server still cannot verify the context of generation.

### 6.3 Formalizing the Ceiling

The architectural ceiling can be formalized as follows: any detection system $D$ whose inputs are entirely supplied by a client $C$ under adversarial control cannot achieve deterministic separation between the distributions $P(\text{input} \mid \text{legitimate})$ and $P(\text{input} \mid \text{adversarial})$, because the adversary can arbitrarily transform the latter distribution to match the former. Server-side correlation can reduce the overlap between these distributions but cannot eliminate it entirely. The ceiling is determined by the adversary's knowledge of $D$'s decision boundary and the cost of fabricating inputs that cross it.

---

## 7. Generalization to Remote Attestation and Trusted Execution Environments

### 7.1 Lessons from the Botguard Case Study

The Botguard VM serves as a microcosm of attestation challenges that generalize to any software-only remote attestation scheme. Four architectural lessons emerge:

- **Complexity does not equal security.** The Botguard VM's self-modifying opcodes, rolling encryption, and chronometric defenses represent extraordinary engineering investment. None of these prevent environmental spoofing because none of them alter the fundamental architecture: the attestation logic shares an execution substrate with the adversary.

- **Temporal integrity requires a hardware anchor.** All chronometric defenses are subvertible when the adversary controls the clock source. Hardware-backed real-time counters—isolated from the main processor and its timer APIs—are necessary for meaningful temporal attestation.

- **Token portability is an architectural property.** Session binding, content binding, and graduated enforcement are mitigations that raise operational cost; they are not structural solutions. True token binding requires cryptographic linking of the token to a hardware identity that cannot be duplicated.

- **Attestation must be remote-verifiable.** A security mechanism whose output cannot be independently verified by the Relying Party is an appeal to authority, not a security guarantee. The Botguard token's validity depends entirely on the server trusting that the client executed the VM faithfully. This circular trust relationship is the core architectural fragility.

### 7.2 Applying the Taxonomy Beyond Web Security

The Taxonomy of Attestation Rigor presented in Section 3 applies beyond the browser context. IoT device attestation, mobile payment integrity checks, and DRM systems all face the same fundamental trade-off between hardware-backed and software-only attestation. In each domain, the absence of a hardware root of trust implies that "Sole Control" is unverifiable, and the attacker who controls the execution environment can subvert any software-based measurement.

### 7.3 Open Problems

The Botguard case study highlights several open research problems:

- **Hardware-anchored session binding:** Can attestation tokens be cryptographically bound to a hardware identity (e.g., TPM) through a standard web API, obviating the need for software-only attestation?

- **Multi-factor attestation:** Can the combination of multiple weak signals (environmental, behavioral, network-level) achieve the same verification strength as a single strong hardware anchor?

- **Zero-knowledge approaches:** Can client integrity be verified without transmitting the raw environmental measurements, using zero-knowledge proofs that the client environment satisfies certain constraints?

---

## 8. Conclusions

This Systematization of Knowledge has examined Google's Botguard JavaScript Virtual Machine as a canonical case study in the inherent fragility of client-side trust. The central thesis—that software-only client-side attestation is architecturally incapable of proving the absence of an adversary—has been supported through three integrated lines of evidence.

First, the Taxonomy of Attestation Rigor demonstrated that the gap between hardware-backed and software-only attestation is not a matter of degree but of kind. Hardware-backed schemes (e.g., WebAuthn with TEE) provide a hardware root of trust that is inaccessible to software-level adversaries; software-only schemes (e.g., Botguard) rely entirely on obfuscation and environmental checks that execute on the adversary-controlled host. The chronometric defense, however sophisticated, is structurally subvertible because the adversary controls the clock.

Second, the Puppet strategy provided a concrete adversarial model demonstrating token portability as an architectural vulnerability rather than an implementation bug. The four-stage pipeline—stealth layer, token generation, interception, injection—proves that the server cannot distinguish between a token generated by a legitimate user and one generated by a sufficiently advanced emulator. This is not a cryptographic break but a trust-boundary demonstration.

Third, the analysis of YouTube's PO Token system revealed that even the most advanced multi-layer token architectures—with session binding, content binding, and graduated server-side enforcement—do not eliminate the foundational vulnerability. They raise the adversary's operational cost but leave the architectural gap intact.

The implications for the broader security community are clear. Client-side attestation mechanisms, however sophisticated, cannot achieve adversary-verifiable security without a hardware root of trust. Defenders should accept this ceiling, invest in server-side anomaly correlation, and advocate for hardware-anchored attestation standards in the web platform. Complexity is not a substitute for a hardware trust anchor; the ceiling is architectural, not computational.

---

## References

\bibliographystyle{ieeetr}

\begin{thebibliography}{99}

\bibitem{abel2021}
Abel, T.~K. (2021). \emph{Kits K\"{a}rneriks: Breaking the Glass on Client-Side Fraud Defense.} GitHub Research Repository. \url{https://github.com/tomkabel/google-botguard-security-research}

\bibitem{cypa}
Cypa (@dsekz). \emph{botguard-reverse.} GitHub Repository. \url{https://github.com/dsekz/botguard-reverse}

\bibitem{luanrt}
LuanRT. \emph{BgUtils.} GitHub Repository. \url{https://github.com/LuanRT/BgUtils}

\bibitem{fido2}
FIDO Alliance. (2021). \emph{WebAuthn Level 2.} W3C Recommendation. \url{https://www.w3.org/TR/webauthn-2/}

\bibitem{rfc8471}
Jones, M. et al. (2018). \emph{Token Binding Protocol Version 1.0.} RFC 8471, IETF. \url{https://datatracker.ietf.org/doc/rfc8471/}

\bibitem{tee}
Sadeghi, A.-R. et al. (2015). A Survey of Trusted Execution Environments. \emph{ACM Computing Surveys}, 48(1), 1--36.

\bibitem{obfuscation}
Schrittwieser, S. et al. (2016). Protecting Software Through Obfuscation: A Survey. \emph{ACM Computing Surveys}, 48(1), 1--37.

\bibitem{mitb}
Callegati, F., Cerroni, W., and Ramilli, M. (2009). Man-in-the-Browser: An Overview of a Web Threat. \emph{IEEE Internet Computing}, 13(6), 76--80.

\bibitem{evilginx}
Kuts, K. (2017). \emph{EvilGinx: Man-in-the-Middle Attack Framework.} GitHub Repository.

\bibitem{chromeheadless}
Nakajima, S. (2024). \emph{go-rod: A Golang Browser Automation Framework.} GitHub Repository.

\end{thebibliography}

---

*This document is for educational and research purposes only. The techniques described herein are documented to inform the design of more secure authentication systems, not to enable unauthorized access to protected services.*
