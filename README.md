# Kits Kärneriks: Breaking the Glass on Client-Side Fraud Defense

## 1. The Objective

This repository chronicles a dual-pronged assault on Google's login infrastructure. The primary target is "Botguard," a defensive mechanism often dismissed as a simple fingerprinting script. It is not. It is a hostile, obfuscated Virtual Machine (VM) running directly in the client's browser.

In 2021, we proved this system could be bypassed. We did not do this by untangling the knot; we cut it. By utilizing a hardened headless browser, we generated valid security tokens on the legitimate domain and trafficked them to a Man-in-the-Middle (MITM) phishing context. This document details the architectural flaws of that client-side trust model and integrates a deep-dive reverse engineering analysis of the VM internals that make Botguard such a formidable adversary.

> 🚨 **Operational Note** 🚨
>
> The architectural analysis here applies to the core Botguard VM logic found in ReCaptcha v2 and Google's v2/v3 login flows. While specific variable names shift with every compile, the underlying "CPU-in-JavaScript" logic remains the engine of their defense.

---

## Attribution & Acknowledgments

This document integrates three distinct contributions:

1. **Original Research (2021):** The bypass strategy described in Section 4—the "Puppet" approach using go-rod for environmental spoofing and token extraction—represents our original proof-of-concept demonstrating that client-side token generation can be decoupled from its usage context.

2. **VM Internal Analysis:** The technical deep-dive into Botguard's Virtual Machine architecture (Sections 2, 3, and 6) builds upon the pioneering reverse engineering work conducted by **Cypa** (@dsekz). Specifically:
   - The opcode identification and classification
   - The anti-debug mechanism analysis (chronometric defense)
   - The anti-logger mechanism documentation
   - The memory reader function analysis (Register 21, Z.W, Z.U)

   This VM analysis was originally published in Cypa's [botguard-reverse](https://github.com/dsekz/botguard-reverse) repository. We acknowledge this work as the foundation for understanding Botguard's internal architecture.

3. **PO Token Analysis:** Section 7 documents the modern Proof of Origin (PO) Token system used by YouTube's web player. This section is derived from reverse-engineering work by **LuanRT** published in the [BgUtils](https://github.com/LuanRT/BgUtils) repository, used under MIT License.

---

## 2. The Defense: It's Not a Script, It's a CPU *(Based on Cypa's Analysis)*

To defeat the enemy, you must understand its biology. Botguard is not a static list of checks. It is a custom, register-based Virtual Machine written in JavaScript.

When the browser loads the login page, it doesn't just run code; it boots a processor. This VM executes a custom bytecode binary. This is the heavy armor. It beats standard Control Flow Flattening (CFF) because you cannot simply beautify the code to read it. You must write a disassembler, a decompiler, and a custom debugger just to see the instructions.

### The Virtual Machine Architecture

The VM emulates a modern CPU. It uses registers to hold variables and operational states. While older obfuscators might use stack-based logic (like Java or WASM), Botguard uses a register-based approach that mimics the x86 architecture sitting in your actual hardware.

The initialization sequence is frantic. It locates its own bytecode string, grabs a substring (often the first three characters + an underscore), and uses that dynamic key to locate the initialization function. This prevents static analysis tools from easily finding the entry point. Once the VM boots, it begins executing opcodes.

### The Opcodes

We identified the instruction set through painful trial and error. The VM utilizes a mix of standard logic and custom operations:

* **`328 (USHR) / 381 (ADD)`:** Standard bitwise and arithmetic operations.
* **`65 (SETPROP) / 467 (GETPROP)`:** Manipulation of object properties, used to bind the anti-tamper mechanisms to the DOM.
* **`220 (IN)`:** Checks for the existence of properties, likely looking for `webdriver` flags.
* **`289 (HALT)`:** Kills the execution if an anomaly is detected.

The most dangerous aspect is **Self-Modifying Code**. The VM brings in new opcodes at runtime. It constructs an array of integers (Register 274) and maps them to string definitions, using a `LOADSTRING` opcode to generate new instructions on the fly. An `EVAL` opcode (mapped as `LOADOP`) then compiles these into executable logic. The code you see at the start is not the code that runs at the end.

