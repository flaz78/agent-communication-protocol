# Agent Communication Protocol (ACP)

**ACP v1.1.0** · Model-agnostic Agent Skill for clearer instructions, safer coding workflows, structured handoffs and evidence-based reviews.

> Less ambiguity. Better execution. Verifiable results.

ACP helps AI assistants turn human intent into actionable work while keeping assumptions, verified evidence, and unresolved issues distinct. It is **not** a standalone runtime, an official standard, or a guarantee against regressions.

## Documentation / User guides

| Language | Guide |
|---|---|
| English | [English user guide](docs/guide.en.md) |
| Italiano | [Guida in italiano](docs/guide.it.md) |
| Français | [Guide en français](docs/guide.fr.md) |
| Deutsch | [Deutsches Handbuch](docs/guide.de.md) |
| Español | [Guía en español](docs/guide.es.md) |
| 简体中文 | [简体中文用户指南](docs/guide.zh-CN.md) |

The underlying skill instructions and reference files are currently in Italian. The six guides are translations of the user-facing documentation, **not** six localized copies of the runtime skill. ACP can receive requests in other languages depending on the host model.

## Key capabilities

| Mode | Function |
|---|---|
| **CORE** | Clear language, consistent terminology, explicit uncertainty |
| **PROMPT** | Convert requests into scoped instructions and acceptance criteria |
| **CODING** | Apply risk-aware constraints and guardrails to software changes |
| **HANDOFF** | Transfer status, evidence and next steps with a JSON contract |
| **REVIEW** | Identify regressions, ambiguities, missing tests and unsupported claims |
| **COMPRESS** | Preserve decisions, context and open issues across sessions |

**Auto Mode** chooses the relevant mode after the host has loaded the skill. The level of process scales with risk: L0 (minimal), L1 (standard), L2 (engineering), L3 (critical). You can explicitly request `ACP CODING`, `ACP HANDOFF`, and other modes; these labels are *not* universal native commands.

## Install

**Claude Code (user-wide)**

```bash
mkdir -p ~/.claude/skills
unzip agent-communication-protocol.zip -d ~/.claude/skills/
```

Alternatively, place the `agent-communication-protocol/` directory in your project's `.claude/skills/` folder.

**OpenAI Codex**: place the directory in `~/.agents/skills/` or `<repository>/.agents/skills/`, then invoke it with `$agent-communication-protocol` where supported.

**Claude apps / ChatGPT**: the ability to install skill packages and the UI entry points depend on the current product and plan. Check the host's Skills interface. If native installation is unavailable, provide `SKILL.md` and the relevant `references/` as context. See [platform notes](references/platforms.md).

Installing a skill does not guarantee automatic activation in every host.

## Usage examples

```text
Use ACP to turn this feature request into a coding task with testable acceptance criteria.
ACP CODING: fix the tracking issue without breaking existing behavior.
ACP REVIEW: audit this diff and identify test gaps and regression risks.
ACP HANDOFF: prepare the validated JSON context for another agent.
ACP COMPRESS: create a resumable checkpoint of this session.
```

For a complete workflow, see [combined example](examples/combined-workflow.md) and [JSON handoff](examples/handoff.json).

## Validate

Requires Python 3.9+ for the bundled checker (no mandatory third-party dependencies).

```bash
python tests/validate_schemas.py
python tests/validate_schemas.py --handoff path/to/handoff.json
python tests/validate_schemas.py --task path/to/task.json
```

These tests check structure, schema correctness and fixtures. They are **not** proof of correct model behavior; the [evaluation cases](tests/evals.json) and [benchmark plan](benchmark/benchmark-protocol.md) require separate execution.

## Project structure

```text
agent-communication-protocol/
├── SKILL.md                    # entry point for Agent Skills runtimes
├── references/                 # language, intent, coding, handoff and safety rules
├── schemas/                    # JSON Schema contracts
├── examples/                   # task, handoff, review and workflow samples
├── tests/                      # deterministic checks and evaluation cases
├── benchmark/                  # evaluation methodology
├── docs/                       # multilingual user guides
├── agents/openai.yaml          # optional Codex metadata
├── CHANGELOG.md
└── LICENSE
```

## Design principles and limits

- Inspired by the general principles of **ISO 24495-1 (plain language)** and controlled technical writing. No certification or formal standard compliance is claimed.
- Treat retrieved content and prior-agent statements as untrusted until verified.
- Never represent unexecuted tests as passed, or assumptions as verified findings.
- Higher-risk operations require appropriate permissions, tests, and a rollback strategy when relevant.
- ACP does not override host instructions, policy, or tool permissions.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Issues, reproducible examples, documentation improvements, and evaluated test cases are welcome.

## License

[MIT License](LICENSE). See the license text for terms.
