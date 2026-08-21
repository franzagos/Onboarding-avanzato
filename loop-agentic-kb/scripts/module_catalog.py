#!/usr/bin/env python3
"""Canonical module catalog shared by the KB build and delivery scripts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Module:
    module_id: str
    filename: str
    title: str

    @property
    def is_markdown(self) -> bool:
        return self.filename.endswith(".md")

    @property
    def export_filename(self) -> str:
        stem = self.filename.rsplit(".", 1)[0]
        return f"{stem}.md"


MODULES = (
    Module("00", "00-agent-manifest.md", "Agent Manifest"),
    Module("01", "01-knowledge-base.md", "Knowledge Base"),
    Module("02", "02-product-message-map.md", "Product Message Map"),
    Module("03", "03-competitors.md", "Competitors"),
    Module("04", "04-personas.md", "Personas"),
    Module("05", "05-psychographics.md", "Psychographics"),
    Module("06", "06-pain-points.md", "Pain Points"),
    Module("07", "07-reviews-voc.md", "Reviews & Voice of Customer"),
    Module("08", "08-brand-voice.md", "Brand Voice"),
    Module("09", "09-tone-of-voice.md", "Tone of Voice"),
    Module("10", "10-lexicon.md", "Lexicon"),
    Module("11", "11-product-offer-registry.yaml", "Product & Offer Registry"),
    Module("12", "12-claims-proof-library.yaml", "Claims & Proof Library"),
    Module("13", "13-funnel-awareness-matrix.yaml", "Funnel & Awareness Matrix"),
    Module("14", "14-creative-strategy-library.yaml", "Creative Strategy Library"),
    Module("15", "15-meta-ads-brief.yaml", "Meta Ads Brief"),
    Module("16", "16-google-ads-playbook.md", "Google Ads Playbook"),
    Module("17", "17-landing-page-map.yaml", "Landing Page Map"),
    Module("18", "18-asset-library.yaml", "Asset Library"),
    Module("19", "19-market-packs", "Market Packs"),
    Module("20", "20-measurement-framework.yaml", "Measurement Framework"),
    Module("21", "21-experiment-memory.yaml", "Experiment Memory"),
)

MODULE_BY_ID = {module.module_id: module for module in MODULES}
MODULE_BY_FILENAME = {module.filename: module for module in MODULES}

PROFILES = {
    "onboarding": tuple(f"{number:02d}" for number in range(0, 11)),
    "meta": (
        "00", "01", "02", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "17", "18", "20",
    ),
    "google": (
        "00", "01", "02", "04", "06", "07", "10", "11", "12", "13",
        "16", "17", "18", "20",
    ),
    "activation": tuple(f"{number:02d}" for number in range(0, 21)),
    "full": tuple(f"{number:02d}" for number in range(0, 22)),
}

CORE_FILES = (
    "sources.yaml",
    "evidence-ledger.yaml",
    "assumptions-and-gaps.yaml",
    "context-pack.yaml",
    "brand-database.yaml",
    "qa-report.yaml",
)

FULL_SUPPORT_FILES = ("strategic-summary.md", "review-checklist.yaml")


def normalize_module_id(value: str) -> str:
    candidate = value.strip()
    if candidate.isdigit():
        candidate = f"{int(candidate):02d}"
    if candidate in MODULE_BY_ID:
        return candidate
    if candidate in MODULE_BY_FILENAME:
        return MODULE_BY_FILENAME[candidate].module_id
    raise ValueError(f"unknown module: {value}")


def select_module_ids(profile: str, requested: list[str] | None = None) -> tuple[str, ...]:
    if profile == "custom":
        if not requested:
            raise ValueError("--modules is required with --profile custom")
        selected = {normalize_module_id(value) for value in requested}
        selected.add("00")
        return tuple(module.module_id for module in MODULES if module.module_id in selected)
    if requested:
        raise ValueError("--modules can only be used with --profile custom")
    try:
        return PROFILES[profile]
    except KeyError as error:
        raise ValueError(f"unknown profile: {profile}") from error


def selected_modules(profile: str, requested: list[str] | None = None) -> tuple[Module, ...]:
    ids = set(select_module_ids(profile, requested))
    return tuple(module for module in MODULES if module.module_id in ids)
