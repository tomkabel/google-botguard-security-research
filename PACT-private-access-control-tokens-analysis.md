# Private Access Control Tokens and the Software-Anchor Turn: A Critical Analysis

## Introduction and Scope

On June 22, 2026, Cloudflare announced **Private Access Control Tokens (PACT)** as a cross-industry initiative with Mozilla Firefox, Google Chrome, Microsoft Edge, and Shopify. The stated goal is to replace invasive CAPTCHAs and behavioral surveillance with anonymous cryptographic attestation while also adapting to a web in which bots now account for roughly **58 percent of HTTP requests**, leaving only 42 percent attributable to humans ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)). PACT extends the Privacy Pass architecture, which the IETF formalized in 2024 as **RFC 9576**, and adds native support across major browser engines plus an explicit focus on agentic AI traffic ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)).

It is important to be precise about the state of PACT. As of mid-2026, PACT is **a proposal, not a product**. There is no deployment timeline, no IETF draft published under the PACT name, and no finalized issuance-governance specification ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)). What exists is a press statement, early design discussion in the `antifraudcg/pact` repository, and an invitation to reason about an architecture before its most consequential decision has been made: **who gets to issue tokens, and on what basis** ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)).

This report evaluates PACT specifically as an architecture that leans on **software or contextual anchors**—active subscriptions, account standing, issuer vouching, or other first-party relationship signals—rather than on hardware-backed roots of trust such as Apple's Secure Enclave or Android Play Integrity.

---

## 1. Trust Model Shift: From Hardware Scarcity to Issuer Judgment

### The hardware baseline

Apple's existing Private Access Tokens provide the clearest hardware-anchor contrast. In that model, the device operating system manufacturer performs attestation. Cloudflare's implementation can check, without installing client software, whether a device is on the latest OS version, whether it is jailbroken, and whether the login window is in focus ([Cloudflare Blog](https://blog.cloudflare.com/private-attestation-token-device-posture/)). The scarcity signal is anchored to:

> Approved device + approved hardware + approved operating environment.

Mozilla has specifically warned that widespread reliance on that model could strengthen platform gatekeepers by making access to web resources dependent on hardware-controlled attestation ([Krishna Gupta](https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/)). PACT is therefore an attempt to broaden the trust model so that scarcity can originate from different kinds of anchors, not only from the device manufacturer ([Krishna Gupta](https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/)).

### The shift in Sybil economics

Substituting a hardware root of trust with software-level issuer endorsements does not remove the Sybil problem; it moves it. In the Privacy Pass/PACT model, an **Attester** is "a party that knows something about the user," and an **Issuer** signs the blinded token ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)). If the "something" is an active subscription, account standing, or issuer vouching, then the attacker's unit of scarcity is no longer a compromised device but a **credentialed account**.

That is a meaningful change in attacker economics. Hardware attestation forces a bot operator to acquire or emulate many trusted devices, each with a secure hardware-backed identity. Contextual anchors force the attacker to acquire or synthesize many accounts, subscriptions, or vouches. The latter can be automated through credential stuffing, bulk account registration, stolen session tokens, or simply paying for cheap subscriptions in bulk. As one analysis put it:

> Token farming creates a new abuse layer upstream; the fix, hardware attestation, slides back into exactly what WEI was killed for ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)).

### The browser "trust" boundary is not a trust anchor

In the proposed design, the browser is treated as a trusted user-agent that mediates credential storage, issuer selection, challenge budgets, and conversion ([GitHub Issue #6](https://github.com/antifraudcg/pact/issues/6)). But a sophisticated bot operator often controls the browser profile, the device, or both. The browser can be a convenient API boundary for legitimate users, but it is not a trustworthy admission controller when the user-agent itself is automated or compromised. The cryptographic unlinkability of Privacy Pass tokens does not fix this; it merely ensures that a token can be redeemed without revealing which issuer produced it or which user obtained it. The token's value still depends entirely on the quality of the issuer's admission process.

---

## 2. Centralization and Gatekeeping: The Trust Oligopoly Risk

### The strategic position of the platform coordinator

The announcement does not specify who qualifies as an Attester, but it frames Cloudflare—already underpinning a substantial share of global web infrastructure—as a natural central participant ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)). One analysis noted that PACT "raises trust on Cloudflare's network," not necessarily on the open web as a whole ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)). That distinction matters: a standard that works best for sites hosted behind the entity proposing it is not clearly neutral global public infrastructure.