## 3. Anti-Tamper Mechanisms *(Based on Cypa's Analysis)*

Botguard actively fights back against analysis. It assumes it is being watched.

### Chronometric Defense (Anti-Debug)

The script is obsessed with time. It constantly polls `performance.now()` combined with `Date.now()`. If you set a breakpoint in DevTools, the execution pauses, but the clock keeps ticking. When you resume, the delta between timestamps is massive.

The VM uses this delta to mutate a **Seed** (stored in the VM context `K.U`). The seed determines the decryption key for the next block of bytecode. If the time delta suggests a debugger was active, the seed corrupts. The program doesn't crash immediately; it silently diverges into a garbage execution path, generating an invalid token that the server will reject. You think you are debugging it, but you are ghost-hunting in a dead timeline.

### The Anti-Logger

You cannot print the variables. The script aggressively binds to console methods. It creates a trap function that overrides properties using a `create` (or similar) method. If you attempt to inject a `console.log` or use a conditional logpoint, the trap triggers.

This trap modifies the `t.prototype` stack, which is linked to the memory reader function. By logging a variable, you inadvertently shift the memory pointer. The VM reads the wrong bytes, the instruction stream corrupts, and the session dies.

## 4. The Bypass: Environmental Spoofing *(Original Research)*

Given the complexity of the VM—self-modifying opcodes, rolling encryption keys, and time-based seed mutation—pure reverse engineering is a high-cost attrition war. The most efficient attack vector is not to break the lock but to steal the key.

### The "Puppet" Strategy

The server-side validation checks the token's integrity, not its origin. The token proves that *a* browser passed the checks. It does not prove *which* user is holding the token.

We deployed **go-rod**, a Golang-based browser automation framework, to act as the token factory.

1. **Stealth Layer:** Standard headless Chrome leaks its identity (e.g., `navigator.webdriver = true`). We patched this using stealth libraries to mask the user agent, override prototype methods, and spoof WebGL rendering contexts.

2. **Token Extraction:** The automated browser navigates to `accounts.google.com`. It inputs a target email. Botguard runs, validates the environment, and mints the `bgRequest` token.

3. **Interception:** We hook the request on the client side immediately after generation. We abort the network call to Google (preventing the token from being "spent") and extract the string.

4. **Injection:** This fresh, valid token is passed to our MITM proxy. The proxy attaches it to the victim's request. Google's server sees a valid token from a "clean" browser and authorizes the phishing session.

This method bypasses the VM entirely. We do not care about the opcodes or the registers because we are giving the VM exactly what it wants: a compliant browser environment.

## 5. The Reality Check

* **Client-Side Checks are Vulnerable to Environmental Spoofing:** While powerful, client-side defenses are fundamentally running on an attacker-controlled machine. With sufficient effort, the environment can be mimicked to satisfy the checks. The use of stealth plugins is a clear example of this.

* **Token Portability is a Fundamental Weakness:** The security of token-based systems like Botguard relies on the token being non-transferable. This research demonstrates that if token generation can be outsourced to a "clean" environment, the token can then be used in a "dirty" one, defeating the purpose of the check. This vulnerability extends to YouTube's PO Token system, though the multi-layer token architecture and content binding provide some additional friction.

* **The Importance of Layered Defense:** This bypass works because it circumvents a single, albeit strong, layer of defense. More advanced defensive systems should correlate the token's fingerprint with server-side signals (e.g., IP address reputation, historical session data, behavioral analysis) to detect anomalies. The PO Token's `sps` mechanism represents a step in this direction—server-side enforcement that doesn't rely solely on token validity.

The industry creates these elaborate cat-and-mouse games, adding layers of obfuscation and behavioral analysis. Yet, as long as the logic relies on a token that can be ported from a clean environment to a dirty one, the defense is bypassable. It isn't about breaking the encryption; it is about abusing the architecture.

