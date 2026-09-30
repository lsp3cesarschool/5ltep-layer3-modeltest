"""Shared helpers: paths, the upstream (production) code, case rendering.

The benchmark never re-implements the judge's prompt: it imports it from a
checkout of the main repository (5ltep-layer3) at a chosen ref, placed in
./upstream by the workflow (or pointed to by the UPSTREAM variable). What is
tested is therefore exactly what runs in production.
"""

import hashlib
import importlib
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
GOLD_FILE = ROOT / "gold" / "cases.json"
CANDIDATES_FILE = ROOT / "candidates.json"
RESULTS_DIR = ROOT / "results"
RUNS_DIR = RESULTS_DIR / "runs"
DISCOVERED_FILE = RESULTS_DIR / "discovered.json"
LEADERBOARD_FILE = RESULTS_DIR / "leaderboard.json"
RECOMMENDATION_FILE = RESULTS_DIR / "recommendation.json"
PROFILE_ID = "ibama-autos-infracao"

SEEDS = [11, 22, 33]
TEMPERATURE = 0.7
NUM_PREDICT = 400
NUM_CTX = 4096


def upstream_path() -> Path:
    return Path(os.environ.get("UPSTREAM", ROOT / "upstream")).resolve()


def import_upstream():
    """Import the production modules (src.judge, src.profile) from the upstream checkout."""
    path = str(upstream_path())
    if path not in sys.path:
        sys.path.insert(0, path)
    for name in [m for m in sys.modules if m == "src" or m.startswith("src.")]:
        del sys.modules[name]  # a different ref may have been imported before
    judge = importlib.import_module("src.judge")
    profile = importlib.import_module("src.profile")
    return judge, profile


def upstream_ref() -> str:
    head = upstream_path() / ".git"
    try:
        import subprocess
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=upstream_path(), capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return os.environ.get("UPSTREAM_REF", "unknown") if not head.exists() else "unknown"


def load_gold() -> dict:
    return json.loads(GOLD_FILE.read_text(encoding="utf-8"))


def case_frame(case: dict) -> pd.DataFrame:
    df = pd.DataFrame(case["monthly"])
    df.index = pd.PeriodIndex(df.pop("month"), freq="M")
    df.index.name = "month"
    return df


def render(case: dict, judge, profile_mod) -> tuple[str, str, dict, dict]:
    """(system prompt, user prompt, response schema, categories) for one case, as production builds them."""
    prof = profile_mod.load(str(upstream_path() / "profiles" / f"{PROFILE_ID}.json"))
    monthly = case_frame(case)
    month = pd.Period(case["month"], freq="M")
    row = pd.Series(case["det_row"])
    args = (prof, case["series"], month, monthly, row, case["other_flagged"], case["events"])
    try:
        prompt = judge.build_prompt(*args, case["same_month_flagged"])
    except TypeError:  # older prompt versions take no same-month list
        prompt = judge.build_prompt(*args)
    system = judge.system_prompt(prof)
    schema = judge.response_schema(prof)
    return system, prompt, schema, prof.categories


def gold_hash() -> str:
    # Line endings normalised, so the hash is the same on Windows and on the Linux runner.
    return hashlib.sha256(GOLD_FILE.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_")


def entry_key(entry: dict, prompt_fp: str, g_hash: str) -> str:
    """Cache key: a result is reused only for the same model build, prompt code and gold set."""
    raw = "|".join([entry["backend"], entry["model"], entry.get("digest") or "", prompt_fp, g_hash,
                    json.dumps(entry.get("options", {}), sort_keys=True)])
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def parse_answer(text: str, categories: dict) -> dict:
    try:
        data = json.loads(text)
        cat = str(data.get("category", "")).strip().upper()
        if cat not in categories:
            raise ValueError(cat)
        return {"category": cat, "confidence": float(data.get("confidence", 0) or 0),
                "reasoning": str(data.get("reasoning", ""))[:1500]}
    except (ValueError, TypeError, AttributeError):
        return {"category": "INVALID", "confidence": 0.0, "reasoning": (text or "")[:500]}
