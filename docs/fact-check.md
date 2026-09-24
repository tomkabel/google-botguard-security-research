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

## Phase 8 research (2026-09-24)

Accessed 2026-09-24 (UTC). Tool: local Firecrawl (live pages, Wayback CDX API and snapshots, the Crossref, Europe PMC and Hugging Face APIs). brightdata.com, swappa.com and backmarket.com cannot be reached from this network (NextDNS block or scraper refusal). Their figures come from Wayback snapshots, which are listed below. paper.md was not edited.

### 1. Bright Data residential proxy price [95]
- Live page: DNS-blocked ("brightdata.com is blocked"), the same as on 2026-09-23.
- Wayback snapshots (both return 200 and show the same prices):
  - https://web.archive.org/web/20260907204324/https://brightdata.com/pricing/proxy-network/residential-proxies (7 Sep 2026)
  - https://web.archive.org/web/20260924054801/https://brightdata.com/pricing/proxy-network/residential-proxies (24 Sep 2026, requested by us through /save)
- Prices on the page. List prices are struck through; the prices after them apply with coupon RESIGB50 ("50% OFF Residential Proxies for 3 months"):

  | Plan | List $/GB | With coupon $/GB | Commitment |
  |---|---|---|---|
  | Pay as you go | $8 | $4 | none |
  | 141 GB included | $7 | $4 (implied $3.54) | $499/mo |
  | 332 GB included | $6 | $3 (implied $3.01) | $999/mo |
  | 798 GB included | $5 | $3 (implied $2.50) | $1,999/mo |
  | >1 TB | "Custom price per GB" | | contact sales |

  The site menu reads "Starts from ~~$5~~ $2.5/GB". The monthly fees are the discounted ones (798 GB × $2.50 ≈ $1,999). "From $5.88/GB" no longer appears anywhere.
- Verdict on "∼$2.50–$6/GB": **PARTIAL**. The $2.50 floor is real but promotional: it needs the largest self-serve plan plus a 3-month coupon. The upper bound of $6 is not the list maximum. List prices run from $5/GB (plan) to $8/GB (pay as you go). Proposed wording: "∼$2.50–$8/GB (list $5–$8/GB; $2.50–$4/GB under a launch promotion) [95]". Or cite list prices only, "$5–$8/GB". Change the access date of [95] to the snapshot date and give the snapshot URL.

### 2. Used PAT-capable iPhone price (D in §5.x)
- Capable devices: Apple's iOS 16 user guide lists iPhone 8/8 Plus, X, XR, XS/XS Max, 11 series, SE (2nd and 3rd gen) and later (https://support.apple.com/en-us/guide/iphone/iphe3fa5df43/16.0/ios/16.0). So "iPhone 8 or newer" is correct.
- Swappa (used marketplace; averages come from its listings). Live swappa.com refuses the scraper, so these come from Wayback snapshots:
  - iPhone XR, "Updated July 08, 2026": starting price $103, average $136. Unlocked 64 GB averages $136 (39 listings) and 128 GB $150. Carrier-locked 64 GB units run $114–$125. https://web.archive.org/web/20260708190037/https://swappa.com/prices/apple-iphone-xr
  - Swappa price index, "Prices Updated August 12, 2026" (averages): iPhone SE 2nd Gen $105 (215 listings), SE 3rd Gen $141, iPhone 11 $188 (307 listings), iPhone 12 $216, iPhone 13 $286. https://web.archive.org/web/20260812144427/https://swappa.com/prices (a request for the 20260913174608 timestamp redirects to this capture).
  - iPhone 8: no 2026 Swappa capture exists. UNVERIFIED.
- Back Market: live page and Wayback captures (20260919041745, 20260919041909) returned empty or error pages. UNVERIFIED.
- Our requests to /save the Swappa iPhone 11 and SE 2 pages returned an error page; we did not confirm whether a capture exists.
- Verdict on "$100–$300": **OK**. The cheapest PAT-capable models average $105–$188 on Swappa (Jul–Aug 2026), and the iPhone XR starts at $103. $300 covers an iPhone 13. Proposed citation: "Swappa used-price data, iPhone XR/SE 2/11, July–August 2026 (Wayback snapshots)". Caveat: Swappa averages are asking prices of active listings, not completed sales.

