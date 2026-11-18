"""Shared fixtures: a tiny repository layout in a temp directory."""

from __future__ import annotations

import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

CATALOG = """\
categories:
  - {id: lang, name_en: "Languages", name_id: "Bahasa"}
  - {id: empty, name_en: "Empty", name_id: "Kosong"}
badges:
  - {id: zig, name: "Zig", slug: zig, hex: "F7A41D", logo_color: black, category: lang}
  - {id: node-red, name: "Node-RED", slug: nodered, hex: "8F0000", logo_color: white,
     category: lang}
"""

README = """\
# t
<!-- STATS:START -->
<!-- STATS:END -->
<!-- TOC:START -->
<!-- TOC:END -->
<!-- BADGES:START -->
<!-- BADGES:END -->
"""


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """Create a minimal repo with a catalog and both README files."""
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "badges.yml").write_text(CATALOG, encoding="utf-8")
    (tmp_path / "README.md").write_text(README, encoding="utf-8")
    (tmp_path / "README.id.md").write_text(README, encoding="utf-8")
    return tmp_path


class ShieldsStub:
    """A tiny local stand-in for Shields.io whose answer depends on the badge label."""

    def __init__(self) -> None:
        self.behaviors: dict[str, str] = {}
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                label = self.path.split("/badge/", 1)[1].split("?", 1)[0].rsplit("-", 1)[0]
                mode = stub.behaviors.get(label, "ok")
                if mode == "error":
                    self.send_response(500)
                    self.end_headers()
                    return
                ctype = "text/html" if mode == "html" else "image/svg+xml;charset=utf-8"
                body = "<svg>" + ("" if mode == "nologo" else "<image/>") + "</svg>"
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.end_headers()
                self.wfile.write(body.encode())

            def log_message(self, *args: object) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()


@pytest.fixture()
def shields() -> Iterator[ShieldsStub]:
    stub = ShieldsStub()
    yield stub
    stub.server.shutdown()
