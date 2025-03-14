import typing as t
from pathlib import Path
import json
import logging
from contextlib import AbstractContextManager

log = logging.getLogger(__name__)

__all__ = ["ChromeBookmarksController"]


class ChromeBookmarksController(AbstractContextManager):
    def __init__(
        self, bookmarks_file: str, output_file: str, include_separators: bool = False
    ) -> None:
        self.bookmarks_file = bookmarks_file
        self.output_file = output_file
        self.include_separators = include_separators

        self.file_reader = None

        self.logger = log.getChild("ChromeBookmarksController")

    def __enter__(self) -> None:
        if not Path(self.bookmarks_file).exists():
            msg = f"Could not find bookmarks file at path '{self.bookmarks_file}'."
            self.logger.error(msg)

            raise

        try:
            self.file_reader = open(self.bookmarks_file, "r", encoding="utf-8")
            self.logger.debug(f"Read contents of file '{self.bookmarks_file}'")
        except Exception as exc:
            msg = (
                f"({type(exc)}) Error opening file '{self.bookmarks_file}' for reading."
            )
            self.logger.error(msg)

            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.logger is None:
            self.logger = log.getChild("ChromeBookmarksController")

        if exc_val:
            self.logger.exception(f"({exc_type}) {exc_val}")
            return False

        return True
