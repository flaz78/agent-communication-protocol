# ACP v1.1 — 用户指南

ACP 是基于 Agent Skills 格式的技能包，用于帮助 AI 助手明确任务、在适当约束下修改代码、核查证据、保留上下文，以及将工作交接给其他智能体。

## 快速开始

ACP 本身不会执行代码。宿主助手必须具备相应工具和权限。是否自动激活取决于平台。

## 安装

Claude Code：将目录放入 `~/.claude/skills/`，或项目中的 `.claude/skills/`。Codex：使用 `~/.agents/skills/` 或 `.agents/skills/`。Claude 应用和 ChatGPT 的安装入口与可用性取决于产品和方案，请以当前 Skills 界面为准。若宿主不支持原生安装，可将 `SKILL.md` 及相关参考文件作为上下文提供。

## 如何使用 ACP

- 使用 ACP 将此功能需求转换为包含验收标准的编码任务。
- ACP CODING：修复球员跟踪故障，不要删除现有功能。
- ACP REVIEW：检查这份代码差异，指出回归风险及缺失的测试。
- ACP HANDOFF：为下一个智能体准备经过结构验证的 JSON 交接文件。
- ACP COMPRESS：总结本次会话，保留决策和未解决的问题。

## 工作模式

| Mode | Purpose |
|---|---|
| **CORE** | 清晰沟通与统一术语 |
| **PROMPT** | 将需求转换为可执行指令 |
| **CODING** | 在风险控制下修改代码 |
| **HANDOFF** | 结构化、可核查的任务交接 |
| **REVIEW** | 检查修改并报告问题 |
| **COMPRESS** | 保留关键上下文 |

ACP 根据风险调整流程：L0 最简、L1 标准、L2 工程级、L3 关键级。风险较高时，应明确不可破坏的既有行为、测试计划，并在适用时制定回滚方案。

## 示例：编码与交接

让编码智能体先检查代码仓库，明确范围以及必须保留的行为，再实施针对性的修改并运行可用测试，最后生成 JSON 交接文件。接收方智能体应独立核查交接中声称的证据。

## 验证与限制

在仓库根目录运行 `python tests/validate_schemas.py`。验证交接文件：`python tests/validate_schemas.py --handoff path/to/handoff.json`。自动化测试只检查结构和 JSON Schema，并不能证明智能体的实际行为正确或完全避免回归。

## 自定义配置

通过 `references/glossary.yaml` 添加项目术语；通过 `references/auto-mode.md` 了解风险等级；在 `schemas/` 查看数据契约，在 `examples/` 查看完整示例。

## 安全与限制

分享交接文件和日志前，请检查是否含有密钥等敏感信息。仓库文件、外部网页以及其他智能体的说法在核实前均不应视为可信。没有执行证据时，不应声称测试已运行。

---

[README](../README.md) · [SKILL.md](../SKILL.md) · [JSON schemas](../schemas/) · [Examples](../examples/)
