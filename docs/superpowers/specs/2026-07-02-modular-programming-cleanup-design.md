# Modular Programming 完善与历史清理设计

日期：2026-07-02
状态：accepted

## 背景

`architecture-design` 和 `project-memory` 两套旧 skill 已融合为 `modular-programming/`
（7 个 skill + `_shared`）。核心工具内容（渲染脚本、图格式文档、模块分类文档、示例）
已原样迁移。剩余工作：补齐迁移缺口、优化流程细节、删除旧目录。

## 范围

### 1. 新增 `_shared/references/pm-maintenance-rules.md`

合并旧 `project-memory/pm-audit-memory/references/pm-archive-rules.md`（54 行）与
`pm-compression-rules.md`（119 行，未提交），去重后形成一份 PM 维护规则：

- 归档触发时机与归档必须保留的字段（final status、design paths、evidence）；
- 压缩触发条件与压缩不可丢失的信息；
- 措辞对齐新 schema（active task / backlog / design index / L0-L3）。

引用方：`modular-status`、`modular-audit` 的 Required References。

### 2. 流程与细节修复

- `modular-workflow-rules.md` 新增 **Session Entry** 节：任何工作开始前先读
  `project-management.md` 与 `architecture/main-design.md`，优先接续 active task。
- `modular-workflow-rules.md` 新增**路由速查表**：请求类型 → skill + 级别 + 产物。
- 七个 SKILL.md description 去 "Codex" 硬编码，改为 agent 中性措辞；README 同步。
- `modular-change`：L2 路径显式补 PM start；baseline 更新步骤加重渲染架构图提醒。
- `modular-init`：项目 AI 规则片段加入 session-entry 规则。

### 3. 迁移渲染器自身架构文档

`architecture-design/architecture/modules/` 中描述渲染脚本内部结构的 12 个模块文档
（graph-model、layout-engine、svg-renderer、render-runtime、rules-layer、format-spec、
module-kind-taxonomy、parser-loader、html-output、cli-orchestrator、diagnostics、
agent-ui-metadata）迁至 `modular-programming/_shared/scripts/renderer-docs/`，
附 README 索引，路径/名称对齐新位置。

不迁移：旧 skill 包装相关模块文档（skill-package、skill-instructions、
examples-fixtures、fixtures-output、rendered-artifacts）、`dist/` 渲染产物、
指向旧仓库结构的 `current-project.arch.json`。

### 4. 清理与提交

- commit 1（完善）：上述新增/修改文件 + 本设计文档与相关 docs。
- commit 2（清理）：删除 `architecture-design/`、`project-memory/`、`scripts/`，
  连同其未提交修改一起丢弃；确认 install.sh 与 README 无残留引用。

## 验证

- `./install.sh --dry-run <tmp>` 通过且只安装新套件；
- `render_modular_graph.py _shared/examples/system-overview.arch.json` 渲染无告警；
- 仓库内 `pm-*` / `architecture-design` / `Codex` 残留仅限 migration-rules 中刻意
  保留的 legacy 名称映射。

## 不做（YAGNI）

- 不改造 `check_pm_project.py` 审计脚本（未来独立任务）。
- 不为本仓库自建 PM/architecture dogfood（未来独立任务）。
- 不重写 git 提交历史。
