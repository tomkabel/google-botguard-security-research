# Bibliography — SoK: Architectural and Economic Ceilings of Client-Side Anti-Automation

**Target: 50+ references, ≥15 from 2021–2025** | **Format: ACM/IEEE style**

---

## 1. SoK Precedent & Structural References

**[1]** J. Bonneau, A. Miller, J. Clark, A. Narayanan, J. A. Kroll, and E. W. Felten. "SoK: Research Perspectives and Challenges for Bitcoin and Cryptocurrencies." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2015. DOI: 10.1109/SP.2015.14.
- **Use:** Canonical SoK structure template. Taxonimizes design space → surveys per component → identifies open challenges.

**[2]** K. Thomas et al. "SoK: Hate, Harassment, and the Changing Landscape of Online Abuse." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00028.
- **Use:** Exemplifies unifying fragmented measurement studies with a common threat model and taxonomy.

**[3]** Y. Wu, W. K. Edwards, and S. Das. "SoK: Social Cybersecurity." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2022. DOI: 10.1109/SP46214.2022.9833757.
- **Use:** Demonstrates dual-axis analytical frameworks for broad interdisciplinary domains.

**[4]** N. Mathews, J. K. Holland, S. E. Oh, M. S. Rahman, N. Hopper, and M. Wright. "SoK: A Critical Evaluation of Efficient Website Fingerprinting Defenses." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2023. DOI: 10.1109/SP46215.2023.10179289.
- **Use:** Web-tracking defense systematization using cost/utility evaluation metrics.

**[5]** T. Rokicki, C. Maurice, and P. Laperdrix. "SoK: In Search of Lost Time: A Review of JavaScript Timers in Browsers." In *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, 2021. DOI: 10.1109/EuroSP51992.2021.00039.
- **Use:** Browser timing side channels; relevant to L4 chronometric analysis.

---

## 2. Browser Fingerprinting & Telemetry

**[6]** P. Laperdrix, N. Bielova, B. Baudry, and G. Avoine. "Browser Fingerprinting: A Survey." *ACM Trans. Web*, Vol. 14, No. 2, Article 8, pp. 1–33, 2020. DOI: 10.1145/3386040.
- **Use:** Canonical survey; baseline for environmental introspection (L1).

**[7]** U. Iqbal, S. Englehardt, and Z. Shafiq. "Fingerprinting the Fingerprinters: Learning to Detect Browser Fingerprinting Behaviors." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2021. DOI: 10.1109/SP40001.2021.00019.
- **Use:** ML detection of fingerprinting scripts; supports analysis of defender detection capabilities.

**[8]** A. Gómez-Boix, P. Laperdrix, and B. Baudry. "Hiding in the Crowd: An Analysis of the Effectiveness of Browser Fingerprinting at Large Scale." In *Proc. The Web Conference (WWW)*, pp. 309–318, 2018. DOI: 10.1145/3178876.3186097.
- **Use:** Large-scale fingerprinting uniqueness analysis; empirical baseline for anti-detect profile requirements.

**[9]** T. Laor et al. "DRAWNAPART: A Device Identification Technique based on Remote GPU Fingerprinting." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2022. DOI: 10.14722/ndss.2022.24093.
- **Use:** GPU-based hardware fingerprinting; demonstrates continuously evolving sensor telemetry surface.

**[10]** S. Wu, P. Sun, Y. Zhao, and Y. Cao. "Him of Many Faces: Characterizing Billion-scale Adversarial and Benign Browser Fingerprints on Commercial Websites." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.24049.
- **Use:** Largest-scale browser fingerprint characterization; empirical evidence for profile commoditization.

**[11]** X. Lin, P. Ilia, S. Solanki, and J. Polakis. "Phish in Sheep's Clothing: Exploring the Authentication Pitfalls of Browser Fingerprinting." In *Proc. USENIX Security Symposium*, 2022.
- **Use:** Security analysis of fingerprinting-based authentication; demonstrates that fingerprinting is probabilistic, not deterministic.

