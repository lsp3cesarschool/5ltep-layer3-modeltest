"""Score every current candidate, pick a recommendation, update README.md and LEIAME.md.

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
from bench.common import (CANDIDATES_FILE, LEADERBOARD_FILE, RECOMMENDATION_FILE, RESULTS_DIR, ROOT,  # noqa: E402
                          RUNS_DIR, load_gold)

CATS = ["PDC", "SP", "DQE", "GES"]
REPO = "lsp3cesarschool/5ltep-layer3-modeltest"

# The leaderboard is written into README.md (English) and LEIAME.md (Portuguese).
DOCS = {"en": "README.md", "pt": "LEIAME.md"}
TEXT = {
    "en": {
        "updated": "*Updated {when} UTC · {n} gold cases · 3 seeds each · production prompt at `{commit}`*",
        "recommendation": "**Recommendation:** {reason}.",
        "header": "| # | Model | Backend | macro-F1 [95% CI] | Acc. | Consist. | Valid | Latency p50 / p90 (s) | Anomalies/h | Status |",
        "comparisons": "### Same model, different back-ends or formats",
        "cmp_header": "| Candidate | Back-end | Model file / tag | macro-F1 [95% CI] | Consist. | Latency p50 / p90 (s) |",
        "not_measured": "not measured yet", "unrunnable": "does not fit the free runner",
        "not_run": "not run yet", "eligible": "eligible", "not_eligible": "not eligible: ",
        "valid": "valid answers {:.0%}", "coverage": "covered {:.0%} of the cases in the time budget",
        "latency": "p90 latency {:.0f}s", "experiment": "experiment",
        "no_eligible": "no eligible candidate yet",
        "prod_is_best": "the production model is the best eligible candidate",
        "prod_no_result": "the production model has no result yet",
        "beats": "{best} beats {current} by {diff} macro-F1 (paired 95% CI {ci})",
        "not_enough": "; not enough to recommend a switch",
    },
    "pt": {
        "updated": "*Atualizado em {when} UTC · {n} casos do gabarito · 3 sementes cada · prompt de produção em `{commit}`*",
        "recommendation": "**Recomendação:** {reason}.",
        "header": "| # | Modelo | Motor | macro-F1 [IC 95%] | Acurácia | Consist. | Válidas | Latência p50 / p90 (s) | Anomalias/h | Situação |",
        "comparisons": "### Mesmo modelo, motores ou formatos diferentes",
        "cmp_header": "| Candidato | Motor | Arquivo / tag do modelo | macro-F1 [IC 95%] | Consist. | Latência p50 / p90 (s) |",
        "not_measured": "ainda não medido", "unrunnable": "não cabe no runner gratuito",
        "not_run": "ainda não executado", "eligible": "elegível", "not_eligible": "não elegível: ",
        "valid": "respostas válidas {:.0%}", "coverage": "cobriu {:.0%} dos casos no tempo disponível",
        "latency": "latência p90 de {:.0f} s", "experiment": "experimento",
        "no_eligible": "nenhum candidato elegível ainda",
        "prod_is_best": "o modelo de produção é o melhor candidato elegível",
        "prod_no_result": "o modelo de produção ainda não tem resultado",
        "beats": "{best} supera {current} por {diff} de macro-F1 (IC 95% pareado {ci})",
        "not_enough": "; não é suficiente para recomendar a troca",
    },
}


def num(x, lang: str, spec: str = "") -> str:
    """A number in the document's convention (decimal comma in Portuguese)."""
    s = format(x, spec) if spec else str(x)
    return s.replace(".", ",") if lang == "pt" else s


def interval(ci, lang: str) -> str:
    ci = ci or ["–", "–"]
    return f"[{num(ci[0], lang)}; {num(ci[1], lang)}]" if lang == "pt" else f"[{ci[0]}, {ci[1]}]"


def status_text(r: dict, lang: str) -> str:
    t = TEXT[lang]
    if "macro_f1" not in r:
        return t["not_run"]
    reasons = r.get("_reasons", [])
    if not reasons:
        return t["eligible"]
    parts = [t[code] if value is None else num(t[code].format(value), lang) for code, value in reasons]
    return t["not_eligible"] + "; ".join(parts)


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
            reasons.append(("valid", m["valid_rate"]))
        if m["coverage"] < sel["min_coverage"]:
            reasons.append(("coverage", m["coverage"]))
        if m["latency_p90_s"] is not None and m["latency_p90_s"] > sel["max_p90_latency_s"]:
            reasons.append(("latency", m["latency_p90_s"]))
        if e.get("experiment"):
            reasons.append(("experiment", None))
        row = {"label": e["label"], "backend": e["backend"], "model": e["model"], "digest": e["digest"],
               "eligible": not reasons, "_reasons": reasons, "tested_at": r["ended_at"],
               "server": r.get("server", {}), "entry": e, **m}
        row["status"] = status_text(row, "en")
        rows.append(row)

    scored = [r for r in rows if "macro_f1" in r]
    scored.sort(key=lambda r: (-r["macro_f1"], -r["consistency"], r["latency_median_s"] or 1e9))
    prod = plan["production"]
    current = next((r for r in scored if r["backend"] == prod["backend"] and r["model"] == prod["model"]
                    and not r["entry"].get("experiment")), None)
    eligible = [r for r in scored if r["eligible"]]
    best = eligible[0] if eligible else None
    switch, reasons = False, {lang: TEXT[lang]["no_eligible"] for lang in TEXT}
    comparison = None
    if best and current:
        if best is current:
            reasons = {lang: TEXT[lang]["prod_is_best"] for lang in TEXT}
        else:
            comparison = paired_diff(best, current, gold, sel["bootstrap_resamples"], rng)
            margin_ok = comparison["diff"] is not None and comparison["diff"] >= sel["switch_margin_macro_f1"]
            ci_ok = comparison.get("ci95") and comparison["ci95"][0] > 0
            switch = bool(margin_ok and ci_ok)
            reasons = {lang: TEXT[lang]["beats"].format(best=best["label"], current=current["label"],
                                                       diff=num(comparison["diff"], lang, "+.3f"),
                                                       ci=interval(comparison["ci95"], lang)) +
                       ("" if switch else TEXT[lang]["not_enough"]) for lang in TEXT}
    elif best:
        reasons = {lang: TEXT[lang]["prod_no_result"] for lang in TEXT}
    reason = reasons["en"]

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
    use = card(best) if switch else (card(current) or prod)
    rec = {
        "generated_at": now,
        "benchmark": f"https://github.com/{REPO}",
        "gold_cases": len(gold_cases), "gold_hash": plan["gold_hash"],
        "prompt_commit": plan["prompt_refs"].get("main", {}).get("commit"),
        # "use" is what Layer 3 instances with LLM_MODEL=auto run: the production model,
        # replaced only when a switch is recommended.
        "use": use,
        "production": card(current) or prod,
        "recommended": card(best),
        "switch_recommended": switch,
        "comparison": comparison,
        "reason": reason,
    }
    RECOMMENDATION_FILE.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    if switch:
        adopt(best, now)
    comparisons = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8")).get("comparisons", [])
    write_markdown(rows, scored, rec, len(gold_cases), now, comparisons, reasons)
    print(reason)


