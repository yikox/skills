---
name: skills 仓库架构
status: implemented
review_status: reviewed
---

# skills 仓库架构

## Scope

本仓库是 modular-programming 技能套件的源仓库：九个 modular-* 工作流技能、共享规则与模板、确定性审计脚本、高级架构图渲染工具，以及把套件分发到各 agent skills 目录（`~/.claude/skills` 等）的安装脚本。运行环境为支持 SKILL.md 技能协议的 agent（Claude Code / Codex 等）+ Python 3 标准库 + bash。无外部服务依赖。

## Module Map

| Module | Form | Kind | Responsibility | Status |
| --- | --- | --- | --- | --- |
| workflow-skills | atomic | config-rule | 九个技能入口 SKILL.md，定义工作流执行规则 | implemented |
| shared-references | atomic | config-rule | 跨技能共享的规则语料（工作流/存储/评审/图格式/模块化方法论与评估） | implemented |
| shared-assets | atomic | resource-file | 文档模板与渲染示例夹具 | implemented |
| audit-checker | atomic | function-flow | 项目记忆一致性的确定性检查脚本 | implemented |
| graph-tooling | atomic | function-flow | 高级架构图 JSON 渲染器与本地预览服务 | implemented |
| installer | atomic | function-flow | 技能套件安装/同步脚本 | implemented |

## Advanced Architecture Graph

- Source: `architecture/graphs/current-project.arch.json`
- Rendered: `architecture/rendered/current-project-architecture.html`
- 图是本仓库维护的高级可视化产物；默认 AI 工作流只要求 `main-design.md` 与 `modules/*.md`。

## Cross-Module Flow

- 技能执行流：agent 加载 workflow-skills 中某技能 → 读 shared-references 规则与 shared-assets 模板 → 按需触发 audit-checker（一致性检查）或 graph-tooling（高级可视化渲染）。
- 分发流：installer 把技能目录与 `_shared` 平铺复制到目标 skills 目录，保证 `../_shared/` 相对引用在安装后依然成立。

## Shared Constraints

- 运行时依赖仅 Python 3 标准库与 bash；不引入第三方包。
- 规则文本（shared-references）与检查器硬编码词表（audit-checker）必须同一变更内同步。
- 无主路径（不属于任何模块的 behavior-bearing 之外内容）：`docs/**`（superpowers 流程存档）、`PM/**`（本仓库自身的项目记忆）。
- 本仓库自身用 modular 工作流管理，docs-language 为 `zh`，confirmation 档位为 `standard`。

## Open Questions

- modular-autopilot 的端到端与负路径演练尚未执行（见 ADR-2026-07-03 Follow-Up）。

## Review Notes

- Review status: reviewed（2026-07-03 依据现有代码建立基线，与 checker 校验一致）