**[12]** Z. Liu, P. Shrestha, and N. Saxena. "Gummy Browsers: Targeted Browser Spoofing against State-of-the-Art Fingerprinting Techniques." In *Proc. International Conference on Applied Cryptography and Network Security (ACNS)*, June 2022. arXiv: 2110.10129.
- **Use:** Advanced fingerprinting evasion using ML-assisted browser profile synthesis.

**[13]** B. A. Azad, O. Starov, P. Laperdrix, and N. Nikiforakis. "Taming the Shape Shifter: Detecting Anti-fingerprinting Browsers." In *Proc. DIMVA*, 2020.
- **Use:** Detection of anti-detect browsers; supports conjunctive cost model for profile virtualization.

**[14]** N. Andriamilanto, T. Allard, G. Le Guelvouit, and A. Garel. "A Large-scale Empirical Analysis of Browser Fingerprints Properties for Web Authentication." *ACM Trans. Web*, Vol. 16, No. 1, Article 1, pp. 1–62, 2022. DOI: 10.1145/3478026.
- **Use:** Empirical analysis of fingerprint stability for authentication; supports stateful telemetry profile longevity analysis.

---

## 3. Behavioral Biometrics & Sensor Telemetry

**[15]** A. Acien, A. Morales, J. Fierrez, R. Vera-Rodriguez, and O. Delgado-Mohatar. "BeCAPTCHA: Behavioral Bot Detection using Touchscreen and Mobile Sensors benchmarked on HuMIdb." *Engineering Applications of Artificial Intelligence*, Vol. 98, 104058, 2021. DOI: 10.1016/j.engappai.2020.104058.
- **Use:** Touchscreen + accelerometer behavioral bot detection; primary citation for sensor telemetry pillar.

**[16]** A. Acien, A. Morales, J. Fierrez, and R. Vera-Rodriguez. "BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection." *Pattern Recognition*, Vol. 127, 108643, 2022. DOI: 10.1016/j.patcog.2022.108643.
- **Use:** GAN-based mouse trajectory synthesis; evidence for ML synthesis cost of behavioral biometrics bypass.

**[17]** H. Niu, J. Chen, Z. Zhang, and Z. Cai. "Mouse Dynamics Based Bot Detection Using Sequence Learning." In *Biometric Recognition (CCBR)*, LNCS Vol. 12878, pp. 49–56. Springer, 2021. DOI: 10.1007/978-3-030-86608-2_6.
- **Use:** Sequence-learning approach to mouse dynamics; supports L1 behavioral telemetry analysis.

**[18]** H. Niu, C. Cheng, and Z. Cai. "Learning Human Behavior for Bot Detection: A Perspective on Mouse Movement (MouseAgent)." In *Proc. China Automation Congress (CAC)*, pp. 6575–6580. IEEE, 2023. DOI: 10.1109/CAC59555.2023.10451138.
- **Use:** Adversarial GAN-based mouse movement synthesis explicitly designed to evade bot detectors.

**[19]** C. Iliou, T. Kostoulas, T. Tsikrika, V. Katos, S. Vrochidis, and I. Kompatsiaris. "Detection of Advanced Web Bots by Combining Web Logs with Mouse Behavioural Biometrics." *Digital Threats: Research and Practice*, Vol. 2, No. 3, Article 24, pp. 1–26. ACM, 2021. DOI: 10.1145/3447815.
- **Use:** Fused web logs + mouse biometrics detection; demonstrates behavioral telemetry effectiveness.

**[20]** H. Fereidooni et al. "AuthentiSense: A Scalable Behavioral Biometrics Authentication Scheme using Few-Shot Learning for Mobile Platforms." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2023. DOI: 10.14722/ndss.2023.24044.
- **Use:** Accelerometer/gyroscope/magnetometer behavioral authentication; sensor telemetry for continuous authentication.

**[21]** S. Sadeghpour and N. Vlajic. "ReMouse Dataset: On the Efficacy of Measuring the Similarity of Human-Generated Trajectories for the Detection of Session-Replay Bots." *Journal of Cybersecurity and Privacy*, Vol. 3, No. 1, pp. 95–117. MDPI, 2023. DOI: 10.3390/jcp3010007.
- **Use:** Session-replay bot detection via trajectory similarity; supports temporal consistency analysis.

