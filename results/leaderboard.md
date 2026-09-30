*Updated 2026-09-30 18:07 UTC · 30 gold cases · 3 seeds each · production prompt at `c9ccc85`*

**Recommendation:** the production model is the best eligible candidate.

| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | **1.00** [1.0, 1.0] | 1.00 | 1.00 | 100% | 1975.7 / 2443.5 | 0.6 | not eligible: covered 13% of the cases in the time budget; p90 latency 2444s; experiment |
| 2 | gemma4:12b | ollama | **0.89** [0.738, 1.0] | 0.90 | 0.99 | 100% | 57.4 / 204.0 | 11.6 | not eligible: p90 latency 204s |
| 3 | qwen3:4b | ollama | **0.75** [0.595, 0.889] | 0.77 | 0.87 | 100% | 21.1 / 39.5 | 47.1 | eligible |
| 4 | granite4.2:8b | ollama | **0.71** [0.531, 0.844] | 0.63 | 0.78 | 44% | 148.3 / 180.0 | 8.3 | not eligible: valid answers 44%; p90 latency 180s |
| 5 | qwen3:4b (llama.cpp) | llamacpp | **0.69** [0.518, 0.827] | 0.70 | 0.84 | 100% | 34.0 / 50.4 | 31.7 | eligible |
| 6 | qwen3.5:9b | ollama | **0.68** [0.496, 0.823] | 0.70 | 0.86 | 100% | 25.7 / 83.3 | 28.1 | eligible |
| 7 | ministral-3:3b | ollama | **0.67** [0.497, 0.815] | 0.70 | 0.83 | 100% | 26.5 / 53.7 | 37.3 | eligible |
| 8 | qwen3:8b | ollama | **0.59** [0.426, 0.744] | 0.63 | 0.88 | 100% | 39.1 / 141.2 | 17.0 | eligible |
| 9 | ministral-3:8b | ollama | **0.57** [0.438, 0.661] | 0.63 | 0.90 | 100% | 61.1 / 169.9 | 13.0 | not eligible: p90 latency 170s |
| 10 | gemma3n:e2b | ollama | **0.54** [0.349, 0.7] | 0.53 | 0.70 | 100% | 15.6 / 63.1 | 39.5 | eligible |
| 11 | qwen3:4b-q4_K_M | ollama | **0.53** [0.357, 0.685] | 0.57 | 0.86 | 100% | 21.6 / 58.9 | 36.6 | eligible |
| 12 | gemma3:4b | ollama | **0.52** [0.314, 0.689] | 0.53 | 0.84 | 100% | 24.9 / 92.0 | 26.2 | eligible |
| 13 | qwen3.5:4b | ollama | **0.50** [0.356, 0.65] | 0.57 | 0.86 | 100% | 23.9 / 106.1 | 24.8 | eligible |
| 14 | lfm2.5:8b-a1b | ollama | **0.49** [0.307, 0.66] | 0.50 | 0.73 | 100% | 9.0 / 39.2 | 66.2 | eligible |
| 15 | granite4.2:3b | ollama | **0.49** [0.38, 0.604] | 0.57 | 0.77 | 73% | 43.5 / 64.4 | 26.5 | not eligible: valid answers 73% |
| 16 | qwen3:1.7b | ollama | **0.44** [0.267, 0.556] | 0.47 | 0.76 | 100% | 14.7 / 37.7 | 56.0 | eligible |
| 17 | qwen3.5:2b-q4_K_M | ollama | **0.43** [0.275, 0.592] | 0.47 | 0.79 | 100% | 9.2 / 37.6 | 67.5 | eligible |
| 18 | gemma3:4b (llama.cpp) | llamacpp | **0.40** [0.217, 0.563] | 0.43 | 0.83 | 100% | 21.1 / 76.6 | 31.5 | eligible |
| 19 | gemma3:12b | ollama | **0.38** [0.312, 0.427] | 0.50 | 0.98 | 100% | 61.6 / 283.9 | 9.0 | not eligible: p90 latency 284s |
| 20 | qwen3.5:2b | ollama | **0.35** [0.181, 0.496] | 0.37 | 0.73 | 100% | 14.7 / 48.7 | 48.6 | eligible |
| 21 | qwen3.5:0.8b | ollama | **0.34** [0.171, 0.477] | 0.40 | 0.68 | 100% | 5.4 / 21.9 | 115.0 | eligible |
| 22 | Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | **0.34** [0.192, 0.458] | 0.40 | 0.77 | 100% | 38.9 / 122.1 | 19.0 | eligible |
| 23 | phi4-mini:3.8b | ollama | **0.30** [0.16, 0.437] | 0.37 | 0.73 | 100% | 17.3 / 61.8 | 39.9 | eligible |
| 24 | gemma3:4b (prompt v1) | ollama | **0.29** [0.159, 0.38] | 0.40 | 0.92 | 100% | 25.6 / 43.4 | 41.2 | not eligible: experiment |
| 25 | gemma3n:e4b | ollama | **0.28** [0.146, 0.368] | 0.37 | 0.89 | 100% | 20.3 / 80.8 | 30.6 | eligible |
| 26 | llama3.1:8b | ollama | **0.20** [0.076, 0.312] | 0.30 | 0.90 | 100% | 18.1 / 47.3 | 46.7 | eligible |
| 27 | granite4:7b-a1b-h | ollama | **0.16** [0.061, 0.267] | 0.27 | 0.84 | 100% | 7.2 / 35.7 | 74.3 | eligible |
| 28 | llama3.2:3b | ollama | **0.10** [0.047, 0.149] | 0.23 | 0.90 | 100% | 22.6 / 54.0 | 39.2 | eligible |
| 29 | gemma4:e2b | ollama | **0.10** [0.045, 0.143] | 0.23 | 0.94 | 100% | 10.6 / 40.3 | 60.9 | eligible |

