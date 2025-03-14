"""Scrape a bookmarks.html file exported from your browser and parse it into a JSON file.

Description:
    Loads a bookmarks.html file & scrapes it with BeautifulSoup. Discovered bookmarks are formatted
    into a Python dict, which can be optionally saved to a JSON file.

    The app can be run as a CLI by calling it directly, i.e. `python crawlbookmarks --help`.
"""
from __future__ import annotations

import logging

from crawlbookmarks.main import run_cli

log = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        ## Start the CLI
        run_cli()
    except Exception as exc:
        logging.basicConfig(
            level="ERROR", format="%(asctime)s - %(levelname)s - %(message)s"
        )

        log.error(f"Error running crawlbookmarks CLI. Details: {exc}")

        exit(1)
