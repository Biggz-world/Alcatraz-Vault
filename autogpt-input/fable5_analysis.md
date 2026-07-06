# Fable 5 Traces — Analysis

**Source:** Glint Research / TeichAI
**Dataset:** `fable5_cot_merged.jsonl` (4,665 traces)
**File:** `~/Downloads/fable5_cot_merged.jsonl`
**Date analyzed:** 2026-07-05

## Overview

A compact, high-signal corpus of **Fable 5 coding-agent traces** converted into Hugging Face Agent Traces / Pi-compatible sessions. Captures the full reasoning-action loop of `claude-fable-5` agents across 60 source sessions.

## Key Stats

| Metric | Value |
|--------|-------|
| Total traces | 4,665 |
| Source sessions | 60 |
| Median CoT length | 2,562 chars |
| Average context length | 6,837 chars |
| Tool-use rate | 74% |
| Text output rate | 26% |

## Tool Distribution

| Tool | Share |
|------|-------|
| Bash | 45.9% |
| Edit | 29.7% |
| Read | 13.5% |
| WebSearch | 2.7% |
| PowerShell | 2.7% |
| TaskUpdate | 2.7% |
| Other (MCP, etc.) | 2.7% |

## Behavioral Patterns

| Pattern | Prevalence |
|---------|-----------|
| Plans before action | 86% |
| Refers to previous context | 82% |
| Reads/inspects first | 78% |
| Handles errors/recovery | 78% |
| Direct action without plan | 14% |

## Reasoning Style

The Fable 5 traces exhibit a distinct **plan-then-execute** pattern:

1. **Context Assessment** — reads current state, checks files, inspects environment
2. **Deliberate Planning** — 2,500+ char structured reasoning before each action
3. **Tool Selection** — prefers Bash for broad exploration, Edit for targeted changes
4. **Post-Action Verification** — reads results, checks for errors, adjusts
5. **Iterative Refinement** — refers back to earlier steps, builds on previous context

## Origin Distribution

| Source | Traces |
|--------|--------|
| Local (lane's machines) | 3,712 |
| Imported HF slice | 953 |

## Fine-Tuned Model

A custom fine-tune exists in LM Studio:
- `huihui-gemma-4-12b-coder-fable5-composer2.5-v1-abliterated` (Q4_K_S)
- Base: Gemma 4 12B
- Trained on Fable 5 traces + Composer 2.5 data
- Ready to use at `http://127.0.0.1:1234/v1`

## Usage

- **SFT training:** Load `fable5_cot_merged.jsonl` with `context` as input and `completion` as target
- **Agent loop reproduction:** Use the `fable5-reasoning` skill for behavioral prompting
- **Pi-compatible:** Each trace maps to HF Agent Traces format for Data Studio

## File Format

Each JSONL row:
- `uid` — unique row identifier
- `session` — source session UUID
- `model` — always `claude-fable-5`
- `context` — prompt + prior transcript
- `cot` — reasoning trace (Chain-of-Thought)
- `output_type` — `tool_use` or `text`
- `output` — tool call details or text payload
- `completion` — full serialized completion
- `origin` — provenance (`local` or `hf`)

## Paths

- Raw data: `C:\Users\o0DoU\Downloads\fable5_cot_merged.jsonl`
- LM Studio model: `huihui-gemma-4-12b-coder-fable5-composer2.5-v1-abliterated`
- Skill: `fable5-reasoning` (loaded by Hermes for behavioral prompting)
