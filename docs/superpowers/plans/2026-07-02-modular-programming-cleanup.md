# Modular Programming 完善与历史清理 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 补齐 modular-programming 迁移缺口（PM 维护规则、会话入口规则、路由速查表、agent 中性措辞、渲染器文档），然后删除旧 skill 目录并分两个 commit 提交。

**Architecture:** 纯文档/仓库结构变更。新增 1 个 shared reference，修改 7 个 SKILL.md + 2 个 reference + README，迁移 12 个渲染器模块文档，最后 `git rm` 三个旧目录。

**Tech Stack:** Markdown、git、python3（仅验证渲染脚本）。

**Spec:** `docs/superpowers/specs/2026-07-02-modular-programming-cleanup-design.md`

## Global Constraints

- 所有新文字用 agent 中性措辞（"the agent" / 祈使句），不出现 "Codex"。
- 旧 skill 名（`pm-*`、`architecture-design`）只允许出现在 `migration-rules.md` 的 legacy 映射和 `modular-audit` 的旧 schema 检测描述里。
- 新内容中的路径引用一律指向 `modular-programming/_shared/...` 布局。
- 每个 commit 末尾带 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`。

---

### Task 1: 新增 pm-maintenance-rules.md 并接线

**Files:**
- Create: `modular-programming/_shared/references/pm-maintenance-rules.md`
- Modify: `modular-programming/modular-status/SKILL.md`（Required References + Archive 节）
- Modify: `modular-programming/modular-audit/SKILL.md`（Required References）

**Interfaces:**
- Consumes: 旧 `project-memory/pm-audit-memory/references/pm-archive-rules.md` 与 `pm-compression-rules.md` 的内容（合并去重的唯一来源）。
- Produces: reference 路径 `../_shared/references/pm-maintenance-rules.md`，后续 SKILL.md 以此路径引用。

- [ ] **Step 1: 写 pm-maintenance-rules.md**

结构（合并两份旧文件，按此大纲重组，替换旧 skill 名与旧路径）：

```markdown
# PM Maintenance Rules
（何时用：modular-status 归档、modular-audit 压缩检查）

## Archive Principles        ← 来自 pm-archive-rules「Principles」
## Archive Candidates        ← 来自「Archive Candidates」，pm-audit-memory → modular-audit
## What Not To Archive       ← 原文，状态词表保持与 storage-schema.md 一致
## Archive Sections          ← 来自「Suggested Sections」
## Design File Movement      ← 来自「File Movement」，pm-audit-memory → modular-audit
## Compression Triggers      ← 来自 pm-compression-rules「Trigger Signals」，删除 Plexus 项目专例，保留通用阈值（~25KB、Recent Updates >8-12 条等）
## Preserve In Main File     ← 原文
## Move Or Condense          ← 原文；目的地路径改为 storage-schema 布局（knowledge-summary.md、architecture/...、archives/project-management-history-YYYY.md）
## Archive File Format       ← 原文含模板代码块
## Compression Procedure     ← 原文；删除 check_pm_project.py 步骤，改为「完成后用 modular-review 检查变更的 PM」；报告 before/after 大小
## Safety Rules              ← 原文
```

- [ ] **Step 2: modular-status/SKILL.md 引用**

Required References 的 Read 列表追加一行：

```markdown
- `../_shared/references/pm-maintenance-rules.md` when archiving or compressing PM history.
```

Archive 节末尾追加一句：

```markdown
Follow `pm-maintenance-rules.md` for archive candidates, protected statuses, and compression.
```

- [ ] **Step 3: modular-audit/SKILL.md 引用**

Required References 追加：

```markdown
- `../_shared/references/pm-maintenance-rules.md` when checking archive candidates or history compression.
```

- [ ] **Step 4: 验证**

Run: `grep -rn "pm-maintenance-rules" modular-programming/ | sort`
Expected: 3 处引用（status、audit、文件自身不算）+ 文件存在。

- [ ] **Step 5: 不单独 commit**（并入 Task 5 的 commit 1）

### Task 2: workflow-rules 加 Session Entry 与路由速查表

**Files:**
- Modify: `modular-programming/_shared/references/modular-workflow-rules.md`

**Interfaces:**
- Produces: 「Session Entry」小节与「Routing Quick Reference」表，供 Task 3 的 modular-init AI 规则片段引用其规则语句。

- [ ] **Step 1: 在「Artifact Hierarchy」之后、「Module Gate」之前插入**

```markdown
## Session Entry

