"""Build the gold set: anomaly cases whose correct category is known by construction.

The cases follow the criteria that the production prompt itself states, so a
model is scored on applying them, not on guessing an annotator's opinion:

  SP   real IBAMA anomalies whose calendar month deviated in the same direction
       in at least 8 of the previous 10 years, with no event within +-6 months
       and no unusual cancellations or records without identifier.
  PDC  a calm month of the real series gets a persistent level change, and the
       event calendar gets a policy event in that month whose content explains it.
  DQE  a calm month nearly empties in an active series (reporting failure), or
       gets a burst of duplicated records without an identifier; no event.
  GES  a gradual three-month ramp that persists, with no event, no seasonality
       and no data-quality signs.

Calm month: nothing flagged by the ensemble within +-6 months, no event within
+-6 months (the window of events the prompt shows), a calendar month without a
seasonal pattern (median same-month ratio between 0.8 and 1.2), from 1998 on (after the 1996 change of
level) and at least 12 months before the end of the series.

Detectors are re-run on every modified series so that the evidence (votes,
scores, Page-Hinkley) is what production would show. Requires the upstream
checkout with PyTorch installed:

  UPSTREAM=../public python gold/build_gold.py
"""

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bench.common import GOLD_FILE, PROFILE_ID, import_upstream, upstream_path, upstream_ref  # noqa: E402

PER_CATEGORY = 8
SEED = 2026
POLICY_EVENTS = [
    "New federal decree changes the administrative procedure for issuing and recording infraction notices",
    "New law changes the rules and minimum values of environmental fines",
    "Agency restructuring moves inspection teams and changes enforcement priorities",
    "New normative instruction changes which conducts are sanctioned with infraction notices",
]


def det_row_dict(det: pd.DataFrame, series: str, month) -> dict:
    row = det[(det.index == month) & (det["series"] == series)].iloc[0]
    keep = ["value", "votes", "ensemble_score", "near_drift", "anomaly"] + \
           [c for c in det.columns if c.endswith("_vote") or c.endswith("_score")]
    out = {}
    for k in keep:
        v = row[k]
        out[k] = bool(v) if isinstance(v, (bool, np.bool_)) else (float(v) if isinstance(v, (float, np.floating)) else
                                                                  int(v) if isinstance(v, (int, np.integer)) else v)
    return out


def flagged_months(det: pd.DataFrame) -> dict:
    fl = det[det["anomaly"]]
    return {"by_month": {m: list(fl[fl.index == m]["series"]) for m in fl.index.unique()}, "df": fl}


def make_case(cid, category, construction, series, month, monthly, det, events, judge_mod):
    fl = det[det["anomaly"]]
    others = [s for s in fl[fl.index == month]["series"] if s != series]
    same = [str(m) for m in fl[fl["series"] == series].index if m.month == month.month]
    frame = monthly.reset_index()
    frame["month"] = frame["month"].astype(str)
    return {
        "id": cid, "gold": category, "construction": construction, "series": series, "month": str(month),
        "det_row": det_row_dict(det, series, month), "other_flagged": others, "same_month_flagged": same,
        "events": events, "monthly": json.loads(frame.to_json(orient="records", double_precision=10)),
    }


