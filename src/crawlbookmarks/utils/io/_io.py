from __future__ import annotations

import json
import logging

log = logging.getLogger(__name__)

__all__ = ["export_to_json"]


def export_to_json(bookmarks_data: dict, output_file: str) -> None:
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(bookmarks_data, file, indent=4)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving parsed bookmarks to JSON file '{output_file}'. Details: {exc}"
        log.error(msg)

        raise
