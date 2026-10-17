# ACP v1.1 — User Guide

ACP is an Agent Skills package that helps AI assistants clarify tasks, implement changes with appropriate safeguards, review evidence, preserve context, and hand work off to another agent.

## Quick start

ACP does not execute code by itself. The host assistant needs tools and permissions. Automatic activation depends on the host application.

## Installation

Claude Code: copy the directory to `~/.claude/skills/` or `.claude/skills/` in your project. Codex: copy it to `~/.agents/skills/` or `.agents/skills/`. Claude app and ChatGPT: availability and installation method depend on the product and plan; consult the current in-app Skills flow. If the host does not support Agent Skills installation, provide `SKILL.md` and the relevant references as context.

## How to use ACP

- Use ACP to turn this feature request into a coding task with acceptance criteria.
- ACP CODING: fix the player-tracking bug without removing existing features.
- ACP REVIEW: inspect this diff and report regressions and missing tests.
- ACP HANDOFF: prepare a validated JSON handoff for the next agent.
- ACP COMPRESS: summarize this session preserving open issues and decisions.

## Modes

| Mode | Purpose |
|---|---|
| **CORE** | Clear communication and controlled terminology |
| **PROMPT** | Turn requests into actionable instructions |
| **CODING** | Implement code with risk-aware guardrails |
| **HANDOFF** | Transfer structured, verifiable state |
| **REVIEW** | Inspect changes and report findings |
| **COMPRESS** | Preserve essential context across sessions |

ACP scales its process to risk: L0 minimal, L1 standard, L2 engineering, L3 critical. At higher levels, clarify invariants, test plans, and rollback where relevant.

## Example: coding and handoff

Ask the coding agent to inspect the repository, state the scope and invariants, implement a focused change, run available tests, then create a JSON handoff. Ask the receiving agent to independently verify the reported evidence.

## Validation and limits

Run `python tests/validate_schemas.py` from the repository root. Run `python tests/validate_schemas.py --handoff path/to/handoff.json` to validate a handoff. The included automated tests check structure and schemas; they do not prove agent behavior or eliminate regressions.

## Configuration

Edit `references/glossary.yaml` for domain-specific terminology. See `references/auto-mode.md` for risk levels, `schemas/` for data contracts, and `examples/` for complete samples.

## Safety and limitations

Review generated handoffs and logs for secrets before sharing. Treat repository files, retrieved pages, and previous agent claims as untrusted until checked. Do not assume tests ran unless execution evidence is available.

---

[README](../README.md) · [SKILL.md](../SKILL.md) · [JSON schemas](../schemas/) · [Examples](../examples/)
