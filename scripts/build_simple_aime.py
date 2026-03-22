#!/usr/bin/env python3
"""
Build train.csv, val.csv, and test.csv from the gepa AIME dataset.

IMPORTANT: Run this script in an environment with internet access to HuggingFace.
The resulting CSVs can then be transferred to restricted environments.

Dataset structure from gepa.examples.aime.init_dataset():
    trainset: list of {"input": problem_text, "additional_context": {...}, "answer": "### <int>"}
    valset:   list of {"input": problem_text, "additional_context": {...}, "answer": "### <int>"}

Output CSV columns:
    input  - the math problem (from item["input"])
    output - the expected answer (from item["answer"])
"""

import csv
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def write_csv(path: str, dataset: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["input", "output"])
        writer.writeheader()
        for item in dataset:
            writer.writerow({"input": item["input"], "output": item["answer"]})
    logger.info("Written %d rows -> %s", len(dataset), path)


def main():
    try:
        import gepa
    except ImportError:
        logger.error("gepa package not found. Install with: pip install gepa")
        sys.exit(1)

    logger.info("Initializing AIME dataset from HuggingFace...")
    trainset, valset, testset = gepa.examples.aime.init_dataset()

    Path("data").mkdir(parents=True, exist_ok=True)
    write_csv("data/train.csv", trainset)
    write_csv("data/val.csv", valset)
    write_csv("data/test.csv", testset)

    logger.info("Done! Transfer the data/ folder to your restricted environment.")


if __name__ == "__main__":
    main()
