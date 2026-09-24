# PACT claims: primary-source audit

Scope: every sentence in `paper.md` that cites [40] (Gupta, krishnag.ceo) or [88] (Rudis, ai.rud.is), plus every PACT sentence without a citation. Sources were fetched on September 24, 2026 with the `firecrawl` CLI. A quote appears below only if it occurs in the fetched page text. Quotes from GitHub issues keep the authors' spelling.

Classes: **(a)** a primary source supports the claim; **(b)** opinion found only in a blog, so the text must name the author; **(c)** unsupported or out of date, so delete it or soften it.

## 0. Findings that change the picture

1. **The PACT architecture now has an IETF draft.** Mozilla's technical post [N1] says the drafts will be taken to the IETF and the W3C, and links to the `Moderation-of-unLinkable-Endorsements` GitHub organisation. That organisation describes MoLE as "a standardization project which began within the Anti-Fraud Community Group at the W3C". Its architecture draft is `draft-jms-mole-architecture-00` [N2]: S. Schlesinger (Google), D. Jackson (Mozilla) and T. Meunier (Cloudflare), dated 6 July 2026, "Intended status: Informational", an individual draft with "no formal standing". The paper's line "no IETF draft under the PACT name, and no issuance-governance specification" (§6.4) is therefore out of date. It is literally true that no draft carries the PACT name, but the claim misleads.
2. **The design changed after issue #6.** [39] is a March 2026 sketch in which origins pick "up to two" aggregating issuers. The public design [N1, N2] instead uses Anchors (which issue Endorsements) and a Moderator (which issues stateful Credentials), and says "we limit each site to nominating a single Moderator." Redemption hides the Anchor. So the §6.4 sentence "the token still reveals which issuer key signed it" does not hold for PACT. It describes PATs.
3. **Revocation is specified.** Two sources describe it: "Revocation falls out of the same mechanism: a Moderator can refuse to return an updated Credential" [N1], and "There is no need for revocation lists or proofs of nonmembership" [39]. The paper says revocation is absent in §4.4 and §6.4, and both places need correcting.
4. **Most of what [40] and [88] are cited for does not appear in them.**
   - Gupta [40] summarises the Mozilla post: "Mozilla describes such an entity as an **Anchor**". He never mentions unbanked, low-income or anonymity-seeking users.
   - Rudis [88] never mentions a public issuer directory, revocation lists, audits, delegation semantics, credential stuffing, stolen session tokens or redemption-side rate limiting. He argues for rate-limited *issuance*.
   - After the fixes below, [88] is kept only for opinions that are attributed to Rudis, and [40] is no longer cited anywhere, so it can be dropped from the reference list.
5. **A quote is misattributed.** The §4.4 quote "knows something about the user" [11, 39] does not appear in [11], [39], [N1], [N2], [N3], [88] or [40].
6. **Reference errors (not edited here):**
   - [39] gives the date as "December 18, 2025". Issue #6 was "opened on Mar 30, 2026". December 18, 2025 is the date of issue #1, which is [108].
   - §3 (l.125) calls PACT "standards-track". [N2] is an individual Informational draft.
   - §6.4 says "Blind signatures". The designs under discussion use Anonymous Credit Tokens (ACT) and Anonymous Rate-Limited Credentials (ARC) [N3], not blind RSA.

## 1. Claim table

