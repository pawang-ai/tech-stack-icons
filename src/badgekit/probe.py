"""Probe Shields.io to confirm each badge renders and actually shows its logo."""

from __future__ import annotations

import logging
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from .models import Badge, Catalog
from .render import badge_url

logger = logging.getLogger(__name__)
SHIELDS = "https://img.shields.io"
USER_AGENT = (
    "markdown-badges-collection-probe (+https://github.com/pawang-ai/markdown-badges-collection)"
)


@dataclass(frozen=True)
class Failure:
    """A badge that did not render as expected."""

    badge_id: str
    reason: str


def fetch(url: str, timeout: float) -> tuple[int, str, str]:
    """Return ``(status, content_type, body)`` for ``url`` (HTTP errors become statuses)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return (
                resp.status,
                resp.headers.get("Content-Type", ""),
                resp.read().decode("utf-8", "replace"),
            )
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), ""


def check_badge(
    badge: Badge, catalog: Catalog, *, base_url: str, timeout: float, retries: int
) -> Failure | None:
    """Fetch one badge; return a :class:`Failure` or ``None`` when it looks right."""
    url = badge_url(badge, catalog).replace(SHIELDS, base_url.rstrip("/"), 1)
    reason = "no attempt"
    for attempt in range(retries + 1):
        try:
            status, ctype, body = fetch(url, timeout)
        except (OSError, TimeoutError) as exc:
            status, ctype, body, reason = 0, "", "", f"request failed: {exc}"
        else:
            if status == 200 and "svg" in ctype.lower() and "<svg" in body:
                return None if "<image" in body else Failure(badge.id, "rendered without a logo")
            reason = f"HTTP {status} ({ctype or 'no content type'})"
        retryable = status in (0, 429) or status >= 500
        if not retryable or attempt == retries:
            break
        time.sleep(2**attempt)
    return Failure(badge.id, reason)


def probe_catalog(
    catalog: Catalog,
    *,
    base_url: str = SHIELDS,
    only: str | None = None,
    limit: int | None = None,
    workers: int = 6,
    timeout: float = 20,
    retries: int = 2,
) -> tuple[int, list[Failure]]:
    """Probe badges concurrently. Returns ``(checked_count, failures)``."""
    badges = [b for b in catalog.badges if only is None or b.source == only]
    if limit:
        badges = badges[:limit]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = pool.map(
            lambda b: check_badge(b, catalog, base_url=base_url, timeout=timeout, retries=retries),
            badges,
        )
        failures = [f for f in results if f is not None]
    return len(badges), failures
