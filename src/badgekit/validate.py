"""Validate catalog integrity: duplicates, colors, categories and logo availability."""

from __future__ import annotations

import json
import logging
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from .models import HEX_RE, ID_RE, LOGO_COLORS, SOURCES, Catalog
from .render import MAX_BADGE_URL_LENGTH, badge_url

logger = logging.getLogger(__name__)


def load_simple_icons_slugs(location: str) -> set[str]:
    """Load the set of slugs from a Simple Icons ``simple-icons.json``.

    Args:
        location: A local file path or an ``https://`` URL.

    Raises:
        OSError: If the file cannot be read or the URL cannot be fetched.
    """
    if location.startswith("https://"):
        with urllib.request.urlopen(location, timeout=30) as resp:  # noqa: S310
            data = json.load(resp)
    else:
        data = json.loads(Path(location).read_text(encoding="utf-8"))
    return {item["slug"] for item in data}


MAX_SVG_BYTES = 20_000
_FORBIDDEN_TAGS = frozenset(
    {
        "script",
        "foreignobject",
        "image",
        "iframe",
        "style",
        "animate",
        "animatetransform",
        "set",
        "use",
    }
)


def check_svg(path: Path) -> list[str]:
    """Return problems that make an SVG unsafe or unsuitable as a Shields.io custom logo."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"cannot read {path.name}: {exc}"]
    problems: list[str] = []
    if len(data) > MAX_SVG_BYTES:
        problems.append(f"{path.name} is {len(data)} bytes (max {MAX_SVG_BYTES})")
    text = data.decode("utf-8", errors="replace")
    if re.search(r"<!(DOCTYPE|ENTITY)", text, re.IGNORECASE):
        return problems + [f"{path.name} must not declare a DOCTYPE or ENTITY"]
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return problems + [f"{path.name} is not valid XML: {exc}"]
    if not root.tag.endswith("}svg") and root.tag != "svg":
        problems.append(f"{path.name} root element is not <svg>")
    if "viewBox" not in root.attrib:
        problems.append(f"{path.name} needs a viewBox")
    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1].lower()
        if tag in _FORBIDDEN_TAGS:
            problems.append(f"{path.name} uses forbidden element <{tag}>")
        for attr, value in el.attrib.items():
            name = attr.rsplit("}", 1)[-1].lower()
            if name.startswith("on") or (name == "href" and not value.startswith("#")):
                problems.append(f"{path.name} has forbidden attribute {name!r}")
    return problems


def validate(catalog: Catalog, simple_icons: set[str] | None = None) -> list[str]:
    """Return a list of human-readable problems (empty if the catalog is valid)."""
    errors: list[str] = []
    category_ids = {c.id for c in catalog.categories}

    for label, values in (
        ("id", [b.id for b in catalog.badges]),
        ("name", [b.name.lower() for b in catalog.badges]),
        ("category id", [c.id for c in catalog.categories]),
    ):
        errors += [f"duplicate {label}: {v}" for v, n in Counter(values).items() if n > 1]

    slugs = Counter(b.slug for b in catalog.badges if b.source == "simple-icons")
    errors += [f"duplicate simple-icons slug: {s}" for s, n in slugs.items() if n > 1]

    for b in catalog.badges:
        where = f"[{b.id}]"
        if not ID_RE.match(b.id):
            errors.append(f"{where} id must be lowercase letters, digits and hyphens")
        if not HEX_RE.match(b.hex):
            errors.append(f"{where} hex must be 6 hex digits without '#', got {b.hex!r}")
        if b.logo_color not in LOGO_COLORS:
            errors.append(f"{where} logo_color must be one of {sorted(LOGO_COLORS)}")
        if b.category not in category_ids:
            errors.append(f"{where} unknown category {b.category!r}")
        if b.source not in SOURCES:
            errors.append(f"{where} source must be one of {sorted(SOURCES)}")
        elif b.source == "custom":
            if not b.logo_file:
                errors.append(f"{where} custom badges require logo_file")
            elif not (catalog.root / b.logo_file).is_file():
                errors.append(f"{where} logo_file not found: {b.logo_file}")
            else:
                errors += [f"{where} {p}" for p in check_svg(catalog.root / b.logo_file)]
        elif simple_icons is not None and b.slug not in simple_icons:
            errors.append(f"{where} slug {b.slug!r} not found in Simple Icons")
        if not any(e.startswith(where) for e in errors):
            length = len(badge_url(b, catalog))
            if length > MAX_BADGE_URL_LENGTH:
                errors.append(
                    f"{where} badge URL is {length} characters (max {MAX_BADGE_URL_LENGTH}); "
                    "use a simpler logo"
                )
    return errors
