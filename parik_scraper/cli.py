"""CLI entry point for the Parik24 live football scraper.

Usage:
    parik-live              # table view of all live football matches
    parik-live --json       # JSON output
    parik-live --live-only  # only matches currently in play (skip scheduled/finished)
    parik-live --league "Бразилія"  # filter by league name substring
    parik-live --url https://parik.club  # use a different base URL
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys

from parik_scraper.models import LiveMatch
from parik_scraper.scraper import DEFAULT_BASE_URL, ParikScraper, ScraperError


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="parik-live",
        description="Fetch live football matches from Parik24.",
    )
    p.add_argument(
        "--url",
        default=DEFAULT_BASE_URL,
        help=f"Base URL of the Parik24 site (default: {DEFAULT_BASE_URL})",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="HTTP timeout in seconds (default: 20)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output as JSON instead of a table",
    )
    p.add_argument(
        "--live-only",
        action="store_true",
        help="Show only matches currently in play (skip scheduled/finished)",
    )
    p.add_argument(
        "--league",
        default=None,
        help="Filter by league name (case-insensitive substring match)",
    )
    return p


def _print_table(matches: list[LiveMatch]) -> None:
    """Print matches as a formatted table using rich."""
    try:
        from rich.console import Console
        from rich.table import Table

        table = Table(title="Parik24 — Live Football", show_lines=False)
        table.add_column("Status", style="bold cyan", width=10)
        table.add_column("Min", justify="right", width=5)
        table.add_column("Home", style="green", min_width=20)
        table.add_column("Score", justify="center", style="bold yellow", width=7)
        table.add_column("Away", style="red", min_width=20)
        table.add_column("League", style="dim", min_width=15)

        for m in matches:
            table.add_row(
                m.status.value,
                str(m.minute) if m.minute > 0 else "-",
                m.home_team,
                m.score,
                m.away_team,
                m.league or "",
            )

        console = Console()
        console.print()
        console.print(table)
        console.print(f"\n[dim]Total: {len(matches)} match(es)[/dim]")
    except ImportError:
        _print_simple(matches)


def _print_simple(matches: list[LiveMatch]) -> None:
    """Fallback plain-text output if rich is not installed."""
    print(f"\n{'Status':<10} {'Min':>4}  {'Home':<30} {'Score':^7} {'Away':<30} League")
    print("-" * 110)
    for m in matches:
        minute_str = str(m.minute) if m.minute > 0 else "-"
        print(
            f"{m.status.value:<10} {minute_str:>4}  "
            f"{m.home_team:<30} {m.score:^7} "
            f"{m.away_team:<30} {m.league or ''}"
        )
    print(f"\nTotal: {len(matches)} match(es)")


async def _run(args: argparse.Namespace) -> int:
    scraper = ParikScraper(base_url=args.url, timeout=args.timeout)
    try:
        async with scraper:
            matches = await scraper.fetch_live_matches()
    except ScraperError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.live_only:
        matches = [m for m in matches if m.is_live]

    if args.league:
        needle = args.league.lower()
        matches = [m for m in matches if m.league and needle in m.league.lower()]

    if args.json_output:
        data = [m.to_dict() for m in matches]
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if not matches:
            print("No live football matches found.")
        else:
            _print_table(matches)

    return 0


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    sys.exit(asyncio.run(_run(args)))


if __name__ == "__main__":
    main()
