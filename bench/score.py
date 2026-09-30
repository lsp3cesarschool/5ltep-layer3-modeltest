"""Score every current candidate, pick a recommendation, update the README.

Metrics per candidate (majority label of the three seeds per case):
  macro-F1 over the four categories (primary), with a bootstrap 95% CI over cases;
  accuracy and recall per category; label consistency (share of the 3 runs that
  agree with the majority); unanimous rate; valid-answer rate; latency per call
  (median and p90) and anomalies judged per hour on the runner; coverage (cases
  completed within the time budget).

Recommendation: among non-experimental candidates with valid rate, coverage
and p90 latency within the limits of candidates.json, the highest macro-F1
(ties: consistency, then speed). A switch is recommended only if that model is
not the production one, beats it by at least `switch_margin_macro_f1`, and the
paired bootstrap 95% CI of the difference is above zero: with a few dozen
cases, small differences are noise.
"""

import json
import random
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bench.common import (LEADERBOARD_FILE, RECOMMENDATION_FILE, RESULTS_DIR, ROOT, RUNS_DIR,  # noqa: E402
                          load_gold)

CATS = ["PDC", "SP", "DQE", "GES"]
REPO = "lsp3cesarschool/5ltep-layer3-modeltest"


def majority(runs: list[dict]) -> str:
    valid = [r for r in runs if r["category"] != "INVALID"]
    if not valid:
        return "INVALID"
    counts = Counter(r["category"] for r in valid)
    top = max(counts.values())
    tied = [c for c, n in counts.items() if n == top]
    return max(tied, key=lambda c: sum(r["confidence"] for r in valid if r["category"] == c))


def macro_f1(pairs: list[tuple[str, str]]) -> float:
    """Mean F1 over the categories present in the gold labels of `pairs`."""
    f1s = []
    for c in [c for c in CATS if any(g == c for g, _ in pairs)]:
        tp = sum(1 for g, p in pairs if g == c and p == c)
        fp = sum(1 for g, p in pairs if g != c and p == c)
        fn = sum(1 for g, p in pairs if g == c and p != c)
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if prec + rec else 0.0)
    return sum(f1s) / len(f1s) if f1s else 0.0