### How origins become gatekeepers

In one design sketch, the origin configures **up to two aggregating issuers** and the credit cost per request ([GitHub Issue #6](https://github.com/antifraudcg/pact/issues/6)). This puts enormous power in the origin's choice. If major destinations converge on a small set of issuers—because those issuers are already embedded in browser ecosystems, payment systems, or CDN infrastructure—then access to the practical web becomes conditional on having a relationship with one of those issuers.

That is the same structural power dynamic that critics identified in Google's Web Environment Integrity proposal. PACT attests personhood or account standing rather than client integrity, but the power structure is similar: a small number of platforms become the gatekeepers of which clients are treated as legitimate ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)).

### The ratchet effect

PACT tokens are initially optional friction-reducers. That is what makes the centralization risk hard to see. As adoption spreads, however, the **absence** of a token starts to carry information. Defenders rationally adjust: token-bearing traffic gets through cleanly, untokened traffic is challenged more aggressively, and risk thresholds are recalibrated. No single actor decides to make tokens mandatory; it happens through incremental optimization across many sites ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)).

The result is that legitimate traffic with no issuer relationship—internet-wide measurement systems, security research scanners, archival crawlers, RSS readers, Tor users, and alternative browsers—becomes systematically suspect ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)). The open web becomes an access regime with extra friction imposed on whoever does not carry a platform-issued credential.

---

## 3. Evasion and Abuse: The Limits of Contextual Anchors

### Harvesting and purchasing valid tokens

The PACT pipeline is vulnerable to abuse at the token supply level. If malicious actors harvest or buy valid tokens from compromised devices, the system's integrity drops. Rate-limiting token redemption at the verifier level remains necessary precisely because token acquisition may be polluted ([SourceFeed](https://sourcefeed.dev/a/cryptographic-trust-over-tracking-inside-the-pact-protocol)). That admission is important: the cryptographic scheme does not prevent bad tokens from entering circulation; it only prevents certain kinds of linkability.

### Emulation and automated scaling

Without a cryptographic hardware anchor tied to the device, a bot operator does not need to defeat a secure enclave. They need to emulate whatever contextual signals the issuer checks. If the issuer relies on account standing, the operator can automate account creation or buy aged accounts. If the issuer relies on subscription status, the operator can pay for bulk subscriptions and treat that cost as an operating expense. If the issuer relies on issuer vouching, compromised or malicious issuers can vouch for bot accounts.

The attack scenarios listed for security testing include unauthorized endorsement acquisition, token replay, token theft, credential export, anchor impersonation, malicious anchor behavior, Sybil amplification, metadata leakage, and downgrade attacks ([Krishna Gupta](https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/)). These are not exotic theoretical attacks; they follow directly from the fact that the anchor is software-level and therefore duplicable.

### Browser-state compromise

In the browser-mediated design, the browser is supposed to protect credential storage, issuer selection, challenge budgets, and conversion ([GitHub Issue #6](https://github.com/antifraudcg/pact/issues/6)). But if an attacker compromises the browser profile—through malware, credential theft, or simply operating a real browser with stolen session state—the attacker can exercise the same `navigator.pact`-style APIs as the legitimate user. A copied browser profile may carry the credentials needed to obtain new tokens, or may contain already-issued tokens that can be replayed until rate limits trigger.

---

## 4. Privacy Trade-offs: Does Software Anchoring Increase Issuer Metadata Leakage?

### What the issuer sees

In a simple PACT flow, the Attester is "a party that knows something about the user," and the Issuer signs the blinded token ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)). If the Attester is an identity provider, subscription service, or e-commerce platform, then the token-issuing authority sees a meaningful slice of context: which account requested a token, when the request occurred, and possibly payment or standing signals. Blind signatures protect against linkability at the **origin**, but they do not prevent the issuer from knowing that a particular account holder requested issuance.

