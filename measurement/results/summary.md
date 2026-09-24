| Config | Model | Pass | Honeypot hit | `navigator.webdriver` | Action p50 / p90 (s) | Run p50 (s) |
|---|---|---|---|---|---|---|
| a-dom | – | 10/10 | 10/10 | 10/10 | 0.07 / 0.11 | 1.3 |
| a-role | – | 10/10 | 0/10 | 10/10 | 0.11 / 0.14 | 1.4 |
| b-xdotool | – | 10/10 | 0/10 | 0/10 | 0.47 / 1.89 | 7.0 |
| c-vlm | glm-5.3-flash | 10/10 | 0/10 | 0/10 | 1.40 / 1.89 | 26.3 |
| c-vlm | qwen3.8-27b | 10/10 | 0/10 | 0/10 | 1.57 / 2.54 | 44.1 |
| d-hybrid | glm-5.3-flash | 10/10 | 0/10 | 0/10 | 0.49 / 2.01 | 15.0 |
| d-hybrid | qwen3.8-27b | 9/10 | 0/10 | 0/10 | 1.83 / 3.09 | 42.7 |

| Config | Model | VLM calls/run | VLM call p50 / p90 (s) | LLM tokens in / out per call | Cost per success |
|---|---|---|---|---|---|
| c-vlm | glm-5.3-flash | 11 | 0.77 / 1.34 | 1,586 / 24 | €0.0019 |
| c-vlm | qwen3.8-27b | 18 | 1.45 / 2.09 | 1,336 / 95 | €0.0136 |
| d-hybrid | glm-5.3-flash | 3.5 | 1.01 / 1.82 | 1,549 / 115 | €0.0010 |
| d-hybrid | qwen3.8-27b | 13 | 1.66 / 3.70 | 1,269 / 142 | €0.0125 |

- d-hybrid / glm-5.3-flash: scripted control resumed after the VLM step in 9/10 runs.
- d-hybrid / qwen3.8-27b: scripted control resumed after the VLM step in 0/10 runs.
- Total LLM spend: €0.2779.

## Experiment B: cross-site generalisation (pass = server flow_done with all answers correct)

| Variant | a-dom | a-role | b-xdotool | c-vlm / glm-5.3-flash | c-vlm / kimi-k3 | t-a11y / glm-5.3-flash |
|---|---|---|---|---|---|---|
| base form (control) | 6/6 | 6/6 | 6/6 | 6/6 · 11 calls · 25 s | – | 6/6 · 11 calls · 9 s |
| v1 reworded labels | 6/6 | 6/6 | 6/6 | 6/6 · 11 calls · 23 s | – | 6/6 · 12 calls · 13 s |
| v2 German labels/title, button 'Weiter' | 0/6 | 0/6 | 0/6 | 6/6 · 11 calls · 25 s | 1/1 · 15 calls · 78 s | 6/6 · 11 calls · 10 s |
| v3 randomised ids/names | 0/6 | 0/6 | 6/6 | 6/6 · 11 calls · 27 s | – | 6/6 · 11 calls · 6 s |
| v4 optional decoy field placed first | 6/6 | 6/6 | 0/6 | 6/6 · 16 calls · 29 s | – | 6/6 · 11 calls · 7 s |
| v5 two fields per page, reordered | 0/6 | 0/6 | 0/6 | 6/6 · 17 calls · 34 s | 1/1 · 20 calls · 107 s | 6/6 · 13 calls · 10 s |
| v6 icon button placed above the field | 0/6 | 0/6 | 6/6 | 2/6 · 19 calls · 59 s | 1/1 · 16 calls · 164 s | 6/6 · 11 calls · 8 s |
| v7 dropdown for city | 0/6 | 0/6 | 0/6 | 6/6 · 12 calls · 26 s | 1/1 · 15 calls · 76 s | 6/6 · 11 calls · 7 s |
| v8 checkbox for confirmation | 0/6 | 0/6 | 0/6 | 6/6 · 11 calls · 24 s | 1/1 · 13 calls · 58 s | 6/6 · 11 calls · 7 s |
| v9 combined: German, random ids, decoy field, button above, dropdown, checkbox | 0/6 | 0/6 | 0/6 | 6/6 · 18.5 calls · 34 s | 1/1 · 17 calls · 152 s | 6/6 · 11 calls · 8 s |
| All variants (v1–v9) | 12/54 | 12/54 | 18/54 | 50/54 · €0.0029/success | 6/6 · €0.1348/success | 54/54 · €0.0005/success |

