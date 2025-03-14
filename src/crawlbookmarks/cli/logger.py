import sys
import logging
from pathlib import Path
import argparse


def set_logging_format(args: argparse.Namespace) -> None:
    """Setup logging based on args passed to CLI."""
    # Use the root logger
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()

    formatter = None

    ## -d/--debug arg
    if args.debug:
        root_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s > [%(levelname)s] > %(module)s.%(funcName)s:%(lineno)s > %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    ## Standard logging
    else:
        root_logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s > %(message)s", datefmt="%H:%M:%S")

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    ## Set up file logging if a file path is provided
    if args.log_file:
        file_path = Path(args.log_file)

        if file_path.exists() and not (args.append or args.overwrite):
            root_logger.error(
                f"File {file_path} already exists. Use -a/--append or -o/--overwrite to modify."
            )
            sys.exit(1)

        ## Create directories if they do not exist
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            msg = f"({type(exc)}) Unable to create directory: '{file_path.parent}'. Details: {exc}"
            root_logger.error(msg)
            sys.exit(1)

        ## File mode based on append/overwrite
        file_mode = "a" if args.append else "w"
        file_handler = logging.FileHandler(file_path, mode=file_mode)
        file_formatter = logging.Formatter(
            "%(asctime)s | [%(levelname)s] | %(message)s", datefmt="%H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel("INFO")

        root_logger.addHandler(file_handler)
