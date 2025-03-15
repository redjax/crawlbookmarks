from __future__ import annotations

import logging

from crawlbookmarks import chrome, firefox

log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level="DEBUG",
        format="%(asctime)s - %(name)s (%(module)s.%(funcName)s:%(lineno)s) - %(levelname)s - %(message)s",
    )

    chrome_controller: chrome.ChromeBookmarksController = (
        chrome.ChromeBookmarksController(
            bookmarks_file="bookmarks.html",
            output_file="bookmarks.json",
            include_separators=True,
            save_results=True,
        )
    )

    try:
        with chrome_controller as chrome_ctl:
            log.debug(f"Parsing Chrome bookmarks")
            parsed_chrome_bookmarks = chrome_ctl.parse_bookmarks()
    except Exception as exc:
        msg = f"({type(exc)}) Error parsing Chrome bookmarks. Details: {exc}"
        log.error(msg)

    ff_controller = firefox.FirefoxBookmarksController(
        bookmarks_file="ff_bookmarks.html",
        output_file="ff_bookmarks.json",
        save_results=True,
    )

    try:
        with ff_controller as ff_ctl:
            log.debug(f"Parsing Firefox bookmarks")
            parsed_ff_bookmarks = ff_ctl.parse_bookmarks()
    except Exception as exc:
        msg = f"({type(exc)}) Error parsing Firefox bookmarks. Details: {exc}"
        log.error(msg)
