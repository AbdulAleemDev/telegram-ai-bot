import logging
import sys


def setup_logging() -> logging.Logger:
    """Configure logging so messages appear immediately in the terminal."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    for handler in logging.root.handlers:
        handler.flush = sys.stdout.flush  # type: ignore[method-assign]

    return logging.getLogger("telegram-bot")
