from bs4 import BeautifulSoup

__all__ = ["parse_bookmarks"]


def parse_bookmarks(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    def parse_folder(element):
        folder = {}
        for item in element.find_all(["h3", "a"], recursive=False):
            if item.name == "h3":
                subfolder_name = item.string.strip()
                next_dl = item.find_next_sibling("dl")
                if next_dl:
                    folder[subfolder_name] = parse_folder(next_dl)
            elif item.name == "a":
                bookmark_name = item.string.strip()
                bookmark_url = item["href"]
                folder[bookmark_name] = bookmark_url
        return folder

    bookmarks = {}
    for dl in soup.find_all("dl", recursive=False):
        bookmarks.update(parse_folder(dl))

    return bookmarks
