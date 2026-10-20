*Updated 2026-10-20 13:43 UTC · 30 gold cases · 3 seeds each · production prompt at `6a6c9ce`*

**Recommendation:** the production model is the best eligible candidate.

| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | **1.00** [1.0, 1.0] | 1.00 | 1.00 | 100% | 2016.8 / 2493.4 | 0.6 | not eligible: covered 13% of the cases in the time budget; p90 latency 2493s; experiment |
| 2 | gemma4:12b | ollama | **0.89** [0.738, 1.0] | 0.90 | 0.99 | 100% | 61.8 / 210.3 | 11.2 | not eligible: p90 latency 210s |
| 3 | qwen3:4b | ollama | **0.81** [0.657, 0.933] | 0.83 | 0.86 | 99% | 39.6 / 95.1 | 22.5 | eligible |
| 4 | qwen3.5:9b | ollama | **0.74** [0.597, 0.875] | 0.77 | 0.87 | 100% | 32.7 / 124.7 | 19.8 | eligible |
| 5 | ministral-3:3b | ollama | **0.67** [0.465, 0.823] | 0.67 | 0.79 | 100% | 28.9 / 76.5 | 28.4 | eligible |
| 6 | qwen3:4b (llama.cpp) | llamacpp | **0.66** [0.504, 0.794] | 0.70 | 0.87 | 100% | 22.9 / 73.8 | 31.4 | eligible |
| 7 | granite4.2:8b | ollama | **0.62** [0.446, 0.764] | 0.57 | 0.79 | 42% | 108.6 / 198.8 | 9.3 | not eligible: valid answers 42%; p90 latency 199s |
| 8 | gemma3:4b | ollama | **0.61** [0.419, 0.771] | 0.63 | 0.86 | 99% | 15.8 / 43.5 | 50.6 | eligible |
| 9 | qwen3.5:4b | ollama | **0.59** [0.436, 0.732] | 0.63 | 0.86 | 100% | 19.9 / 73.9 | 33.5 | eligible |
| 10 | qwen3:4b-q4_K_M | ollama | **0.58** [0.409, 0.71] | 0.60 | 0.80 | 100% | 28.7 / 86.3 | 26.0 | eligible |
| 11 | ministral-3:8b | ollama | **0.57** [0.438, 0.661] | 0.63 | 0.90 | 100% | 60.2 / 168.0 | 13.0 | not eligible: p90 latency 168s |
| 12 | gemma3:4b (llama.cpp) | llamacpp | **0.56** [0.384, 0.716] | 0.60 | 0.84 | 100% | 29.5 / 74.9 | 28.0 | eligible |
| 13 | lfm2.5:8b-a1b | ollama | **0.49** [0.307, 0.66] | 0.50 | 0.73 | 100% | 8.4 / 38.7 | 67.9 | eligible |
| 14 | granite4.2:3b | ollama | **0.49** [0.38, 0.604] | 0.57 | 0.77 | 73% | 45.7 / 68.2 | 25.3 | not eligible: valid answers 73% |
| 15 | phi4-mini:3.8b | ollama | **0.48** [0.318, 0.598] | 0.53 | 0.80 | 100% | 12.1 / 30.9 | 69.3 | eligible |
| 16 | qwen3:8b | ollama | **0.44** [0.348, 0.533] | 0.53 | 0.88 | 100% | 23.4 / 64.0 | 33.9 | eligible |
| 17 | qwen3:1.7b | ollama | **0.44** [0.274, 0.567] | 0.47 | 0.76 | 100% | 16.3 / 39.4 | 52.2 | eligible |
| 18 | qwen3.5:2b-q4_K_M | ollama | **0.43** [0.225, 0.593] | 0.43 | 0.77 | 100% | 10.5 / 43.6 | 57.7 | eligible |
| 19 | qwen3.5:0.8b | ollama | **0.36** [0.165, 0.531] | 0.37 | 0.69 | 100% | 11.5 / 28.2 | 75.9 | eligible |
| 20 | Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | **0.36** [0.225, 0.49] | 0.43 | 0.83 | 100% | 64.5 / 170.7 | 12.7 | not eligible: p90 latency 171s |
| 21 | qwen3.5:2b | ollama | **0.36** [0.174, 0.525] | 0.40 | 0.79 | 100% | 9.8 / 26.6 | 82.9 | eligible |
| 22 | gemma3:12b | ollama | **0.35** [0.273, 0.416] | 0.47 | 0.97 | 100% | 69.8 / 294.9 | 8.6 | not eligible: p90 latency 295s |
| 23 | gemma3:4b (prompt v1) | ollama | **0.34** [0.242, 0.408] | 0.47 | 0.93 | 100% | 25.3 / 82.2 | 28.8 | not eligible: experiment |
| 24 | granite4:7b-a1b-h | ollama | **0.31** [0.156, 0.44] | 0.37 | 0.80 | 100% | 6.2 / 25.2 | 100.1 | eligible |
| 25 | gemma4:e2b | ollama | **0.20** [0.078, 0.306] | 0.30 | 0.97 | 100% | 13.4 / 61.1 | 42.5 | eligible |
| 26 | llama3.1:8b | ollama | **0.15** [0.059, 0.26] | 0.27 | 0.87 | 100% | 30.9 / 103.1 | 23.1 | eligible |
| 27 | llama3.2:3b | ollama | **0.10** [0.047, 0.149] | 0.23 | 0.90 | 100% | 20.4 / 51.0 | 42.2 | eligible |
| – | gemma3n:e2b | ollama | | | | | | | not run yet |
| – | gemma3n:e4b | ollama | | | | | | | not run yet |

