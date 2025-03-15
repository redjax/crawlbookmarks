from bs4 import BeautifulSoup, Tag
import logging

__all__ = ["parse_bookmarks"]

log = logging.getLogger(__name__)


def parse_bookmarks(html_file: str):
    log.debug(f"Reading bookmarks from file '{html_file}'.")

    def parse_folder(dl_element, depth=0):
        # log.debug(f"{'  ' * depth}Parsing folder: {dl_element.name}")
        folder = {}

        for item in dl_element.contents:
            if isinstance(item, Tag):
                if item.name == "dt":
                    if item.h3:
                        folder_name = (
                            item.h3.string.strip()
                            if item.h3.string
                            else "Unnamed Folder"
                        )
                        log.debug(f"{'  ' * depth}Folder: {folder_name}")
                        folder_attrs = dict(item.h3.attrs)  # Save the H3 attributes
                        folder[folder_name] = {
                            "attributes": folder_attrs,
                            "children": {},
                        }
                        next_dl = item.find_next_sibling("dl")
                        if next_dl:
                            folder[folder_name]["children"] = parse_folder(
                                next_dl, depth + 1
                            )
                elif item.a:
                    bookmark_name = (
                        item.a.string.strip() if item.a.string else "Unnamed Bookmark"
                    )
                    bookmark_url = item.a.get("href", "")
                    log.debug(
                        f"{'  ' * depth}Bookmark: {bookmark_name} -> {bookmark_url}"
                    )
                    bookmark_attrs = dict(item.a.attrs)  # Save the A attributes
                    folder[bookmark_name] = {
                        "url": bookmark_url,
                        "attributes": bookmark_attrs,
                    }

        return folder

    try:
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
    except Exception as e:
        msg = f"({type(e)}) Error parsing bookmarks file '{html_file}'. Details: {e}"
        log.error(msg)

        raise

    bookmarks = {}
    root_dl = soup.find("dl")

    if root_dl:
        bookmarks = parse_folder(root_dl)
        log.debug(f"Bookmarks: {bookmarks}")
        return bookmarks
    else:
        log.warning(
            "No root <DL> tag found. Is this a valid bookmarks.html file exported from Firefox?"
        )
        return {}
