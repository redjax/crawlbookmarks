from __future__ import annotations

import logging

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

__all__ = ["check_valid_bookmarks_file"]


def check_valid_bookmarks_file(bookmarks_file):
    from bs4 import BeautifulSoup

    with open(bookmarks_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    root_dl = soup.find("dl")

    if not root_dl:
        print("No <DL> tag found!")
    else:
        print("Found root <DL> tag!")
        print(
            root_dl.prettify()[:1000]
        )  # Print the first 1000 characters of the DL tag for inspection
