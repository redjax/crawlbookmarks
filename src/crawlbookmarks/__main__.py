import logging

from crawlbookmarks.main import run_cli

log = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        run_cli()
    except Exception as exc:
        logging.basicConfig(
            level="ERROR", format="%(asctime)s - %(levelname)s - %(message)s"
        )

        log.error(f"Error running crawlbookmarks CLI. Details: {exc}")

        exit(1)