**[22]** D. DeAlcala et al. "BeCAPTCHA-Type: Biometric Keystroke Data Generation for Improved Bot Detection." In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, pp. 1051–1060. IEEE, 2023. DOI: 10.1109/CVPRW59228.2023.00112.
- **Use:** Keystroke dynamics synthesis; demonstrates ML-generated behavioral biometric feasible.

**[23]** G. Stragapede, R. Vera-Rodriguez, R. Tolosana, and A. Morales. "BehavePassDB: Public Database for Mobile Behavioral Biometrics and Benchmark Evaluation." *Pattern Recognition*, 2022. DOI: 10.1016/j.patcog.2022.109010.
- **Use:** Public behavioral biometrics benchmark; supports standardization gap analysis in Section 8.

---

## 4. JavaScript Obfuscation & VM Deobfuscation

**[24]** S. Schrittwieser, S. Katzenbeisser, J. Kinder, G. Merzdovnik, and E. Weippl. "Protecting Software through Obfuscation: Can It Keep Pace with Progress in Code Analysis?" *ACM Comput. Surv.*, Vol. 49, No. 1, Article 4, pp. 1–37, 2016. DOI: 10.1145/2886012.
- **Use:** Foundational survey of obfuscation techniques; L2 baseline.

**[25]** P. Saxena, D. Akhawe, S. Hanna, F. Mao, S. McCamant, and D. Song. "A Symbolic Execution Framework for JavaScript." In *Proc. IEEE Symposium on Security and Privacy (S&P)*, pp. 513–528, 2010.
- **Use:** First symbolic execution engine for JavaScript (Kudzu); supports temporal constraint analysis in Section 5.7.

**[26]** T. Blazytko, M. Contag, C. Aschermann, and T. Holz. "Syntia: Synthesizing the Semantics of Obfuscated Code." In *Proc. USENIX Security Symposium*, pp. 643–659, 2017.
- **Use:** Monte Carlo Tree Search-driven program synthesis recovers VM instruction semantics; evidence for automated RE against VM defenses.

**[27]** M. Schloegel et al. "Loki: Hardening Code Obfuscation Against Automated Attacks." In *Proc. USENIX Security Symposium*, pp. 3055–3073, 2022.
- **Use:** Defense-side paper on formal verification of obfuscation resilience; provides metrics for defender perspective.

**[28]** B. Rozière, M. Lachaux, L. Chanussot, and G. Lample. "DOBF: A Deobfuscation Pre-Training Objective for Programming Languages." In *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. 34, 2021. arXiv: 2102.07492.
- **Use:** BERT-style pre-training for deobfuscation; AST-level ML for code recovery.

**[29]** V. Raychev, M. Vechev, and A. Krause. "Predicting Program Properties from 'Big Code'." In *Proc. ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL)*, pp. 111–124, 2015. DOI: 10.1145/2676726.2677009.
- **Use:** CRF-based structured prediction for identifier recovery from obfuscated JavaScript; 63% name recovery.

**[30]** K. Coogan, G. Lu, and S. Debray. "Deobfuscation of Virtualization-Obfuscated Software: A Semantics-Based Approach." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 275–284, 2011. DOI: 10.1145/2046707.2046739.
- **Use:** Inside-out approach to VM bytecode reverse engineering via system-call value flows.

---

## 5. Hardware-Anchored Authentication (FIDO2/WebAuthn/Passkeys)

**[31]** J. Hodges, J.C. Jones, M.B. Jones, A. Kumar, and E. Lundberg, Eds. "Web Authentication: An API for Accessing Public Key Credentials, Level 2." *W3C Recommendation*, 8 April 2021. URL: https://www.w3.org/TR/2021/REC-webauthn-2-20210408/.
- **Use:** Formal specification for hardware-anchored authentication; Section 4.5 and 7.2.

