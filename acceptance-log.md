# living-docs 验收日志

<!-- docs-acceptance 追加式记录。对套件本身的修改,唯一合法输入是本日志。 -->

## 2026-07-09 docs-sync(本仓库 v1→v2 一次性迁移)— 全过,待用户整体验收

- 清单:6 通过 / 0 存疑
  1. 漂移清单与 diff 相符:三分支实测——对齐(exit 0)、DRIFT(改 docs-sync/SKILL.md 后点名 living-docs-suite,exit 1)、ORPHAN(orphan-test.txt 被点名,exit 1)。
  2. .last-sync == 迁移完成时 HEAD(f447354);其后仅记账文件(PM/**,在 ignored_paths)变更。
  3. 漂移模块结论明确:迁移重建了全部 4 份模块文档 + main-design(v1 的 6 模块地图随冻结整体替换)。
  4. 证据可追溯:v1 记账文档以 v1- 前缀移入 archives/(project-management、knowledge-summary、v1-baseline/),commit 链完整保留在 project.md 变更日志。
  5. 耗时:迁移 + 验证约 8 分钟,达标。
  6. project.md 四章合规:当前焦点 2 行、变更日志一条一行、知识按主题四小节。
- 用户结论:**待定**——用户要求整体验收,本条留待其确认后补记。
- 备注:与设计文档的一处偏差已记录(无 _shared 层,skill 自包含;原因:installer 平铺布局 + _shared 在清理列表)。计数规则:本条在用户确认前不计入"连续 5 次全过"。
