#!/usr/bin/env python3
"""Check release metadata and generated plugin files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import sync_plugin


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as f:
        return json.load(f)


def changelog_version() -> str:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^##\s+([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError("CHANGELOG.md has no version heading")
    return match.group(1)


def check_versions() -> int:
    versions = {
        "CHANGELOG.md": changelog_version(),
        ".claude-plugin/plugin.json": read_json(".claude-plugin/plugin.json")["version"],
        "plugins/goal-setter/.codex-plugin/plugin.json": read_json(
            "plugins/goal-setter/.codex-plugin/plugin.json"
        )["version"],
    }
    unique = set(versions.values())
    if len(unique) == 1:
        print(f"versions match: {unique.pop()}")
        return 0
    for path, version in versions.items():
        print(f"version mismatch: {path} -> {version}")
    return 1


def main() -> int:
    status = 0
    status |= sync_plugin.check()
    status |= check_versions()
    return status


if __name__ == "__main__":
    sys.exit(main())
