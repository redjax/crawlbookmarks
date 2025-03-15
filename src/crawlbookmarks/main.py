from __future__ import annotations

import logging

from crawlbookmarks import chrome, cli
from crawlbookmarks.utils import io

log = logging.getLogger(__name__)

__all__ = ["run_cli", "start_crawl"]


def run_cli() -> None:
    """Entrypoint for the CLI app.

    Description:
        Calls the cli.parse_args() method, which takes a user's input parameters & maps them to args in
        an argparse.Namespace object.
    """
    ## Parse args into a namespace object
    args = cli.parse_args()
    ## Configure logging based on args
    cli.set_logging_format(args)

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