By contrast, hardware attestation can issue a device-posture token without the origin or verifier collecting user device data ([Cloudflare Blog](https://blog.cloudflare.com/private-attestation-token-device-posture/)). The privacy burden shifts to the device manufacturer or operating system vendor, which is still a concern—Mozilla's warning about platform gatekeepers applies here—but the issuer does not necessarily need a first-party identity relationship with the user. Thus, in the unmodified, first-party-issuer version of PACT, the move away from hardware anchors likely **increases** the metadata footprint exposed to the initial token-issuing authority.

### Mitigations exist but are not guaranteed

The aggregating-issuer proposal in the PACT repository is designed to reduce exactly this risk. An aggregating issuer has no first-party relationship with the user in its aggregating role, receives only unlinkable credential material via transfers, and issues its own access tokens. Its unlinkability holds regardless of the aggregating issuer's behavior ([GitHub Issue #6](https://github.com/antifraudcg/pact/issues/6)). There is also an IssuerHide architecture under discussion that uses zero-knowledge proofs at redemption to hide which issuer produced a credential, avoiding the need for an intermediary entirely ([GitHub Issue #1](https://github.com/antifraudcg/pact/issues/1)).

These are meaningful privacy improvements, but they are **design options**, not properties of PACT as announced. Unless aggregation or issuer-hiding is made a default or mandatory part of the standard, the practical privacy outcome will depend on whether origins and browsers choose to deploy the privacy-preserving variant. The base architecture leaves the initial issuer in a privileged observation position.

---

## 5. Socioeconomic and Digital Exclusion

### Financial signals as personhood signals

If contextual anchors include "active subscription," "account standing," or "credit card status," then the system is no longer merely distinguishing humans from bots. It is distinguishing **consumers with persistent platform relationships** from everyone else. PACT delegates verification to entities that already have an established relationship with the user, such as identity providers, device manufacturers, or platforms like Shopify ([SourceFeed](https://sourcefeed.dev/a/cryptographic-trust-over-tracking-inside-the-pact-protocol)). Those relationships are unevenly distributed across society.

Unbanked and low-income users, people who avoid maintaining accounts with large platforms, and privacy-conscious individuals who refuse persistent online identities may have no usable issuer relationship. If a website configures its trust policy to require tokens from issuers that depend on payment or identity status, those users cannot obtain the credential regardless of how human they are.

### The ratchet makes exclusion worse

The ratchet effect converts this from a minor inconvenience into a structural barrier. When a token is optional, a user without one can still solve a CAPTCHA or accept a challenge. When token absence becomes a risk signal, the same user may be blocked, throttled, or pushed through increasingly aggressive verification. Traffic from internet measurement, security research, archival crawling, RSS readers, Tor users, and alternative browsers is already vulnerable because it has no issuer relationship ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)).

This inverts the intended anti-abuse effect: sophisticated bot operators can often afford to buy accounts or subscriptions, while legitimate low-income or anonymity-seeking users cannot. A CAPTCHA at least can be solved without proving consumer status. A subscription-anchored token cannot.

---

## 6. The “Lemon Problem” of Token Issuers

### No issuer accreditation model exists

PACT does not specify who qualifies as an Attester, and the announcement did not resolve the governance question ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)). That is not a secondary issue; it is the core security issue. A blind-signature token only proves that some issuer signed it. It does not prove that a meaningful personhood or account-quality check occurred.

If many issuers can participate with different standards, the ecosystem faces a classic adverse-selection problem. Low-quality issuers can issue tokens cheaply to anyone. Origins that want to reduce friction may accept those tokens because they convert more legitimate-looking traffic. High-quality issuers that perform expensive account vetting are then undercut. The market selects for lax issuance.

### Malicious and compromised issuers

