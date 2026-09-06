# Plan: T1 (server-side companion §6.5), T-cost, T-xref

**Status:** self-reviewed autonomous pass. This repo's handoff normally stops here for
human review before implementation; running fully autonomously (per task instructions),
this plan was critically self-reviewed against the ground rules below and then
implemented in the same session — noted so a reviewer can tell this wasn't a rubber
stamp. No claim below proceeds without either a real citation or explicit
"analysis"/"author's own instantiation" framing.

## 1. The gap, restated precisely

- §1.2/§3.1 exclude "purely server-side defenses (WAF, TLS fingerprinting...)" from
  scope, on economic-model grounds.
- §4.3 concludes the defender's "only recourse" once client-side attestation is
  cryptographically valid but attacker-controlled (SDK-proxied device, PACT token
  farming) is "network-layer behavioral metadata: ASN reputation scoring,
  IP-to-Account cardinality analysis, velocity... cross-session pattern matching."
- The paper builds the entire case for that recourse and never analyzes it. That's
  the excluded chapter.

## 2. Where it goes

New `### 6.5` subsection, same level as 6.1–6.4, before the `---` separator that
precedes `## 7. Open Problems`. Not a companion manuscript — a subsection, because
(a) it must cite directly into §4.1/§4.3/§5.2/§6.3/§6.4 by section number, which is
cleaner within one document, and (b) README/AGENTS.md describe the manuscript as
"self-contained" (v3.0 changelog literally inlined the bibliography for this reason).

## 3. Section-by-section claims and citations

1. **Boundary honesty.** State this is a deliberate, flagged exception to §1.2's own
   exclusion criterion, extending the SoK past its stated scope specifically because
   §4.3 names the recourse without analyzing it. Framed as analysis, not a new
   systematic review — §3.1 gets one sentence noting a supplementary, non-systematic
   10-reference set outside the original search methodology (full honesty about the
   corpus boundary; see §5 below for the exact count reconciliation).
2. **Passive server-side traffic-artifact continuity, defined.** TLS ClientHello
   ordering (JA3), the JA4+ suite (JA4/JA4H/JA4T covering TLS+HTTP+TCP jointly), H2/H3
   frame and settings-negotiation behavior, and TCP/IP kernel fields (MTU, TTL, initial
   window — the same fields §4.1 already names as containerization leaks). Citations:
   JA3 (Salesforce eng blog 2019), JA4+ and JA4T (FoxIO blog 2023/2024), Husák et al.
   EURASIP 2016 (academic grounding for passive TLS/TCP fingerprinting), p0f v3
   (Zalewski — canonical passive TCP/IP fingerprinting tool), two Akamai blog posts
   (passive fingerprinting across protocol layers; TLS-fingerprint tampering as a
   documented evasion precedent).
3. **Why it's modality-independent.** Ties to §1.3 Axis C: the TLS/TCP handshake is
   negotiated by the OS network stack and TLS library, layers Operator Synthesis does
   not touch — same survival logic as Type IV/V (§4.2) but without a hardware root of
   trust. Connects explicitly to §4.1's containerization-gap artifacts and §5.2's
   macroscopic latency signal as already server-observable.
