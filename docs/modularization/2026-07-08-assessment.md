# 文档体系减重评估（2026-07-08）

评估对象：本仓库模块化工作流的文档产出（PM/skills/**）与产生它们的规则/模板（shared-references、shared-assets）。
性质：证据快照，非基线事实。评估人：modular-advisor。

## 结论

- 流程规则层已是轻量设计（L1 默认不进 Active Tasks、图可选、诊断模式、pm-maintenance-rules 有压缩规则），**不重**。`verified`
- 重在 PM 主文件的"重复记账"：同一事实最多出现在 5 个节；且自家压缩规则的触发条件已满足但从未执行。`verified`
- 模块文档与变更设计文档信息密度高、契约具体，不属"空话"，无需减重。`verified`

## 证据

1. `PM/skills/project-management.md`（121 行）中"中英双语"一事出现在 Active Tasks（done 未归档）、Design Index、Testing and Validation（两大段）、Recent Updates（两条）、Current Status 共 5 处；完整证据本已在 `architecture/modules/installer/changes/2026-07-05-bilingual-zh-en.md` 的 Implementation/Validation 节。
2. Testing and Validation 节（L63-71）为 5 条几乎同款的验证命令清单——`pm-maintenance-rules.md` 明确将"repeated CI/build/release procedure notes"列为应移出项。
3. Archive Evidence 单元格为段落级，复述设计文档 Implementation 节；"implemented in source; install pending" 重复 6 次。
4. Modular Design Index 14 行全为 implemented/reviewed——按规则应移入 Design Archive，索引只留基线与活跃件。
5. 基线文档（6 个 modules/*.md + main-design.md）末尾 Review Notes 节与 front matter `review_status` 完全同义（checker 仅校验 front matter，`check_modular_project.py:96,192`）；变更设计中的 Review Notes 则承载真实评审结论，性质不同。
6. Roadmap 与 Requirements Backlog 记同一 REQ；Milestones 唯一一行与 Archive 重复。
7. `docs/superpowers/` 残留约 390 行已被迁移内容的前身文件。

## 根因

`pm-maintenance-rules.md` 只定义了"何时压缩"（事后），未定义"写入时证据的单一居所"（事前）；PM 模板提供了过多平行记账面（Testing and Validation / Roadmap / Milestones / Evidence 段落列），引导每次收尾时把同一证据抄写多处。

## 修复路径（用户已确认顺序：先 2 后 1）

1. 一次性压缩：按现行 pm-maintenance-rules 执行（modular-status / modular-audit）。
2. 根因修复（L2，proposed）：见 `PM/skills/architecture/modules/shared-references/changes/2026-07-08-evidence-single-home.md`。
