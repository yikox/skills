---
name: skills 仓库架构
status: implemented
review_status: reviewed
---

# skills 仓库架构

## Scope

本仓库是 modular-programming 技能套件的源仓库：十个 modular-* 工作流技能、共享规则与模板、确定性审计脚本、高级架构图渲染工具，以及把套件分发到各 agent skills 目录（`~/.claude/skills` 等）的安装脚本。运行环境为支持 SKILL.md 技能协议的 agent（Claude Code / Codex 等）+ Python 3 标准库 + bash。无外部服务依赖。

套件按语言分层为 `<lang>/modular-programming/`（`lang` ∈ {en, zh}）。`en/` 为主/源，本 baseline 与 `code_paths` 均以 `en/` 描述；`zh/` 是 `en/` 的中文翻译镜像，结构逐目录对等，不单独维护 baseline。可执行代码（`*.py`）与受控词表 token 保持英文单源，两语言目录内容一致（详见 Shared Constraints）。安装脚本按语言参数从对应目录分发。

## Module Map

| Module | Form | Kind | Responsibility | Status |
| --- | --- | --- | --- | --- |
| workflow-skills | atomic | config-rule | 十个技能入口 SKILL.md，定义工作流执行规则 | implemented |
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
- L2/L3 流程改造流：用户接受架构 patch 摘要后，在功能分支的第一颗 commit 中先把目标模块地图写入 `architecture/main-design.md` / `architecture/modules/*.md` 与 PM active 行；后续实现提交必须让代码与该目标地图收敛，合并前完成验证与 PM closeout。main 分支只保留已实现且与代码一致的模块地图。

## Shared Constraints

- 运行时依赖仅 Python 3 标准库与 bash；不引入第三方包。
- 受控词表以 shared-references 的 `vocab.md` 为单一事实源，audit-checker 启动时解析（不再硬编码）；drift-guard 测试保证 vocab.md 与检查器内置 fallback 一致。
- 无主路径（不属于任何模块的 behavior-bearing 之外内容）：`docs/**`（superpowers 流程存档）、`PM/**`（本仓库自身的项目记忆）、`zh/**`（`en/**` 的中文翻译镜像，随 en 模块同步，不单独建模块）。
- 语言镜像约束：`zh/modular-programming` 与 `en/modular-programming` 逐目录对等；只翻译散文，`*.py` 脚本与 vocab/front-matter 的机器 token（module_form/module_kind/relation_kind/status 等取值）保持英文单源，两语言目录逐字一致，否则 audit-checker 对 zh 失效。
- 本仓库自身用 modular 工作流管理，docs-language 为 `zh`，confirmation 档位为 `standard`。
- 默认不再为 L2/L3 长期维护独立变更设计文件。分支承载已接受的 architecture patch；独立 proposal / changes 文件只在复杂、跨天、需离线审阅或非 git 协作时使用。完成后过程文件默认归档，日常入口不读取 archive。

## Open Questions

- modular-autopilot 的端到端与负路径演练尚未执行（见 ADR-2026-07-03 Follow-Up）。
