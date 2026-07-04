#!/usr/bin/env python3
"""Build the object-storage migration manifest for approved species media.

The manifest is deliberately public-safe. It does not download files, does not
create signed URLs, and does not mark anything mirrored until object storage
credentials and derivative generation are configured outside Git.

Usage:
  python scripts/build_species_media_storage_manifest.py
  python scripts/build_species_media_storage_manifest.py --check
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
POLICY_PATH = ROOT / "content" / "media" / "species-media-storage-policy.yaml"
MANIFEST_PATH = ROOT / "content" / "media" / "species-media-storage-manifest.yaml"
REVIEW_PACK_PATH = (
    ROOT
    / "content"
    / "media"
    / "review-packs"
    / f"species-media-storage-manifest-{date.today().isoformat()}.md"
)

SOURCE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif", "svg", "tif", "tiff"}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def slug(value: str) -> str:
    value = (value or "none").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "none"


def url_host(url: str | None) -> str | None:
    if not url:
        return None
    return urlparse(url).netloc.lower().removeprefix("www.")


def source_extension(url: str | None) -> str:
    if not url:
        return "jpg"
    path = urlparse(url).path
    ext = Path(path).suffix.lower().lstrip(".")
    if ext in SOURCE_EXTENSIONS:
        return "jpg" if ext == "jpeg" else ext
    return "jpg"


def public_url(base_url: str, key: str) -> str:
    return f"{base_url.rstrip('/')}/{key}"


def variant_record(variant: dict, prefix: str, source_ext: str, base_url: str) -> dict:
    key = prefix + variant["key_template"].format(source_ext=source_ext)
    record = {
        "name": variant["name"],
        "role": variant["role"],
        "public_use": variant.get("public_use") is True,
        "format": variant.get("format"),
        "width": variant.get("width"),
        "height": variant.get("height"),
        "object_key": key,
        "status": "pending_generation",
    }
    if record["public_use"]:
        record["public_url"] = public_url(base_url, key)
    return record


def build_record(record: dict, policy: dict) -> dict:
    primary = record.get("primary") or {}
    species_path = ROOT / record["species_page"]
    page_fm = frontmatter(species_path)
    website_path = (page_fm.get("outputs") or {}).get("website_path")
    asset_id = primary.get("approved_asset_id")
    taxon_group = record.get("taxon_group")
    species_slug = record.get("slug") or slug(record.get("common_name"))
    source_ext = source_extension(primary.get("original_media_url") or primary.get("source_url"))
    prefix = policy["object_keys"]["prefix_pattern"].format(
        taxon_group=taxon_group,
        slug=species_slug,
        asset_id=asset_id,
    )
    variants = [
        variant_record(
            variant,
            prefix,
            source_ext,
            policy["public_delivery"]["public_base_url"],
        )
        for variant in policy.get("variants") or []
    ]

    rights_status = primary.get("rights_status")
    mirror_allowed = rights_status in {"owned", "licensed", "public-domain", "cc0", "cc-by", "cc-by-sa", "partner-grant"}
    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "website_path": website_path,
        "taxon_group": taxon_group,
        "slug": species_slug,
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "approved_asset_id": asset_id,
        "current_public_media_url": primary.get("original_media_url") or primary.get("source_url"),
        "source_url": primary.get("source_url"),
        "source_host": url_host(primary.get("source_url")),
        "original_media_url": primary.get("original_media_url"),
        "original_media_host": url_host(primary.get("original_media_url")),
        "creator": primary.get("creator"),
        "credit": primary.get("credit"),
        "license": primary.get("license"),
        "license_url": primary.get("license_url"),
        "rights_status": rights_status,
        "qa_status": primary.get("qa_status"),
        "approved_surfaces": primary.get("approved_surfaces") or [],
        "blocked_surfaces": primary.get("blocked_surfaces") or [],
        "storage": {
            "provider": policy["provider"]["primary"],
            "bucket": policy["buckets"]["production"],
            "public_base_url": policy["public_delivery"]["public_base_url"],
            "object_prefix": prefix,
            "source_ext": source_ext,
            "status": "mirror_pending",
            "mirror_allowed_by_current_rights_status": mirror_allowed,
            "no_download_performed": True,
            "public_site_preference": "current_approved_source_url_until_owned_variants_exist",
            "variants": variants,
        },
        "migration_gate": {
            "ready_for_mirror_review": primary.get("status") == "approved" and primary.get("qa_status") == "approved",
            "requires_human_recheck_before_copy": True,
            "requires_exif_strip": True,
            "requires_checksum_after_upload": True,
            "requires_database_asset_row": True,
            "requires_database_variant_rows": True,
        },
    }


def build_manifest(policy: dict, registry: dict) -> dict:
    records = [
        build_record(record, policy)
        for record in registry.get("records") or []
        if (record.get("primary") or {}).get("status") == "approved"
    ]
    provider_counts = Counter((record.get("storage") or {}).get("provider") for record in records)
    host_counts = Counter(record.get("source_host") or "none" for record in records)
    rights_counts = Counter(record.get("rights_status") or "none" for record in records)
    public_variant_total = sum(
        1
        for record in records
        for variant in (record.get("storage") or {}).get("variants") or []
        if variant.get("public_use") is True
    )
    object_total = sum(len((record.get("storage") or {}).get("variants") or []) for record in records)
    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "policy": {
            "source": "content/media/species-media-storage-policy.yaml",
            "no_download_performed": True,
            "candidate_public_use": False,
            "github_is_not_pixel_storage": True,
            "object_storage_is_pixel_storage": True,
            "public_routes_must_use_approved_variants_only": True,
        },
        "summary": {
            "approved_species_records": len(records),
            "provider_counts": dict(sorted(provider_counts.items())),
            "rights_status_counts": dict(sorted(rights_counts.items())),
            "source_host_counts": dict(sorted(host_counts.items())),
            "planned_object_count": object_total,
            "planned_public_variant_count": public_variant_total,
            "mirror_pending_count": len(records),
            "owned_storage_ready_count": 0,
        },
        "records": records,
    }


def render_review_pack(manifest: dict) -> str:
    lines = [
        "# Species Media Storage Manifest",
        "",
        f"Generated: {manifest['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Approved species records: {manifest['summary']['approved_species_records']}",
        f"- Planned objects: {manifest['summary']['planned_object_count']}",
        f"- Planned public variants: {manifest['summary']['planned_public_variant_count']}",
        f"- Mirror pending: {manifest['summary']['mirror_pending_count']}",
        f"- Owned storage ready: {manifest['summary']['owned_storage_ready_count']}",
        "",
        "## Operating Boundary",
        "",
        "- GitHub stores metadata, review evidence, object keys, and public-safe manifests.",
        "- Object storage stores the pixels.",
        "- Vercel renders the app and receives environment variables.",
        "- This manifest did not download, transform, upload, or sign any media.",
        "",
        "## Records",
        "",
        "| Species | Rights | Source host | Object prefix | Public variants | Status |",
        "|---|---|---|---|---:|---|",
    ]
    for record in manifest.get("records") or []:
        public_variants = sum(
            1 for variant in (record.get("storage") or {}).get("variants") or [] if variant.get("public_use") is True
        )
        lines.append(
            "| {species} | {rights} | {host} | `{prefix}` | {variants} | {status} |".format(
                species=record.get("common_name"),
                rights=record.get("rights_status"),
                host=record.get("source_host"),
                prefix=(record.get("storage") or {}).get("object_prefix"),
                variants=public_variants,
                status=(record.get("storage") or {}).get("status"),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_if_changed(path: Path, content: str, check: bool) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if current == content:
        return False
    if check:
        print(f"{path.relative_to(ROOT)} is stale; run scripts/build_species_media_storage_manifest.py")
        raise SystemExit(1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    policy = load_yaml(POLICY_PATH)
    registry = load_yaml(REGISTRY_PATH)
    manifest = build_manifest(policy, registry)
    manifest_text = yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False, width=120)
    review_text = render_review_pack(manifest)

    changed_manifest = write_if_changed(MANIFEST_PATH, manifest_text, args.check)
    changed_review = write_if_changed(REVIEW_PACK_PATH, review_text, args.check)
    if args.check:
        print("Species media storage manifest is up to date.")
    else:
        if changed_manifest:
            print(f"Wrote {MANIFEST_PATH.relative_to(ROOT)}")
        if changed_review:
            print(f"Wrote {REVIEW_PACK_PATH.relative_to(ROOT)}")
        if not changed_manifest and not changed_review:
            print("Species media storage manifest is already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
