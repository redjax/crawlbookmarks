import argparse

__all__ = ["parse_args"]


def parse_args() -> argparse.Namespace:
    """Parse CLI args."""

    parser = argparse.ArgumentParser(
        "crawlbookmarks",
        description="Parse a bookmarks.html file exported from your browser into JSON.",
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable DEBUG logging", default=False
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="When present, logs will be saved to a file",
        default=None,
    )

    parser.add_argument(
        "-i",
        "--input",
        "--in",
        type=str,
        help="Path to your bookmarks.html file to parse",
    )
    parser.add_argument(
        "-o",
        "--output",
        "--out",
        type=str,
        help="Path to a .json file where the parsed bookmarks will be saved",
    )
    parser.add_argument(
        "-s",
        "--include-separators",
        action="store_true",
        help="When present, will include any separator bookmarks (i.e. from Vivaldi)",
        default=False,
    )

    return parser.parse_args()
