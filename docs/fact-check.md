# Fact-check log (Phase 1, item 6)

Accessed 2026-09-23. Tool: local Firecrawl. WebFetch/WebSearch were used where noted.
Verdicts: OK = matches the primary source; FIXED = paper.md was edited; PARTIAL = true with caveats; UNVERIFIED = no primary source could be reached.

| Claim | Location | Source | Verdict |
|---|---|---|---|
| OSWorld is arXiv:2404.07972, Xie et al. | Ref [56], §2.5 | https://arxiv.org/abs/2404.07972 | OK. Title and first author (Tianbao Xie) match. The NeurIPS 2024 D&B venue is not stated on the arXiv page. |
| RFC 9421, Backman, Richer, Sporny, Feb 2024 | Ref [59] | https://datatracker.ietf.org/doc/rfc9421/ | OK |
| Li et al.: honeysites characterise bot fingerprints and behaviour | §2.5, [50] | https://ieeexplore.ieee.org/document/9519384 ; https://www.securitee.org/files/goodbotbadbot_oakland2021.pdf | OK (Aristaeus honeysites, with browser, behaviour and TLS fingerprinting) |
| Azad et al.: anti-bot services block simple bots but miss adaptive ones | §2.5, [51] | Abstract not retrieved (search returned no results) | UNVERIFIED. TODO(author): check against the DIMVA 2020 abstract. |
| Jonker et al.: bot-framework fingerprint surface, detector deployment in the top 1M | §2.5, [52] | https://dl.acm.org/doi/abs/10.1007/978-3-030-29962-0_28 | OK ("12.8% of websites show indications of web bot detection" in the Alexa Top 1M) |
| Vastel et al.: FP crawler blocking evadable by altering a few attributes | §2.5, [53] | https://www.ndss-symposium.org/wp-content/uploads/2020/02/23010.pdf | PARTIAL. The paper was found, but the evasion claim was not re-read in full. |
| Picasso uses canvas rendering to identify device class | §2.5, [3] | DOI 10.1145/2994459.2994467 | OK (title: "Lightweight Device Class Fingerprinting"). The word "attest" is loose. |
| Sivakorn et al. broke image reCAPTCHA and exploited checkbox risk analysis | §2.5, [19] | https://ieeexplore.ieee.org/document/7467367 | PARTIAL. The abstract confirms 70.78% solved, 19 s per challenge. The risk-analysis/cookie part is in the paper body but was not shown in the retrieved snippet. |
| GPT-5 is $1.25 in / $10 out per M tokens, half of GPT-4o's input price | §5 table, §5.1, [94] | https://developers.openai.com/api/docs/models/gpt-5 | OK ($1.25 / $10). GPT-4o input is $2.50, which was not re-fetched this session. Note: the current general page [94] no longer lists base gpt-5. Cite the model page instead. |
| Gemini 2.5 Computer Use is $1.25 in / $10 out | §5 table, [95] | https://ai.google.dev/gemini-api/docs/pricing (gemini-2.5-computer-use-preview-10-2025) | OK for prompts of 200k tokens or less. It is $2.50 / $15 above 200k. |
| Claude Sonnet 4.6 is $3 in / $15 out | §5 table, [96] | https://platform.claude.com/docs/en/about-claude/pricing | OK |
| Bright Data residential "from $5.88/GB" | §5 table, [97] | https://brightdata.com/pricing/proxy-network/residential-proxies | **FIXED → UNVERIFIED**. The page is blocked by the network's DNS filter (NextDNS), and WebFetch failed on TLS. Secondary trackers (e.g. proxyfacts.com/blog/bright-data-pricing) report $8/GB pay-as-you-go (list), with a 50%-off coupon on the page, and $2.50–$3.50/GB on promoted monthly plans, so $5.88 looks stale. The row now reads TODO(author). |
| PAT attester "can perform rate-limiting" | §3.2 (l.176), §4.3 (l.283), §6.3 | WWDC22 10077 transcript, t=383 s: "This attester can also perform rate-limiting" | PARTIAL. Apple publishes no per-device limit values. §6.3 had "Apple applies per-device rate limits"; it is **FIXED** to quote the WWDC wording. §3.2 and §4.3 cite [10] for per-device rate-limiting (Chu et al. analyse rate-limited Privacy Pass in general). Left as is, but the "per-device" wording is an inference. |
| Cloudflare and Fastly are PAT issuers, Apple is the attester | §6.3 | WWDC22 10077 (t=495 s); https://www.fastly.com/documentation/solutions/demos/pat/ | OK |
| Android Keystore keys are bound to the creating app | §4.3 (l.285) | https://source.android.com/docs/security/features/keystore#access-control | OK. The caller UID is part of key identity, "preventing one app from accessing another's keys". Caveat: an app can explicitly *grant* a key to another UID. |
| Private State Tokens are maintained after the Oct 2025 Sandbox retirements | §6.3, [110] | https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies | OK ("We'll also maintain Private State Tokens") |
| DBSC: key in a TPM, non-exportable, short-lived cookies, no attestation server | §3.2, §6.1, [27][28][102] | https://developer.chrome.com/docs/web-platform/device-bound-session-credentials | PARTIAL. The key is stored in a TPM "when available". The Chrome docs caution that malware present *during registration* "may be able to extract the private key". §6.1 says "generated as non-exportable". Registration-time caveat now added to §6.1 (see row below). |
| DBSC spec editors "D. Rubery and K. Monsen" | Ref [27] | https://w3c.github.io/webappsec-dbsc/ | PARTIAL. The ED of 8 Sep 2026 lists Daniel Rubery (Google) plus a second editor shown only as thefrog@chromium.org. "K. Monsen" was not confirmed. |
| DBSC key capture at registration time | §6.1, [102] | developers.chrome.com DBSC page ("If malware is present on the device during session registration, it may be able to extract the private key") | FIXED: caveat added |
| PPI per-install price | §4.3, [74] | Caballero et al. 2011: $7–$180 per 1,000 installs | FIXED: "$0.10–$0.50 per infection" replaced by $0.007–$0.18 |
| VLM step latency 5–15 s | §5.2, Table 5.1, [98] | No public per-step figure; OSWorld-Human (arXiv:2506.16042): tasks take tens of minutes, planning/reflection 75–94% of latency | FIXED: marked assumption consistently, contextual cite |
| Searles et al. 1,400 participants | §2.5, [20] | USENIX Sec '23 abstract: "1,400 participants collectively solved 14,000 CAPTCHAs" | OK |
| Bonneau et al. "25 properties" | §2.5, [61] | Framework names 25 usability/deployability/security *benefits*, 35 schemes | FIXED |
| GPT-5 $1.25/$10 | Table 5.1, [94] | developers.openai.com/api/docs/models/gpt-5 (general pricing page no longer lists base GPT-5) | FIXED: ref points to model page |

## Edits made to paper.md
1. §6.3, Apple PAT bullet: "Apple applies per-device rate limits and decides which devices are attested" was changed to "Apple's attester performs device attestation and 'can also perform rate-limiting' [1], though Apple publishes no per-device limits".
2. §5 parameter table, proxy row: "verified: Bright Data list price from $5.88/GB, volume tiers lower [97]" was replaced with a TODO(author) noting the price was not re-verified.

## Blocked
- brightdata.com is DNS-blocked on this network. Re-check it from another network and archive a copy (e.g. web.archive.org).
- Archive/screenshot URLs for the four price pages were not produced.
