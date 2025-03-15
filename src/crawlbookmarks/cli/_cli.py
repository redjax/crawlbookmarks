from __future__ import annotations

import argparse
import logging

log = logging.getLogger(__name__)

from crawlbookmarks.cli.logger import set_logging_format
from crawlbookmarks import chrome
from crawlbookmarks.utils import io
from crawlbookmarks import firefox

__all__ = ["run_cli"]


def parse_args() -> argparse.Namespace:
    """Parse CLI args."""
    parser = argparse.ArgumentParser(
        "crawlbookmarks",
        description="Parse a bookmarks.html file exported from your browser into JSON.",
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable DEBUG logging", default=False
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="When present, logs will be saved to a file",
        default=None,
    )

    parser.add_argument(
        "-i",
        "--input",
        "--in",
        type=str,
        help="Path to your bookmarks.html file to parse",
        default="bookmarks.html",
    )
    parser.add_argument(
        "-o",
        "--output",
        "--out",
        type=str,
        help="Path to a .json file where the parsed bookmarks will be saved",
        default="bookmarks.json",
    )
    parser.add_argument(
        "-s",
        "--include-separators",
        action="store_true",
        help="When present, will include any separator bookmarks (i.e. from Vivaldi)",
        default=False,
    )

    return parser.parse_args()


def run_cli() -> None:
    """Entrypoint for the CLI app.

    Description:
        Calls the cli.parse_args() method, which takes a user's input parameters & maps them to args in
        an argparse.Namespace object.
    """
    ## Parse args into a namespace object
    args = parse_args()
    ## Configure logging based on args
    set_logging_format(args)

    log.info("Parsing bookmarks")

    if args.debug:
        log.debug("DEBUG logging enabled")

    ## Set vars from args
    html_file = args.input
    output_file = args.output
    include_separators = args.include_separators

    log.debug(
        f"""
Args:

html_file: {html_file}
output_file: {output_file}
include_separators: {include_separators}
debug: {args.debug}
"""
    )

    log.debug(f"Parsing file '{html_file}'")
    try:
        ## Attempt to parse bookmarks file into a variable
        bookmarks_data: dict = chrome.parse_bookmarks(
            html_file=html_file, include_separators=include_separators
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error parsing bookmarks in file '{html_file}'. Details: {exc}"
        log.error(msg)

        exit(1)

    log.debug(f"Exporting parsed bookmarks to {output_file}")
    try:
        ## Save parsed bookmarks to a JSON file
        io.export_to_json(bookmarks_data, output_file)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving parsed bookmarks to file '{output_file}'. Details: {exc}"
        log.error(msg)

        exit(1)

    log.info(f"Bookmarks exported successfully to '{output_file}'")
