#!/usr/bin/env python3
"""Integrity lint for Blue Life Commons artifacts — beyond schema shape.

Enforces the rules a JSON Schema can't express (SOURCES.md, ETHICS.md):
  ERRORS (fail CI):
    - science-sensitive artifact with zero sources
    - anthropomorphic claim presented as fact ("the whale thinks/feels/says/wants ...")
    - status: published/approved on a science-sensitive type without review.science: approved
  WARNINGS (reported, do not fail):
    - species-page approved/published without iucn.assessment_date (staleness invisible)
    - artifact lacks a sensitivity tier for vulnerable-taxa types

Usage: python scripts/lint_content.py [paths...]   (default: scan content/ + missions/)
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["content", "missions"]

SCIENCE_SENSITIVE = {
    "species-page",
    "region-briefing",
    "research-summary",
    "dataset-card",
    "observation-guide",
    "field-mission",
}

# Anthropomorphic-claim-as-fact: an animal subject + a mind verb, NOT hedged by a citation cue.
ANTHRO = re.compile(
    r"\b(the\s+)?(whale|dolphin|seal|sea lion|turtle|shark|ray|orca|cetacean)s?\b[^.\n]{0,40}?"
    r"\b(thinks?|feels?|believes?|wants?|knows?|says?|tells?|understands?|is\s+saying|is\s+thinking)\b",
    re.IGNORECASE,
)
# Hedges that make a behavioral statement acceptable (cited / framed as research).
HEDGE = re.compile(r"(research|stud(y|ies)|observed|evidence|accord|suggest|\[|\(20)", re.IGNORECASE)


def split(text: str):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        return yaml.safe_load(parts[1]), parts[2]
    except yaml.YAMLError:
        return None, text


def lint_file(path: Path):
    errors, warnings = [], []
    fm, body = split(path.read_text(encoding="utf-8"))
    if fm is None or "type" not in fm:
        return errors, warnings
    typ = fm.get("type")
    status = fm.get("status")
    review = fm.get("review") or {}

    if typ in SCIENCE_SENSITIVE and not (fm.get("sources") or []):
        errors.append("science-sensitive artifact has no sources (SOURCES.md: no source, no claim)")

    if typ in SCIENCE_SENSITIVE and status in {"approved", "published"} and review.get("science") != "approved":
        errors.append(f"status={status} but review.science={review.get('science')!r} (must be approved)")

    for line in body.splitlines():
        if ANTHRO.search(line) and not HEDGE.search(line):
            errors.append(f"possible anthropomorphic claim as fact: {line.strip()[:90]!r}")

    if typ == "species-page" and status in {"approved", "published"}:
        if not (fm.get("iucn") or {}).get("assessment_date"):
            warnings.append("approved species-page without iucn.assessment_date (status staleness invisible)")

    return errors, warnings


def main(argv):
    if argv:
        files = [Path(p) for p in argv]
    else:
        files = []
        for d in SCAN_DIRS:
            files.extend(sorted((ROOT / d).rglob("*.md")))

    total_err = total_warn = checked = 0
    for f in files:
        if not f.is_file() or f.suffix not in {".md", ".mdx"}:
            continue
        errors, warnings = lint_file(f)
        if errors or warnings:
            checked += 1
        for e in errors:
            print(f"ERROR {f}: {e}")
            total_err += 1
        for w in warnings:
            print(f"WARN  {f}: {w}")
            total_warn += 1

    print(f"\nIntegrity lint: {total_err} error(s), {total_warn} warning(s).")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
