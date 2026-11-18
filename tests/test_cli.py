from pathlib import Path

from badgekit.cli import main


def test_build_then_check_passes(repo: Path) -> None:
    assert main(["--root", str(repo), "build"]) == 0
    assert (repo / "docs" / "badges.json").is_file()
    assert "### Languages" in (repo / "README.md").read_text(encoding="utf-8")
    assert "### Bahasa" in (repo / "README.id.md").read_text(encoding="utf-8")
    assert main(["--root", str(repo), "check"]) == 0


def test_check_detects_stale_output(repo: Path) -> None:
    main(["--root", str(repo), "build"])
    (repo / "data" / "badges.yml").write_text(
        (repo / "data" / "badges.yml").read_text(encoding="utf-8")
        + '  - {id: go, name: Go, slug: go, hex: "00ADD8", logo_color: white, category: lang}\n',
        encoding="utf-8",
    )
    assert main(["--root", str(repo), "check"]) == 1
    assert main(["--root", str(repo), "build"]) == 0
    assert main(["--root", str(repo), "check"]) == 0


def test_validate_failure_returns_1(repo: Path) -> None:
    (repo / "data" / "badges.yml").write_text(
        "categories:\n  - {id: c, name_en: C, name_id: C}\n"
        'badges:\n  - {id: a, name: A, slug: a, hex: "zzz", category: c}\n',
        encoding="utf-8",
    )
    assert main(["--root", str(repo), "validate"]) == 1


def test_missing_catalog_returns_2(tmp_path: Path) -> None:
    assert main(["--root", str(tmp_path), "stats"]) == 2


def test_stats(repo: Path, capsys) -> None:  # noqa: ANN001
    assert main(["--root", str(repo), "stats"]) == 0
    assert "2 badges in 1 categories" in capsys.readouterr().out


def test_probe_command(repo: Path, shields) -> None:  # noqa: ANN001
    assert main(["--root", str(repo), "probe", "--base-url", shields.url, "--workers", "2"]) == 0
    shields.behaviors["Zig"] = "nologo"
    assert main(["--root", str(repo), "probe", "--base-url", shields.url]) == 1


def test_check_fails_when_readme_would_get_too_big(repo: Path, monkeypatch) -> None:  # noqa: ANN001
    main(["--root", str(repo), "build"])
    monkeypatch.setattr("badgekit.cli.README_MAX_BYTES", 10)
    assert main(["--root", str(repo), "check"]) == 1