<table>
  <tr>
    <td><img width="1024" height="512" alt="botguard_white" src="https://github.com/user-attachments/assets/b2304d98-c1a0-4d9b-8c10-f62aceb2d1fe" /></td>
    <td><img width="1024" height="512" alt="botguard_dark" src="https://github.com/user-attachments/assets/c8515399-ef0f-4260-9e4b-998a8ff31104" /></td>
  </tr>
</table>

## 6. Technical Findings: The Memory Reader *(Based on Cypa's Analysis)*

For those intent on the pure reverse-engineering path, the heart of the beast is the memory reader function, often minified as `H`.

It reads bytes from the bytecode array but encrypts them before return.

* **Register 21:** Acts as a rolling key array.
* **`Z.W`:** A position tracker that increments linearly.
* **`Z.U`:** The seed, which mutates based on time and execution history.

The function `H(true, L, 8)` reads 8 bits. If the first argument is true, it calls an encryption routine using Register 21. A `SETPROP` opcode exists specifically to scramble these keys, resetting the position and pulling a new seed from the reader. This circular dependency (the reader relies on the seed, the seed relies on the reader) makes static analysis nearly impossible without perfect emulation.

---

## 7. PO Token Generation & Attestation *(Based on BgUtils Research)*

> **Note:** This analysis is based on reverse-engineering work by LuanRT published in the BgUtils repository. Google regularly updates their security mechanisms; specific details may change over time.

This section documents the modern Proof of Origin (PO) Token system used by YouTube's web player. While the earlier sections focused on BotGuard in login/ReCaptcha contexts, YouTube employs an additional layer of protection through PO Tokens and attestation challenges. The following analysis is derived from reverse-engineering work by **LuanRT** published in the [BgUtils](https://github.com/LuanRT/BgUtils) repository.

### Challenge Initialization

Before a PO Token can be generated, the client must obtain a BotGuard challenge. This challenge consists of a VM script and its associated bytecode program. There are three methods to retrieve this data:

1. **Direct from Page Source**: The InnerTube challenge response is embedded in the initial page's HTML source when the page loads.

2. **InnerTube API**: An API endpoint that returns challenge data in a readable format. This is typically the easiest method:

   ```typescript
   const innertube = await Innertube.create();
   const challengeResponse = await innertube.getAttestationChallenge('ENGAGEMENT_TYPE_UNBOUND');
   
   const interpreterUrl = challengeResponse.bg_challenge.interpreter_url.private_do_not_access_or_else_trusted_resource_url_wrapped_value;
   const interpreterJavascript = await fetch(`https:${interpreterUrl}`).then(r => r.text());
   ```

3. **Web Anti-Abuse Private API**: An internal Google API (`jnn-pa.googleapis.com`) also used by Google Drive. Responses may be obfuscated depending on the `requestKey`:

   ```typescript
   const response = await fetch('https://jnn-pa.googleapis.com/$rpc/google.internal.waa.v1.Waa/Create', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json+protobuf',
       'x-goog-api-key': '[REDACTED]',
     },
     body: JSON.stringify([requestKey, interpreterHash])
   });
   ```

Once retrieved, the VM script is executed to make the BotGuard instance available in the global scope.

### Integrity Token Retrieval

The integrity token is the first critical output. It is obtained from Google's attestation server and relies directly on the BotGuard response to assess the runtime environment's integrity.

To begin, the BotGuard VM must be loaded with the bytecode program:

```javascript
// BotGuard returns several functions via vmFunctionsCallback
const vmFunctionsCallback = (asyncSnapshotFunction, shutdownFunction, passEventFunction, checkCameraFunction) => {
  // Store these for later use
};

this.syncSnapshotFunction = await this.vm.a(this.program, vmFunctionsCallback, true, undefined, () => {}, [[], []])[0];
```

The `asyncSnapshotFunction` is then invoked to obtain the BotGuard response:

```javascript
const webPoSignalOutput = [];
const botguardResponse = await snapshot({
  contentBinding: undefined,
  signedTimestamp: undefined,
  webPoSignalOutput: webPoSignalOutput,  // BotGuard fills this with minter functions
  skipPrivacyBuffer: undefined
});
```