A malicious issuer can simply issue valid tokens to bots at scale. A compromised issuer can have its signing keys abused for the same purpose. The verifier may not be able to tell the difference between a token from a strict issuer and a token from a negligent one unless it maintains issuer-specific reputation, rate limits, and audit data. Rate-limiting redemption at the verifier level helps reduce damage, but it does not remove the polluted supply ([SourceFeed](https://sourcefeed.dev/a/cryptographic-trust-over-tracking-inside-the-pact-protocol)).

### What is missing

The announced PACT proposal lacks several mechanisms needed to control issuer quality:

| Mechanism | Purpose | Status as of mid-2026 |
|---|---:|---:|
| Issuer accreditation | Define who may issue for the web | Not specified ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)) |
| Public issuer directory | Let origins evaluate issuer quality | Not specified |
| Revocation lists | Remove compromised issuers or tokens | Not specified |
| Audit requirements | Hold issuers accountable for admission quality | Not specified |
| Rate-limited issuance | Prevent bulk token harvesting | Only closest existing draft is `draft-ietf-privacypass-rate-limit-tokens` ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)) |

Without these, PACT is not a trust protocol so much as a **trust-proxy protocol**: it inherits the security posture of whatever issuer an origin happens to configure.

---

## 7. Geopolitical and Sovereign Borders

### The governance blank extends to jurisdiction

The PACT materials reviewed here do not address how issuer requirements interact with national firewalls, data localization laws, or state-mandated digital identity. That is a serious omission because the question of "who controls the trust root" is not only a corporate governance question; it is also a sovereign governance question ([Krishna Gupta](https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/)).

### Government issuers and mandatory trust

If a government demands to become a mandatory PACT token issuer, it could use that position to observe issuance events, deny tokens to disfavored users or classes of traffic, and require browsers or origins within its jurisdiction to accept only state-issued credentials. Even if redemption remains unlinkable to the origin, the state-issuer would still see who requested a token and when. That turns a bot-defense mechanism into a potential access-control instrument.

### Data localization and network sovereignty

National firewalls could block foreign issuer endpoints and compel domestic issuers. Data localization rules could require issuance and attestation servers to be physically located within national borders. Countries could then create distinct trust zones, where a token issued in one jurisdiction is not accepted in another. This would balkanize the web at the protocol layer, not merely at the application layer.

The announcement does not propose a sovereignty model, a jurisdiction-respecting issuer framework, or a mechanism for users to challenge issuer denial. Until that is resolved, PACT's standardization could produce a system that is technically interoperable but politically fragmented.

---

## 8. Longevity and Protocol Decay

### Contextual signals rot faster than hardware signals

An active subscription can expire. Account standing can change. A payment relationship can be closed. Issuer policy can be altered. The contextual signals that anchor PACT today are inherently dynamic. Over a multi-year horizon, bot operators will learn which signals are cheapest to fake and will adapt accordingly.

The protocol will require fallback mechanisms and legacy bot-detection pipelines for older browsers and non-browser clients, creating dual-path maintenance for developers ([SourceFeed](https://sourcefeed.dev/a/cryptographic-trust-over-tracking-inside-the-pact-protocol)). That dual-path burden is not temporary: as long as some legitimate clients lack PACT support or issuer relationships, origin operators must maintain both token-based and legacy challenge systems.

### Browser privacy evolution changes the substrate

PACT credentials are proposed to integrate with `Clear-Site-Data`, Permissions Policy, and process isolation ([GitHub Issue #6](https://github.com/antifraudcg/pact/issues/6)). But browser privacy features continue to change. Third-party cookie bans, storage partitioning, and stricter permission models can alter how tokens are stored, issued, and redeemed. A system that assumes a stable browser-mediated credential store may find that store constrained or partitioned by future privacy designs.

### The agentic AI transition complicates token semantics

PACT is explicitly motivated by the rise of agentic AI traffic ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)). The web is shifting from a simple "human → website" model toward a "human → AI agent → website/API" model ([Krishna Gupta](https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/)). If one human deploys many agents, does each agent get its own token? If they share a token, replay and theft risks increase. If they request delegated issuance, the protocol must include a secure delegation path. None of this is resolved.

### The ratchet accelerates decay

The ratchet effect makes protocol decay more costly than in a truly optional system. Once token-bearing traffic is treated as cleaner and untokened traffic is challenged more, the token credential becomes high-stakes. Attackers invest more to obtain it, which degrades the signal. That in turn pressures adopters to demand stronger anchors—likely hardware attestation. As noted, the end state of that pressure is a slide back toward the Web Environment Integrity model that PACT was meant to avoid ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)).

