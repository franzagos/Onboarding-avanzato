#!/usr/bin/env python3
"""Validate the canonical v2 structure and referential integrity of a Loop Agentic KB."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


FULL_REQUIRED = [
    "00-agent-manifest.md", "01-knowledge-base.md", "02-product-message-map.md",
    "03-competitors.md", "04-personas.md", "05-psychographics.md",
    "06-pain-points.md", "07-reviews-voc.md", "08-brand-voice.md",
    "09-tone-of-voice.md", "10-lexicon.md", "11-product-offer-registry.yaml",
    "12-claims-proof-library.yaml", "13-funnel-awareness-matrix.yaml",
    "14-creative-strategy-library.yaml", "15-meta-ads-brief.yaml",
    "16-google-ads-playbook.md", "17-landing-page-map.yaml",
    "18-asset-library.yaml", "19-market-packs", "20-measurement-framework.yaml",
    "21-experiment-memory.yaml", "sources.yaml", "evidence-ledger.yaml",
    "assumptions-and-gaps.yaml", "context-pack.yaml", "strategic-summary.md",
    "brand-database.yaml", "review-checklist.yaml", "qa-report.yaml",
]

NUCLEUS_REQUIRED = [
    "00-agent-manifest.md", "11-product-offer-registry.yaml",
    "12-claims-proof-library.yaml", "15-meta-ads-brief.yaml",
    "16-google-ads-playbook.md", "17-landing-page-map.yaml",
    "18-asset-library.yaml", "20-measurement-framework.yaml",
    "sources.yaml", "evidence-ledger.yaml", "assumptions-and-gaps.yaml",
    "context-pack.yaml", "brand-database.yaml", "qa-report.yaml",
]

EXPECTED_ROOTS = {
    "11-product-offer-registry.yaml": ["products:", "offers:"],
    "12-claims-proof-library.yaml": ["claims:"],
    "13-funnel-awareness-matrix.yaml": ["funnel_records:"],
    "14-creative-strategy-library.yaml": ["creative_angles:"],
    "15-meta-ads-brief.yaml": ["meta_briefs:"],
    "17-landing-page-map.yaml": ["landing_pages:", "intent_routes:"],
    "18-asset-library.yaml": ["assets:"],
    "20-measurement-framework.yaml": ["objectives:", "metrics:", "events:"],
    "21-experiment-memory.yaml": ["experiments:"],
    "sources.yaml": ["sources:"],
    "evidence-ledger.yaml": ["evidence:"],
    "assumptions-and-gaps.yaml": ["assumptions:", "gaps:", "missing_inputs:"],
    "context-pack.yaml": ["generated_from:", "entity_ids:"],
    "review-checklist.yaml": ["review_items:"],
    "brand-database.yaml": ["database:"],
    "qa-report.yaml": ["issues:", "module_assessments:", "validation_summary:"],
}

LEGACY_FILES = {
    "01a-product-message-map.md", "02-competitors.md", "03-personas.md",
    "04-psychographics.md", "05-pain-points.md", "06-reviews-voc.md",
    "07-brand-voice.md", "07a-tone-of-voice.md", "07b-lessico.md",
    "13-funnel-awareness-matrix.md", "14-creative-strategy-library.md",
    "15-meta-ads-brief.md", "17-landing-page-map.md", "20-measurement-framework.md",
    "sources.md", "assumptions-and-gaps.md",
}

AUTHORITIES = {
    "source_ids": ("sources.yaml", "source_id", "SRC-"),
    "evidence_ids": ("evidence-ledger.yaml", "evidence_id", "EV-"),
    "product_ids": ("11-product-offer-registry.yaml", "product_id", "PROD-"),
    "offer_ids": ("11-product-offer-registry.yaml", "offer_id", "OFF-"),
    "claim_ids": ("12-claims-proof-library.yaml", "claim_id", "ACL-"),
    "asset_ids": ("18-asset-library.yaml", "asset_id", "AST-"),
    "experiment_ids": ("21-experiment-memory.yaml", "experiment_id", "EXP-"),
    "blocking_input_ids": ("assumptions-and-gaps.yaml", "input_id", "INP-"),
}

PLACEHOLDERS = [
    re.compile(r"Da compilare\."), re.compile(r"YYYY-MM-DD"),
    re.compile(r"\bto_define\b", re.I), re.compile(r"\b(?:TODO|TBD)\b"),
    re.compile(r"\b(?:SRC|EV|PROD|OFF|ACL|AST|EXP|INP)-000\b"),
]


def top_level_key_exists(text: str, key: str) -> bool:
    return re.search(rf"(?m)^{re.escape(key)}(?:\s|$)", text) is not None


def definitions(text: str, key: str) -> list[str]:
    pattern = re.compile(rf'(?m)^\s*-?\s*{re.escape(key)}:\s*["\']?([A-Z]+-[A-Za-z0-9-]+)')
    return pattern.findall(text)


def references(text: str, key: str) -> list[str]:
    found: list[str] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(rf"^(\s*){re.escape(key)}:\s*(.*)$", line)
        if not match:
            index += 1
            continue
        indent = len(match.group(1))
        rest = match.group(2)
        found.extend(re.findall(r"\b[A-Z]+-[A-Za-z0-9-]+\b", rest))
        index += 1
        while index < len(lines):
            next_line = lines[index]
            if not next_line.strip():
                index += 1
                continue
            next_indent = len(next_line) - len(next_line.lstrip())
            if next_indent <= indent:
                break
            found.extend(re.findall(r"\b[A-Z]+-[A-Za-z0-9-]+\b", next_line))
            index += 1
    return found


def record_blocks(text: str, id_key: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        rf'(?ms)^\s*-\s+{re.escape(id_key)}:\s*["\']?([A-Z]+-[A-Za-z0-9-]+)["\']?\s*$'
        rf'(.*?)(?=^\s*-\s+{re.escape(id_key)}:|\Z)'
    )
    return pattern.findall(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--mode", choices=["full", "nucleus"], default="full")
    parser.add_argument("--stage", choices=["draft", "review", "activation"], default="review")
    parser.add_argument("--compat-v1", action="store_true")
    args = parser.parse_args()

    root = args.path.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}")
        return 2

    required = FULL_REQUIRED if args.mode == "full" else NUCLEUS_REQUIRED
    for name in required:
        if not (root / name).exists():
            errors.append(f"missing: {name}")

    present_legacy = sorted(name for name in LEGACY_FILES if (root / name).exists())
    for name in present_legacy:
        message = f"legacy filename: {name}"
        (warnings if args.compat_v1 else errors).append(message)

    texts: dict[str, str] = {}
    for path in sorted(root.rglob("*.md")) + sorted(root.rglob("*.yaml")):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        texts[relative] = text
        if "\t" in text:
            errors.append(f"{relative}: tab indentation")
        for placeholder in PLACEHOLDERS:
            if placeholder.search(text):
                message = f"{relative}: placeholder remains ({placeholder.pattern})"
                (warnings if args.stage == "draft" else errors).append(message)

    for relative, text in texts.items():
        if relative.endswith(".yaml"):
            if not top_level_key_exists(text, "meta:"):
                errors.append(f"{relative}: missing meta root")
            if not re.search(r'(?m)^\s+schema_version:\s*["\']2\.1["\']?\s*$', text):
                errors.append(f"{relative}: missing schema_version 2.1")
            for expected in EXPECTED_ROOTS.get(relative, []):
                if not top_level_key_exists(text, expected):
                    errors.append(f"{relative}: missing root {expected}")
            for required_root in ("standalone_context:", "module_quality:"):
                if not top_level_key_exists(text, required_root):
                    errors.append(f"{relative}: missing root {required_root}")
            quality_match = re.search(
                r'(?ms)^module_quality:\s*\n(.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)', text
            )
            if quality_match:
                quality = quality_match.group(1)
                for dimension in (
                    "coverage", "evidence", "depth", "actionability",
                    "standalone_usability", "consistency", "freshness", "overall",
                ):
                    status_match = re.search(
                        rf'(?m)^\s+{dimension}:\s*["\']?(pass|conditional|fail)["\']?\s*$', quality
                    )
                    if not status_match:
                        errors.append(f"{relative}: module_quality missing/invalid {dimension}")
                    elif args.stage != "draft" and dimension == "overall" and status_match.group(1) != "pass":
                        errors.append(f"{relative}: module_quality.overall must be pass at {args.stage} stage")
        elif relative in {name for name, _, _ in [
            ("00-agent-manifest.md", "00", ""), ("01-knowledge-base.md", "01", ""),
            ("02-product-message-map.md", "02", ""), ("03-competitors.md", "03", ""),
            ("04-personas.md", "04", ""), ("05-psychographics.md", "05", ""),
            ("06-pain-points.md", "06", ""), ("07-reviews-voc.md", "07", ""),
            ("08-brand-voice.md", "08", ""), ("09-tone-of-voice.md", "09", ""),
            ("10-lexicon.md", "10", ""), ("16-google-ads-playbook.md", "16", ""),
        ]}:
            if not text.startswith("---\n") or 'schema_version: "2.1"' not in text[:500]:
                errors.append(f"{relative}: missing canonical frontmatter")
            expected_number = relative[:2]
            if not re.search(rf"(?m)^# {re.escape(expected_number)} \u2014 ", text):
                errors.append(f"{relative}: H1 number does not match filename")

    required_markdown_sections = (
        "## Executive summary", "## Scopo e decisione supportata",
        "## Contesto autonomo", "## Metodologia e coverage",
        "## Evidenze", "## Inferenze e ipotesi",
        "## Gap e input bloccanti", "## Implicazioni e handoff",
        "## Quality gate",
    )
    for relative, text in texts.items():
        if not relative.endswith(".md"):
            continue
        for section in required_markdown_sections:
            if section not in text:
                message = f"{relative}: missing standalone section {section}"
                (warnings if args.stage == "draft" else errors).append(message)
        frontmatter = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""
        if "module_quality:" not in frontmatter:
            errors.append(f"{relative}: missing module_quality in frontmatter")
        elif args.stage != "draft" and not re.search(r'(?m)^\s+overall:\s*["\']?pass["\']?\s*$', frontmatter):
            errors.append(f"{relative}: module_quality.overall must be pass at {args.stage} stage")

    database_text = texts.get("brand-database.yaml", "")
    for authority in (
        "sources.yaml", "evidence-ledger.yaml", "11-product-offer-registry.yaml",
        "12-claims-proof-library.yaml", "18-asset-library.yaml", "21-experiment-memory.yaml",
    ):
        if authority not in database_text:
            errors.append(f"brand-database.yaml: missing authority {authority}")

    known: dict[str, set[str]] = {}
    for ref_key, (authority, definition_key, prefix) in AUTHORITIES.items():
        authority_text = texts.get(authority, "")
        ids = definitions(authority_text, definition_key)
        known[ref_key] = set(ids)
        if len(ids) != len(set(ids)):
            errors.append(f"{authority}: duplicate {definition_key}")
        for item_id in ids:
            if not item_id.startswith(prefix):
                errors.append(f"{authority}: invalid prefix for {item_id}; expected {prefix}")

    for relative, text in texts.items():
        for ref_key, (_, _, prefix) in AUTHORITIES.items():
            for item_id in references(text, ref_key):
                if not item_id.startswith(prefix):
                    errors.append(f"{relative}: invalid {ref_key} value {item_id}; expected {prefix}")
                elif item_id not in known[ref_key]:
                    errors.append(f"{relative}: orphan {ref_key} reference {item_id}")
        for legacy_prefix in ("CL-", "AS-", "CR-", "FM-"):
            if re.search(rf"\b{re.escape(legacy_prefix)}[A-Za-z0-9-]+", text):
                errors.append(f"{relative}: legacy ID prefix {legacy_prefix}")

    gaps_text = texts.get("assumptions-and-gaps.yaml", "")
    for input_id, block in record_blocks(gaps_text, "input_id"):
        class_match = re.search(r'(?m)^\s+classification:\s*["\']?([a-z_]+)', block)
        classification = class_match.group(1) if class_match else None
        if classification not in {"non_blocking", "branch_blocking", "run_blocking"}:
            errors.append(f"assumptions-and-gaps.yaml: {input_id} invalid classification")
        prompt_match = re.search(r'(?m)^\s+request_text:\s*["\']([^"\']+)["\']', block)
        if not prompt_match or not prompt_match.group(1).startswith("Mi serve "):
            errors.append(f"assumptions-and-gaps.yaml: {input_id} request_text must start with 'Mi serve '")
        if classification in {"branch_blocking", "run_blocking"}:
            for required_field in ("required_for", "affected_modules", "reason", "minimum_acceptable"):
                if not re.search(rf"(?m)^\s+{required_field}:", block):
                    errors.append(f"assumptions-and-gaps.yaml: {input_id} missing {required_field}")

    claims_text = texts.get("12-claims-proof-library.yaml", "")
    for claim_id, block in record_blocks(claims_text, "claim_id"):
        if re.search(r'(?m)^\s+status:\s*["\']?approved_for_ads', block):
            for required_field in ("owner", "approved_at", "evidence_ids", "markets", "channels"):
                field_match = re.search(rf"(?m)^\s+{required_field}:\s*(.*)$", block)
                if not field_match or field_match.group(1).strip() in {"null", "[]", "\"\"", "''"}:
                    errors.append(f"12-claims-proof-library.yaml: {claim_id} approved without {required_field}")

    for message in sorted(set(errors)):
        print(f"ERROR: {message}")
    for message in sorted(set(warnings)):
        print(f"WARN: {message}")
    print(
        f"Validation complete ({args.mode}/{args.stage}): "
        f"{len(set(errors))} error(s), {len(set(warnings))} warning(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
