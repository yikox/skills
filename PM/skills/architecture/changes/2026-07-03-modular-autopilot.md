---
title: modular-autopilot 监督者技能
level: L3
status: accepted
review_status: reviewed
primary_module: modular-autopilot
impacted_modules: [modular-change, modular-audit, _shared]
---

# modular-autopilot 监督者技能

## Request

为 modular-programming 技能体系新增一个"监督者角色"技能 `modular-autopilot`：接手一份已由用户通过 modular-change 流程接受的 L2/L3 change 设计，先做入口审阅并向用户反馈，经用户一次确认后，自主完成"实现计划 → subagent 执行 → 验证 → modular 收尾"全流程，全程记录决策日志，最后交结项报告。目的：把"设计已接受 → 落地完成"之间的所有人工确认点收敛为一次入口确认加一份结项报告。

## Current Baseline

- modular-change L2/L3 路径在"设计接受"之后只写了 `-> implementation plan -> implement -> verify` 一行文字，无具体技能承接，计划与执行环节全靠临场发挥。
- 每一步（计划确认、评审争议裁决、收尾）都隐含人工介入；交互档位（high/standard/low-touch）只调节确认强度，不存在"打包授权后全自主"的模式。
- superpowers 插件提供 writing-plans（计划方法论）、subagent-driven-development（逐任务 subagent 执行 + 双评审 + 最终全分支评审 + 进度台账）、using-git-worktrees、finishing-a-development-branch，但它们不懂 modular 语义：不检查设计接受状态、不产出可追溯 front matter、终态直接进分支收尾而跳过 PM completion 和 baseline 更新。

## Target Architecture

新增技能 `modular-programming/modular-autopilot/SKILL.md`，与现有七个技能并列。**技能形态而非 agent 形态**：由主会话加载执行，因为 subagent-driven-development 需要向下派发 implementer/reviewer subagent，而 subagent 不能再派发 subagent——监督者必须坐在主会话里。

### 职责边界

- **起点**：一份已接受（review 通过 + 用户确认）的 L2/L3 change 设计文档。设计环节（modular-change 上游）不归它管。
- **终点**：结项报告。push / PR / 任何仓库外可见动作一律不做，报告中给出建议命令由用户执行。

### 阶段一：入口审阅（唯一人工确认点）

接到设计文档后重点检查三类问题，产出审阅反馈发给用户，**用户确认后进入全自主区**：

1. **模块地图正确性**：设计声明的主模块/受影响模块与 `main-design.md`、模块 `code_paths` 一致；模块地图与代码现状无明显脱节。有问题在此拦截，不带病进执行。
2. **设计内部一致性与可执行性**：Target Design / Contract Impact / Validation 之间无矛盾；无模糊到无法写计划的表述；无漏判的 L3 成分（L2 设计中隐含的边界/契约改动）。
3. **执行前提**：Validation 声明的验证手段可操作（测试命令存在）、worktree 可建、依赖的模块契约文档齐全。

审阅反馈内容：发现的问题 + 建议 + 计划采用的执行方式简述。

### 阶段二：实现计划（调用 superpowers:writing-plans）

- 设计文档 + `main-design.md` + 受影响模块契约文档作为 spec 输入。
- 设计中的模块边界与契约约束**逐字**注入计划的 Global Constraints 区块——SDD 会把该区块交给每个任务评审者，使其自动成为模块边界守门员。
- 计划存放：`architecture/modules/<module>/plans/`（L2）或 `architecture/plans/`（L3），**不放** `changes/` 目录（modular-audit 的 `check_designs` 通配 `changes/*.md` 会将其误判为设计文档）。计划 front matter 含 `source_design:`（设计文档路径）与 `level:`，供 audit 追溯。
- 计划写完后执行**计划↔设计一致性自审**：任务不越出主模块边界；设计 Validation 区块每项在计划中有对应验证步骤；Global Constraints 完整搬运契约约束。通过即自批，记决策日志。
- **不走** writing-plans 自带的执行交接问询（subagent-driven vs inline 二选一），直接进入阶段三。

### 阶段三：subagent 执行（superpowers:subagent-driven-development）

- 先经 using-git-worktrees 建立隔离工作区。
- SDD 内部机制原样使用：预检、逐任务 implementer + task-reviewer 双评审、Critical/Important 必修复重审、最终全分支评审（最强模型）、progress ledger。
- plan-mandated 冲突按"设计文档为准"自裁，记决策日志。
- **不进** finishing-a-development-branch 的合并/PR 分支，最终评审通过后转入阶段四。

### 阶段四：modular 收尾

1. 按设计 Validation 区块收集验证证据（SDD 测试记录、commit 区间、评审结论）。
2. 更新模块/架构 baseline，重渲染受影响的图。
3. 设计文档标 `status: implemented`。
4. PM completion 记录，证据引用 SDD 台账。
5. 跑 modular-audit 自检（漂移兜底）。
6. 产出结项报告。

