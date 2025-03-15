from bs4 import BeautifulSoup, Tag
import logging

__all__ = ["parse_bookmarks"]

log = logging.getLogger(__name__)


def parse_bookmarks(html_file: str, parser: str = "lxml"):
    log.debug(f"Reading bookmarks from file '{html_file}'.")
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, parser)

    def parse_folder(dl_element, depth=0):
        log.debug(f"{'  ' * depth}Parsing folder: {dl_element.name}")
        folder = {}

        for item in dl_element.contents:
            if isinstance(item, Tag):  # Only process Tag elements
                if item.name == "dt":
                    if item.h3:
                        folder_name = (
                            item.h3.string.strip()
                            if item.h3.string
                            else "Unnamed Folder"
                        )
                        log.debug(f"{'  ' * depth}Folder: {folder_name}")
                        next_dl = item.find_next_sibling("dl")
                        if next_dl:
                            folder[folder_name] = parse_folder(next_dl, depth + 1)
                    elif item.a:
                        bookmark_name = (
                            item.a.string.strip()
                            if item.a.string
                            else "Unnamed Bookmark"
                        )
                        bookmark_url = item.a.get("href", "")
                        log.debug(
                            f"{'  ' * depth}Bookmark: {bookmark_name} -> {bookmark_url}"
                        )
                        folder[bookmark_name] = bookmark_url
                    else:
                        log.warning(f"{'  ' * depth}Unexpected dt content: {item}")

        return folder

    bookmarks = {}
    root_dl = soup.find("dl")

    if root_dl:
        # log.debug(f"Root DL: {root_dl}")
        bookmarks = parse_folder(root_dl)
        log.debug(f"Bookmarks: {bookmarks}")
        return bookmarks
    else:
        log.warning(
            "No root <DL> tag found. Is this a valid bookmarks.html file exported from Firefox?"
        )
        return {}
