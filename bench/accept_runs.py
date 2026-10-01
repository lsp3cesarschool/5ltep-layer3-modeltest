"""Accept the result of each "run" job, and only that (SECURITY.md).

Each run job executes a downloaded model with a read-only token and hands over one file,
results/runs/<slug>__<key>.json, in an artifact named run-<slug>. A compromised job could put
other files in its artifact, for instance a fake result for another candidate, to lower the
production model or to favour its own. This script takes from artifact run-<slug> only the file
named after that candidate's planned key, checks its structure and bounds its text, and copies
it into results/runs/. Everything else is ignored and reported.

  python bench/accept_runs.py <folder with one sub-folder per artifact>
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bench.common import RESULTS_DIR, RUNS_DIR  # noqa: E402

MAX_BYTES = 8_000_000
MAX_TEXT = 2400
CATEGORY = re.compile(r"^[A-Z]{2,10}$")


def check(data: dict, entry: dict) -> dict:
    if not isinstance(data, dict) or data.get("key") != entry["key"] or data.get("label") != entry["label"]:
        raise ValueError("key or label does not match the plan")
    answers = data.get("answers")
    if not isinstance(answers, list):
        raise ValueError("no answers")
    for a in answers:
        if not isinstance(a, dict) or not isinstance(a.get("case"), str) or not isinstance(a.get("runs"), list):
            raise ValueError("malformed answer")
        for r in a["runs"]:
            if not isinstance(r, dict) or not CATEGORY.match(str(r.get("category", ""))):
                raise ValueError("malformed run")
            if not isinstance(r.get("latency_s", 0), (int, float)) or not isinstance(r.get("seed", 0), int):
                raise ValueError("malformed run numbers")
            r["reasoning"] = str(r.get("reasoning", ""))[:MAX_TEXT]
    data["entry"] = entry  # what was planned, not what the job says it ran
    return data


def main(folder: str) -> None:
    plan = json.loads((RESULTS_DIR / "plan.json").read_text(encoding="utf-8"))
    by_slug = {e["slug"]: e for e in plan["entries"]}
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    accepted, refused = 0, []
    for art in sorted(Path(folder).glob("run-*")):
        entry = by_slug.get(art.name.removeprefix("run-"))
        if not entry:
            refused.append(f"{art.name}: not in the plan")
            continue
        expected = f"{entry['slug']}__{entry['key']}.json"
        for f in art.rglob("*"):
            if f.is_file() and f.name != expected:
                refused.append(f"{art.name}/{f.name}: not this candidate's result")
        path = next((f for f in art.rglob(expected) if f.is_file()), None)
        if not path:
            continue  # the job failed before writing anything
        try:
            if path.stat().st_size > MAX_BYTES:
                raise ValueError("too large")
            data = check(json.loads(path.read_text(encoding="utf-8")), entry)
        except (ValueError, json.JSONDecodeError) as exc:
            refused.append(f"{art.name}/{path.name}: {exc}")
            continue
        (RUNS_DIR / expected).write_text(json.dumps(data, indent=1), encoding="utf-8")
        accepted += 1
    for r in refused:
        print(f"::warning::refused {r}")
    print(f"accepted {accepted} result file(s); refused {len(refused)}")


if __name__ == "__main__":
    main(sys.argv[1])
