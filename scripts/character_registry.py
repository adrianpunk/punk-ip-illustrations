#!/usr/bin/env python3
"""Manage local Punk IP character packages with no external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MANIFEST_NAME = "character.json"
CURRENT_NAME = "current-character.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_slug(slug: str) -> None:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug must use lowercase letters, digits, and single hyphens")


def character_dir(root: Path, slug: str) -> Path:
    validate_slug(slug)
    return root.resolve() / "characters" / slug


def next_path(directory: Path, stem: str, suffix: str) -> Path:
    candidate = directory / f"{stem}{suffix}"
    if not candidate.exists():
        return candidate
    version = 2
    while True:
        candidate = directory / f"{stem}-v{version}{suffix}"
        if not candidate.exists():
            return candidate
        version += 1


def copy_versioned(source: Path, directory: Path, stem: str, required_suffix: str | None = None) -> Path:
    source = source.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Missing asset: {source}")
    suffix = required_suffix or source.suffix.lower()
    if not suffix:
        raise ValueError(f"Asset must have a file extension: {source}")
    if source.parent == directory.resolve() and source.name.startswith(stem) and source.suffix.lower() == suffix:
        return source
    destination = next_path(directory, stem, suffix)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source != destination:
        shutil.copy2(source, destination)
    return destination


def manifest_path(root: Path, slug: str) -> Path:
    return character_dir(root, slug) / MANIFEST_NAME


def resolved_manifest(root: Path, slug: str, allow_draft: bool = False) -> dict:
    directory = character_dir(root, slug)
    manifest = load_json(directory / MANIFEST_NAME)
    if manifest.get("status") != "confirmed" and not allow_draft:
        raise ValueError(f"Character '{slug}' is not confirmed")
    assets = manifest.get("assets", {})
    for key in ("sheet", "clean_reference", "spec"):
        value = assets.get(key)
        if not value:
            raise ValueError(f"Manifest is missing assets.{key}")
        path = Path(value)
        if not path.is_absolute():
            path = directory / path
        if not path.is_file():
            raise FileNotFoundError(f"Missing {key}: {path}")
        assets[key] = str(path.resolve())
    manifest["assets"] = assets
    manifest["manifest_path"] = str((directory / MANIFEST_NAME).resolve())
    return manifest


def command_register(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    directory = character_dir(root, args.slug)
    directory.mkdir(parents=True, exist_ok=True)
    old_path = directory / MANIFEST_NAME
    old = load_json(old_path) if old_path.exists() else {}

    sheet = copy_versioned(Path(args.sheet), directory, "character-sheet")
    clean = copy_versioned(Path(args.clean_reference), directory, "character-reference-clean")
    spec = copy_versioned(Path(args.spec), directory, "character-spec", ".md")

    now = utc_now()
    manifest = {
        "schema_version": 1,
        "slug": args.slug,
        "name": args.name,
        "status": "draft",
        "revision": int(old.get("revision", 0)) + 1,
        "created_at": old.get("created_at", now),
        "updated_at": now,
        "confirmed_at": None,
        "assets": {
            "sheet": sheet.name,
            "clean_reference": clean.name,
            "spec": spec.name,
        },
    }
    write_json(old_path, manifest)
    print(json.dumps(resolved_manifest(root, args.slug, allow_draft=True), ensure_ascii=False, indent=2))


def command_confirm(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    manifest = resolved_manifest(root, args.slug, allow_draft=True)
    path = manifest_path(root, args.slug)
    stored = load_json(path)
    now = utc_now()
    stored["status"] = "confirmed"
    stored["updated_at"] = now
    stored["confirmed_at"] = now
    write_json(path, stored)
    write_json(
        root / CURRENT_NAME,
        {
            "schema_version": 1,
            "slug": args.slug,
            "manifest": str(path.relative_to(root)),
            "updated_at": now,
        },
    )
    print(json.dumps(resolved_manifest(root, args.slug), ensure_ascii=False, indent=2))


def command_activate(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    manifest = resolved_manifest(root, args.slug)
    path = manifest_path(root, args.slug)
    write_json(
        root / CURRENT_NAME,
        {
            "schema_version": 1,
            "slug": args.slug,
            "manifest": str(path.relative_to(root)),
            "updated_at": utc_now(),
        },
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


def current_slug(root: Path) -> str:
    current = load_json(root / CURRENT_NAME)
    slug = current.get("slug")
    if not isinstance(slug, str):
        raise ValueError("current-character.json does not contain a valid slug")
    return slug


def command_resolve(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    slug = args.slug or current_slug(root)
    print(json.dumps(resolved_manifest(root, slug, allow_draft=args.allow_draft), ensure_ascii=False, indent=2))


def command_list(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    active = None
    try:
        active = current_slug(root)
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        pass
    result = []
    directory = root / "characters"
    if directory.is_dir():
        for path in sorted(directory.glob(f"*/{MANIFEST_NAME}")):
            try:
                item = load_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            result.append(
                {
                    "slug": item.get("slug"),
                    "name": item.get("name"),
                    "status": item.get("status"),
                    "revision": item.get("revision"),
                    "active": item.get("slug") == active,
                    "manifest_path": str(path.resolve()),
                }
            )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Punk IP character packages")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register = subparsers.add_parser("register", help="Copy generated assets into a draft character package")
    register.add_argument("--root", required=True)
    register.add_argument("--slug", required=True)
    register.add_argument("--name", required=True)
    register.add_argument("--sheet", required=True)
    register.add_argument("--clean-reference", required=True)
    register.add_argument("--spec", required=True)
    register.set_defaults(func=command_register)

    confirm = subparsers.add_parser("confirm", help="Confirm a draft character and make it active")
    confirm.add_argument("--root", required=True)
    confirm.add_argument("--slug", required=True)
    confirm.set_defaults(func=command_confirm)

    activate = subparsers.add_parser("activate", help="Make a confirmed character active")
    activate.add_argument("--root", required=True)
    activate.add_argument("--slug", required=True)
    activate.set_defaults(func=command_activate)

    resolve = subparsers.add_parser("resolve", help="Resolve an active or named character to absolute asset paths")
    resolve.add_argument("--root", required=True)
    resolve.add_argument("--slug")
    resolve.add_argument("--allow-draft", action="store_true")
    resolve.set_defaults(func=command_resolve)

    list_command = subparsers.add_parser("list", help="List local characters")
    list_command.add_argument("--root", required=True)
    list_command.set_defaults(func=command_list)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (FileNotFoundError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