**[32]** D. Kuchhal, M. Saad, A. Oest, and F. Li. "Evaluating the Security Posture of Real-World FIDO2 Deployments." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 2381–2395, 2023. DOI: 10.1145/3576915.3623063.
- **Use:** Systematizes FIDO2 threat model; finds weak real-world configurations; malware resistance analysis.

**[33]** T. Tarrach et al. "A Security and Usability Analysis of Local Attacks Against FIDO2." In *Proc. Network and Distributed System Security Symposium (NDSS)*, 2024.
- **Use:** Identifies flaws including message integrity gaps accessible to browser extensions; broken clone detection.

**[34]** M. Kepkowski, L. Hanzlik, I. D. Wood, and M. A. Kaafar. "How Not to Handle Keys: Timing Attacks on FIDO Authenticator Privacy." In *Proc. Privacy Enhancing Technologies Symposium (PETS)*, Vol. 2022, No. 4, pp. 705–726, 2022. DOI: 10.56553/popets-2022-0129.
- **Use:** Remote timing side-channel on FIDO2 authenticators; demonstrates cross-service linkability.

**[35]** M. Islam, S. S. Arora, R. Chatterjee, and K. C. Wang. "Detecting Compromise of Passkey Storage on the Cloud." In *Proc. USENIX Security Symposium*, pp. 7743–7762, 2025.
- **Use:** First framework to detect leaked synced passkeys; Passkeys security analysis.

---

## 6. Device Bound Session Credentials (DBSC)

**[36]** D. Rubery and K. Monsen, Eds. "Device Bound Session Credentials (DBSC)." *W3C Web Application Security Working Group / WICG*, 2024. URL: https://w3c.github.io/webappsec-dbsc/.
- **Use:** Primary specification; Section 4.5 and 7.1.

**[37]** Google Chrome Security Team. "Fighting Cookie Theft Using Device Bound Sessions." *Chromium Blog*, 2 April 2024. URL: https://blog.google/chromium/fighting-cookie-theft-using-device/.
- **Use:** Official DBSC announcement; TPM-backed key storage, periodic proof-of-possession.

---

## 7. Privacy Pass / Private Access Tokens (PATs)

**[38]** A. Davidson, J. Iyengar, and C. A. Wood. "The Privacy Pass Architecture." *RFC 9576*, IETF, June 2024. DOI: 10.17487/RFC9576.
- **Use:** Privacy Pass architectural framework; Section 4.4 and 7.3.

**[39]** T. Pauly, S. Valdez, and C. A. Wood. "The Privacy Pass HTTP Authentication Scheme." *RFC 9577*, IETF, June 2024. DOI: 10.17487/RFC9577.
- **Use:** HTTP PrivateToken scheme; wire-level deployment model.

**[40]** S. Celi, A. Davidson, S. Valdez, and C. A. Wood. "Privacy Pass Issuance Protocols." *RFC 9578*, IETF, June 2024. DOI: 10.17487/RFC9578.
- **Use:** VOPRF and RSA blind signature issuance protocols.

**[41]** A. Davidson, I. Goldberg, N. Sullivan, G. Tankersley, and F. Valsorda. "Privacy Pass: Bypassing Internet Challenges Anonymously." *Proc. on Privacy Enhancing Technologies (PoPETs)*, Vol. 2018, No. 3, pp. 164–180, 2018. DOI: 10.1515/popets-2018-0026.
- **Use:** Original Privacy Pass protocol; foundational work on anonymous attestation.

**[42]** B. Kreuter, T. Lepoint, M. Orrù, and M. Raykova. "Anonymous Tokens with Private Metadata Bit." In *Advances in Cryptology — CRYPTO 2020*, pp. 308–336. Springer, 2020. DOI: 10.1007/978-3-030-56784-2_11.
- **Use:** PMBTokens; core cryptographic influence on Google's Private State Token design.

**[43]** H. Chu, K. Do, S. Faller, and L. Hanzlik. "On the Security of Rate-limited Privacy Pass." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2023. ePrint: 2023/1805.
- **Use:** First formal security model for rate-limited Privacy Pass.

