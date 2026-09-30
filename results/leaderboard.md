*Updated 2026-09-30 12:40 UTC · 30 gold cases · 3 seeds each · production prompt at `5a1e733`*

**Recommendation:** qwen3:4b beats gemma3:4b by +0.310 macro-F1 (paired 95% CI [0.089, 0.535]).

| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | **1.00** [1.0, 1.0] | 1.00 | 1.00 | 100% | 1739.5 / 2152.3 | 0.6 | not eligible: covered 13% of the cases in the time budget; p90 latency 2152s; experiment |
| 2 | qwen3:4b | ollama | **0.81** [0.657, 0.933] | 0.83 | 0.86 | 99% | 35.8 / 91.3 | 23.7 | eligible |
| 3 | ministral-3:3b | ollama | **0.69** [0.516, 0.84] | 0.70 | 0.83 | 98% | 42.5 / 57.1 | 27.4 | eligible |
| 4 | granite4.2:8b | ollama | **0.62** [0.438, 0.755] | 0.57 | 0.79 | 42% | 101.9 / 190.8 | 9.9 | not eligible: valid answers 42%; p90 latency 191s |
| 5 | qwen3.5:9b | ollama | **0.61** [0.432, 0.771] | 0.63 | 0.83 | 100% | 35.8 / 183.1 | 14.7 | not eligible: p90 latency 183s |
| 6 | qwen3:8b | ollama | **0.59** [0.416, 0.753] | 0.63 | 0.88 | 100% | 33.3 / 140.9 | 17.9 | eligible |
| 7 | ministral-3:8b | ollama | **0.57** [0.43, 0.665] | 0.63 | 0.90 | 100% | 47.9 / 164.0 | 14.5 | not eligible: p90 latency 164s |
| 8 | granite4.2:3b | ollama | **0.56** [0.438, 0.656] | 0.63 | 0.72 | 76% | 52.9 / 87.0 | 23.8 | not eligible: valid answers 76% |
| 9 | qwen3:4b-q4_K_M | ollama | **0.53** [0.369, 0.7] | 0.57 | 0.86 | 100% | 21.5 / 58.8 | 37.0 | eligible |
| 10 | gemma3:4b | ollama | **0.50** [0.325, 0.66] | 0.53 | 0.84 | 99% | 22.2 / 63.4 | 35.2 | eligible |
| 11 | qwen3.5:4b | ollama | **0.50** [0.356, 0.65] | 0.57 | 0.86 | 100% | 23.7 / 106.2 | 24.7 | eligible |
| 12 | gemma3n:e2b | ollama | **0.48** [0.273, 0.642] | 0.47 | 0.74 | 100% | 11.8 / 42.1 | 57.3 | eligible |
| 13 | phi4-mini:3.8b | ollama | **0.48** [0.318, 0.598] | 0.53 | 0.80 | 100% | 30.8 / 65.5 | 30.2 | eligible |
| 14 | qwen3.5:2b-q4_K_M | ollama | **0.43** [0.276, 0.583] | 0.47 | 0.79 | 100% | 9.6 / 38.0 | 66.4 | eligible |
| 15 | gemma3:4b (llama.cpp) | llamacpp | **0.40** [0.22, 0.565] | 0.43 | 0.83 | 100% | 22.6 / 78.8 | 30.4 | eligible |
| 16 | qwen3:1.7b | ollama | **0.39** [0.235, 0.514] | 0.43 | 0.77 | 100% | 12.6 / 27.6 | 72.4 | eligible |
| 17 | lfm2.5:8b-a1b | ollama | **0.39** [0.261, 0.503] | 0.47 | 0.78 | 100% | 4.8 / 19.3 | 131.5 | eligible |
| 18 | gemma3:12b | ollama | **0.38** [0.312, 0.426] | 0.50 | 0.98 | 100% | 53.4 / 285.8 | 9.4 | not eligible: p90 latency 286s |
| 19 | gemma3n:e4b | ollama | **0.36** [0.224, 0.485] | 0.43 | 0.86 | 100% | 22.3 / 118.4 | 22.7 | eligible |
| 20 | qwen3.5:2b | ollama | **0.35** [0.174, 0.496] | 0.37 | 0.73 | 100% | 11.8 / 47.5 | 53.2 | eligible |
| 21 | qwen3.5:0.8b | ollama | **0.34** [0.168, 0.487] | 0.40 | 0.68 | 100% | 5.4 / 20.4 | 120.6 | eligible |
| 22 | Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | **0.34** [0.194, 0.459] | 0.40 | 0.77 | 100% | 36.7 / 122.2 | 19.4 | eligible |
| 23 | gemma3:4b (prompt v1) | ollama | **0.29** [0.149, 0.375] | 0.40 | 0.92 | 100% | 25.6 / 43.4 | 41.2 | not eligible: experiment |
| 24 | llama3.1:8b | ollama | **0.20** [0.083, 0.31] | 0.30 | 0.90 | 100% | 18.5 / 47.4 | 46.4 | eligible |
| 25 | granite4:7b-a1b-h | ollama | **0.16** [0.061, 0.267] | 0.27 | 0.84 | 100% | 7.5 / 35.6 | 73.7 | eligible |
| 26 | llama3.2:3b | ollama | **0.10** [0.047, 0.149] | 0.23 | 0.90 | 100% | 19.3 / 49.6 | 43.7 | eligible |
| – | gemma4:12b | ollama | | | | | | | not run yet |
| – | gemma4:e2b | ollama | | | | | | | not run yet |
