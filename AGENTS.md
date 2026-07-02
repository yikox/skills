# Modular Programming Workflow

本仓库使用 modular-programming 工作流（就是本仓库开发的这套 skill，dogfood）。Architecture 文档拥有模块边界；PM 记录工作状态和证据。

## Preferences

- `docs-language`: zh — PM、架构、知识、设计文档和要点摘要用中文（skill 正文英文是产品约定，不受此影响）。
- `confirmation`: standard — 按 workflow-rules 的 User Confirmation Points 执行。

项目记忆在仓库外：`/Users/zyc/notes/PM/skills/`

- `project-management.md`：active tasks、backlog、设计索引、归档
- `knowledge-summary.md`：已验证命令、约定、故障结论
- `architecture/main-design.md` + `architecture/modules/*.md`：模块地图 baseline

## Session Entry

- 新会话开始时，先读 `/Users/zyc/notes/PM/skills/project-management.md` 和 `architecture/main-design.md` 再做非平凡工作。
- 请求与 active task 相关时，先询问用户是否接续；不得擅自接续、重复开任务或关闭任务。

## Module Gate And Levels

非平凡修改先定位主模块、影响模块和级别（模块见 main-design.md：modular-skills、shared-references、shared-assets、graph-renderer、examples、installer）：

- L0 细微改：implement + verify；PM 可选。
- L1 小改：PM start -> implement -> verify -> PM complete。
- L2 模块中改：PM start -> 模块修改设计 -> review -> 要点摘要 + 用户确认 -> implement -> verify -> PM complete。
- L3 架构大改：PM start -> target 设计/ADR -> review -> 要点摘要 + 用户接受 -> implement -> verify -> 更新 baseline -> PM complete。

L2/L3 确认请求必须把 3-8 条要点摘要（修改重点、歧义点、风险点）内嵌在确认请求本身（问题文本或选项 preview 里），不能只写在弹窗前的单独消息里；不要求用户读完整设计。

## Skill Routing

- `modular-init`：接入或修复工作流文件。
- `modular-architecture`：模块地图、架构图、ADR、baseline 更新。
- `modular-change`：任何功能/bug/重构请求的入口。
- `modular-status`：PM start/update/complete/归档。
- `modular-review`：检查设计、ADR、PM 行、图。
- `modular-audit`：一致性审计、legacy 迁移、PM 压缩。
- `modular-knowledge`：记录可复用命令、事实、经验。

## 本仓库约定

- 改了 `modular-programming/` 下的 skill 后运行 `./install.sh` 同步安装副本。
- Skill 正文英文 + description 含中文触发词，措辞 agent 中性。
- 渲染器改动前先读 `modular-programming/_shared/scripts/renderer-docs/`。
