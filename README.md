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
*No results yet: the first benchmark run fills this table.*
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
