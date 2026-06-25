# Project Memory Skills

`project-memory` 是一组用于维护外部项目记忆的 PM skills。它把项目状态、架构设计、需求、变更设计、审核结果、路线图、知识沉淀和迁移审计放到项目外部的 notes workspace 中，帮助后续 AI agent 在不同会话里延续上下文。

这套 skills 面向轻量但长期演进的软件项目。默认文档语言跟随项目 PM 文档本身，中文项目优先写中文。

## 存储位置

PM 文档放在 notes workspace 下的 `PM/<project-slug>/`：

```text
<notes-root>/
└── PM/
    └── <project-slug>/
        ├── project-management.md
        ├── knowledge-summary.md
        └── architecture/
            ├── main-design.md
            └── modules/
                ├── <module>.md
                └── <module>/
                    └── changes/
                        └── <date>-<change>.md
```

主架构文档使用 `architecture/main-design.md`，不要用 `architecture/README.md` 作为主设计文档。`README.md` 只作为目录说明时使用。

## Skills 总览

| Skill | 主要职责 | 常见触发 |
| --- | --- | --- |
| `pm-init` | 初始化或修复项目记忆连接，创建基础 PM 文档，更新项目 AI 协作规则 | 初始化 PM、连接 notes、修复 AGENTS/CLAUDE 规则 |
| `pm-document-architecture` | 创建和维护主架构设计、模块设计、Mermaid 图、SVG-first UI 示意图，并写入 PM 设计索引 | 写架构设计文档、生成模块文档、画架构图或 UI 示意图 |
| `pm-record-requirement` | 在设计前澄清需求，确定模块、修改内容、范围、影响点、验收标准和开放问题，写入需求待办 | 记录需求、明确需求、先记到 PM |
| `pm-review-artifact` | 自动审核需求、架构文档和设计文档；修明确缺陷，列出需人类确认的问题 | 自动审核、人工确认前检查、需求/架构/设计审核 |
| `pm-groom-roadmap` | 梳理需求池、优先级、路线图、里程碑和下一步工作 | 排优先级、路线图规划、下一步做什么 |
| `pm-design-requirement` | 把需求转成模块归属的变更设计文档，写回 PM 设计索引；实现完成后记录落地证据 | 需求转设计、待办转设计、设计接受、设计落地 |
| `pm-track-status` | 维护 `project-management.md` 中的当前状态、任务、里程碑、风险、归档和设计状态 | 开始/完成任务、提交后更新 PM、归档完成项 |
| `pm-record-knowledge` | 维护 `knowledge-summary.md`，记录可复用的技术事实、命令、故障根因、项目约定 | remember this、记录知识、调试结论沉淀 |
| `pm-audit-memory` | 审计 PM 一致性、陈旧任务、缺失设计链接、生命周期错位、架构漂移和归档候选 | 检查 PM、审计项目记忆、清理待办 |
| `pm-migrate-memory` | 把旧 PM 文档或旧 skill schema 迁移到当前 `pm-*` 结构 | 迁移 PM、修复 PM 结构、统一 schema |

## 标准流程

`pm-init` 是项目设置阶段，不属于日常交付流程。初始化完成后，典型流程是：

```text
pm-document-architecture
  -> pm-review-artifact
  -> pm-record-requirement
  -> pm-review-artifact
  -> pm-groom-roadmap
  -> pm-design-requirement
  -> pm-review-artifact
  -> human confirmation
  -> AI implements from accepted spec
  -> pm-design-requirement marks landing and updates PM evidence
  -> pm-document-architecture refreshes durable baseline if needed
  -> pm-audit-memory
  -> pm-track-status archives implemented/obsolete rows when appropriate
```

实现阶段不需要单独 skill。AI 根据已经接受的 spec 实现代码；实现后通过现有的设计/状态 skills 更新 PM、设计状态和落地证据。

## 文档分层

架构文档记录长期有效的系统事实和目标架构：

- `architecture/main-design.md`：主架构设计，列出模块、边界、数据流、关键约束和设计文档索引。
- `architecture/modules/<module>.md`：模块设计，描述模块职责、接口、依赖、数据、风险和演进方向。
- 图表可以使用 Mermaid；UI 界面示意图优先用 SVG-first 资产。
- 每次绘制图表后要对照代码、PM、架构事实检查准确性，发现错误后修改并再次校验。

