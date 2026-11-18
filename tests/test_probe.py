from pathlib import Path

from badgekit.loader import load_catalog
from badgekit.probe import probe_catalog


def _catalog(repo: Path):  # noqa: ANN202
    return load_catalog(repo / "data" / "badges.yml")


def test_all_badges_ok(repo: Path, shields) -> None:  # noqa: ANN001
    checked, failures = probe_catalog(_catalog(repo), base_url=shields.url, retries=0)
    assert (checked, failures) == (2, [])


def test_missing_logo_is_reported(repo: Path, shields) -> None:  # noqa: ANN001
    shields.behaviors["Zig"] = "nologo"
    _, failures = probe_catalog(_catalog(repo), base_url=shields.url, retries=0)
    assert [(f.badge_id, f.reason) for f in failures] == [("zig", "rendered without a logo")]


def test_server_error_and_wrong_content_type_are_reported(
    repo: Path, shields
) -> None:  # noqa: ANN001
    shields.behaviors.update({"Zig": "error", "Node--RED": "html"})
    _, failures = probe_catalog(_catalog(repo), base_url=shields.url, retries=0)
    reasons = {f.badge_id: f.reason for f in failures}
    assert reasons["zig"].startswith("HTTP 500")
    assert reasons["node-red"].startswith("HTTP 200")


def test_only_and_limit_filters(repo: Path, shields) -> None:  # noqa: ANN001
    catalog = _catalog(repo)
    assert probe_catalog(catalog, base_url=shields.url, only="custom", retries=0)[0] == 0
    assert probe_catalog(catalog, base_url=shields.url, limit=1, retries=0)[0] == 1


def test_unreachable_server_is_a_failure(repo: Path) -> None:
    checked, failures = probe_catalog(
        _catalog(repo), base_url="http://127.0.0.1:1", retries=0, timeout=1
    )
    assert checked == 2 and len(failures) == 2
