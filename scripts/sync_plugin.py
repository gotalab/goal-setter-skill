#!/usr/bin/env python3
"""Sync the root goal-setter skill into the Codex plugin bundle."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    ("skills/goal-setter/SKILL.md", "plugins/goal-setter/skills/goal-setter/SKILL.md"),
    ("skills/goal-setter/agents/openai.yaml", "plugins/goal-setter/skills/goal-setter/agents/openai.yaml"),
    (
        "skills/goal-setter/scripts/validate_goal_length.py",
        "plugins/goal-setter/skills/goal-setter/scripts/validate_goal_length.py",
    ),
    ("assets/goal-setter-icon.png", "plugins/goal-setter/assets/goal-setter-icon.png"),
    ("assets/goal-setter-composer-icon.png", "plugins/goal-setter/assets/goal-setter-composer-icon.png"),
]


def changed_pairs() -> list[tuple[Path, Path]]:
    changed: list[tuple[Path, Path]] = []
    for src_rel, dst_rel in PAIRS:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            raise FileNotFoundError(src)
        if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
            changed.append((src, dst))
    return changed


def sync() -> None:
    for src, dst in changed_pairs():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"synced {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def check() -> int:
    changed = changed_pairs()
    if not changed:
        print("plugin bundle is in sync")
        return 0
    for src, dst in changed:
        print(f"out of sync: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if plugin files are out of sync")
    args = parser.parse_args(argv)
    if args.check:
        return check()
    sync()
    return 0


if __name__ == "__main__":
    sys.exit(main())
