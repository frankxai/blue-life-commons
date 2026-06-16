#!/usr/bin/env python3
"""Validate YAML frontmatter of content artifacts against schema/artifact-schema.yaml.

Usage: python scripts/validate_artifacts.py [paths...]
With no arguments, scans content/ and missions/ for Markdown files with frontmatter.
Files without frontmatter (plain docs, templates README files) are skipped.
"""
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "artifact-schema.yaml"
SCAN_DIRS = ["content", "missions"]


def extract_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])


def main(argv):
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    if argv:
        files = [Path(p) for p in argv]
    else:
        files = []
        for d in SCAN_DIRS:
            files.extend(sorted((ROOT / d).rglob("*.md")))

    errors = 0
    checked = 0
    for f in files:
        if not f.is_file() or f.suffix not in {".md", ".mdx"}:
            continue
        try:
            fm = extract_frontmatter(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            print(f"FAIL {f}: invalid YAML frontmatter: {e}")
            errors += 1
            continue
        if fm is None:
            continue
        checked += 1
        file_errors = sorted(validator.iter_errors(fm), key=lambda e: list(e.path))
        if file_errors:
            errors += 1
            print(f"FAIL {f}:")
            for e in file_errors:
                loc = "/".join(str(p) for p in e.path) or "(root)"
                print(f"  - {loc}: {e.message}")
        else:
            print(f"OK   {f}")

    print(f"\nChecked {checked} artifact(s); {errors} file(s) with errors.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