若项目 PM 目录在代码仓库内：所有 modular 文档更新（baseline、PM、设计状态）在 worktree 分支合并回主分支**之后**、于主工作区执行，避免文档改动滞留在未合并分支。

### 中途硬停机条件（仅两条）

因模块地图错误与方向性矛盾已在入口审阅拦截，自主区仅在以下情况停下找用户：

1. SDD 报 BLOCKED，且补上下文 / 换更强模型 / 拆小任务三种手段都失效；
2. 执行中发现的事实**推翻入口审阅结论**（如实际代码与模块文档严重不符）——说明入口审阅有漏，宁停不硬跑。

### 决策日志与结项报告

- **决策日志**：每次自主裁决（自批计划、裁决评审争议、降级 Minor 发现）追加一行（时间、决定、理由），与 SDD progress ledger 同目录（`.superpowers/sdd/`）。
- **结项报告**：结果与证据（commit 区间、测试输出、评审结论）／替用户做的决定清单（决策日志摘要，逐条附理由，供事后问责）／实现与设计的偏差及处理／遗留 Minor 项与风险／建议用户执行的动作（合并、push、PR 命令原文）。

## Module Impact

| Module            | Impact                                                                                                                                                     |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| modular-autopilot | 新增技能，本变更主体                                                                                                                                                 |
| modular-change    | L2/L3 路径的 `-> implementation plan -> implement -> verify` 段落补充指引：设计接受后可移交 modular-autopilot；同时在确认步骤显式写入"确认后将设计 status 置为 accepted"（否则 autopilot 的入口门槛无从判定） |
| modular-audit     | storage schema 与检查器需认知 `plans/` 目录：布局文档补充计划文件位置；可选新增"孤儿计划"检查（PM 已完成但计划未归档/删除）                                                                              |
| _shared           | `storage-schema.md` 布局补 `plans/`；`modular-workflow-rules.md` 的 Design/ADR/Plan Boundaries 一节补计划存放与生命周期规则                                                   |

## Alternatives

| Option                                        | Tradeoff                                                                                          |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 自建 modular-plan 技能重造计划方法论                     | 完全可控、无外部依赖，但需自行发明并长期维护 writing-plans 已打磨的质量规则（任务粒度、No Placeholders、Interfaces 块、self-review），性价比低 |
| 直接在 modular-change 文档中固化"如何调用 superpowers"的流程 | 无新技能、改动小，但每个人工确认点仍在，无法达成"一次授权、全程自主、最后汇报"的目标                                                       |
| 监督者做成 agent（.claude/agents）                   | 概念上更像"角色"，但 subagent 无法派发 SDD 所需的下级 subagent，执行环节瘫痪，不可行                                           |

## ADR Need

需要一份 ADR：记录"监督者为主会话技能而非 agent"的决定（subagent 嵌套限制）与"入口一次确认替代全流程确认点"的授权模型（对交互档位安全底线的例外及其边界）。

## Implementation Strategy

高层过渡：新增 `modular-autopilot/SKILL.md` → 同步修订 modular-change / storage-schema / workflow-rules 的衔接点 → （可选）modular-audit 增加孤儿计划检查。硬依赖 superpowers 插件（writing-plans、subagent-driven-development、using-git-worktrees），在技能 Required References 中声明；superpowers 缺席时技能应明确报错并指引安装，不提供内联降级路径。详细步骤待本设计接受后由实现计划承接。

## Validation

- 技能文档评审：与 modular-workflow-rules、storage-schema、review-rules 无冲突；modular-audit 检查器对 `plans/` 目录文件不误报。
- 端到端演练：选一个真实 L2 变更，走完"入口审阅 → 用户确认 → 计划 → SDD 执行 → 收尾 → 结项报告"全流程，检验决策日志与报告的完整性。
- 负路径演练：给一份含模块地图错误的设计，确认入口审阅能拦截；模拟 BLOCKED 三板斧失效，确认硬停机而非硬跑。

## Risks

- 入口审阅是唯一防线：若审阅质量不足，问题会带进无人值守的自主区。缓解：审阅清单写死在技能中，且保留"事实推翻审阅结论即停机"的兜底。
- superpowers 插件升级可能改变 writing-plans/SDD 行为（如新增确认问询），衔接点可能悄然失效。缓解：技能中对衔接点的期望写明确（"不走执行交接问询"），演练在插件升级后重跑。
- PM 目录在仓库内时的 worktree 时序规则依赖执行纪律，写错顺序会造成文档漂移。缓解：收尾步骤按固定顺序写入技能，audit 自检兜底。

## Review Notes

- Review status: reviewed（自审通过：无占位符、章节与模板一致、状态词合法；用户于 2026-07-03 确认接受）
