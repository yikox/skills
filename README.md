# 模块化编程 Skills

这个仓库提供一套 `modular-programming` skills，用来让 AI agent 按“先定位模块，再设计/实现”的方式开发项目。

核心原则：

```text
Architecture 是模块地图和系统结构的权威来源。
PM 记录正在做什么、做到哪一步、完成证据是什么。
非平凡修改必须先定位主模块，否则不能直接进入实现计划。
```

## 什么时候用

新项目刚开始：

```text
Use $modular-init 初始化这个项目的模块化编程工作流。
```

已有项目迁移：

```text
Use $modular-architecture 根据当前代码反推出模块地图。
Use $modular-audit 检查旧 PM/架构文档并迁移到模块化工作流。
```

日常开发功能、修 bug、重构：

```text
Use $modular-change 处理这个修改。
```

只想更新项目状态：

```text
Use $modular-status 记录这个任务开始/完成。
```

只想记录可复用知识：

```text
Use $modular-knowledge 记录这个调试结论/命令/项目约定。
```

## Skills 分工

| Skill | 什么时候用 | 主要产物 |
| --- | --- | --- |
| `modular-init` | 新项目接入、修复项目记忆、初始化模块化工作流 | `project-management.md`、`knowledge-summary.md`、基础 `architecture/` |
| `modular-architecture` | 创建/更新模块地图、迁移老项目架构、写架构变更或 ADR、渲染全局图 | `architecture/main-design.md`、`architecture/modules/*.md`、图、ADR |
| `modular-change` | 日常开发入口：功能、bug、重构、模块修改、架构修改 | L0/L1/L2/L3 分级、设计、实现、验证、收尾 |
| `modular-status` | 记录开始、进展、完成、阻塞、设计索引、归档 | PM active task、完成记录、证据 |
| `modular-review` | 自动审核模块归属、变更级别、设计、ADR、PM 状态、图一致性 | review notes、修复项、开放问题 |
| `modular-audit` | 长时间未维护、迁移旧项目、检查架构漂移和 PM 垃圾 | 审计结果、迁移缺口、清理建议 |
| `modular-knowledge` | 记录构建命令、测试命令、故障原因、架构事实、项目约定 | `knowledge-summary.md` |

## 推荐使用流程

### 1. 初始化新项目

```text
Use $modular-init 初始化项目。
```

Agent 应该先问清楚项目目标、运行环境、主要工作流、状态/存储、外部系统，然后建立模块地图：

```text
architecture/main-design.md
architecture/modules/<module>.md
architecture/graphs/current-project.arch.json
project-management.md
knowledge-summary.md
```

初始化成功的标准不是“写了 plan”，而是用户能看懂：

- 系统有哪些模块；
- 每个模块负责什么；
- 模块之间怎么协作；
- 后续修改应该落在哪个模块。

### 2. 迁移老项目

```text
Use $modular-architecture 迁移当前项目架构。
Use $modular-audit 检查迁移结果。
```

迁移时先还原事实，不默认重构：

```text
扫描代码结构、入口、配置、测试、状态、IO、生成物
-> 推断 current baseline
-> 标记 verified / inferred / unclear
-> 生成模块文档和全局图
-> 把 TODO、bug、需求归属到模块
-> 在 PM 记录迁移缺口
```

如果模块边界不清楚，先把它作为架构缺口记录下来，不要假装已经明确。

### 3. 日常开发

日常开发优先用：

```text
Use $modular-change 实现这个需求/修复这个 bug/重构这个模块。
```

`modular-change` 必须先做模块门判断：

```text
用户请求
-> 读取 architecture baseline
-> 定位 Primary Module
-> 列出 Impacted Modules
-> 判断 L0/L1/L2/L3
-> 决定是否需要 PM、设计、ADR、评审
```

如果 L1/L2/L3 无法定位主模块，必须先回到 `modular-architecture` 补架构，不进入实现计划。

## 修改分级

