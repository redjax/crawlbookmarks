from __future__ import annotations

import logging

from crawlbookmarks import chrome, start_crawl

log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level="DEBUG", format="%(asctime)s - %(levelname)s - %(message)s"
    )

    bookmarks_controller: chrome.ChromeBookmarksController = (
        chrome.ChromeBookmarksController(
            bookmarks_file="bookmarks.html",
            output_file="bookmarks.json",
            include_separators=True,
            save_results=True,
        )
    )

    try:
        with bookmarks_controller as bookmarks_ctl:
            log.debug(f"Parsing bookmarks")
            parsed_bookmarks = bookmarks_ctl.parse_bookmarks()
    except Exception as exc:
        msg = f"({type(exc)}) Error parsing bookmarks. Details: {exc}"
        log.error(msg)
