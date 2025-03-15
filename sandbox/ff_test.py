import logging

from crawlbookmarks import firefox
import json

log = logging.getLogger(__name__)

logging.basicConfig(level="DEBUG")

# Usage
html_file = "ff_bookmarks.html"
parsed_bookmarks = firefox.parse_bookmarks(html_file)

# Output to JSON file
with open("ff_bookmarks.json", "w", encoding="utf-8") as f:
    json.dump(parsed_bookmarks, f, indent=2)

print("Bookmarks have been parsed and saved to ff_bookmarks.json")
