# CrawlBookmarks

Python app to parse a bookmarks.html file into JSON. Tested with bookmarks exported from a Chromium-based browser.

## Setup

[Export your browser's bookmarks to a .html file](https://helpdeskgeek.com/how-to-transfer-bookmarks-to-and-from-all-major-browsers/). Then, run this app with `--input path/to/your/bookmarks.html`.

A file named `bookmarks.json` will be outputted to the path where you ran this script. You can change the output path by passing `--output path/to/bookmarks.json`.

### With uv

- Setup environment with `uv sync`
- Run the script with `uv run -m src/crawlbookmarks --help`

### With virtualenv

...

## Usage

This package provides a CLI entrypoint in [`__main__.py`](./src/crawlbookmarks/__main__.py). If you call the package like `python -m crawlbookmarks --help` or `uv run -m crawlbookmarks --help`, you can see usage.

```shell
usage: crawlbookmarks [-h] [-d] [--log-file LOG_FILE] [-i INPUT] [-o OUTPUT] [-s]

Parse a bookmarks.html file exported from your browser into JSON.

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable DEBUG logging
  --log-file LOG_FILE   When present, logs will be saved to a file
  -i INPUT, --input INPUT, --in INPUT
                        Path to your bookmarks.html file to parse
  -o OUTPUT, --output OUTPUT, --out OUTPUT
                        Path to a .json file where the parsed bookmarks will be saved
  -s, --include-separators
                        When present, will include any separator bookmarks (i.e. from Vivaldi)
```