def percentile(values: list[float], q: float) -> float | None:
    v = sorted(x for x in values if x is not None)
    if not v:
        return None
    k = (len(v) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def bootstrap_ci(pairs, n, rng) -> list[float]:
    stats = sorted(macro_f1([pairs[rng.randrange(len(pairs))] for _ in pairs]) for _ in range(n))
    return [round(stats[int(0.025 * n)], 3), round(stats[int(0.975 * n) - 1], 3)]


def metrics(run: dict, n_boot: int, rng) -> dict:
    per_case = {a["case"]: a for a in run["answers"]}
    pairs = [(a["gold"], majority(a["runs"])) for a in run["answers"]]
    calls = [r for a in run["answers"] for r in a["runs"]]
    lat = [r["latency_s"] for r in calls if r["latency_s"] is not None]
    cons = []
    for a in run["answers"]:
        maj = majority(a["runs"])
        cons.append(sum(1 for r in a["runs"] if r["category"] == maj) / len(a["runs"]))
    mean_lat = sum(lat) / len(lat) if lat else None
    confusion = {g: dict(Counter(p for gg, p in pairs if gg == g)) for g in CATS}
    return {
        "coverage": round(run["cases_done"] / run["cases_total"], 3),
        "cases_done": run["cases_done"],
        "macro_f1": round(macro_f1(pairs), 3) if pairs else 0.0,
        "macro_f1_ci95": bootstrap_ci(pairs, n_boot, rng) if pairs else None,
        "accuracy": round(sum(g == p for g, p in pairs) / len(pairs), 3) if pairs else 0.0,
        "recall": {c: round(sum(1 for g, p in pairs if g == c and p == c) / max(1, sum(1 for g, _ in pairs if g == c)), 3)
                   for c in CATS},
        "consistency": round(sum(cons) / len(cons), 3) if cons else 0.0,
        "unanimous_rate": round(sum(c == 1 for c in cons) / len(cons), 3) if cons else 0.0,
        "valid_rate": round(sum(r["category"] != "INVALID" for r in calls) / len(calls), 3) if calls else 0.0,
        "latency_median_s": round(percentile(lat, 0.5), 1) if lat else None,
        "latency_p90_s": round(percentile(lat, 0.9), 1) if lat else None,
        "anomalies_per_hour": round(3600 / (3 * mean_lat), 1) if mean_lat else None,
        "confusion": confusion,
        "_pairs": {case: p for case, (_, p) in zip(per_case, pairs)},
    }


def paired_diff(a: dict, b: dict, gold: dict, n: int, rng) -> dict:
    common = [c for c in a["_pairs"] if c in b["_pairs"]]
    if not common:
        return {"diff": None}
    def f1(m, cases):
        return macro_f1([(gold[c], m["_pairs"][c]) for c in cases])
    diffs = sorted(f1(a, s) - f1(b, s) for s in ([common[rng.randrange(len(common))] for _ in common] for _ in range(n)))
    return {"diff": round(f1(a, common) - f1(b, common), 3),
            "ci95": [round(diffs[int(0.025 * n)], 3), round(diffs[int(0.975 * n) - 1], 3)]}


def main() -> None:
    plan = json.loads((RESULTS_DIR / "plan.json").read_text(encoding="utf-8"))
    sel = plan["selection"]
    gold_cases = load_gold()["cases"]
    gold = {c["id"]: c["gold"] for c in gold_cases}
    rng = random.Random(7)
    runs = {}
    for p in RUNS_DIR.glob("*.json"):
        r = json.loads(p.read_text(encoding="utf-8"))
        runs[r["key"]] = r
    rows = []
    for e in plan["entries"]:
        r = runs.get(e["key"])
        if not r:
            rows.append({"label": e["label"], "backend": e["backend"], "status": "not run yet", "entry": e})
            continue
        m = metrics(r, sel["bootstrap_resamples"], rng)
        reasons = []
        if m["valid_rate"] < sel["min_valid_rate"]:
            reasons.append(f"valid answers {m['valid_rate']:.0%}")
        if m["coverage"] < sel["min_coverage"]:
            reasons.append(f"covered {m['coverage']:.0%} of the cases in the time budget")
        if m["latency_p90_s"] is not None and m["latency_p90_s"] > sel["max_p90_latency_s"]:
            reasons.append(f"p90 latency {m['latency_p90_s']:.0f}s")
        if e.get("experiment"):
            reasons.append("experiment")
        rows.append({"label": e["label"], "backend": e["backend"], "model": e["model"], "digest": e["digest"],
                     "status": "eligible" if not reasons else "not eligible: " + "; ".join(reasons),
                     "eligible": not reasons, "tested_at": r["ended_at"], "server": r.get("server", {}),
                     "entry": e, **m})

    scored = [r for r in rows if "macro_f1" in r]
    scored.sort(key=lambda r: (-r["macro_f1"], -r["consistency"], r["latency_median_s"] or 1e9))
    prod = plan["production"]
    current = next((r for r in scored if r["backend"] == prod["backend"] and r["model"] == prod["model"]
                    and not r["entry"].get("experiment")), None)
    eligible = [r for r in scored if r["eligible"]]
    best = eligible[0] if eligible else None
    switch, reason = False, "no eligible candidate yet"
    comparison = None
    if best and current:
        if best is current:
            reason = "the production model is the best eligible candidate"
        else:
            comparison = paired_diff(best, current, gold, sel["bootstrap_resamples"], rng)
            margin_ok = comparison["diff"] is not None and comparison["diff"] >= sel["switch_margin_macro_f1"]
            ci_ok = comparison.get("ci95") and comparison["ci95"][0] > 0
            switch = bool(margin_ok and ci_ok)
            reason = (f"{best['label']} beats {current['label']} by {comparison['diff']:+.3f} macro-F1 "
                      f"(paired 95% CI {comparison['ci95']})" +
                      ("" if switch else "; not enough to recommend a switch"))
    elif best:
        reason = "the production model has no result yet"

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    public = [{k: v for k, v in r.items() if not k.startswith("_") and k != "entry"} for r in rows]
    for r in public:
        r.pop("_pairs", None)
    LEADERBOARD_FILE.write_text(json.dumps({"generated_at": now, "gold_hash": plan["gold_hash"],
                                            "gold_cases": len(gold_cases), "prompt_refs": plan["prompt_refs"],
                                            "selection": sel, "rows": public,
                                            "unavailable": plan.get("unavailable", [])}, indent=1), encoding="utf-8")

    def card(r):
        if not r:
            return None
        return {"label": r["label"], "backend": r["backend"], "model": r["model"], "digest": r["digest"],
                "options": r["entry"].get("options", {}), "macro_f1": r["macro_f1"], "macro_f1_ci95": r["macro_f1_ci95"],
                "consistency": r["consistency"], "valid_rate": r["valid_rate"],
                "latency_p90_s": r["latency_p90_s"], "anomalies_per_hour": r["anomalies_per_hour"],
                "tested_at": r["tested_at"]}
    rec = {
        "generated_at": now,
        "benchmark": f"https://github.com/{REPO}",
        "gold_cases": len(gold_cases), "gold_hash": plan["gold_hash"],
        "prompt_commit": plan["prompt_refs"].get("main", {}).get("commit"),
        "production": card(current) or prod,
        "recommended": card(best),
        "switch_recommended": switch,
        "comparison": comparison,
        "reason": reason,
    }
    RECOMMENDATION_FILE.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    write_markdown(rows, scored, rec, len(gold_cases), now)
    print(reason)


def write_markdown(rows, scored, rec, n_cases, now) -> None:
    lines = [f"*Updated {now[:16].replace('T', ' ')} UTC · {n_cases} gold cases · 3 seeds each · "
             f"production prompt at `{(rec.get('prompt_commit') or '')[:7]}`*", "",
             f"**Recommendation:** {rec['reason']}.", "",
             "| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(scored, 1):
        ci = r["macro_f1_ci95"] or ["–", "–"]
        lines.append(f"| {i} | {r['label']} | {r['backend']} | **{r['macro_f1']:.2f}** [{ci[0]}, {ci[1]}] | "
                     f"{r['accuracy']:.2f} | {r['consistency']:.2f} | {r['valid_rate']:.0%} | "
                     f"{r['latency_median_s']} / {r['latency_p90_s']} | {r['anomalies_per_hour']} | {r['status']} |")
    for r in rows:
        if "macro_f1" not in r:
            lines.append(f"| – | {r['label']} | {r['backend']} | | | | | | | {r['status']} |")
    table = "\n".join(lines)
    (RESULTS_DIR / "leaderboard.md").write_text(table + "\n", encoding="utf-8")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    new = re.sub(r"(<!-- LEADERBOARD:START -->)(.*?)(<!-- LEADERBOARD:END -->)",
                 lambda m: f"{m.group(1)}\n{table}\n{m.group(3)}", text, flags=re.S)
    readme.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
