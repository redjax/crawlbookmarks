from __future__ import annotations

import json

from bs4 import BeautifulSoup

def parse_bookmarks(html_file: str, include_separators: bool = True):
    # Open and read the HTML file
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Initialize data structure to hold bookmarks
    bookmarks_data = {}

    # Function to recursively parse folders and bookmarks
    def parse_folder(folder, parent_path=""):
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

    # Start parsing from the root
    for dl in soup.find_all("dl"):
        parse_folder(dl)

    return bookmarks_data


def export_to_json(bookmarks_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(bookmarks_data, file, indent=4)


if __name__ == "__main__":
    # Usage
    html_file = "bookmarks.html"
    output_file = "bookmarks.json"
    include_separators = False  # Set to False to exclude separators

    bookmarks_data = parse_bookmarks(html_file, include_separators)
    export_to_json(bookmarks_data, output_file)

    print("Bookmarks exported successfully to", output_file)
