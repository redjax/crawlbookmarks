from __future__ import annotations

import logging

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

__all__ = ["check_valid_bookmarks_file"]


def check_valid_bookmarks_file(bookmarks_file: str) -> bool:
    """Check if a bookmarks file is valid by looking for a top-level <DL> tag."""
    from bs4 import BeautifulSoup

    try:
        with open(bookmarks_file, "r", encoding="utf-8") as file:
            html_content = file.read()
    except Exception as exc:
        msg = f"({type(exc)}) Error opening bookmarks file '{bookmarks_file}'. Details: {exc}"
        log.error(msg)

        raise

    ## Parse contents of file into BeautifulSoup object
    soup = BeautifulSoup(html_content, "html.parser")
    ## Find root <DL> tag
    root_dl = soup.find("dl")

    if not root_dl:
        log.warning(f"No <DL> tag found in file '{bookmarks_file}'.")

        return False
    else:
        log.debug("Found root <DL> tag!")

        return True
