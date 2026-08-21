#!/usr/bin/env python3
"""Build a deduplicated Markdown dossier from selected KB modules."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re

from module_catalog import MODULE_BY_ID, PROFILES, select_module_ids
from render_module import block_by_name, load_json, render_one, scalar


def remove_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


def remove_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^## {re.escape(heading)}\s*\n.*?(?=^## |\Z)"
    )
    return pattern.sub("", text).strip()


def demote_headings(text: str) -> str:
    return re.sub(r"(?m)^(#{1,5}) ", lambda match: f"{match.group(1)}# ", text)


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "kb"


def document_heading(path: Path, fallback: str) -> str:
    text = remove_frontmatter(path.read_text(encoding="utf-8"))
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1) if match else fallback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--profile", choices=["auto", *PROFILES, "custom"], default="auto")
    parser.add_argument("--modules", nargs="*")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--without-source-appendix", action="store_true")
    args = parser.parse_args()

    root = args.path.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    manifest = load_json(root / "kb-manifest.json", {})
    profile = manifest.get("profile", "full") if args.profile == "auto" else args.profile
    try:
        if args.profile == "auto":
            ids = tuple(str(item["id"]) for item in manifest.get("modules", []))
            if not ids:
                ids = select_module_ids("full")
        else:
            ids = select_module_ids(profile, args.modules)
    except ValueError as error:
        parser.error(str(error))

    brand = manifest.get("brand") or manifest.get("brand_id") or "Knowledge Base"
    brand_id = manifest.get("brand_id") or slug(str(brand))
    title = args.title or f"{brand} — Knowledge Base completa"
    output = args.output or root / "deliverables" / f"{brand_id}-{profile}-complete.md"
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    export_dir = root / "exports" / "modules"
    export_dir.mkdir(parents=True, exist_ok=True)
    module_files: list[tuple[str, str, Path]] = []
    for module_id in ids:
        module = MODULE_BY_ID[module_id]
        try:
            paths, _ = render_one(root, module, export_dir)
        except FileNotFoundError as error:
            print(f"ERROR: {error}")
            return 1
        for path in paths:
            module_files.append((module_id, module.title, path))

    database = (root / "brand-database.yaml").read_text(encoding="utf-8")
    db_meta = block_by_name(database, "meta")
    db_context = block_by_name(database, "standalone_context")
    lines = [
        f"# {title}",
        "",
        f"Generato il {date.today().isoformat()} dal package canonico `{brand_id}`.",
        "",
        "## Contesto globale",
        "",
        f"- Brand: {scalar(db_meta, 'brand_id', str(brand))}",
        f"- Profilo: {profile}",
        f"- Mercati: {scalar(db_context, 'markets')}",
        f"- Lingue: {scalar(db_context, 'languages')}",
        f"- Aggiornato al: {scalar(db_context, 'as_of')}",
        f"- Limiti generali: {scalar(db_context, 'limitations')}",
        "",
        "## Indice",
        "",
    ]
    for module_id, module_title, path in module_files:
        fallback = f"{module_id} — {module_title}"
        heading = document_heading(path, fallback)
        lines.append(f"- [{heading}](#{slug(heading)})")

    for module_id, module_title, path in module_files:
        content = remove_frontmatter(path.read_text(encoding="utf-8"))
        content = remove_section(content, "Contesto autonomo")
        content = demote_headings(content)
        lines.extend(["", "---", "", content.strip(), ""])

    if not args.without_source_appendix:
        for filename, heading in (
            ("sources.yaml", "Registro delle fonti"),
            ("assumptions-and-gaps.yaml", "Assunzioni, gap e input mancanti"),
        ):
            source = root / filename
            if source.exists():
                lines.extend([
                    "", "---", "", f"## {heading}", "", "```yaml",
                    source.read_text(encoding="utf-8").rstrip(), "```", "",
                ])

    content = "\n".join(lines).rstrip() + "\n"
    output.write_text(content, encoding="utf-8")
    build_manifest = {
        "schema_version": "1.0",
        "profile": profile,
        "module_ids": list(ids),
        "output": str(output),
        "sha256": hashlib.sha256(content.encode()).hexdigest(),
        "generated_at": date.today().isoformat(),
    }
    (output.parent / "build-manifest.json").write_text(
        json.dumps(build_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Final Markdown: {output}")
    print(f"Modules included: {len(module_files)}; bytes: {len(content.encode())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
