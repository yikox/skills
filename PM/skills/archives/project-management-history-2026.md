# Project Management History 2026

Source: project-management.md
Compressed on: 2026-07-08

以下为压缩时自主文件原样移入的历史细节（验证记录与长更新条目）。此后新工作遵循 pm-maintenance-rules「证据单一居所」，证据直接写入设计文档，本文件仅存放规则生效前的存量。

## Testing and Validation（原节全文）

- 确定性检查（en 版 checker，须豁免 zh 镜像）：`python3 en/modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**' --exclude 'zh/**'` 退出码 0。
- check_plans fixture 验证：坏计划（缺 source_design / level 非法 / 越界路径 / 目录级别不匹配）全部拦截，正例与归档件静默。
- 2026-07-03 审计跟进修复验证：`python3 -m unittest discover -s modular-programming/modular-audit/tests`、`python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'`、三个 Python 脚本 py_compile、架构图渲染、`./install.sh --dry-run`、`git diff --check` 全部通过。
- 2026-07-04 轻量默认工作流验证：`python3 -m unittest discover -s modular-programming/modular-audit/tests`、`python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'`、三个 Python 脚本 py_compile、高级架构图渲染、`./install.sh --dry-run`、`git diff --check` 全部通过。
- 2026-07-04 vocab 单一事实源 + 拆分验证：checker 0 error/0 warning；unittest 10 tests OK（含 3 个新 vocab drift-guard）；三脚本 py_compile；图重渲染含新 `audit-checker reads shared-references` 边；`./install.sh --dry-run` 覆盖 vocab.md 与 module-kinds/；`git diff --check` 干净；9 个 kind 分片与原文逐行 diff 零漂移；主动破坏 vocab.md（删 `composite`）触发 drift-guard 测试失败、还原后恢复。
- 2026-07-05 中英双语结构层验证（L2）：`git mv modular-programming en/modular-programming`（82 rename，历史保留）+ `cp` 生成 zh 骨架；install.sh 加语言参数——`./install.sh`（缺 lang）与 `./install.sh fr`（非法）退出码 2，`./install.sh en/zh --dry-run` 各 10 技能 + `_shared` 退出码 0；en 版 checker 自审计（`--exclude 'zh/**'`）0 error/0 warning，6 模块；unittest 10 OK；zh 三脚本 py_compile OK；`git diff --check` 干净。（结构层 commit 7cf18d3）
- 2026-07-05/06 zh 翻译 + token 完整性验证（L2）：6 个并行 subagent 译 39 文件；机器 token 无中文污染（grep module_form/module_kind/status/level/relation_* 等含 CJK 为空）；vocab.md 及全部 `*.py`/`*.arch.json` 在 en/zh 逐字一致；`./install.sh zh --dry-run` 10 技能；`render_modular_graph.py` 渲染 zh system-overview.arch.json 成功；en 版 checker 自审计 0/0；`git diff --check` 干净。（翻译 commit 03d55f3）

## Archive Completed Work 证据原文（压缩前）

- 2026-07-05 narrator + advisor 改名：narrator：设计 `architecture/modules/workflow-skills/changes/2026-07-05-modular-narrator.md`（2026-07-07 自 docs/superpowers/ 迁入）+ 计划 commit 22459ea + 实现 a537db2 + README 三处注册 7723924 + 路由表 e6d3ac8；改名 commit 265aa52；基线（workflow-skills 十技能 + narrator/advisor 划界、main-design Module Map）于 2026-07-07 审计补录。
- 2026-07-04 词表单一事实源 vocab.md（评估痛点 1，L3）：新增 `_shared/references/vocab.md`；checker `load_vocab()` 清单驱动 + fallback；5 处散文改为引用；audit-checker↔shared-references 新增 reads 边（module docs + 图 + 重渲染）；main-design/shared-references 退役"手工同步词表"约束；新增 3 个 drift-guard 单测（含 vocab.md 与内置 fallback 一致性断言）；checker 0/0、unittest 10 OK、render/install dry-run/diff-check 通过；主动破坏 vocab.md 一致性被测试拦截。
- 2026-07-04 拆分 module-kind-classification（评估痛点 3，L2）：917→319 行；9 类 kind 逐字搬到 `module-kinds/<kind>.md`（逐行 diff 证明零漂移）；主文件保留为索引；4 处引用无锚点、契约兼容；shared-references baseline 已记 module-kinds/。
- 2026-07-04 新增高级角色 modular-architect + 方法论/评估共享参考（L3）：autopilot 托管执行；SDD 四任务全绿 + 终审 Ready to merge；merge 22c98e8；baseline（main-design/workflow-skills/shared-references）已更新；checker 0 error、unittest OK、install dry-run 见新技能；决策日志见 plans/archive/2026-07-04-modular-architect-decisions.md。
- 2026-07-04 轻量默认模块化工作流改造（L3）：共享规则、技能入口、模板、README、checker 与 PM baseline 已更新；最终验证见上方 Testing and Validation。
- 2026-07-03 审计跟进修复：新增 checker unittest；modular-audit 0 error/0 warning；py_compile、架构图渲染、install dry-run、diff-check 通过；实际安装因审批额度限制未执行。
- 2026-07-03 modular-autopilot 监督者技能（L3）：commits 7e55bf5..fa0b54b + e128077 收尾 + 77b70c2 加固；SDD 每任务双评审 + 最终全分支评审 Ready to merge；checker fixture 全绿。