**[44]** Apple Inc. "Replace CAPTCHAs with Private Access Tokens." *WWDC22 Session*, June 8, 2022. URL: https://developer.apple.com/videos/play/wwdc2022/10077/.
- **Use:** Apple PAT deployment; iOS 16+ hardware attestation via Secure Enclave.

**[45]** WICG. "Private State Token API." *WICG Community Group Draft*. URL: https://wicg.github.io/trust-token-api/.
- **Use:** Browser-level anonymous attestation specification.

---

## 8. Economics of Security

**[46]** R. Anderson and T. Moore. "The Economics of Information Security." *Science*, Vol. 314, No. 5799, pp. 610–613, 2006. DOI: 10.1126/science.1130992.
- **Use:** Foundational economics-of-security framing; motivates economic analysis in Section 2.5 and 6.

**[47]** C. Herley and D. Florêncio. "Nobody Sells Gold for the Price of Silver: Dishonesty, Uncertainty and the Underground Economy." In *Proc. Workshop on the Economics of Information Security (WEIS)*, June 2009. Published in T. Moore, D. Pym, and C. Ioannidis (Eds.), *Economics of Information Security and Privacy*, pp. 33–53. Springer, 2010. DOI: 10.1007/978-1-4419-6967-5_3.
- **Use:** Underground economy pricing theory; economic ceilings framework.

**[48]** T. Moore. "The Economics of Cybersecurity: Principles and Policy Options." *Int. J. Crit. Infrastruct. Prot.*, Vol. 3, No. 3, pp. 103–117, 2010. DOI: 10.1016/j.ijcip.2010.10.002.
- **Use:** Cybersecurity economic principles; cost-benefit analysis framework.

**[49]** H. R. Varian. *Intermediate Microeconomics: A Modern Approach*, 9th ed. W. W. Norton & Company, 2014.
- **Use:** Microeconomic terminology (marginal cost, convexity, supply constraints); used conceptually, not mathematically.

**[50]** R. Anderson et al. "Measuring the Cost of Cybercrime." In R. Böhme (Ed.), *The Economics of Information Security and Privacy*, pp. 265–300. Springer, 2013. DOI: 10.1007/978-3-642-39498-0_12.
- **Use:** Landmark cost-of-cybercrime measurement; supports economic ceiling analysis in Section 6.

**[51]** M. Motoyama, K. Levchenko, C. Kanich, D. McCoy, G. M. Voelker, and S. Savage. "Re: CAPTCHAs—Understanding CAPTCHA-Solving Services in an Economic Context." In *Proc. USENIX Security Symposium*, 2010.
- **Use:** CAPTCHA-solving farm economics; human labor cost floor for behavioral biometrics.

**[52]** M. Motoyama, D. McCoy, K. Levchenko, S. Savage, and G. M. Voelker. "Dirty Jobs: The Role of Freelance Labor in Web Service Abuse." In *Proc. USENIX Security Symposium*, 2011.
- **Use:** Freelance human labor in web abuse; supports human labor cost floor analysis.

---

## 9. Infostealer / PPI Malware Economy

**[53]** J. Caballero, C. Grier, C. Kreibich, and V. Paxson. "Measuring Pay-per-Install: The Commoditization of Malware Distribution." In *Proc. USENIX Security Symposium*, 2011.
- **Use:** Seminal PPI measurement study; foundational reference for Section 4.5 and 7.1 bypass cost model.

**[54]** A. Côté Cyr. "Life on a Crooked RedLine: Analyzing the Infamous Infostealer's Backend." *ESET Research / WeLiveSecurity*, November 8, 2024. URL: https://www.welivesecurity.com/en/eset-research/life-crooked-redline-analyzing-infamous-infostealers-backend/.
- **Use:** RedLine Stealer backend analysis; infostealer-as-a-service operations.

