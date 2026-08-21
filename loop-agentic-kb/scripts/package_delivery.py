#!/usr/bin/env python3
"""Create a user-facing ZIP with the final dossier, module exports and canonical data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import zipfile

from module_catalog import CORE_FILES, MODULE_BY_ID, PROFILES


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--profile", choices=["auto", *PROFILES, "custom"], default="auto")
    parser.add_argument("--modules", nargs="*")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = args.path.expanduser().resolve()
    manifest_path = root / "kb-manifest.json"
    if not root.is_dir() or not manifest_path.exists():
        parser.error(f"invalid KB package: {root}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    profile = manifest.get("profile", "full") if args.profile == "auto" else args.profile
    brand_id = manifest.get("brand_id", "knowledge-base")

    build_script = Path(__file__).with_name("build_final_md.py")
    command = [sys.executable, str(build_script), str(root), "--profile", args.profile]
    if args.modules:
        command.extend(["--modules", *args.modules])
    result = subprocess.run(command, check=False, text=True, capture_output=True)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode

    build_manifest = json.loads((root / "deliverables" / "build-manifest.json").read_text(encoding="utf-8"))
    final_md = Path(build_manifest["output"])
    output = args.output or root / "deliverables" / f"{brand_id}-{profile}-delivery.zip"
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    canonical_files = [root / name for name in (*CORE_FILES, "review-checklist.yaml")]
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(final_md, f"deliverables/{final_md.name}")
        archive.write(manifest_path, "manifest/kb-manifest.json")
        archive.write(root / "deliverables" / "build-manifest.json", "manifest/build-manifest.json")
        for module_id in build_manifest["module_ids"]:
            module = MODULE_BY_ID[module_id]
            if module.filename == "19-market-packs":
                paths = sorted((root / "exports" / "modules" / module.filename).glob("*.md"))
            else:
                paths = [root / "exports" / "modules" / module.export_filename]
            for path in paths:
                if path.exists():
                    archive.write(path, f"modules/{path.relative_to(root / 'exports' / 'modules')}")
            canonical = root / module.filename
            if canonical.is_file() and canonical.suffix == ".yaml":
                archive.write(canonical, f"data/modules/{canonical.name}")
        for path in canonical_files:
            if path.exists():
                archive.write(path, f"data/{path.name}")

    print(result.stdout, end="")
    print(f"Delivery ZIP: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
