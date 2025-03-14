from __future__ import annotations

import json
import logging

from bs4 import BeautifulSoup

from crawlbookmarks import chrome
from crawlbookmarks.utils import io

log = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(
        level="DEBUG",
        format="%(asctime)s - %(levelname)s - %(message)s",  # Corrected levelname
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Usage
    html_file = "bookmarks.html"
    output_file = "bookmarks.json"
    include_separators = False  # Set to False to exclude separators

    bookmarks_data = chrome.parse_bookmarks(html_file, include_separators)
    io.export_to_json(bookmarks_data, output_file)

    log.info(f"Bookmarks exported successfully to '{output_file}'")
