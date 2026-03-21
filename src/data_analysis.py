"""
Data analysis for the GEPA prompt optimization pipeline.
Loads train.csv and test.csv, produces a detailed report written to reports/.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.constants import TRAIN_CSV, TEST_CSV, SEED_PROMPT_FILE, ANALYSIS_REPORT, REPORTS_DIR


class SplitStats(TypedDict):
    name: str
    num_examples: int
    input_len_min: int
    input_len_max: int
    input_len_avg: float
    output_len_min: int
    output_len_max: int
    output_len_avg: float
    input_tok_avg: float
    output_tok_avg: float
    total_tokens: int
    samples: list[dict[str, str]]


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))  # type: ignore[return-value]


def token_estimate(text: str) -> int:
    """Rough token count: ~4 chars per token."""
    return max(1, len(text) // 4)


def analyse_split(rows: list[dict[str, str]], name: str) -> SplitStats:
    inputs  = [r["input"]  for r in rows]
    outputs = [r["output"] for r in rows]

    input_lens  = [len(s) for s in inputs]
    output_lens = [len(s) for s in outputs]
    input_toks  = [token_estimate(s) for s in inputs]
    output_toks = [token_estimate(s) for s in outputs]

    return SplitStats(
        name=name,
        num_examples=len(rows),
        input_len_min=min(input_lens),
        input_len_max=max(input_lens),
        input_len_avg=sum(input_lens) / len(input_lens),
        output_len_min=min(output_lens),
        output_len_max=max(output_lens),
        output_len_avg=sum(output_lens) / len(output_lens),
        input_tok_avg=sum(input_toks) / len(input_toks),
        output_tok_avg=sum(output_toks) / len(output_toks),
        total_tokens=sum(input_toks) + sum(output_toks),
        samples=rows[:3],
    )


def format_report(train_stats: SplitStats, test_stats: SplitStats, seed_prompt: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 70,
        "GEPA PROMPT OPTIMIZATION — DATA ANALYSIS REPORT",
        f"Generated: {ts}",
        "=" * 70,
        "",
        "SEED PROMPT",
        "-" * 70,
        seed_prompt.strip(),
        "",
    ]

    for stats in (train_stats, test_stats):
        lines += [
            f"{stats['name'].upper()} SET",
            "-" * 70,
            f"  Examples          : {stats['num_examples']}",
            f"  Input  length     : min={stats['input_len_min']}  max={stats['input_len_max']}  avg={stats['input_len_avg']:.1f} chars",
            f"  Output length     : min={stats['output_len_min']}  max={stats['output_len_max']}  avg={stats['output_len_avg']:.1f} chars",
            f"  Avg input tokens  : {stats['input_tok_avg']:.1f}",
            f"  Avg output tokens : {stats['output_tok_avg']:.1f}",
            f"  Total tokens      : {stats['total_tokens']}",
            "",
            "  Sample examples (first 3):",
        ]
        for i, row in enumerate(stats["samples"], 1):
            lines.append(f"    [{i}] Input  : {row['input'][:80]}")
            lines.append(f"        Output : {row['output'][:80]}")
        lines.append("")

    lines += [
        "COMBINED STATISTICS",
        "-" * 70,
        f"  Total examples : {train_stats['num_examples'] + test_stats['num_examples']}",
        f"  Total tokens   : {train_stats['total_tokens'] + test_stats['total_tokens']}",
        f"  Train/Test split: {train_stats['num_examples']} / {test_stats['num_examples']}",
        "",
        "=" * 70,
        "END OF REPORT",
        "=" * 70,
    ]
    return "\n".join(lines)


def main():
    REPORTS_DIR.mkdir(exist_ok=True)

    print("Loading data...")
    train_rows = load_csv(TRAIN_CSV)
    test_rows  = load_csv(TEST_CSV)
    seed_prompt = SEED_PROMPT_FILE.read_text(encoding="utf-8")

    print(f"  Train: {len(train_rows)} examples")
    print(f"  Test : {len(test_rows)} examples")

    train_stats = analyse_split(train_rows, "train")
    test_stats  = analyse_split(test_rows,  "test")

    report = format_report(train_stats, test_stats, seed_prompt)

    _ = ANALYSIS_REPORT.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {ANALYSIS_REPORT}")
    print(report)


if __name__ == "__main__":
    main()
