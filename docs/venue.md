# Target venue: IEEE S&P 2027 (SoK)

Sources (accessed 2026-09-23):
- CFP: https://sp2027.ieee-security.org/cfpapers.html
- Call for Artifacts: https://sp2027.ieee-security.org/cfartifacts.html

Event: 48th IEEE S&P, May 17-20, 2027, Montreal, Canada.

## SoK criteria
> "we solicit systematization of knowledge (SoK) papers that evaluate, systematize, and contextualize existing knowledge ... Suitable papers are those that provide an important new viewpoint on an established, major research area, support or challenge long-held beliefs in such an area with compelling evidence, or present a convincing, comprehensive new taxonomy of such an area. Survey papers without such insights are not appropriate and may be rejected without full review."

- Title must start with "SoK:", plus a checkbox on the submission form.
- Reviewed by the full PC, "held to the same standards as traditional research papers", and judged "based on their treatment of existing work and value to the community".

## Page limit and format
> "Submitted papers may include up to 13 pages of text and up to 5 pages for references and appendices, totaling no more than 18 pages. All text and figures past page 13 must be clearly marked as part of the appendix. ... Reviewers are not required to read appendices. For SoK papers, the references do not count towards the number of pages."

- Camera-ready: at most 18 pages (PC chairs may allow more).
- Format: US letter, IEEE compsoc template, `\documentclass[conference,compsoc]{IEEEtran}` (IEEEtran.cls v1.8b). Changing the margins, font or spacing, or scrunching space, can get the paper rejected without review.
- Oversize papers are rejected without review.

## Anonymity
- No author names or affiliations. Cite your own work in the third person. No acknowledgments that identify the authors.
- Artifact repositories must be anonymized too (the CFP suggests GitFront or Anonymous GitHub).
- arXiv preprints and talks are allowed, but authors should not advertise the work widely.
- Papers desk-rejected for anonymity or format can be resubmitted in the next cycle. If a break is found after reviews are done, the paper must wait one year.

## Ethics
> "All papers must complete the 'Ethics Considerations' field when registering a paper on HotCRP ... authors of accepted papers will be asked to add the 'Ethics Considerations' section itself to their manuscript at the camera ready stage, where it will not count toward page limits."

- A Research Ethics Committee (REC) checks papers that reviewers flag, and may recommend rejection. The CFP points to the Menlo Report.
- The CFP has sub-guidance on vulnerability disclosure, human subjects, live systems, and new tools. The live-systems part is relevant to any Botguard or anti-bot probing.

## Generative-AI policy
- The IEEE PSPB policy applies (https://pspb.ieee.org/images/files/PSPB/opsmanual.pdf), plus an S&P-specific policy based on IEEE SaTML 2026.
- Using generative AI is allowed but must be disclosed in the HotCRP field "Generative AI usage considerations".
- Suggested wording for editorial use: "Generative AI was used for editorial purposes in this manuscript, and all outputs were inspected by the authors to ensure accuracy and originality."
- The criteria are Accuracy and Originality (authors are responsible for the literature review), Transparency, and Responsibility.

## Artifacts and open science
> "Papers are strongly encouraged to provide artifact repositories that are anonymized ... Artifact repositories must not be updated after the paper deadline has passed."

- Artifact Evaluation happens after acceptance and is optional ("strongly encouraged"). It covers availability, functionality and reproducibility.
- A mandatory "Open Science" section, as USENIX requires: **not found in the S&P 2027 CFP. Treat as unknown or not required.**

## Deadlines (two cycles)
| | Cycle 1 | Cycle 2 |
|---|---|---|
| Abstract registration | Jun 4, 2026 (passed) | **Nov 10, 2026** |
| Paper submission | Jun 11, 2026 | **Nov 17, 2026** |
| Early reject | Jul 27, 2026 | Jan 18, 2027 |
| Reviews released | Aug 20, 2026 | Feb 11, 2027 |
| Rebuttal due | Aug 27, 2026 | Feb 16, 2027 |
| Interactive rebuttal ends / revised manuscript | Sep 3, 2026 | Feb 26, 2027 |
| Notification | Sep 11, 2026 | Mar 5, 2027 |
| Camera-ready | Oct 16, 2026 | Apr 8, 2027 |

- Each author can submit at most 6 papers per cycle, enforced at abstract registration.
- Artifact dates for Cycle 2: register by Mar 7, 2027 (optional), submit by Mar 12, 2027, decision on Apr 5, 2027.

## Rebuttal
- Papers that reach the second round get one of two rebuttal types. Both are limited to 750 words.
  - Non-interactive: address factual errors and reviewer questions only. No new results.
  - Interactive: the 750-word rebuttal, then a HotCRP comment with any new material the reviewers requested, plus a revised manuscript PDF.
- Breaking the rebuttal rules means immediate rejection. Papers rejected during the rebuttal period must wait one year before resubmitting.
- Every accepted paper gives a short talk (about 5-7 minutes) and a poster.

## Unknown / not found
- Whether a separate SoK-specific page limit exists beyond "references do not count". None found.
- A mandatory Open Science section. None found.
- The Major Revision process: the CFP describes the interactive rebuttal with a revised manuscript. No separate "major revision" track was found.