| 级别 | 场景 | 流程 |
| --- | --- | --- |
| L3 大改 | 新增/拆分/合并模块，改变模块边界、跨模块契约、核心数据流、状态归属、存储、运行时、外部系统，或需要长期架构决策 | PM start -> 架构变更/ADR -> review -> 人工接受 -> plan -> implement -> verify -> 更新 baseline -> PM complete |
| L2 中改 | 单个主模块内的重构、内部结构、文件组织、算法、状态流变化；不改变外部契约或只做兼容调整 | PM start -> 模块修改方案 -> review -> implement -> verify -> 更新模块架构 -> PM complete |
| L1 小改 | 模块内局部行为增减，不改变边界、公共接口、核心流程 | PM start -> implement -> verify -> 必要时更新模块文档 -> PM complete |
| L0 细微改 | typo、注释、格式、文案、局部常量、机械修改，不改变行为和模块理解 | 标记模块 -> implement -> verify；PM/架构更新可选 |

强制规则：

```text
L1/L2/L3 必须在开头记录 PM start，结尾记录 PM complete。
L0 默认不强制 PM，除非用户明确要求追踪、属于已有任务、或影响发布证据。
```

## Architecture 和 PM 的关系

Architecture 负责“系统是什么”：

```text
architecture/main-design.md
architecture/modules/*.md
architecture/changes/*.md
architecture/adrs/*.md
architecture/graphs/*.arch.json
architecture/rendered/*.html|svg
```

PM 负责“现在在做什么、状态是什么”：

```text
project-management.md
```

PM 可以索引模块、设计和 ADR，但不能自己定义模块边界。模块边界必须来自 Architecture。

## Baseline 和 Target

大改动不能直接把未实现的设计写成当前事实。

```text
baseline architecture = 当前已实现或已接受的系统事实
target architecture = 已提出/已评审/已接受但未必落地的目标结构
```

L3 大改应先写 target architecture 或 ADR，评审通过后再进入实现。实现验证完成后，才能把 target 转成 baseline。

## 常用口令

```text
Use $modular-init 给这个项目接入模块化编程工作流。
Use $modular-architecture 为这个老项目生成模块地图。
Use $modular-change 按模块化流程实现这个需求。
Use $modular-change 先判断这个修改是 L0/L1/L2/L3。
Use $modular-status 记录这个 L2 修改开始。
Use $modular-status 记录这个任务完成，附验证结果。
Use $modular-review 审核这个模块修改方案。
Use $modular-audit 检查 PM 和 Architecture 是否漂移。
Use $modular-knowledge 记录这个构建命令和故障结论。
```

## 安装

从仓库根目录运行：

```sh
./install.sh
```

预览安装内容：

```sh
./install.sh --dry-run
```

指定安装目录：

```sh
./install.sh ~/.agents/skills ~/.codex/skills ~/.claude/skills
```

默认安装到：

```text
~/.agents/skills
~/.codex/skills
~/.claude/skills
```

安装脚本会安装：

```text
_shared
modular-init
modular-architecture
modular-change
modular-status
modular-review
modular-audit
modular-knowledge
```

旧的 `project-memory/` 和 `architecture-design/` 已从仓库移除（可在 git 历史中找回）。安装脚本会从目标目录清理旧的 `pm-*` 和 `architecture-design` skill 名称。

## 仓库结构

```text
modular-programming/
  _shared/
    references/          # 模块化流程、存储结构、评审、迁移、图格式
    assets/              # PM、架构、模块、变更、ADR、知识模板
    scripts/             # 图渲染器
    examples/            # 可渲染示例
  modular-init/
  modular-architecture/
  modular-change/
  modular-status/
  modular-review/
  modular-audit/
  modular-knowledge/
```

## 验证

列出当前 active skill：

```sh
find modular-programming -name SKILL.md -print
```

Dry-run 安装：

```sh
./install.sh --dry-run /tmp/modular-skills-install
```

渲染示例架构图：

```sh
python3 modular-programming/_shared/scripts/render_modular_graph.py \
  modular-programming/_shared/examples/system-overview.arch.json \
  -o /tmp/modular-graph.html
```
