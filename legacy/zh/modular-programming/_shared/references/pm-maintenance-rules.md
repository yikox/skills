# PM 维护规则

在归档已完成的 PM 行（`modular-status`）或审计并压缩过大的 `project-management.md`（`modular-audit`）时使用这些规则。目标是一份能一眼看清当前状态、又不丢失可追溯性的 PM 文件。

## 归档原则

- 归档是一个位置或小节，而非一种生命周期状态。
- 保留最终生命周期状态可见，如 `implemented`、`obsolete` 或项目的等价措辞。
- 保留日期、需求 ID、architecture patch commit、可选 proposal 路径、实现提交、PR、发布说明，或用户确认的证据。
- 优先把行移入归档小节，而非删除它们。
- 不要归档任何下一步动作仍处于进行中、阻塞或不明状态的内容。

## 归档候选

- 结果已在 Recent Updates 或某个发布/里程碑小节中总结后，被标记为 done/completed 的进行中任务。
- 标记为 `implemented` 且带有实现证据或明确用户确认的需求行。
- 标记为 `obsolete` 且带有简短原因的需求行。
- 标记为 `implemented` 或 `obsolete` 的可选 proposal 索引行。
- 被 `modular-audit` 识别出并经证据或用户确认的陈旧行。

## 不要归档什么

除非用户明确取消，否则不要归档处于以下进行中状态的行：

- `needs-clarification`
- `ready-for-design`
- `designing`
- `designed`
- `accepted`
- `implementing`
- `blocked`
- `needs-review`

在 Modular Design Index 中保持 `architecture/main-design.md` 与模块基线文档被索引。默认只归档可选 proposal 索引行。分支携带的 architecture patch commit 是 PM 证据，不是设计索引行。

## 归档小节

存在时使用既有的小节名。否则只添加所需的归档小节：

- `Requirements Archive` / `需求归档`
- `Design Archive` / `设计归档`
- `Task Archive` / `任务归档`

对小型项目，一个带紧凑表格的 `Archive` / `归档` 小节就够了。

## 可选 proposal 文件移动

默认不要移动 proposal 文件。移动文件可能破坏 PM 链接与未来的 agent 上下文。

如果用户明确要求移动旧的 proposal 文件：

1. 把它们移到稳定的归档路径，如 `architecture/modules/<module>/changes/archive/`。
2. 更新每一处 PM 路径、需求行、模块文档链接与设计交叉引用。
3. 移动后运行 `modular-audit`。

## 压缩触发条件

当满足以下一项或多项时，建议压缩：

- `project-management.md` 因当前状态被历史淹没而难以浏览。
- 文件大于约 25 KB，或单行/单条更新长于约 1,000 字符。
- `Recent Updates` / `最近更新` 有超过 8-12 条条目，或包含实现/调试叙述。
- `Milestones` / `里程碑` 重复了已存在于发布页面、可选 proposal 文档、提交或 `knowledge-summary.md` 中的发布说明。
- 旧的已完成工作占据了文件主体，而进行中任务、阻塞项、需求与下一步却很少。

## 在主文件中保留

在 `project-management.md` 中保持以下内容可见：

- 项目概览与当前状态；
- 当前版本、最新发布状态与活跃阻塞项；
- 进行中任务、当前焦点与下一步具体步骤；
- 待解风险与阻塞项；
- 需求待办清单与模块化设计索引；
- 活跃的路线图/待办项；
- 最近 5-8 条以结果为导向的简洁要点更新；
- 指向细节已迁出的归档/历史文件的链接。

不要移除稳定 ID、日期、architecture patch commit、可选 proposal 路径、发布 URL、提交 SHA、标签、PR 链接、阻塞证据，或用户确认的实现证据。

## 证据单一居所

这是**写入时**规则：证据在落笔那一刻就只写进一个居所，而不是先写多处、事后再压缩。

- 每份证据只有一个居所：
  - 使用默认分支 architecture patch 的 L2/L3 工作——证据写成一条 PM 完成指针，指向 architecture patch commit 加 implementation commit / PR；
  - 使用可选 proposal 的工作——验证与实现证据只写进该 proposal 的 Validation / Implementation 节，或者在 proposal 不保持活跃时写进归档执行产物；
  - 没有可选 proposal 的工作（L0/L1）——证据写成 `Recent Updates` 的一条单行（结论 + 验证命令或 commit）。
