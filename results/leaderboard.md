*Updated 2026-10-01 17:46 UTC · 30 gold cases · 3 seeds each · production prompt at `1554bc4`*

**Recommendation:** the production model is the best eligible candidate.

| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | **1.00** [1.0, 1.0] | 1.00 | 1.00 | 100% | 1875.6 / 2308.1 | 0.6 | not eligible: covered 13% of the cases in the time budget; p90 latency 2308s; experiment |
| 2 | gemma4:12b | ollama | **0.93** [0.804, 1.0] | 0.93 | 0.99 | 100% | 79.0 / 307.7 | 8.0 | not eligible: p90 latency 308s |
| 3 | qwen3:4b | ollama | **0.81** [0.658, 0.935] | 0.83 | 0.86 | 99% | 33.8 / 92.6 | 24.0 | eligible |
| 4 | qwen3.5:9b | ollama | **0.79** [0.615, 0.921] | 0.80 | 0.88 | 100% | 52.5 / 98.3 | 19.0 | eligible |
| 5 | ministral-3:3b | ollama | **0.67** [0.509, 0.819] | 0.70 | 0.83 | 100% | 26.4 / 53.3 | 37.7 | eligible |
| 6 | qwen3:4b (llama.cpp) | llamacpp | **0.66** [0.501, 0.797] | 0.70 | 0.87 | 100% | 21.2 / 72.5 | 32.6 | eligible |
| 7 | granite4.2:8b | ollama | **0.62** [0.438, 0.755] | 0.57 | 0.79 | 42% | 92.6 / 183.0 | 10.5 | not eligible: valid answers 42%; p90 latency 183s |
| 8 | qwen3:8b | ollama | **0.59** [0.418, 0.744] | 0.63 | 0.88 | 100% | 38.7 / 139.8 | 17.2 | eligible |
| 9 | qwen3:4b-q4_K_M | ollama | **0.58** [0.408, 0.711] | 0.60 | 0.80 | 100% | 23.5 / 82.4 | 28.5 | eligible |
| 10 | ministral-3:8b | ollama | **0.57** [0.43, 0.665] | 0.63 | 0.90 | 100% | 50.5 / 165.1 | 14.1 | not eligible: p90 latency 165s |
| 11 | gemma3n:e2b | ollama | **0.54** [0.336, 0.685] | 0.53 | 0.70 | 100% | 14.5 / 61.8 | 41.1 | eligible |
| 12 | granite4.2:3b | ollama | **0.53** [0.4, 0.634] | 0.60 | 0.68 | 70% | 25.4 / 38.6 | 51.5 | not eligible: valid answers 70% |
| 13 | qwen3.5:4b | ollama | **0.50** [0.357, 0.645] | 0.57 | 0.86 | 100% | 25.7 / 107.7 | 23.9 | eligible |
| 14 | qwen3.5:2b-q4_K_M | ollama | **0.43** [0.276, 0.588] | 0.47 | 0.79 | 100% | 9.4 / 37.7 | 67.1 | eligible |
| 15 | gemma3:4b (llama.cpp) | llamacpp | **0.40** [0.22, 0.565] | 0.43 | 0.83 | 100% | 25.1 / 81.6 | 28.2 | eligible |
| 16 | qwen3:1.7b | ollama | **0.39** [0.229, 0.521] | 0.43 | 0.77 | 100% | 13.5 / 28.6 | 69.0 | eligible |
| 17 | lfm2.5:8b-a1b | ollama | **0.39** [0.259, 0.498] | 0.47 | 0.78 | 100% | 5.7 / 25.8 | 101.3 | eligible |
| 18 | gemma3:12b | ollama | **0.35** [0.271, 0.417] | 0.47 | 0.98 | 100% | 50.0 / 188.1 | 12.8 | not eligible: p90 latency 188s |
| 19 | qwen3.5:2b | ollama | **0.35** [0.179, 0.484] | 0.37 | 0.73 | 100% | 12.2 / 47.3 | 52.6 | eligible |
| 20 | qwen3.5:0.8b | ollama | **0.34** [0.177, 0.48] | 0.40 | 0.68 | 100% | 5.3 / 20.4 | 120.6 | eligible |
| 21 | Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | **0.34** [0.183, 0.452] | 0.40 | 0.77 | 100% | 38.9 / 121.9 | 19.0 | eligible |
| 22 | phi4-mini:3.8b | ollama | **0.30** [0.163, 0.431] | 0.37 | 0.73 | 100% | 18.8 / 61.7 | 38.9 | eligible |
| 23 | gemma3:4b (prompt v1) | ollama | **0.29** [0.161, 0.375] | 0.40 | 0.92 | 100% | 25.6 / 43.4 | 41.2 | not eligible: experiment |
| 24 | llama3.1:8b | ollama | **0.20** [0.083, 0.31] | 0.30 | 0.90 | 100% | 25.6 / 72.6 | 31.4 | eligible |
| 25 | gemma4:e2b | ollama | **0.20** [0.071, 0.308] | 0.30 | 0.97 | 100% | 13.4 / 60.8 | 42.5 | eligible |
| 26 | granite4:7b-a1b-h | ollama | **0.16** [0.059, 0.261] | 0.27 | 0.84 | 100% | 7.7 / 36.2 | 72.5 | eligible |
| 27 | llama3.2:3b | ollama | **0.10** [0.048, 0.15] | 0.23 | 0.90 | 100% | 19.5 / 50.7 | 42.9 | eligible |
| – | gemma3:4b | ollama | | | | | | | not run yet |
| – | gemma3n:e4b | ollama | | | | | | | not run yet |

