from __future__ import annotations

from contextlib import AbstractContextManager
import logging
from pathlib import Path
import typing as t

from crawlbookmarks import chrome
from crawlbookmarks.utils import io

log = logging.getLogger(__name__)

__all__ = ["ChromeBookmarksController"]


class ChromeBookmarksController(AbstractContextManager):
    """Controller class for Chrome bookmarks.

    Params:
        bookmarks_file (str): Path to the bookmarks HTML file to parse (default: bookmarks.html)
        output_file (str): Path where the parsed bookmarks data will be saved (default: bookmarks.json)
        save_results (bool): When `True`, results will be saved to the path in `output_file` (default: True)
        include_separators (bool): When `True`, include separator bookmarks (default: False)
    """

    def __init__(
        self,
        bookmarks_file: str = "bookmarks.html",
        output_file: str = "bookmarks.json",
        save_results: bool = True,
        include_separators: bool = False,
    ) -> None:
        self.bookmarks_file = bookmarks_file
        self.output_file = output_file
        self.include_separators = include_separators
        self.save_results = save_results

        self.logger = log.getChild("ChromeBookmarksController")

    def __enter__(self) -> t.Self:
        if not Path(self.bookmarks_file).exists():
            msg = f"Could not find bookmarks file at path '{self.bookmarks_file}'."
            self.logger.error(msg)
            raise FileNotFoundError(msg)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_val:
            self.logger.exception(f"({exc_type}) {exc_val}")
            return False
        return True

    def parse_bookmarks(self) -> dict:
        """Parse bookmarks into dict and optionally save to file."""
        self.logger.debug(f"Parsing file '{self.bookmarks_file}'")
        try:
            bookmarks_data = chrome.parse_bookmarks(
                html_file=self.bookmarks_file,
                include_separators=self.include_separators,
            )
        except Exception as exc:
            msg = f"({type(exc)}) Error parsing bookmarks in file '{self.bookmarks_file}'. Details: {exc}"
            self.logger.error(msg)
            raise

        if self.save_results:
            self.save_bookmarks(bookmarks_data)

        return bookmarks_data

    def save_bookmarks(self, bookmarks_data: dict) -> None:
        """Save parsed bookmarks data to output file."""
        self.logger.debug(f"Exporting parsed bookmarks to {self.output_file}")
        try:
            io.export_to_json(bookmarks_data, self.output_file)
        except Exception as exc:
            msg = f"({type(exc)}) Error saving parsed bookmarks to file '{self.output_file}'. Details: {exc}"
            self.logger.error(msg)
            raise

        self.logger.info(f"Bookmarks exported successfully to '{self.output_file}'")
