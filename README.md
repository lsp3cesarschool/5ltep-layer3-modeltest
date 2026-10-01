# 5LTEP-L3 · Model benchmark

[![Recommended model](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Flsp3cesarschool%2F5ltep-layer3-modeltest%2Fmain%2Fresults%2Fstatus.json)](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/benchmark.yml) [![Tests](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/tests.yml/badge.svg)](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/tests.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**English** · [Português](LEIAME.md)

**Which local LLM should judge the anomalies of [5ltep-layer3](https://github.com/lsp3cesarschool/5ltep-layer3)?**
A monthly, reproducible benchmark of small open models on the production prompt, with a gold set
whose right answers are known by construction.

| Resource | What you find there |
|---|---|
| 🏆 **Leaderboard** | [below](#leaderboard), updated by every run |
| 📌 **Current recommendation** | [recommendation.json](https://raw.githubusercontent.com/lsp3cesarschool/5ltep-layer3-modeltest/main/results/recommendation.json): machine-readable, read by every Layer 3 instance |
| 🏛️ **Instances that use it** | [5ltep-layer3](https://github.com/lsp3cesarschool/5ltep-layer3) (IBAMA) and [5ltep-layer3-aneel](https://github.com/lsp3cesarschool/5ltep-layer3-aneel) (ANEEL, control case) |
| 🔒 **Security** | [SECURITY.md](SECURITY.md): what is not trusted (the model, the data portal, web sources), how the toolkit contains it, and how to report a vulnerability |

## What the models are asked to do

Layer 3 of the 5L-TEP (Five-Layer Trust Engineering Pyramid) watches monthly series built from open
government data (e.g. the number of IBAMA infraction notices per month) and flags **anomalies**:
months that depart from the usual pattern. A statistical ensemble finds them; an **LLM-as-a-Judge**
then reads each anomaly with its context (the same month in previous years, known events such as new
laws, signs in the records themselves) and says which of four causes explains it best:

| Code | Category | Example | Why it matters |
|---|---|---|---|
| **PDC** | Policy-Driven Change | notices drop right after a new decree changes the sanctioning procedure | explained by a known event: document it, no correction needed |
| **SP** | Seasonal Pattern | January has fewer notices almost every year (holidays, budget cycle) | expected behaviour: no action |
| **DQE** | Data-Quality Event | a month with almost no records in an active series, or a burst of records without identifier | a **data problem**: always sent to a human steward, first in line for correction |
| **GES** | Genuine Enforcement Shift | a gradual, lasting increase with no event, no seasonality and no data signs | a real change nobody has explained yet: worth investigating |

The point of Layer 3 is to tell people **where to look first**: the anomalies that nothing explains,
and above all those that look like data problems. A good judge must therefore apply these criteria
consistently. That is what this benchmark measures, for every candidate model, on the free hardware
the pipeline actually runs on.

## Leaderboard

<!-- LEADERBOARD:START -->
*Updated 2026-10-01 18:30 UTC · 30 gold cases · 3 seeds each · production prompt at `1554bc4`*

**Recommendation:** the production model is the best eligible candidate.

| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | **1.00** [1.0, 1.0] | 1.00 | 1.00 | 100% | 1875.6 / 2308.1 | 0.6 | not eligible: covered 13% of the cases in the time budget; p90 latency 2308s; experiment |
| 2 | gemma4:12b | ollama | **0.93** [0.808, 1.0] | 0.93 | 0.99 | 100% | 79.0 / 307.7 | 8.0 | not eligible: p90 latency 308s |
| 3 | qwen3:4b | ollama | **0.81** [0.657, 0.933] | 0.83 | 0.86 | 99% | 33.8 / 92.6 | 24.0 | eligible |
| 4 | qwen3.5:9b | ollama | **0.79** [0.631, 0.928] | 0.80 | 0.88 | 100% | 52.5 / 98.3 | 19.0 | eligible |
| 5 | ministral-3:3b | ollama | **0.67** [0.497, 0.815] | 0.70 | 0.83 | 100% | 26.4 / 53.3 | 37.7 | eligible |
| 6 | qwen3:4b (llama.cpp) | llamacpp | **0.66** [0.504, 0.794] | 0.70 | 0.87 | 100% | 21.2 / 72.5 | 32.6 | eligible |
| 7 | granite4.2:8b | ollama | **0.62** [0.446, 0.764] | 0.57 | 0.79 | 42% | 92.6 / 183.0 | 10.5 | not eligible: valid answers 42%; p90 latency 183s |
| 8 | qwen3:8b | ollama | **0.59** [0.426, 0.744] | 0.63 | 0.88 | 100% | 38.7 / 139.8 | 17.2 | eligible |
| 9 | qwen3:4b-q4_K_M | ollama | **0.58** [0.419, 0.715] | 0.60 | 0.80 | 100% | 23.5 / 82.4 | 28.5 | eligible |
| 10 | ministral-3:8b | ollama | **0.57** [0.438, 0.661] | 0.63 | 0.90 | 100% | 50.5 / 165.1 | 14.1 | not eligible: p90 latency 165s |
| 11 | gemma3n:e2b | ollama | **0.54** [0.349, 0.7] | 0.53 | 0.70 | 100% | 14.5 / 61.8 | 41.1 | eligible |
| 12 | granite4.2:3b | ollama | **0.53** [0.408, 0.638] | 0.60 | 0.68 | 70% | 25.4 / 38.6 | 51.5 | not eligible: valid answers 70% |
| 13 | gemma3:4b | ollama | **0.50** [0.325, 0.66] | 0.53 | 0.84 | 99% | 15.2 / 40.6 | 53.8 | eligible |
| 14 | qwen3.5:4b | ollama | **0.50** [0.356, 0.65] | 0.57 | 0.86 | 100% | 25.7 / 107.7 | 23.9 | eligible |
| 15 | qwen3.5:2b-q4_K_M | ollama | **0.43** [0.275, 0.592] | 0.47 | 0.79 | 100% | 9.4 / 37.7 | 67.1 | eligible |
| 16 | gemma3:4b (llama.cpp) | llamacpp | **0.40** [0.217, 0.563] | 0.43 | 0.83 | 100% | 25.1 / 81.6 | 28.2 | eligible |
| 17 | qwen3:1.7b | ollama | **0.39** [0.23, 0.519] | 0.43 | 0.77 | 100% | 13.5 / 28.6 | 69.0 | eligible |
| 18 | lfm2.5:8b-a1b | ollama | **0.39** [0.261, 0.503] | 0.47 | 0.78 | 100% | 5.7 / 25.8 | 101.3 | eligible |
| 19 | gemma3n:e4b | ollama | **0.36** [0.184, 0.522] | 0.33 | 0.50 | 39% | 74.8 / 120.8 | 18.2 | not eligible: valid answers 39% |
| 20 | gemma3:12b | ollama | **0.35** [0.274, 0.417] | 0.47 | 0.98 | 100% | 50.0 / 188.1 | 12.8 | not eligible: p90 latency 188s |
| 21 | qwen3.5:2b | ollama | **0.35** [0.181, 0.496] | 0.37 | 0.73 | 100% | 12.2 / 47.3 | 52.6 | eligible |
| 22 | qwen3.5:0.8b | ollama | **0.34** [0.171, 0.477] | 0.40 | 0.68 | 100% | 5.3 / 20.4 | 120.6 | eligible |
| 23 | Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | **0.34** [0.192, 0.458] | 0.40 | 0.77 | 100% | 38.9 / 121.9 | 19.0 | eligible |
| 24 | phi4-mini:3.8b | ollama | **0.30** [0.16, 0.437] | 0.37 | 0.73 | 100% | 18.8 / 61.7 | 38.9 | eligible |
| 25 | gemma3:4b (prompt v1) | ollama | **0.29** [0.159, 0.38] | 0.40 | 0.92 | 100% | 25.6 / 43.4 | 41.2 | not eligible: experiment |
| 26 | llama3.1:8b | ollama | **0.20** [0.076, 0.312] | 0.30 | 0.90 | 100% | 25.6 / 72.6 | 31.4 | eligible |
| 27 | gemma4:e2b | ollama | **0.20** [0.078, 0.306] | 0.30 | 0.97 | 100% | 13.4 / 60.8 | 42.5 | eligible |
| 28 | granite4:7b-a1b-h | ollama | **0.16** [0.061, 0.267] | 0.27 | 0.84 | 100% | 7.7 / 36.2 | 72.5 | eligible |
| 29 | llama3.2:3b | ollama | **0.10** [0.047, 0.149] | 0.23 | 0.90 | 100% | 19.5 / 50.7 | 42.9 | eligible |

### Same model, different back-ends or formats

**gemma3:4b on Ollama vs llama.cpp.** Same 4-bit Gemma 3 4B weights served by two engines, same prompt, seeds and temperature.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| gemma3:4b | ollama | `gemma3:4b` | 0.50 [0.325, 0.66] | 0.84 | 15.2 / 40.6 |
| gemma3:4b (llama.cpp) | llamacpp | `gemma-3-4b-it-Q4_K_M` | 0.40 [0.217, 0.563] | 0.83 | 25.1 / 81.6 |

**qwen3:4b on Ollama vs llama.cpp.** Qwen3 4B from the Ollama library (two tags) and the official Qwen GGUF on llama.cpp; thinking off in all. Tags can point to different builds (see the digests in results/leaderboard.json).

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:4b | ollama | `qwen3:4b` | 0.81 [0.657, 0.933] | 0.86 | 33.8 / 92.6 |
| qwen3:4b-q4_K_M | ollama | `qwen3:4b-q4_K_M` | 0.58 [0.419, 0.715] | 0.80 | 23.5 / 82.4 |
| qwen3:4b (llama.cpp) | llamacpp | `Qwen3-4B-Q4_K_M` | 0.66 [0.504, 0.794] | 0.87 | 21.2 / 72.5 |

**8B at 4 bits vs 8B at ~2 bits (ternary).** A conventional 4-bit 8B model on Ollama and a ternary 8B (Bonsai) on the PrismML fork of llama.cpp.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:8b | ollama | `qwen3:8b` | 0.59 [0.426, 0.744] | 0.88 | 38.7 / 139.8 |
| Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | `Ternary-Bonsai-8B-PQ2_0` | 0.34 [0.192, 0.458] | 0.77 | 38.9 / 121.9 |

**27B compressed to fit the runner.** Ternary-Bonsai-2-27B (5.95 GB) is a ternary version of Qwen3.8-27B, whose 4-bit build does not fit in 16 GB of RAM. Measured on a sample only (4 cases, 1 seed): calls take many minutes on 4 vCPUs.

| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |
|---|---|---|---|---|---|
| Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | `Ternary-Bonsai-2-27B-PTQ1_0` | 1.00 [1.0, 1.0] | 1.00 | 1875.6 / 2308.1 |
| Qwen3.8-27B at 4 bits (qwen3.8:27b-q4_K_M, 18 GB) | | | does not fit the free runner | | |
<!-- LEADERBOARD:END -->

**How to read the table.** Each row is one candidate, run on all gold cases with three seeds.
**#** is the rank by macro-F1. **Model** is the Ollama tag or the GGUF file tested; **Backend** is the
inference engine (`ollama`, `llamacpp` for the official llama.cpp build, `llamacpp-prism` for the
PrismML fork that runs the ternary Bonsai models). **macro-F1 [95% CI]** is the main score: for each
case, the label chosen by the majority of the three runs is compared with the gold label, an F1 is
computed per category (PDC, SP, DQE, GES) and the four are averaged, so every category weighs the same;
the brackets give the 95% bootstrap confidence interval over cases (overlapping intervals mean the
difference may be noise). **Acc.** is the plain share of cases labelled correctly. **Consist.** is the
share of the three runs that agree with the majority (1.00 = always the same answer). **Valid** is the
share of answers that are well-formed JSON with a known category. **Latency p50 / p90** is the median
and 90th-percentile time of one call on the free runner, in seconds, and **Anomalies/h** the number of
anomalies (three calls each) judged per hour at the mean latency. **Status** tells whether the
candidate can be recommended (valid ≥ 95%, coverage ≥ 90% of the cases within the time budget, p90
latency ≤ 150 s, not an experiment) or why not.

## Why a separate benchmark

Layer 3 classifies each statistical anomaly with an LLM-as-a-Judge (categories PDC, SP, DQE, GES,
[above](#what-the-models-are-asked-to-do)). The model runs on the free GitHub Actions CPU runner, so it must be small, fast and
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
4. **Score** (`bench/score.py`): metrics, eligibility, recommendation, the table of this README and
   of its Portuguese version, `LEIAME.md`.

## Gold set

[`gold/cases.json`](gold/cases.json), built by [`gold/build_gold.py`](gold/build_gold.py) from the
monthly series of IBAMA's infraction notices committed in 5ltep-layer3. Each case carries the full
evidence the judge receives (series, detector votes re-computed on the case's data, events), and a
**gold label known by construction**, following the criteria the production prompt states:

| Category | Cases | How they are built |
|---|---|---|
| SP | real | anomalies whose calendar month deviated the same way in ≥ 8 of the previous 10 years; no event within 6 months; no data-quality signs |
| PDC | synthetic | a quiet month gets a persistent change (×2.5 to ×4, or ×0.4 to ×0.25), and the calendar gets a policy event in that month |
| DQE | synthetic | a quiet month drops to 3% of its level (reporting failure), or is multiplied by 2.2 to 4 with 45% of records without identifier and 3× cancellations (duplicated batch); no event |
| GES | synthetic | a gradual three-month ramp (to ×2 to ×3, or ×0.5 to ×0.33) that persists; no event, no seasonality, no data-quality signs |

Current set: 30 cases (7 SP, 8 PDC, 8 DQE, 7 GES). A synthetic case is kept only if the ensemble flags
its month, as in production; stronger variants are tried only when no quiet month is flagged at the
weaker one, and a category keeps fewer cases rather than repeating one (gradual ramps are rarely
flagged, hence 7 GES). The gold set
measures whether a model **applies the stated criteria to the evidence**; it does not measure world
knowledge, and it is not a substitute for steward-reviewed real anomalies. If stewards record
decisions in the main repositories, those decisions can be added as further cases, real ones, from
more than one portal.

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
When that happens, the winner becomes the benchmark's new production reference (`production` in
[`candidates.json`](candidates.json)), so later months compare candidates against the model the
instances actually use.

## How the main repositories use it

No tokens cross repositories: each Layer 3 instance reads the public
[`results/recommendation.json`](results/recommendation.json). Its field **`use`** is the model approved
for production (the previous one, until a switch is recommended).

- **Automatic (default):** with `LLM_MODEL=auto`, every run of an instance starts by reading `use` and
  judges with that model and its options (e.g. thinking off). The approval happens here, under the
  statistical rule above.
- **Pinned:** with `LLM_MODEL` set to a tag, the instance keeps that model; its monthly *Model check*
  opens an issue when this benchmark recommends another one.

In both cases, **earlier judgments are kept**: each one records the model and prompt version that
produced it, and a new model only judges anomalies that are new or whose data changed. Re-judging the
history with the current model is a separate, explicit choice (the `rejudge` input of the instance's
Layer 3 workflow).

## Back-ends

| Back-end | Used for |
|---|---|
| **Ollama** | production back-end; all library models |
| **llama.cpp** (official Ubuntu x64 build) | the same model as on Ollama, to compare engines (speed and answers): gemma3:4b and qwen3:4b |
| **llama.cpp, PrismML fork** (built from source, cached) | ternary / 1-bit *Bonsai* models (e.g. [Ternary-Bonsai-2-27B](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf), a 27B model in 5.95 GB), whose formats are not in mainline llama.cpp or Ollama |

The leaderboard ranks every candidate; the **"Same model, different back-ends or formats"** tables
under it put side by side the candidates that differ only in engine or compression, as declared in
`comparisons` in [`candidates.json`](candidates.json). First findings (30/09/2026): the same Gemma 3 4B
weights scored 0.50 on Ollama and 0.40 on llama.cpp at the same speed, with overlapping intervals, so
there is no reason to leave Ollama.

**Run-to-run variation.** Answers are not repeatable even on the same engine: a change in the production code (not in the prompt
text) forced a second run of every candidate on the same day, and with the same model digest, Ollama
version (0.35.0)
and seeds, no answer of `qwen3:4b` or `gemma3:4b` was identical (0 of 90 each), the majority label
matched in only 23 and 22 of the 30 cases, and macro-F1 moved from 0.81 to 0.75 (`qwen3:4b`) and from
0.50 to 0.52 (`gemma3:4b`). The bootstrap interval covers the choice of cases, not this variation, so
differences smaller than about 0.05–0.10 between two models, or between two runs, should be read as
noise. The switch rule (margin ≥ 0.05 and paired interval above zero) guards against part of it.

Hyper-compressed large models answer a real question for this setting: at the same memory, is a 27B
at ~1.75 bits/weight better than a 4B at 4 bits? On a CPU runner the price is speed: every token reads
all 27B weights. In the first run, Ternary-Bonsai-2-27B loaded on the 16 GB runner but no call finished
within 15 minutes, so it is now measured on a small sample only, as an experiment.

## Cost: free, but slow

**Free.** Everything here runs on GitHub's standard hosted runners of a **public** repository, which
GitHub does not charge for: *"GitHub Actions usage is free for self-hosted runners and for public
repositories that use standard GitHub-hosted runners"* ([About billing for GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions)),
and *"Use of the standard GitHub-hosted runners is free and unlimited on public repositories"*, on a
Linux runner with 4 CPUs and 16 GB of RAM ([GitHub-hosted runners reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)).
No GPU, no API key, no paid service.

**Slow.** The models run on those CPUs: tens of seconds to minutes per call. The *Anomalies/h* column
of the [leaderboard](#leaderboard), updated by every run, shows how many anomalies (three calls each)
each model judges per hour on this runner: a few dozen for the small models, much less for the large
ones.

**Why slow is a good fit for this project.** Layer 3 watches *monthly* series: the data are evaluated
month by month, so there is something new to judge only once a month, and usually only a handful of
anomalies at that. Even the first run over IBAMA's whole history (44 anomalies since 1980, 132 calls,
in September 2026) took about an hour and a half of judging, in two batches. And the deadline is generous: the next
month's data arrive only a month later, so a run could take the whole month and still be on time.
Batches chain on their own (each job is limited to 6 hours), so the runner's speed never blocks a
result; it only spends part of a window that is much larger than needed. For this use case, a free,
CPU-only runner is not a compromise but the right size: no cost, and capacity to spare.

**This benchmark** follows the same logic. It runs once a month (day 20), before the main
repositories' model check (day 22) and their next monthly run (day 5). Each candidate is a separate
job, with up to 20 running at once, so even a full run of every candidate takes only a few hours.

**Limits that shape the design.** Each job can run for up to 6 hours, and up to 20 jobs run at once
([Actions limits](https://docs.github.com/en/actions/reference/limits)); hence the time budget per
candidate, the sampling of very slow models (the 27B Bonsai needs tens of minutes per call) and the
parallel jobs. Installing Ollama or llama.cpp in the runner is ordinary use of the runner; the model
weights are downloaded from their official sources at run time.

## Adding a candidate

Add an entry to [`candidates.json`](candidates.json):

```json
{"label": "my-model:4b", "backend": "ollama", "model": "my-model:4b", "options": {"think": false}}
{"label": "Some GGUF", "backend": "llamacpp", "model": "some-gguf", "hf_repo": "org/repo-GGUF", "hf_file": "model-Q4_K_M.gguf"}
```

`"experiment": true` measures a candidate without making it eligible (e.g. an older prompt version via
`"prompt_ref"`). For comparison groups, `title_pt`, `note_pt` and `unrunnable_pt` give the text of
LEIAME.md. Run *Actions → Model benchmark → Run workflow*, optionally with `only`.

## Licences

Code: MIT. Models are downloaded at run time from their official sources and are not redistributed;
each keeps its own licence. Ollama and llama.cpp are MIT; the Bonsai models are Apache-2.0.
