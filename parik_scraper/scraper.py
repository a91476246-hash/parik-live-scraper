"""HTTP scraper for Parik24 live football data."""

from __future__ import annotations

from typing import Any

import httpx

from parik_scraper.models import LiveMatch
from parik_scraper.parser import parse_parik_live_page

DEFAULT_BASE_URL = "https://parik24ua.kyiv.ua"

_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


class ScraperError(Exception):
    """Raised when the scraper fails."""


class ParikScraper:
    """Scrape Parik24 for live football matches via plain HTTP."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 20.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._live_url = f"{self._base_url}/uk/all-live"
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        if self._client is not None:
            return
        self._client = httpx.AsyncClient(
            headers={
                "User-Agent": _DEFAULT_USER_AGENT,
                "Accept-Language": "uk-UA,uk;q=0.9",
                "Accept": "text/html,application/xhtml+xml",
            },
            follow_redirects=True,
            timeout=httpx.Timeout(self._timeout),
        )

    async def stop(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> ParikScraper:
        await self.start()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.stop()

    async def fetch_live_matches(self) -> list[LiveMatch]:
        """Fetch and parse the live-matches page.

        Returns only football matches.

        Raises:
            ScraperError: on network or parsing failures.
        """
        if self._client is None:
            raise ScraperError("ParikScraper is not started — call start() or use 'async with'")

        try:
            response = await self._client.get(self._live_url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ScraperError(f"HTTP {exc.response.status_code}: {self._live_url}") from exc
        except httpx.HTTPError as exc:
            raise ScraperError(f"Request failed: {exc}") from exc

        html = response.text
        if len(html) < 500:
            raise ScraperError("Response body too small — page may be blocked")

        return parse_parik_live_page(html)