- PM 的其余各节（Active Tasks 的备注、Archive 的证据列、设计索引的备注、Current Status）只写一行结论加指针（patch commit / implementation commit / 可选 proposal / 需求 ID），不复述命令清单，也不复述实现叙事。
- 同一事实在 PM 主文件中最多出现在一个节。生命周期推进（如 Active Tasks 完成后进 Archive）是把行**移动**过去，不是复制一份。
- 若使用分支 patch 的工作仍需要超过一行 PM 证据与 commit message 的长期解释，这本身就是信号：它可能需要可选 proposal 或归档执行产物。

## 轻量 PM 模式

常规 L1 工作不应让 PM 文件变得嘈杂。当未来上下文需要时，优先在 `Recent Updates` 中放一条以结果为导向的说明：

```markdown
- 2026-07-04 - 修复 checker 对 group interface provider 越界未拦截的问题；验证 `python3 -m unittest discover -s modular-programming/modular-audit/tests` 通过。
```

仅当工作跨会话、携带显著风险或发布证据、属于某个既有进行中任务，或用户明确要求跟踪时，才对 L1 使用 `Active Tasks`。

## 移动或精简

移动或总结以下内容：

- 较旧的 `Recent Updates` 细节；
- 冗长的逐次发布实现叙述；
- 详细的调试根因与测试日志；
- 重复的 CI/构建/发布流程说明；
- 可在未来工作中复用的经验教训；
- 已在里程碑、发布说明、可选 proposal 文档或提交中体现的已完成进行中任务细节。

选择能保留未来有用性的目的地：

- `knowledge-summary.md`：可复用命令、根因、测试/部署工作流、环境约束、约定与经验。
- `architecture/...`：持久的架构事实、模块边界、ADR、可选 proposal 归档与已实现的基线更新。
- `archives/project-management-history-YYYY.md`：非当前状态、但应保持可追溯的历史 PM 更新细节。
- 发布页面、变更日志、提交或 PR：外部证据已存在；在 PM 中只保留一个紧凑的指针。

## 归档文件格式

在把详细历史移出主文件时，创建或追加到：

```text
archives/project-management-history-YYYY.md
```

使用这种形态：

```markdown
# Project Management History YYYY

Source: project-management.md
Compressed on: YYYY-MM-DD

## YYYY-MM

- YYYY-MM-DD - 原始的详细更新，或其忠实的精简版本。
```

保留足够的细节，以便还原某个决策为何做出。不要移动机密或临时草稿内容。

## 主文件压缩模式

用紧凑的要点替换冗长的条目：

```markdown
## 最近更新

- 2026-06-25 - 修复列表块编辑态 4 个交互问题，提交 `e4b39be`，测试 629 绿；详细根因和实现过程已归档到 `archives/project-management-history-2026.md`。
- 2026-06-24 - 完成列表块块内子块渲染并合并到 main；patch `abc1234`，实现 `def5678`。
```

把当前状态小节压缩到未来 agent 首先需要的事实：

```markdown
- Current version: 0.4.11; local macOS dmg exists.
- Latest public GitHub Release: v0.4.8.
- v0.4.9-v0.4.11 are blocked from full release by CI billing/spending limit.
- Current focus: editor and AI conversation experience.
```

对 `Milestones` / `里程碑`，只保留版本/日期/结果。把实现细节放进紧凑的 Recent Updates 说明、可选 proposal 文档、commit/PR 或归档历史。

## 压缩流程

1. 阅读 `project-management.md`、`knowledge-summary.md`、相关架构文档，以及任何既有的 `archives/project-management-history-*.md`。
2. 区分当前状态小节与历史小节。
3. 建立一份保留清单：
   - 当前版本与发布状态；
   - 活跃阻塞项与风险；
   - 进行中任务与下一步；
   - 待解需求与已接受 architecture patch / proposal；
   - 最新的有用更新；
   - 所有必须保持可达的链接/ID/证据。
4. 用与既有 PM 相同的语言与标题风格起草压缩后的主文件。
5. 酌情把较旧的细节移入归档/历史文件、知识文档、可选 proposal 文档或 commit/PR。
6. 从 `project-management.md` 向任何归档/历史文件添加紧凑指针。
7. 之后对改动过的 PM 运行 `modular-review`。
8. 报告压缩前后大小、被压缩的小节、创建/更新的归档文件，以及有意保留在主文件中的任何事实。

## 安全规则

- 不要通过删除证据来压缩。用链接来移动或总结。
- 不要把未解决的阻塞项、活跃需求、进行中任务、活跃 architecture patch / proposal 或当前焦点压缩进只在归档中的历史。
- 总结时不要改写项目的含义或状态。
- 除非证据已支撑，否则不要把工作标记为完成、接受、废弃或已实现作为压缩的一部分。
- 优先小范围的小节级编辑，而非整体重写。
- 如果请求只是审计、而非明确的压缩请求，在移动大量历史前先询问用户。