变更设计文档记录某个需求如何修改系统：

- 路径放在 `architecture/modules/<module>/changes/<date>-<change>.md`。
- 由 `pm-design-requirement` 生成或维护。
- 设计文档必须关联需求 ID、主模块、设计状态、审核状态、实现状态、影响模块、验收标准、开放问题和实现证据。
- 实现完成后才能标记设计落地；不能只因为设计写完就标记 implemented。

## 审核与确认

`pm-review-artifact` 是自动审核官：

- 可以修复明确、低风险的问题，比如缺失设计路径、状态字段、需求 ID、开放问题位置、PM 索引同步。
- 可以把无阻塞问题的 artifact 标记为 reviewed。
- 不能替代人类做产品取舍、重大范围决定、架构接受、设计接受或无证据的实现落地确认。
- 有疑惑时要把问题写入 PM row、架构文档的 review/open questions，或变更设计文档的 review findings。

人工确认后，继续由相应 skill 更新状态；不需要单独的人类确认记录 skill。

## 状态边界

常用需求状态：

```text
needs-clarification -> ready-for-design -> designing -> designed
  -> accepted -> implementing -> implemented
```

常用设计状态：

```text
draft -> proposed -> accepted -> implemented
```

常用审核状态：

```text
not-reviewed -> needs-review -> reviewed
```

状态可以保留项目已有词汇，但要在 PM 中保持同一含义，不要把需求、设计、实现状态混在同一字段里。

## 常见场景

新项目接入 PM：

```text
pm-init
```

已有代码仓库生成架构文档：

```text
pm-document-architecture
pm-review-artifact
```

用户提出一个新需求，但还不清楚：

```text
pm-record-requirement
pm-review-artifact
```

需求已经清楚，准备转设计：

```text
pm-design-requirement
pm-review-artifact
human confirmation
```

实现完成，需要更新 PM：

```text
pm-design-requirement
pm-document-architecture   # only if durable architecture changed
pm-track-status
pm-record-knowledge        # only if reusable knowledge was discovered
```

长时间没维护、迁移旧 PM、或项目状态混乱：

```text
pm-audit-memory
pm-migrate-memory          # only when schema migration is needed
pm-groom-roadmap           # only when priority or roadmap needs grooming
```

## 审计频率

建议在这些时机运行 `pm-audit-memory`：

- 每个非平凡功能实现完成后。
- 每次迁移 PM schema 后。
- 每个里程碑收尾时。
- 长时间暂停后重新接手项目前。
- 当 PM 中出现 designed/accepted/implemented 状态，但设计路径、审核状态或实现证据不明确时。

如果项目活跃，可以每周或每个 sprint 做一次轻量审计；个人项目可以按阶段或明显状态变化触发。

## 校验工具

仓库提供两个维护脚本：

```sh
python3 scripts/check_pm_reference_sync.py
python3 scripts/check_pm_project.py /path/to/PM/<project-slug>
```

`check_pm_reference_sync.py` 用于检查重复引用文件是否同步。

`check_pm_project.py` 用于对单个外部 PM 项目做确定性 lint，检查：

- 需求和设计文档链路。
- 本地 Markdown 链接是否断开。
- `architecture/main-design.md` 是否存在。
- 变更设计是否缺需求 ID、审核状态或实现证据。
- PM 设计索引状态和设计文档状态是否冲突。
- 需求待办是否仍是旧表结构或缺模块、修改摘要、范围/影响点。

## 安装

从仓库根目录运行：

```sh
./install.sh
```

默认安装到：

```text
~/.agents/skills
~/.codex/skills
~/.claude/skills
```

预览安装变更：

```sh
./install.sh --dry-run
```

## 维护原则

- 先读现有 PM 文档，再编辑；避免重写用户手写内容。
- 只记录可持续使用的项目状态和知识，不记录临时 scratch。
- 不在 PM 文档中保存密钥、token、私钥或敏感凭据。
- 需求、设计、实现和审核各自有边界；不要用一个状态覆盖所有生命周期。
- 架构 baseline 不记录待办计划；待办变更通过需求和 change design 表达。
- 自动审核负责提前发现问题，人类负责确认方向和取舍。
