"""Invariants of the real catalog in this repository (not the tiny fixture)."""

import base64
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import pytest

from badgekit.loader import load_catalog
from badgekit.render import MAX_BADGE_URL_LENGTH, badge_url
from badgekit.validate import validate

ROOT = Path(__file__).resolve().parent.parent
CATALOG = load_catalog(ROOT / "data" / "badges.yml")
CUSTOM = [b for b in CATALOG.badges if b.source == "custom"]


def test_real_catalog_is_valid() -> None:
    assert validate(CATALOG) == []


def test_there_are_custom_badges() -> None:
    assert len(CUSTOM) >= 100


@pytest.mark.parametrize("badge", CUSTOM, ids=lambda b: b.id)
def test_custom_logo_survives_the_url_round_trip(badge) -> None:  # noqa: ANN001
    url = badge_url(badge, CATALOG)
    assert len(url) <= MAX_BADGE_URL_LENGTH
    assert "+" not in url.split("?", 1)[1]
    assert "logoColor" not in url
    logo = parse_qs(urlsplit(url).query)["logo"][0]
    assert logo.startswith("data:image/svg+xml;base64,")
    decoded = base64.b64decode(logo.split(",", 1)[1])
    assert decoded == (ROOT / badge.logo_file).read_bytes()
    assert unquote(url).count("data:image/svg+xml;base64,") == 1
