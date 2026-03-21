#!/usr/bin/env bash
# pipeline.sh — Run analysis, optimization, or both.
#
# Usage:
#   ./pipeline.sh --analysis          # run data analysis only
#   ./pipeline.sh --optimization      # run prompt optimization only
#   ./pipeline.sh --all               # run both (default)
#   ./pipeline.sh                     # same as --all
#
# Prerequisites:
#   - uv installed  (https://docs.astral.sh/uv/)
#   - ollama running locally with models pulled:
#       ollama pull qwen2.5:7b
#       ollama pull qwen2.5:72b

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPORTS_DIR="$ROOT/reports"
LOG_FILE="$REPORTS_DIR/pipeline_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$REPORTS_DIR"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

# ── uv environment bootstrap ──────────────────────────────────────────────────
if [ ! -d "$ROOT/.venv" ]; then
  log "Creating virtual environment with uv..."
  uv venv "$ROOT/.venv"
fi
log "Syncing dependencies..."
uv sync --project "$ROOT" --quiet
PYTHON="$ROOT/.venv/bin/python"

# ── Argument parsing ──────────────────────────────────────────────────────────
RUN_ANALYSIS=false
RUN_OPTIMIZATION=false

case "${1:-}" in
  --analysis)     RUN_ANALYSIS=true ;;
  --optimization) RUN_OPTIMIZATION=true ;;
  --all | "")     RUN_ANALYSIS=true; RUN_OPTIMIZATION=true ;;
  *)
    echo "Usage: $0 [--analysis | --optimization | --all]"
    exit 1
    ;;
esac

log "Pipeline started"
log "Reports dir : $REPORTS_DIR"

if $RUN_ANALYSIS; then
  log "── Running data analysis ──"
  "$PYTHON" "$ROOT/src/data_analysis.py" 2>&1 | tee -a "$LOG_FILE"
  log "── Data analysis complete ──"
fi

if $RUN_OPTIMIZATION; then
  log "── Running prompt optimization ──"
  "$PYTHON" "$ROOT/src/optimization.py" 2>&1 | tee -a "$LOG_FILE"
  log "── Optimization complete ──"
fi

log "Pipeline finished. Log: $LOG_FILE"
