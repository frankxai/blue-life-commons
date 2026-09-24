#!/usr/bin/env python3
"""Validate kit manifests and release gates without external dependencies.

Usage: python3 scripts/validate_kits.py [kits/k0-sampling/manifest.json ...]
No arguments validates every kits/*/manifest.json. This intentionally supports
only the JSON Schema keywords used by schema/kit-schema.json; unknown keywords
fail closed so this executable contract cannot silently drift from the schema.
"""

import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "kit-schema.json"
PRIVATE_KEYS = {
    "address", "street_address", "house_number", "postal_code",
    "coordinates", "latitude", "longitude", "precise_location",
    "exact_location",
}
SUPPORTED = {
    "$schema", "$id", "title", "type", "additionalProperties", "required",
    "properties", "$defs", "$ref", "const", "enum", "pattern", "minLength",
    "minItems", "minimum", "format", "items",
}


def schema_errors(value, spec, defs, pointer="$"):
    """Small strict evaluator for the *actual* keywords in our kit schema."""
    unknown = set(spec) - SUPPORTED
    if unknown:
        return [f"{pointer}: unsupported schema keywords {sorted(unknown)}"]
    if "$ref" in spec:
        name = spec["$ref"].removeprefix("#/$defs/")
        if spec["$ref"] != f"#/$defs/{name}" or name not in defs:
            return [f"{pointer}: unsupported schema reference {spec['$ref']}"]
        return schema_errors(value, defs[name], defs, pointer)
    errors = []
    types = {"object": dict, "array": list, "string": str, "integer": int}
    kind = spec.get("type")
    if kind and type(value) is not types[kind]:
        return [f"{pointer}: expected {kind}"]
    if "const" in spec and value != spec["const"]:
        errors.append(f"{pointer}: must equal {spec['const']!r}")
    if "enum" in spec and value not in spec["enum"]:
        errors.append(f"{pointer}: value not in allowed set")
    if isinstance(value, dict):
        for key in spec.get("required", []):
            if key not in value:
                errors.append(f"{pointer}.{key}: missing")
        if spec.get("additionalProperties") is False:
            for key in sorted(set(value) - set(spec.get("properties", {}))):
                errors.append(f"{pointer}.{key}: unknown field")
        for key, child in spec.get("properties", {}).items():
            if key in value:
                errors += schema_errors(value[key], child, defs, f"{pointer}.{key}")
    if isinstance(value, list):
        if len(value) < spec.get("minItems", 0):
            errors.append(f"{pointer}: too few items")
        for index, child in enumerate(value):
            if "items" in spec:
                errors += schema_errors(child, spec["items"], defs, f"{pointer}[{index}]")
    if isinstance(value, str):
        if len(value) < spec.get("minLength", 0):
            errors.append(f"{pointer}: too short")
        if "pattern" in spec and not re.fullmatch(spec["pattern"], value):
            errors.append(f"{pointer}: wrong format")
        if spec.get("format") == "uri" and (
            urlparse(value).scheme != "https" or not urlparse(value).netloc
        ):
            errors.append(f"{pointer}: expected an HTTPS URL")
        if spec.get("format") == "date":
            try:
                if dt.date.fromisoformat(value).isoformat() != value:
                    raise ValueError
            except ValueError:
                errors.append(f"{pointer}: expected ISO date")
    if type(value) is int and value < spec.get("minimum", value):
        errors.append(f"{pointer}: below minimum")
    return errors


def private_location_errors(node, pointer="$"):
    errors = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key.lower() in PRIVATE_KEYS:
                errors.append(f"{pointer}.{key}: private location field forbidden")
            errors += private_location_errors(value, f"{pointer}.{key}")
    if isinstance(node, list):
        for index, value in enumerate(node):
            errors += private_location_errors(value, f"{pointer}[{index}]")
    return errors


def source_path_errors(path_string, field):
    path = Path(path_string)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        return [f"{field}: must be a repository-relative path"]
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():
        return [f"{field}: linked source file does not exist in repository"]
    return []


def invariant_errors(kit):
    errors = private_location_errors(kit)
    parts = kit["parts"]
    ids = [part["id"] for part in parts]
    if len(ids) != len(set(ids)):
        errors.append("parts: duplicate part id")
    for field in ("budget_eur", *(f"parts.{p['id']}.cost_eur" for p in parts)):
        cost = kit["budget_eur"] if field == "budget_eur" else next(
            p["cost_eur"] for p in parts if field == f"parts.{p['id']}.cost_eur"
        )
        if cost["min"] > cost["max"]:
            errors.append(f"{field}: min exceeds max")
    mins = sum(part["cost_eur"]["min"] for part in parts)
    maxes = sum(part["cost_eur"]["max"] for part in parts)
    if kit["budget_eur"]["min"] < mins or kit["budget_eur"]["max"] < maxes:
        errors.append("budget_eur: budget cannot cover the line-item totals")
    for part in parts:
        if part["price_basis"] == "vendor-listing" and not (
            part.get("vendor_url") and part.get("checked_on")
        ):
            errors.append(f"parts.{part['id']}: vendor listing needs URL and price check date")
        if kit["environment"] == "dry-side" and part["contact"] == "permitted-water":
            errors.append(f"parts.{part['id']}: water-contact part in a dry-side kit")
    for field in ("protocol_path", "test_report_path", "replication_report_path"):
        if field in kit:
            errors += source_path_errors(kit[field], field)
    for index, path in enumerate(kit["source_designs"]):
        errors += source_path_errors(path, f"source_designs[{index}]")
    maturity = kit["maturity"]
    if maturity != "proposed" and not kit.get("test_report_path"):
        errors.append("test_report_path: required beyond proposed maturity")
    if maturity in ("authorized-field-trial", "replicated"):
        if kit["environment"] != "approved-open-water":
            errors.append("environment: field trial requires approved-open-water")
        if any(v != "approved" for v in kit["review"].values()):
            errors.append("review: all reviewers must approve before field trial")
        if not kit.get("approval_reference"):
            errors.append("approval_reference: required before field trial")
    if maturity == "replicated" and not kit.get("replication_report_path"):
        errors.append("replication_report_path: required for replicated maturity")
    if kit["environment"] == "approved-open-water" and maturity not in (
        "authorized-field-trial", "replicated"
    ):
        errors.append("environment: open water requires field-trial maturity")
    if any(c["kind"] == "measured" for c in kit["claims"]):
        if maturity == "proposed" or not kit.get("test_report_path"):
            errors.append("claims: measured claim needs a test report and bench-tested maturity")
    return errors


def validate_file(path, schema):
    try:
        kit = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{path}: invalid JSON or unreadable file: {exc}"], None
    errors = schema_errors(kit, schema, schema["$defs"])
    if errors:
        return errors, kit
    return invariant_errors(kit), kit


def main(argv):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    paths = [Path(arg) for arg in argv] if argv else sorted((ROOT / "kits").glob("*/manifest.json"))
    if not paths:
        print("FAIL no kit manifests found")
        return 1
    bad = 0
    ids = {}
    for path in paths:
        errors, kit = validate_file(path, schema)
        if kit and isinstance(kit, dict) and kit.get("id"):
            if kit["id"] in ids:
                errors.append(f"id: duplicate of {ids[kit['id']]}")
            ids[kit["id"]] = path
        print(("FAIL" if errors else "OK") + f"  {path}")
        for error in errors:
            print(f"  - {error}")
        bad += bool(errors)
    print(f"Checked {len(paths)} kit(s), {bad} invalid.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