This response is then exchanged for an integrity token from the `GenerateIT` endpoint:

```typescript
const payload = [requestKey, botguardResponse];
const integrityTokenResponse = await fetch('https://jnn-pa.googleapis.com/$rpc/google.internal.waa.v1.Waa/GenerateIT', {
  method: 'POST',
   headers: {
     'Content-Type': 'application/json+protobuf',
     'x-goog-api-key': '[REDACTED]',
   },
   body: JSON.stringify(payload)
});
// Returns: [integrityToken, estimatedTtlSecs, mintRefreshThreshold, websafeFallbackToken]
```

### Minting WebPO Tokens

The `webPoSignalOutput` array populated during the snapshot call contains functions used to create PO Tokens. The first function serves as a minter:

```javascript
// Helper functions assumed available:
// - base64ToU8(base64String): Decodes base64 to Uint8Array
// - u8ToBase64(u8Array, urlSafe): Encodes Uint8Array to base64 (urlSafe=true removes padding)

const getMinter = webPoSignalOutput[0];
const mintCallback = await getMinter(base64ToU8(integrityToken));

// Bind to an identifier (Visitor ID, Data Sync ID, or Video ID)
const result = await mintCallback(new TextEncoder().encode(identifier));
const poToken = u8ToBase64(result, true);  // Result is 110-128 bytes
```

### Token Types

YouTube's player uses three distinct PO Token types:

- **Cold Start Token**: A placeholder token used to initiate playback before the full session-bound token is minted. It uses a simple XOR cipher and is bound to the Data Sync ID or Visitor ID.

- **Session Bound Token**: Generated when the user first interacts with the player. If the user is logged in, it binds to the account's Data Sync ID; otherwise, it uses the Visitor ID.

- **Content Bound Token**: Generated for every `/player` request (`serviceIntegrityDimensions.poToken`). It is bound to the specific Video ID and should not be cached.

### StreamProtectionStatus (sps)

The player checks a value called `sps` in each media segment response (only when using UMP or SABR streaming protocols) to determine if a PO Token is required:

- **Status 1**: Stream has a valid PO Token, user has YouTube Premium, or stream doesn't require tokens.
- **Status 2**: PO Token required; client can request up to 1-2 MB of data before playback is interrupted.
- **Status 3**: PO Token mandatory; no further data can be requested without a valid token.

### Applicability of the Puppet Bypass

The environmental spoofing approach described in Section 4 is theoretically applicable to YouTube's PO Token system. The core vulnerability—token portability—remains present. A compliant browser environment can generate valid PO Tokens that are then transferred to a different context. However, YouTube's architecture introduces additional complexity:

- **Multi-Layer Token System**: Unlike the single `bgRequest` token in login flows, YouTube requires three distinct token types (cold start, session-bound, content-bound), each with different binding semantics.
- **StreamProtectionStatus Enforcement**: The `sps` mechanism provides server-side enforcement that can interrupt playback if valid tokens are not provided, limiting the time window for token reuse.
- **Content Binding**: Content-bound tokens are tied to specific Video IDs, making them less portable than session-bound tokens.

These factors make the Puppet approach more complex to execute against YouTube but do not fundamentally alter the architectural vulnerability inherent in client-side token generation.

---

## References

1. **Cypa** — BotGuard VM Reverse Engineering
   - Repository: [https://github.com/dsekz/botguard-reverse](https://github.com/dsekz/botguard-reverse)
   - The foundational reverse engineering analysis of Botguard's VM architecture, opcodes, and anti-debug mechanisms.

2. **LuanRT** — BgUtils (PO Token Generation)
   - Repository: [https://github.com/LuanRT/BgUtils](https://github.com/LuanRT/BgUtils)
   - Reverse-engineered implementation of YouTube's PO Token generation and attestation processes.
   - Content used under MIT License.

---

## 8. Contact

For questions, discussions, or collaboration inquiries related to this research, please reach out via the repository's issue tracker or the author's linked profile.

---

*This document is for educational and research purposes only.*
