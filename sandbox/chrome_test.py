import logging

from crawlbookmarks import chrome
import json

log = logging.getLogger(__name__)

logging.basicConfig(level="DEBUG")

# Usage
html_file = "bookmarks.html"
parsed_bookmarks = chrome.parse_bookmarks(html_file)

# Output to JSON file
with open("bookmarks.json", "w", encoding="utf-8") as f:
    json.dump(parsed_bookmarks, f, indent=2)

print("Bookmarks have been parsed and saved to bookmarks.json")