Before starting any non-trivial work in a project that uses this workflow:

1. Read `project-management.md` for active tasks, blockers, and current focus.
2. Read `architecture/main-design.md` for the current module map.
3. If the request continues an active task, resume that task instead of opening a duplicate.
4. If PM or architecture is missing or stale, repair it with `modular-init` or `modular-audit` before large changes.

## Routing Quick Reference

| Request shape | Skill | Typical level | Expected artifact |
| --- | --- | --- | --- |
| Set up / repair workflow files | `modular-init` | - | PM, knowledge, baseline architecture |
| Define or migrate module map, graphs, ADR | `modular-architecture` | - | baseline/target docs, graph, rendered diagram |
| Feature, bug fix, refactor, behavior change | `modular-change` | L0-L3 | level-specific path |
| Record start/progress/completion/archive | `modular-status` | L1-L3 | PM rows and evidence |
| Check a design, ADR, PM row, or graph | `modular-review` | - | review notes, fixes, open questions |
| Consistency check or legacy migration | `modular-audit` | - | audit report, migration gaps |
| Save reusable commands/facts/lessons | `modular-knowledge` | - | knowledge-summary entries |
```

- [ ] **Step 2: 验证**

Run: `grep -n "Session Entry\|Routing Quick Reference" modular-programming/_shared/references/modular-workflow-rules.md`
Expected: 两个标题都存在，位于 Module Gate 之前。

### Task 3: 去 Codex 硬编码 + 流程细节修复

**Files:**
- Modify: 7 个 `modular-programming/*/SKILL.md` 的 frontmatter description
- Modify: `README.md:3`
- Modify: `modular-programming/modular-change/SKILL.md`（L2 路径、baseline 步骤）
- Modify: `modular-programming/modular-init/SKILL.md`（step 7）

- [ ] **Step 1: description 去 Codex**

7 个 SKILL.md 中 `Use when Codex should` 全部替换为 `Use when the agent should`；`Codex` 其他出现处（如有）同样中性化。README 第 3 行 `用来让 Codex 按` 改为 `用来让 AI agent 按`。

Run: `grep -rn "Codex" README.md modular-programming/ | grep -v renderer-docs`
Expected: 无输出。

- [ ] **Step 2: modular-change L2 路径补 PM start**

`### L2 Module Change` 编号列表第 1 步前插入：

```markdown
1. Record PM start with primary module, impacted modules, level, and expected design path.
```

（原 1-5 顺延为 2-6。）

- [ ] **Step 3: modular-change baseline 步骤加重渲染提醒**

Workflow 第 9 步改为：

```markdown
9. Update architecture baseline only when durable module behavior, contract, relationship, or constraints changed; re-render affected graphs (see `modular-architecture` Baseline Update).
```

- [ ] **Step 4: modular-init step 7 加 session entry**

改为：

```markdown
7. Update AI collaboration docs with two short rules: start sessions by reading `project-management.md` and `architecture/main-design.md`; non-trivial work must pass the module gate and L1/L2/L3 work must record PM start and completion.
```

- [ ] **Step 5: 验证**

Run: `grep -c "PM start" modular-programming/modular-change/SKILL.md`
Expected: 计数比修改前 +1；重读 diff 确认无编号错乱。

### Task 4: 迁移渲染器架构文档

**Files:**
- Create: `modular-programming/_shared/scripts/renderer-docs/README.md`
- Create: `modular-programming/_shared/scripts/renderer-docs/<12 个模块文档>.md`（从 `architecture-design/architecture/modules/` 复制：graph-model、layout-engine、svg-renderer、render-runtime、rules-layer、format-spec、module-kind-taxonomy、parser-loader、html-output、cli-orchestrator、diagnostics、agent-ui-metadata）

- [ ] **Step 1: 复制 12 个文档**

```bash
mkdir -p modular-programming/_shared/scripts/renderer-docs
for f in graph-model layout-engine svg-renderer render-runtime rules-layer format-spec module-kind-taxonomy parser-loader html-output cli-orchestrator diagnostics agent-ui-metadata; do
  cp architecture-design/architecture/modules/$f.md modular-programming/_shared/scripts/renderer-docs/$f.md
done
```

- [ ] **Step 2: 修正文档内旧路径/旧名**

在 12 个文件内将 `render_arch_graph.py` → `render_modular_graph.py`，`scripts/render_arch_graph.py` 等旧相对路径 → `_shared/scripts/render_modular_graph.py`；指向未迁移模块文档（skill-package 等）的链接改为纯文字或删除。

Run: `grep -rn "render_arch_graph\|architecture-design" modular-programming/_shared/scripts/renderer-docs/`
Expected: 无输出。

- [ ] **Step 3: 写 README.md 索引**

```markdown
# Renderer Internal Architecture

Module docs for `render_modular_graph.py` (the architecture graph renderer).
Read these before modifying the renderer script.

| Doc | Covers |
| --- | --- |
| format-spec.md | `.arch.json` input contract |
| parser-loader.md | JSON loading and validation |
| graph-model.md | in-memory graph model |
| rules-layer.md | relation/level validation rules |
| module-kind-taxonomy.md | module kind semantics and colors |
| layout-engine.md | layout computation |
| svg-renderer.md | SVG output |
| html-output.md | HTML wrapper output |
| render-runtime.md | interactive runtime behavior |
| cli-orchestrator.md | CLI entry and pipeline |
| diagnostics.md | warnings and error reporting |
| agent-ui-metadata.md | agent/UI metadata handling |
```

- [ ] **Step 4: 验证渲染脚本仍可用**

Run: `python3 modular-programming/_shared/scripts/render_modular_graph.py modular-programming/_shared/examples/system-overview.arch.json -o <scratchpad>/graph.html`
Expected: 成功生成，无 warning。

### Task 5: Commit 1（完善）

- [ ] **Step 1: 提交所有新增/修改**

```bash
git add README.md modular-programming/ docs/
git commit -m "Complete modular-programming skill suite

Add pm-maintenance-rules (merged archive+compression rules), session-entry
rule and routing quick reference, agent-neutral wording, L2 PM-start and
re-render reminders, and renderer internal docs migrated from
architecture-design.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Expected: `git status` 中 modular-programming、README、docs 全部干净；旧目录改动仍未提交。

### Task 6: 删除旧目录并 Commit 2（清理）

- [ ] **Step 1: 确认 install.sh 无残留依赖**

Run: `grep -n "scripts/\|project-memory\|architecture-design" install.sh`
Expected: 仅剩「从安装目标清理 legacy 名称」的逻辑（prune/legacy 数组），无对仓库内旧目录文件的复制引用；若 install.sh 自身未提交修改属于旧套件遗留，纳入本 commit。

- [ ] **Step 2: 删除旧目录（含未提交修改）**

```bash
git rm -r --force architecture-design project-memory scripts
```

- [ ] **Step 3: 全仓残留检查**

Run: `grep -rn "pm-\|architecture-design" --include="*.md" --include="*.sh" . | grep -v ".git/" | grep -v migration-rules | grep -v modular-audit/SKILL.md | grep -v docs/superpowers`
Expected: 无输出（legacy 名称仅存于 migration-rules 映射、audit 检测描述、docs 历史文档）。

- [ ] **Step 4: dry-run 安装验证**

Run: `./install.sh --dry-run <scratchpad>/install-test`
Expected: 成功，仅列出 `_shared` + 7 个 modular-* skill。

- [ ] **Step 5: Commit 2**

```bash
git add -A
git commit -m "Remove legacy architecture-design and project-memory skills

All valuable content (renderer docs, archive/compression rules, examples,
references) now lives under modular-programming/.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Expected: `git status` 完全干净；`git log --oneline -3` 显示两个新 commit。
