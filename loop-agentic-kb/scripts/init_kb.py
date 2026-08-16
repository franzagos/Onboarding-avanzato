#!/usr/bin/env python3
"""Create the deterministic folder skeleton for a Loop Agentic KB."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re


MODULES = [
    ("00-agent-manifest.md", "Agent Manifest"),
    ("01-knowledge-base.md", "Knowledge Base"),
    ("02-product-message-map.md", "Product Message Map"),
    ("03-competitors.md", "Competitors"),
    ("04-personas.md", "Personas"),
    ("05-psychographics.md", "Psychographics"),
    ("06-pain-points.md", "Pain Points"),
    ("07-reviews-voc.md", "Reviews & Voice of Customer"),
    ("08-brand-voice.md", "Brand Voice"),
    ("09-tone-of-voice.md", "Tone of Voice"),
    ("10-lexicon.md", "Lexicon"),
    ("13-funnel-awareness-matrix.md", "Funnel & Awareness Matrix"),
    ("14-creative-strategy-library.md", "Creative Strategy Library"),
    ("15-meta-ads-brief.md", "Meta Ads Brief"),
    ("16-google-ads-playbook.md", "Google Ads Playbook"),
    ("17-landing-page-map.md", "Landing Page Map"),
    ("20-measurement-framework.md", "Measurement Framework"),
    ("sources.md", "Source Registry"),
    ("assumptions-and-gaps.md", "Assumptions and Gaps"),
]

YAML_FILES = [
    "11-product-offer-registry.yaml",
    "12-claims-proof-library.yaml",
    "18-asset-library.yaml",
    "21-experiment-memory.yaml",
    "context-pack.yaml",
]


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "brand"


def write_new(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    root = args.output.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "19-market-packs").mkdir(exist_ok=True)

    today = date.today().isoformat()
    for filename, title in MODULES:
        write_new(
            root / filename,
            f"# {args.brand} — {title}\n\n"
            "## Stato\n\n- Status: draft\n- Readiness: not_assessed\n\n"
            "## Scopo\n\nDa compilare.\n\n"
            "## Evidenze\n\nDa compilare.\n\n"
            "## Inferenze e ipotesi\n\nDa compilare.\n\n"
            "## Gap\n\nDa compilare.\n\n"
            "## Handoff\n\nDa compilare.\n",
        )

    write_new(root / "19-market-packs" / ".gitkeep", "")
    for filename in YAML_FILES:
        write_new(
            root / filename,
            f'meta:\n  brand: "{args.brand}"\n  brand_id: "{slugify(args.brand)}"\n'
            f'  created_at: "{today}"\n  status: "draft"\nitems: []\n',
        )

    print(f"Created KB skeleton: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