### Same model, different back-ends or formats

**gemma3:4b on Ollama vs llama.cpp.** Same 4-bit Gemma 3 4B weights served by two engines, same prompt, seeds and temperature.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| gemma3:4b | ollama | `gemma3:4b` | 0.52 [0.314, 0.689] | 0.84 | 24.9 / 92.0 |
| gemma3:4b (llama.cpp) | llamacpp | `gemma-3-4b-it-Q4_K_M` | 0.40 [0.217, 0.563] | 0.83 | 21.1 / 76.6 |

**qwen3:4b on Ollama vs llama.cpp.** Qwen3 4B from the Ollama library (two tags) and the official Qwen GGUF on llama.cpp; thinking off in all. Tags can point to different builds (see the digests in results/leaderboard.json).

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:4b | ollama | `qwen3:4b` | 0.75 [0.595, 0.889] | 0.87 | 21.1 / 39.5 |
| qwen3:4b-q4_K_M | ollama | `qwen3:4b-q4_K_M` | 0.53 [0.357, 0.685] | 0.86 | 21.6 / 58.9 |
| qwen3:4b (llama.cpp) | llamacpp | `Qwen3-4B-Q4_K_M` | 0.69 [0.518, 0.827] | 0.84 | 34.0 / 50.4 |

**8B at 4 bits vs 8B at ~2 bits (ternary).** A conventional 4-bit 8B model on Ollama and a ternary 8B (Bonsai) on the PrismML fork of llama.cpp.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:8b | ollama | `qwen3:8b` | 0.59 [0.426, 0.744] | 0.88 | 39.1 / 141.2 |
| Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | `Ternary-Bonsai-8B-PQ2_0` | 0.34 [0.192, 0.458] | 0.77 | 38.9 / 122.1 |

**27B compressed to fit the runner.** Ternary-Bonsai-2-27B (5.95 GB) is a ternary version of Qwen3.8-27B, whose 4-bit build does not fit in 16 GB of RAM. Measured on a sample only (4 cases, 1 seed): calls take many minutes on 4 vCPUs.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | `Ternary-Bonsai-2-27B-PTQ1_0` | 1.00 [1.0, 1.0] | 1.00 | 1975.7 / 2443.5 |
| Qwen3.8-27B at 4 bits (qwen3.8:27b-q4_K_M, 18 GB) | | | does not fit the free runner | | |
