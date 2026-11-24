#!/usr/bin/env python
"""Generate student/ notebooks from instructor/ by stripping cells tagged "solution".

Usage:
    python tools/make_student_notebooks.py            # whole course
    python tools/make_student_notebooks.py --check    # exit 1 if student/ is out of date

Rules:
  * Cells whose metadata.tags contains "solution" are removed.
  * Outputs and execution counts of the remaining cells are cleared.
  * Non-notebook files (e.g. 2.5_automated_report/) are copied as-is.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent
SRC, DST = ROOT / "instructor", ROOT / "student"
TAG = "solution"


def strip_notebook(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    nb.cells = [c for c in nb.cells if TAG not in c.get("metadata", {}).get("tags", [])]
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs, cell.execution_count = [], None
    return nb


def build(check: bool = False) -> int:
    stale = 0
    for src in sorted(SRC.rglob("*")):
        if src.is_dir() or ".ipynb_checkpoints" in src.parts or "__pycache__" in src.parts:
            continue
        dst = DST / src.relative_to(SRC)
        if src.suffix == ".ipynb":
            nb = strip_notebook(nbformat.read(src, as_version=4))
            expected = nbformat.writes(nb)
            current = dst.read_text(encoding="utf-8") if dst.exists() else None
            if check:
                stale += current != expected
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(expected, encoding="utf-8")
            print(f"student <- {src.relative_to(ROOT)}")
        else:
            if check:
                stale += not dst.exists() or dst.read_bytes() != src.read_bytes()
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return stale


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    n = build(check=args.check)
    if args.check and n:
        print(f"{n} student file(s) out of date. Run: python tools/make_student_notebooks.py")
        sys.exit(1)