### 3. Azad et al. [48], "Web Runner 2049" (DIMVA 2020)
- Abstract (Springer, open access: https://link.springer.com/chapter/10.1007/978-3-030-52683-2_7), key sentences:
  > "On the positive side, our results show that by relying on browser fingerprinting, more than 75% of protected websites in our dataset, successfully defend against attacks by basic bots built with Python scripts or PhantomJS. At the same time, by using less popular browsers in terms of automation (e.g., Safari on Mac and Chrome on Android) attackers can successfully bypass the protection of up to 82% of protected websites."
  > "Our findings show that the majority of protected websites are prone to bot attacks and the existing anti-bot solutions cannot substantially limit the ability of determined attackers."
- paper.md l.92: "Commercial anti-bot services [48] and fingerprint-based crawler blocking [49] miss bots that alter their fingerprints."
- Verdict: **PARTIAL / imprecise**. Azad et al. did not alter fingerprints. They drove real, less-automated browsers (Safari on Mac, Chrome on Android), so their bots presented genuine but unexpected environments. The "alter their fingerprints" part fits [49] (Vastel et al.), not [48]. The sentence also leaves out the positive finding (basic bots are blocked on >75% of sites). Proposed wording: "Commercial anti-bot services stop basic scripted bots on most sites but are bypassed on up to 82% of protected sites by automating less common real browsers [48]; fingerprint-based crawler blocking misses bots that alter a few fingerprint attributes [49]."
- Side note: the earlier Phase 1 row "Azad et al.: … [51]" (UNVERIFIED) is resolved by this entry. The reference number is now [48].

### 4. Archived copies of the price pages [92]–[95]
| Ref | Snapshot | Price the paper cites | Snapshot shows |
|---|---|---|---|
| [92] GPT-5 | https://web.archive.org/web/20260921120808/https://developers.openai.com/api/docs/models/gpt-5 | $1.25 / $10 | OK: "Input $1.25, Cached input $0.125, Output $10.00" |
| [93] Gemini 2.5 CU | https://web.archive.org/web/20260924054733/https://ai.google.dev/gemini-api/docs/pricing (requested by us via /save) | $1.25 / $10 | OK: `gemini-2.5-computer-use-preview-10-2025` paid tier "$1.25, prompts <= 200k tokens / $2.50 > 200k"; output "$10.00 <= 200k / $15.00 > 200k". The live page on 2026-09-24 shows the same. |
| [93] (older) | https://web.archive.org/web/20260922123229/https://ai.google.dev/gemini-api/docs/pricing | | **Do not cite.** In this capture a second table sits under the CU heading ($1.00/$5.00 "through December 31, 2026", Gemini 3.x grounding). It looks like a rendering artefact from a neighbouring model; neither the live page nor the 24 Sep capture has it. |
| [94] Claude Sonnet 4.6 | https://web.archive.org/web/20260923181040/https://platform.claude.com/docs/en/about-claude/pricing | $3 / $15 | OK: "Claude Sonnet 4.6 · $3 / MTok · $15 / MTok" (batch $1.50/$7.50) |
| [95] Bright Data | https://web.archive.org/web/20260924054801/https://brightdata.com/pricing/proxy-network/residential-proxies (also 20260907204324) | ∼$2.50–$6/GB | See task 1 |

Another note on [93]: the tools table now says Computer use is "Charged as regular tokens per model pricing (e.g., standard Gemini 3.5 Flash pricing). See the Gemini 2.5 Computer Use Preview pricing table for legacy model rates." Google now calls the 2.5 CU model "legacy". The price is still correct.

### 5. IEEE S&P 2027 CFP re-check (https://sp2027.ieee-security.org/cfpapers.html)
- Page limit and appendices: "Submitted papers may include up to 13 pages of text and up to 5 pages for references and appendices, totaling no more than 18 pages. All text and figures past page 13 must be clearly marked as part of the appendix. The final camera-ready paper must be no more than 18 pages, although, at the PC chairs' discretion, additional pages may be allowed. Reviewers are not required to read appendices." So appendices are allowed after the references and count toward the 5-page / 18-page budget.
- SoK references: "For SoK papers, the references do not count towards the number of pages." The CFP does not say whether references are excluded from the 18-page total or only from the 13-page body. Read literally, a SoK gets 13 pages of body plus up to 5 pages of appendices, with references free. Ask the PC chairs if the bibliography is long.
- Ethics: "All papers must complete the "Ethics Considerations" field when registering a paper on HotCRP to make the relevant disclosures. Authors are also welcome to add relevant details to their submitted PDF (in the body or appendix of the paper), but regardless, authors of accepted papers will be asked to add the "Ethics Considerations" section itself to their manuscript at the camera ready stage, where it will not count toward page limits." If none apply, the field must say "None", with a short justification encouraged.
- Generative AI: the HotCRP field is mandatory for any use. The CFP says authors "are required to disclose and motivate the use of generative AI in their submission. If the authors choose to use or study generative AI in their work–whether as part of their research methodology and/or in the process of preparing the manuscript–they must complete the "Generative AI usage considerations" field on HotCRP when registering their paper to make the relevant disclosures." Suggested wording: "If the authors have used generative AI to improve their writing, they should state: 'Generative AI was used for editorial purposes in this manuscript, and all outputs were inspected by the authors to ensure accuracy and originality.'" The CFP does not require a separate section in the PDF. However, the Transparency criterion says: "If generative AI was integral to the paper's methodology (including as an object of study), its use should be explicitly detailed", and authors "must elaborate on how they handled limitations". The Responsibility criterion asks authors to justify the experiments' environmental footprint: "why was generative AI necessary, why was a particular model size selected, how the authors minimized the volume of queries made, which hardware was used". Our §5.7 uses VLMs as an object of study, so the paper itself should describe model choice, query volume and reproducibility limits. Non-compliance is "grounds for desk rejection".
- Differences from docs/venue.md:
  1. venue.md summarises the GenAI policy as the HotCRP field plus editorial wording. It leaves out the Transparency and Responsibility duties above: detail methodological use in the paper, handle limitations, and justify the footprint (model size, query volume, hardware). These apply to §5.7 and should be added.
  2. venue.md quotes the page-limit text correctly. It does not note the open question of whether SoK references also fall outside the 18-page total.
  3. venue.md's Ethics section matches the CFP, including the "None" option.

### 6. Melious models: open weights, license, image input, EUR price
Source: https://melious.ai/hub/models/<id>, "Input modalities" (icon labels in the HTML), "Pricing" and "Resources" blocks. Licenses were cross-checked against the Hugging Face API (`license:` tag, safetensors count) and the LICENSE files.

| Melious id | Open weights (HF repo, created) | License | Image input | EUR in / out per 1M tok (cache hit) |
|---|---|---|---|---|
| glm-5.3-flash | Yes, zai-org/GLM-5.3-Flash (2026-08-25, 62 safetensors shards) | MIT | Yes ("Text supported, Image supported"; HF pipeline image-text-to-text) | €0.10 / €0.40 (€0.02) |
| qwen3.8-27b | Yes, Qwen/Qwen3.8-27B (2026-08-05, 18 shards) | Apache-2.0 | Yes | €0.40 / €2.40 (€0.10) |
| kimi-k2.7-code | Yes, moonshotai/Kimi-K2.7-Code (2026-06-11, 64 shards) | "Other" = Modified MIT (MIT plus a clause: display "Kimi K2.7 Code" in the UI of commercial products with >100M MAU or >$20M monthly revenue) | Yes (text, image, video) | €0.70 / €3.50 (€0.20) |
| kimi-k3 | Yes, moonshotai/Kimi-K3 (2026-06-13, 96 shards) | "Other" = custom "Kimi K3 License" (MIT-like, with added conditions for Model-as-a-Service operators whose revenue exceeds $20M over 12 months) | Yes | €2.80 / €14.00 (€0.70) |
| mistral-small-4-119b-instruct | Yes, mistralai/Mistral-Small-4-119B-2603 (10 shards) | Apache-2.0 | Yes (text and image) | €0.15 / €0.60 (no cache price listed) |

Consistency check: measurement/results/summary.json gives glm-5.3-flash a spend of €0.0190 for 113 calls × 1,586 in / 23.8 out tokens. At €0.10/€0.40 that is €0.0179 + €0.0011 = €0.0190, so the hub price matches the measured cost.

### 7. Mouse-dynamics datasets
- **Balabit Mouse Dynamics Challenge** (https://github.com/balabit/Mouse-Dynamics-Challenge). The repo has **no license file**: the GitHub API returns `"license": null` (created 2016-08-01, last push 2018-09-21). The README states the intent: "We make the data set accessible to researchers and experts in the fields of IT security and data science with the hope of contributing to research and providing a benchmark data set." It also asks: "If you are using the data in your publication, please cite it as follows". Academic use and citation are clearly invited. Redistributing the data is not formally licensed, so link to the repo and do not re-host the files in our artifact. Citation (verbatim from the README): Fülöp, Á., Kovács, L., Kurics, T., Windhager-Pokol, E. (2016). *Balabit Mouse Dynamics Challenge data set*. Available at: https://github.com/balabit/Mouse-Dynamics-Challenge
- **SapiMouse** (Antal et al.). The code repo https://github.com/margitantal68/sapimouse is **Apache-2.0**. The raw data is not in the repo; it is a zip on the university page https://www.ms.sapientia.ro/~manyi/sapimouse/sapimouse.html. That page gives **no license or terms of use** and lists the papers to cite. The data were collected from 120 volunteer subjects at Sapientia University. The public download plus the authors' request to cite the listed papers supports academic use. Apache-2.0 formally covers the code only; treat the data license as unspecified and do not re-host. Citation (Crossref): M. Antal, N. Fejer, K. Buza, "SapiMouse: Mouse Dynamics-based User Authentication Using Deep Feature Learning," in *Proc. IEEE 15th Int. Symp. on Applied Computational Intelligence and Informatics (SACI)*, Timisoara, Romania, May 2021, pp. 61–66. DOI: 10.1109/SACI51354.2021.9465583. Related bot paper: M. Antal, K. Buza, N. Fejer, "SapiAgent: A Bot Based on Deep Learning to Generate Human-Like Mouse Trajectories," *IEEE Access* 9:124396–124408, 2021. DOI: 10.1109/ACCESS.2021.3111098.

### Still UNVERIFIED after Phase 8
- Bright Data live page (DNS block); only Wayback captures were read.
- iPhone 8 used price (no 2026 capture) and Back Market prices (captures unreadable).
- Whether SoK references are excluded from the 18-page total as well as from the 13-page body (the CFP is ambiguous).
