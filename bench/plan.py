"""Decide which candidates need a (new) run.

A candidate is re-tested only when something that can change its answers
changed: the model build (Ollama manifest digest or GGUF file hash), the
production prompt code at the upstream ref, or the gold set. Otherwise its
earlier result is reused. Writes results/plan.json (every current entry and
its key) and, on GitHub Actions, the matrix of entries to run.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bench.common import (CANDIDATES_FILE, DISCOVERED_FILE, PROFILE_ID, RESULTS_DIR, RUNS_DIR, entry_key,  # noqa: E402
                          gold_hash, slug, upstream_path)
from bench.discover import manifest  # noqa: E402

PROMPT_FILES = ["src/judge.py", "src/profile.py", f"profiles/{PROFILE_ID}.json"]
FIRST_SEEN_FILE = RESULTS_DIR / "first_seen.json"

# Names that reach a shell, a URL or a job name (SECURITY.md): anything else is skipped.
SAFE = {
    "label": re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._:()+/-]{0,79}$"),
    "model": re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}(/[A-Za-z0-9][A-Za-z0-9._-]{0,63})?(:[A-Za-z0-9][A-Za-z0-9._-]{0,63})?$"),
    "hf_repo": re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}/[A-Za-z0-9][A-Za-z0-9._-]{0,95}$"),
    "hf_file": re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,150}\.gguf$"),
}
BACKENDS = {"ollama", "llamacpp", "llamacpp-prism"}


def safe_entry(entry: dict) -> bool:
    if entry.get("backend") not in BACKENDS:
        return False
    return all(SAFE[k].match(str(entry[k])) for k in SAFE if k in entry and entry[k] is not None)


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=upstream_path(), capture_output=True, text=True, check=True).stdout.strip()


def prompt_fingerprint(ref: str) -> tuple[str, str]:
    """(commit, fingerprint) of the production prompt code at `ref`."""
    commit = git("rev-parse", f"{ref}^{{commit}}")
    blobs = []
    for f in PROMPT_FILES:
        try:
            blobs.append(git("rev-parse", f"{commit}:{f}"))
        except subprocess.CalledProcessError:
            blobs.append("missing")
    return commit, hashlib.sha256("|".join(blobs).encode()).hexdigest()


def resolve_digest(entry: dict) -> str | None:
    if entry["backend"] == "ollama":
        name, _, tag = entry["model"].partition(":")
        info = manifest(name, tag or "latest")
        return info[0] if info else None
    r = requests.get(f"https://huggingface.co/api/models/{entry['hf_repo']}/tree/main", timeout=30)
    if r.status_code != 200:
        return None
    for f in r.json():
        if f.get("path") == entry["hf_file"]:
            return (f.get("lfs") or {}).get("oid") or f.get("oid")
    return None


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="run every candidate again")
    ap.add_argument("--only", default="", help="comma-separated labels to run (implies re-running them)")
    args = ap.parse_args(argv)

    cfg = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))
    discovered = json.loads(DISCOVERED_FILE.read_text(encoding="utf-8"))["entries"] if DISCOVERED_FILE.exists() else []
    g_hash = gold_hash()
    only = {s.strip() for s in args.only.split(",") if s.strip()}
    done_keys = {p.stem.split("__")[-1] for p in RUNS_DIR.glob("*.json")}
    refs: dict[str, tuple[str, str]] = {}
    plan, matrix, seen, unavailable = [], [], set(), []
    first_seen = json.loads(FIRST_SEEN_FILE.read_text(encoding="utf-8")) if FIRST_SEEN_FILE.exists() else {}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for raw in cfg["entries"] + discovered:
        entry = dict(raw)
        if not safe_entry(entry):
            print(f"::warning::skipping a candidate with an unexpected name or back-end: {str(raw)[:120]}")
            continue
        entry.setdefault("prompt_ref", "main")
        entry.setdefault("options", {})
        entry.setdefault("experiment", False)
        try:
            entry["digest"] = resolve_digest(entry)
        except requests.RequestException:
            entry["digest"] = None
        if not entry["digest"] or not re.match(r"^(sha256:)?[0-9a-f]{64}$", entry["digest"]):
            unavailable.append(entry["label"])
            continue
        # When this exact build was first seen: a new build is adopted only after a waiting period.
        build = f"{entry['backend']}|{entry.get('model')}|{entry['digest']}"
        entry["first_seen"] = first_seen.setdefault(build, now)
        dedup = (entry["backend"], entry["digest"], entry["prompt_ref"], json.dumps(entry["options"], sort_keys=True))
        if dedup in seen:
            continue  # e.g. "latest" and a size tag pointing to the same build
        seen.add(dedup)
        if entry["prompt_ref"] not in refs:
            refs[entry["prompt_ref"]] = prompt_fingerprint(entry["prompt_ref"])
        entry["prompt_sha"], p_fp = refs[entry["prompt_ref"]]
        entry["key"] = entry_key(entry, p_fp, g_hash)
        entry["slug"] = slug(entry["label"])
        plan.append(entry)
        rerun = args.force or entry["label"] in only
        if (entry["key"] not in done_keys or rerun) and (not only or entry["label"] in only):
            matrix.append(entry)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIRST_SEEN_FILE.write_text(json.dumps(first_seen, indent=1, sort_keys=True), encoding="utf-8")
    (RESULTS_DIR / "plan.json").write_text(json.dumps({
        "gold_hash": g_hash, "prompt_refs": {k: {"commit": v[0], "fingerprint": v[1]} for k, v in refs.items()},
        "production": cfg["production"], "selection": cfg["selection"], "entries": plan,
        "unavailable": unavailable}, indent=1), encoding="utf-8")
    print(f"{len(plan)} current candidates, {len(matrix)} to run, unavailable: {unavailable or 'none'}")
    for e in matrix:
        print(f"  run: {e['label']} [{e['backend']}] key {e['key']}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"matrix={json.dumps(matrix)}\n")
            fh.write(f"count={len(matrix)}\n")


if __name__ == "__main__":
    main()
