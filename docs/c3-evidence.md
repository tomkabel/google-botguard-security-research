# C3 evidence: attestation-market centralization

Scope: reviewer requests (a) to (c) on C3 and the rate-limiting question from one board. Sources are primary only (IETF, RFC Editor, GitHub repos of the proposers, Apple/Google/Cloudflare developer docs and vendor posts). All were fetched on **2026-09-24** with the `firecrawl` CLI, or with `gh api` for GitHub repository contents. `paper.md` was not edited.

Citation labels `[Nk]` are placeholders; their entries are in §6. Paper numbering was renumbered during this work (commit 393912e: PACT is now [9], Chu et al. [8], Kreuter et al. [7], PST spec [23]), so the old numbers below follow the current `paper.md`.

---

## 1. Counts

| Party class | Count (as of 2026-09-24) | Source | Knowable? |
|---|---|---|---|
| PAT attesters | **1** (Apple). No other PAT attester is documented. | [1] WWDC22 t=383 s; [N5] | Named set only |
| PAT issuers, publicly named | **2** (Cloudflare, Fastly). Apple: "You can test with token issuers from Cloudflare and Fastly" [N5]. WWDC22: "there are two token issuers that you can already start testing with. Fastly and Cloudflare" and "Issuers will be able to sign up later this year at register.apple.com" [1, t=490–517 s]. | [1], [N5] | **Total unknowable.** Apple publishes no list of issuers registered through register.apple.com. |
| Privacy Pass (non-PAT) attesters in Cloudflare's client | **1 operator**. Silk's README lists "Privacy Pass Attesters: Cloudflare Research with Turnstile". The source's defaults are `pp-attester-turnstile.research.cloudflare.com` and its `-dev` twin. | [N7] | Yes, for the default client config |
| Privacy Pass issuers named in Cloudflare docs | **2**: "Cloudflare Managed Challenge is a Privacy Pass origin serving two Privacy Pass challenges: one for Apple PAT Issuer, one for Cloudflare Research Issuer." | [N6] | Only Cloudflare's own view |
| Other Privacy Pass issuers from vendor announcements | **1** found: Kagi runs "all the 'Server roles' (Attester, Issuer, Origin)" in the RFC 9576 §4.1 shared model (Feb 13, 2025). | [N8] | **Total unknowable.** RFC 9576–9578 define no issuer registry, and any origin may run a joint issuer. The RFCs name no deployed issuer. |
| Chrome PST issuers, registry entries | **9** entries in `pst-issuers.json` (commit `fd735c7`, 2026-08-23). **7** are third-party (hCaptcha, Polyset, CaptchaFox, AUTHFY, Amazon Ads, ClearSale, Contentpass). **2** are Chromium/Google demo issuers (`trusttoken.dev`, `privatetokens.dev`). | [N3] | Yes |
| Chrome PST issuers, unexpired on 2026-09-24 | **1** (Amazon Ads, expiry 2027-06-01). The other 8 expired between 2023-11-24 and 2026-08-24; Contentpass lapsed 2026-08-24 and its renewal (issue #62) is still open. Registration rule: entries expire "6 months after the issuer request has been filed" and "Expired issuer entries will result in invalid tokens". 3 new issuer requests are pending (HeatToken #12, MAIL.RU #27, TruSources #47). | [N3] | The file is knowable. Whether Chrome's server-side key distribution enforces each expiry cannot be observed from public data. |
| PACT participants named | **5 organisations**: Cloudflare, plus "Mozilla, Google, Microsoft, and Shopify" [9] (quote verified in `docs/pact-sources.md`, C12). MoLE draft authors: **3** (S. Schlesinger, Google LLC; D. Jackson, Mozilla; T. Meunier, Cloudflare) [88, header]. | [9], [88] | Yes |
| PACT implementers named | **0**. `antifraudcg/pact` has a 7-byte README (`# pact`), 1 commit, and 12 issues opened by 7 distinct GitHub accounts. MoLE's Acknowledgments read "TODO acknowledge." [88]. MoLE is still at -00 (2026-07-06), individual, with no stream. | [112], [88] | Named set only; no deployment exists |

---

## 2. Rate-limit roles: who enforces per-client limits

**Short answer.** RFC 9576–9578 do not assign per-client rate limiting to any role. RFC 9576 §7.1 says: "Rate-limiting issuance, at either the Client, Attester, or Issuer, can also help mitigate these attacks." The IETF protocol that does specify it, draft-ietf-privacypass-rate-limit-tokens-06 [N1], puts **enforcement on the Attester**. The Issuer only supplies the per-Origin limit value and learns the Origin but not the Client. Paper §6.3 says the *issuer* counts, which is wrong for split deployments (see §5).

**Draft status.** The draft is still named `draft-ietf-privacypass-rate-limit-tokens`. It is a privacypass WG document, latest revision -06 of 2024-04-01, intended status Experimental, with IESG state "Expired". It replaces `draft-privacypass-rate-limit-tokens` and `draft-private-access-tokens`. Its authors are from Google, Fastly, Apple, Google and Cloudflare. The WG's later rate-limiting work, ARC (`draft-ietf-privacypass-arc-protocol-01`, 2026-03-02) [N2], is now marked "Dead WG Document". Cite [N1] alongside [8].

### RFC 9576 (architecture) [4]
- §3.5.1: "Issuers trust Attesters to perform attestation correctly". Also: "Clients trust the Attester to not share any Client-specific information with the Issuer."
- §4.4 (Split Origin, Attester, Issuer): "This is the most general deployment model and is necessary for some types of issuance protocols where the Attester plays a role in token issuance; see [RATE-LIMITED]". And: "the Attester sees potentially sensitive Client-identifying information, such as account identifiers or IP addresses; the Issuer sees only the information necessary for issuance; and the Origin sees token challenges, corresponding tokens, and Client source information, such as their IP address."
- §4.2 (Joint Attester and Issuer): issuance protocols in which the Issuer learns the Origin, "such as the issuance protocol described in [RATE-LIMITED], are not appropriate". So rate-limited issuance requires the split model.
- §5.2: "A consequence of limiting the number of participants (Attesters or Issuers) in Privacy Pass deployments for meaningful privacy is that it forces concentrated centralization among those participants."
- §7.1: "Rate-limiting issuance, at either the Client, Attester, or Issuer, can also help mitigate these attacks." The RFC does not choose which.

### RFC 9577 (HTTP auth scheme) [36]
- §3.1: "if a Client's ability to generate tokens via an Attester and Issuer is limited to a certain rate, a malicious Origin could send an excessive number of token challenges ... Clients SHOULD have some implementation-specific policy to minimize the number of tokens that can be retrieved by Origins."
- §4: "Origins SHOULD minimize the number of challenges sent to a particular Client context ... to avoid overwhelming Clients and Issuers with token requests that might cause Clients to hit rate limits."
- The only enforcement it specifies is Origin-side double-spend prevention (§2.2.2: "Origins SHOULD implement some form of double-spend prevention").

### RFC 9578 (issuance protocols) [37]
- Defines only the VOPRF (type 1) and blind-RSA (type 2) exchanges. It contains no per-client limit; "rate limit" does not occur in the text. The ARC draft describes these as "one-time-use" tokens that "cannot be used by the server to rate limit a specific client. This is because there is no mechanism in the issuance protocol to link repeated Client token requests" [N2, §2].

### draft-ietf-privacypass-rate-limit-tokens-06 [N1]
- **What the Attester learns** (§1.3): "The Attester knows the Client's identity and learns the Client's public key (Client Key), the Issuer being targeted (Issuer Name), the period of time for which the Issuer's policy is valid (Issuer Policy Window), the number of tokens the Issuer is willing to issue within the current policy window, and the number of tokens issued to a given Client for the claimed Origin in the policy window. The Attester does not know the identity of the Origin ..., but knows a Client-anonymized identifier for it (Client's Origin Alias)."
- **What the Issuer learns** (§1.3): "The Issuer knows a per-Origin secret (Issuer Origin Secret) and policy about client access, and learns the Origin's identity (Origin Name) during issuance. The Issuer does not learn the Client's identity or information about the Client's access pattern."
- **Origin** (§1.3): "The Origin does not learn which Attester was used by a Client for issuance."
- **Client identifier** (§1.3): "An Attester is expected to employ a stable Client identifier, such as an IP address, a device identifier, or an account at the Attester". Also: "An Issuer therefore chooses to issue tokens to only known and reputable Attesters".
- **Attester state** (§5.1.2): "Attesters MUST NOT allow Clients to change their Client Key more than once within a policy window". It keeps "A counter of successful tokens issued" per (Client Key, Client's Origin Alias, policy window).
- **Issuer state** (§5.1.3): "For each Origin, Issuers need to know what rate limit to enforce during a policy window". The Issuer sets the value; it does not hold per-client state.
- **Enforcement** (§5.5.2): "If the count is greater than or equal to the limit, the Attester drops the token and responds to the client with an HTTP 429 (Too Many Requests) error."
- **Enforcement and centralization** (§8.6): "The rate limit is enforced by the Attester based on state about the Client that only the Attester holds". Also: "Issuers need to be selective in which Attesters they allow, to ensure that a single Client cannot trivially work with many Attesters in order to exceed the rate limit." And: "Since the effectiveness of the rate limit requires a bounded set of Attesters for any particular use case, deployments need to consider the impact on centralization".
- **Collusion** (§9.6): "Issuers and Attesters should be run by mutually distinct organizations". "If a Attester and Origin are able to collude, they can correlate a client's identity and origin access patterns through timestamp correlation."

**Contrast, ARC [N2].** Per-context limits are enforced at presentation by the Origin, which checks presentation tags: §8.2, "the Origin SHOULD perform a check that the tag output from VerifyPresentation has not previously been seen". §9: "ARC requires a joint Origin and Issuer configuration given that it is privately verifiable." Per-client supply of credentials still rests on attestation at issuance.

§8.6 of [N1] is the IETF's own statement of the trilemma. Goal (ii) is enforced by the party that knows identity, and it holds only if the set of such parties stays bounded, which gives up (iii).

---

## 3. Trilemma table

Goals: (i) redemptions unlinkable to identities; (ii) bounded per-client token supply; (iii) no small set of trusted parties. Paper numbers are used where they exist; `[Nk]` entries are in §6.

| Scheme | (i) Unlinkable | (ii) Bounded supply | (iii) No small set | Source |
|---|---|---|---|---|
| Privacy Pass (Cloudflare, CAPTCHA) | Yes | No: per solve | No: CF attester + issuer | [4 §7.1, N6, N7] |
| Apple PATs | Yes | Partial: Apple "can" | No: 1 attester | [1, 4, N5] |
| Rate-limited PATs | Yes, absent collusion | Yes: Attester, per origin | No: "bounded set" | [N1 §1.3, §8.6] |
| Chrome PST | Partial: ≤6 keys | Partial: browser caps | Partial: Chrome registry | [N3, N4] |
| PACT/MoLE | Yes (goal) | Partial: Anchor-bound | Partial: scale favours Moderators | [88 §7.1, §7.3, §9.3] |
| WEI (withdrawn) | Partial: no device ID | Partial: proposed | No: platform attester | [N9] |
| Play Integrity | No: Google decrypts | Partial: activity level | No: Google | [N11, N12] |
| App Attest | No: per-install key | Partial: 30-day key count | No: Apple | [N14–N16] |

Cell justifications (the table must stay short; these belong in a footnote or the artifact):
- **Privacy Pass (CF).** (i) Blind RSA, publicly verifiable. (ii) Tokens are issued per Turnstile solve, so supply is bounded by solve cost, not by client identity. Tokens can be pooled ("hoarding attack", RFC 9576 §7.1). (iii) The default client trusts one attester operator, Cloudflare Research [N7].
- **Apple PATs.** (ii) "This attester can also perform rate-limiting" [1, t=383 s]. No limit values are published. iOS 16/Ventura support token type 2 only [N5]; we found no evidence that the rate-limited type is deployed.
- **Rate-limited PATs.** (i) Holds only under non-collusion [N1 §9.6]. The draft expired in 2024 with no deployment evidence.
- **Chrome PST.** (i) "there is a limitation of six keys per issuer" [N4], so the key choice carries ~2.6 bits. (ii) "Each device can store up to 500 tokens per top-level website and issuer" and "a limit of two token redemptions per device and issuer every 48 hours" [N4]. The browser enforces both; our reading is that a fresh profile or a modified client resets them. (iii) Anyone can file a GitHub issue, but Chrome merges it; 1 of 9 entries was unexpired on 2026-09-24 [N3].
- **PACT/MoLE.** (i) "The presentation must not be linkable to past updates, or to the Redeem & Issue flow" [88 §7.3]. (ii) "Anchors will need to constrain how many times they will Endorse a given user" [88 §7.1], with no enforcement or audit. (iii) Each Moderator picks its Anchors, but "Moderators inherently benefit from scale" [88 §9.3].
- **WEI.** (i) "We strongly feel the following data should never be included: A device ID". The explainer was only "researching an issuer-attester split", and websites could query the attester "to detect potentially hyperactive devices" [N9]. (ii) "Some indicator enabling rate limiting against a physical device" was listed as under discussion [N9]. (iii) Attesters "will typically come from the operating system (platform)", e.g. "Google Play" [N9].
- **Play Integrity.** (i) "By default, Google Play manages response encryption, meaning your backend calls Google's server to decrypt verdicts" [N12 setup]. Device recall stores per-device bits "on Google's servers ... even after your app is reinstalled or the device is reset" [N11]. (ii) `recentDeviceActivity` LEVEL_1–4 counts integrity-token requests "on this device in the last hour per app" [N12]. It is a signal the app must act on, not a cap. (iii) Google only.
- **App Attest.** (i) The server stores the attested key and every later assertion is signed with it [N14], so requests from one install are linkable by design. (ii) Risk metric: "the number of attested keys associated with a given device over the past 30 days" [N15]. DeviceCheck adds "two per-device binary digits stored on an Apple server" [N16]. (iii) Apple only.

---

## 4. Precedents paragraph (drop-in for §6.3)

Platform attestation is the deployed precedent for (ii). Google's SafetyNet Attestation API "was deprecated in 2022 and fully turned down in January 2025" in favour of the Play Integrity API [N13]. Play Integrity returns Google-issued device verdicts and, on request, a per-app count of recent token requests, because "High-volume-activity abusers commonly generate valid attestation results from real devices and provide them to bots" [N11, N12]. Apple's App Attest certifies a per-install hardware key and reports how many keys a device attested in 30 days, and DeviceCheck stores two bits per device [N14–N16]. Web Environment Integrity, posted on April 25, 2023, proposed such verdicts for the web. It named App Attest and Play Integrity as inspiration and "Google Play" as an example attester, and it rejected fully masked PATs because attesters would get no feedback on errors [N9]. Google marked it "no longer pursued" on November 2, 2023, citing only "We've heard your feedback" [N9, N10]; all three meet (ii) through one vendor and relax (i) or (iii).

(6 sentences. It adds text; paired with the cuts in §5 it still needs about 4 lines elsewhere.)

---

## 5. Wording corrections (new ≤ old)

Lengths were computed against current `paper.md` with 3-digit reference numbers ([120] for [N1], [122] for [N3]). Each OLD string occurs exactly once.

1. **§6.3, trilemma paragraph (factual error: in split deployments the Attester counts, not the Issuer [N1 §8.6]).** 109 → 108 chars.
   - OLD: `A scheme meeting (i) and (ii) must rate-limit on something the issuer can count without identifying the user.`
   - NEW: `A scheme meeting (i) and (ii) needs a per-client unit that, in split deployments, the Attester counts [N1].`
2. **§6.3, trilemma paragraph (cite the IETF draft, not only [8]).** 107 → 104 chars.
   - OLD: `Constructions such as [7, 8] make issuance unlinkable and rate-limited but do not analyze market structure.`
   - NEW: `Constructions [7, 8, N1] make issuance unlinkable and rate-limited but do not analyze market structure.`
3. **§6.3, PST bullet (adds the count).** 61 → 55 chars.
   - OLD: `Concentration is in the browser vendor's issuer registration.`
   - NEW: `Chrome gates issuers; 1 of 9 listed is unexpired [N3].`
4. **§5.6, `R` definition (outside §4.4/§6.3, same citation issue).** 62 → 53 chars.
   - OLD: `per-origin limit needs the rate-limited issuance extension [8]`
   - NEW: `per-origin limit needs rate-limited issuance [8, N1]`

No change is needed in §4.4. "Apple is the only attester and Cloudflare and Fastly are issuers" is supported by [1] and [N5]. The sentence does not claim they are the *only* issuers, which the public data could not support. "iOS 16+/macOS Ventura+" matches [N5]. The §6.3 Apple bullet ("can also perform rate-limiting", no published per-device limits) is supported by [1].

---

## 6. Reference entries (paper style; assign numbers from [120])

**[N1]** S. Hendrickson, J. Iyengar, T. Pauly, S. Valdez, and C. A. Wood. "Rate-Limited Token Issuance Protocol." *Internet-Draft draft-ietf-privacypass-rate-limit-tokens-06* (privacypass WG; expired), IETF, April 1, 2024. URL: https://datatracker.ietf.org/doc/draft-ietf-privacypass-rate-limit-tokens/. Accessed September 24, 2026.

**[N2]** C. Yun, C. A. Wood, and A. Faz-Hernandez. "Privacy Pass Issuance Protocol for Anonymous Rate-Limited Credentials." *Internet-Draft draft-ietf-privacypass-arc-protocol-01* (privacypass WG; dead WG document), IETF, March 2, 2026. URL: https://datatracker.ietf.org/doc/draft-ietf-privacypass-arc-protocol/. Accessed September 24, 2026.

**[N3]** Google Chrome. "Private State Tokens Issuer Registration" and `pst-issuers.json` (commit fd735c7, August 23, 2026). *GoogleChrome/private-tokens*, GitHub. URL: https://github.com/GoogleChrome/private-tokens. Accessed September 24, 2026.

**[N4]** Google. "Private State Tokens developer guide." *Privacy Sandbox*. URL: https://privacysandbox.google.com/protections/private-state-tokens/developer-guide. Accessed September 24, 2026.

**[N5]** Apple Inc. "Challenge: Private Access Tokens." *Apple Developer News*, June 9, 2022. URL: https://developer.apple.com/news/?id=huqjyh7k. Accessed September 24, 2026.

**[N6]** T. Meunier, C. D. Rubin, and A. Faz-Hernández. "Privacy Pass: Upgrading to the Latest Protocol Version." *Cloudflare Blog*, January 4, 2024. URL: https://blog.cloudflare.com/privacy-pass-standard/. Accessed September 24, 2026.

**[N7]** Cloudflare, Inc. "Silk – Privacy Pass Client" (README and default attester configuration). *cloudflare/pp-browser-extension*, GitHub. URL: https://github.com/cloudflare/pp-browser-extension. Accessed September 24, 2026.

**[N8]** Kagi Inc. "Introducing Privacy Pass Authentication for Kagi Search." *Kagi Blog*, February 13, 2025. URL: https://blog.kagi.com/kagi-privacy-pass. Accessed September 24, 2026.

**[N9]** B. Wiser, B. Benko, P. Pfeiffenberger, and S. Kataev. "Web Environment Integrity Explainer." *explainers-by-googlers/Web-Environment-Integrity*, GitHub, April 25, 2023; marked "no longer pursued" November 2, 2023. URL: https://github.com/explainers-by-googlers/Web-Environment-Integrity. Accessed September 24, 2026.

**[N10]** Android team. "Increasing Trust for Embedded Media." *Android Developers Blog*, November 2, 2023. URL: https://android-developers.googleblog.com/2023/11/increasing-trust-for-embedded-media.html. Accessed September 24, 2026.

**[N11]** Google. "Play Integrity API overview." *Android Developers*. URL: https://developer.android.com/google/play/integrity/overview. Accessed September 24, 2026.

**[N12]** Google. "Integrity verdicts" and "Set up the Play Integrity API." *Android Developers*. URL: https://developer.android.com/google/play/integrity/verdicts. Accessed September 24, 2026.

**[N13]** Google. "About the SafetyNet Attestation API deprecation." *Android Developers*. URL: https://developer.android.com/privacy-and-security/safetynet/deprecation-timeline. Accessed September 24, 2026.

**[N14]** Apple Inc. "Establishing Your App's Integrity." *Apple Developer Documentation (DeviceCheck)*. URL: https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity. Accessed September 24, 2026.

**[N15]** Apple Inc. "Assessing Fraud Risk." *Apple Developer Documentation (DeviceCheck)*. URL: https://developer.apple.com/documentation/devicecheck/assessing-fraud-risk. Accessed September 24, 2026.

**[N16]** Apple Inc. "Accessing and Modifying Per-Device Data." *Apple Developer Documentation (DeviceCheck)*. URL: https://developer.apple.com/documentation/devicecheck/accessing-and-modifying-per-device-data. Accessed September 24, 2026.

To save space: [N11]/[N12] and [N14]–[N16] can each be merged into one entry, and [N7], [N8], [N13] can be dropped if the table footnote is cut.
