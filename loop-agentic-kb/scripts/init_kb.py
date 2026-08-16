#!/usr/bin/env python3
"""Create the canonical v2 folder skeleton for a Loop Agentic KB."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re


MARKDOWN_MODULES = [
    ("00-agent-manifest.md", "00", "Agent Manifest"),
    ("01-knowledge-base.md", "01", "Knowledge Base"),
    ("02-product-message-map.md", "02", "Product Message Map"),
    ("03-competitors.md", "03", "Competitors"),
    ("04-personas.md", "04", "Personas"),
    ("05-psychographics.md", "05", "Psychographics"),
    ("06-pain-points.md", "06", "Pain Points"),
    ("07-reviews-voc.md", "07", "Reviews & Voice of Customer"),
    ("08-brand-voice.md", "08", "Brand Voice"),
    ("09-tone-of-voice.md", "09", "Tone of Voice"),
    ("10-lexicon.md", "10", "Lexicon"),
    ("16-google-ads-playbook.md", "16", "Google Ads Playbook"),
    ("strategic-summary.md", "SUMMARY", "Strategic Summary"),
]

TEMPLATE_FILES = {
    "11-product-offer-registry.yaml": "product-offer-registry-template.yaml",
    "12-claims-proof-library.yaml": "claims-proof-template.yaml",
    "18-asset-library.yaml": "asset-library-template.yaml",
    "21-experiment-memory.yaml": "experiment-memory-template.yaml",
    "sources.yaml": "sources-template.yaml",
    "evidence-ledger.yaml": "evidence-ledger-template.yaml",
    "assumptions-and-gaps.yaml": "assumptions-gaps-template.yaml",
}

GENERIC_YAML = {
    "13-funnel-awareness-matrix.yaml": "funnel_records: []\n",
    "14-creative-strategy-library.yaml": "creative_angles: []\n",
    "15-meta-ads-brief.yaml": "meta_briefs: []\n",
    "17-landing-page-map.yaml": "landing_pages: []\nintent_routes: []\n",
    "20-measurement-framework.yaml": "objectives: []\nmetrics: []\nevents: []\n",
    "context-pack.yaml": "generated_from: []\nentity_ids: {}\n",
    "review-checklist.yaml": "review_items: []\n",
    "qa-report.yaml": "issues: []\nvalidation_summary: null\n",
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "brand"


def write_new(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def meta(brand_id: str, today: str, source_of_truth: bool = False) -> str:
    truth = "true" if source_of_truth else "false"
    return (
        "meta:\n"
        '  schema_version: "2.0"\n'
        f'  brand_id: "{brand_id}"\n'
        f'  generated_at: "{today}"\n'
        "  last_reviewed_at: null\n"
        '  status: "draft"\n'
        f"  source_of_truth: {truth}\n"
    )


def markdown(brand: str, brand_id: str, module_id: str, title: str, today: str) -> str:
    return (
        "---\n"
        'schema_version: "2.0"\n'
        f'module_id: "MOD-{module_id.lower()}"\n'
        f'brand_id: "{brand_id}"\n'
        f'generated_at: "{today}"\n'
        'status: "draft"\n'
        "source_ids: []\n"
        "evidence_ids: []\n"
        "blocking_input_ids: []\n"
        "---\n\n"
        f"# {module_id} — {brand}: {title}\n\n"
        "## Scopo e decisione supportata\n\nDa compilare.\n\n"
        "## Stato e readiness\n\nDa compilare.\n\n"
        "## Risultati\n\nDa compilare.\n\n"
        "## Evidenze\n\nDa compilare.\n\n"
        "## Inferenze e ipotesi\n\nDa compilare.\n\n"
        "## Gap e input bloccanti\n\nDa compilare.\n\n"
        "## Implicazioni e handoff\n\nDa compilare.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    root = args.output.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "19-market-packs").mkdir(exist_ok=True)

    today = date.today().isoformat()
    brand_id = slugify(args.brand)
    created: list[str] = []
    skipped: list[str] = []

    def emit(relative: str, content: str) -> None:
        target = root / relative
        (created if write_new(target, content) else skipped).append(relative)

    for filename, module_id, title in MARKDOWN_MODULES:
        emit(filename, markdown(args.brand, brand_id, module_id, title, today))

    assets = Path(__file__).resolve().parent.parent / "assets"
    for filename, template_name in TEMPLATE_FILES.items():
        content = (assets / template_name).read_text(encoding="utf-8")
        content = content.replace("{{BRAND_ID}}", brand_id).replace("{{DATE}}", today)
        emit(filename, content)

    for filename, body in GENERIC_YAML.items():
        emit(filename, meta(brand_id, today) + body)

    print(f"KB skeleton: {root}")
    print(f"Created ({len(created)}): {', '.join(created) if created else 'none'}")
    print(f"Skipped existing ({len(skipped)}): {', '.join(skipped) if skipped else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
