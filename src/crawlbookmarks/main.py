from __future__ import annotations

import logging

from crawlbookmarks import chrome
from crawlbookmarks.utils import io
from crawlbookmarks import cli

log = logging.getLogger(__name__)

__all__ = ["run_cli"]


def run_cli():
    args = cli.parse_args()
    cli.set_logging_format(args)

    if args.debug:
        log.debug("DEBUG logging enabled")

    html_file = args.input
    output_file = args.output
    include_separators = args.include_separators

    log.debug(f"Parsing file '{html_file}'")
    try:
        bookmarks_data = chrome.parse_bookmarks(
            html_file=html_file, include_separators=include_separators
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error parsing bookmarks in file '{html_file}'. Details: {exc}"
        log.error(msg)

        exit(1)

    log.debug(f"Exporting parsed bookmarks to {output_file}")
    try:
        io.export_to_json(bookmarks_data, output_file)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving parsed bookmarks to file '{output_file}'. Details: {exc}"
        log.error(msg)

        exit(1)

    log.info(f"Bookmarks exported successfully to '{output_file}'")


if __name__ == "__main__":
    run_cli()