**[55]** Microsoft Threat Intelligence. "Lumma Stealer: Breaking Down the Delivery Techniques and Capabilities of a Prolific Infostealer." *Microsoft Security Blog*, May 21, 2025. URL: https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/.
- **Use:** Lumma Stealer technical analysis; illustrates infostealer sophistication and the PPI ecosystem.

**[56]** S. Pastrana, A. Hutchings, D. R. Thomas, and J. Tapiador. "Malware Finances and Operations: A Data-Driven Study of the Value Chain for Infections and Compromised Access." *arXiv:2306.15726*, 2023.
- **Use:** Infostealer value chain pricing data ($75–$200/mo MaaS, $1–$350 device sales); economic quantification of bypass cost.

**[57]** K. Drakonakis, S. Ioannidis, and J. Polakis. "The Cookie Hunter: Automated Black-box Auditing for Web Authentication and Authorization Flaws." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2020. DOI: 10.1145/3372297.3417869.
- **Use:** Large-scale cookie hijacking vulnerability study; demonstrates infostealer attack surface.

---

## 10. Anti-Detect Browser & Proxy Economics

**[58]** R. van Wegberg, B. Klievink, M. van Eeten, et al. "Plug and Prey? Measuring the Commoditization of Cybercrime via Online Anonymous Markets." In *Proc. USENIX Security Symposium*, pp. 1009–1026, 2018.
- **Use:** Cybercrime commoditization; supports anti-detect market analysis and conjunctive cost model.

**[59]** K. Thomas et al. "Framing Dependencies Introduced by Underground Commoditization." In *Proc. Workshop on the Economics of Information Security (WEIS)*, 2015.
- **Use:** Underground market dependencies; supports Tragedy of the Commons analysis for IP reputation.

**[60]** Cloudflare, Inc. "Bot Management Technical Documentation." *Cloudflare Docs*, 2023–2024.
- **Use:** Grey literature; architectural intent for Turnstile Managed Challenge. Cited for mechanism description, not efficacy proof.

**[61]** Google Chrome Security Team. "Device Bound Session Credentials (DBSC)." *Chrome for Developers*, 2024. URL: https://developers.chrome.com/docs/web-platform/device-bound-session-credentials.
- **Use:** Official DBSC developer documentation.

**[62]** Human Security, Inc. (formerly PerimeterX). "The Economics of Bot Mitigation." *Industry Whitepaper*, 2022.
- **Use:** Grey literature; stateful telemetry operational description.

**[63]** Kasada Pty Ltd. "Polymorphic Security Technical Documentation." *Industry Documentation*, 2023.
- **Use:** Grey literature; VM-based defense commercial implementation.

**[64]** DataDome SAS. "Bot Detection and Mitigation Technical Overview." *Industry Documentation*, 2023.
- **Use:** Grey literature; stateful behavioral telemetry commercial implementation.

---

## 11. Threat Modeling & Standards

**[65]** P. A. Grassi et al. "Digital Identity Guidelines." *NIST Special Publication 800-63-3*, 2017.
- **Use:** Authenticated threat model boundaries; authoritative for ATO quadrants.

**[66]** OWASP Foundation. "Automated Threat Handbook." *OWASP Project*, 2018–2024. URL: https://owasp.org/www-project-automated-threats-to-web-applications/.
- **Use:** Anonymous/scraping attack-objective taxonomy; authoritative for anonymous quadrants.

**[67]** R. Fielding and J. Reschke, Eds. "The OAuth 2.0 Authorization Framework: Bearer Token Usage." *RFC 6750*, IETF, October 2012.
- **Use:** Bearer token semantics; portability property.

**[68]** M. Jones, J. Bradley, and N. Sakimura. "JSON Web Token (JWT)." *RFC 7519*, IETF, May 2015.
- **Use:** Token format; foundational for token semiotics analysis.

**[69]** D. Fett, B. Campbell, J. Bradley, T. Lodderstedt, M. Jones, and D. Waite. "OAuth 2.0 Demonstrating Proof of Possession (DPoP)." *RFC 9449*, IETF, September 2023.
- **Use:** Proof-of-possession mechanism; contrasts with bearer token portability.