---

## Conclusion

The shift from hardware anchors to software/contextual anchors is not inherently more private, more decentralized, or more open. It relocates trust from device manufacturers to identity providers, payment platforms, and cloud intermediaries. That trade avoids some of the device-vendor gatekeeping that made Web Environment Integrity unacceptable, but it introduces a different set of problems: Sybil resistance becomes account-fraud resistance, initial issuers gain metadata visibility, and users without platform relationships risk exclusion.

The cryptographic layer is the least controversial part of PACT. Blind signatures and Privacy Pass give plausible unlinkability at the verifier. But the protocol's security ultimately depends on **who is allowed to issue tokens and how tightly their admission process is controlled**. That governance layer is currently absent. PACT does not specify who qualifies as an Attester ([TechTimes](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)), and without accreditation, revocation, auditing, aggregation defaults, and an explicit open-web fallback, the ecosystem will face a market for low-quality issuers, a ratchet toward de facto mandatory credentials, and a new structural dependency on a small set of platforms.

The right time to address these issues is before browser shipping and before widespread origin adoption. The IETF Privacy Pass working group and the rate-limited issuance draft are the most concrete venues for that technical and governance work ([ai.rud.is](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)). If PACT standardizes the mechanism but defers the power questions, the open web will have acquired another trust oligopoly—one that may be cryptographically elegant but still excludes the token-less user and still depends on a handful of commercial gatekeepers.

---

## References

- Cloudflare. (2026, June 23). *Cloudflare, Chrome, and Firefox Plan to Replace CAPTCHAs With Cryptographic Tokens*. TechTimes. [https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm](https://www.techtimes.com/articles/318891/20260623/cloudflare-chrome-firefox-plan-replace-captchas-cryptographic-tokens.htm)

- SourceFeed. (2026, June 23). *Cryptographic Trust Over Tracking: Inside the PACT Protocol*. [https://sourcefeed.dev/a/cryptographic-trust-over-tracking-inside-the-pact-protocol](https://sourcefeed.dev/a/cryptographic-trust-over-tracking-inside-the-pact-protocol)

- SourceFeed. (2026, June 23). *The Cryptographic Battle for the Bot-Era Web*. [https://sourcefeed.dev/a/the-cryptographic-battle-for-the-bot-era-web](https://sourcefeed.dev/a/the-cryptographic-battle-for-the-bot-era-web)

- Cloudflare. (n.d.). *Verify Apple devices with no installed software*. Cloudflare Blog. [https://blog.cloudflare.com/private-attestation-token-device-posture/](https://blog.cloudflare.com/private-attestation-token-device-posture/)

- antifraudcg/pact. (2025, December 18). *Design Proposal for PACT via ACTs with Aggregating Issuers* · Issue #6. GitHub. [https://github.com/antifraudcg/pact/issues/6](https://github.com/antifraudcg/pact/issues/6)

- antifraudcg/pact. (2025, December 18). *Sketching an architecture that uses issuer blinding* · Issue #1. GitHub. [https://github.com/antifraudcg/pact/issues/1](https://github.com/antifraudcg/pact/issues/1)

- hrbrmstr. (2026, June 23). *PACT: The open web doesn’t need another trust oligopoly*. ai.rud.is. [https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/](https://ai.rud.is/posts/2026-06-23-pact-the-open-web-doesnt-need-another-trust-oligopoly/)

- Gupta, K. (2026, June). *PACT — Private Access Control Tokens: A Privacy-Preserving Trust Architecture for Humans and AI Agents on the Web*. Krishna Gupta. [https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/](https://krishnag.ceo/blog/pact-private-access-control-tokens-a-privacy-preserving-trust-architecture-for-humans-and-ai-agents-on-the-web/)