| # | Loc. | Paper sentence (abridged) | Class | Primary source | Supporting quote (verbatim from fetched text) |
|---|---|---|---|---|---|
| C1 | §2 l.84 | "PACT [11] attests personhood or account standing through *issuer judgment* rather than hardware [39, 40]." | a | N1 | "However, hardware is just one option for scarcity." / "To a user who meets the Anchor’s criteria, like having a subscription, an account in good standing, or a verified phone number, an Anchor issues a batch of Endorsement tokens, following the Privacy Pass model." |
| C2 | §4.2 l.242 | "PACT also treats the browser as a trusted user-agent [39], an assumption that fails when a copied or compromised profile can exercise the same issuance APIs as a legitimate user [39, 88]." | a (the "fails" clause is the authors' analysis, which N2 supports) | [39]; N2 | [39]: "User-agent behind the API. Mediates credential storage, issuer selection, challenge budgets, and conversion." N2 §6: "Can control a number of Clients and deviate from the protocol." (Rudis's nearest phrase is "compromised-but-attested clients minting on behalf of whoever pays", which does not mention profiles or APIs.) |
| C3 | §4.3 l.264 | "Bulk registration, credential stuffing, stolen session tokens and cheap subscriptions feed token farming [88]." | a (the designers expect farming; the list of inputs is the authors' analysis) | N5; N1; N2 | N5: "Our thesis is that we expect malicious bots to obtain PACT tokens, but that in order for them to be useful at scale, they would effectively need to be well-behaved to accrue a positive endorsement over time." N1: "A paid subscription costs an attacker the same as a real user." N2 §9.1: "if a malicious user can perform X queries before their credential is revoked and they have E endorsements then their total access is X * E." |
| C4 | §4.3 l.264 | "...so verifier-side redemption rate limiting remains necessary for any anchor [88]." | a | N3 | "Sites and their embedded partners can ensure that any tokens derived from a trusted credential cannot be used on their site more than a certain limit per set timeframe." |
| C5 | §4.4 l.280 | "PACT [11] extends issuance to any party that "knows something about the user" [11, 39]." | c (the quote is not in any source) | N3; [11] | N3: "Any entity or organization may provide credentials to users, and can choose how they want to represent them." [11]: "Private Access Control Tokens (PACT) are designed to allow sites with strong knowledge of “personhood” to issue anonymous tokens." |
| C6 | §4.4 l.280 | "This addresses reason 1 only by multiplying security-critical parties." (no citation) | a (the authors' analysis, which N1 supports) | N1 | "If an issuer misbehaves then the site’s rate limits become ineffective, enabling volumetric abuse." |
| C7 | §4.4 l.280 | "It worsens reason 2, as no issuer accreditation, revocation or audit regime has been specified (§6.4) [11, 88]." | c (revocation is specified; the accreditation and audit parts are supported) | N2; N4; N1 | N2 §9.3: "MoLE allows each Moderator to make an independent decision about which anchors to trust rather than requiring shared Issuers to be established and coordinated." N2 §8: "TODO: Discuss use of DAP / PPM / Prio". N4: "Does this necessitate centralization, and if so, do we want to pursue some kind of public governance structure?" N1: "Revocation falls out of the same mechanism: a Moderator can refuse to return an updated Credential." |
| C8 | §4.4 l.280 | "It worsens reason 3, as unbanked, low-income and anonymity-seeking users may lack a usable issuer [40]." | c ("worsens" and the user groups are not in [40]) | N4; N1 | N4: "How do we make sure smaller anchors are accepted at scale so that our goal of anyone in the world can get a useable anchor?" N1: "If the user has no Endorsements from suitable Anchors at all, existing mechanisms (CAPTCHAs, account creation, federated login) could be used to bootstrap a Credential the same way, so the system degrades to today’s experience rather than locking the user out." |
| C9 | §6 l.456 | "Industry deployment over 2024–2026 has advanced along three tracks: … (Privacy Pass, Apple PATs, PACT)." (no citation) | c (PACT is not deployed) → soften | [11] | "committing to developing and submitting for standardization a privacy-preserving protocol to help humans and bots prove that their traffic is not malicious" |
| C10 | §6.2 l.477 | "It adds no hardware root; it concentrates the judgement of which parties may vouch that a person is present (§6.4)." (the PACT clause has no citation) | a (the second clause is the authors' analysis, which the designers dispute) | N1; N2 | N1: "However, hardware is just one option for scarcity." N2 §9.3: "MoLE aims to avoid the same centralization risk through a number of mechanisms." |
| C11 | §6.4 l.485 | "It is a proposal: there is no deployment timeline, no IETF draft under the PACT name, and no issuance-governance specification." (no citation) | c (out of date; see §0.1) | N1; N2 | N1: "The IETF is the natural venue for the cryptographic protocols underneath, and the W3C for the WebAPI surface that sits on top." N2: "Intended status: Informational" and "6 July 2026". (The "no deployment timeline" part: neither [11] nor N1 gives a date. Rudis also says so: "There’s no deployment timeline, no IETF draft under a PACT name".) |
| C12 | §6.4 l.485 | Announcement date, partners, "to be standardized", personhood quote [11]; builds on Privacy Pass; design work from December 2025 [107] | a | [11]; N3; [108] | [11]: "San Francisco, CA, June 22, 2026" and "New Private Access Control Tokens (PACT) technology, developed alongside Mozilla, Google, Microsoft, and Shopify". N3: "The proposed mechanism is based on cryptography being explored in the Privacy Pass working group." N3 was opened on Dec 2, 2025 and issue #1 on Dec 18, 2025. |
| C13 | §6.4 l.487 | "PACT breaks with the hardware anchor behind Type IV's Tier 1 classification (§4.2)." (no citation) | a | N1 | "However, hardware is just one option for scarcity." |
| C14 | §6.4 l.487 | "PACT accepts *software or contextual anchors*: active subscriptions, account standing, first-party relationships, or issuer vouching [39, 40]." | a (re-source to N1) | N1; N2 | N1 quote as in C1. N2 §4: "The nature of the trust relationship is specific to the Anchor and may be based on some kind of strong authentication, e.g. a login, or may be relatively weak, e.g. based on solving a CAPTCHA." |
| C15 | §6.4 l.487 | "This relocates the Sybil problem rather than removing it. The attacker's unit of scarcity becomes a credentialed account." (no citation) | a (authors' analysis) | N2 | N2 §9.1 X * E quote (C3). |
| C16 | §6.4 l.487 | "Bulk registration, credential stuffing, stolen session tokens, and cheap subscriptions are automatable inputs to token farming upstream of the protocol [88]." | a (re-source); the list is the authors' analysis | N5; N2 | As in C3. |
| C17 | §6.4 l.487 | "Under Operator Synthesis it is not a trust anchor, because an operator may control the profile, the device, or both." (no citation) | a (authors' analysis) | N2 | "Can control a number of Clients and deviate from the protocol." |
| C18 | §6.4 l.487 | "Blind signatures make a redeemed token unlinkable to its issuance, but the token still reveals which issuer key signed it." (no citation) | c (wrong for PACT: the Anchor is hidden, and the designs use ACT/ARC, not blind signatures) | N2; N1 | N2: "Redeeming an Endorsement does not reveal which Anchor was used, only that it came from the Anchor Set." N1: "Because the Moderator can’t see which Anchor backed a Credential at issuance, it can’t give a Credential from a strong Anchor more access than one from a weak Anchor" |
| C19 | §6.4 l.487 | "Its value depends entirely on the issuer's admission process." (no citation) | a | N2 | "Cannot violate the endorsement criteria of a Moderator's trusted Anchors but may control other Anchors." |
| C20 | §6.4 l.489 | "Origins configure up to two aggregating issuers and a credit cost per request [39]." | a for the March 2026 sketch, but superseded | [39]; N1 | [39]: "Configures which aggregating issuers (up to two) it trusts and the credit cost per request." N1: "we limit each site to nominating a single Moderator." |
| C21 | §6.4 l.489 | "This makes issuer choice a gatekeeping decision and Cloudflare a natural central participant [88]." | a (centralisation risk, in the designers' own words); the Cloudflare framing appears in [11] itself | N1; N2; [11] | N1: "Enabling Moderators that cover many sites carries a centralisation risk, similar to the concentration we see today in anti-abuse providers." N2 §9.3: "Moderators inherently benefit from scale". [11]: "Using PACT on Cloudflare’s network raises the bar for trustworthiness and integrity online without the traditional costs." |
| C22 | §6.4 l.489 | "As adoption spreads, the absence of a token carries information: untokened traffic is challenged more aggressively, and no single actor decides to make tokens mandatory [88]." | b | [88] only | "As adoption spreads, the _absence_ of a token starts to carry information." / "Follow that trajectory to its end and the token stops being optional, even though no one decided to require it." |
| C23 | §6.4 l.489 | "Legitimate traffic with no issuer relationship (measurement systems, …, alternative browsers) becomes systematically suspect [88]." | b (the designers intend a fallback: N1, N3) | [88]; counterpoint N1 | [88]: "legitimate use cases with no issuer relationship and therefore no token". N1: the fallback quote in C8. N3: "does not become so critical that sites would exclude access to services without the signal" |
| C24 | §6.4 l.489 | "PACT as announced has no issuer accreditation, public issuer directory, revocation lists, or audit requirements [88]." | c (directory, revocation lists and audit are not in [88]; revocation lists are unnecessary by design [39]) | N2; N4; [39] | N2 §8 "TODO" quote; N4 governance quote (C7). [39]: "There is no need for revocation lists or proofs of nonmembership." Rudis's nearest phrase: "while the issuer accreditation model is still a blank page". |
| C25 | §6.4 l.489 | "Low-quality issuers can then undercut high-quality ones, and a token proves only that *some* issuer signed it, not that a meaningful personhood check occurred." (no citation) | a | N1; N2 | N1: "The initial access has to be uniform across the Moderator’s whole pool of Anchors, which in practice means setting it at the strength of the weakest." N2 §4 CAPTCHA quote (C14). |
| C26 | §6.4 l.489 | "Account-standing anchors favor users with persistent platform relationships: bot operators can afford accounts, while low-income or anonymity-seeking users cannot [40]." | c (not in [40]) | N1 | "A paid subscription costs an attacker the same as a real user." |
| C27 | §6.4 l.489 | "PACT is motivated by agentic AI traffic [11], yet its semantics for human → AI agent → website delegation are unresolved [88]." | c (not in [88]; N2 §2.2 addresses delegation) | [11]; N2; N1 | N2 §2.2: "distinguishability via request content, timing, or rate is the user agent's responsibility, not the Credential's." N1: "An agent can carry its user’s Credentials, in which case the user remains accountable for how the agent behaves." |
| C28 | §6.4 l.489 | "Until issuer governance is specified, PACT inherits the security posture of whatever issuer an origin configures [88]." | a (re-source) | N2 | N2 §10.1: "Anchor key compromise will enable an attacker to produce as many endorsement as they wish." (spelling as in the draft) |
| C29 | §7.2 l.505 | "For PACT, aggregating-issuer and IssuerHide designs [39, 108] would mitigate initial-issuer metadata exposure, but they remain options rather than defaults, and no decentralized issuer network has been specified [11, 88]." | c ("options rather than defaults" is out of date: Anchor-hiding is a core goal in N2) | N2 | N2 §5: "Endorsement Redemptions are Anchor-hiding". N2 §9.3 quote (C7). |
| C30 | §4.2 l.242 | "Software-anchored variants do not qualify." (no citation) | n/a (authors' analysis; no source needed) | none | none |
| C31 | §4.3 l.264 | "PACT-style anchors replace the device-compromise ceiling with an account-acquisition ceiling (§6.4)." (no citation) | a (authors' analysis) | N2 | X * E quote (C3). |
| C32 | §3 l.155 | "Examples: Apple PATs, Cloudflare/Fastly Privacy Pass issuance, PACT (proposed)." (no citation) | a | [11] | As in C12. |
| C33 | §3 l.129 | "Snowballing and announcements added recent work (… PACT …)" (no citation) | n/a (methodology statement) | none | none |

**Counts** (33 claims): **(a) 19**, **(b) 2**, **(c) 10**, plus **2 n/a**.
- **(a)** C1, C2, C3, C4, C6, C10, C12, C13, C14, C15, C16, C17, C19, C20, C21, C25, C28, C31, C32. Six of these are the authors' own analysis, which a primary source now supports: C6, C15, C17 and C31, plus the analysis parts of C2 and C3.
- **(b)** C22 and C23, both Rudis. The text must name him ("Rudis argues").
- **(c)** C5 (quote not found in any source), C7 (revocation), C8, C9, C11 (out of date), C18 (wrong for PACT), C24, C26, C27, C29. Each gets a softened, re-sourced replacement in §3; none needs deleting.
- **n/a** C30 and C33 (authors' analysis and methodology; no source needed).

## 2. New reference entries

**[N1]** D. Jackson. "PACT: Anonymous Credentials for the Web." *Mozilla Hacks*, June 23, 2026. URL: https://hacks.mozilla.org/2026/06/pact-anonymous-credentials-for-the-web/. Accessed September 24, 2026.

**[N2]** S. Schlesinger, D. Jackson, and T. Meunier. "Moderation of unLinkable Endorsements (MoLE) Architecture." *Internet-Draft draft-jms-mole-architecture-00* (individual, Informational; work in progress), IETF, July 6, 2026. URL: https://datatracker.ietf.org/doc/draft-jms-mole-architecture/. Accessed September 24, 2026.

**[N3]** D. Jackson, S. Schlesinger, and E. Trouton. "Private Access Control Tokens" (PACT problem statement). W3C Anti-Fraud Community Group, antifraudcg/proposals GitHub Issue #22, December 2, 2025. URL: https://github.com/antifraudcg/proposals/issues/22. Accessed September 24, 2026.

**[N4]** antifraudcg/pact. "Fragmentation vs. Centralization of Anchors." GitHub Issue #12, June 25, 2026. URL: https://github.com/antifraudcg/pact/issues/12. Accessed September 24, 2026.

**[N5]** antifraudcg/pact. "Malicious Bot use of tokens, browser use." GitHub Issue #11, June 25, 2026. URL: https://github.com/antifraudcg/pact/issues/11. Accessed September 24, 2026.

Existing entries:
- **[39]:** correct the date to "March 30, 2026".
- **[40]:** no longer cited after these replacements, so delete it and renumber.
- **[88]:** keep it. It is still cited in C22 and C23, now with attribution.

## 3. Replacement text (old → new)

Citation numbers are unchanged; N1–N5 are the new sources. Each new sentence is no longer than the old one; §4 lists the character counts.

### §2 (l.84)

- OLD: PACT [11] attests personhood or account standing through *issuer judgment* rather than hardware [39, 40].
- NEW: PACT [11] attests personhood or account standing through *issuer judgment* rather than hardware [39, N1].

### §4.2 (l.242)

- OLD: PACT also treats the browser as a trusted user-agent [39], an assumption that fails when a copied or compromised profile can exercise the same issuance APIs as a legitimate user [39, 88].
- NEW: PACT treats the browser as a trusted user-agent [39], yet its draft threat model lets attackers "control a number of Clients" [N2], e.g. a copied or compromised profile.

### §4.3 (l.264)

- OLD: Bulk registration, credential stuffing, stolen session tokens and cheap subscriptions feed token farming [88].
- NEW: Bulk registration, credential stuffing and cheap subscriptions feed token farming, as designers expect [N5].

- OLD: The cryptographic layer prevents only certain linkability [4], not polluted tokens, so verifier-side redemption rate limiting remains necessary for any anchor [88].
- NEW: The cryptographic layer prevents only certain linkability [4], not polluted tokens, so verifier-side rate limiting remains necessary for any anchor [N3].

### §4.4 (l.280)

- OLD: PACT [11] extends issuance to any party that "knows something about the user" [11, 39].
- NEW: PACT [11] opens issuance: "Any entity or organization may provide credentials" [N3].

- OLD: It worsens reason 2, as no issuer accreditation, revocation or audit regime has been specified (§6.4) [11, 88].
- NEW: It worsens reason 2: each Moderator picks its Anchors, with no accreditation or audit regime (§6.4) [N2, N4].

- OLD: It worsens reason 3, as unbanked, low-income and anonymity-seeking users may lack a usable issuer [40].
- NEW: Reason 3 stays open: its designers ask how "anyone in the world can get a useable anchor" [N4].

### §6 (l.456)

- OLD: Industry deployment over 2024–2026 has advanced along three tracks: DBSC, passkeys, and anonymous attestation (Privacy Pass, Apple PATs, PACT).
- NEW: Industry work over 2024–2026 advanced along three tracks: DBSC, passkeys, and anonymous attestation (Privacy Pass, Apple PATs, proposed PACT).

### §6.4, paragraph 1 (l.485)

- OLD: It is a proposal: there is no deployment timeline, no IETF draft under the PACT name, and no issuance-governance specification.
- NEW: It is a proposal with no deployment timeline; its architecture is an individual, Informational IETF draft (MoLE) [N1, N2].

### §6.4, paragraph 2 (l.487)

- OLD: PACT accepts *software or contextual anchors*: active subscriptions, account standing, first-party relationships, or issuer vouching [39, 40].
- NEW: PACT accepts *software or contextual anchors*: "a subscription, an account in good standing, or a verified phone number" [N1].

- OLD: Bulk registration, credential stuffing, stolen session tokens, and cheap subscriptions are automatable inputs to token farming upstream of the protocol [88].
- NEW: Bulk registration, credential stuffing, stolen session tokens, and cheap subscriptions are automatable inputs to token farming [N2, N5].

- OLD: Blind signatures make a redeemed token unlinkable to its issuance, but the token still reveals which issuer key signed it.
- NEW: Redemption hides which Anchor endorsed the client [N1, N2], so a Moderator cannot tell a strong Anchor from a weak one.

### §6.4, paragraph 3 (l.489)

- OLD: Origins configure up to two aggregating issuers and a credit cost per request [39].
- NEW: Each site nominates one Moderator, which picks the Anchors it trusts [N1, N2].

- OLD: This makes issuer choice a gatekeeping decision and Cloudflare a natural central participant [88].
- NEW: Shared Moderators carry "a centralisation risk" [N1]; [11] pitches "PACT on Cloudflare's network".

- OLD: As adoption spreads, the absence of a token carries information: untokened traffic is challenged more aggressively, and no single actor decides to make tokens mandatory [88].
- NEW: Rudis argues that as adoption spreads, the absence of a token carries information, so tokens become mandatory without anyone deciding it [88].

- OLD: Legitimate traffic with no issuer relationship (measurement systems, security scanners, archival crawlers, RSS readers, Tor users, alternative browsers) becomes systematically suspect [88].
- NEW: Traffic with no issuer relationship (scanners, archival crawlers, RSS readers, Tor users) then becomes suspect [88], though the designers intend a fallback to today's challenges [N1].

- OLD: PACT as announced has no issuer accreditation, public issuer directory, revocation lists, or audit requirements [88].
- NEW: The draft has no Anchor accreditation or audit; Anchor feedback is a "TODO" [N2].

- OLD: Low-quality issuers can then undercut high-quality ones, and a token proves only that *some* issuer signed it, not that a meaningful personhood check occurred.
- NEW: Access starts "at the strength of the weakest" Anchor [N1]; a token proves only that *some* trusted Anchor vouched, not that a real personhood check occurred.

- OLD: Account-standing anchors favor users with persistent platform relationships: bot operators can afford accounts, while low-income or anonymity-seeking users cannot [40].
- NEW: Account-standing anchors favor lasting platform relationships. "A paid subscription costs an attacker the same as a real user" [N1], so the poor pay most.

- OLD: PACT is motivated by agentic AI traffic [11], yet its semantics for human → AI agent → website delegation are unresolved [88].
- NEW: PACT targets agentic traffic [11]; agents may use the user's Credential, and telling them apart is the user agent's job [N2].

- OLD: Until issuer governance is specified, PACT inherits the security posture of whatever issuer an origin configures [88].
- NEW: Until Anchor governance is specified, PACT inherits the posture of the weakest Anchor a Moderator trusts [N2].

### §7.2 (l.505)

- OLD: For PACT, aggregating-issuer and IssuerHide designs [39, 108] would mitigate initial-issuer metadata exposure, but they remain options rather than defaults, and no decentralized issuer network has been specified [11, 88].
- NEW: For PACT, Anchor-hiding, which grew out of aggregating-issuer and IssuerHide designs [39, 108], is now a draft goal [N2], but openness rests on per-Moderator Anchor choice, not distributed issuance.

## 4. Length check

The script output is pasted below. It compares characters, counts citation markers such as "[N1]" as written, and checks that each OLD string occurs verbatim in `paper.md`.

```
OK  old= 105 new= 105  | PACT [11] attests personhood or account standing through *is
OK  old= 187 new= 169  | PACT also treats the browser as a trusted user-agent [39], a
OK  old= 110 new= 108  | Bulk registration, credential stuffing, stolen session token
OK  old= 164 new= 153  | The cryptographic layer prevents only certain linkability [4
OK  old=  87 new=  84  | PACT [11] extends issuance to any party that "knows somethin
OK  old= 111 new= 109  | It worsens reason 2, as no issuer accreditation, revocation 
OK  old= 103 new=  95  | It worsens reason 3, as unbanked, low-income and anonymity-s
OK  old= 143 new= 142  | Industry deployment over 2024–2026 has advanced along three 
OK  old= 127 new= 122  | It is a proposal: there is no deployment timeline, no IETF d
OK  old= 142 new= 126  | PACT accepts *software or contextual anchors*: active subscr
OK  old= 157 new= 136  | Bulk registration, credential stuffing, stolen session token
OK  old= 122 new= 119  | Blind signatures make a redeemed token unlinkable to its iss
OK  old=  83 new=  78  | Origins configure up to two aggregating issuers and a credit
OK  old=  98 new=  98  | This makes issuer choice a gatekeeping decision and Cloudfla
OK  old= 174 new= 142  | As adoption spreads, the absence of a token carries informat
OK  old= 189 new= 183  | Legitimate traffic with no issuer relationship (measurement 
OK  old= 117 new=  81  | PACT as announced has no issuer accreditation, public issuer
OK  old= 159 new= 158  | Low-quality issuers can then undercut high-quality ones, and
OK  old= 168 new= 154  | Account-standing anchors favor users with persistent platfor
OK  old= 126 new= 125  | PACT is motivated by agentic AI traffic [11], yet its semant
OK  old= 118 new= 110  | Until issuer governance is specified, PACT inherits the secu
OK  old= 221 new= 198  | For PACT, aggregating-issuer and IssuerHide designs [39, 108
total old 3011 new 2795
```

All 22 OLD strings appear verbatim in `paper.md`, and no NEW string is longer than its OLD string. The total goes from 3011 to 2795 characters (−216). A second check confirmed that every quoted passage in this file appears in the fetched source text, after normalising curly quotes and markdown.
