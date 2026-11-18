"""Command-line interface: ``badgekit build | check | validate | probe | stats``."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import __version__
from .loader import load_catalog
from .models import Catalog, DataError
from .probe import SHIELDS, probe_catalog
from .render import (
    inject,
    render_llms_txt,
    render_stats,
    render_tables,
    render_toc,
    to_json,
)
from .validate import load_simple_icons_slugs, validate

logger = logging.getLogger("badgekit")

READMES = {"en": "README.md", "id": "README.id.md"}
# GitHub stops rendering a README after 500 KiB; fail well before that.
README_MAX_BYTES = 450 * 1024


def build_outputs(root: Path, catalog: Catalog) -> dict[Path, str]:
    """Compute the new content of every generated file, keyed by path."""
    outputs: dict[Path, str] = {}
    for lang, filename in READMES.items():
        path = root / filename
        text = path.read_text(encoding="utf-8")
        text = inject(text, "STATS", render_stats(catalog, lang))
        text = inject(text, "TOC", render_toc(catalog, lang))
        text = inject(text, "BADGES", render_tables(catalog, lang))
        outputs[path] = text
    outputs[root / "docs" / "badges.json"] = (
        json.dumps(to_json(catalog), indent=2, ensure_ascii=False) + "\n"
    )
    outputs[root / "docs" / "llms.txt"] = render_llms_txt(catalog)
    return outputs


def _load(root: Path) -> Catalog:
    return load_catalog(root / "data" / "badges.yml")


def cmd_build(root: Path) -> int:
    """Regenerate README files and docs assets."""
    outputs = build_outputs(root, _load(root))
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        logger.info("wrote %s", path.relative_to(root))
    return 0


def cmd_validate(root: Path, simple_icons: str | None) -> int:
    """Validate the catalog and print any problems."""
    catalog = _load(root)
    slugs = load_simple_icons_slugs(simple_icons) if simple_icons else None
    errors = validate(catalog, slugs)
    for err in errors:
        logger.error(err)
    if errors:
        logger.error("%d problem(s) found", len(errors))
        return 1
    logger.info(
        "OK: %d badges valid%s", len(catalog.badges), "" if slugs else " (slugs not checked)"
    )
    return 0


def cmd_check(root: Path, simple_icons: str | None) -> int:
    """Validate and verify generated files are up to date (for CI)."""
    code = cmd_validate(root, simple_icons)
    outputs = build_outputs(root, _load(root))
    stale = [
        p.relative_to(root)
        for p, content in outputs.items()
        if not p.exists() or p.read_text(encoding="utf-8") != content
    ]
    for p in stale:
        logger.error("%s is out of date; run `badgekit build`", p)
    too_big = [
        (p.relative_to(root), len(c.encode()))
        for p, c in outputs.items()
        if p.name in READMES.values() and len(c.encode()) > README_MAX_BYTES
    ]
    for p, size in too_big:
        logger.error(
            "%s is %d KiB (limit %d KiB); move the catalog out of the README",
            p,
            size // 1024,
            README_MAX_BYTES // 1024,
        )
    return 1 if code or stale or too_big else 0


def cmd_probe(root: Path, args: argparse.Namespace) -> int:
    """Ask Shields.io to render every badge and confirm each one shows its logo."""
    catalog = _load(root)
    checked, failures = probe_catalog(
        catalog, base_url=args.base_url, only=args.only, limit=args.limit, workers=args.workers
    )
    for f in failures:
        logger.error("%s: %s", f.badge_id, f.reason)
    logger.info(
        "probed %d badges: %d ok, %d failed", checked, checked - len(failures), len(failures)
    )
    return 1 if failures else 0


def cmd_stats(root: Path) -> int:
    """Print badge counts per category."""
    catalog = _load(root)
    print(render_stats(catalog, "en"))
    for cat in catalog.categories:
        print(f"  {cat.name_en}: {len(catalog.badges_in(cat.id))}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(prog="badgekit", description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="regenerate README files and docs/")
    sub.add_parser("stats", help="show counts per category")
    for name, text in (
        ("validate", "validate data/badges.yml"),
        ("check", "validate + verify outputs"),
    ):
        p = sub.add_parser(name, help=text)
        p.add_argument("--simple-icons", help="path or https URL of simple-icons.json")
    pr = sub.add_parser("probe", help="render every badge on Shields.io and check the logo shows")
    pr.add_argument("--only", choices=["simple-icons", "custom"], help="probe one logo source")
    pr.add_argument("--limit", type=int, help="probe only the first N badges")
    pr.add_argument("--workers", type=int, default=6)
    pr.add_argument("--base-url", default=SHIELDS, help="use a different Shields.io server")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        if args.command == "build":
            return cmd_build(args.root)
        if args.command == "validate":
            return cmd_validate(args.root, args.simple_icons)
        if args.command == "check":
            return cmd_check(args.root, args.simple_icons)
        if args.command == "probe":
            return cmd_probe(args.root, args)
        return cmd_stats(args.root)
    except (DataError, ValueError, OSError) as exc:
        logger.error("error: %s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
