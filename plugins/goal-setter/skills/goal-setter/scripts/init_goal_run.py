#!/usr/bin/env python3
"""Create a simple goal run with GOAL.md and execution-notes.md.

This helper intentionally creates only two run files:

  GOAL.md
  execution-notes.md

Storage policy:

  * --plan-dir writes sidecar files into an existing plan/spec directory.
  * --run-root writes under an explicit project-local or user-chosen root.
  * default writes to user state outside the repository.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


RUN_RE = re.compile(r"^(?P<seq>\d{4})--")


def git_root(cwd: Path) -> Path | None:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return None
    out = proc.stdout.strip()
    return Path(out) if out else None


def slugify(text: str, fallback: str, max_len: int = 64) -> str:
    text = unicodedata.normalize("NFKC", text or "").strip().lower()
    chars: list[str] = []
    last_dash = False
    for ch in text:
        if ch.isalnum():
            chars.append(ch)
            last_dash = False
        else:
            if not last_dash:
                chars.append("-")
                last_dash = True
    slug = "".join(chars).strip("-")
    if not slug:
        slug = fallback
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("-") or fallback
    return slug


def next_sequence(goal_runs_dir: Path) -> int:
    if not goal_runs_dir.exists():
        return 1
    max_seq = 0
    for child in goal_runs_dir.iterdir():
        if not child.is_dir():
            continue
        match = RUN_RE.match(child.name)
        if match:
            max_seq = max(max_seq, int(match.group("seq")))
    return max_seq + 1


def project_fingerprint(root: Path) -> str:
    name = slugify(root.name, "project", max_len=40)
    digest = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:10]
    return f"{name}-{digest}"


def default_user_state_root(root: Path) -> Path:
    xdg_state = os.environ.get("XDG_STATE_HOME")
    if xdg_state:
        base = Path(xdg_state).expanduser()
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path.home() / ".local" / "state"
    return base / "Codex" / "goal-runs" / project_fingerprint(root)


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def render(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def template_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "references"


def load_template(name: str) -> str:
    return (template_dir() / name).read_text(encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Create a goal run with two files.")
    parser.add_argument("--project-root", default=None, help="Project root. Defaults to git root or cwd.")
    parser.add_argument("--plan-dir", default=None, help="Existing plan/spec directory to receive GOAL.md sidecar files.")
    parser.add_argument("--run-root", default=None, help="Explicit root for run directories. Defaults to user state outside the repo.")
    parser.add_argument("--area", default=None, help="Searchable area/module keyword, e.g. checkout, auth, billing.")
    parser.add_argument("--outcome", default=None, help="Searchable outcome keyword, e.g. confirmation-flow.")
    parser.add_argument("--title", required=True, help="Human-readable goal title.")
    parser.add_argument("--objective", required=True, help="One-sentence verifiable objective.")
    parser.add_argument("--validation", default="discover from repo docs and relevant tests", help="Known validation command(s) or discovery rule.")
    parser.add_argument("--dry-run", action="store_true", help="Print paths without writing files.")
    args = parser.parse_args(argv)

    cwd = Path.cwd().resolve()
    root = Path(args.project_root).resolve() if args.project_root else (git_root(cwd) or cwd)
    timestamp = _dt.datetime.now().astimezone().strftime("%Y-%m-%d-%H%M%S")
    if args.plan_dir:
        run_dir = Path(args.plan_dir).expanduser()
        if not run_dir.is_absolute():
            run_dir = root / run_dir
        run_dir = run_dir.resolve()
        if not run_dir.exists() or not run_dir.is_dir():
            raise SystemExit(f"--plan-dir must be an existing directory: {run_dir}")
        run_id = run_dir.name
    else:
        if not args.area or not args.outcome:
            raise SystemExit("--area and --outcome are required unless --plan-dir is provided.")
        goal_runs_dir = Path(args.run_root).expanduser().resolve() if args.run_root else default_user_state_root(root)
        seq = next_sequence(goal_runs_dir)
        area_slug = slugify(args.area, "general")
        outcome_slug = slugify(args.outcome, "goal")
        run_id = f"{seq:04d}--{timestamp}--{area_slug}--{outcome_slug}"
        run_dir = goal_runs_dir / run_id
    created_at = _dt.datetime.now().astimezone().isoformat(timespec="seconds")
    goal_path = display_path(run_dir / "GOAL.md", root)
    notes_path = display_path(run_dir / "execution-notes.md", root)

    values = {
        "title": args.title.strip(),
        "run_id": run_id,
        "created_at": created_at,
        "objective": args.objective.strip(),
        "validation": args.validation.strip(),
        "goal_path": goal_path,
        "notes_path": notes_path,
    }
    goal = render(load_template("GOAL.template.md"), **values)
    notes = render(load_template("execution-notes.template.md"), **values)

    if args.dry_run:
        print(run_dir)
        print(run_dir / "GOAL.md")
        print(run_dir / "execution-notes.md")
        return 0

    if args.plan_dir:
        if (run_dir / "GOAL.md").exists() or (run_dir / "execution-notes.md").exists():
            raise SystemExit(f"Goal sidecar files already exist in: {run_dir}")
    else:
        run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "GOAL.md").write_text(goal, encoding="utf-8")
    (run_dir / "execution-notes.md").write_text(notes, encoding="utf-8")

    print(f"Created goal run: {run_id}")
    print(f"GOAL.md: {run_dir / 'GOAL.md'}")
    print(f"execution-notes.md: {run_dir / 'execution-notes.md'}")
    print("\nCompact set_goal objective:")
    print(
        f"Execute `{goal_path}` as the completion contract. "
        "Work autonomously until its Done when is satisfied by evidence, preserving its constraints, validation, progress/pivot, and On block rules. "
        f"Keep `{notes_path}` current only at meaningful checkpoints with material decisions, evidence, coverage limits, blockers, and final review. "
        "Do not restate or expand the plan in the native Goal; stop only under `GOAL.md` On block rules."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
