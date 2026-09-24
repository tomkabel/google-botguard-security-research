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

| Variant | a-dom | a-role | b-xdotool | c-vlm / glm-5.3-flash | c-vlm / kimi-k3 |
|---|---|---|---|---|---|
| base form (control) | 2/2 | 2/2 | 2/2 | 2/2 · 11 calls · 37 s | – |
| v1 reworded labels | 2/2 | 2/2 | 2/2 | 2/2 · 11.5 calls · 47 s | – |
| v2 German labels/title, button 'Weiter' | 0/2 | 0/2 | 0/2 | 2/2 · 12 calls · 35 s | 1/1 · 15 calls · 78 s |
| v3 randomised ids/names | 0/2 | 0/2 | 2/2 | 2/2 · 11 calls · 27 s | – |
| v4 optional decoy field placed first | 2/2 | 2/2 | 0/2 | 2/2 · 16 calls · 30 s | – |
| v5 two fields per page, reordered | 0/2 | 0/2 | 0/2 | 2/2 · 17.5 calls · 34 s | 1/1 · 20 calls · 107 s |
| v6 icon button placed above the field | 0/2 | 0/2 | 2/2 | 1/2 · 19.5 calls · 72 s | 1/1 · 16 calls · 164 s |
| v7 dropdown for city | 0/2 | 0/2 | 0/2 | 2/2 · 12.5 calls · 25 s | 1/1 · 15 calls · 76 s |
| v8 checkbox for confirmation | 0/2 | 0/2 | 0/2 | 2/2 · 12 calls · 27 s | 1/1 · 13 calls · 58 s |
| v9 combined: German, random ids, decoy field, button above, dropdown, checkbox | 0/2 | 0/2 | 0/2 | 2/2 · 20 calls · 37 s | 1/1 · 17 calls · 152 s |
| All variants (v1–v9) | 4/18 | 4/18 | 6/18 | 17/18 · €0.0028/success | 6/6 · €0.1348/success |

- Honeypot hits (runs): a-dom 12, a-role 0, b-xdotool 0, c-vlm / glm-5.3-flash 0, c-vlm / kimi-k3 0.
- Experiment B LLM spend: €0.8603.

## Experiment A: kinematic detector on point-to-click movements

| Movement source | Movements | Flagged as bot | Median samples (50 Hz) | Median straightness | Median duration (s) |
|---|---|---|---|---|---|
| Balabit human, held-out users | 19136 | 1718 (9%) | 61 | 0.827 | 1.22 |
| Synthetic straight/teleport, held-out | 19136 | 18264 (95%) | 5 | 1.000 | 0.08 |
| (a) Playwright CDP click (a-role) | 42 | 42 (100%) | 1 | 1.000 | 0.00 |
| (b) scripted xdotool, pointer jumps | 98 | 98 (100%) | 1 | 1.000 | 0.00 |
| (c) VLM agent, glm-5.3-flash | 154 | 154 (100%) | 1 | 1.000 | 0.00 |
| (c) VLM agent, kimi-k3 | 59 | 59 (100%) | 1 | 1.000 | 0.00 |
| (e) smoothed OS input, min-jerk | 100 | 0 (0%) | 24 | 0.956 | 0.46 |

- Rule (grid search over samples < N or straightness > S): bot iff straightness > 0.9925; fitted on Balabit users user15, user16, user21, user23, user35, user7 (n = 68578), held-out accuracy 93.2% on users user12, user20, user29, user9 (n = 38272; humans flagged 9.0%, synthetic bots flagged 95.4%).
