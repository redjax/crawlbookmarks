from __future__ import annotations

import json
import logging

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

__all__ = ["check_valid_bookmarks_file", "export_to_json"]


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


def export_to_json(bookmarks_data: dict, output_file: str) -> None:
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(bookmarks_data, file, indent=4)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving parsed bookmarks to JSON file '{output_file}'. Details: {exc}"
        log.error(msg)

        raise
