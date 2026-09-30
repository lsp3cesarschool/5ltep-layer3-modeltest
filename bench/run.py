"""Run one candidate over the gold set.

  python bench/run.py --entry '{"backend": "ollama", "model": "gemma3:4b", ...}'

Every case is judged with the three production seeds; the run stops early when
the time budget is spent and records how much it covered, so a slow model
(e.g. a 27B on CPU) still yields a partial, clearly labelled result.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bench import clients  # noqa: E402
from bench.common import (NUM_CTX, NUM_PREDICT, RUNS_DIR, SEEDS, TEMPERATURE, gold_hash, import_upstream,  # noqa: E402
                          load_gold, parse_answer, render, slug, upstream_ref)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry", required=True, help="candidate as JSON (from the plan)")
    ap.add_argument("--budget-minutes", type=float, default=None)
    ap.add_argument("--limit", type=int, default=None, help="only the first N cases (smoke test)")
    args = ap.parse_args(argv)
    entry = json.loads(args.entry)
    budget = args.budget_minutes or entry.get("budget_minutes", 300)

    judge, profile_mod = import_upstream()
    gold = load_gold()
    cases = gold["cases"][: args.limit] if args.limit else gold["cases"]
    client = clients.make(entry)
    started = datetime.now(timezone.utc)
    deadline = time.monotonic() + budget * 60
    answers, stopped = [], None
    # Interleave seeds per case so a partial run still covers whole cases.
    for case in cases:
        if time.monotonic() > deadline:
            stopped = "time budget"
            break
        system, prompt, schema, categories = render(case, judge, profile_mod)
        runs = []
        for seed in SEEDS:
            try:
                text, secs, tokens = client.generate(system, prompt, seed, schema, TEMPERATURE, NUM_PREDICT, NUM_CTX)
                parsed = parse_answer(text, categories)
            except requests.RequestException as exc:
                text, secs, tokens = "", None, None
                parsed = {"category": "INVALID", "confidence": 0.0, "reasoning": f"request failed: {exc}"[:500]}
            runs.append({**parsed, "seed": seed, "latency_s": None if secs is None else round(secs, 2),
                         "tokens": tokens})
        answers.append({"case": case["id"], "gold": case["gold"], "runs": runs})
        print(f"{case['id']:32s} gold={case['gold']:3s} -> {'/'.join(r['category'] for r in runs)} "
              f"({', '.join(str(r['latency_s']) for r in runs)} s)", flush=True)

    out = {
        "entry": entry,
        "key": entry["key"],
        "label": entry["label"],
        "upstream_ref": upstream_ref(),
        "gold_hash": gold_hash(),
        "cases_total": len(gold["cases"]),
        "cases_done": len(answers),
        "stopped": stopped,
        "server": client.info(),
        "started_at": started.isoformat(timespec="seconds"),
        "ended_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "answers": answers,
    }
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNS_DIR / f"{slug(entry['label'])}__{entry['key']}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(answers)}/{len(gold['cases'])} cases; saved {path}")


if __name__ == "__main__":
    main()