### Same model, different back-ends or formats

**gemma3:4b on Ollama vs llama.cpp.** Same 4-bit Gemma 3 4B weights served by two engines, same prompt, seeds and temperature.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| gemma3:4b | ollama | `gemma3:4b` | 0.61 [0.419, 0.771] | 0.86 | 15.8 / 43.5 |
| gemma3:4b (llama.cpp) | llamacpp | `gemma-3-4b-it-Q4_K_M` | 0.56 [0.384, 0.716] | 0.84 | 29.5 / 74.9 |

**qwen3:4b on Ollama vs llama.cpp.** Qwen3 4B from the Ollama library (two tags) and the official Qwen GGUF on llama.cpp; thinking off in all. Tags can point to different builds (see the digests in results/leaderboard.json).

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:4b | ollama | `qwen3:4b` | 0.81 [0.657, 0.933] | 0.86 | 39.6 / 95.1 |
| qwen3:4b-q4_K_M | ollama | `qwen3:4b-q4_K_M` | 0.58 [0.409, 0.71] | 0.80 | 28.7 / 86.3 |
| qwen3:4b (llama.cpp) | llamacpp | `Qwen3-4B-Q4_K_M` | 0.66 [0.504, 0.794] | 0.87 | 22.9 / 73.8 |

**8B at 4 bits vs 8B at ~2 bits (ternary).** A conventional 4-bit 8B model on Ollama and a ternary 8B (Bonsai) on the PrismML fork of llama.cpp.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:8b | ollama | `qwen3:8b` | 0.44 [0.348, 0.533] | 0.88 | 23.4 / 64.0 |
| Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | `Ternary-Bonsai-8B-PQ2_0` | 0.36 [0.225, 0.49] | 0.83 | 64.5 / 170.7 |

**27B compressed to fit the runner.** Ternary-Bonsai-2-27B (5.95 GB) is a ternary version of Qwen3.8-27B, whose 4-bit build does not fit in 16 GB of RAM. Measured on a sample only (4 cases, 1 seed): calls take many minutes on 4 vCPUs.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | `Ternary-Bonsai-2-27B-PTQ1_0` | 1.00 [1.0, 1.0] | 1.00 | 2016.8 / 2493.4 |
| Qwen3.8-27B at 4 bits (qwen3.8:27b-q4_K_M, 18 GB) | | | does not fit the free runner | | |
