"""Render badges to URLs, Markdown, README blocks, JSON and llms.txt."""

from __future__ import annotations

import base64
import re
from typing import Any
from urllib.parse import quote

from .models import Badge, Catalog

MAX_BADGE_URL_LENGTH = 3000
REPO = "pawang-ai/markdown-badges-collection"
SITE = "https://pawang-ai.github.io/markdown-badges-collection/"


def escape_label(text: str) -> str:
    """Escape a badge label for a Shields.io static-badge path segment."""
    text = text.replace("-", "--").replace("_", "__")
    return quote(text, safe="-_.~!*'()")


def logo_param(badge: Badge, catalog: Catalog) -> str:
    """Return the value for the ``logo=`` query parameter."""
    if badge.source == "custom" and badge.logo_file:
        svg = (catalog.root / badge.logo_file).read_bytes()
        return "data:image/svg+xml;base64," + base64.b64encode(svg).decode("ascii")
    return badge.slug


def badge_url(badge: Badge, catalog: Catalog, style: str | None = None) -> str:
    """Build the Shields.io URL for ``badge``.

    The logo value is percent-encoded: a raw ``+`` in a query string is read as a space, which
    would corrupt a base64 data URI. Shields.io cannot recolor custom logos, so ``logoColor`` is
    only sent for Simple Icons logos (custom logos have their color baked into the SVG).
    """
    logo = quote(logo_param(badge, catalog), safe="")
    url = f"https://img.shields.io/badge/{escape_label(badge.name)}-{badge.hex.upper()}?logo={logo}"
    if badge.source != "custom":
        url += f"&logoColor={badge.logo_color}"
    return f"{url}&style={style}" if style else url


def badge_markdown(badge: Badge, catalog: Catalog) -> str:
    """Return the copy-paste Markdown snippet for ``badge``."""
    return f"[![{badge.name}]({badge_url(badge, catalog)})](#)"


def render_tables(catalog: Catalog, lang: str) -> str:
    """Render all categories as Markdown tables in ``lang`` (``en`` or ``id``)."""
    code_header = "Kode Markdown" if lang == "id" else "Markdown Code"
    top = "Kembali ke atas" if lang == "id" else "Back to top"
    parts: list[str] = []
    for cat in catalog.categories:
        items = catalog.badges_in(cat.id)
        if not items:
            continue
        parts += [f"### {cat.name(lang)}", "", f"| Preview | {code_header} |", "| --- | --- |"]
        for b in items:
            md = badge_markdown(b, catalog)
            parts.append(f"| {md} | `{md}` |")
        parts += [
            "",
            f"[{top} ⬆️](#table-of-contents)" if lang == "en" else f"[{top} ⬆️](#daftar-isi)",
            "",
        ]
    return "\n".join(parts).rstrip() + "\n"


def render_toc(catalog: Catalog, lang: str) -> str:
    """Render a linked list of non-empty categories."""
    lines = []
    for cat in catalog.categories:
        count = len(catalog.badges_in(cat.id))
        if count:
            name = cat.name(lang)
            anchor = re.sub(r"[^\w\s-]", "", name.lower()).strip().replace(" ", "-")
            lines.append(f"- [{name}](#{anchor}) ({count})")
    return "\n".join(lines) + "\n"


def render_stats(catalog: Catalog, lang: str) -> str:
    """Return a one-line summary of badge and category counts."""
    cats = sum(1 for c in catalog.categories if catalog.badges_in(c.id))
    if lang == "id":
        return f"{len(catalog.badges)} badge dalam {cats} kategori"
    return f"{len(catalog.badges)} badges in {cats} categories"


def inject(text: str, name: str, content: str) -> str:
    """Replace the content between ``<!-- name:START -->`` and ``<!-- name:END -->``.

    Raises:
        ValueError: If either marker is missing.
    """
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise ValueError(f"Markers {start} / {end} not found")
    return pattern.sub(lambda _m: f"{start}\n{content.strip()}\n{end}", text, count=1)


def to_json(catalog: Catalog) -> list[dict[str, Any]]:
    """Return the catalog as JSON-serializable records (used for ``docs/badges.json``)."""
    records = []
    for cat in catalog.categories:
        for b in catalog.badges_in(cat.id):
            records.append(
                {
                    "id": b.id,
                    "name": b.name,
                    "category": cat.id,
                    "category_name": {"en": cat.name_en, "id": cat.name_id},
                    "slug": b.slug,
                    "hex": b.hex.upper(),
                    "logo_color": b.logo_color,
                    "source": b.source,
                    "url": badge_url(b, catalog),
                    "markdown": badge_markdown(b, catalog),
                }
            )
    return records


def render_llms_txt(catalog: Catalog) -> str:
    """Render a ``llms.txt`` summary so AI crawlers can understand the project."""
    lines = [
        "# markdown-badges-collection",
        "",
        "> Copy-paste Shields.io badges for GitHub README and profile: tech, framework and "
        "tool badges with official brand colors and logos from Simple Icons and devicon.",
        "",
        f"This catalog has {render_stats(catalog, 'en')}. Each badge is a static Shields.io "
        "badge: `https://img.shields.io/badge/<Name>-<HEX>"
        "?logo=<simple-icons-slug>&logoColor=<white|black>`. "
        "Badges whose logo is missing from Simple Icons embed a single-color SVG from devicon as a "
        "base64 data URI instead.",
        "",
        "## Resources",
        f"- [Searchable catalog]({SITE}): browse, filter and copy badges",
        f"- [badges.json]({SITE}badges.json): machine-readable list of all badges",
        f"- [README (English)](https://github.com/{REPO}/blob/main/README.md)",
        f"- [README (Bahasa Indonesia)](https://github.com/{REPO}/blob/main/README.id.md)",
        "",
        "## Categories",
    ]
    for cat in catalog.categories:
        count = len(catalog.badges_in(cat.id))
        if count:
            lines.append(f"- {cat.name_en}: {count}")
    lines += ["", "## License", "MIT. Logos and brand names belong to their respective owners.", ""]
    return "\n".join(lines)
