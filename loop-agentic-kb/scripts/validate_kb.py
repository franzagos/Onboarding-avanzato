#!/usr/bin/env python3
"""Validate Loop Agentic KB structure without external dependencies."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


FULL_REQUIRED = [
    "00-agent-manifest.md", "01-knowledge-base.md", "11-product-offer-registry.yaml",
    "12-claims-proof-library.yaml", "13-funnel-awareness-matrix.md",
    "14-creative-strategy-library.md", "15-meta-ads-brief.md",
    "16-google-ads-playbook.md", "17-landing-page-map.md",
    "18-asset-library.yaml", "19-market-packs", "20-measurement-framework.md",
    "21-experiment-memory.yaml", "sources.md", "assumptions-and-gaps.md",
]

NUCLEUS_REQUIRED = [
    "00-agent-manifest.md", "11-product-offer-registry.yaml",
    "12-claims-proof-library.yaml", "15-meta-ads-brief.md",
    "16-google-ads-playbook.md", "17-landing-page-map.md",
    "20-measurement-framework.md", "sources.md",
    "assumptions-and-gaps.md",
]

COMPATIBLE_MODULES = [
    ("product message map", ["02-product-message-map.md", "01a-product-message-map.md"]),
    ("competitors", ["03-competitors.md", "02-competitors.md"]),
    ("personas", ["04-personas.md", "03-personas.md"]),
    ("psychographics", ["05-psychographics.md", "04-psychographics.md"]),
    ("pain points", ["06-pain-points.md", "05-pain-points.md"]),
    ("reviews VOC", ["07-reviews-voc.md", "06-reviews-voc.md"]),
    ("brand voice", ["08-brand-voice.md", "07-brand-voice.md"]),
    ("tone of voice", ["09-tone-of-voice.md", "07a-tone-of-voice.md"]),
    ("lexicon", ["10-lexicon.md", "07b-lessico.md"]),
    ("context pack", ["context-pack.yaml", "seletti-context-pack.yaml"]),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--mode", choices=["full", "nucleus"], default="full")
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

    compatible = COMPATIBLE_MODULES if args.mode == "full" else [COMPATIBLE_MODULES[-1]]
    for label, alternatives in compatible:
        if not any((root / name).exists() for name in alternatives):
            errors.append(f"missing {label}; accepted: {', '.join(alternatives)}")

    for path in root.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.lstrip().startswith("#"):
            errors.append(f"missing heading: {path.name}")
        if "Da compilare." in text:
            warnings.append(f"placeholder remains: {path.name}")

    for path in root.glob("*.yaml"):
        text = path.read_text(encoding="utf-8")
        if "\t" in text:
            errors.append(f"tab indentation in YAML: {path.name}")
        if not re.search(r"(?m)^(meta:|brand:|products:|claims:|assets:|experiments:)", text):
            warnings.append(f"unrecognized YAML root: {path.name}")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    print(f"Validation complete ({args.mode}): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

