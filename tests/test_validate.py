import dataclasses
from pathlib import Path

import pytest

from badgekit.loader import load_catalog
from badgekit.models import Catalog
from badgekit.validate import check_svg, load_simple_icons_slugs, validate


def _catalog(repo: Path, **changes: object) -> Catalog:
    catalog = load_catalog(repo / "data" / "badges.yml")
    badges = list(catalog.badges)
    badges[0] = dataclasses.replace(badges[0], **changes)
    return dataclasses.replace(catalog, badges=tuple(badges))


def test_valid_catalog(repo: Path) -> None:
    catalog = load_catalog(repo / "data" / "badges.yml")
    assert validate(catalog, {"zig", "nodered"}) == []


def test_duplicate_id_and_name(repo: Path) -> None:
    catalog = load_catalog(repo / "data" / "badges.yml")
    dup = dataclasses.replace(catalog, badges=catalog.badges + (catalog.badges[0],))
    errors = validate(dup)
    assert any("duplicate id: zig" in e for e in errors)
    assert any("duplicate name: zig" in e for e in errors)


def test_bad_hex_color_and_category(repo: Path) -> None:
    errors = validate(_catalog(repo, hex="#FFF", logo_color="red", category="nope"))
    assert any("hex must be" in e for e in errors)
    assert any("logo_color" in e for e in errors)
    assert any("unknown category" in e for e in errors)


def test_unknown_slug(repo: Path) -> None:
    catalog = load_catalog(repo / "data" / "badges.yml")
    assert any("not found in Simple Icons" in e for e in validate(catalog, {"nodered"}))


def test_custom_requires_existing_logo(repo: Path) -> None:
    assert any("require logo_file" in e for e in validate(_catalog(repo, source="custom")))
    errors = validate(_catalog(repo, source="custom", logo_file="assets/logos/missing.svg"))
    assert any("logo_file not found" in e for e in errors)


def test_load_simple_icons_slugs(tmp_path: Path) -> None:
    path = tmp_path / "si.json"
    path.write_text('[{"slug": "a"}, {"slug": "b"}]', encoding="utf-8")
    assert load_simple_icons_slugs(str(path)) == {"a", "b"}


GOOD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" fill="#fff">'
    '<path d="M0 0h8v8z"/></svg>'
)


def _svg(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "logo.svg"
    path.write_text(text, encoding="utf-8")
    return path


def test_check_svg_accepts_a_clean_logo(tmp_path: Path) -> None:
    assert check_svg(_svg(tmp_path, GOOD_SVG)) == []


@pytest.mark.parametrize(
    ("svg", "fragment"),
    [
        (GOOD_SVG.replace("<path", "<script>alert(1)</script><path"), "forbidden element <script>"),
        (GOOD_SVG.replace("<path", '<image href="data:x"/><path'), "forbidden element <image>"),
        (GOOD_SVG.replace("<path", '<path onload="x()"'), "forbidden attribute"),
        (
            GOOD_SVG.replace("<path", '<a href="https://evil.test"><path').replace(
                "/></svg>", "/></a></svg>"
            ),
            "forbidden attribute",
        ),
        ('<!DOCTYPE svg [<!ENTITY a "b">]>' + GOOD_SVG, "DOCTYPE"),
        (GOOD_SVG.replace(' viewBox="0 0 128 128"', ""), "needs a viewBox"),
        ("<svg", "not valid XML"),
        ("<html/>", "root element is not <svg>"),
    ],
)
def test_check_svg_rejects_unsafe_input(tmp_path: Path, svg: str, fragment: str) -> None:
    assert any(fragment in problem for problem in check_svg(_svg(tmp_path, svg)))


def test_check_svg_rejects_oversized_files(tmp_path: Path) -> None:
    assert any("max" in p for p in check_svg(_svg(tmp_path, GOOD_SVG + " " * 25_000)))


def _custom_repo(repo: Path, svg: str) -> Catalog:
    (repo / "assets" / "logos").mkdir(parents=True)
    (repo / "assets" / "logos" / "x.svg").write_text(svg, encoding="utf-8")
    (repo / "data" / "badges.yml").write_text(
        "categories:\n  - {id: c, name_en: C, name_id: C}\nbadges:\n"
        "  - {id: x, name: X, slug: x, hex: '112233', category: c, source: custom,\n"
        "     logo_file: assets/logos/x.svg}\n",
        encoding="utf-8",
    )
    return load_catalog(repo / "data" / "badges.yml")


def test_custom_badge_within_budget_is_valid(repo: Path) -> None:
    assert validate(_custom_repo(repo, GOOD_SVG)) == []


def test_badge_url_over_budget_is_rejected(repo: Path) -> None:
    big = GOOD_SVG.replace("M0 0h8v8z", "M" + "1 2 " * 700)
    errors = validate(_custom_repo(repo, big))
    assert any("badge URL is" in e and "max 3000" in e for e in errors)


def test_custom_badge_reports_unsafe_svg(repo: Path) -> None:
    errors = validate(_custom_repo(repo, GOOD_SVG.replace("<path", "<script/><path")))
    assert any("forbidden element <script>" in e for e in errors)
