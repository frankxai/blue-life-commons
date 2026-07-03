#!/usr/bin/env python3
"""Build media outreach packets for official, partner, and NGO requests.

The acquisition plan says what each species needs next. This script turns that
plan into practical outreach requests grouped by source domain, with reusable
permission fields and email-ready copy. It deliberately omits candidate file
pages and direct image URLs, because outreach planning is not image approval.

Usage:
  python scripts/build_species_media_outreach_packets.py
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
ACQUISITION_PLAN_PATH = ROOT / "content" / "media" / "species-media-acquisition-plan.yaml"
PUBLIC_EXPLORER_PATH = ROOT / "content" / "media" / "species-media-public-explorer-manifest.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
OUTREACH_PACKETS_PATH = ROOT / "content" / "media" / "species-media-outreach-packets.yaml"
REVIEW_PACK_PATH = (
    ROOT
    / "content"
    / "media"
    / "review-packs"
    / f"species-media-outreach-packets-{date.today().isoformat()}.md"
)

REQUEST_TYPE_BY_LANE = {
    "ethics_first_candidate_review": "request_ethically_safe_alternative_or_context",
    "official_public_domain_review": "confirm_official_public_domain_terms",
    "open_public_domain_review": "confirm_public_domain_terms",
    "open_license_attribution_review": "confirm_open_license_attribution_terms",
    "partner_or_ngo_media_grant": "request_media_grant_or_replacement",
    "promotion_apply_ready": "no_outreach_promotion_ready",
    "primary_approved_maintenance": "rights_maintenance_recheck",
}

REQUEST_LABELS = {
    "request_ethically_safe_alternative_or_context": "Ask for an ethically safe alternative image or source context before rights review.",
    "confirm_official_public_domain_terms": "Confirm official/public-domain image-level terms and credit wording.",
    "confirm_public_domain_terms": "Confirm public-domain basis, original source, and species caption.",
    "confirm_open_license_attribution_terms": "Confirm creator, attribution, license URL, and surface compatibility.",
    "request_media_grant_or_replacement": "Request written permission or a replacement official/partner image.",
    "no_outreach_promotion_ready": "No outreach needed before the curator promotion command.",
    "rights_maintenance_recheck": "Recheck approved rights, attribution, and blocked surfaces on schedule.",
}

REQUESTED_SURFACES = [
    "species page visual slot",
    "species visual explorer card",
    "education deck",
    "grant or partner report",
    "social crop",
]

BLOCKED_UNTIL_PERMISSION = [
    "species page hero image",
    "downloaded/cropped source-page image",
    "social crop",
    "paid ads or merchandise",
    "any use that exposes precise sensitive location metadata",
]

REQUIRED_PERMISSION_FIELDS = [
    "exact image or media item",
    "creator or photographer",
    "required credit line",
    "license name and license URL",
    "rights status",
    "commercial-use compatibility",
    "derivative/crop compatibility",
    "approved surfaces",
    "blocked surfaces",
    "embargo, revocation, or takedown terms",
    "sensitive-location or EXIF handling",
    "welfare or depiction constraints",
    "written permission contact and date",
]


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def by_id(payload):
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def domain(url):
    if not url:
        return None
    return urlparse(url).netloc.lower().removeprefix("www.")


def slug(value):
    allowed = []
    for char in (value or "source-to-confirm").lower():
        if char.isalnum():
            allowed.append(char)
        elif char in {".", "-", "_"}:
            allowed.append("-")
    return "-".join("".join(allowed).split("-")).strip("-") or "source-to-confirm"


def request_type(acquisition_record):
    lane = acquisition_record.get("acquisition_lane")
    return REQUEST_TYPE_BY_LANE.get(lane, "request_media_grant_or_replacement")


def target_domains(acquisition_record):
    source_strategy = acquisition_record.get("source_strategy") or {}
    targets = [
        item
        for item in source_strategy.get("outreach_targets") or []
        if item and item != "partner_media_grant_needed"
    ]
    current_visual = acquisition_record.get("current_visual") or {}
    source_domain = current_visual.get("public_source_domain") or domain(current_visual.get("public_source_url"))
    if source_domain:
        targets.append(source_domain)
    return sorted(set(targets)) or ["source-to-confirm"]


def body_lines(acquisition_record, public_record, request):
    common_name = acquisition_record.get("common_name")
    scientific_name = acquisition_record.get("scientific_name")
    artifact_id = acquisition_record.get("artifact_id")
    source_url = ((acquisition_record.get("current_visual") or {}).get("public_source_url"))
    website_path = acquisition_record.get("website_path") or public_record.get("website_path")
    lines = [
        "Hello,",
        "",
        (
            "Blue Life Commons is preparing source-led species media records and would "
            f"like to confirm image-level media terms for {common_name} "
            f"({scientific_name})."
        ),
        "",
        f"Species record: {artifact_id}",
    ]
    if website_path:
        lines.append(f"Future public page path: {website_path}")
    if source_url:
        lines.append(f"Current source card URL: {source_url}")
    lines.extend(
        [
            "",
            "Could you point us to an official image, partner media item, or permission path that includes:",
            "- exact creator/photographer and credit line",
            "- image-level license or written permission terms",
            "- approved and blocked surfaces",
            "- crop/derivative/social-use constraints",
            "- any sensitive-location, EXIF, welfare, or embargo constraints",
            "",
            (
                "Until those terms are explicit, we will keep the page on a source-card "
                "fallback and will not copy, crop, download, or use the image as a species hero."
            ),
            "",
            "Thank you.",
        ]
    )
    if request == "request_ethically_safe_alternative_or_context":
        lines.insert(
            7,
            "We are especially trying to avoid imagery that could imply unsafe proximity, handling, baiting, crowding, or sensitive-location exposure.",
        )
    return lines


def build_record(registry_record, acquisition_record, public_record, approval_record):
    artifact_id = registry_record.get("artifact_id")
    acquisition_record = acquisition_record or {}
    public_record = public_record or {}
    approval_record = approval_record or {}
    current_visual = acquisition_record.get("current_visual") or {}
    source_strategy = acquisition_record.get("source_strategy") or {}
    approval_gap = acquisition_record.get("approval_gap") or {}
    request = request_type(acquisition_record)
    targets = target_domains(acquisition_record)

    return {
        "artifact_id": artifact_id,
        "ownership_key": f"{artifact_id}|{registry_record.get('species_page')}",
        "species_page": registry_record.get("species_page"),
        "website_path": acquisition_record.get("website_path") or public_record.get("website_path"),
        "common_name": registry_record.get("common_name"),
        "scientific_name": registry_record.get("scientific_name"),
        "taxon_group": registry_record.get("taxon_group"),
        "priority": acquisition_record.get("priority") or "P2",
        "outreach_status": "draft",
        "request_type": request,
        "request_label": REQUEST_LABELS[request],
        "acquisition": {
            "lane": acquisition_record.get("acquisition_lane"),
            "label": acquisition_record.get("acquisition_label"),
            "target_source_family": source_strategy.get("target_source_family"),
            "target_source_family_label": source_strategy.get("target_source_family_label"),
            "google_images_role": source_strategy.get("google_images_role") or "discovery_only",
            "partner_media_grant_needed": source_strategy.get("partner_media_grant_needed") is True,
            "outreach_targets": targets,
        },
        "current_public_source": {
            "kind": current_visual.get("public_visual_kind"),
            "source_url": current_visual.get("public_source_url"),
            "domain": current_visual.get("public_source_domain") or domain(current_visual.get("public_source_url")),
            "source_type": current_visual.get("public_source_type"),
            "source_card_status": current_visual.get("source_card_status"),
            "public_use": current_visual.get("public_use") is True,
            "source_card_does_not_authorize_image_copy": True,
        },
        "approval_gap": {
            "decision": approval_gap.get("decision") or approval_record.get("decision"),
            "checks_complete": approval_gap.get("checks_complete") or 0,
            "checks_total": approval_gap.get("checks_total") or 0,
            "promotion_allowed_now": approval_gap.get("promotion_allowed_now") is True,
        },
        "permission_request": {
            "requested_surfaces": REQUESTED_SURFACES,
            "blocked_until_written_permission": BLOCKED_UNTIL_PERMISSION,
            "required_permission_fields": REQUIRED_PERMISSION_FIELDS,
            "source_card_fallback_until_approved": True,
            "candidate_direct_urls_omitted": True,
            "candidate_public_use": False,
            "written_permission_required_before_reuse": True,
        },
        "message_template": {
            "subject": f"Blue Life Commons media permission request: {registry_record.get('common_name')}",
            "body_lines": body_lines(acquisition_record, public_record, request),
        },
        "handoff": {
            "approval_queue_record": f"{rel(APPROVAL_QUEUE_PATH)}#{artifact_id}",
            "acquisition_plan_record": f"{rel(ACQUISITION_PLAN_PATH)}#{artifact_id}",
            "public_explorer_record": f"{rel(PUBLIC_EXPLORER_PATH)}#{artifact_id}",
            "after_permission_next_step": "Update species-media-approval-queue.yaml with reviewer, date, checks, approved-primary metadata, then run promote_species_media.py as a dry run.",
        },
    }


def build_target_packets(records):
    grouped = defaultdict(list)
    for record in records:
        for target in (record.get("acquisition") or {}).get("outreach_targets") or ["source-to-confirm"]:
            grouped[target].append(record)

    packets = []
    for target, target_records in sorted(grouped.items()):
        source_urls = sorted(
            {
                (record.get("current_public_source") or {}).get("source_url")
                for record in target_records
                if (record.get("current_public_source") or {}).get("source_url")
            }
        )
        request_counts = Counter(record.get("request_type") or "none" for record in target_records)
        lane_counts = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in target_records)
        packets.append(
            {
                "target_id": slug(target),
                "target": target,
                "status": "draft",
                "request_count": len(target_records),
                "species_artifact_ids": [record["artifact_id"] for record in target_records],
                "source_urls": source_urls,
                "request_type_counts": dict(sorted(request_counts.items())),
                "acquisition_lane_counts": dict(sorted(lane_counts.items())),
                "preferred_contact_route": "Use the publisher, institution, NGO, or partner media/contact page. Do not infer private email addresses.",
                "packet_goal": "Confirm image-level rights or request a written media grant/replacement image.",
                "permission_fields": REQUIRED_PERMISSION_FIELDS,
                "records": [
                    {
                        "artifact_id": record["artifact_id"],
                        "common_name": record["common_name"],
                        "scientific_name": record["scientific_name"],
                        "request_type": record["request_type"],
                        "priority": record["priority"],
                        "source_url": (record.get("current_public_source") or {}).get("source_url"),
                    }
                    for record in target_records
                ],
            }
        )
    return packets


def build_payload():
    registry = load_yaml(REGISTRY_PATH)
    acquisition = load_yaml(ACQUISITION_PLAN_PATH)
    public = load_yaml(PUBLIC_EXPLORER_PATH)
    approval = load_yaml(APPROVAL_QUEUE_PATH)

    acquisition_by_id = by_id(acquisition)
    public_by_id = by_id(public)
    approval_by_id = by_id(approval)

    records = [
        build_record(
            registry_record,
            acquisition_by_id.get(registry_record.get("artifact_id")),
            public_by_id.get(registry_record.get("artifact_id")),
            approval_by_id.get(registry_record.get("artifact_id")),
        )
        for registry_record in registry.get("records") or []
    ]
    packets = build_target_packets(records)
    request_counts = Counter(record.get("request_type") or "none" for record in records)
    status_counts = Counter(record.get("outreach_status") or "none" for record in records)
    lane_counts = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in records)
    target_family_counts = Counter(
        (record.get("acquisition") or {}).get("target_source_family") or "none" for record in records
    )
    domain_counts = Counter((record.get("current_public_source") or {}).get("domain") or "none" for record in records)
    priorities = Counter(record.get("priority") or "none" for record in records)
    approved_primary_needed = sum(
        1
        for record in records
        if (record.get("approval_gap") or {}).get("promotion_allowed_now") is not True
    )

    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "sources": {
            "registry": rel(REGISTRY_PATH),
            "acquisition_plan": rel(ACQUISITION_PLAN_PATH),
            "public_explorer": rel(PUBLIC_EXPLORER_PATH),
            "approval_queue": rel(APPROVAL_QUEUE_PATH),
        },
        "policy": {
            "outreach_is_not_approval": True,
            "public_safe": True,
            "candidate_direct_urls_omitted": True,
            "candidate_public_use": False,
            "source_card_does_not_authorize_image_copy": True,
            "google_images_discovery_only": True,
            "written_permission_required_before_reuse": True,
            "do_not_infer_private_contact_details": True,
            "no_scraping_or_bulk_download": True,
        },
        "summary": {
            "species_records": len(records),
            "outreach_target_count": len(packets),
            "outreach_request_count": sum(packet["request_count"] for packet in packets),
            "approved_primary_needed": approved_primary_needed,
            "request_type_counts": dict(sorted(request_counts.items())),
            "outreach_status_counts": dict(sorted(status_counts.items())),
            "acquisition_lane_counts": dict(sorted(lane_counts.items())),
            "target_source_family_counts": dict(sorted(target_family_counts.items())),
            "priority_counts": dict(sorted(priorities.items())),
            "source_domain_counts": dict(sorted(domain_counts.items())),
        },
        "target_packets": packets,
        "records": records,
    }


def markdown(payload):
    summary = payload.get("summary") or {}
    lines = [
        "# Species Media Outreach Packets",
        "",
        f"Generated: {payload.get('generated_at')}",
        "",
        "Public-safe operating packet for requesting or confirming official, partner, NGO, or open-license species media. This packet does not approve images and does not include candidate direct image URLs or Commons file pages.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary.get('species_records')}",
        f"- Outreach targets: {summary.get('outreach_target_count')}",
        f"- Outreach requests: {summary.get('outreach_request_count')}",
        f"- Approved primary images still needed: {summary.get('approved_primary_needed')}",
        "",
        "## Request Type Counts",
        "",
    ]
    for request, count in (summary.get("request_type_counts") or {}).items():
        lines.append(f"- `{request}`: {count}")

    lines.extend(["", "## Target Packets", ""])
    for packet in payload.get("target_packets") or []:
        lines.append(f"### {packet.get('target')}")
        lines.append("")
        lines.append(f"- Requests: {packet.get('request_count')}")
        lines.append(f"- Status: `{packet.get('status')}`")
        lines.append(f"- Contact route: {packet.get('preferred_contact_route')}")
        if packet.get("source_urls"):
            lines.append("- Source URLs:")
            for source_url in packet["source_urls"]:
                lines.append(f"  - {source_url}")
        lines.append("- Species:")
        for record in packet.get("records") or []:
            lines.append(
                f"  - {record.get('common_name')} (*{record.get('scientific_name')}*) - `{record.get('request_type')}`"
            )
        lines.append("")

    lines.extend(
        [
            "## Species Request Board",
            "",
            "| Species | Target | Request | Checks | Public source |",
            "|---|---|---|---|---|",
        ]
    )
    for record in payload.get("records") or []:
        source = record.get("current_public_source") or {}
        gap = record.get("approval_gap") or {}
        targets = ", ".join((record.get("acquisition") or {}).get("outreach_targets") or []) or "-"
        source_url = source.get("source_url")
        source_cell = f"[{source.get('domain')}]({source_url})" if source_url else source.get("domain") or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{record.get('common_name')}<br>`{record.get('artifact_id')}`",
                    targets,
                    f"`{record.get('request_type')}`",
                    f"{gap.get('checks_complete')}/{gap.get('checks_total')}",
                    source_cell,
                ]
            )
            + " |"
        )

    lines.extend(["", "## Reusable Permission Checklist", ""])
    for field in REQUIRED_PERMISSION_FIELDS:
        lines.append(f"- {field}")
    lines.extend(["", "## Message Templates", ""])
    for record in payload.get("records") or []:
        template = record.get("message_template") or {}
        lines.append(f"### {record.get('common_name')}")
        lines.append("")
        lines.append(f"Subject: {template.get('subject')}")
        lines.append("")
        lines.append("```text")
        for line in template.get("body_lines") or []:
            lines.append(line)
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    payload = build_payload()
    OUTREACH_PACKETS_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTREACH_PACKETS_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    REVIEW_PACK_PATH.write_text(markdown(payload), encoding="utf-8")
    print(f"Wrote {rel(OUTREACH_PACKETS_PATH)}")
    print(f"Wrote {rel(REVIEW_PACK_PATH)}")
    print(
        "Species media outreach packets: "
        f"{payload['summary']['species_records']} records, "
        f"{payload['summary']['outreach_target_count']} targets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
