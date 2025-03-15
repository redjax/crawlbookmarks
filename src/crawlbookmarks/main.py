from __future__ import annotations

import logging

from crawlbookmarks import chrome, cli
from crawlbookmarks.utils import io

log = logging.getLogger(__name__)

__all__ = ["start_crawl"]


def start_crawl(
    bookmarks_file: str, output_file: str, include_separators: bool
) -> dict:
    """Run bookmark parse as a function call (instead of from the CLI).

    Params:
        bookmarks_file (str): Path to a bookmarks HTML file to read.
        output_file (str): Path to a JSON file where parsed bookmarks will be saved.
        include_separators (bool): When `True`, includes bookmarks that serve as a separator.

    Returns:
        (dict): The parsed bookmarks data.

    """
    log.debug(f"Parsing file '{bookmarks_file}'")
    try:
        ## Parse bookmarks into a dict
        bookmarks_data: dict = chrome.parse_bookmarks(
            html_file=bookmarks_file, include_separators=include_separators
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error parsing bookmarks in file '{bookmarks_file}'. Details: {exc}"
        log.error(msg)

        exit(1)

    log.debug(f"Exporting parsed bookmarks to {output_file}")
    try:
        ## Save parsed bookmarks data to JSON file
        io.export_to_json(bookmarks_data, output_file)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving parsed bookmarks to file '{output_file}'. Details: {exc}"
        log.error(msg)

        exit(1)

    log.info(f"Bookmarks exported successfully to '{output_file}'")

    return bookmarks_data


if __name__ == "__main__":
    ## Execute the CLI when this script is called directly
    run_cli()