## Recent Updates 长条目原文（压缩前）

- 2026-07-08 - 文档减重：modular-advisor 评估（`docs/modularization/2026-07-08-assessment.md`）→ L2"证据单一居所 + 记账面减重"经评审、接受并实现（en/zh 各 5 文件，先 zh 后 en）；下一步按新规则做 PM 一次性压缩。
- 2026-07-06 - 中英双语翻译落地：6 个并行 subagent 完成 zh 散文中文化（39 文件），token 完整性验证全绿（机器 token 无污染、`*.py`/`*.arch.json`/vocab en-zh 逐字一致）；设计 implemented（commit 03d55f3）。发现：en/ 实为中英混合（历史 docs-language=zh），非纯英文源——若要 en/ 纯英文化列后续 backlog。install 实际同步仍待运行（权限）。
- 2026-07-05 - 中英双语版本（L2，主模块 installer）：目录改为 `<lang>/modular-programming/`（en 源/主、zh 镜像），install.sh 加必填语言参数（zh|en），README 补 README_EN 并双向链接，baseline（main-design Scope/Shared Constraints、installer 契约、各模块 code_paths 加 en/ 前缀）已更新；结构层验证全绿。
- 2026-07-05 - 新增第 10 个技能 modular-narrator（项目讲述者：只读调查 + 通俗讲解，独立可用，与 advisor 以"理解 vs 提案"划界），设计/计划走 superpowers 流程，实现 commits 4cb8c34..e6d3ac8；同日 modular-architect 改名 modular-advisor（265aa52）。基线与 PM 记录于 2026-07-07 审计补录，设计/计划同日迁入 `architecture/modules/workflow-skills/`（changes/ 与 plans/archive/）。
- 2026-07-04 - modular-architect 评估本仓库（成熟度 High），据痛点 1/3 出两份变更设计并经 modular-review（补图更新步骤）→ 用户接受（设计 1 方案 A、不补 ADR）→ 落地：vocab.md 单一事实源（L3，checker 清单驱动 + fallback + drift-guard 测试）与 module-kind-classification 拆分（L2，索引 + module-kinds/ 分片）；checker 0/0、unittest 10 OK、render/install dry-run/diff-check 通过；install 同步待运行。
- 2026-07-04 - 新增第 9 个技能 modular-architect（模块化架构师，高级顾问角色，只提案不实现）+ modular-methodology/modular-assessment 两个共享参考；autopilot 托管执行 SDD 四任务全绿，merge 22c98e8，baseline 与 PM 已同步。
- 2026-07-04 - 评审后修复：checker 例外 glob（shared/ignored_paths）加幽灵检查、v0.3 结构校验对 v0.1/v0.2 老图降级为 warning；audit SKILL/Routing Quick Reference/module-authoring-rules 补齐"图可选、L1 减重"漏改；验证 `python3 -m unittest discover -s modular-programming/modular-audit/tests`（7 tests OK）与自审计 0 error/0 warning。
- 2026-07-04 - 落地轻量默认模块化工作流：L1 PM 减重、诊断模式、硬化 L1/L2/L3、图降为高级可视化、默认事实源改为 main-design + modules。
- 2026-07-03 - 修复审计发现：autopilot 未落地不标 implemented、README/AI snippet/openai.yaml 补齐 8 技能曝光、audit-checker 增加 group/interface/scope 校验与 unittest；安装同步待审批可用后运行。
- 2026-07-03 - modular-autopilot 技能合入 main；check_plans 加固（路径越界、目录级别匹配）。
- 2026-07-03 - 初始化本仓库 modular 项目记忆（模块地图 6 模块、图、PM、知识文档）。