### Same model, different back-ends or formats

**gemma3:4b on Ollama vs llama.cpp.** Same 4-bit Gemma 3 4B weights served by two engines, same prompt, seeds and temperature.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| gemma3:4b | | | not measured yet | | |
| gemma3:4b (llama.cpp) | llamacpp | `gemma-3-4b-it-Q4_K_M` | 0.40 [0.22, 0.565] | 0.83 | 25.1 / 81.6 |

**qwen3:4b on Ollama vs llama.cpp.** Qwen3 4B from the Ollama library (two tags) and the official Qwen GGUF on llama.cpp; thinking off in all. Tags can point to different builds (see the digests in results/leaderboard.json).

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:4b | ollama | `qwen3:4b` | 0.81 [0.658, 0.935] | 0.86 | 33.8 / 92.6 |
| qwen3:4b-q4_K_M | ollama | `qwen3:4b-q4_K_M` | 0.58 [0.408, 0.711] | 0.80 | 23.5 / 82.4 |
| qwen3:4b (llama.cpp) | llamacpp | `Qwen3-4B-Q4_K_M` | 0.66 [0.501, 0.797] | 0.87 | 21.2 / 72.5 |

**8B at 4 bits vs 8B at ~2 bits (ternary).** A conventional 4-bit 8B model on Ollama and a ternary 8B (Bonsai) on the PrismML fork of llama.cpp.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:8b | ollama | `qwen3:8b` | 0.59 [0.418, 0.744] | 0.88 | 38.7 / 139.8 |
| Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | `Ternary-Bonsai-8B-PQ2_0` | 0.34 [0.183, 0.452] | 0.77 | 38.9 / 121.9 |

**27B compressed to fit the runner.** Ternary-Bonsai-2-27B (5.95 GB) is a ternary version of Qwen3.8-27B, whose 4-bit build does not fit in 16 GB of RAM. Measured on a sample only (4 cases, 1 seed): calls take many minutes on 4 vCPUs.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | `Ternary-Bonsai-2-27B-PTQ1_0` | 1.00 [1.0, 1.0] | 1.00 | 1875.6 / 2308.1 |
| Qwen3.8-27B at 4 bits (qwen3.8:27b-q4_K_M, 18 GB) | | | does not fit the free runner | | |
