| Config | Model | Pass | Honeypot hit | `navigator.webdriver` | Action p50 / p90 (s) | Run p50 (s) |
|---|---|---|---|---|---|---|
| a-dom | – | 10/10 | 10/10 | 10/10 | 0.07 / 0.11 | 1.3 |
| a-role | – | 10/10 | 0/10 | 10/10 | 0.11 / 0.14 | 1.4 |
| b-xdotool | – | 10/10 | 0/10 | 0/10 | 0.47 / 1.89 | 7.0 |
| c-vlm | gemma-4-26b-a4b | 10/10 | 0/10 | 0/10 | 3.37 / 10.44 | 174.4 |
| c-vlm | glm-5.3-flash | 10/10 | 0/10 | 0/10 | 1.40 / 1.89 | 26.3 |
| c-vlm | qwen3.8-27b | 10/10 | 0/10 | 0/10 | 1.57 / 2.54 | 44.1 |
| d-hybrid | gemma-4-26b-a4b | 10/10 | 0/10 | 0/10 | 3.68 / 9.12 | 158.3 |
| d-hybrid | glm-5.3-flash | 10/10 | 0/10 | 0/10 | 0.49 / 2.01 | 15.0 |
| d-hybrid | qwen3.8-27b | 9/10 | 0/10 | 0/10 | 1.83 / 3.09 | 42.7 |

| Config | Model | VLM calls/run | VLM call p50 / p90 (s) | LLM tokens in / out per call | Cost per success |
|---|---|---|---|---|---|
| c-vlm | gemma-4-26b-a4b | 18.5 | 6.18 / 10.71 | 645 / 887 | €0.0097 |
| c-vlm | glm-5.3-flash | 11 | 0.77 / 1.34 | 1,586 / 24 | €0.0019 |
| c-vlm | qwen3.8-27b | 18 | 1.45 / 2.09 | 1,336 / 95 | €0.0136 |
| d-hybrid | gemma-4-26b-a4b | 18 | 5.45 / 10.04 | 613 / 817 | €0.0085 |
| d-hybrid | glm-5.3-flash | 3.5 | 1.01 / 1.82 | 1,549 / 115 | €0.0010 |
| d-hybrid | qwen3.8-27b | 13 | 1.66 / 3.70 | 1,269 / 142 | €0.0125 |

- d-hybrid / gemma-4-26b-a4b: scripted control resumed after the VLM step in 0/10 runs.
- d-hybrid / glm-5.3-flash: scripted control resumed after the VLM step in 9/10 runs.
- d-hybrid / qwen3.8-27b: scripted control resumed after the VLM step in 0/10 runs.
- Total LLM spend: €0.4601.
