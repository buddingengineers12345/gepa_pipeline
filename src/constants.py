"""
Key constants for the GEPA prompt optimization pipeline.
Modify these values to configure the pipeline.
"""

import os
from pathlib import Path

# ── Directories ───────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"
SRC_DIR = ROOT_DIR / "src"

# ── Data files ────────────────────────────────────────────────────────────────
TRAIN_CSV = DATA_DIR / "train.csv"
TEST_CSV = DATA_DIR / "test.csv"
SEED_PROMPT_FILE = DATA_DIR / "seed_prompt.txt"

# ── Language model settings ───────────────────────────────────────────────────
# Uses Ollama local inference. Ensure `ollama serve` is running.
# Pull models first:
#   ollama pull qwen3:1.7b
#   ollama pull gpt-oss:20b
TASK_LM = "ollama/qwen3:1.7b"  # Lightweight model — evaluates prompt quality
REFLECTION_LM = "ollama/qwen3:8b"  # Large model — generates improved prompts
# REFLECTION_LM = "ollama/gpt-oss:20b"  # Large model — generates improved prompts

# Ollama server URL (default: http://localhost:11434)
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# ── Optimization settings ─────────────────────────────────────────────────────
MAX_METRIC_CALLS = 100  # Budget: total LM calls allowed during optimisation
VAL_SPLIT = 0.2  # Fraction of training data used as validation

# ── Report file names ─────────────────────────────────────────────────────────
ANALYSIS_REPORT = REPORTS_DIR / "data_analysis_report.txt"
OPTIMIZATION_REPORT = REPORTS_DIR / "optimization_report.txt"

# ── OpenAI API key — not required for Ollama (leave unset) ───────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
