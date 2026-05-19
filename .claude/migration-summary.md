# AI-Governance Migration Summary

**Date**: 2026-05-19  
**Repository**: gepa_pipeline  
**Scope**: Markdown-only AI-governance refactor

## Files Created

1. `/home/engineer/workspace/gepa_pipeline/AGENTS.md` — Canonical agent guide (model-agnostic)
2. `/home/engineer/workspace/gepa_pipeline/CLAUDE.md` — Claude-specific thin wrapper
3. `/home/engineer/workspace/gepa_pipeline/GEMINI.md` — Gemini-specific thin wrapper
4. `/home/engineer/workspace/gepa_pipeline/CURSOR.md` — Cursor-specific thin wrapper

## AgentMemory Configuration

- **TEAM_ID**: `gepa_pipeline`
- **Scope**: Project-scoped memory isolation via AGENTMEMORY_TEAM_ID in `.env.agentmemory`
- **No MEMORY.md/CONFLICTS.md files**: This repo had no prior memory files; all cross-session tracking will use AgentMemory exclusively

## Context Loading Table

| When the task involves… | Read |
|---|---|
| Adding or modifying Python modules | `src/constants.py` for model/config setup |
| Shell pipeline execution | `pipeline.sh` and the [README.md](./README.md) troubleshooting section |

## Validation Results

✅ No references to `MEMORY.md` or `CONFLICTS.md` in any instruction file  
✅ All relative links in the 4 root files resolve correctly  
✅ Each wrapper file is ≤ ~20 lines  
✅ AGENTS.md uses canonical TEAM_ID `gepa_pipeline`  
✅ No source code changes; markdown-only refactor  
✅ No new directory trees created (`.claude/` already existed)

## Anomalies

None. The repo had no prior markdown instruction files, so no cleanup or archival was needed. All reference docs live in the codebase itself (README.md, src/constants.py, etc.).
