#!/usr/bin/env python3
"""Render canonical KB modules as standalone Markdown deliverables."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from module_catalog import MODULE_BY_ID, MODULES, Module, normalize_module_id


RENDERER_VERSION = "1.0"
INTERNAL_ROOTS = {"meta", "standalone_context", "module_quality"}


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def scalar(text: str, key: str, default: str = "—") -> str:
    match = re.search(rf'(?m)^\s+{re.escape(key)}:\s*(.+?)\s*$', text)
    if not match:
        return default
    value = match.group(1).strip().strip('"\'')
    return value if value not in {"", "null", "[]", "{}"} else default


def top_level_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^([A-Za-z_][A-Za-z0-9_-]*):(?:\s.*)?$", text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[match.start():end].rstrip()))
    return blocks


def block_by_name(text: str, name: str) -> str:
    return next((body for key, body in top_level_blocks(text) if key == name), "")


def humanize(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").strip().title()


def render_yaml(module: Module, source: Path, text: str) -> str:
    meta = block_by_name(text, "meta")
    context = block_by_name(text, "standalone_context")
    quality = block_by_name(text, "module_quality")
    content_blocks = [
        (name, body) for name, body in top_level_blocks(text) if name not in INTERNAL_ROOTS
    ]
    lines = [
        "---",
        'schema_version: "2.1"',
        f'module_id: "MOD-{module.module_id}"',
        f'source_file: "{module.filename}"',
        f'source_sha256: "{hashlib.sha256(text.encode()).hexdigest()}"',
        "---",
        "",
        f"# {module.module_id} — {module.title}",
        "",
        "## Stato del modulo",
        "",
        f"- Brand: {scalar(meta, 'brand_id')}",
        f"- Stato: {scalar(meta, 'status')}",
        f"- Generato il: {scalar(meta, 'generated_at')}",
        f"- Ultima revisione: {scalar(meta, 'last_reviewed_at')}",
        "",
        "## Contesto autonomo",
        "",
        f"- Sintesi brand: {scalar(context, 'brand_summary')}",
        f"- Ambito: {scalar(context, 'scope')}",
        f"- Mercati: {scalar(context, 'markets')}",
        f"- Lingue: {scalar(context, 'languages')}",
        f"- Aggiornato al: {scalar(context, 'as_of')}",
        f"- Limiti: {scalar(context, 'limitations')}",
        f"- Input bloccanti: {scalar(context, 'blocking_input_ids')}",
        "",
        "## Quality gate",
        "",
        "| Dimensione | Stato |",
        "|---|---|",
    ]
    for dimension in (
        "coverage", "evidence", "depth", "actionability", "standalone_usability",
        "consistency", "freshness", "overall",
    ):
        lines.append(f"| {humanize(dimension)} | {scalar(quality, dimension)} |")

    if not content_blocks:
        lines.extend(["", "## Contenuto", "", "Nessun record disponibile."])
    for name, body in content_blocks:
        lines.extend([
            "",
            f"## {humanize(name)}",
            "",
            "```yaml",
            body,
            "```",
        ])
    lines.extend([
        "",
        "---",
        "",
        f"Fonte canonica: `{source.name}`. Questo file è una vista Markdown derivata; modificare la fonte canonica e rigenerare l'export.",
        "",
    ])
    return "\n".join(lines)


def render_one(root: Path, module: Module, output_dir: Path, force: bool = False) -> tuple[list[Path], bool]:
    source = root / module.filename
    if module.filename == "19-market-packs":
        written: list[Path] = []
        market_output = output_dir / module.filename
        market_output.mkdir(parents=True, exist_ok=True)
        if not source.is_dir():
            return written, False
        changed = False
        for market_file in sorted(source.glob("*.md")):
            target = market_output / market_file.name
            content = market_file.read_text(encoding="utf-8")
            if force or not target.exists() or target.read_text(encoding="utf-8") != content:
                target.write_text(content, encoding="utf-8")
                changed = True
            written.append(target)
        return written, changed
    if not source.is_file():
        raise FileNotFoundError(f"missing canonical module: {source}")

    text = source.read_text(encoding="utf-8")
    rendered = text if module.is_markdown else render_yaml(module, source, text)
    target = output_dir / module.export_filename
    target.parent.mkdir(parents=True, exist_ok=True)
    changed = force or not target.exists() or target.read_text(encoding="utf-8") != rendered
    if changed:
        target.write_text(rendered, encoding="utf-8")
    return [target], changed


def manifest_module_ids(root: Path) -> list[str]:
    manifest = load_json(root / "kb-manifest.json", {})
    return [str(item["id"]) for item in manifest.get("modules", []) if "id" in item]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--module", action="append", dest="modules")
    selection.add_argument("--all", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = args.path.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    output_dir = (args.output or root / "exports" / "modules").expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.modules:
            ids = [normalize_module_id(value) for value in args.modules]
        elif args.all:
            ids = [module.module_id for module in MODULES if (root / module.filename).exists()]
        else:
            ids = manifest_module_ids(root)
            if not ids:
                parser.error("no module selected and kb-manifest.json is missing or empty")
    except ValueError as error:
        parser.error(str(error))

    rendered_count = 0
    skipped_count = 0
    outputs: list[str] = []
    for module_id in ids:
        try:
            paths, changed = render_one(root, MODULE_BY_ID[module_id], output_dir, args.force)
        except FileNotFoundError as error:
            print(f"ERROR: {error}")
            return 1
        outputs.extend(str(path) for path in paths)
        rendered_count += int(changed)
        skipped_count += int(not changed)

    state = {
        "renderer_version": RENDERER_VERSION,
        "modules": ids,
        "outputs": outputs,
    }
    (output_dir.parent / "render-manifest.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Markdown exports: {output_dir}")
    print(f"Rendered: {rendered_count}; unchanged: {skipped_count}; files: {len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