def adopt(best: dict, now: str) -> None:
    """A recommended switch becomes the new production reference of the benchmark itself,
    so the next months compare candidates against the model instances actually use."""
    cfg = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))
    previous = cfg["production"].get("model")
    if previous == best["model"] and cfg["production"].get("backend") == best["backend"]:
        return
    cfg["production"] = {"backend": best["backend"], "model": best["model"],
                         "options": best["entry"].get("options", {}), "since": now[:10], "previous": previous}
    CANDIDATES_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def comparison_tables(scored: list[dict], comparisons: list[dict], lang: str = "en") -> list[str]:
    """One small table per group of candidates that differ only in back-end or format.
    Groups may carry `title_pt` / `note_pt` / `unrunnable_pt` for the Portuguese document."""
    t = TEXT[lang]
    by_label = {r["label"]: r for r in scored}
    out = []
    for g in comparisons:
        title = g.get(f"title_{lang}", g["title"]) if lang != "en" else g["title"]
        note = g.get(f"note_{lang}", g.get("note", "")) if lang != "en" else g.get("note", "")
        out += ["", f"**{title}.** {note}", "", t["cmp_header"], "|---|---|---|---|---|---|"]
        for label in g["labels"]:
            r = by_label.get(label)
            if r:
                out.append(f"| {label} | {r['backend']} | `{r['model']}` | {num(r['macro_f1'], lang, '.2f')} "
                           f"{interval(r['macro_f1_ci95'], lang)} | {num(r['consistency'], lang, '.2f')} | "
                           f"{num(r['latency_median_s'], lang)} / {num(r['latency_p90_s'], lang)} |")
            else:
                out.append(f"| {label} | | | {t['not_measured']} | | |")
        if g.get("unrunnable"):
            model = g.get(f"unrunnable_{lang}", g["unrunnable"]) if lang != "en" else g["unrunnable"]
            out.append(f"| {model} | | | {t['unrunnable']} | | |")
    return out


def leaderboard(rows, scored, rec, n_cases, now, comparisons, reason: str, lang: str) -> str:
    t = TEXT[lang]
    lines = [t["updated"].format(when=now[:16].replace("T", " "), n=n_cases,
                                 commit=(rec.get("prompt_commit") or "")[:7]), "",
             t["recommendation"].format(reason=reason), "",
             t["header"], "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(scored, 1):
        lines.append(f"| {i} | {r['label']} | {r['backend']} | **{num(r['macro_f1'], lang, '.2f')}** "
                     f"{interval(r['macro_f1_ci95'], lang)} | {num(r['accuracy'], lang, '.2f')} | "
                     f"{num(r['consistency'], lang, '.2f')} | {r['valid_rate']:.0%} | "
                     f"{num(r['latency_median_s'], lang)} / {num(r['latency_p90_s'], lang)} | "
                     f"{num(r['anomalies_per_hour'], lang)} | {status_text(r, lang)} |")
    for r in rows:
        if "macro_f1" not in r:
            lines.append(f"| – | {r['label']} | {r['backend']} | | | | | | | {status_text(r, lang)} |")
    if comparisons:
        lines += ["", t["comparisons"]] + comparison_tables(scored, comparisons, lang)
    return "\n".join(lines)


def write_markdown(rows, scored, rec, n_cases, now, comparisons=(), reasons=None) -> None:
    """Fill the leaderboard markers of README.md and LEIAME.md (each in its language);
    results/leaderboard.md keeps the English table."""
    reasons = reasons or {"en": rec["reason"]}
    for lang, name in DOCS.items():
        doc = ROOT / name
        if not doc.exists():
            continue
        table = leaderboard(rows, scored, rec, n_cases, now, comparisons, reasons.get(lang, rec["reason"]), lang)
        if lang == "en":
            (RESULTS_DIR / "leaderboard.md").write_text(table + "\n", encoding="utf-8")
        text = doc.read_text(encoding="utf-8")
        new = re.sub(r"(<!-- LEADERBOARD:START -->)(.*?)(<!-- LEADERBOARD:END -->)",
                     lambda m: f"{m.group(1)}\n{table}\n{m.group(3)}", text, flags=re.S)
        doc.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