- Honeypot hits (runs): a-dom 36, a-role 0, b-xdotool 0, c-vlm / glm-5.3-flash 0, c-vlm / kimi-k3 0, t-a11y / glm-5.3-flash 0.
- Experiment B LLM spend: €0.9960.

### Per agent (v1–v9 pooled; 95% Wilson interval; cost per success = v1–v9 spend / v1–v9 successes)

| Agent | Base form | Variants v1–v9 | 95% CI (Wilson) | Cost per success |
|---|---|---|---|---|
| a-dom | 6/6 | 12/54 | 13%–35% | – |
| a-role | 6/6 | 12/54 | 13%–35% | – |
| b-xdotool | 6/6 | 18/54 | 22%–47% | – |
| c-vlm / glm-5.3-flash | 6/6 | 50/54 | 82%–97% | €0.0029 |
| c-vlm / kimi-k3 | – | 6/6 | 61%–100% | €0.1348 |
| t-a11y / glm-5.3-flash | 6/6 | 54/54 | 93%–100% | €0.0005 |

### Script repair: a-dom selectors adapted per variant (lines changed, not minutes)

| Variant | v1 | v2 | v3 | v4 | v5 | v6 | v7 | v8 | v9 | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Lines changed (vs base a-dom script) | 0 | 1 | 5 | 0 | 3 | 1 | 1 | 1 | 6 | 18 |
| Adapted a-dom passes (server) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 9/9 |

## Experiment A: kinematic detector on point-to-click movements

| Movement source | Movements | Flagged as bot (rule) | Flagged (classifier) | Median samples (50 Hz) | Median straightness | Median duration (s) |
|---|---|---|---|---|---|---|
| Balabit human, held-out users | 19136 | 1718 (9%) | 43 (0%) | 61 | 0.827 | 1.22 |
| Synthetic straight/teleport, held-out | 19136 | 18264 (95%) | 7859 (41%) | 5 | 1.000 | 0.08 |
| Synthetic min-jerk, held-out | 19136 | 287 (1%) | 17222 (90%) | 61 | 0.882 | 1.22 |
| (a) Playwright CDP click (a-role) | 126 | 126 (100%) | 24 (19%) | 1 | 1.000 | 0.00 |
| (b) scripted xdotool, pointer jumps | 98 | 98 (100%) | 0 (0%) | 1 | 1.000 | 0.00 |
| (c) VLM agent, glm-5.3-flash | 455 | 455 (100%) | 0 (0%) | 1 | 1.000 | 0.00 |
| (c) VLM agent, kimi-k3 | 59 | 59 (100%) | 0 (0%) | 1 | 1.000 | 0.00 |
| (e) smoothed OS input, min-jerk | 100 | 0 (0%) | 35 (35%) | 24 | 0.956 | 0.46 |
| (t) text-only LLM on accessibility tree, Playwright click | 312 | 312 (100%) | 0 (0%) | 1 | 1.000 | 0.00 |

- Rule (grid search over samples < N or straightness > S): bot iff straightness > 0.9925; fitted on Balabit users user15, user16, user21, user23, user35, user7 (n = 68578), held-out accuracy 93.2% on users user12, user20, user29, user9 (n = 38272; humans flagged 9.0%, synthetic bots flagged 95.4%).
- Classifier: logistic regression (numpy Newton/IRLS, L2) on samples, duration_s, v_mean, v_std, a_std, jerk_mean, curvature, pause_s, straightness; bot class = min-jerk paths with bow and jitter, paired human duration and pause (same generator family as e-smooth, so the (e) row is in-distribution). Held-out ROC AUC 0.9985; at the threshold for 90% TPR on held-out min-jerk bots, held-out humans flagged 0.22% (n = 38272).
