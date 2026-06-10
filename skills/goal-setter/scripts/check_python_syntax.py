#!/usr/bin/env python3
"""Read-only Python syntax check for sandboxed skill helper scripts.

This intentionally uses compile() instead of py_compile so it does not create
__pycache__ or .pyc files next to the checked script.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Python syntax without writing .pyc files.")
    parser.add_argument("paths", nargs="+", help="Python files to syntax-check.")
    args = parser.parse_args()

    failed = False
    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except Exception as exc:
            failed = True
            print(f"{path}: FAIL: {exc}")
        else:
            print(f"{path}: ok")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
