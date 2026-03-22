"""Shared utilities for the GEPA pipeline."""

import csv
import logging
from pathlib import Path


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logger with a simple console handler."""
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def load_csv(path: Path) -> list[dict[str, str]]:
    """Load a CSV file and return its rows as a list of dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))  # type: ignore[return-value]
