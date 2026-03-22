"""
Prompt optimization using the GEPA framework.
Loads train/test data and the seed prompt, runs gepa.optimize(),
and writes the result to reports/.
"""

import logging
import math
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.constants import (
    MAX_METRIC_CALLS,
    OPTIMIZATION_REPORT,
    REFLECTION_LM,
    REPORTS_DIR,
    SEED_PROMPT_FILE,
    TASK_LM,
    TEST_CSV,
    TRAIN_CSV,
    VAL_SPLIT,
)
from src.utils import configure_logging, load_csv

logger = logging.getLogger(__name__)


def csv_to_gepa_dataset(rows: list[dict[str, str]]):
    """Convert list of {input, output} dicts to GEPA DefaultDataInst format."""
    return [
        {"input": r["input"], "additional_context": {}, "answer": r["output"]}
        for r in rows
    ]


def split_train_val(rows: list[dict[str, str]], val_fraction: float):
    n_val = max(1, math.ceil(len(rows) * val_fraction))
    return rows[n_val:], rows[:n_val]


def write_report(seed_prompt: str, result: object, elapsed: float):
    REPORTS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    best: dict[str, str] = result.best_candidate  # type: ignore[attr-defined]

    lines: list[str] = [
        "=" * 70,
        "GEPA PROMPT OPTIMIZATION — RESULTS REPORT",
        f"Generated : {ts}",
        f"Elapsed   : {elapsed:.1f}s",
        "=" * 70,
        "",
        "SEED PROMPT",
        "-" * 70,
        seed_prompt.strip(),
        "",
        "OPTIMIZED PROMPT",
        "-" * 70,
        best.get("system_prompt", str(best)),
        "",
        "CONFIGURATION",
        "-" * 70,
        f"  task_lm          : {TASK_LM}",
        f"  reflection_lm    : {REFLECTION_LM}",
        f"  max_metric_calls : {MAX_METRIC_CALLS}",
        "",
        "=" * 70,
        "END OF REPORT",
        "=" * 70,
    ]
    OPTIMIZATION_REPORT.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Report written to: %s", OPTIMIZATION_REPORT)


def main():
    configure_logging()

    try:
        import gepa  # type: ignore[import-untyped]
    except ImportError:
        logger.error("gepa not installed. Run: pip install gepa")
        sys.exit(1)

    logger.info("Loading data...")
    all_train = load_csv(TRAIN_CSV)
    test_rows = load_csv(TEST_CSV)
    seed_prompt = SEED_PROMPT_FILE.read_text(encoding="utf-8").strip()

    train_rows, val_rows = split_train_val(all_train, VAL_SPLIT)
    logger.info("  Train=%d  Val=%d  Test=%d", len(train_rows), len(val_rows), len(test_rows))

    trainset = csv_to_gepa_dataset(train_rows)
    valset = csv_to_gepa_dataset(val_rows)

    seed_candidate = {"system_prompt": seed_prompt}

    logger.info(
        "Running optimization (task_lm=%s, reflection_lm=%s)...", TASK_LM, REFLECTION_LM
    )
    start = datetime.now()

    result: object = gepa.optimize(  # type: ignore[misc]
        seed_candidate=seed_candidate,
        trainset=trainset,
        valset=valset,
        task_lm=TASK_LM,
        reflection_lm=REFLECTION_LM,
        max_metric_calls=MAX_METRIC_CALLS,
    )

    elapsed = (datetime.now() - start).total_seconds()
    logger.info("Optimization complete in %.1fs", elapsed)

    best_candidate: dict[str, str] = result.best_candidate  # type: ignore[attr-defined]
    logger.info("Optimized prompt:\n%s", best_candidate.get("system_prompt", str(best_candidate)))

    write_report(seed_prompt, result, elapsed)


if __name__ == "__main__":
    main()
