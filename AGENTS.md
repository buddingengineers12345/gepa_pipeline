# AGENTS.md - Gepa Pipeline

> Canonical, model-agnostic agent guide. CLAUDE.md / GEMINI.md / CURSOR.md are
> thin wrappers that point here. Edit shared knowledge in THIS file only.

## What this repo is

The **GEPA Prompt Optimization Pipeline** is an end-to-end system for iteratively improving natural language prompts used by language models on problem-solving tasks. It uses the GEPA framework with local Ollama inference (no cloud APIs required by default) to analyze datasets, optimize prompts through multi-candidate generation, and produce detailed reports with before/after comparisons.

## Behavioral guidelines

Bias toward caution over speed; use judgment on trivial tasks.

- **Think before coding** - state assumptions; surface multiple interpretations instead of silently picking one; ask when unclear.
- **Simplicity first** - minimum code that solves the problem; nothing speculative, no unrequested abstraction or flexibility.
- **Surgical changes** - touch only what the task requires; match existing style; don't refactor what isn't broken; remove only orphans your change creates.
- **Goal-driven execution** - define a verifiable success check before starting; loop until it passes.

## Context loading (progressive disclosure)

1. Read this file first.
2. Load a deeper reference ONLY when the task touches its area:
   | When the task involves... | Read |
   |---|---|
   | Adding or modifying Python modules | `src/constants.py` for model/config setup |
   | Shell pipeline execution | `pipeline.sh` and the [README.md](./README.md) troubleshooting section |

3. Do not bulk-load all references - avoid context flooding.

## Memory - AgentMemory only

This repo uses AgentMemory (MCP server `localhost:3111`, project-scoped TEAM_ID `gepa_pipeline`).

- Session start: call `memory_recall` with the task/goal.
- During work: call `memory_save` for durable decisions, bug root causes, conventions, gotchas (types: pattern | architecture | bug | workflow | preference).
- Session end: call `memory_save` with lessons learned.
- Do NOT create, read, or append to `MEMORY.md`, `CONFLICTS.md`, `NOTES.md`, or any markdown "memory" / "conflict log" file. Cross-session memory and conflict tracking live in AgentMemory exclusively.

## Repo-specific guidance

**Stack**: Python 3.10+, uv package manager, Pydantic, GEPA framework, LiteLLM, local Ollama inference.

**Key files**:
- `src/constants.py` - model and Ollama configuration, budget settings
- `src/data_analysis.py` - dataset statistics generation
- `src/optimization.py` - GEPA optimization pipeline (dual LM: task + reflection)
- `pipeline.sh` - main orchestrator with --analysis / --optimization / --all modes
- `data/` - train.csv, test.csv, seed_prompt.txt (inputs)
- `reports/` - analysis and optimization report outputs

**Common tasks**:
- Reconfigure models: edit `TASK_LM`, `REFLECTION_LM`, `OLLAMA_HOST` in `src/constants.py`
- Adjust optimization budget: `MAX_METRIC_CALLS` in `src/constants.py`
- Run pipeline: `./pipeline.sh [--analysis | --optimization | --all]`
- Import environment: source `.env` or rely on AgentMemory for persisted TEAM_ID injection

## AgentMemory Insights (snapshot 2026-05-21)

### Architecture & Design
_No durable insights surfaced this snapshot._

### Working Preferences & Conventions
- AgentMemory is project-scoped by TEAM_ID `gepa_pipeline`; all cross-session memory queries via MCP use explicit `project` parameter or REST to localhost:3111.

### Bugs, Incidents & Gotchas
_No durable insights surfaced this snapshot._

### Active Projects / WIP Context
_No durable insights surfaced this snapshot._