def main() -> None:
    judge, profile_mod = import_upstream()
    aggregate = __import__("src.aggregate", fromlist=["x"])
    detectors = __import__("src.detectors", fromlist=["x"])
    prof = profile_mod.load(str(upstream_path() / "profiles" / f"{PROFILE_ID}.json"))
    base = aggregate.load_series(upstream_path() / "data" / PROFILE_ID / "monthly_series.csv").astype(float)
    events = [e for e in prof.events(include_suggested=False)]
    series_names = list(prof.series)
    rng = random.Random(SEED)
    det, _ = detectors.detect_all(base, series_names)
    cases = []

    # --- SP: real anomalies with a strong seasonal signature ------------------------------
    fl = det[det["anomaly"]]
    sp = []
    for month, row in fl.iterrows():
        s = row["series"]
        col = base[s]
        hist = judge.same_month_history(col, month)
        ratio = judge.trailing_ratio(col).loc[month]
        same_dir = sum(1 for _, r in hist if (r < 1) == (ratio < 1))
        near_event = any(abs((pd.Period(e["month"], freq="M") - month).n) <= 6 for e in events)
        ctx = base.loc[month]
        prev = base[(base.index >= month - 12) & (base.index < month)]
        signs = ctx["missing_key"] > 2 * max(prev["missing_key"].median(), 1) or \
            ctx["excluded"] > 2 * max(prev["excluded"].median(), 1)
        if len(hist) == 10 and same_dir >= 8 and not near_event and not signs and not row["near_drift"]:
            sp.append((month, s))
    rng.shuffle(sp)
    for month, s in sorted(sp[:PER_CATEGORY]):
        cases.append(make_case(f"SP-{s}-{month}", "SP", "real anomaly; same calendar month deviated the same way "
                               "in >= 8 of the previous 10 years; no event within 6 months", s, month, base, det,
                               events, judge))

    # --- calm months for the synthetic cases ----------------------------------------------
    flagged_idx = sorted(fl.index.unique())
    seas = {}
    for s in series_names:
        r = judge.trailing_ratio(base[s]).dropna()
        seas[s] = r.groupby(r.index.month).median()
    calm = []
    for m in base.index:
        if m.year < 1998 or m > base.index.max() - 12:
            continue
        if any(abs((m - f).n) <= 6 for f in flagged_idx):
            continue
        if any(abs((pd.Period(e["month"], freq="M") - m).n) <= 6 for e in events):
            continue
        if any(not 0.8 <= seas[s].get(m.month, 1) <= 1.2 for s in series_names):
            continue
        calm.append(m)
    rng.shuffle(calm)
    if len(calm) < 3 * PER_CATEGORY:
        sys.exit(f"Only {len(calm)} calm months; relax the criteria")
    count_cols = [c for c in series_names if prof.series[c]["kind"] == "count"] + ["excluded", "missing_key"]
    skipped = []
    shortfalls = {}

    def synth(category, builder, n, strengths=(0,)):
        """Build n cases; a case counts only if the ensemble flags its target month, as in production.

        Each (series, month, direction, strength) is tried once, so no case repeats;
        stronger variants are tried only after every calm month was tried at the weaker one.
        """
        made, used_months = 0, set()
        tries = iter([(k, m) for k in strengths for m in calm])
        while made < n:
            s = series_names[made % len(series_names)]
            up = (made // len(series_names)) % 2 == 0  # alternate direction within each series
            for strength, month in tries:
                if (s, month) in used_months:
                    continue
                mod, evs, construction, candidates = builder(base.copy(), month, s, made, up, strength)
                mod[count_cols] = mod[count_cols].round()
                d, _ = detectors.detect_all(mod, series_names)
                flagged_here = d[(d["series"] == s) & d["anomaly"]].index
                target = next((t for t in candidates if t in flagged_here), None)
                if target is None:
                    skipped.append(f"{category} {s} {month} strength {strength}")
                    continue
                used_months.add((s, month))
                cases.append(make_case(f"{category}-{s}-{target}", category, construction, s, target, mod, d, evs,
                                       judge))
                made += 1
                break
            else:
                # every calm month was tried at every strength: keep what could be built
                shortfalls[category] = n - made
                print(f"warning: {category}: only {made} of {n} flagged cases could be built")
                return

    def pdc(m, month, s, i, up, strength):
        f = ((2.5, 3.0, 4.0) if up else (0.4, 0.3, 0.25))[strength]
        m.loc[m.index >= month, series_names] *= f
        m.loc[m.index >= month, ["excluded", "missing_key"]] *= f
        ev = events + [{"month": str(month), "kind": "policy", "label": POLICY_EVENTS[i % len(POLICY_EVENTS)],
                        "source": "benchmark (synthetic)", "status": "verified"}]
        return (m, sorted(ev, key=lambda e: e["month"]),
                f"persistent x{f} from this month; policy event in the same month", [month])

    def dqe(m, month, s, i, up, strength):
        if not up:
            m.loc[month, series_names] *= 0.03
            m.loc[month, ["excluded", "missing_key"]] = 0
            how = "one month drops to 3% of its level (reporting failure); no event"
        else:
            k = (2.2, 3.0, 4.0)[strength]
            n = m.loc[month, "notices"]
            m.loc[month, series_names] *= k
            m.loc[month, "missing_key"] = round(0.45 * n * k)
            m.loc[month, "excluded"] = round(m.loc[month, "excluded"] * 3 + 5)
            how = (f"one month x{k} with 45% of records without identifier and 3x cancellations "
                   "(duplicated batch); no event")
        return m, events, how, [month]

    def ges(m, month, s, i, up, strength):
        f = (2.0, 2.5, 3.0)[strength] if up else (0.5, 0.4, 1 / 3)[strength]
        k = pd.Series(1.0, index=m.index)
        k[m.index >= month] = f
        k[month], k[month + 1] = f ** (1 / 3), f ** (2 / 3)
        m[series_names + ["excluded", "missing_key"]] = m[series_names + ["excluded", "missing_key"]].mul(k, axis=0)
        return (m, events, f"gradual ramp to x{f:.2g} over three months, persistent; no event, no data-quality signs",
                [month + 2, month + 1, month + 3, month])

    synth("PDC", pdc, PER_CATEGORY, strengths=(0, 1, 2))
    synth("DQE", dqe, PER_CATEGORY, strengths=(0, 1, 2))
    synth("GES", ges, PER_CATEGORY, strengths=(0, 1, 2))

    gold = {
        "_comment": "Gold set of the model benchmark; see gold/build_gold.py for how each case is built.",
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "upstream_ref": upstream_ref(),
        "profile": PROFILE_ID,
        "seed": SEED,
        "counts": pd.Series([c["gold"] for c in cases]).value_counts().to_dict(),
        "shortfalls": shortfalls,
        "skipped_not_flagged": skipped,
        "cases": cases,
    }
    GOLD_FILE.write_text(json.dumps(gold, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(cases)} cases written to {GOLD_FILE}: {gold['counts']}")
    for c in cases:
        print(f"  {c['id']:32s} votes={c['det_row']['votes']} drift={c['det_row']['near_drift']} :: {c['construction']}")


if __name__ == "__main__":
    main()
