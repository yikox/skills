---
name: modular-autopilot
description: Supervise autonomous execution of an accepted L2/L3 change design through intake review, implementation planning, subagent-driven execution, and modular closeout, with a decision log and final report. Use when the user hands an accepted design over for hands-off execution and wants one confirmation at intake plus a report at the end; Chinese triggers include 自主执行, 托管执行, 监督执行, 交给监督者, 自动落地, 全程代办.
---

# 模块化监督者（Modular Autopilot）

充当介于"设计已接受"与"变更已落地"之间的高级监督角色。仅在用户明确希望对一份已接受且已评审的 L2/L3 设计进行放手执行时使用。在接单时向用户索取恰好一次确认；此后自主完成规划、执行与收尾，记录每一个代用户所做的决策，并交付最终报告。绝不 push、绝不开 PR、绝不采取任何外部可见的动作——把推荐命令写进报告里即可。

## 硬依赖

本 skill 需要 superpowers 插件的 `writing-plans`、`subagent-driven-development` 与 `using-git-worktrees` 三个 skill。若其中任一不可用，停下并告知用户安装 superpowers 插件。没有内置的降级方案。

## 必读参考

阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`

## 前置条件

只接受 front matter 为 `status: accepted` 且 `review_status: reviewed` 的变更设计文档。其余一律拒绝，并把用户导回 `modular-change` / `modular-review`。设计阶段不是本 skill 的职责。

## 阶段 1：接单评审（唯一的人工确认）

在做任何事之前，检查三类问题：

1. **模块地图正确性。** 设计的主模块与受影响模块与 `architecture/main-design.md` 及各模块的 `code_paths` 一致；模块地图相对实际代码没有明显漂移。问题止步于此——绝不把一张有问题的地图带入自主区。
2. **设计的自洽性与可规划性。** 目标设计、契约影响、验证各节互不矛盾；没有含糊到无法据以规划的措辞；一份 L2 设计不能藏着 L3 的内容（边界或跨模块契约变更）。
3. **执行前置条件。** 设计所指名的验证命令确实存在且可运行；能够创建 git worktree；受影响模块的契约文档存在。

给用户发一份接单报告：发现、建议，以及你将如何执行的简短提纲。等待明确确认。确认之后，除非触发硬停止，否则不再回到用户。

## 阶段 2：实现计划

1. 用设计文档、`architecture/main-design.md` 及受影响模块的文档作为 spec，调用 `superpowers:writing-plans`。
2. 把设计的模块边界与契约约束**逐字**复制到计划的 Global Constraints 一节——subagent-driven-development 会把该节交给每一个 task reviewer，从而免费地让每个 reviewer 都成为模块边界的守门人。
3. 把计划保存到 `architecture/modules/<module>/plans/<YYYY-MM-DD>-<change>-plan.md`（L2）或 `architecture/plans/<YYYY-MM-DD>-<change>-plan.md`（L3）。绝不保存到 `changes/` 目录下。计划的 front matter 必须包含 `source_design:`（相对 pm-root 的设计路径）与 `level:`。
4. 执行"计划对设计"的自审：没有任务越过设计声明影响之外的模块边界；设计 Validation 一节的每一项在计划中都有对应的验证步骤；Global Constraints 承载了所有契约约束。
5. 通过后，自行批准并追加一行决策日志。完全跳过 writing-plans 的执行交接提问；直接进入阶段 3。

## 阶段 3：子 agent 执行

1. 通过 `superpowers:using-git-worktrees` 创建隔离工作区。
2. 原样用 `superpowers:subagent-driven-development` 执行计划：预检计划评审、每个任务的 implementer 加 task-reviewer、针对 Critical/Important 发现的修复循环、最终的整分支评审、进度台账。
3. 凡是 SDD 会请人来裁决计划所规定的冲突之处，你自己按"设计文档为准"来裁决，并记录裁决。
4. 不要进入 `finishing-a-development-branch`。当最终整分支评审通过时，转入阶段 4。

## 阶段 4：收尾

1. 对照设计 Validation 一节收集验证证据：SDD 台账、提交区间、测试输出、评审结论。
2. 在改动基线事实之前，确认实现已落地到主工作区：worktree 分支已在本地合并、某个 commit/PR 已包含该代码，或用户明确确认代码在可达工作区之外且已落地。仅仅一个通过的 worktree 分支本身不算落地证据。
3. 若代码尚未落地，停在"已实现"收尾之前：让设计保持 `status: accepted`，不更新模块/架构基线，不记录 PM 完成，并交付一份待合并报告，附上供用户执行的确切 merge/push/PR 命令。
4. 有了落地证据之后，更新模块/架构基线并重新渲染受影响的图（见 `modular-architecture` 的 Baseline Update）。
5. 把设计标记为 `status: implemented`。
6. 通过 `modular-status` 带证据记录 PM 完成。
7. 运行 modular-audit 的确定性检查器作为漂移自查；把发现并入报告。
8. 交付最终报告。

当 PM 目录位于代码仓库内部时，所有模块化文档更新（基线、PM、设计状态）都要在实现已落地到主工作区之后、于主工作区中进行——绝不在 worktree 里做，否则它们会搁浅在一个未合并的分支上。

## 硬停止

只有两种情况会暂停自主区并返回用户：

1. SDD 报告 BLOCKED，且三种补救全部失败：补充上下文、换更强的模型、拆分任务。
2. 执行中发现的事实推翻了接单评审的结论（例如代码严重与模块文档矛盾）。这说明接单评审漏掉了什么——停下，而不是硬推过去。

无论其他情况如何：绝不 push、绝不创建 PR、绝不销毁 worktree 之外的数据。

## 决策日志

每一次自主裁决，向 `.superpowers/sdd/decision-log.md`（与 SDD 进度台账同目录）追加一行：

```text
<ISO-8601 time> | <decision> | <reason>
```

至少记录：计划的自我批准、每一次计划所规定的冲突裁决、每一次 Minor 发现的延后处理。

`.superpowers/sdd/` 是随 worktree 一起消亡的临时草稿。在收尾时，把决策日志复制到归档计划旁边（例如 `architecture/plans/archive/<YYYY-MM-DD>-<change>-decisions.md`），这样问责记录能在 worktree 清理后留存。

## 最终报告

按顺序交付以下各节：

1. **成果与证据**——落地了什么、提交区间、测试输出、最终评审结论。
2. **代你所做的决策**——决策日志摘要，每条附上其理由，用于事后问责。
3. **对设计的偏离**——每一处偏离及其处理方式。
4. **遗留项**——Minor 发现、风险、建议的后续跟进。
5. **推荐动作**——供用户执行的确切 merge/push/PR 命令。
