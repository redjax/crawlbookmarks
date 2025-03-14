import logging

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

__all__ = ["parse_bookmarks"]


def parse_bookmarks(html_file: str, include_separators: bool = True) -> dict:
    """Open and read the HTML file."""

    def parse_folder(folder, parent_path=""):
        """Function to recursively parse folders and bookmarks."""
        folder_name = folder.find("h3").text if folder.find("h3") else "Root"
        folder_path = parent_path + "/" + folder_name if parent_path else folder_name

        if folder_path not in bookmarks_data:
            bookmarks_data[folder_path] = {}

        # Parse bookmarks in the current folder
        for dt in folder.find_all("dt"):
            if dt.a:
                bookmark_name = dt.a.text
                bookmark_url = dt.a["href"]
                if include_separators or bookmark_name != "---":
                    bookmarks_data[folder_path][bookmark_url] = bookmark_name

        # Recursively parse subfolders
        for dl in folder.find_all("dl"):
            parse_folder(dl, folder_path)

    try:
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
    except Exception as e:
        msg = f"({type(e)}) Error parsing bookmarks file '{html_file}'. Details: {e}"
        log.error(msg)

        raise

    ## Initialize data structure to hold bookmarks
    bookmarks_data = {}

    ## Start parsing from the root
    for dl in soup.find_all("dl"):
        try:
            parse_folder(dl)
        except Exception as exc:
            msg = f"({type(exc)}) Error parsing folder '{dl}'. Details: {exc}"
            log.error(msg)

            continue

    return bookmarks_data
