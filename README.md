# 5LTEP-L3 · Model benchmark

**Which local LLM should judge the anomalies of [5ltep-layer3](https://github.com/lsp3cesarschool/5ltep-layer3)?**
A monthly, reproducible benchmark of small open models on the production prompt, with a gold set
whose right answers are known by construction.

[![Model benchmark](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/benchmark.yml/badge.svg)](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/benchmark.yml)
[![Tests](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/tests.yml/badge.svg)](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

📌 **Current recommendation (machine-readable):**
<https://raw.githubusercontent.com/lsp3cesarschool/5ltep-layer3-modeltest/main/results/recommendation.json>

## Leaderboard

<!-- LEADERBOARD:START -->
*Updated 2026-09-30 07:43 UTC · 30 gold cases · 3 seeds each · production prompt at `5a1e733`*

**Recommendation:** qwen3:4b beats gemma3:4b by +0.310 macro-F1 (paired 95% CI [0.078, 0.535]).

| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | gemma4:12b | ollama | **0.89** [0.738, 1.0] | 0.90 | 0.97 | 100% | 106.8 / 278.1 | 7.6 | not eligible: p90 latency 278s |
| 2 | qwen3:4b | ollama | **0.81** [0.657, 0.933] | 0.83 | 0.86 | 99% | 35.8 / 91.3 | 23.7 | eligible |
| 3 | ministral-3:3b | ollama | **0.69** [0.516, 0.84] | 0.70 | 0.83 | 98% | 42.5 / 57.1 | 27.4 | eligible |
| 4 | granite4.2:8b | ollama | **0.62** [0.446, 0.764] | 0.57 | 0.79 | 42% | 101.9 / 190.8 | 9.9 | not eligible: valid answers 42%; p90 latency 191s |
| 5 | qwen3.5:9b | ollama | **0.61** [0.432, 0.771] | 0.63 | 0.83 | 100% | 35.8 / 183.1 | 14.7 | not eligible: p90 latency 183s |
| 6 | qwen3:8b | ollama | **0.59** [0.429, 0.744] | 0.63 | 0.88 | 100% | 33.3 / 140.9 | 17.9 | eligible |
| 7 | ministral-3:8b | ollama | **0.57** [0.438, 0.661] | 0.63 | 0.90 | 100% | 47.9 / 164.0 | 14.5 | not eligible: p90 latency 164s |
| 8 | granite4.2:3b | ollama | **0.56** [0.438, 0.656] | 0.63 | 0.72 | 76% | 52.9 / 87.0 | 23.8 | not eligible: valid answers 76% |
| 9 | qwen3:4b-q4_K_M | ollama | **0.53** [0.363, 0.685] | 0.57 | 0.86 | 100% | 21.5 / 58.8 | 37.0 | eligible |
| 10 | gemma3:4b | ollama | **0.50** [0.325, 0.66] | 0.53 | 0.84 | 99% | 22.2 / 63.4 | 35.2 | eligible |
| 11 | qwen3.5:4b | ollama | **0.50** [0.356, 0.65] | 0.57 | 0.86 | 100% | 23.7 / 106.2 | 24.7 | eligible |
| 12 | gemma3n:e2b | ollama | **0.48** [0.271, 0.647] | 0.47 | 0.74 | 100% | 11.8 / 42.1 | 57.3 | eligible |
| 13 | phi4-mini:3.8b | ollama | **0.48** [0.318, 0.598] | 0.53 | 0.80 | 100% | 30.8 / 65.5 | 30.2 | eligible |
| 14 | qwen3.5:2b-q4_K_M | ollama | **0.43** [0.274, 0.582] | 0.47 | 0.79 | 100% | 9.6 / 38.0 | 66.4 | eligible |
| 15 | gemma3:4b (llama.cpp) | llamacpp | **0.40** [0.217, 0.563] | 0.43 | 0.83 | 100% | 22.6 / 78.8 | 30.4 | eligible |
| 16 | qwen3:1.7b | ollama | **0.39** [0.23, 0.514] | 0.43 | 0.77 | 100% | 12.6 / 27.6 | 72.4 | eligible |
| 17 | lfm2.5:8b-a1b | ollama | **0.39** [0.261, 0.503] | 0.47 | 0.78 | 100% | 4.8 / 19.3 | 131.5 | eligible |
| 18 | gemma3:12b | ollama | **0.38** [0.308, 0.424] | 0.50 | 0.98 | 100% | 53.4 / 285.8 | 9.4 | not eligible: p90 latency 286s |
| 19 | gemma3n:e4b | ollama | **0.36** [0.216, 0.49] | 0.43 | 0.86 | 100% | 22.3 / 118.4 | 22.7 | eligible |
| 20 | qwen3.5:2b | ollama | **0.35** [0.174, 0.49] | 0.37 | 0.73 | 100% | 11.8 / 47.5 | 53.2 | eligible |
| 21 | qwen3.5:0.8b | ollama | **0.34** [0.175, 0.478] | 0.40 | 0.68 | 100% | 5.4 / 20.4 | 120.6 | eligible |
| 22 | gemma4:e2b | ollama | **0.30** [0.194, 0.386] | 0.40 | 0.96 | 100% | 13.0 / 28.6 | 68.8 | eligible |
| 23 | gemma3:4b (prompt v1) | ollama | **0.29** [0.16, 0.382] | 0.40 | 0.92 | 100% | 25.6 / 43.4 | 41.2 | not eligible: experiment |
| 24 | llama3.1:8b | ollama | **0.20** [0.076, 0.312] | 0.30 | 0.90 | 100% | 18.5 / 47.4 | 46.4 | eligible |
| 25 | granite4:7b-a1b-h | ollama | **0.16** [0.061, 0.267] | 0.27 | 0.84 | 100% | 7.5 / 35.6 | 73.7 | eligible |
| 26 | llama3.2:3b | ollama | **0.10** [0.047, 0.149] | 0.23 | 0.90 | 100% | 19.3 / 49.6 | 43.7 | eligible |
| – | Ternary-Bonsai-8B (Q2_0) | llamacpp-prism | | | | | | | not run yet |
| – | Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | | | | | | | not run yet |
<!-- LEADERBOARD:END -->

## Why a separate benchmark

Layer 3 of the 5L-TEP classifies each statistical anomaly with an LLM-as-a-Judge (categories PDC,
SP, DQE, GES). The model runs on the free GitHub Actions CPU runner, so it must be small, fast and
reliable. New small models appear every month, and the answers of a 4B model depend a lot on the
prompt (in production, one prompt revision moved 17 labels at once). Choosing the model by feel, or
by general-purpose leaderboards, is not enough: it has to be measured **on this task, with this
prompt, on this hardware**.

## How it works

```
discover ──► plan ──► run (one job per candidate, in parallel) ──► score ──► recommendation.json
 Ollama       only what changed:        gold set × 3 seeds,          macro-F1 + CI, consistency,
 library      model digest, prompt      production prompt,            validity, latency; README
 (new tags)   code or gold set          same seeds and temperature    leaderboard
```

1. **Discover** (`bench/discover.py`): lists the tags of the watched families and of the library's
   newest models, keeps plain size tags that fit the runner (1–9 GB), and records them in
   `results/discovered.json`. The curated list is in [`candidates.json`](candidates.json).
2. **Plan** (`bench/plan.py`): resolves each candidate's build (Ollama manifest digest or GGUF file
   hash) and the fingerprint of the production prompt code at the current `main` of 5ltep-layer3.
   A candidate is run again only if one of these, or the gold set, changed.
3. **Run** (`bench/run.py`): the prompt of every gold case is rendered by the **production code**
   (`src/judge.py` of 5ltep-layer3, checked out at the planned commit), then sent with the
   production seeds (11, 22, 33) and temperature (0.7) and the same JSON schema. Each candidate has a
   time budget (5 h by default); a run that does not finish is kept, marked partial.
4. **Score** (`bench/score.py`): metrics, eligibility, recommendation, this README's table.

## Gold set

[`gold/cases.json`](gold/cases.json), built by [`gold/build_gold.py`](gold/build_gold.py) from the
monthly series of IBAMA's infraction notices committed in 5ltep-layer3. Each case carries the full
evidence the judge receives (series, detector votes re-computed on the case's data, events), and a
**gold label known by construction**, following the criteria the production prompt states:

| Category | Cases | How they are built |
|---|---|---|
| SP | real | anomalies whose calendar month deviated the same way in ≥ 8 of the previous 10 years; no event within 6 months; no data-quality signs |
| PDC | synthetic | a quiet month gets a persistent ×2.5/×3 or ×0.4/×0.3 change, and the calendar gets a policy event in that month |
| DQE | synthetic | a quiet month drops to 3% of its level (reporting failure), or is multiplied by 2.2 with 45% of records without identifier and 3× cancellations (duplicated batch); no event |
| GES | synthetic | a gradual three-month ramp to ×2 or ×0.5 that persists; no event, no seasonality, no data-quality signs |

A synthetic case is kept only if the ensemble flags its month, as in production. The gold set
measures whether a model **applies the stated criteria to the evidence**; it does not measure world
knowledge, and it is not a substitute for steward-reviewed real anomalies. Steward decisions from the
main repositories can be added as further cases when there are enough of them.

## Metrics and recommendation

| Metric | Meaning |
|---|---|
| macro-F1 [95% CI] | primary score: majority label of the three seeds vs. the gold label, averaged over the four categories; bootstrap CI over cases |
| accuracy, recall per category | complementary views of the same answers |
| consistency | share of the three runs that agree with the majority (1 = always the same label) |
| valid | share of answers that parse and use a known category |
| latency p50 / p90, anomalies/h | cost on the free runner (4 vCPU, 16 GB, CPU only) |
| coverage | cases completed within the time budget |

A candidate is **eligible** with ≥ 95% valid answers, ≥ 90% coverage and p90 latency ≤ 150 s per call.
The **recommended** model is the eligible, non-experimental candidate with the highest macro-F1 (ties:
consistency, then speed). A **switch** from the production model is recommended only when the winner
beats it by at least 0.05 macro-F1 and the paired bootstrap 95% CI of the difference is above zero.

## How the main repositories use it

No tokens cross repositories. Each Layer 3 instance reads the public
[`results/recommendation.json`](results/recommendation.json) on its own schedule
(`python main.py check-model`, workflow *Model check*); when `switch_recommended` is true and the
recommended model differs from its own `LLM_MODEL`, it opens an issue in its own repository. Changing
the model remains a steward decision (repository variable `LLM_MODEL`), because every anomaly is then
judged again.

## Back-ends

| Back-end | Used for |
|---|---|
| **Ollama** | production back-end; all library models |
| **llama.cpp** (official Ubuntu x64 build) | the same GGUF as a production model, to compare engines (speed and answers) |
| **llama.cpp, PrismML fork** (built from source, cached) | ternary / 1-bit *Bonsai* models (e.g. [Ternary-Bonsai-2-27B](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf), a 27B model in 5.95 GB), whose formats are not in mainline llama.cpp or Ollama |

Hyper-compressed large models answer a real question for this setting: at the same memory, is a 27B
at ~1.75 bits/weight better than a 4B at 4 bits? On a CPU runner the price is speed (all 27B
weights are read for every token), which the latency columns and the time budget make visible.

## Adding a candidate

Add an entry to [`candidates.json`](candidates.json):

```json
{"label": "my-model:4b", "backend": "ollama", "model": "my-model:4b", "options": {"think": false}}
{"label": "Some GGUF", "backend": "llamacpp", "model": "some-gguf", "hf_repo": "org/repo-GGUF", "hf_file": "model-Q4_K_M.gguf"}
```

`"experiment": true` measures a candidate without making it eligible (e.g. an older prompt version via
`"prompt_ref"`). Run *Actions → Model benchmark → Run workflow*, optionally with `only`.

## Licences

Code: MIT. Models are downloaded at run time from their official sources and are not redistributed;
each keeps its own licence. Ollama and llama.cpp are MIT; the Bonsai models are Apache-2.0. Public
repositories run GitHub Actions on standard runners at no cost.
