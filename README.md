# 模块化编程 Skills

这个仓库提供一套 `modular-programming` skills，用来让 AI agent 按“先定位模块，再设计/实现”的方式开发项目。默认路径尽量轻量：小改快速完成，复杂修改再升级到设计、评审和 PM 治理。

核心原则：

```text
Architecture 是模块地图和系统结构的权威来源。
PM 记录正在做什么、做到哪一步、完成证据是什么。
非平凡修改必须先定位主模块，否则不能直接进入实现计划。
新会话开始先读 project-management.md 和 architecture/main-design.md；涉及 active task 时先询问用户是否接续。
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

PM 文件太长、历史淹没当前状态：

```text
Use $modular-status 归档已完成的任务和需求。
Use $modular-audit 检查 PM 是否需要压缩，按 pm-maintenance-rules 处理。
```

日常用户只需要记住四个主入口：`modular-init`、`modular-change`、`modular-audit`、`modular-knowledge`。其他 skill 是内部路由或高级能力。

完整的“请求类型 -> skill -> 产物”速查表见
`modular-programming/_shared/references/modular-workflow-rules.md` 的 Routing Quick Reference。

## Skills 分工

| Skill | 什么时候用 | 主要产物 |
| --- | --- | --- |
| `modular-init` | 新项目接入、修复项目记忆、初始化模块化工作流 | `project-management.md`、`knowledge-summary.md`、基础 `architecture/` |
| `modular-architecture` | 内部/高级：创建/更新模块地图、迁移老项目架构、写架构变更或 ADR、可选渲染图 | `architecture/main-design.md`、`architecture/modules/*.md`、可选图、ADR |
| `modular-change` | 日常开发入口：功能、bug、重构、模块修改、架构修改 | L0/L1/L2/L3 分级、设计、实现、验证、收尾 |
| `modular-autopilot` | 高级：已接受并 review 通过的 L2/L3 设计需要一次授权后自主落地 | intake 审阅、实现计划、执行、决策日志、结项/待合并报告 |
| `modular-architect` | 高级：评估项目模块化程度、讨论老项目重构方案或新项目模块化设计（未接入工作流的项目也可用） | 评估报告、分阶段重构方案、模块化设计方案（只提案，不实现） |
| `modular-narrator` | 高级：只读调查项目并通俗讲解，帮用户理解（独立可用，不依赖工作流） | 对话讲解，不落文件 |
| `modular-status` | 内部：记录开始、进展、完成、阻塞、设计索引、归档 | PM active task、完成记录、证据 |
| `modular-review` | 内部：自动审核模块归属、变更级别、设计、ADR、PM 状态、已维护图一致性 | review notes、修复项、开放问题 |
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
project-management.md
knowledge-summary.md
```

init 会先用选择题询问工作流偏好：`docs-language`（文档语言 zh/en/follow-project）和
`confirmation`（确认粒度 high-touch/standard/low-touch，low-touch 也不跳过 L3 接受、
模块地图落盘等安全底线），偏好写进项目 AI 文档的 Preferences 区，后续所有 skill 遵守。

架构图不是默认产物。`main-design.md + modules/*.md` 足够支撑 AI 工作；图是给人看的高级可视化能力，需要时再由 `modular-architecture` 渲染。

模块地图草案需要用户确认后才落盘为 baseline。init 还会把工作流规则
（`_shared/assets/ai-rules-snippet.md`）合并进项目的 `CLAUDE.md`/`AGENTS.md`
（合并不覆盖，首次写入前先确认），让后续每个会话都自动遵守会话入口、模块门和 PM 规则。

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

`modular-change` 必须先过会话入口和模块门：

```text
用户请求
-> 新会话先读 project-management.md（active task、阻塞、当前焦点）
-> 读 architecture/main-design.md（模块地图）
-> 若与 active task 相关，询问用户是否接续，不擅自接续或关闭
-> 定位 Primary Module
-> 列出 Impacted Modules
-> 判断 L0/L1/L2/L3（L3 需先告知用户并确认）
-> 决定是否需要 PM、设计、ADR、评审
```

如果架构地图缺失或明显过期导致无法定位主模块，先回到 `modular-architecture` 补架构，不进入实现计划。

如果 bug 根因或模块归属暂时不清楚，先进入诊断模式：复现、读代码、运行测试、收集证据；诊断阶段不做结构性修改、不标完成。定位后再按 L1/L2/L3 路由；若诊断证明是架构地图问题，再补架构。

## 修改分级

| 级别 | 场景 | 流程 |
| --- | --- | --- |
| L3 大改 | 新增/拆分/合并模块，改变模块边界、跨模块契约、核心数据流、状态归属、存储、运行时、外部系统，或需要长期架构决策 | PM start -> 架构变更/ADR -> review -> 要点摘要 -> 人工接受 -> plan -> implement -> verify -> 更新 baseline -> PM complete |
| L2 中改 | 单个主模块内的重构、内部结构、文件组织、算法、状态流变化；不改变外部契约或只做兼容调整 | PM start -> 模块修改方案 -> review -> 要点摘要 -> 用户确认 -> implement -> verify -> 更新模块架构 -> PM complete |
| L1 小改 | 单模块、通常 1-3 文件、局部行为增减，不改变边界、公共接口、核心流程 | implement -> verify -> 必要时一条 Recent Updates；跨会话/有风险/用户要求时才进 Active Tasks |
| L0 细微改 | typo、注释、格式、文案、局部常量、机械修改，不改变行为和模块理解 | 标记模块 -> implement -> verify；PM/架构更新可选 |

强制规则：

```text
L2/L3 必须在开头记录 PM start，结尾记录 PM complete。
L1 默认轻量留痕，只有跨会话、有风险、发布证据、用户要求或属于 active task 时才完整记录。
L0 默认不强制 PM，除非用户明确要求追踪、属于已有任务、或影响发布证据。
```

Bug 修复至少 L1（改行为就不是 L0），按修复形态而非症状严重度分级：

```text
小 bug（根因局部、小改）L1：
  复现 -> 定位根因 -> 修复
  -> 验证（失败用例通过 + 既有验证不回退）
  -> 必要时一条 Recent Updates；跨会话/有风险/用户要求/已有 active task 时才 PM start/complete
大 bug（根因结构性、需多步重构）L2：
  走 L2 流程，模块修改设计必须含根因分析
根因在模块边界/跨模块契约 -> 与用户确认升 L3
可复用的根因（环境坑、反复出现的模式）记入 knowledge-summary.md
```

## 需要用户确认的节点

必须确认（阻塞，未确认不往下走）：

- 新项目/迁移的初始模块地图（模块划分、边界、命名），确认后才落盘为 baseline；
- 项目记忆存放位置；首次创建或修改 CLAUDE.md/AGENTS.md 等 AI 文档；
- 判定为 L3 时，先告知并确认再进入架构变更流程；
- L2 模块修改方案，实现前确认；
- L3 target architecture / ADR 方向，review 后接受；
- L2 升级为 L3；
- 产品范围取舍、多个模块归属方案二选一；
- 取消 active task、归档大量历史。

请求 L2/L3 确认时，必须先给出 3-8 条要点摘要（修改重点、歧义点、风险点），让用户不读完整设计也能决策。

只需报告（不阻塞，用户有异议再纠正）：

- PM start/update/complete 记录；
- L0/L1 分级；
- 实现验证后的 baseline 更新；若项目维护图，再报告图渲染；
- 归档单条已完成任务。

## Architecture 和 PM 的关系

Architecture 负责“系统是什么”：

```text
architecture/main-design.md
architecture/modules/*.md
architecture/changes/*.md
architecture/adrs/*.md
architecture/graphs/*.arch.json        # 可选高级可视化
architecture/rendered/*.html|svg       # 可选高级可视化
```

PM 负责“现在在做什么、状态是什么”：

```text
project-management.md
```

PM 可以索引模块、设计和 ADR，但不能自己定义模块边界。模块边界必须来自 Architecture。

图是高级可视化能力，不是默认架构事实来源。默认事实来源是 `architecture/main-design.md` 和 `architecture/modules/*.md`。

## 模块与代码、关系语义

```text
模块文档 frontmatter code_paths 声明模块拥有的代码（glob 列表）。
每个承载行为的代码路径属于且只属于一个模块；测试随被测模块。
shared_paths / ignored_paths 可记录共享工具、集成测试、生成物、框架 glue code 等非 owner 例外。
modular-change 用"变更路径 ∩ code_paths"确定性定位主模块。
modular-audit 检查孤儿路径、幽灵 glob、重叠认领。

图中箭头 = 依赖方向：A -> B 读作 A 依赖/使用 B（数据流写 described）。
关系 kind 五词：uses / reads / writes / triggers / distributes。
solid = 运行时依赖，dashed = 非运行时（构建、验证夹具、同步约定）。
当项目维护架构图时，图是模块间关系的权威可视化来源，模块文档 Dependencies 表是它的子集视图。默认不维护图时，以 `main-design.md` 和模块文档为准。

模块文档写作规范见 module-authoring-rules.md：
顶层模块 4-9 个；契约必须具体；不复述代码；验证可执行；
不确定事实标注 (inferred)/(unclear)；契约/依赖/约束/code_paths 变化必须同步文档。
```

## Baseline 和 Target

大改动不能直接把未实现的设计写成当前事实。

```text
baseline architecture = 当前已实现或已接受的系统事实
target architecture = 已提出/已评审/已接受但未必落地的目标结构
```

L3 大改应先写 target architecture 或 ADR，评审通过后再进入实现。实现验证完成后，才能把 target 转成 baseline。基线更新后重新渲染受影响的架构图。

## PM 归档与压缩

PM 的价值是“当前状态一眼可见”。当已完成的历史开始淹没 active task 时：

- 已完成/废弃的任务、需求、设计索引行，保留最终状态和证据后移入归档区；
- `project-management.md` 超过约 25 KB、最近更新超过 8-12 条、或塞满实现细节叙述时，把旧细节移到
  `archives/project-management-history-YYYY.md`、`knowledge-summary.md` 或架构文档；
- 归档和压缩都不允许删除证据（ID、日期、设计路径、commit、PR、验证结果），只能移动或带链接摘要。

细则见 `modular-programming/_shared/references/pm-maintenance-rules.md`。

## 常用口令

```text
Use $modular-init 给这个项目接入模块化编程工作流。
Use $modular-architecture 为这个老项目生成模块地图。
Use $modular-change 按模块化流程实现这个需求。
Use $modular-change 先判断这个修改是 L0/L1/L2/L3。
Use $modular-autopilot 执行这份已接受的 L2/L3 设计。
Use $modular-architect 评估这个项目的模块化程度，讨论重构方案。
Use $modular-status 记录这个 L2 修改开始。
Use $modular-status 记录这个任务完成，附验证结果。
Use $modular-review 审核这个模块修改方案。
Use $modular-audit 检查 PM 和 Architecture 是否漂移。
Use $modular-status 归档已完成的任务，压缩过长的 PM 历史。
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
modular-autopilot
modular-architect
modular-narrator
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
    references/          # 模块化流程、存储结构、评审、迁移、PM 维护、图格式
    assets/              # PM、架构、模块、变更、ADR、知识模板
    scripts/             # 图渲染器（renderer-docs/ 是渲染器自身的模块文档）
    examples/            # 可渲染示例
  modular-init/
  modular-architecture/
  modular-change/
  modular-autopilot/
  modular-architect/
  modular-narrator/
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