**[70]** J. H. Saltzer and M. D. Schroeder. "The Protection of Information in Computer Systems." *Proc. IEEE*, Vol. 63, No. 9, pp. 1278–1308, 1975.
- **Use:** Foundational security principles; referenced in historical context.

---

## 12. Supporting Academic References

**[71]** E. Bursztein, M. Martin, and J. C. Mitchell. "Text-based CAPTCHA Strengths and Weaknesses." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, 2012. DOI: 10.1145/2046707.2046724.
- **Use:** CAPTCHA security analysis; represents previous-generation anti-automation.

**[72]** J. Bonneau, C. Herley, P. C. van Oorschot, and F. Stajano. "Passwords and the Evolution of Imperfect Authentication." *Commun. ACM*, Vol. 58, No. 7, pp. 78–87, 2015. DOI: 10.1145/2699390.
- **Use:** Authentication evolution; supports historical arc in Section 2.

**[73]** M. Guerar, L. Verderame, M. Migliardi, F. Palmieri, and A. Merlo. "Gotta CAPTCHA 'Em All: A Survey of 20 Years of the Human-or-Computer Dilemma." *ACM Comput. Surv.*, Vol. 54, No. 9, Article 192, pp. 1–33, 2021. DOI: 10.1145/3477142.
- **Use:** Comprehensive CAPTCHA survey; historical context for Section 2.2.

**[74]** E. Ulqinaku, H. Assal, A. A. Gkaniatsas, S. Schechter, and S. Capkun. "Is Real-time Phishing Eliminated with FIDO?" In *Proc. USENIX Security Symposium*, 2021.
- **Use:** FIDO2 phishing resistance analysis; supports Section 7.2 on Passkeys.

**[75]** L. Allodi. "Economic Factors of Vulnerability Trade and Exploitation: Empirical Evidence from a Prominent Russian Cybercrime Market." In *Proc. ACM Conference on Computer and Communications Security (CCS)*, pp. 1483–1499, 2017. DOI: 10.1145/3133956.3133960.
- **Use:** Cybercrime market pricing data; supports underground economy pricing claims.

**[76]** M. Jones and D. Hardt. "The OAuth 2.0 Authorization Framework: Bearer Token Usage." *RFC 6750*, IETF, October 2012. DOI: 10.17487/RFC6750.
- **Use:** Bearer token semantics and portability properties; cited for bearer token characterization of VM attestation outputs.

**[77]** M. Jones, J. Bradley, and N. Sakimura. "JSON Web Token (JWT)." *RFC 7519*, IETF, May 2015. DOI: 10.17487/RFC7519.
- **Use:** Standard token format; supports analysis of bearer token portability in client-side anti-automation contexts.

**[78]** D. Fett, B. Campbell, J. Bradley, T. Lodderstedt, M. Jones, and D. Waite. "OAuth 2.0 Demonstrating Proof of Possession (DPoP)." *RFC 9449*, IETF, September 2023. DOI: 10.17487/RFC9449.
- **Use:** Proof-of-possession mechanism for bound tokens; contrasts with bearer token portability in DBSC context.

---

## Reference Count Summary

| Category | Count |
|----------|-------|
| SoK Precedent | 5 |
| Browser Fingerprinting | 9 |
| Behavioral Biometrics & Sensor Telemetry | 9 |
| Obfuscation & Deobfuscation | 7 |
| Hardware-Anchored Auth | 5 |
| DBSC | 2 |
| Privacy Pass / PATs | 8 |
| Economics of Security | 7 |
| Infostealer / PPI Malware | 5 |
| Anti-Detect Browser & Proxy | 4 |
| Threat Modeling & Standards | 6 |
| Token Standards (RFC) | 3 |
| Supporting Academic | 5 |
| **Total** | **78** |

**2021–2025 references:** 30+ (meets ≥15 requirement).

**Note on grey literature citations:** All vendor URLs must be archived via the Wayback Machine at submission time and citations must use permanent archive links per the Wayback Machine Mandate. Live URLs are listed here for reference during drafting; archiving must be completed before finalization.
