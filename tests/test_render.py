from pathlib import Path

import pytest

from badgekit.loader import load_catalog
from badgekit.render import (
    badge_markdown,
    badge_url,
    escape_label,
    inject,
    render_stats,
    render_tables,
    render_toc,
    to_json,
)


@pytest.mark.parametrize(
    ("raw", "escaped"),
    [
        ("Node-RED", "Node--RED"),
        ("Ant Design", "Ant%20Design"),
        ("snake_case", "snake__case"),
        (".NET", ".NET"),
    ],
)
def test_escape_label(raw: str, escaped: str) -> None:
    assert escape_label(raw) == escaped


def test_badge_url_and_markdown(repo: Path) -> None:
    catalog = load_catalog(repo / "data" / "badges.yml")
    zig = catalog.badges[0]
    assert (
        badge_url(zig, catalog)
        == "https://img.shields.io/badge/Zig-F7A41D?logo=zig&logoColor=black"
    )
    assert badge_url(zig, catalog, style="flat-square").endswith("&style=flat-square")
    assert badge_markdown(zig, catalog).startswith("[![Zig](https://img.shields.io/badge/Zig-")


def test_custom_logo_is_percent_encoded_without_logocolor(repo: Path) -> None:
    (repo / "assets" / "logos").mkdir(parents=True)
    (repo / "assets" / "logos" / "x.svg").write_text("<svg/>", encoding="utf-8")
    (repo / "data" / "badges.yml").write_text(
        "categories:\n  - {id: c, name_en: C, name_id: C}\nbadges:\n"
        "  - {id: x, name: X, slug: x, hex: '112233', category: c, source: custom,\n"
        "     logo_file: assets/logos/x.svg}\n",
        encoding="utf-8",
    )
    catalog = load_catalog(repo / "data" / "badges.yml")
    url = badge_url(catalog.badges[0], catalog)
    assert "logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2Zy8%2B" in url
    assert "+" not in url.split("logo=")[1]  # a raw '+' would be read as a space
    assert "logoColor" not in url  # Shields.io cannot recolor custom logos


def test_tables_are_localized_and_skip_empty_categories(repo: Path) -> None:
    catalog = load_catalog(repo / "data" / "badges.yml")
    en, idn = render_tables(catalog, "en"), render_tables(catalog, "id")
    assert "### Languages" in en and "Markdown Code" in en
    assert "### Bahasa" in idn and "Kode Markdown" in idn
    assert "Empty" not in en and "Kosong" not in idn
    assert en.index("Node-RED") < en.index("| [![Zig]")  # sorted by name


def test_toc_and_stats(repo: Path) -> None:
    catalog = load_catalog(repo / "data" / "badges.yml")
    assert render_toc(catalog, "en") == "- [Languages](#languages) (2)\n"
    assert render_stats(catalog, "en") == "2 badges in 1 categories"
    assert render_stats(catalog, "id") == "2 badge dalam 1 kategori"


def test_inject_replaces_and_is_idempotent() -> None:
    text = "a\n<!-- X:START -->\nold\n<!-- X:END -->\nb\n"
    once = inject(text, "X", "new")
    assert "old" not in once and "new" in once
    assert inject(once, "X", "new") == once


def test_inject_missing_marker() -> None:
    with pytest.raises(ValueError, match="not found"):
        inject("no markers", "X", "y")


def test_to_json(repo: Path) -> None:
    catalog = load_catalog(repo / "data" / "badges.yml")
    records = to_json(catalog)
    assert [r["id"] for r in records] == ["node-red", "zig"]
    assert records[1]["category_name"] == {"en": "Languages", "id": "Bahasa"}