4. **Honest limits.** (a) Not an authenticator — cite NIST SP 800-63B's
   authenticator/risk-signal boundary to frame this as a continuity/risk score that
   only ever gates step-up, never asserts identity. (b) Evadable — cite Akamai's own
   report of bots spoofing TLS fingerprints as a real, documented precedent (this is
   the honest analogue to "fingerprintproxy-class TLS spoofing" the handoff names;
   fingerprintproxy itself is not cited — it's a sibling repo, not a published,
   independently checkable source, so citing it would violate "never assert what you
   haven't verified" against academic standards). Value is cross-layer coherence +
   calibrated scoring, not any single signal, consistent with the paper's existing
   economics-of-security framing (§2.4).
5. **Cost-to-evade bridge (T-cost).** Reuse §5.1's `C_effective` accounting-identity
   shape with a substitution: cost-to-evade a continuity score as
   `Cost_proxy_tier + Cost_fingerprint_spoof_tooling + Cost_state_orchestration`,
   gated by an unmeasured `P(score drop below threshold | spoofed layer)`. Explicitly
   name that missing probability as the empirical gap (mirrors §7.1's existing
   "empirical gap" framing) — sets up an eval-harness-style experiment without
   claiming its result.
6. **Centralization counterpoint.** A first-party, server-observed score requires no
   OS-vendor coordination and no issuer economy — direct counterpoint to §6.3's
   Apple/Google/Microsoft consolidation and §6.4's PACT issuer-judgment consolidation.
   Also state the honest reverse limitation: no coordination means no
   cross-origin interoperability, the opposite failure mode from PACT.
7. **T-xref.** One sentence citing the author's own published essays (tomabel.ee) —
   "What Client-Side Trust Is Actually Worth" and the Smart-ID/eID "Achilles' Heel"
   signing-relay report — as applied case studies of the same structural claim
   (attestation not bound to context degrades into a signal), explicitly marked as
   self-citations, not additional peer-reviewed sources, and not marketing copy.
8. **Author's-own-system disclosure.** One footnote, generic: "one production
   instantiation of this class of scoring... disclosed here as the author's own
   system rather than as a claim of independent validation... referenced only as an
   existence proof that the architecture is buildable, not as evidence of its
   detection accuracy, which remains unmeasured in any publicly reviewable way." No
   product name in the running text; the footnote is the only place a live system is
   acknowledged, and it explicitly disclaims performance claims.

## 4. Candidate references (verified live via web search before drafting; none invented)

| # | Citation | Verified via |
|---|---|---|
| 86 | J. Althouse, J. Atkinson, J. Atkins, "TLS Fingerprinting with JA3 and JA3S," Salesforce Engineering Blog, Jan 15 2019 | confirmed URL + date |
| 87 | FoxIO, "JA4+ Network Fingerprinting," FoxIO Blog, Sep 26 2023 | confirmed URL + date |
| 88 | FoxIO, "JA4T: TCP Fingerprinting," FoxIO Blog, Apr 23 2024 | confirmed URL + date |
| 89 | M. Husák, M. Čermák, T. Jirsík, P. Čeleda, "HTTPS Traffic Analysis and Client Identification Using Passive SSL/TLS Fingerprinting," EURASIP J. Information Security, 2016, DOI 10.1186/s13635-016-0030-7 | confirmed DOI (also cited in RFC 8446's own references) |
| 90 | M. Zalewski, "p0f v3: Passive Fingerprinter," tool documentation | confirmed URL |
| 91 | Akamai, "Bots Tampering with TLS to Avoid Detection," Akamai Security Blog, May 15 2019 | confirmed URL + date |
| 92 | Akamai, "Evading Link Scanning Security Services with Passive Fingerprinting," Akamai Security Blog, Dec 9 2020 | confirmed URL + date |
| 93 | NIST SP 800-63B, "Digital Identity Guidelines: Authentication and Lifecycle Management" | confirmed on csrc.nist.gov |
| 94 | Author's own essay, "What Client-Side Trust Is Actually Worth," tomabel.ee/disclosures/what-client-side-trust-is-actually-worth | confirmed live route in tomabel.ee repo (`src/App.tsx`) |
| 95 | Author's own report, "The Achilles' Heel of Estonia's e-State — Smart-ID / eID Research," tomabel.ee/disclosures/smart-id-achilles-heel | confirmed live route in tomabel.ee repo (`src/App.tsx`) |

`fingerprintproxy` (sibling repo) is deliberately **not** cited as an academic source —
it's the author's own unpublished tool, not an independently checkable reference.
It is acknowledged only implicitly, generically, as "fingerprintproxy-class TLS
spoofing" per the handoff's own phrasing, without a repo link, to keep this section
academic rather than a product/tooling plug.

## 5. Build-integrity / renumbering approach

- Current bibliography: [1]–[85] (57 academic + 10 standards + 18 grey, per §3.1).
- Append [86]–[95] at the end (10 new: 1 academic [89], 1 standard [93], 8 grey
  [86,87,88,90,91,92,94,95]) — matches the paper's existing thematic-append
  convention (refs are grouped by topic-of-introduction, not citation-order).
- New total: 95 references (58 academic + 11 standards + 26 grey). Update §3.1's
  final sentence to state both the original 85-corpus count and the new 95 total,
  attributing the delta to the flagged non-systematic supplement.
- No existing `[N]` renumbered — appending avoids any renumbering risk entirely.
- README.md's three "85-reference" mentions updated to 95; one changelog entry added.
- `make` rebuild verified after edits (pandoc + lualatex, DejaVu Sans font — do not
  touch the Makefile/font pipeline per AGENTS.md's documented pitfall).
- Footnotes use pandoc's native `[^id]` / `[^id]: text` syntax (unused elsewhere in
  the doc but standard pandoc-markdown, renders as real PDF footnotes under
  lualatex) — verified in the actual build, not assumed.

## 6. Touch list

- `paper.md`: §1.2 scope paragraph (+1 sentence), §3.1 (+1 sentence, count
  reconciliation), new `### 6.5` subsection (~700 words) with 2 footnotes, References
  list (+10 entries).
- `README.md`: reference-count mentions (85 → 95), one changelog entry.
- `notes/companion-plan.md`: this file.
- Nothing else. No Makefile/AGENTS.md changes — the font/build pitfall is unrelated
  to this content change and must not be touched.

## 7. Explicitly rejected/out of scope

- No companion manuscript file — a subsection is the lazier, more consistent choice
  and the handoff explicitly allows it ("or a companion manuscript").
- No PSD2/RTS regulatory mapping — that's Task 13 in the master plan, scoped to the
  `proksimity` repo, not this SoK.
- No feature-count/product-metric claims of any kind (accuracy, precision, ECE) —
  those are Proksimity's own unresolved honesty gaps (master plan §3.2 G3) and citing
  them here would import an unverified empirical claim into an academic manuscript.
  The footnote explicitly disclaims this.
- No renumbering of existing [1]–[85] — append-only.
