"""Tests of the benchmark logic (no model server, no network)."""

import json
import random
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
